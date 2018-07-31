#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>

namespace eosio {
#define MIN_DISPLAYNAME_LEN 3
// this function must be translated to JS
// rewirite it using implementation string_to_name(char*) to achive better
// performance
uint64_t hash_display_name(const std::string &displayname) {
  char s[13];
  int len = 12;
  if (displayname.length() < 12) len = displayname.length();

  for (int i = 0; i < len; ++i) s[i] = 97 + (displayname[i] % 26);
  s[len] = 0;
  return ::eosio::string_to_name(s);
}

/// @abi table
struct disptoacc {
  uint64_t owner;
  std::string displayname;
  uint64_t primary_key() const { return owner; }
  EOSLIB_SERIALIZE(disptoacc, (owner)(displayname))
};

typedef multi_index<N(disptoacc), disptoacc> disptoacc_index;
};  // namespace eosio