#include "peerania.token.hpp"

namespace eosio {

void token::create(name issuer, asset maximum_supply) {
  require_auth(_self);

  auto sym = maximum_supply.symbol;
  eosio_assert(sym.is_valid(), "invalid symbol name");
  eosio_assert(maximum_supply.is_valid(), "invalid supply");
  eosio_assert(maximum_supply.amount > 0, "max-supply must be positive");
  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  eosio_assert(existing == statstable.end(),
               "token with symbol already exists");

  statstable.emplace(_self, [&](auto& s) {
    s.supply.symbol = maximum_supply.symbol;
    s.max_supply = maximum_supply;
    s.issuer = issuer;
  });
}

void token::issue(name to, asset quantity, string memo) {
  auto sym = quantity.symbol;
  eosio_assert(sym.is_valid(), "invalid symbol name");
  eosio_assert(memo.size() <= 256, "memo has more than 256 bytes");

  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  eosio_assert(existing != statstable.end(),
               "token with symbol does not exist, create token before issue");
  const auto& st = *existing;

  require_auth(st.issuer);
  eosio_assert(quantity.is_valid(), "invalid quantity");
  eosio_assert(quantity.amount > 0, "must issue positive quantity");

  eosio_assert(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");
  eosio_assert(quantity.amount <= st.max_supply.amount - st.supply.amount,
               "quantity exceeds available supply");

  statstable.modify(st, same_payer, [&](auto& s) { s.supply += quantity; });

  add_balance(st.issuer, quantity, st.issuer);

  if (to != st.issuer) {
    SEND_INLINE_ACTION(*this, transfer, {{st.issuer, "active"_n}},
                       {st.issuer, to, quantity, memo});
  }
}

void token::retire(asset quantity, string memo) {
  auto sym = quantity.symbol;
  eosio_assert(sym.is_valid(), "invalid symbol name");
  eosio_assert(memo.size() <= 256, "memo has more than 256 bytes");

  stats statstable(_self, sym.code().raw());
  auto existing = statstable.find(sym.code().raw());
  eosio_assert(existing != statstable.end(),
               "token with symbol does not exist");
  const auto& st = *existing;

  require_auth(st.issuer);
  eosio_assert(quantity.is_valid(), "invalid quantity");
  eosio_assert(quantity.amount > 0, "must retire positive quantity");

  eosio_assert(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");

  statstable.modify(st, same_payer, [&](auto& s) { s.supply -= quantity; });

  sub_balance(st.issuer, quantity);
}

void token::transfer(name from, name to, asset quantity, string memo) {
  eosio_assert(from != to, "cannot transfer to self");
  require_auth(from);
  eosio_assert(is_account(to), "to account does not exist");
  auto sym = quantity.symbol.code();
  stats statstable(_self, sym.raw());
  const auto& st = statstable.get(sym.raw());

  require_recipient(from);
  require_recipient(to);

  eosio_assert(quantity.is_valid(), "invalid quantity");
  eosio_assert(quantity.amount > 0, "must transfer positive quantity");
  eosio_assert(quantity.symbol == st.supply.symbol,
               "symbol precision mismatch");
  eosio_assert(memo.size() <= 256, "memo has more than 256 bytes");

  auto payer = has_auth(to) ? to : from;

  sub_balance(from, quantity);
  add_balance(to, quantity, payer);
}

void token::sub_balance(name user, asset value) {
  accounts from_acnts(_self, user.value);

  const auto& from =
      from_acnts.get(value.symbol.code().raw(), "no balance object found");
  eosio_assert(from.balance.amount >= value.amount, "overdrawn balance");

  from_acnts.modify(from, user, [&](auto& a) { a.balance -= value; });
}

void token::add_balance(name user, asset value, name ram_payer) {
  accounts to_acnts(_self, user.value);
  auto to = to_acnts.find(value.symbol.code().raw());
  if (to == to_acnts.end()) {
    to_acnts.emplace(ram_payer, [&](auto& a) { a.balance = value; });
  } else {
    to_acnts.modify(to, same_payer, [&](auto& a) { a.balance += value; });
  }
}

void token::open(name user, const symbol& symbol, name ram_payer) {
  require_auth(ram_payer);

  auto sym_code_raw = symbol.code().raw();

  stats statstable(_self, sym_code_raw);
  const auto& st = statstable.get(sym_code_raw, "symbol does not exist");
  eosio_assert(st.supply.symbol == symbol, "symbol precision mismatch");

  accounts acnts(_self, user.value);
  auto it = acnts.find(sym_code_raw);
  if (it == acnts.end()) {
    acnts.emplace(ram_payer, [&](auto& a) { a.balance = asset{0, symbol}; });
  }
}

void token::close(name user, const symbol& symbol) {
  require_auth(user);
  accounts acnts(_self, user.value);
  auto it = acnts.find(symbol.code().raw());
  eosio_assert(it != acnts.end(),
               "Balance row already deleted or never existed. Action won't "
               "have any effect.");
  eosio_assert(it->balance.amount == 0,
               "Cannot close because the balance is not zero.");
  acnts.erase(it);
}

asset get_inflation(uint16_t period){
    const symbol sym = symbol("PEER", 6);
    int64_t reward_pool = 1000000ULL*(START_POOL - (period/INFLATION_PERIOD) * POOL_REDUSE);
    if (reward_pool < 0) reward_pool = 0;
    return asset(reward_pool, sym);
}

asset get_reward(asset total_reward, int rating_to_reward, int total_rating){
  return total_reward * rating_to_reward / total_rating;
}

void token::pickupreward(name user, const uint16_t period) {
  require_auth(user);
  time current_time = now();
  eosio_assert(get_period(current_time) > period,
               "This period isn't ended yet!");
  period_reward_index period_reward_table(_self, user.value);
  eosio_assert(period_reward_table.find(period) == period_reward_table.end(),
               "You already pick up this reward");

  total_reward_index total_reward_table(_self, scope_all_periods);
  auto iter_total_reward = total_reward_table.find(period);
  if (iter_total_reward == total_reward_table.end()) {
    asset quantity = get_inflation(period);
    const symbol sym = quantity.symbol;
    stats statstable(_self, sym.code().raw());
    auto existing = statstable.find(sym.code().raw());
    const auto& st = *existing;
    statstable.modify(st, _self, [&](auto& s) { s.supply += quantity; });
    add_balance(peerania_main, quantity, _self);
    iter_total_reward = total_reward_table.emplace(_self, [&quantity, period](auto &total_reward_item){
      total_reward_item.period = period;
      total_reward_item.total_reward = quantity;
    });
  }

  period_rating_index period_rating_table(peerania_main, user.value);
  auto period_rating = period_rating_table.find(period);
  eosio_assert(period_rating != period_rating_table.end(), "No reward for you in this period");

  total_rating_index total_rating_table(peerania_main, scope_all_periods);
  auto total_rating = total_rating_table.find(period);
  eosio_assert(total_rating != total_rating_table.end(), "Fatal internal error");

  asset user_reward = get_reward(iter_total_reward->total_reward, period_rating->rating_to_award, total_rating->total_rating_to_reward);
  period_reward_table.emplace(user, [user_reward, period](auto &reward){
    reward.period = period;
    reward.reward = user_reward;
  });
  // Subbalance
  accounts from_acnts(_self, peerania_main.value);
  const auto& from = from_acnts.get(user_reward.symbol.code().raw(), "no balance object found");
  eosio_assert(from.balance.amount >= user_reward.amount, "overdrawn balance");

  from_acnts.modify(from, user, [&](auto& a) { a.balance -= user_reward; });

  add_balance(user, user_reward, user);
}

}  // namespace eosio

EOSIO_DISPATCH(eosio::token,
               (create)(issue)(transfer)(open)(close)(retire)(pickupreward))