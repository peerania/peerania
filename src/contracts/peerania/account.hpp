#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include "property.hpp"

///@abi table
struct account {
  table_name owner;
  // mandatory fields
  std::string display_name;
  std::string ipfs_profile;
  time registration_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  uint16_t rating = 0;
  uint16_t moderation_points = 0;
  uint64_t primary_key() const { return owner; }
  EOSLIB_SERIALIZE(account,
                   (owner)(display_name)(ipfs_profile)(registration_time)(
                       string_properties)(integer_properties)(rating)(moderation_points))
};

const scope_name all_accounts = N(allaccounts);
typedef eosio::multi_index<N(account), account> account_index;