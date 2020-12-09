#include "boost.hpp"

int64_t getboost(eosio::name user, uint16_t period = get_period(now())) {
  eosio::name peeranha_token = eosio::name("peeranhatken");
  
  boost_index boost_table(peeranha_token, user.value);
  const uint64_t scope_all_boost = eosio::name("allboost").value;
  statistics_boost_index statistics_boost_table(peeranha_token, scope_all_boost);

  if (boost_table.begin() == boost_table.end() || statistics_boost_table.begin() == statistics_boost_table.end()) {
    return 1000;
  }
  
  auto iter_last_boost = boost_table.rbegin();
  while(iter_last_boost->period > period) {
    ++iter_last_boost;
    if (iter_last_boost == boost_table.rend()) return 1000;
  }

  auto iter_last_statistics = statistics_boost_table.rbegin();
  while(iter_last_statistics->period > period) {
    ++iter_last_statistics;
    if (iter_last_statistics == statistics_boost_table.rend()) return 1000;
  }
  
  uint64_t percent =  iter_last_boost->streaked_tokens.amount * 100 / iter_last_statistics->max_stake.amount;
  
  if (percent >= 80)
    return 4000;       // x4
  else if (percent >= 60)
    return 3000;       // x3
  else if (percent >= 40)
    return 2000;       // x2
  else if (percent >= 20)
    return 1250;       //  x1.25
  else 
    return 1000;       // x1
}