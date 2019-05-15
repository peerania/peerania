#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>

struct [[
  eosio::table("globalstat"), eosio::contract("peerania")
]] globalstat {
  uint64_t version;
  // mandatory fields
  uint32_t user_count;
  uint16_t communities_count;

  uint64_t primary_key() const { return version; }
  EOSLIB_SERIALIZE(
      globalstat,
      (version)(user_count)(communities_count)  )
};

const uint64_t scope_all_stat = eosio::name("allstat").value;
typedef eosio::multi_index<"globalstat"_n, globalstat> global_stat_index;
