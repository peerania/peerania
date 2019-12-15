#pragma once
#include <eosio/eosio.hpp>
#include "peeranha_types.h"

#if STAGE == 1
int PERIOD_LENGTH = 7200;                // 2 hours
time START_PERIOD_TIME = 1575406800UL;  // Tuesday, 3 December 2019 г., 21:00:00
#else
int PERIOD_LENGTH = 604800;                // 7 day = 1 week
time START_PERIOD_TIME = 1569888000UL;  // Monday 1st october 2019
#endif

uint16_t get_period(time t) {
  t -= START_PERIOD_TIME;
  return t / PERIOD_LENGTH;
}

// scoped by user
struct [[eosio::table("periodrating"), eosio::contract("peeranha.main")]] periodrating {
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
struct [[eosio::table("totalrating"), eosio::contract("peeranha.main")]] totalrating {
  uint16_t period;
  uint32_t total_rating_to_reward;
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(totalrating, (period)(total_rating_to_reward))
};

typedef eosio::multi_index<"totalrating"_n, totalrating> total_rating_index;
const uint64_t scope_all_periods = eosio::name("allperiods").value;