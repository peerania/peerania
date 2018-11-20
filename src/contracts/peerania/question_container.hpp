#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <vector>
#include "history.hpp"

// Answer id starts from FORUM_INDEX_START
#define EMPTY_ANSWER_ID 0

// Return true if the action must be applied to question
#define apply_to_question(answer_id) ((answer_id) == EMPTY_ANSWER_ID)

// Comment id starts from FORUM_INDEX_START
#define EMPTY_COMMENT_ID 0

// Return true if the action must be applied to answer
#define apply_to_answer(comment_id) ((comment_id) == EMPTY_COMMENT_ID)

#define FORUM_INDEX_START 1

#ifndef DEBUG
#define MAX_ANSWER_COUNT 200
#define MAX_COMMENT_COUNT 200
#else
#define MAX_ANSWER_COUNT 4
#define MAX_COMMENT_COUNT 4
#endif

#define PROPERTY_DELETION_VOTES 0
#define PROPERTY_MODERATION_VOTES 1
#define PROPERTY_LAST_MODIFIED 3

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

struct [[eosio::table("question")]] question {
  uint64_t id;
  time post_time;
  account_name user;
  std::string title;
  std::string ipfs_link;
  std::vector<answer> answers;
  std::vector<comment> comments;
  // additionl info
  uint16_t correct_answer_id = 0;
  int16_t rating = 0;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint64_t primary_key() const { return id; }
  uint64_t date_rkey() const { return (1ULL << 33) - post_time; }
  uint64_t rating_rkey() const { return (1 << 17) - rating; }
  uint128_t user_and_id_key() const { return ((uint128_t)user << 64) + id; }
  EOSLIB_SERIALIZE(question,
                   (id)(post_time)(user)(title)(ipfs_link)(answers)(comments)(
                       correct_answer_id)(rating)(properties)(history))
};

const scope_name all_questions = N(allquestions);
typedef eosio::multi_index<
    N(question), question,
    eosio::indexed_by<
        N(byposttime),
        eosio::const_mem_fun<question, uint64_t, &question::date_rkey>>,
    eosio::indexed_by<
        N(byrating),
        eosio::const_mem_fun<question, uint64_t, &question::rating_rkey>>,
    eosio::indexed_by<
        N(byowner),
        eosio::const_mem_fun<question, uint128_t, &question::user_and_id_key>>>
    question_index;

template <typename T>
void push_new_forum_item(std::vector<T> &container, T &item) {
  if (container.empty())
    item.id = FORUM_INDEX_START;
  else
    item.id = container.back().id + 1;
  container.push_back(item);
}

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

/*
Invariant 1:
  The id of answers or comments in question and answer vector are increases
  with index increasing.
  Used for binary search(methods post, delete, modifty, etc.)

Invariant 2:
  If question field {correct_answer_id} not equal to EMPTY_ANSWER
  Vector {answers} must contain answer with id equeal {correct_answer_id}
  Used in methood mmark_answer_as_correct
*/