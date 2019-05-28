#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>
#include <string>
#include "economy.h"
#include "peerania_types.h"
#include "property.hpp"
#include "status.hpp"

struct report {
  eosio::name user;
  time report_time;
  uint8_t report_points;
};

struct [[ eosio::table("account"), eosio::contract("peerania") ]] account {
  eosio::name user;
  // mandatory fields
  std::string display_name;
  std::string ipfs_profile;
  std::string ipfs_avatar;
  time registration_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  int rating = 0;
  uint8_t moderation_points = 0;
  int pay_out_rating = 0;
  uint16_t last_update_period = 0;
  uint8_t questions_left = 0;
  uint8_t answers_left;
  uint8_t comments_left;
  std::vector<uint16_t> followed_communities;

  std::vector<report> reports;
  uint8_t report_power;
  time last_freeze;
  bool is_freezed;

  void update() {
    uint16_t current_period =
        (now() - registration_time) / ACCOUNT_STAT_RESET_PERIOD;
    uint16_t periods_have_passed = current_period - last_update_period;
    if (periods_have_passed > 0) {
      if (rating <= 0) {
        rating += periods_have_passed * BAN_RATING_INCREMENT_PER_PERIOD;
        if (rating > 0) rating = 1;
      } else {
        questions_left = status_question_limit(rating);
        moderation_points = status_moderation_points(rating);
      }
      last_update_period = current_period;
    }

    if (is_freezed) {
      if ((now() - last_freeze) >= (MIN_FREEZE_PERIOD * (1 << (report_power - 1)))) {
        reports.clear();
        is_freezed = false;
        last_freeze = now();
      }
    } else {
      if (report_power != 0 &&
          (now() - last_freeze) >= REPORT_POWER_RESET_PERIOD) {
        report_power = 0;
      }
      auto iter_report = reports.begin();
      while (iter_report != reports.end() && now() - iter_report->report_time >= REPORT_RESET_PERIOD) {
        iter_report = reports.erase(iter_report);
      }
    }
  }

  uint64_t primary_key() const { return user.value; }
  uint64_t rating_rkey() const { return (1ULL << 32) - rating; }
  uint64_t registration_time_key() const { return registration_time; }

  EOSLIB_SERIALIZE(
      account,
      (user)(display_name)(ipfs_profile)(ipfs_avatar)(registration_time)(
          string_properties)(integer_properties)(rating)(moderation_points)(
          pay_out_rating)(last_update_period)(questions_left)(
          followed_communities)(questions_asked)(answers_given)(
          correct_answers)(reports)(report_power)(last_freeze)(is_freezed))
};

#define MIN_DISPLAY_NAME_LEN 3
#define MAX_DISPLAY_NAME_LEN 20

void assert_display_name(const std::string &display_name) {
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN &&
                   display_name.length() <= MAX_DISPLAY_NAME_LEN,
               "The display name too short.");
}

const uint64_t scope_all_accounts = eosio::name("allaccounts").value;
typedef eosio::multi_index<
    "account"_n, account,
    eosio::indexed_by<"rating"_n, eosio::const_mem_fun<account, uint64_t,
                                                       &account::rating_rkey>>,
    eosio::indexed_by<"time"_n,
                      eosio::const_mem_fun<account, uint64_t,
                                           &account::registration_time_key>>>
    account_index;
