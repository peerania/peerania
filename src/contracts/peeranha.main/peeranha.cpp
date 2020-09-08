#include "peeranha.hpp"
#include "peeranha_account.cpp"
#include "peeranha_communities_and_tags.cpp"
#include "peeranha_forum.cpp"
#include "peeranha_vote.cpp"
#include "peeranha_top_question.cpp"

void peeranha::registeracc(eosio::name user, std::string display_name,
                           IpfsHash ipfs_profile, IpfsHash ipfs_avatar) {
  require_auth(user);
  register_account(user, display_name, ipfs_profile, ipfs_avatar);
}

void peeranha::setaccprof(eosio::name user, IpfsHash ipfs_profile,
                          std::string display_name, IpfsHash ipfs_avatar) {
  require_auth(user);
  set_account_profile(user, ipfs_profile, display_name, ipfs_avatar);
}

void peeranha::postquestion(eosio::name user, uint16_t community_id,
                            std::vector<uint32_t> tags, std::string title,
                            IpfsHash ipfs_link, const uint8_t type) {
  require_auth(user);
  post_question(user, community_id, tags, title, ipfs_link, type);
}

void peeranha::postanswer(eosio::name user, uint64_t question_id,
                          IpfsHash ipfs_link, uint8_t official_answer) {
  require_auth(user);
  bool buf_official_answer = official_answer;
  post_answer(user, question_id, ipfs_link, buf_official_answer);
}

void peeranha::postcomment(eosio::name user, uint64_t question_id,
                           uint16_t answer_id, IpfsHash ipfs_link) {
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
                           std::string title, IpfsHash ipfs_link) {
  require_auth(user);
  modify_question(user, question_id, community_id, tags, title, ipfs_link);
}

void peeranha::modanswer(eosio::name user, uint64_t question_id,
                         uint16_t answer_id, IpfsHash ipfs_link, uint8_t official_answer) {
  require_auth(user);
  bool buf_official_answer = official_answer;
  modify_answer(user, question_id, answer_id, ipfs_link, buf_official_answer);
}
void peeranha::modcomment(eosio::name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id,
                          IpfsHash ipfs_link) {
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
                           IpfsHash ipfs_description,
                           std::vector<suggest_tag> suggested_tags) {
  require_auth(user);
  create_community(user, name, ipfs_description, suggested_tags);
}

