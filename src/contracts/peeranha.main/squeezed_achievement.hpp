#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>

struct [[eosio::table("achieve"), eosio::contract("peeranha.main")]] squeezed_achievement {
  uint32_t id;
  uint64_t count;

  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"achieve"_n, squeezed_achievement> squeezed_achievement_index;
const uint64_t scope_all_squeezed_achievements = eosio::name("allachieve").value;