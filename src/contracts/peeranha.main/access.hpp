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

void check_rating(const account &acc, const int rating, const char *msg, uint16_t community_id) {
  bool global_moderator_flag = acc.has_moderation_flag(MODERATOR_FLG_IGNORE_RATING);
  bool community_moderator_flag = (community_id != 0) && find_account_property_community(acc.user, COMMUNITY_ADMIN_FLG_IGNORE_RATING, community_id);

  if (global_moderator_flag || community_moderator_flag)
    return;
  eosio::check(acc.rating >= rating, msg);
}

void assert_allowed(const account &action_caller, eosio::name data_user,
                    Action action, uint16_t community_id = 0) {
  switch (action) {
    case POST_QUESTION:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, POST_QUESTION_ALLOWED,
                   "You can't post question!", community_id);
      break;
    case POST_ANSWER:
      if (action_caller.user == data_user)
        check_rating(action_caller, POST_ANSWER_OWN_ALLOWED,
                     "You can't post answer to your question", community_id);
      else
        check_rating(action_caller, POST_ANSWER_ALLOWED,
                     "You can't post answer to this question", community_id);
      break;
    case POST_COMMENT:
      if (action_caller.user == data_user)
        check_rating(action_caller, POST_COMMENT_OWN_ALLOWED,
                     "You can't post comment for your item", community_id);
      else
        check_rating(action_caller, POST_COMMENT_ALLOWED,
                     "You can't post comment for this item", community_id);
      break;
    case UPVOTE:
      eosio::check(action_caller.user != data_user,
                   "You cant upvote for your own items");
      check_rating(action_caller, UPVOTE_ALLOWED,
                   "Your rating is too small to upvote", community_id);
      break;
    case DOWNVOTE:
      eosio::check(action_caller.user != data_user,
                   "You cant downvote for your own items");
      check_rating(action_caller, DOWNVOTE_ALLOWED,
                   "Your rating is too small to downvote", community_id);
      break;
    case REPORT_FORUM_ITEM:
      eosio::check(action_caller.user != data_user,
                   "You cant vote for deletion of your own items");
      check_rating(action_caller, VOTE_FOR_DELETION_ALLOWED,
                   "Your rating is too small to put deletion flag", community_id);
      break;
    case CREATE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, CREATE_COMMUNITY_ALLOWED,
                   "Your rating is too small to create community!", community_id);
      break;
    case CREATE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, CREATE_TAG_ALLOWED,
                   "Your rating is too small to create tag!", community_id);
      break;
    case VOTE_CREATE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
     check_rating(action_caller, VOTE_CREATE_COMMUNITY_ALLOWED,
                   "Your rating is too small to vote community!", community_id);
      break;
    case VOTE_CREATE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, VOTE_CREATE_TAG_ALLOWED,
                   "Your rating is too small to vote tag!", community_id);
      break;
    case VOTE_DELETE_COMMUNITY:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, VOTE_DELETE_COMMUNITY_ALLOWED,
                   "Your rating is too small to vote for community deletion!", community_id);
      break;
    case VOTE_DELETE_TAG:
      eosio::check(action_caller.user == data_user,
                   "Internal function call error");
      check_rating(action_caller, VOTE_DELETE_TAG_ALLOWED,
                   "Your rating is too small to vote for tag deletion!", community_id);
      break;
    case VOTE_REPORT_PROFILE:
      eosio::check(action_caller.user != data_user,
                   "You can't report own profile");
      check_rating(action_caller, REPORT_PROFILE_ALLOWED,
                   "Your rating is too small to report profile", community_id);
      break;
    default:
      eosio::check(action_caller.user == data_user, "Action not allowed");
      break;
  }
}