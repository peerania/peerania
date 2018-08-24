#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include "account.hpp"

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
  VOTE,
  MARK_ANSWER_AS_CORRECT,
  VOTE_FOR_DELETION,
  VOTE_FOR_MODERATION
};

void assert_allowed(const account &action_caller, const account &data_owner,
                    Action action) {}

void assert_allowed(const account &action_caller, Action action) {}

void assert_allowed(const account &action_caller, account_name data_owner,
                    Action action) {
  switch (action) {
    case VOTE_FOR_DELETION:
      eosio_assert(action_caller.owner != data_owner, "Action not allowed");
      break;
    default:
      eosio_assert(action_caller.owner == data_owner, "Action not allowed");
      break;
  }
}

void assert_allowed(account_name action_caller, account_name data_owner,
                    Action action) {
  eosio_assert(action_caller == data_owner, "Action not allowed");
}