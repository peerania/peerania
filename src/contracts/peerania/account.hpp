#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>
#include <string>
#include "property.hpp"
#include "status.hpp"
#include "peerania_types.h"

struct [[eosio::table("account")]] account {
  eosio::name owner;
  // mandatory fields
  std::string display_name;
  std::string ipfs_profile;
  time registration_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  int16_t rating = 0;
  uint16_t moderation_points = 0;
  int16_t pay_out_rating = 0;
  time last_seen;
  uint8_t questions_left = 0;
  uint64_t primary_key() const { return owner.value; }
  uint64_t rating_rkey() const { return (1 << 17) - pay_out_rating; }
  EOSLIB_SERIALIZE(account,
                   (owner)(display_name)(ipfs_profile)(registration_time)(
                       string_properties)(integer_properties)(rating)(
                       moderation_points)(pay_out_rating)(last_seen)
                       (questions_left))
};

#define ACCOUNT_STAT_RESET_PERIOD 259200 //3 Days
void update_account(account &acc){
  time current_time = now();
  if ((current_time - acc.registration_time)/ACCOUNT_STAT_RESET_PERIOD - (acc.last_seen - acc.registration_time)/ACCOUNT_STAT_RESET_PERIOD > 0){
    acc.moderation_points = status_moderation_points(acc.pay_out_rating);
    acc.questions_left = status_question_limit(acc.pay_out_rating);
  }
}

#define MIN_DISPLAY_NAME_LEN 3
#define MAX_DISPLAY_NAME_LEN 20

void assert_display_name(const std::string &display_name) {
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN &&
                   display_name.length() <= MAX_DISPLAY_NAME_LEN,
               "The display name too short.");
}
const uint64_t scope_all_accounts = "allaccounts"_n.value;
typedef eosio::multi_index<"account"_n, account> account_index;
