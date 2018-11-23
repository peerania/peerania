#include "peerania.hpp"
#include "peerania_account.cpp"
#include "peerania_forum.cpp"
#include "peerania_vote.cpp"

void peerania::registeracc(eosio::name owner, std::string display_name,
                           std::string ipfs_profile) {
  require_auth(owner);
  register_account(owner, display_name, ipfs_profile);
}

void peerania::setaccstrprp(eosio::name owner, uint8_t key,
                            std::string value) {
  require_auth(owner);
  set_account_string_property(owner, key, value);
}

void peerania::setaccintprp(eosio::name owner, uint8_t key, int32_t value) {
  require_auth(owner);
  set_account_integer_property(owner, key, value);
}

void peerania::setipfspro(eosio::name owner, std::string ipfs_profile) {
  require_auth(owner);
  set_account_ipfs_profile(owner, ipfs_profile);
}

void peerania::setdispname(eosio::name owner, std::string display_name) {
  require_auth(owner);
  set_account_display_name(owner, display_name);
}

void peerania::postquestion(eosio::name user, std::string title,
                            std::string ipfs_link) {
  require_auth(user);
  post_question(user, title, ipfs_link);
}

void peerania::postanswer(eosio::name user, uint64_t question_id,
                          std::string ipfs_link) {
  require_auth(user);
  post_answer(user, question_id, ipfs_link);
}

void peerania::postcomment(eosio::name user, uint64_t question_id,
                           uint16_t answer_id, const std::string &ipfs_link) {
  require_auth(user);
  post_comment(user, question_id, answer_id, ipfs_link);
}

void peerania::delquestion(eosio::name user, uint64_t question_id) {
  require_auth(user);
  delete_question(user, question_id);
}

void peerania::delanswer(eosio::name user, uint64_t question_id,
                         uint16_t answer_id) {
  require_auth(user);
  delete_answer(user, question_id, answer_id);
}

void peerania::delcomment(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id) {
  require_auth(user);
  delete_comment(user, question_id, answer_id, comment_id);
}

void peerania::modquestion(eosio::name user, uint64_t question_id,
                           const std::string &title,
                           const std::string &ipfs_link) {
  require_auth(user);
  modify_question(user, question_id, title, ipfs_link);
}

void peerania::modanswer(eosio::name user, uint64_t question_id,
                         uint16_t answer_id, const std::string &ipfs_link) {
  require_auth(user);
  modify_answer(user, question_id, answer_id, ipfs_link);
}
void peerania::modcomment(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id,
                          const std::string &ipfs_link) {
  require_auth(user);
  modify_comment(user, question_id, answer_id, comment_id, ipfs_link);
}

void peerania::upvote(eosio::name user, uint64_t question_id,
                      uint16_t answer_id) {
  require_auth(user);
  vote(user, question_id, answer_id, true);
}

void peerania::downvote(eosio::name user, uint64_t question_id,
                        uint16_t answer_id) {
  require_auth(user);
  vote(user, question_id, answer_id, false);
}

void peerania::mrkascorrect(eosio::name user, uint64_t question_id,
                            uint16_t answer_id) {
  require_auth(user);
  mark_answer_as_correct(user, question_id, answer_id);
}

void peerania::votedelete(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id) {
  require_auth(user);
  vote_for_deletion(user, question_id, answer_id, comment_id);
}

void peerania::votemoderate(eosio::name user, uint64_t question_id,
                            uint16_t answer_id, uint16_t comment_id) {}

#ifdef DEBUG
void peerania::setaccrtmpc(eosio::name user, int16_t rating,
                           uint16_t moderation_points) {
  auto itr = find_account(user);
  account_table.modify(itr, _self, [&](auto &account) {
    account.rating = rating;
    account.moderation_points = moderation_points;
  });
}

void peerania::resettables() {
  auto iter_account = account_table.begin();
  while (iter_account != account_table.end()) {
    // clean reward tables for user
    auto period_rating_table = period_rating_index(_self, iter_account->owner.value);
    auto iter_period_rating = period_rating_table.begin();
    while (iter_period_rating != period_rating_table.end()) {
      iter_period_rating = period_rating_table.erase(iter_period_rating);
    }

    // remove user
    iter_account = account_table.erase(iter_account);
  }

  // clean reward total
  auto iter_total_rating = total_rating_table.begin();
  while (iter_total_rating != total_rating_table.end()) {
    iter_total_rating = total_rating_table.erase(iter_total_rating);
  }

  // clean constants
  constants_index all_constants_table(_self, scope_all_constants);
  auto iter_constants = all_constants_table.begin();
  while (iter_constants != all_constants_table.end()) {
    iter_constants = all_constants_table.erase(iter_constants);
  }

  // clean forum
  auto iter_question = question_table.begin();
  while (iter_question != question_table.end())
    iter_question = question_table.erase(iter_question);
}

void peerania::chnguserrt(eosio::name user, int16_t rating_change) {
  update_rating(user, rating_change);
}

void peerania::setquestrt(uint64_t question_id, int16_t rating) {
  auto iter_question = find_question(question_id);
  question_table.modify(iter_question, _self,
                        [rating](auto &question) { question.rating = rating; });
}

#endif

#ifndef DEBUG
EOSIO_DISPATCH(peerania,
          (registeracc)(setaccintprp)(setaccstrprp)(setipfspro)(setdispname)(
              postquestion)(postanswer)(postcomment)(delquestion)(delanswer)(
              delcomment)(modanswer)(modquestion)(modcomment)(upvote)(downvote)(
              mrkascorrect)(votedelete)(votemoderate))
#else
EOSIO_DISPATCH(peerania,
          (registeracc)(setaccintprp)(setaccstrprp)(setipfspro)(setdispname)(
              postquestion)(postanswer)(postcomment)(delquestion)(delanswer)(
              delcomment)(modanswer)(modquestion)(modcomment)(upvote)(downvote)(
              mrkascorrect)(votedelete)(votemoderate)(setaccrtmpc)(resettables)(
              chnguserrt)(setquestrt))
#endif