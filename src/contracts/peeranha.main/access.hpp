#pragma once
#include <eosio/eosio.hpp>
#include "account.hpp"
#include "economy.h"
#include "peeranha_types.h"
#include "property.hpp"

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
  REPORT_FORUM_ITEM,
  VOTE_FOR_MODERATION,
  CREATE_TAG,
  CREATE_COMMUNITY,
  VOTE_CREATE_TAG,
  VOTE_CREATE_COMMUNITY,
  VOTE_DELETE_TAG,
  VOTE_DELETE_COMMUNITY,
  VOTE_REPORT_PROFILE,
};

void check_rating(const account &acc, const int rating, const char *msg) {
  if (!acc.has_moderation_flag(MODERATOR_FLG_IGNORE_RATING))
    eosio::check(acc.rating >= rating, msg);
}

void assert_allowed(const account &action_caller, eosio::name data_user,
                    Action action) {
  switch (action) {
    case POST_QUESTION:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, POST_QUESTION_ALLOWED,
                   "You can't post question!");
      break;
    case POST_ANSWER:
      if (action_caller.user == data_user)
        check_rating(action_caller, POST_ANSWER_OWN_ALLOWED,
                     "You can't post answer to your question");
      else
        check_rating(action_caller, POST_ANSWER_ALLOWED,
                     "You can't post answer to this question");
      break;
    case POST_COMMENT:
      if (action_caller.user == data_user)
        check_rating(action_caller, POST_COMMENT_OWN_ALLOWED,
                     "You can't post comment for your item");
      else
        check_rating(action_caller, POST_COMMENT_ALLOWED,
                     "You can't post comment for this item");
      break;
    case UPVOTE:
      eosio::check(action_caller.user != data_user,
                   "You cant upvote for your own items");
      check_rating(action_caller, UPVOTE_ALLOWED,
                   "Your rating is too small to upvote");
      break;
    case DOWNVOTE:
      eosio::check(action_caller.user != data_user,
                   "You cant downvote for your own items");
      check_rating(action_caller, DOWNVOTE_ALLOWED,
                   "Your rating is too small to downvote");
      break;
    case REPORT_FORUM_ITEM:
      eosio::check(action_caller.user != data_user,
                   "You cant vote for deletion of your own items");
      check_rating(action_caller, VOTE_FOR_DELETION_ALLOWED,
                   "Your rating is too small to put deletion flag");
      break;
    case CREATE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, CREATE_COMMUNITY_ALLOWED,
                   "Your rating is too small to create community!");
      break;
    case CREATE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, CREATE_TAG_ALLOWED,
                   "Your rating is too small to create tag!");
      break;
    case VOTE_CREATE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
     check_rating(action_caller, VOTE_CREATE_COMMUNITY_ALLOWED,
                   "Your rating is too small to vote community!");
      break;
    case VOTE_CREATE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, VOTE_CREATE_TAG_ALLOWED,
                   "Your rating is too small to vote tag!");
      break;
    case VOTE_DELETE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, VOTE_DELETE_COMMUNITY_ALLOWED,
                   "Your rating is too small to vote for community deletion!");
      break;
    case VOTE_DELETE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, VOTE_DELETE_TAG_ALLOWED,
                   "Your rating is too small to vote for tag deletion!");
      break;
    case VOTE_REPORT_PROFILE:
      eosio::check(action_caller.user != data_user,
                   "You can't report own profile");
      check_rating(action_caller, REPORT_PROFILE_ALLOWED,
                   "Your rating is too small to report profile");
      break;
    default:
      eosio::check(action_caller.user == data_user, "Action not allowed");
      break;
  }
}