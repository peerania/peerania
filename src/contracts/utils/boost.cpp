#include "boost.hpp"

int64_t getboost(eosio::name user, uint16_t period = get_period(now())) {
  eosio::name peeranha_token = eosio::name("peeranhatken");
  
  boost_index boost_table(peeranha_token, user.value);
  const uint64_t scope_all_boost = eosio::name("allboost").value;
  statistics_boost_index statistics_boost_table(peeranha_token, scope_all_boost);

  if (boost_table.begin() == boost_table.end() || statistics_boost_table.begin() == statistics_boost_table.end()) {
    return MULTIPLICATION_TOTAL_RATING;
  }
  
  auto iter_last_boost = boost_table.rbegin();
  while(iter_last_boost->period > period) {
    ++iter_last_boost;
    if (iter_last_boost == boost_table.rend()) return MULTIPLICATION_TOTAL_RATING;
  }

  auto iter_last_statistics = statistics_boost_table.rbegin();
  while(iter_last_statistics->period > period) {
    ++iter_last_statistics;
    if (iter_last_statistics == statistics_boost_table.rend()) return MULTIPLICATION_TOTAL_RATING;
  }

  if (iter_last_boost->staked_tokens.amount == 0 || iter_last_statistics->max_stake.amount == 0) {
    return MULTIPLICATION_TOTAL_RATING;
  }

  uint64_t percent = iter_last_boost->staked_tokens.amount * MAX_MULTIPLICATION_TOTAL_RATING / iter_last_statistics->max_stake.amount + MULTIPLICATION_TOTAL_RATING;

  return percent;
}