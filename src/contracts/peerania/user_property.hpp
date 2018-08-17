#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
// properties

// system properties

// system constants
#define SYSTEM_PROP_START 200

struct str_key_value {
  uint8_t key;
  std::string value;
  EOSLIB_SERIALIZE(str_key_value, (key)(value))
};

struct int_key_value {
  uint8_t key;
  int32_t value;
  EOSLIB_SERIALIZE(int_key_value, (key)(value))
};