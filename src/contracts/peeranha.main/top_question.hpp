#pragma once
#include <eosio/eosio.hpp>
#include <vector>

struct [[eosio::table("topquestion"), eosio::contract("peeranha.main")]] top_question {
  uint64_t community_id;
  std::vector<uint64_t> top_questions;

  uint64_t primary_key() const { return community_id; }
};
typedef eosio::multi_index<"topquestion"_n, top_question> top_question_index;
const uint64_t scope_all_top_questions = eosio::name("alltopquest").value;