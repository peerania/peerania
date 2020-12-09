#pragma once
#include <eosio/eosio.hpp>
#include "account.hpp"

struct [[ eosio::table("statboost"), eosio::contract("peeranha.token") ]] statistics_boost {
    eosio::asset sum_tokens;
    eosio::asset max_stake;
    eosio::name user_max_stake;
    uint64_t period;

    uint64_t primary_key() const { return period; }
  };
  typedef eosio::multi_index<"statboost"_n, statistics_boost> statistics_boost_index;
  const uint64_t scope_all_boost = eosio::name("allboost").value;

  struct [[ eosio::table("boost"), eosio::contract("peeranha.token") ]] boost_tokens {
    eosio::asset staked_tokens;
    eosio::asset unstaked_tokens;
    uint64_t period;

    uint64_t primary_key() const { return period; }
  };
  typedef eosio::multi_index<"boost"_n, boost_tokens> boost_index;

// Stub solution:( no ability to compile correctly
#include "boost.cpp"