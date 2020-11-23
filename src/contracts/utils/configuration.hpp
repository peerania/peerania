#pragma once
#include <eosio/eosio.hpp>
#include "account.hpp"


struct [[eosio::table("config"), eosio::contract("peeranha.main")]] configuration {
  uint64_t key;
  uint64_t value;

  bool has_community_moderation_flag(int mask, uint16_t community_id) const;
  uint64_t primary_key() const { return key; }
};
typedef eosio::multi_index<"config"_n, configuration> configuration_index;
const uint64_t scope_all_configuration = eosio::name("allconfiguration").value; 