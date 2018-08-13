#pragma once
#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <vector>

namespace eosio {
#define COMMENT_TO_QUESTION 0

struct comment {
  uint16_t id;
  time registration_time;
  account_name user;
  std::string ipfs_link;
};

struct answer {
  uint16_t id;
  time registration_time;
  account_name user;
  std::string ipfs_link;
  std::vector<comment> comments;
};

/// @abi table
struct question {
  uint64_t id;
  time registration_time;
  account_name user;
  std::string ipfs_link;
  std::vector<answer> answers;
  std::vector<comment> comments;
  // additionl info
  uint64_t primary_key() const { return id; }
  EOSLIB_SERIALIZE(question, (id)(registration_time)(user)(ipfs_link)(answers)(comments))
};

typedef multi_index<N(question), question> question_index;
};  // namespace eosio