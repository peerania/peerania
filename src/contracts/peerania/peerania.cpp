#include "peerania.hpp"
#include "peerania_account.cpp"
#include "peerania_communities_and_tags.cpp"
#include "peerania_forum.cpp"
#include "peerania_vote.cpp"

void peerania::registeracc(eosio::name user, std::string display_name,
                           std::string ipfs_profile) {
  require_auth(user);
  register_account(user, display_name, ipfs_profile);
}

void peerania::setaccstrprp(eosio::name user, uint8_t key, std::string value) {
  require_auth(user);
  set_account_string_property(user, key, value);
}

void peerania::setaccintprp(eosio::name user, uint8_t key, int32_t value) {
  require_auth(user);
  set_account_integer_property(user, key, value);
}

void peerania::setaccprof(eosio::name user, std::string ipfs_profile,
                          std::string display_name) {
  require_auth(user);
  set_account_profile(user, ipfs_profile, display_name);
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
                           uint16_t answer_id, std::string ipfs_link) {
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
                           uint16_t community_id, std::vector<uint32_t> tags,
                           std::string title, std::string ipfs_link) {
  require_auth(user);
  modify_question(user, question_id, community_id, tags, title, ipfs_link);
}

void peerania::modanswer(eosio::name user, uint64_t question_id,
                         uint16_t answer_id, std::string ipfs_link) {
  require_auth(user);
  modify_answer(user, question_id, answer_id, ipfs_link);
}
void peerania::modcomment(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id,
                          std::string ipfs_link) {
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

// Tags and communities
void peerania::crcommunity(eosio::name user, std::string name,
                           std::string ipfs_description,
                           std::vector<suggest_tag> suggested_tags) {
  require_auth(user);
  create_community(user, name, ipfs_description, suggested_tags);
}

void peerania::crtag(eosio::name user, uint16_t community_id, std::string name,
                     std::string ipfs_description) {
  require_auth(user);
  create_tag(user, community_id, name, ipfs_description);
}

void peerania::vtcrcomm(eosio::name user, uint32_t community_id) {
  require_auth(user);
  vote_create_community(user, community_id);
}

void peerania::vtcrtag(eosio::name user, uint16_t community_id,
                       uint32_t tag_id) {
  require_auth(user);
  vote_create_tag(user, community_id, tag_id);
}

void peerania::vtdelcomm(eosio::name user, uint32_t community_id) {
  require_auth(user);
  vote_delete_community(user, community_id);
}

void peerania::vtdeltag(eosio::name user, uint16_t community_id,
                        uint32_t tag_id) {
  require_auth(user);
  vote_delete_tag(user, community_id, tag_id);
}

void peerania::followcomm(eosio::name user, uint16_t community_id) {
  require_auth(user);
  follow_community(user, community_id);
}

void peerania::unfollowcomm(eosio::name user, uint16_t community_id) {
  require_auth(user);
  unfollow_community(user, community_id);
}

EOSIO_DISPATCH(
    peerania,
    (registeracc)(setaccintprp)(setaccstrprp)(setaccprof)(postquestion)(
        postanswer)(postcomment)(delquestion)(delanswer)(delcomment)(modanswer)(
        modquestion)(modcomment)(upvote)(downvote)(mrkascorrect)(votedelete)(
        crtag)(crcommunity)(vtcrtag)(vtcrcomm)(vtdeltag)(vtdelcomm)(followcomm)(
        unfollowcomm))