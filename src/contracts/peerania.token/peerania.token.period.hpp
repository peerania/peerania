#pragma once

#include <eosio/asset.hpp>
#include <eosio/eosio.hpp>
#include <eosio/name.hpp>

#include <string>

#define INFLATION_PERIOD 52 //52 periods(52 weeks)
#define START_POOL 200000
#define POOL_REDUSE 25000

// scoped by user
struct [[eosio::table("periodreward"), eosio::contract("peerania.tkn")]] periodreward {
  uint16_t period;
  eosio::asset reward;
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(periodreward, (period)(reward))
};

typedef eosio::multi_index<"periodreward"_n, periodreward> period_reward_index;

// owned by main
// scopeed by const = N(allperiods)
struct [[eosio::table("totalreward"), eosio::contract("peerania.tkn")]] totalreward {
  uint16_t period;
  eosio::asset total_reward;
  uint64_t primary_key() const {
    // implicit cast
    return period;
  };
  EOSLIB_SERIALIZE(totalreward, (period)(total_reward))
};

typedef eosio::multi_index<"totalreward"_n, totalreward> total_reward_index;