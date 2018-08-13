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
  int len = len = (display_name.length() < 12) ? display_name.length() : 12;
  for (int i = 0; i < len; ++i) {
    s[i] = 97 + (display_name[i] % 26);
  }
  s[len] = '\0';
  return ::eosio::string_to_name(s);
}

//display name to account
/// @abi table disptoacc
struct disp_to_acc {
  account_name owner;
  std::string display_name;
  uint64_t primary_key() const { return owner; }
  EOSLIB_SERIALIZE(disp_to_acc, (owner)(display_name))
};

typedef multi_index<N(disptoacc), disp_to_acc> disp_to_acc_index;
};  // namespace eosio