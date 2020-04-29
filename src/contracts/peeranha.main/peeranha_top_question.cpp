#include "peeranha.hpp"
#include <stdint.h>

void peeranha::add_top_question(eosio::name user, uint16_t community_id, uint64_t question_id) {
  top_question_index top_question_table(_self, scope_all_top_questions);
  assert_community_exist(community_id);

  question_index question_table(_self, scope_all_questions);      
  auto _iter_community = question_table.find(question_id);        
  eosio::check(_iter_community != question_table.end() , "check valid question");

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
          eosio::check(iter_top_question == top_question.top_questions.end() , "question has already been added");
          top_question.top_questions.push_back(question_id);
        });
  }
}

void peeranha::remove_top_question(eosio::name user, uint16_t community_id, uint64_t question_id){  
  top_question_index top_question_table(_self, scope_all_top_questions);
  assert_community_exist(community_id);
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

void peeranha::up_question(eosio::name user, uint16_t community_id, uint64_t question_id){
  top_question_index top_question_table(_self, scope_all_top_questions);
  assert_community_exist(community_id);
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

void peeranha::down_question(eosio::name user, uint16_t community_id, uint64_t question_id){
  top_question_index top_question_table(_self, scope_all_top_questions);
  assert_community_exist(community_id);
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

void peeranha::move_question(eosio::name user, uint16_t community_id, uint64_t question_id,  uint16_t new_position){
  top_question_index top_question_table(_self, scope_all_top_questions);
  assert_community_exist(community_id);
  auto iter_community = top_question_table.find(community_id);
  
  if (iter_community != top_question_table.end()) {
    top_question_table.modify(
      iter_community, _self, [question_id, new_position](auto &top_question) {
        eosio::check(new_position >= 1 && new_position <=top_question.top_questions.size(), "wrong position");
        auto iter_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
        eosio::check(iter_question != top_question.top_questions.end(), "nonexistent question");
        top_question.top_questions.erase(iter_question);
        auto position = new_position + top_question.top_questions.begin() - 1;
        top_question.top_questions.insert(position, question_id);
        });
  }
}
