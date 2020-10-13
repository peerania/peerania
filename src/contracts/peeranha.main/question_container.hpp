#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "IpfsHash.hpp"
#include "account.hpp"
#include "history.hpp"
#include "property.hpp"

// Answer id starts from FORUM_INDEX_START
#define EMPTY_ANSWER_ID 0

// Return true if the action must be applied to question
#define apply_to_question(answer_id) ((answer_id) == EMPTY_ANSWER_ID)

// Comment id starts from FORUM_INDEX_START
#define EMPTY_COMMENT_ID 0

// Return true if the action must be applied to answer
#define apply_to_answer(comment_id) ((comment_id) == EMPTY_COMMENT_ID)

#define FORUM_INDEX_START 1

#define MAX_ANSWER_COUNT 200
#define MAX_COMMENT_COUNT 200

#define PROPERTY_REPORT_POINTS 1
#define PROPERTY_MODERATION_VOTES 2
#define PROPERTY_LAST_MODIFIED 3
#define PROPERTY_QUESTION_TYPE 4
#define PROPERTY_OFFICIAL_ANSWER 10
#define PROPERTY_ANSWER_15_MINUTES 12   //(12 - achive id)
#define PROPERTY_FIRST_ANSWER 13        //(13 - achive id)
#define PROPERTY_EMPTY_ANSWER 15
#define PROPERTY_EMPTY_QUESTION 15

#define MAX_QUESTION_ID 0xfffffffffULL

#define QUESTION_TYPE_EXPERT 0
#define QUESTION_TYPE_GENERAL 1


struct comment {
  uint16_t id;
  time post_time;
  eosio::name user;
  IpfsHash ipfs_link;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint16_t bkey() const { return id; }
  EOSLIB_SERIALIZE(comment,
                   (id)(post_time)(user)(ipfs_link)(properties)(history))
};

struct answer {
  uint16_t id;
  time post_time;
  eosio::name user;
  IpfsHash ipfs_link;
  std::vector<comment> comments;
  // additional info
  int16_t rating = 0;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint16_t bkey() const { return id; }
  EOSLIB_SERIALIZE(answer, (id)(post_time)(user)(ipfs_link)(comments)(rating)(
                               properties)(history))
};

struct [[
  eosio::table("question"), eosio::contract("peeranha.main")
]] question {
  uint64_t id;
  uint16_t community_id;
  std::vector<uint32_t> tags;
  time post_time;
  eosio::name user;
  std::string title;
  IpfsHash ipfs_link;
  std::vector<answer> answers;
  std::vector<comment> comments;
  // additionl info
  uint16_t correct_answer_id = 0;
  int16_t rating = 0;
  std::vector<int_key_value> properties;
  std::vector<history_item> history;
  uint64_t primary_key() const { return id; }
  uint64_t community_skey() const {
    return (static_cast<uint64_t>(community_id) << 36) + id;
  }
  EOSLIB_SERIALIZE(
      question,
      (id)(community_id)(tags)(post_time)(user)(title)(ipfs_link)(answers)(
          comments)(correct_answer_id)(rating)(properties)(history))
};

const uint64_t scope_all_questions = eosio::name("allquestions").value;
typedef eosio::multi_index<
    "question"_n, question,
    eosio::indexed_by<
        "community"_n,
        eosio::const_mem_fun<question, uint64_t, &question::community_skey>>>
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
  eosio::check(iter_answer != q.answers.end(), "Answer not found");
  return iter_answer;
}

template <typename T>
std::vector<comment>::iterator find_comment(T &item, uint16_t comment_id) {
  auto iter_comment =
      binary_find(item.comments.begin(), item.comments.end(), comment_id);
  eosio::check(iter_comment != item.comments.end(), "Comment not found");
  return iter_comment;
}

#ifdef SUPERFLUOUS_INDEX
struct [[
  eosio::table("usrquestions"),
  eosio::contract("peeranha.main")
]] usrquestions {
  uint64_t question_id;
  uint64_t primary_key() const { return question_id; }
};
typedef eosio::multi_index<"usrquestions"_n, usrquestions> user_questions_index;

struct [[
  eosio::table("usranswers"), eosio::contract("peeranha.main")
]] usranswers {
  uint64_t question_id;
  uint16_t answer_id;
  uint64_t primary_key() const { return question_id; }
};
typedef eosio::multi_index<"usranswers"_n, usranswers> user_answers_index;
#endif


inline void assert_title(const std::string &title) {
  assert_readble_string(title, 3, 256, "Invalid title length");
}

inline void assert_question_type(int question_type){
  eosio::check(question_type <= QUESTION_TYPE_GENERAL, "Question type not exists");
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

int_key_value add_official_answer()
{
  int_key_value key_value;
  key_value.key = PROPERTY_OFFICIAL_ANSWER;
  key_value.value = 1;
  return key_value;
}