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
  add_balance(to, quantity, _self);
}

void token::sub_balance(name user, asset value) {
  accounts from_acnts(_self, user.value);

  const auto &from =
      from_acnts.get(value.symbol.code().raw(), "no balance object found");
  eosio::check(from.balance.amount >= value.amount + getstakedbalance(user), "overdrawn balance");

  from_acnts.modify(from, _self, [&](auto &a) { a.balance -= value; });
}

void token::add_balance(name user, asset value, name ram_payer) {
  accounts to_acnts(_self, user.value);
  auto to = to_acnts.find(value.symbol.code().raw());
  if (to == to_acnts.end()) {
    to_acnts.emplace(ram_payer, [&](auto &a) { a.balance = value; });
  } else {
    to_acnts.modify(to, _self, [&](auto &a) { a.balance += value; });
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
  if (reward_pool > inflation_reward_pool * MULTIPLICATION_TOTAL_RATING) {
    reward_pool = inflation_reward_pool * MULTIPLICATION_TOTAL_RATING;
  }
  const int64_t remaining_user_supply =
      st->user_max_supply.amount - st->user_supply.amount;
  if (reward_pool > remaining_user_supply * MULTIPLICATION_TOTAL_RATING) {
    reward_pool = remaining_user_supply * MULTIPLICATION_TOTAL_RATING;
  }
  auto quantity = asset(reward_pool, sym);
  quantity.amount /= MULTIPLICATION_TOTAL_RATING;
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
  int64_t boost = getboost(user, period - 1);
  asset user_reward =
      get_user_reward(iter_total_reward->total_reward,
                      period_rating->rating_to_award * boost, total_rating_to_reward);
  auto prom_quantity = get_award(period_rating->rating_to_award * boost, total_rating_to_reward, period);
  if (prom_quantity.amount) {
    sub_balance(user_prom_leave, prom_quantity);
    user_reward += prom_quantity;
  }
  period_reward_table.emplace(user, [user_reward, period](auto &reward) {
    reward.period = period;
    reward.reward = user_reward;
  });
  add_balance(user, user_reward, _self);
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

void token::addboost(name user, asset tokens) {
  require_auth(user);
  boost_index boost_table(_self, user.value);
  const uint16_t next_period = get_period(now()) + 1;
  auto iter_last_boost = boost_table.rbegin();

  accounts from_acnts(_self, user.value);
  const auto &from =
      from_acnts.get(tokens.symbol.code().raw(), "no balance object found");
  eosio::check(from.balance.amount >= tokens.amount, "overdrawn balance");
  eosio::check(tokens.amount >= 0, "boost must be positive ");

  asset change_boost = tokens;
  
  const bool is_first_boost_user = boost_table.rend() == boost_table.rbegin();

  auto iter_boost = boost_table.find(next_period);

  if (iter_boost == boost_table.end()) {
    if (!is_first_boost_user)
      change_boost = tokens - iter_last_boost->staked_tokens;
      
    auto iter_boost = boost_table.emplace(
      _self, [next_period, tokens](auto &boost) {
        boost.staked_tokens = tokens;
        boost.period = next_period;
      });
  } else {
    change_boost -= iter_boost->staked_tokens;
    boost_table.modify(
      iter_boost, _self, [tokens](auto &boost) {
        boost.staked_tokens = tokens;
      });
  }
  update_statistics_boost(change_boost, user);
}

void token::update_statistics_boost(asset tokens, name user) {
  statistics_boost_index statistics_boost_table(_self, scope_all_boost);
  const uint16_t next_period = get_period(now()) + 1;
  auto iter_last_statistics = statistics_boost_table.rbegin();

  const bool is_first_transaction = iter_last_statistics == statistics_boost_table.rend();
  if (is_first_transaction || iter_last_statistics->period != next_period) {
    asset new_tokens;
    asset max_stake;
    name user_max_stake;
    if (is_first_transaction) {
      new_tokens = tokens;
      max_stake = tokens;
      user_max_stake = user;
    } else {
      new_tokens = iter_last_statistics->sum_tokens + tokens;
      max_stake = iter_last_statistics->max_stake;
      user_max_stake = iter_last_statistics->user_max_stake;

      get_value_statistic_boost(tokens, max_stake, user_max_stake, user);
    }
    statistics_boost_table.emplace(
      _self, [new_tokens, next_period, max_stake, user_max_stake](auto &stat_boost) {
        stat_boost.sum_tokens = new_tokens;
        stat_boost.max_stake = max_stake;
        stat_boost.user_max_stake = user_max_stake;
        stat_boost.period = next_period;
      });
  } else {
    auto iter_total_rating_change = statistics_boost_table.find(next_period);
    asset max_stake = iter_total_rating_change->max_stake;
    name user_max_stake = iter_total_rating_change->user_max_stake;

    get_value_statistic_boost(tokens, max_stake, user_max_stake, user);
 
    statistics_boost_table.modify(
      iter_total_rating_change, _self, [tokens, max_stake, user_max_stake](auto &stat_boost) {
        stat_boost.sum_tokens += tokens;
        stat_boost.max_stake = max_stake;
        stat_boost.user_max_stake = user_max_stake;
      });
  }
}

void token::get_value_statistic_boost(asset &tokens, asset &max_stake, name &user_max_stake, name user) {
  if (tokens.amount > 0) {
    boost_index boost_table(_self, user.value);
    auto iter_last_boost = boost_table.rbegin();
    if (iter_last_boost->staked_tokens.amount > max_stake.amount) {
    max_stake = iter_last_boost->staked_tokens;
      user_max_stake = user;
    }
  } else if (tokens.amount < 0 && user_max_stake == user) {
    const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
    max_stake = asset{0, sym};
    account_index account_table(peeranha_main, scope_all_accounts);
    for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
      boost_index boost_table(_self, iter_account->user.value);
      auto iter_last_boost = boost_table.rbegin();
      if (boost_table.begin() != boost_table.end() && iter_last_boost->staked_tokens.amount > max_stake.amount) {
        max_stake = iter_last_boost->staked_tokens;
        user_max_stake = iter_account->user;
      }
    }
  }
}

int64_t token::getstakedbalance(name user) {
  boost_index boost_table(_self, user.value);

  if (boost_table.begin() == boost_table.end()) {
    return 0;
  }

  auto iter_last_boost = boost_table.rbegin();
  uint16_t period = get_period(now());

  int64_t output_value = 0;
  if (iter_last_boost->period <= period) {
    output_value = iter_last_boost->staked_tokens.amount;
  } else {
    auto iter_buf_boost = iter_last_boost;
    
    ++iter_buf_boost;
    if (iter_buf_boost == boost_table.rend()) {                 // only 1 boost entry
      output_value =  iter_last_boost->staked_tokens.amount;
    } else {
      if (iter_last_boost->staked_tokens.amount > iter_buf_boost->staked_tokens.amount) {  // add boost
        output_value =  iter_last_boost->staked_tokens.amount;
      } else {                                                                            // reduced boost
        output_value =  iter_buf_boost->staked_tokens.amount;
      }
    }
  }
  
  return output_value;
}

uint64_t token::getvalboost(name user, uint64_t period) { ///???
  boost_index boost_table(_self, user.value);

  if (boost_table.begin() == boost_table.end()) {
    return 0;
  }

  auto iter_last_boost = boost_table.find(period);
  return iter_last_boost->staked_tokens.amount;
}

asset token::get_award(uint64_t rating_to_award, uint32_t total_rating_to_reward, uint64_t period) {
  token_awards_index token_awards_table(_self, scope_all_token_awards);
  const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
  auto iter_token_awards_table = token_awards_table.find(period);

  if (iter_token_awards_table == token_awards_table.end()) {
    const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
    return asset{0, sym};
  }

  uint64_t part_award = rating_to_award * 100 * 1000 / total_rating_to_reward;        // 1000 - for accuracy
  asset quantity = iter_token_awards_table->sum_token * part_award / (100 * 1000);    // 1000 - for accuracy
  return quantity;
}

void token::setbounty(name user, asset bounty, uint64_t question_id, uint64_t timestamp) {
    require_auth(user);
    question_bounty bounty_table(_self, scope_all_bounties);
    auto iter_bounty = bounty_table.find(question_id);
    eosio::check(iter_bounty == bounty_table.end(), "Bounty is already set for this question");
    eosio::check(bounty.is_valid(), "invalid quantity");
    eosio::check(bounty.amount > 0, "must transfer positive quantity");
    sub_balance(user, bounty);

    bounty_table.emplace(_self, [&](auto &a) {
        a.user = user;
        a.amount = bounty;
        a.question_id = question_id;
        a.status = BOUNTY_STATUS_ACTIVE;
        a.timestamp = timestamp;
    });
}

void token::editbounty(name user, asset bounty, uint64_t question_id, uint64_t timestamp) {
    require_auth(user);
    question_bounty bounty_table(_self, scope_all_bounties);
    auto iter_bounty = bounty_table.find(question_id);
    eosio::check(iter_bounty != bounty_table.end(), "Bounty not found!");
    eosio::check(iter_bounty->status == BOUNTY_STATUS_ACTIVE,
                            "Bounty have already been paid");
    question_index question_table(peeranha_main, scope_all_questions);
    auto iter_question = question_table.find(question_id);
    eosio::check(iter_question != question_table.end(), "Question not found!");
    eosio::check(iter_question->user == user, "You cannot modify this bounty");
    eosio::check(iter_bounty->amount < bounty, "New amount cannot be less than previous");
    asset diff_bounty = bounty - iter_bounty->amount;
    sub_balance(user, diff_bounty);
    bounty_table.modify(iter_bounty, _self, [&](auto &a) {
        a.amount = bounty;
        a.timestamp = timestamp;
    });
}

void token::paybounty(name user, uint64_t question_id, uint8_t on_delete) {
    require_auth(user);
    question_bounty bounty_table(_self, scope_all_bounties);
    auto iter_bounty = bounty_table.find(question_id);
    eosio::check(iter_bounty != bounty_table.end(), "Bounty not found!");
    eosio::check(iter_bounty->status == BOUNTY_STATUS_ACTIVE,
                        "You have already got your bounty");

    question_index question_table(peeranha_main, scope_all_questions);
    auto iter_question = question_table.find(question_id);
    eosio::check(iter_question != question_table.end(), "Question not found!");

    if (on_delete == 1 && iter_question->answers.empty()) {
        eosio::check(iter_question->user == user, "You can't get this bounty");
        add_balance(user, iter_bounty->amount, _self);
        bounty_table.modify(iter_bounty, _self, [&](auto &a) { a.status = BOUNTY_STATUS_PAID; });
    } else if (on_delete == 0) {
        eosio::check(iter_question->correct_answer_id != 0, "Correct answer is not chosen!");
        auto iter_answer = binary_find(iter_question->answers.begin(),
                                           iter_question->answers.end(), iter_question->correct_answer_id);
        eosio::check(iter_answer->user == user, "You can't get this bounty");
        add_balance(user, iter_bounty->amount, _self);
        bounty_table.modify(iter_bounty, _self, [&](auto &a) { a.status = BOUNTY_STATUS_PAID; });
    }
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

void token::addhotquestn(name user, uint64_t question_id, int hours) {
  require_auth(user);
  question_index question_table(peeranha_main, scope_all_questions);
  auto iter_question = question_table.find(question_id);
  
  eosio::check(iter_question->user == user, "Wrong user transaction");
  eosio::check(iter_question != question_table.end(), "Question not found");
  eosio::check(hours > 0, "Hours must be positive");

  const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
  auto quantity = asset(int64_to_peer(hours * TOKEN_PROMOTED_QUESTION), sym);
  sub_balance(user, quantity);
  add_balance(user_prom_leave, quantity / 2, _self);
  add_balance(user_prom_stay, quantity / 2, _self);

  token_awards_index token_awards_table(_self, scope_all_token_awards);
  uint64_t period = get_period(now());
  auto iter_token_awards = token_awards_table.find(period);

   if (iter_token_awards == token_awards_table.end()) {
    token_awards_table.emplace(
      _self, [quantity, period](auto &token_awards) {
        token_awards.sum_token = quantity / 2;
        token_awards.period = period;
      });
  } else {
    token_awards_table.modify(
      iter_token_awards, _self, [quantity](auto &token_awards) {
        token_awards.sum_token += quantity / 2;
      });
  }

  time time_now = now();
  promoted_questions_index promoted_questions_table(_self, iter_question->community_id);
  auto iter_clear = promoted_questions_table.begin();
  while (iter_clear != promoted_questions_table.end()) {
    if (iter_clear->ends_time < time_now) {
      iter_clear = promoted_questions_table.erase(iter_clear); 
    } else {
      ++iter_clear;
    }
  }

  auto iter_promoted_questions = promoted_questions_table.find(question_id);
  eosio::check(iter_promoted_questions == promoted_questions_table.end(), "This question is already marked as promoted");
  promoted_questions_table.emplace(
    _self, [&](auto &promoted_question) {
      promoted_question.question_id = question_id;
      promoted_question.start_time = time_now;
      promoted_question.ends_time = time_now + hours * ONE_HOUR;
    }); 
}

void token::delhotquestn(name user, uint64_t question_id) {
  require_auth(user);
  question_index question_table(peeranha_main, scope_all_questions);
  auto iter_question = question_table.find(question_id);
  eosio::check(iter_question != question_table.end(), "Question not found");

  promoted_questions_index promoted_questions_table(_self, iter_question->community_id); 
  auto iter_promoted_questions = promoted_questions_table.find(iter_question->id);
  eosio::check(iter_promoted_questions != promoted_questions_table.end(), "Hop question not found");

  return_promoted_tokens(iter_promoted_questions, iter_question->user);
  promoted_questions_table.erase(iter_promoted_questions);
}

void token::return_promoted_tokens(promoted_questions_index::const_iterator &iter_promoted_questions, name user) {
  if (iter_promoted_questions->ends_time < now()) {
    uint64_t return_token = (now() - iter_promoted_questions->ends_time) / ONE_HOUR;
    if (return_token) {
      const symbol sym = symbol(peeranha_asset_symbol, TOKEN_PRECISION);
      auto quantity = asset(int64_to_peer(return_token), sym) / 2;
      //sub_balance(_self, quantity);
      //sub_balance(другой акк, quantity);
      //add_balance(user, quantity, _self);

      token_awards_index token_awards_table(_self, scope_all_token_awards);
      uint64_t period = get_period(iter_promoted_questions->start_time);
      auto iter_token_awards = token_awards_table.find(period);
      eosio::check(iter_token_awards != token_awards_table.end(), "No promoted entry found");

      token_awards_table.modify(
        iter_token_awards, _self, [quantity](auto &token_awards) {
          token_awards.sum_token -= quantity;
      });
    }
  }
}

#if STAGE == 1 || STAGE == 2

void token::resettables() {
  require_auth(_self);
  account_index account_table(peeranha_main, scope_all_accounts);

  for (auto iter_acc = account_table.begin(); iter_acc != account_table.end(); iter_acc++) {
    accounts to_acnts(_self, iter_acc->user.value);
    auto iter_to_acnts = to_acnts.begin();
    while (iter_to_acnts != to_acnts.end()) {
      iter_to_acnts = to_acnts.erase(iter_to_acnts);
    }
    
    period_reward_index period_reward_table(_self, iter_acc->user.value);
    auto iter_period_reward = period_reward_table.begin();
    while (iter_period_reward != period_reward_table.end()) {
      iter_period_reward = period_reward_table.erase(iter_period_reward);
    }

    boost_index boost_table(_self, iter_acc->user.value);
    auto iter_boost = boost_table.begin();
    while (iter_boost != boost_table.end()) {
      iter_boost = boost_table.erase(iter_boost);
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

  statistics_boost_index statistics_boost_table(_self, scope_all_boost);
  auto iter_statistics_boost = statistics_boost_table.begin();
  while (iter_statistics_boost != statistics_boost_table.end()) {
    iter_statistics_boost = statistics_boost_table.erase(iter_statistics_boost);
  }

  invited_users_index invited_users_table(_self, all_invited);
  auto iter_invited_user = invited_users_table.begin();
  while (iter_invited_user != invited_users_table.end()) {
    iter_invited_user = invited_users_table.erase(iter_invited_user);
  }

  token_awards_index token_awards_table(_self, scope_all_token_awards);
  auto iter_token_awards = token_awards_table.begin();
  while (iter_token_awards != token_awards_table.end()) {
    iter_token_awards = token_awards_table.erase(iter_token_awards);
  }

  community_table_index community_table(peeranha_main, scope_all_communities);
  auto iter_community = community_table.begin();
  while (iter_community != community_table.end()) {
    promoted_questions_index promoted_questions_table(_self, iter_community->id);
    auto iter_promoted_questions = promoted_questions_table.begin();
    while (iter_promoted_questions != promoted_questions_table.end()) {
      iter_promoted_questions = promoted_questions_table.erase(iter_promoted_questions);
    }
    ++iter_community;
  }

  question_bounty bounty_table(_self, scope_all_bounties);
  auto iter_bounty = bounty_table.begin();
  while (iter_bounty != bounty_table.end()) {
    iter_bounty = bounty_table.erase(iter_bounty);
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
               (addboost)(setbounty)(editbounty)(paybounty)(addhotquestn)(delhotquestn)

#if STAGE == 1 || STAGE == 2
                   (resettables)
#if STAGE == 2
                       (mapcrrwpool)
#endif

#endif
                      (payforcpu))
