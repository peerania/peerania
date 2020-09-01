#pragma once
#pragma once
#include "peeranha.hpp"
#include <stdint.h>

struct [[ eosio::table("telegramacc"), eosio::contract("peeranha.main") ]] telegram_account {
  eosio::name user;
  int telegram_id; 
  bool confirmed;
  
  uint64_t primary_key() const { return user.value; }
  int telegram_rkey() const { return telegram_id; }

  EOSLIB_SERIALIZE(
      telegram_account,
      (user)(telegram_id)(confirmed))
};

const uint64_t scope_all_telegram_accounts = eosio::name("alltelacc").value;
typedef eosio::multi_index<"telegramacc"_n, telegram_account> telegram_account_index;
// typedef eosio::multi_index<
//     "telegramacc"_n, telegram_account
//     ,
//     eosio::indexed_by<"tel"_n, eosio::const_mem_fun<telegram_account, uint64_t,
//                                                       &telegram_account::telegram_rkey>>
//     > telegram_account_index;