void peeranha::crtag(eosio::name user, uint16_t community_id, std::string name,
                     IpfsHash ipfs_description) {
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

void peeranha::reportprof(eosio::name user, eosio::name user_to_report) {
  require_auth(user);
  report_profile(user, user_to_report);
}

void peeranha::updateacc(eosio::name user) {
  require_auth(user);
  update_account(user);
}

void peeranha::givemoderflg(eosio::name user, int flags) {
  require_auth(_self);
  give_moderator_flag(user, flags);
}

void peeranha::givecommuflg(eosio::name user, int flags, uint16_t community_id) {
  require_auth(_self);
  give_moderator_flag(user, flags, community_id);
}

void peeranha::editcomm(uint16_t community_id, std::string new_name, IpfsHash new_ipfs_link) {
  require_auth(_self);
  edit_community(community_id, new_name, new_ipfs_link);
}

void peeranha::chgqsttype(eosio::name user, uint64_t question_id, int type, bool restore_rating){
   require_auth(user);
   change_question_type(user, question_id, type, restore_rating);
}

void peeranha::addtotopcomm(eosio::name user, uint16_t community_id, uint64_t question_id){
  require_auth(user);
  add_top_question(user, community_id, question_id);
}

void peeranha::remfrmtopcom(eosio::name user, uint16_t community_id, uint64_t question_id){
  require_auth(user);
  remove_top_question(user, community_id, question_id);
}

void peeranha::upquestion(eosio::name user, uint16_t community_id, uint64_t question_id){
  require_auth(user);
  up_top_question(user, community_id, question_id);
}

void peeranha::downquestion(eosio::name user, uint16_t community_id, uint64_t question_id){
  require_auth(user);
  down_top_question(user, community_id, question_id);
}

void peeranha::movequestion(eosio::name user, uint16_t community_id, uint64_t question_id, uint16_t new_position){
  require_auth(user);
  move_top_question(user,  community_id, question_id, new_position);
}

#ifdef SUPERFLUOUS_INDEX
void peeranha::freeindex(int size) {
  require_auth(_self);
  // int total_count_to_free = 0;
  auto iter_account = account_table.begin();
  while (iter_account != account_table.end()) {
    // clean user_questions table
    user_questions_index user_questions_table(_self, iter_account->user.value);
    auto iter_user_questions = user_questions_table.begin();
    while (iter_user_questions != user_questions_table.end()) {
      iter_user_questions = user_questions_table.erase(iter_user_questions);
    }

    // clean user_answers table
    user_answers_index user_answers_table(_self, iter_account->user.value);
    auto iter_user_answers = user_answers_table.begin();
    while (iter_user_answers != user_answers_table.end()) {
      iter_user_answers = user_answers_table.erase(iter_user_answers);
    }
  }
}
#endif

#if STAGE == 1 || STAGE == 2
void peeranha::setaccrten(eosio::name user, int rating, int16_t energy) {
  require_auth(_self);
  auto itr = find_account(user);
  if (energy >= 0)
    account_table.modify(itr, _self, [rating, energy](auto &account) {
      account.rating = rating;
      account.energy = energy;
    });
  else
    account_table.erase(itr);
}

void peeranha::resettables() {
  require_auth(_self);
  auto iter_account = account_table.begin();
  while (iter_account != account_table.end()) {
    // clean reward tables for user
    period_rating_index period_rating_table(_self, iter_account->user.value);
    auto iter_period_rating = period_rating_table.begin();
    while (iter_period_rating != period_rating_table.end()) {
      iter_period_rating = period_rating_table.erase(iter_period_rating);
    }

    top_question_index top_question_table(_self, scope_all_top_questions);
    auto iter_top_question = top_question_table.begin();
    while (iter_top_question != top_question_table.end()) {
      iter_top_question = top_question_table.erase(iter_top_question);
    }
#ifdef SUPERFLUOUS_INDEX
    // clean user_questions table
    user_questions_index user_questions_table(_self, iter_account->user.value);
    auto iter_user_questions = user_questions_table.begin();
    while (iter_user_questions != user_questions_table.end()) {
      iter_user_questions = user_questions_table.erase(iter_user_questions);
    }

    // clean user_answers table
    user_answers_index user_answers_table(_self, iter_account->user.value);
    auto iter_user_answers = user_answers_table.begin();
    while (iter_user_answers != user_answers_table.end()) {
      iter_user_answers = user_answers_table.erase(iter_user_answers);
    }
#endif
    // remove user
    iter_account = account_table.erase(iter_account);
  }

  // clean create community table
  create_community_index create_community_table(_self, scope_all_communities);
  auto iter_create_community = create_community_table.begin();
  while (iter_create_community != create_community_table.end()) {
    iter_create_community = create_community_table.erase(iter_create_community);
  }

  // clean create community table
  property_community_index property_community_table(_self, scope_all_property_community);
  auto iter_user = property_community_table.begin();
  while (iter_user != property_community_table.end()) {
    iter_user = property_community_table.erase(iter_user);
  }

  // clean create tags and tags tables
  community_table_index community_table(_self, scope_all_communities);
  auto iter_community = community_table.begin();
  while (iter_community != community_table.end()) {
    // clean all tags for creation
    create_tag_index create_tag_table(_self, get_tag_scope(iter_community->id));
    auto iter_create_tag = create_tag_table.begin();
    while (iter_create_tag != create_tag_table.end()) {
      iter_create_tag = create_tag_table.erase(iter_create_tag);
    }

    // Clean tags
    tag_table_index tag_table(_self, get_tag_scope(iter_community->id));
    auto iter_tag = tag_table.begin();
    while (iter_tag != tag_table.end()) {
      iter_tag = tag_table.erase(iter_tag);
    }

    iter_community = community_table.erase(iter_community);
  }

  // clean total rating
  auto iter_total_rating = total_rating_table.begin();
  while (iter_total_rating != total_rating_table.end()) {
    iter_total_rating = total_rating_table.erase(iter_total_rating);
  }

  // clean forum
  auto iter_question = question_table.begin();
  while (iter_question != question_table.end()) {
    iter_question = question_table.erase(iter_question);
  }

  // clean global statistics
  global_stat_index global_stat_table(_self, scope_all_stat);
  auto iter_global_stat = global_stat_table.begin();
  while (iter_global_stat != global_stat_table.end()) {
    iter_global_stat = global_stat_table.erase(iter_global_stat);
  }
#if STAGE == 2
  // clean constants
  constants_index all_constants_table(_self, scope_all_constants);
  auto iter_constants = all_constants_table.begin();
  while (iter_constants != all_constants_table.end()) {
    iter_constants = all_constants_table.erase(iter_constants);
  }
#endif
}

void peeranha::chnguserrt(eosio::name user, int16_t rating_change) {
  require_auth(_self);
  update_rating(user, rating_change);
}
#endif

void peeranha::init() {
  global_stat_index global_stat_table(_self, scope_all_stat);
  auto iter_global_stat = global_stat_table.rbegin();
  if (iter_global_stat != global_stat_table.rend() &&
      iter_global_stat->version == version)
    return;
  global_stat_table.emplace(_self, [&](auto &global_stat) {
    global_stat.version = version;
    global_stat.user_count = 0;
    global_stat.communities_count = 0;
  });
}

EOSIO_DISPATCH(
    peeranha,
    (registeracc)(setaccprof)(postquestion)(postanswer)(postcomment)(
        delquestion)(delanswer)(delcomment)(modanswer)(modquestion)(modcomment)(
        upvote)(downvote)(mrkascorrect)(reportforum)(crtag)(crcommunity)(
        vtcrtag)(vtcrcomm)(vtdeltag)(vtdelcomm)(followcomm)(unfollowcomm)(
        reportprof)(updateacc)(givemoderflg)(editcomm)(chgqsttype)
        (addtotopcomm)(remfrmtopcom)(upquestion)(downquestion)(movequestion)(givecommuflg)

#ifdef SUPERFLUOUS_INDEX
        (freeindex)
#endif

#if STAGE == 1 || STAGE == 2
            (chnguserrt)(resettables)(setaccrten)
#endif
                (init)(payforcpu))