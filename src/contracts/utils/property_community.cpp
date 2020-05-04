#pragma once
#include "peeranha.hpp"
//#include "property_community.hpp"
#include <stdint.h>


void peeranha::give_moderator_flag(eosio::name user, int flags, uint16_t community_id) {
  assert_community_exist(community_id);
  property_community_index property_community_table(_self, scope_all_property_community);

  auto iter_user = property_community_table.find(user.value);
  if (iter_user == property_community_table.end()) {
    property_community_table.emplace(
    _self, [flags, community_id](auto &properties) {
      key_community key_value;
      key_value.community = community_id;
      key_value.value = key_value.value | flags;
      propert_community_table.properties.push_back(key_value);
  });
  
  } /*else {
    top_question_table.modify(
        iter_community, _self, [question_id](auto &top_question) {
          auto iter_top_question = find(top_question.top_questions.begin(), top_question.top_questions.end(), question_id);
          eosio::check(iter_top_question == top_question.top_questions.end() , "question has already been added");
          eosio::check(top_question.top_questions.size() <= LIMIT_MAX_QUESTION , "added maximum number of questions");
          top_question.top_questions.push_back(question_id);
        });
        */
  }