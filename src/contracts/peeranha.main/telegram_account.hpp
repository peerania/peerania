#pragma once
#include "peeranha.hpp"
#include <stdint.h>

#define NOT_CONFIRMED_TELEGRAM_ACCOUNT 0
#define CONFIRMED_TELEGRAM_ACCOUNT 1
#define EMPTY_TELEGRAM_ACCOUNT 2

struct [[ eosio::table("telegramacc"), eosio::contract("peeranha.main") ]] telegram_account {
  eosio::name user;
  int telegram_id; 
  uint8_t confirmed;
  
  uint64_t primary_key() const { return user.value; }
  uint64_t telegram_rkey() const { return telegram_id; }

  EOSLIB_SERIALIZE(
      telegram_account,
      (user)(telegram_id)(confirmed))
};

const uint64_t scope_all_telegram_accounts = eosio::name("alltelacc").value;
typedef eosio::multi_index<
    "telegramacc"_n, telegram_account,
    eosio::indexed_by<"userid"_n,
                     eosio::const_mem_fun<telegram_account, uint64_t,
                                          &telegram_account::telegram_rkey>>
    > telegram_account_index;