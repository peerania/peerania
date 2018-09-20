#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
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
  SET_ACCOUNT_IPFS_PROFILE,
  SET_ACCOUNT_DISPLAYNAME,
  UPVOTE,
  DOWNVOTE,
  MARK_ANSWER_AS_CORRECT,
  VOTE_FOR_DELETION,
  VOTE_FOR_MODERATION
};


void assert_allowed(const account &action_caller, account_name data_owner,
                    Action action) {
  switch (action) {
    case POST_ANSWER:
      if (action_caller.owner == data_owner)
        eosio_assert(action_caller.rating >= POST_ANSWER_OWN_ALLOWED,
                     "You can't post answer to your question");
      else
        eosio_assert(action_caller.rating >= POST_ANSWER_ALLOWED,
                     "You can't post answer to this question");
      break;
    case POST_COMMENT:
      if (action_caller.owner == data_owner)
        eosio_assert(action_caller.rating >= POST_COMMENT_OWN_ALLOWED,
                     "You can't post comment for your item");
      else
        eosio_assert(action_caller.rating >= POST_COMMENT_ALLOWED,
                     "You can't post comment for this item");
      break;
    case UPVOTE:
      eosio_assert(action_caller.owner != data_owner,
                   "You cant upvote for your own items");
      eosio_assert(action_caller.rating >= UPVOTE_ALLOWED,
                   "Your rating is too small to upvote");
      break;
    case DOWNVOTE:
      eosio_assert(action_caller.owner != data_owner,
                   "You cant downvote for your own items");
      eosio_assert(action_caller.rating >= DOWNVOTE_ALLOWED,
                   "Your rating is too small to downvote");
      break;
    case VOTE_FOR_DELETION:
      eosio_assert(action_caller.owner != data_owner,
                   "You cant vote for deletion of your own items");
      eosio_assert(action_caller.rating >= VOTE_FOR_DELETION_ALLOWED,
                   "Your rating is too small to put deletion flag");
      break;
    case POST_QUESTION:
        eosio_assert(action_caller.owner != data_owner, "Internal function call error");
        eosio_assert(action_caller.rating >= POST_QUESTION_ALLOWED,
                    "You can't post question!");
    default:
      eosio_assert(action_caller.owner == data_owner, "Action not allowed");
      break;
  }
}