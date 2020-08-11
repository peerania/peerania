#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "property.hpp"

struct key_account_achievements{
  int achievements_id;
  int value;
  time date;

  uint8_t lkey() const { return achievements_id; }
};

struct [[eosio::table("accachieve"), eosio::contract("peeranha.main")]] account_achievements {
  eosio::name user;
  std::vector<key_account_achievements> user_achievements;

  uint64_t primary_key() const { return user.value; }
};
typedef eosio::multi_index<"accachieve"_n, account_achievements> account_achievements_index;
const uint64_t scope_all_account_achievements = eosio::name("allaccachieve").value;