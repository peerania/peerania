
#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include "property.hpp"

struct account_timer {
  uint8_t timer;
  time last_update;
};

struct [[eosio::table("account")]] account {
  account_name owner;
  // mandatory fields
  std::string display_name;
  std::string ipfs_profile;
  time registration_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  int16_t rating = 0;
  uint16_t moderation_points = 0;
  std::vector<account_timer> timers;  // excluded from abi
  int16_t pay_out_rating = 0;
  time last_seen;
  uint64_t primary_key() const { return owner; }
  uint64_t rating_rkey() const { return (1 << 17) - pay_out_rating; }
  uint128_t display_name_key() const {
    uint128_t key = 0;
    for (int i = 0; i < display_name.length() && i < 16; ++i) {
      if (i >= display_name.length())
        key += static_cast<uint128_t>(display_name[i]) << (120 - i * 8);
    }
    return 0;
  }
  EOSLIB_SERIALIZE(account,
                   (owner)(display_name)(ipfs_profile)(registration_time)(
                       string_properties)(integer_properties)(rating)(
                       moderation_points)(timers)(pay_out_rating))
};

const scope_name all_accounts = N(allaccounts);
typedef eosio::multi_index<
    N(account), account,
    eosio::indexed_by<N(byrating), eosio::const_mem_fun<account, uint64_t,
                                                        &account::rating_rkey>>,
    eosio::indexed_by<
        N(bydispname),
        eosio::const_mem_fun<account, uint128_t, &account::display_name_key>>>
    account_index;
