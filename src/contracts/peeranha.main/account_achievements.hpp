#pragma once
#include <eosio/eosio.hpp>
#include <vector>

struct key_account_achievements{
  uint32_t achievements_id;
  uint64_t value;
  time date;

  uint32_t lkey() { return achievements_id; }
};

struct [[eosio::table("accachieve"), eosio::contract("peeranha.main")]] account_achievements {
  eosio::name user;
  std::vector<key_account_achievements> user_achievements;

  uint64_t primary_key() const { return user.value; }
};
typedef eosio::multi_index<"accachieve"_n, account_achievements> account_achievements_index;
const uint64_t scope_all_account_achievements = eosio::name("allaccachieve").value;