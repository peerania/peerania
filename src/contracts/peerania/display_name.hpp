#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>

namespace eosio {
#define MIN_DISPLAY_NAME_LEN 3
// this function must be translated to JS
// rewirite it using implementation string_to_name(char*) to achive better
// performance
uint64_t hash_display_name(const std::string &display_name) {
  char s[13];
  int len = 12;
  if (display_name.length() < 12) len = display_name.length();

  for (int i = 0; i < len; ++i) s[i] = 97 + (display_name[i] % 26);
  s[len] = 0;
  return ::eosio::string_to_name(s);
}

/// @abi table dnametoacc
struct d_name_to_acc{
  uint64_t owner;
  std::string display_name;
  uint64_t primary_key() const { return owner; }
  EOSLIB_SERIALIZE(d_name_to_acc, (owner)(display_name))
};

typedef multi_index<N(dnametoacc), d_name_to_acc> d_name_to_acc_index;
};  // namespace eosio