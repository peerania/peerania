#pragma once
#include <eosio/eosio.hpp>

struct [[eosio::table("accachieve"), eosio::contract("peeranha.main")]] account_achievements {
  eosio::name user;
  uint64_t achievements_id;
  time date;

  uint64_t primary_key() const { return achievements_id; }
};
typedef eosio::multi_index<"accachieve"_n, account_achievements> account_achievements_index;