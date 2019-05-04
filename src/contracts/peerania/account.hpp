#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>
#include <string>
#include "economy.h"
#include "peerania_types.h"
#include "property.hpp"
#include "status.hpp"

struct [[ eosio::table("account"), eosio::contract("peerania") ]] account {
  eosio::name user;
  // mandatory fields
  std::string display_name;
  std::string ipfs_profile;
  time registration_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  int rating = 0;
  uint8_t moderation_points = 0;
  int pay_out_rating = 0;
  uint16_t last_update_period = 0;
  uint8_t questions_left = 0;
  std::vector<uint16_t> followed_communities;
  uint32_t questions_asked = 0;
  uint32_t answers_given = 0;
  uint32_t correct_answers = 0;

  void update() {
    uint16_t current_period =
        (now() - registration_time) / ACCOUNT_STAT_RESET_PERIOD;
    uint16_t periods_have_passed = current_period - last_update_period;
    if (periods_have_passed > 0) {
      if (rating < 0) {
        rating += periods_have_passed * BAN_RATING_INCREMENT_PER_PERIOD;
        if (rating > 0) rating = 0;
      } else {
        questions_left = status_question_limit(rating);
        moderation_points = status_moderation_points(rating);
        last_update_period = current_period;
      }
    }
  }

  uint64_t primary_key() const { return user.value; }
  // uint64_t rating_rkey() const { return (1 << 17) - pay_out_rating; }
  EOSLIB_SERIALIZE(
      account,
      (user)(display_name)(ipfs_profile)(registration_time)(string_properties)(
          integer_properties)(rating)(moderation_points)(pay_out_rating)(
          last_update_period)(questions_left)(followed_communities)(
          questions_asked)(answers_given)(correct_answers))
};

#define MIN_DISPLAY_NAME_LEN 3
#define MAX_DISPLAY_NAME_LEN 20

void assert_display_name(const std::string &display_name) {
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN &&
                   display_name.length() <= MAX_DISPLAY_NAME_LEN,
               "The display name too short.");
}

const uint64_t scope_all_accounts = eosio::name("allaccounts").value;
typedef eosio::multi_index<"account"_n, account> account_index;
