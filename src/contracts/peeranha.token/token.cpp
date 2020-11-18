#include "token.hpp"
#include "economy.hpp"

namespace eosio {

void token::create(name issuer, asset maximum_supply) {
  require_auth(_self);
  auto sym = maximum_supply.symbol;
  eosio::check(sym.is_valid(), "invalid symbol name");
  eosio::check(maximum_supply.is_valid(), "invalid supply");
  eosio::check(maximum_supply.amount > 0, "max-supply must be positive");
  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  eosio::check(existing == statstable.end(),
               "token with symbol already exists");

  statstable.emplace(_self, [&](auto &s) {
    s.supply.symbol = maximum_supply.symbol;
    s.max_supply = maximum_supply;
    s.user_supply.symbol = maximum_supply.symbol;
    s.user_max_supply = maximum_supply * USER_SHARES / 100;
    s.funding_supply.symbol = maximum_supply.symbol;
    s.funding_max_supply = maximum_supply * (100 - USER_SHARES) / 100;
    s.issuer = issuer;
  });
}

void token::issue(name to, asset quantity, string memo) {
  auto sym = quantity.symbol;
  eosio::check(sym.is_valid(), "invalid symbol name");
  eosio::check(memo.size() <= 256, "memo has more than 256 bytes");

  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  eosio::check(existing != statstable.end(),
               "token with symbol does not exist, create token before issue");
  const auto &st = *existing;

  require_auth(st.issuer);
  eosio::check(quantity.is_valid(), "invalid quantity");
  eosio::check(quantity.amount > 0, "must issue positive quantity");

  eosio::check(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");
  eosio::check(quantity.amount <=
                   st.funding_max_supply.amount - st.funding_supply.amount,
               "quantity exceeds available supply");

  statstable.modify(st, same_payer, [&quantity](auto &s) {
    s.supply += quantity;
    s.funding_supply += quantity;
  });

  add_balance(st.issuer, quantity, st.issuer);

  if (to != st.issuer) {
    SEND_INLINE_ACTION(*this, transfer, {{st.issuer, "active"_n}},
                       {st.issuer, to, quantity, memo});
  }
}

void token::retire(asset quantity, string memo) {
  auto sym = quantity.symbol;
  eosio::check(sym.is_valid(), "invalid symbol name");
  eosio::check(memo.size() <= 256, "memo has more than 256 bytes");

  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  eosio::check(existing != statstable.end(),
               "token with symbol does not exist");
  const auto &st = *existing;

  require_auth(st.issuer);
  eosio::check(quantity.is_valid(), "invalid quantity");
  eosio::check(quantity.amount > 0, "must retire positive quantity");

  eosio::check(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");

  statstable.modify(st, same_payer,
                    [&](auto &s) { s.funding_supply -= quantity; });

  sub_balance(st.issuer, quantity);
}

void token::transfer(name from, name to, asset quantity, string memo) {
  eosio::check(from != to, "cannot transfer to self");
  require_auth(from);
  eosio::check(is_account(to), "to account does not exist");
  auto sym = quantity.symbol.code();
  stats statstable(_self, sym.raw());
  const auto &st = statstable.get(sym.raw());

  require_recipient(from);
  require_recipient(to);

  eosio::check(quantity.is_valid(), "invalid quantity");
  eosio::check(quantity.amount > 0, "must transfer positive quantity");
  eosio::check(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");
  eosio::check(memo.size() <= 256, "memo has more than 256 bytes");

  auto payer = has_auth(to) ? to : from;

  sub_balance(from, quantity);
  add_balance(to, quantity, payer);
}

void token::sub_balance(name user, asset value) {
  accounts from_acnts(_self, user.value);

  const auto &from =
      from_acnts.get(value.symbol.code().raw(), "no balance object found");
  eosio::check(from.balance.amount >= value.amount, "overdrawn balance");

  from_acnts.modify(from, user, [&](auto &a) { a.balance -= value; });
}

void token::add_balance(name user, asset value, name ram_payer) {
  accounts to_acnts(_self, user.value);
  auto to = to_acnts.find(value.symbol.code().raw());
  if (to == to_acnts.end()) {
    to_acnts.emplace(ram_payer, [&](auto &a) { a.balance = value; });
  } else {
    to_acnts.modify(to, same_payer, [&](auto &a) { a.balance += value; });
  }
}

void token::open(name user, const symbol &symbol, name ram_payer) {
  require_auth(ram_payer);

  auto sym_code_raw = symbol.code().raw();

  stats statstable(_self, sym_code_raw);
  const auto &st = statstable.get(sym_code_raw, "symbol does not exist");
  eosio::check(st.supply.symbol == symbol, "symbol precision mismatch");

  accounts acnts(_self, user.value);
  auto it = acnts.find(sym_code_raw);
  if (it == acnts.end()) {
    acnts.emplace(ram_payer, [&](auto &a) { a.balance = asset{0, symbol}; });
  }
}

void token::close(name user, const symbol &symbol) {
  require_auth(user);
  accounts acnts(_self, user.value);
  auto it = acnts.find(symbol.code().raw());
  eosio::check(it != acnts.end(),
               "Balance row already deleted or never existed. Action won't "
               "have any effect.");
  eosio::check(it->balance.amount == 0,
               "Cannot close because the balance is not zero.");
  acnts.erase(it);
}

asset token::create_reward_pool(uint16_t period, int total_rating) {
  const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
  stats statstable(_self, sym.code().raw());
  auto st = statstable.find(sym.code().raw());
  int64_t inflation_reward_pool = int64_to_peer(START_POOL);
  for (int inflation_period = 0; inflation_period < period / INFLATION_PERIOD;
       ++inflation_period) {
    inflation_reward_pool *= POOL_REDUSE_COEFFICIENT;
  }
  int64_t reward_pool = int64_to_peer(total_rating * RATING_TOKEN_COEFFICIENT);
  if (reward_pool > inflation_reward_pool) {
    reward_pool = inflation_reward_pool;
  }
  const int64_t remaining_user_supply =
      st->user_max_supply.amount - st->user_supply.amount;
  if (reward_pool > remaining_user_supply) {
    reward_pool = remaining_user_supply;
  }
  auto quantity = asset(reward_pool, sym);
  statstable.modify(st, _self, [&quantity](auto &s) {
    s.supply += quantity;
    s.user_supply += quantity;
  });
  return quantity;
}

asset token::get_user_reward(asset total_reward, int rating_to_reward,
                             int total_rating) {
  return total_reward * rating_to_reward / total_rating;
}

void token::pickupreward(name user, const uint16_t period) {
  require_auth(user);
  time current_time = now();
  eosio::check(get_period(current_time) > period, "This period isn't ended yet!");

  period_reward_index period_reward_table(_self, user.value);
  // Ensure that there is no records in period_reward_table for this period,
  // it means user isn't pickup reward yet
  eosio::check(period_reward_table.find(period) == period_reward_table.end(),
               "You already pick up this reward");
  total_rating_index total_rating_table(peeranha_main, scope_all_periods);
  auto iter_total_rating = total_rating_table.find(period);
  int total_rating_to_reward = iter_total_rating == total_rating_table.end()
                                   ? 0
                                   : iter_total_rating->total_rating_to_reward;

  total_reward_index total_reward_table(_self, scope_all_periods);
  auto iter_total_reward = total_reward_table.find(period);
  // Create reward pool
  if (iter_total_reward == total_reward_table.end()) {
    auto quantity = create_reward_pool(period, total_rating_to_reward);
    iter_total_reward = total_reward_table.emplace(
        _self, [&quantity, period](auto &total_reward_item) {
          total_reward_item.period = period;
          total_reward_item.total_reward = quantity;
        });
  }
  period_rating_index period_rating_table(peeranha_main, user.value);
  auto period_rating = period_rating_table.find(period);
  eosio::check(period_rating != period_rating_table.end(),
               "No reward for you in this period");
  asset user_reward =
      get_user_reward(iter_total_reward->total_reward,
                      period_rating->rating_to_award, total_rating_to_reward);
  period_reward_table.emplace(user, [user_reward, period](auto &reward) {
    reward.period = period;
    reward.reward = user_reward;
  });
  add_balance(user, user_reward, user);
}

void token::inviteuser(name inviter, name invited_user) {
  require_auth(invited_user);

  account_index account_table(peeranha_main, scope_all_accounts);
  auto iter_account_invited_user = account_table.find(invited_user.value);

  eosio::check(iter_account_invited_user == account_table.end(),
               "Invited user already registred");

  auto iter_account_inviter = account_table.find(inviter.value);
  eosio::check(iter_account_inviter != account_table.end(),
               "Inviter isn't registed");

  //eosio::check(inviter != invited_user, "Can't invite self");

  invited_users_index invited_users_table(_self, all_invited);
  auto iter_invited_user = invited_users_table.find(invited_user.value);
  eosio::check(iter_invited_user == invited_users_table.end(),
               "This user already invited");

  const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);

  invited_users_table.emplace(
      _self, [inviter, invited_user, sym](auto &inviter_invited_user) {
        inviter_invited_user.inviter = inviter;
        inviter_invited_user.invited_user = invited_user;
        inviter_invited_user.common_reward.symbol = sym;
      });
}

void token::rewardrefer(name invited_user) {
  require_auth(invited_user);
  invited_users_index invited_users_table(_self, all_invited);
  auto iter_invited_user = invited_users_table.find(invited_user.value);
  eosio::check(iter_invited_user != invited_users_table.end(),
               "This user isn't invited");
  eosio::check(iter_invited_user->common_reward.amount == 0,
               "This users already rewarded");

  const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
  auto quantity = asset(int64_to_peer(REFERAL_REWARD), sym);
  stats statstable(_self, sym.code().raw());

  auto existing = statstable.find(sym.code().raw());
  eosio::check(existing != statstable.end(),
               "token with symbol does not exist, create token before issue");
  const auto &st = *existing;

  eosio::check(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");
  eosio::check(
      quantity.amount <= st.user_max_supply.amount - st.user_supply.amount,
      "quantity exceeds available supply");

  account_index account_table(peeranha_main, scope_all_accounts);
  auto iter_account_invited_user = account_table.find(invited_user.value);

  eosio::check(
      iter_account_invited_user->pay_out_rating >= REFERAL_TARGET_RATING_REACHED,
      "Invited user douesn't reached required rating");


  statstable.modify(st, _self, [&quantity](auto &s) {
    s.supply += quantity;
    s.user_supply += quantity;
  });
  
  invited_users_table.modify(iter_invited_user, _self,
                             [quantity](auto &inviter_invited_user) {
                               inviter_invited_user.common_reward = quantity;
                             });

  auto inviter_supply = quantity * REFERAL_SPLIT_COEFFICIENT / 100;

  add_balance(iter_invited_user->inviter, inviter_supply, _self);
  add_balance(invited_user, quantity - inviter_supply, _self);
}

#if STAGE == 1 || STAGE == 2

void token::resettables(std::vector<eosio::name> allaccs) {
  require_auth(_self);
  for (auto iter_acc = allaccs.begin(); iter_acc != allaccs.end(); iter_acc++) {
    accounts to_acnts(_self, iter_acc->value);
    auto iter_to_acnts = to_acnts.begin();
    while (iter_to_acnts != to_acnts.end()) {
      iter_to_acnts = to_acnts.erase(iter_to_acnts);
    }
    period_reward_index period_reward_table(_self, iter_acc->value);
    auto iter_period_reward = period_reward_table.begin();
    while (iter_period_reward != period_reward_table.end()) {
      iter_period_reward = period_reward_table.erase(iter_period_reward);
    }
  }

  const symbol sym = symbol("PEER", TOKEN_PRECISION);
  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  if (existing != statstable.end())
    statstable.erase(existing);

  total_reward_index total_reward_table(_self, scope_all_periods);
  auto iter_total_reward = total_reward_table.begin();
  while (iter_total_reward != total_reward_table.end()) {
    iter_total_reward = total_reward_table.erase(iter_total_reward);
  }

  invited_users_index invited_users_table(_self, all_invited);
  auto iter_invited_user = invited_users_table.begin();
  while (iter_invited_user != invited_users_table.end()) {
    iter_invited_user = invited_users_table.erase(iter_invited_user);
  }
#if STAGE == 2
  auto dbginfl_table = dbginfl_index(_self, _self.value);
  auto iter_dbginf_table = dbginfl_table.begin();
  while (iter_dbginf_table != dbginfl_table.end()) {
    iter_dbginf_table = dbginfl_table.erase(iter_dbginf_table);
  }
#endif
};
#endif

}  // namespace eosio

EOSIO_DISPATCH(eosio::token,
               (create)(issue)(transfer)(open)(close)(retire)(pickupreward)(inviteuser)(rewardrefer)
#if STAGE == 1 || STAGE == 2
                   (resettables)
#if STAGE == 2
                       (mapcrrwpool)
#endif

#endif 
                      (payforcpu))
