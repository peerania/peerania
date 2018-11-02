#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>

#ifndef DEBUG
#define PERIOD_LENGTH 604800                // 7 day = 1 week
const time START_PERIOD_TIME = 1538341200;  // Monday 1st october 2018
#else
#define PERIOD_LENGTH 3  // 2 sec
time START_PERIOD_TIME;  // We need mechanism which change it once on deploy
#endif

uint16_t get_period(time t) {
  t -= START_PERIOD_TIME;
  return t / PERIOD_LENGTH;
}

// scoped by user
struct [[eosio::table("periodrating")]] periodrating {
  uint16_t period;
  int16_t rating;
  uint16_t rating_to_award = 0;
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(periodrating, (period)(rating)(rating_to_award))
};

typedef eosio::multi_index<N(periodrating), periodrating> period_rating_index;

// owned by main
// scopeed by const = N(allperiods)
struct [[eosio::table("totalrating")]] totalrating {
  uint16_t period;
  uint32_t total_rating_to_reward;
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(totalrating, (period)(total_rating_to_reward))
};

typedef eosio::multi_index<N(totalrating), totalrating> total_rating_index;
const scope_name all_periods = N(allperiods);