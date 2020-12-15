#pragma once
#include <eosio/eosio.hpp>
#include "account.hpp"

#define CONFIGURATION_KEY_QUESTION 1
#define CONFIGURATION_KEY_TELEGRAM 2

struct [[eosio::table("config"), eosio::contract("peeranha.main")]] configuration {
  uint64_t key;
  uint64_t value;

  uint64_t primary_key() const { return key; }
};
typedef eosio::multi_index<"config"_n, configuration> configuration_index;
const uint64_t scope_all_config = eosio::name("allconfig").value; 