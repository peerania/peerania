#include "peeranha.hpp"
#include <stdint.h>

#define  LIMIT_MAX_QUESTION 100

void peeranha::add_top_question(eosio::name user, uint16_t community_id, uint64_t question_id) {
  assert_community_exist(community_id);
  eosio::check(find_account_property_community(user, COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION, community_id), "user not found or user without rights");
  question_index question_table(_self, scope_all_questions);
  auto iter_question = question_table.find(question_id);
  eosio::check(iter_question != question_table.end(), "question not found");
  eosio::check(iter_question->community_id == community_id, "wrong community, question in another community");

  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_community = top_question_table.find(community_id);
  if (iter_community == top_question_table.end()) {
    top_question_table.emplace(
      _self, [community_id, question_id](auto &top_question) {
        top_question.community_id = community_id;
        top_question.top_questions.push_back(question_id);
      });
  } else {
    top_question_table.modify(
      iter_community, _self, [question_id](auto &top_question) {
        auto iter_top_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        eosio::check(iter_top_question == top_question.top_questions.end(), "question has already been added");
        eosio::check(top_question.top_questions.size() <= LIMIT_MAX_QUESTION, "added maximum number of questions");
        top_question.top_questions.push_back(question_id);
      });
  }
}

void peeranha::remove_top_question(eosio::name user, uint16_t community_id, uint64_t question_id) {  
  assert_community_exist(community_id);
  eosio::check(find_account_property_community(user, COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION, community_id), "user not found or user without rights");
  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_community = top_question_table.find(community_id);
  if (iter_community != top_question_table.end()) {
    top_question_table.modify(
      iter_community, _self, [question_id](auto &top_question) {
        auto iter_top_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        eosio::check(iter_top_question != top_question.top_questions.end(), "nonexistent question");
        top_question.top_questions.erase(iter_top_question);
      });
  }
}

void peeranha::delete_top_question(uint16_t community_id, uint64_t question_id) {  
  assert_community_exist(community_id);
  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_community = top_question_table.find(community_id);
  if (iter_community != top_question_table.end()) {
    top_question_table.modify(
      iter_community, _self, [question_id](auto &top_question) {
        auto iter_top_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        if(iter_top_question != top_question.top_questions.end())
          top_question.top_questions.erase(iter_top_question);
      });
  }
}

void peeranha::up_top_question(eosio::name user, uint16_t community_id, uint64_t question_id) {
  assert_community_exist(community_id);
  eosio::check(find_account_property_community(user, COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION, community_id), "user not found or user without rights");
  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_community = top_question_table.find(community_id);
  if (iter_community != top_question_table.end()) {
    top_question_table.modify(
      iter_community, _self, [question_id](auto &top_question) {
        auto iter_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        eosio::check(iter_question != top_question.top_questions.begin(), "the question is already the first");
        eosio::check(iter_question != top_question.top_questions.end(), "nonexistent question");
        std::swap(*iter_question, *(iter_question - 1));
      });
  }
}

void peeranha::down_top_question(eosio::name user, uint16_t community_id, uint64_t question_id) {
  assert_community_exist(community_id);
  eosio::check(find_account_property_community(user, COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION, community_id), "user not found or user without rights");
  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_community = top_question_table.find(community_id);
  if (iter_community != top_question_table.end()) {
    top_question_table.modify(
      iter_community, _self, [question_id](auto &top_question) {
        auto iter_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        eosio::check(iter_question != top_question.top_questions.end(), "the question is already the last");
        eosio::check(iter_question != top_question.top_questions.end(), "nonexistent question");
        std::swap(*iter_question, *(iter_question + 1));
      });
  }
}

void peeranha::move_top_question(eosio::name user, uint16_t community_id, uint64_t question_id,  uint16_t new_position) {
  assert_community_exist(community_id);
  eosio::check(find_account_property_community(user, COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION, community_id), "user not found or user without rights");
  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_community = top_question_table.find(community_id);
  
  if (iter_community != top_question_table.end()) {
    top_question_table.modify(
      iter_community, _self, [question_id, new_position](auto &top_question) {
        eosio::check(new_position >= 0 && new_position <=top_question.top_questions.size(), "wrong position");
        auto iter_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        eosio::check(iter_question != top_question.top_questions.end(), "nonexistent question");
        top_question.top_questions.erase(iter_question);
        auto position = new_position + top_question.top_questions.begin();
        top_question.top_questions.insert(position, question_id);
      });
  }
}