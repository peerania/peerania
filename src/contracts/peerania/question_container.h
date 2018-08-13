#pragma once
#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>

/// @abi table
struct question {
  uint64_t id;          //unique for both question and answer table
  account_name user;
  std::string ipfs_link;
  // additionl info
  uint64_t primary_key() const { return id; }
  EOSLIB_SERIALIZE(question, (id)(user)(ipfs_link))
};


/// @abi table
struct answer{
  uint64_t id;          //unique for both question and answer table
  account_name user;
  std::string ipfs_link;
  // additionl info
  uint64_t primary_key() const { return id; }
  EOSLIB_SERIALIZE(answer, (id)(user)(ipfs_link))
}

/// @abi table
struct comment {
  uint64_t id;          //useless on front
  uint64_t parrent_id;  //id of answer or question
  account_name user;
  std::string ipfs_link;
  uint64_t primary_key() const { return id; }
  EOSLIB_SERIALIZE(comment, (id)(user)(ipfslink)(next_comment)
};

typedef multi_index<N(question), question> question_index;
typedef multi_index<N(answer), answer> answer_index;
typedef multi_index<N(comment), comment> comment_index;