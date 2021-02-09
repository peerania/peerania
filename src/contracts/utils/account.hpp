#pragma once
#include <eosio/eosio.hpp>
#include <eosio/system.hpp>
#include <string>
#include "peeranha_types.h"
#include "property.hpp"
#include "token_common.hpp"
#include "IpfsHash.hpp"
#include "account_economy.h"
#include "property_community.hpp"
#include "boost.hpp"

#define RATING_FOR_LOGIN 1
#define PROPERTY_LAST_RATING_UPDATE_PERIOD 18

struct report {
  eosio::name user;
  time report_time;
  uint8_t report_points;
};

struct given_answer {
  uint64_t question_id;
  uint16_t answer;
};

struct [[ eosio::table("account"), eosio::contract("peeranha.main") ]] account {
  eosio::name user;
  // mandatory fields
  std::string display_name;
  IpfsHash ipfs_profile;
  IpfsHash ipfs_avatar;
  time registration_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  int rating = 0;
  int pay_out_rating = 0;
  uint16_t last_update_period = 0;
  uint16_t energy;
  std::vector<uint16_t> followed_communities;
  // replace to varint
  uint32_t questions_asked;
  uint32_t answers_given;
  uint32_t correct_answers;
  std::vector<report> reports;
  uint8_t report_power;
  time last_freeze;
  bool is_frozen;
  
  void update();

  void reduce_energy(uint8_t value, uint16_t community_id);

  uint16_t get_status_energy() const;
  uint8_t  get_status_moderation_impact(uint16_t community_id) const;
  bool has_moderation_flag(int mask) const;  
  
  uint64_t primary_key() const { return user.value; }
  uint64_t rating_rkey() const { return (1ULL << 32) - rating; }
  uint64_t registration_time_key() const { return registration_time; }

  EOSLIB_SERIALIZE(
      account,
      (user)(display_name)(ipfs_profile)(ipfs_avatar)(registration_time)(
          string_properties)(integer_properties)(rating)(pay_out_rating)(
          last_update_period)(energy)(followed_communities)(questions_asked)(
          answers_given)(correct_answers)(reports)(report_power)(last_freeze)(
          is_frozen))
};

void assert_display_name(const std::string &display_name);

const uint64_t scope_all_accounts = eosio::name("allaccounts").value;
typedef eosio::multi_index<
    "account"_n, account
    ,
    eosio::indexed_by<"rating"_n, eosio::const_mem_fun<account, uint64_t,
                                                      &account::rating_rkey>>,
    eosio::indexed_by<"time"_n,
                     eosio::const_mem_fun<account, uint64_t,
                                          &account::registration_time_key>>
    > account_index;

// Stub solution:( no ability to compile correctly
#include "account.cpp"
