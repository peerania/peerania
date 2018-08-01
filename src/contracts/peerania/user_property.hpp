#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
namespace eosio {
// properties

// system properties

// system constants
#define SYSTEM_PROP_START 250

inline uint64_t user_property_make_pk(account_name owner, uint8_t prop) {
  //10000007 is simple constant to achive better collision resistance
  //on this place could be any constant
  return owner + 1000007L * prop;
}

struct prop_key_value {
  uint8_t key;
  std::string value;
  EOSLIB_SERIALIZE(prop_key_value, (key)(value))
};

///@abi table userprop
struct user_property {
  account_name owner;
  prop_key_value key_value;
  uint64_t primary_key() const { return user_property_make_pk(owner, key_value.key); }
  EOSLIB_SERIALIZE(user_property, (owner)(key_value))
};

typedef multi_index<N(userprop), user_property> user_property_index;

};  // namespace eosio