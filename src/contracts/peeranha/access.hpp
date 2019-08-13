#pragma once
#include <eosio/eosio.hpp>
#include "account.hpp"
#include "economy.h"

enum Action {
  MODIFY_QUESTION,
  DELETE_QUESTION,
  POST_QUESTION,
  MODIFY_ANSWER,
  DELETE_ANSWER,
  POST_ANSWER,
  MODIFY_COMMENT,
  DELETE_COMMENT,
  POST_COMMENT,
  SET_ACCOUNT_PROPERTY,
  SET_ACCOUNT_PROFILE,
  UPVOTE,
  DOWNVOTE,
  MARK_ANSWER_AS_CORRECT,
  VOTE_FOR_DELETION,
  VOTE_FOR_MODERATION,
  CREATE_TAG,
  CREATE_COMMUNITY,
  VOTE_CREATE_TAG,
  VOTE_CREATE_COMMUNITY,
  VOTE_DELETE_TAG,
  VOTE_DELETE_COMMUNITY,
  VOTE_REPORT_PROFILE,
};

void assert_allowed(const account &action_caller, eosio::name data_user,
                    Action action) {
  switch (action) {
    case POST_QUESTION:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= POST_QUESTION_ALLOWED,
                   "You can't post question!");
      break;
    case POST_ANSWER:
      if (action_caller.user == data_user)
        eosio::check(action_caller.rating >= POST_ANSWER_OWN_ALLOWED,
                     "You can't post answer to your question");
      else
        eosio::check(action_caller.rating >= POST_ANSWER_ALLOWED,
                     "You can't post answer to this question");
      break;
    case POST_COMMENT:
      if (action_caller.user == data_user)
        eosio::check(action_caller.rating >= POST_COMMENT_OWN_ALLOWED,
                     "You can't post comment for your item");
      else
        eosio::check(action_caller.rating >= POST_COMMENT_ALLOWED,
                     "You can't post comment for this item");
      break;
    case UPVOTE:
      eosio::check(action_caller.user != data_user,
                   "You cant upvote for your own items");
      eosio::check(action_caller.rating >= UPVOTE_ALLOWED,
                   "Your rating is too small to upvote");
      break;
    case DOWNVOTE:
      eosio::check(action_caller.user != data_user,
                   "You cant downvote for your own items");
      eosio::check(action_caller.rating >= DOWNVOTE_ALLOWED,
                   "Your rating is too small to downvote");
      break;
    case VOTE_FOR_DELETION:
      eosio::check(action_caller.user != data_user,
                   "You cant vote for deletion of your own items");
      eosio::check(action_caller.rating >= VOTE_FOR_DELETION_ALLOWED,
                   "Your rating is too small to put deletion flag");
      break;
    case CREATE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= CREATE_COMMUNITY_ALLOWED,
                   "Your rating is too small to create community!");
      break;
    case CREATE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= CREATE_TAG_ALLOWED,
                   "Your rating is too small to create tag!");
      break;
    case VOTE_CREATE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= VOTE_CREATE_COMMUNITY_ALLOWED,
                   "Your rating is too small to vote community!");
      break;
    case VOTE_CREATE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= VOTE_CREATE_TAG_ALLOWED,
                   "Your rating is too small to vote tag!");
      break;
    case VOTE_DELETE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= VOTE_DELETE_COMMUNITY_ALLOWED,
                   "Your rating is too small to vote for community deletion!");
      break;
    case VOTE_DELETE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      eosio::check(action_caller.rating >= VOTE_DELETE_TAG_ALLOWED,
                   "Your rating is too small to vote for tag deletion!");
      break;
    case VOTE_REPORT_PROFILE:
      eosio::check(action_caller.user != data_user,
                   "You can't report own profile");
      eosio::check(action_caller.rating >= REPORT_PROFILE_ALLOWED,
                   "Your rating is too small to report profile");
      break;
    default:
      eosio::check(action_caller.user == data_user, "Action not allowed");
      break;
  }
}
