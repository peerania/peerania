#pragma once
#include <eosio/eosio.hpp>
#include <eosio/system.hpp>
#include <string>
#include "peeranha_types.h"
#include "property.hpp"
#include "token_common.hpp"
#include "IpfsHash.hpp"
#include "account_economy.h"
#include "property_community.hpp"

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

const uint64_t scope_all_telegram_accounts = eosio::name("alltelegramacc").value;
typedef eosio::multi_index<
    "telegramacc"_n, account
    ,
    eosio::indexed_by<"telegram"_n, eosio::const_mem_fun<telegram_account, int,
                                                      &telegram_account::telegram_rkey>>
    > telegram_account_index;

// Stub solution:( no ability to compile correctly
// #include "account.cpp"
