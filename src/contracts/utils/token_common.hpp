#pragma once
#include <eosio/eosio.hpp>
#include "peeranha_types.h"

#if STAGE == 1
int PERIOD_LENGTH = 7200;               // 2 hours
time START_PERIOD_TIME = 1599571209UL;  // Wed, September 8, 2020 4:20:09 PM GMT+03:00 DST                                                
#elif STAGE == 2
int PERIOD_LENGTH = 3;          // 3 sec

struct [[ eosio::table("constants"), eosio::contract("peeranha") ]] constants {
  uint64_t id;
  time start_period_time;
  uint64_t primary_key() const { return id; }
  EOSLIB_SERIALIZE(constants, (id)(start_period_time))
};
typedef eosio::multi_index<eosio::name("constants"), constants> constants_index;
const uint64_t scope_all_constants = eosio::name("allconstants").value;

#else
int PERIOD_LENGTH = 604800;             // 7 day = 1 week
time START_PERIOD_TIME = 1576454400UL;  // December 16th, 2019 00:00:00
#endif

uint16_t get_period(time t) {
#if STAGE == 2
  constants_index all_constants_table("peeranhamain"_n, scope_all_constants);
  auto settings = all_constants_table.rbegin();
  time START_PERIOD_TIME = settings->start_period_time;
#endif
  t -= START_PERIOD_TIME;
  return t / PERIOD_LENGTH;
}

// scoped by user
struct [[
  eosio::table("periodrating"),
  eosio::contract("peeranha.main")
]] periodrating {
  uint16_t period;
  int rating;
  int rating_to_award = 0;
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(periodrating, (period)(rating)(rating_to_award))
};

typedef eosio::multi_index<"periodrating"_n, periodrating> period_rating_index;

// owned by main
// scopeed by const = N(allperiods)
struct [[
  eosio::table("totalrating"), eosio::contract("peeranha.main")
]] totalrating {
  uint16_t period;
  uint32_t total_rating_to_reward;      // total_rating_to_reward / 1000
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(totalrating, (period)(total_rating_to_reward))
};

typedef eosio::multi_index<"totalrating"_n, totalrating> total_rating_index;
const uint64_t scope_all_periods = eosio::name("allperiods").value;

struct [[
  eosio::table("totalratingg"), eosio::contract("peeranha.main")
]] totalratingg {
  uint16_t period;
  uint32_t total_rating_to_reward;      // total_rating_to_reward / 1000
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(totalratingg, (period)(total_rating_to_reward))
};

typedef eosio::multi_index<"totalratingg"_n, totalratingg> total_ratingg_index;
//const uint64_t scope_all_periods = eosio::name("allperiods").value;