#include "peeranha.hpp"
#include "peeranha_account.cpp"
#include "peeranha_communities_and_tags.cpp"
#include "peeranha_forum.cpp"
#include "peeranha_vote.cpp"
#include "peeranha_top_question.cpp"
#include "telegram_account.cpp"
#include "peeranha_account_achievements.cpp"
#include "squeezed_achievement.cpp"
#include "peeranha_configuration.cpp"

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

void peeranha::telpostqstn(eosio::name bot, uint64_t telegram_id, uint16_t community_id,
                            std::vector<uint32_t> tags, std::string title,
                            IpfsHash ipfs_link, const uint8_t type) {
  require_auth(bot);
  eosio::check(get_configuration(CONFIGURATION_KEY_TELEGRAM) == bot.value, "Wrong bot account");

  eosio::name user = get_telegram_action_account(telegram_id);
  post_question(user, community_id, tags, title, ipfs_link, type);

  user_questions_index user_questions_table(_self, user.value);
  auto iter_user_question = user_questions_table.begin();
  eosio::check(iter_user_question != user_questions_table.end(), "Error set property question");

  auto iter_question = find_question(iter_user_question->question_id);
  auto iter_account = account_table.find(user.value);
  question_table.modify(iter_question, _self,
                      [iter_account](auto &question) {
                        set_property(question.properties, PROPERTY_TELEGRAM_QUESTION, 1);

                        if (get_property_d(iter_account->integer_properties, PROPERTY_EMPTY_ACCOUNT, 0)) {
                          set_property(question.properties, PROPERTY_EMPTY_QUESTION, 1);
                        }
                      });
}

void peeranha::postanswer(eosio::name user, uint64_t question_id,
                          IpfsHash ipfs_link, uint8_t official_answer) {
  require_auth(user);
  bool buf_official_answer = official_answer;
  post_answer(user, question_id, ipfs_link, buf_official_answer);
}

