#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include "account.hpp"


class access {
 public:
  enum ACTION {
    MODIFY_QUESTION,
    DELETE_QUESTION,
    REGISTER_QUESTION,
    MODIFY_ANSWER,
    DELETE_ANSWER,
    REGISTER_ANSWER,
    MODIFY_COMMENT,
    DELETE_COMMENT,
    REGISTER_COMMENT,
    SET_ACCOUNT_PROPERTY,
    SET_ACCOUNT_IPFS_PROFILE,
    SET_ACCOUNT_DISPLAYNAME,
    UPVOTE,
    DOWNVOTE,
    MARK_ANSWER_AS_CORRECT
  };

  access(const account &owner, ACTION action) {
    access_owner = owner;
    access_action = action;
  }

  account_name get_account_name() const { return access_owner.owner; }

  bool is_allowed(account_name data_owner) const {
    if (data_owner == access_owner.owner) return true;
    return false;
  }

  bool is_allowed() const {
    return true;
  }
 private:
  account access_owner;
  ACTION access_action;
};