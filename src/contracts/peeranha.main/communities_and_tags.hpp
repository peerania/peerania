#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "history.hpp"

#define ID_CREATE_COMMUNITY 0

#define MAX_TAG_COMMUNITY_CREATE_ID 0xFFFFFFFF
#define MAX_TAG_COUNT 5

#define MAX_COMMUNITY_ID 0xFFFF
#define MAX_TAG_ID 0xFFFFFFFF

#define MIN_SUGGESTED_TAG 5
#define MAX_SUGGESTED_TAG 25

#define ID_QUESTIONS_TYPE 28
#define ANY_QUESTIONS_TYPE 2

struct suggest_tag {
  std::string name;
  IpfsHash ipfs_description;
};

const uint64_t scope_all_communities = eosio::name("allcomm").value;

struct [[eosio::table("crcommtb"), eosio::contract("peeranha.main")]] crcommtb {
  uint32_t id;
  eosio::name creator;
  std::string name;
  IpfsHash ipfs_description;
  time creation_time;
  std::vector<eosio::name> upvotes;
  std::vector<eosio::name> downvotes;
  std::vector<suggest_tag> suggested_tags;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"crcommtb"_n, crcommtb> create_community_index;

struct [[ eosio::table("crtagtb"), eosio::contract("peeranha.main") ]] crtagtb {
  uint32_t id;
  eosio::name creator;
  std::string name;
  IpfsHash ipfs_description;
  std::vector<eosio::name> upvotes;
  std::vector<eosio::name> downvotes;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"crtagtb"_n, crtagtb> create_tag_index;

struct [[eosio::table("tags"), eosio::contract("peeranha.main")]] tags {
  uint32_t id;
  std::string name;
  IpfsHash ipfs_description;
  uint32_t questions_asked;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"tags"_n, tags> tag_table_index;

struct [[eosio::table("communities"), eosio::contract("peeranha.main")]] communities {
  uint16_t id;
  std::string name;
  IpfsHash ipfs_description;
  time creation_time;
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  uint32_t questions_asked = 0;
  uint32_t answers_given = 0;
  uint32_t correct_answers = 0;
  uint32_t users_subscribed = 0;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"communities"_n, communities> community_table_index;

struct [[eosio::table("commbuf"), eosio::contract("peeranha.main")]] commbuf {
  uint16_t id;
  std::string name;
  IpfsHash ipfs_description;
  time creation_time;
  uint32_t questions_asked = 0;
  uint32_t answers_given = 0;
  uint32_t correct_answers = 0;
  uint32_t users_subscribed = 0;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"commbuf"_n, commbuf> commbuf_table_index;

inline void assert_tag_name(const std::string name) {
  assert_readble_string(name, 2, 30, "Invalid tag name");
}

inline void assert_community_name(const std::string name) {
  assert_readble_string(name, 2, 50, "Invalid community name");
}

inline void assert_community_type(int question_type){
  eosio::check(question_type <= ANY_QUESTIONS_TYPE, "Question type not exists");
}

inline void assert_choose_type_allowed(const account &action_caller, int type) {
  if (type != ANY_QUESTIONS_TYPE){
    eosio::check(action_caller.has_moderation_flag(MODERATOR_FLG_CREATE_COMMUNITY), "User must to be moderator");
  } else return;
}