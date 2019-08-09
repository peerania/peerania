#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "history.hpp"
#include "status.hpp"

#define ID_CREATE_COMMUNITY 0

#define MAX_TAG_COMMUNITY_CREATE_ID 0xFFFFFFFF
#define MAX_TAG_COUNT 5

#define MAX_COMMUNITY_ID 0xFFFF
#define MAX_TAG_ID 0xFFFFFFFF

#define MIN_SUGGESTED_TAG 5
#define MAX_SUGGESTED_TAG 25

struct suggest_tag {
  std::string name;
  std::string ipfs_description;
};

const uint64_t scope_all_communities = eosio::name("allcomm").value;

struct [[eosio::table("crcommtb"), eosio::contract("peerania")]] crcommtb {
  uint32_t id;
  eosio::name creator;
  std::string name;
  std::string ipfs_description;
  time creation_time;
  std::vector<eosio::name> upvotes;
  std::vector<eosio::name> downvotes;
  std::vector<suggest_tag> suggested_tags;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"crcommtb"_n, crcommtb> create_community_index;

struct [[ eosio::table("crtagtb"), eosio::contract("peerania") ]] crtagtb {
  uint32_t id;
  eosio::name creator;
  std::string name;
  std::string ipfs_description;
  std::vector<eosio::name> upvotes;
  std::vector<eosio::name> downvotes;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"crtagtb"_n, crtagtb> create_tag_index;

struct [[eosio::table("tags"), eosio::contract("peerania")]] tags {
  uint32_t id;
  std::string name;
  std::string ipfs_description;
  uint32_t questions_asked;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"tags"_n, tags> tag_table_index;

struct [[eosio::table("communities"), eosio::contract("peerania")]] communities {
  uint16_t id;
  std::string name;
  std::string ipfs_description;
  time creation_time;
  uint32_t questions_asked = 0;
  uint32_t answers_given = 0;
  uint32_t correct_answers = 0;
  uint32_t users_subscribed = 0;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"communities"_n, communities> community_table_index;

void assert_tag_name(const std::string name) {
  eosio::check(name.size() >= 2 && name.size() <= 15, "Invalid tag name");
}

void assert_community_name(const std::string name) {
  eosio::check(name.size() >= 2 && name.size() <= 25, "Invalid community name");
}