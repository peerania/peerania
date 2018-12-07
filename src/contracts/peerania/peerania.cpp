#include "peerania.hpp"
#include "peerania_account.cpp"
#include "peerania_communities_and_tags.cpp"
#include "peerania_forum.cpp"
#include "peerania_vote.cpp"

void peerania::registeracc(eosio::name owner, std::string display_name,
                           std::string ipfs_profile) {
  require_auth(owner);
  register_account(owner, display_name, ipfs_profile);
}

void peerania::setaccstrprp(eosio::name owner, uint8_t key, std::string value) {
  require_auth(owner);
  set_account_string_property(owner, key, value);
}

void peerania::setaccintprp(eosio::name owner, uint8_t key, int32_t value) {
  require_auth(owner);
  set_account_integer_property(owner, key, value);
}

void peerania::setaccprof(eosio::name owner, std::string ipfs_profile,
                          std::string display_name) {
  require_auth(owner);
  set_account_profile(owner, ipfs_profile, display_name);
}

void peerania::postquestion(eosio::name user, uint16_t community_id,
                            std::vector<uint32_t> tags, std::string title,
                            std::string ipfs_link) {
  require_auth(user);
  post_question(user, community_id, tags, title, ipfs_link);
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
  vote_forum_item(user, question_id, answer_id, true);
}

void peerania::downvote(eosio::name user, uint64_t question_id,
                        uint16_t answer_id) {
  require_auth(user);
  vote_forum_item(user, question_id, answer_id, false);
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

// stub
void peerania::votemoderate(eosio::name user, uint64_t question_id,
                            uint16_t answer_id, uint16_t comment_id) {}

// Tags and communities
void peerania::crcommunity(eosio::name user, const std::string &name,
                           const std::string &ipfs_description) {
  require_auth(user);
  create_community_or_tag(user, name, ipfs_description, ID_CREATE_COMMUNITY);
}

void peerania::crtag(eosio::name user, uint16_t community_id, std::string name,
                     std::string ipfs_description) {
  require_auth(user);
  eosio_assert(community_id != ID_CREATE_COMMUNITY, "Invalid community id");
  create_community_or_tag(user, name, ipfs_description, community_id);
}

void peerania::vtcrcomm(eosio::name user, uint16_t community_id) {
  require_auth(user);
  vote_create_community_or_tag(user, community_id, ID_CREATE_COMMUNITY);
}

void peerania::vtcrtag(eosio::name user, uint16_t community_id,
                       uint32_t tag_id) {
  require_auth(user);
  eosio_assert(community_id != ID_CREATE_COMMUNITY, "Invalid community id");
  vote_create_community_or_tag(user, tag_id, community_id);
}

void peerania::vtdelcomm(eosio::name user, uint16_t community_id) {
  require_auth(user);
  vote_delete_community_or_tag(user, community_id, ID_CREATE_COMMUNITY);
}

void peerania::vtdeltag(eosio::name user, uint16_t community_id,
                        uint32_t tag_id) {
  require_auth(user);
  eosio_assert(community_id != ID_CREATE_COMMUNITY, "Invalid community id");
  vote_delete_community_or_tag(user, tag_id, community_id);
}

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
    period_rating_index period_rating_table(_self, iter_account->owner.value);
    auto iter_period_rating = period_rating_table.begin();
    while (iter_period_rating != period_rating_table.end()) {
      iter_period_rating = period_rating_table.erase(iter_period_rating);
    }

    // clean user_questions table
    user_questions_index user_questions_table(_self, iter_account->owner.value);
    auto iter_user_questions = user_questions_table.begin();
    while (iter_user_questions != user_questions_table.end()) {
      iter_user_questions = user_questions_table.erase(iter_user_questions);
    }

    // clean user_answers table
    user_answers_index user_answers_table(_self, iter_account->owner.value);
    auto iter_user_answers = user_answers_table.begin();
    while (iter_user_answers != user_answers_table.end()) {
      iter_user_answers = user_answers_table.erase(iter_user_answers);
    }

    // clean create community table
    create_tag_community_index create_community_table(_self,
                                                      scope_all_communities);
    auto iter_create_community = create_community_table.begin();
    while (iter_create_community != create_community_table.end()) {
      iter_create_community =
          create_community_table.erase(iter_create_community);
    }

    // clean create tags and tags tables
    tag_community_index community_table(_self, scope_all_communities);
    auto iter_community = community_table.begin();
    while (iter_community != community_table.end()) {
      // clean all tags for creation
      create_tag_community_index create_tag_table(
          _self, get_tag_scope(iter_community->id));
      auto iter_create_tag = create_tag_table.begin();
      while (iter_create_tag != create_tag_table.end()) {
        iter_create_tag = create_tag_table.erase(iter_create_tag);
      }

      // Clean tags
      tag_community_index tag_table(_self, get_tag_scope(iter_community->id));
      auto iter_tag = tag_table.begin();
      while (iter_tag != tag_table.end()) {
        iter_tag = tag_table.erase(iter_tag);
      }

      iter_community = community_table.erase(iter_community);
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

#endif

#ifndef DEBUG
EOSIO_DISPATCH(peerania,
               (registeracc)(setaccintprp)(setaccstrprp)(setaccprof)(
                   postquestion)(postanswer)(postcomment)(delquestion)(
                   delanswer)(delcomment)(modanswer)(modquestion)(modcomment)(
                   upvote)(downvote)(mrkascorrect)(votedelete)(votemoderate)(
                   crtag)(crcommunity)(vtcrtag)(vtcrcomm)(vtdeltag)(vtdelcomm))
#else
EOSIO_DISPATCH(
    peerania,
    (registeracc)(setaccintprp)(setaccstrprp)(setaccprof)(postquestion)(
        postanswer)(postcomment)(delquestion)(delanswer)(delcomment)(modanswer)(
        modquestion)(modcomment)(upvote)(downvote)(mrkascorrect)(votedelete)(
        votemoderate)(crtag)(crcommunity)(vtcrtag)(vtcrcomm)(vtdeltag)(
        vtdelcomm)(setaccrtmpc)(resettables)(chnguserrt))
#endif