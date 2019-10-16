#include "peeranha.hpp"
#include "peeranha_account.cpp"
#include "peeranha_communities_and_tags.cpp"
#include "peeranha_forum.cpp"
#include "peeranha_vote.cpp"

void peeranha::registeracc(eosio::name user, std::string display_name,
                           std::string ipfs_profile, std::string ipfs_avatar) {
  require_auth(user);
  register_account(user, display_name, ipfs_profile, ipfs_avatar);
}

void peeranha::setaccprof(eosio::name user, std::string ipfs_profile,
                          std::string display_name, std::string ipfs_avatar) {
  require_auth(user);
  set_account_profile(user, ipfs_profile, display_name, ipfs_avatar);
}

void peeranha::postquestion(eosio::name user, uint16_t community_id,
                            std::vector<uint32_t> tags, std::string title,
                            std::string ipfs_link) {
  require_auth(user);
  post_question(user, community_id, tags, title, ipfs_link);
}

void peeranha::postanswer(eosio::name user, uint64_t question_id,
                          std::string ipfs_link) {
  require_auth(user);
  post_answer(user, question_id, ipfs_link);
}

void peeranha::postcomment(eosio::name user, uint64_t question_id,
                           uint16_t answer_id, std::string ipfs_link) {
  require_auth(user);
  post_comment(user, question_id, answer_id, ipfs_link);
}

void peeranha::delquestion(eosio::name user, uint64_t question_id) {
  require_auth(user);
  delete_question(user, question_id);
}

void peeranha::delanswer(eosio::name user, uint64_t question_id,
                         uint16_t answer_id) {
  require_auth(user);
  delete_answer(user, question_id, answer_id);
}

void peeranha::delcomment(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id) {
  require_auth(user);
  delete_comment(user, question_id, answer_id, comment_id);
}

void peeranha::modquestion(eosio::name user, uint64_t question_id,
                           uint16_t community_id, std::vector<uint32_t> tags,
                           std::string title, std::string ipfs_link) {
  require_auth(user);
  modify_question(user, question_id, community_id, tags, title, ipfs_link);
}

void peeranha::modanswer(eosio::name user, uint64_t question_id,
                         uint16_t answer_id, std::string ipfs_link) {
  require_auth(user);
  modify_answer(user, question_id, answer_id, ipfs_link);
}
void peeranha::modcomment(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id,
                          std::string ipfs_link) {
  require_auth(user);
  modify_comment(user, question_id, answer_id, comment_id, ipfs_link);
}

void peeranha::upvote(eosio::name user, uint64_t question_id,
                      uint16_t answer_id) {
  require_auth(user);
  vote_forum_item(user, question_id, answer_id, true);
}

void peeranha::downvote(eosio::name user, uint64_t question_id,
                        uint16_t answer_id) {
  require_auth(user);
  vote_forum_item(user, question_id, answer_id, false);
}

void peeranha::mrkascorrect(eosio::name user, uint64_t question_id,
                            uint16_t answer_id) {
  require_auth(user);
  mark_answer_as_correct(user, question_id, answer_id);
}

void peeranha::reportforum(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id) {
  require_auth(user);
  report_forum_item(user, question_id, answer_id, comment_id);
}

// Tags and communities
void peeranha::crcommunity(eosio::name user, std::string name,
                           std::string ipfs_description,
                           std::vector<suggest_tag> suggested_tags) {
  require_auth(user);
  create_community(user, name, ipfs_description, suggested_tags);
}

void peeranha::crtag(eosio::name user, uint16_t community_id, std::string name,
                     std::string ipfs_description) {
  require_auth(user);
  create_tag(user, community_id, name, ipfs_description);
}

void peeranha::vtcrcomm(eosio::name user, uint32_t community_id) {
  require_auth(user);
  vote_create_community(user, community_id);
}

void peeranha::vtcrtag(eosio::name user, uint16_t community_id,
                       uint32_t tag_id) {
  require_auth(user);
  vote_create_tag(user, community_id, tag_id);
}

void peeranha::vtdelcomm(eosio::name user, uint32_t community_id) {
  require_auth(user);
  vote_delete_community(user, community_id);
}

void peeranha::vtdeltag(eosio::name user, uint16_t community_id,
                        uint32_t tag_id) {
  require_auth(user);
  vote_delete_tag(user, community_id, tag_id);
}

void peeranha::followcomm(eosio::name user, uint16_t community_id) {
  require_auth(user);
  follow_community(user, community_id);
}

void peeranha::unfollowcomm(eosio::name user, uint16_t community_id) {
  require_auth(user);
  unfollow_community(user, community_id);
}

void peeranha::reportprof(eosio::name user, eosio::name user_to_report){
  require_auth(user);
  report_profile(user, user_to_report);
}

void peeranha::givemoderflg(eosio::name user, int flags){
  require_auth(_self);
  give_moderator_flag(user, flags);
}

void peeranha::init(){
  global_stat_index global_stat_table(_self, scope_all_stat);
  auto iter_global_stat = global_stat_table.rbegin();
  if (iter_global_stat != global_stat_table.rend() && iter_global_stat->version == version)
    return;
  global_stat_table.emplace(_self, [&](auto &global_stat){
      global_stat.version = version;
      global_stat.user_count = 0;
      global_stat.communities_count = 0;
  });
}

EOSIO_DISPATCH(
    peeranha,
    (registeracc)(setaccprof)(postquestion)(
        postanswer)(postcomment)(delquestion)(delanswer)(delcomment)(modanswer)(
        modquestion)(modcomment)(upvote)(downvote)(mrkascorrect)(reportforum)(
        crtag)(crcommunity)(vtcrtag)(vtcrcomm)(vtdeltag)(vtdelcomm)(followcomm)(
        unfollowcomm)(givemoderflg)(init))