void peeranha::telpostansw(eosio::name bot, uint64_t telegram_id, uint64_t question_id,
                          IpfsHash ipfs_link, uint8_t official_answer) {
  require_auth(bot);
  eosio::check(get_configuration(CONFIGURATION_KEY_TELEGRAM) == bot.value, "Wrong bot account");

  bool buf_official_answer = official_answer;
  eosio::name user = get_telegram_action_account(telegram_id);
  post_answer(user, question_id, ipfs_link, buf_official_answer);

  user_answers_index user_answer_table(_self, user.value);
  auto iter_user_answer = user_answer_table.begin();
  eosio::check(iter_user_answer != user_answer_table.end(), "Error set property answer");

  auto iter_question = find_question(iter_user_answer->question_id);
  auto iter_account = account_table.find(user.value);
  question_table.modify(iter_question, _self,
                      [&iter_user_answer, iter_account](auto &question) {
                        auto iter_answer = find_answer(question, iter_user_answer->answer_id);
                        set_property(iter_answer->properties, PROPERTY_TELEGRAM_ANSWER, 1);

                        if (get_property_d(iter_account->integer_properties, PROPERTY_EMPTY_ACCOUNT, 0)) {
                          set_property(iter_answer->properties, PROPERTY_EMPTY_ANSWER, 1);
                        }
                      });
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
                           std::vector<suggest_tag> suggested_tags, uint16_t allowed_question_type) {
  require_auth(user);
  create_community(user, name, allowed_question_type, ipfs_description, suggested_tags);
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

void peeranha::editcomm(eosio::name user, uint16_t community_id, std::string name, IpfsHash ipfs_description, uint16_t allowed_question_type) {
  require_auth(user);
  edit_community(user, community_id, name, ipfs_description, allowed_question_type);
}

void peeranha::edittag(eosio::name user, uint16_t community_id, uint32_t tag_id, const std::string name, const IpfsHash ipfs_description) {
  require_auth(user);
  edit_tag(user, community_id, tag_id, name, ipfs_description);
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


void peeranha::apprvacc(eosio::name user) {
  require_auth(user);
  approve_account(user);
}

void peeranha::dsapprvacc(eosio::name user) {
  require_auth(user);
  disapprove_account(user);
}

void peeranha::dsapprvacctl(eosio::name bot_name, eosio::name user) {
  require_auth(bot_name);
  eosio::check(get_configuration(CONFIGURATION_KEY_TELEGRAM) == bot_name.value, "Wrong bot account");
  disapprove_account(user);
} 

void peeranha::addtelacc(eosio::name bot_name, eosio::name user, uint64_t telegram_id) {
  require_auth(bot_name);
  eosio::check(get_configuration(CONFIGURATION_KEY_TELEGRAM) == bot_name.value, "Wrong bot account");
  add_telegram_account(user, telegram_id, false);
}

void peeranha::addemptelacc(eosio::name bot_name, uint64_t telegram_id, std::string display_name, const IpfsHash ipfs_profile, const IpfsHash ipfs_avatar) {
  require_auth(bot_name);
  eosio::check(get_configuration(CONFIGURATION_KEY_TELEGRAM) == bot_name.value, "Wrong bot account");
  add_empty_telegram_account(telegram_id, display_name, ipfs_profile, ipfs_avatar);
}


void peeranha::updtdsplname(eosio::name bot_name, uint64_t telegram_id, std::string display_name) {
  require_auth(bot_name);
  eosio::check(get_configuration(CONFIGURATION_KEY_TELEGRAM) == bot_name.value, "Wrong bot account");
  update_display_name(telegram_id, display_name);
}

void peeranha::addconfig(uint64_t key, uint64_t value) {
  require_auth(_self);
  add_configuration(key, value);
}

void peeranha::addusrconfig(uint64_t key, eosio::name user) {
  require_auth(_self);
  add_configuration(key, user.value);
}

void peeranha::updateconfig(uint64_t key, uint64_t value) {
  require_auth(_self);
  update_configuration(key, value);
}

void peeranha::upuserconfig(uint64_t key, eosio::name user) {
  require_auth(_self);
  update_configuration(key, user.value);
}

void peeranha::intallaccach() {
  require_auth(_self);
  init_users_achievements();
}

void peeranha::invtblogger(eosio::name user) {
  require_auth(_self);
  invite_blogger(user);
}

void peeranha::intboost(uint64_t period) {
  require_auth(_self);
  auto iter_total_rating = total_rating_table.find(period);
  total_ratingg_index total_rating_table_2(_self, scope_all_periods);

  eosio::check(iter_total_rating != total_rating_table.end(), "Wrong period");

  while (iter_total_rating != total_rating_table.begin()) {
    total_rating_table_2.emplace(_self, [&iter_total_rating](auto &total_rating) {
      total_rating.period = iter_total_rating->period;
      total_rating.total_rating_to_reward = iter_total_rating->total_rating_to_reward;
    });

    total_rating_table.modify(iter_total_rating, _self,
                              [](auto &total_rating) {
                                total_rating.total_rating_to_reward *= MULTIPLICATION_TOTAL_RATING;
                              });
    iter_total_rating--;
  }

  total_rating_table_2.emplace(_self, [&iter_total_rating](auto &total_rating) {
      total_rating.period = iter_total_rating->period;
      total_rating.total_rating_to_reward = iter_total_rating->total_rating_to_reward;
    });

  total_rating_table.modify(iter_total_rating, _self,
                              [](auto &total_rating) {
                                total_rating.total_rating_to_reward *= MULTIPLICATION_TOTAL_RATING;
                              });
}

void peeranha::movecomscnd() {
  require_auth(_self);
  commbuf_table_index commbuf_table (_self, scope_all_communities);
  community_table_index community_table (_self, scope_all_communities);
  auto iter_communities = commbuf_table.begin();
  while (iter_communities != commbuf_table.end()) {
    community_table.emplace(
          _self, [&iter_communities](auto &comm) {
            comm.id = iter_communities->id;
            comm.name = iter_communities->name;
            comm.ipfs_description = iter_communities->ipfs_description;
            comm.creation_time = iter_communities->creation_time;
            comm.questions_asked = iter_communities->questions_asked;
            comm.answers_given = iter_communities->answers_given;
            comm.correct_answers = iter_communities->correct_answers;
            comm.users_subscribed = iter_communities->users_subscribed;
          });
    iter_communities = commbuf_table.erase(iter_communities);
  }
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

    account_achievements_index account_achievements_table(_self, iter_account->user.value);
    auto iter_account_achievements = account_achievements_table.begin();
    while (iter_account_achievements != account_achievements_table.end()) {
      iter_account_achievements = account_achievements_table.erase(iter_account_achievements);
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

  squeezed_achievement_index squeezed_achievement_table(_self, scope_all_squeezed_achievements);
  auto iter_squeezed_achievement = squeezed_achievement_table.begin();
  while (iter_squeezed_achievement != squeezed_achievement_table.end()) {
    iter_squeezed_achievement = squeezed_achievement_table.erase(iter_squeezed_achievement);
  }

  top_question_index top_question_table(_self, scope_all_top_questions);
  auto iter_top_question = top_question_table.begin();
  while (iter_top_question != top_question_table.end()) {
    iter_top_question = top_question_table.erase(iter_top_question);
  }

  // clean create community table
  create_community_index create_community_table(_self, scope_all_communities);
  auto iter_create_community = create_community_table.begin();
  while (iter_create_community != create_community_table.end()) {
    iter_create_community = create_community_table.erase(iter_create_community);
  }

  // clean property community table
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

  // clean create tellos account table
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.begin();
  while (iter_telegram_account != telegram_account_table.end()) {
    iter_telegram_account = telegram_account_table.erase(iter_telegram_account);
  }

  // clean table configuration
  configuration_index configuration_table(_self, scope_all_config);
  auto iter_config = configuration_table.begin();
  while (iter_config != configuration_table.end()) {
    iter_config = configuration_table.erase(iter_config);
  }

  // clean combuf table
  commbuf_table_index combuf_table(_self, scope_all_communities);
  auto iter_combuf = combuf_table.begin();
  while (iter_combuf != combuf_table.end()) {
    iter_combuf = combuf_table.erase(iter_combuf);
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
    (registeracc)(setaccprof)(postquestion)(telpostqstn)(postanswer)(telpostansw)(postcomment)(
        delquestion)(delanswer)(delcomment)(modanswer)(modquestion)(modcomment)(
        upvote)(downvote)(mrkascorrect)(reportforum)(crtag)(crcommunity)(
        vtcrtag)(vtcrcomm)(vtdeltag)(vtdelcomm)(followcomm)(unfollowcomm)(
        reportprof)(updateacc)(givemoderflg)(editcomm)(edittag)(chgqsttype)
        (addtotopcomm)(remfrmtopcom)(upquestion)(downquestion)(movequestion)(givecommuflg)
        (apprvacc)(dsapprvacc)(addtelacc)(addemptelacc)(dsapprvacctl)(updtdsplname)(intallaccach)
        (invtblogger)(movecomscnd)(intboost)(addconfig)(addusrconfig)(updateconfig)(upuserconfig)

#ifdef SUPERFLUOUS_INDEX
        (freeindex)
#endif

#if STAGE == 1 || STAGE == 2
            (chnguserrt)(resettables)(setaccrten)
#endif
                (init)(payforcpu))