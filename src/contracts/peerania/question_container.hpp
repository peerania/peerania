#pragma once
#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <vector>
#include "history.hpp"

// Answer id starts from 1
// If in function param (answer_id == APPLY_TO_QUESTION)
// the action will applied to the question
#define APPLY_TO_QUESTION 0

// Comment id starts from 1
// If in function param (comment_id == APPLY_TO_ANSWER)
// the action will applied to the answer
#define APPLY_TO_ANSWER 0

#define PROPERTY_DELETION_VOTES 0
#define PROPERTY_MODERATION_VOTES 1

struct comment {
  uint16_t id;
  time post_time;
  account_name user;
  std::string ipfs_link;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint16_t bkey() const { return id; }
};

struct answer {
  uint16_t id;
  time post_time;
  account_name user;
  std::string ipfs_link;
  std::vector<comment> comments;
  // additional info
  int16_t rating = 0;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint16_t bkey() const { return id; }
};

/// @abi table
struct question {
  uint64_t id;
  time post_time;
  account_name user;
  std::string ipfs_link;
  std::vector<answer> answers;
  std::vector<comment> comments;
  // additionl info
  uint16_t correct_answer_id = 0;
  int16_t rating = 0;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint64_t primary_key() const { return id; }
  EOSLIB_SERIALIZE(question,
                   (id)(post_time)(user)(ipfs_link)(answers)(comments)(
                       correct_answer_id)(rating)(properties)(history))
};

const scope_name all_questions = N(allquestions);
typedef eosio::multi_index<N(question), question> question_index;

std::vector<answer>::iterator find_answer(question &q, uint16_t answer_id) {
  auto iter_answer = binary_find(q.answers.begin(), q.answers.end(), answer_id);
  eosio_assert(iter_answer != q.answers.end(), "Answer not found");
  return iter_answer;
}

template <typename T>
std::vector<comment>::iterator find_comment(T &item, uint16_t comment_id) {
  auto iter_comment =
      binary_find(item.comments.begin(), item.comments.end(), comment_id);
  eosio_assert(iter_comment != item.comments.end(), "Comment not found");
  return iter_comment;
}