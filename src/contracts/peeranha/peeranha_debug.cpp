#define DEBUG
#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <string>
#include "economy.h"

#undef ACCOUNT_STAT_RESET_PERIOD
#define ACCOUNT_STAT_RESET_PERIOD 3  // 3 sec


#undef VOTES_TO_CREATE_COMMUNITY
#define VOTES_TO_CREATE_COMMUNITY 4
#undef VOTES_TO_DELETE_COMMUNITY
#define VOTES_TO_DELETE_COMMUNITY -3
#undef VOTES_TO_CREATE_TAG
#define VOTES_TO_CREATE_TAG 3
#undef VOTES_TO_DELETE_TAG
#define VOTES_TO_DELETE_TAG -2

#undef MIN_FREEZE_PERIOD
#undef REPORT_RESET_PERIOD
#undef REPORT_POWER_RESET_PERIOD
#undef POINTS_TO_FREEZE
#undef MODERATION_POINTS_REPORT_PROFILE
#define MIN_FREEZE_PERIOD 3
#define REPORT_RESET_PERIOD 2
#define REPORT_POWER_RESET_PERIOD 4
#define POINTS_TO_FREEZE 10
#define MODERATION_POINTS_REPORT_PROFILE 2

#include "question_container.hpp"
#include "access.hpp"
#include "account.hpp"
#include "communities_and_tags.hpp"
#include "history.hpp"
#include "property.hpp"
#include "utils.hpp"

#undef EOSIO_DISPATCH
#define EOSIO_DISPATCH(MEMBER, TYPES)
#include "peeranha.cpp"

extern time
    START_PERIOD_TIME;  // We need mechanism which change it once on deploy
extern int PERIOD_LENGTH;
class[[eosio::contract("peeranha")]] peeranha_d : public peeranha {
  using peeranha::peeranha;

 public:
  struct [[
    eosio::table("constants"), eosio::contract("peeranha")
  ]] constants {
    uint64_t id;
    time start_period_time;
    uint64_t primary_key() const { return id; }
    EOSLIB_SERIALIZE(constants, (id)(start_period_time))
  };
  typedef eosio::multi_index<eosio::name("constants"), constants>
      constants_index;

  const uint64_t scope_all_constants = eosio::name("allconstants").value;

  peeranha_d(eosio::name receiver, eosio::name code,
             eosio::datastream<const char *> ds)
      : peeranha(receiver, code, ds) {
    PERIOD_LENGTH = 3;
    // Initializte some constants for debug
    // could be moved to a separate method
    constants_index all_constants_table(_self, scope_all_constants);
    auto settings = all_constants_table.rbegin();
    if (settings != all_constants_table.rend()) {
      START_PERIOD_TIME = settings->start_period_time;
    } else {
      time current_time = now();
      START_PERIOD_TIME = current_time;
      all_constants_table.emplace(
          _self, [&all_constants_table, current_time](auto &constants) {
            constants.id = all_constants_table.available_primary_key();
            constants.start_period_time = current_time;
          });
      community_table_index community_table(_self, scope_all_communities);
      for (int i = 1; i < 4; ++i) {
        std::string index = std::to_string(i);
        community_table.emplace(
            _self, [i, &index, current_time](auto &community) {
              community.id = i;
              community.name = "DEBUG" + index;
              community.ipfs_description =
                  "Qme1CiDMWNNYqRLxzXmsP8GSngUfoi34juTKBSmSVHGFCE";
              community.creation_time = current_time;
              community.questions_asked = 0;
              community.answers_given = 0;
              community.correct_answers = 0;
              community.users_subscribed = 0;
            });
        tag_table_index tag_table(_self, get_tag_scope(i));
        for (int j = 0; j < 6 / i; ++j) {
          tag_table.emplace(_self, [&index, j](auto &tag) {
            tag.id = j;
            tag.name = "Tag " + std::to_string(j) + " community " + index;
            tag.ipfs_description =
                "QmPkZZtizV8Qat2Y9HkBWmgEX1L8p6VJZi1c6A2cf4vyfu";
            tag.questions_asked = 0;
          });
        }
      }
    }
  }

  ACTION setaccrten(eosio::name user, int rating, int16_t energy) {
    auto itr = find_account(user);
    account_table.modify(itr, _self, [rating, energy](auto &account) {
      account.rating = rating;
      account.energy = energy;
    });
  }

  ACTION resettables() {
    auto iter_account = account_table.begin();
    while (iter_account != account_table.end()) {
      // clean reward tables for user
      period_rating_index period_rating_table(_self, iter_account->user.value);
      auto iter_period_rating = period_rating_table.begin();
      while (iter_period_rating != period_rating_table.end()) {
        iter_period_rating = period_rating_table.erase(iter_period_rating);
      }

      // clean user_questions table
      user_questions_index user_questions_table(_self,
                                                iter_account->user.value);
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
      // remove user
      iter_account = account_table.erase(iter_account);
    }

    // clean create community table
    create_community_index create_community_table(_self, scope_all_communities);
    auto iter_create_community = create_community_table.begin();
    while (iter_create_community != create_community_table.end()) {
      iter_create_community =
          create_community_table.erase(iter_create_community);
    }

    // clean create tags and tags tables
    community_table_index community_table(_self, scope_all_communities);
    auto iter_community = community_table.begin();
    while (iter_community != community_table.end()) {
      // clean all tags for creation
      create_tag_index create_tag_table(_self,
                                        get_tag_scope(iter_community->id));
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

  ACTION chnguserrt(eosio::name user, int16_t rating_change) {
    update_rating(user, rating_change);
  }
};

extern "C" {
void apply(uint64_t receiver, uint64_t code, uint64_t action) {
  if (code == receiver) {
    switch (action) {
      EOSIO_DISPATCH_HELPER(peeranha_d, (chnguserrt)(resettables)(setaccrten))
      EOSIO_DISPATCH_HELPER(
          peeranha,
          (registeracc)(setaccprof)(postquestion)(
              postanswer)(postcomment)(delquestion)(delanswer)(delcomment)(
              modanswer)(modquestion)(modcomment)(upvote)(downvote)(
              mrkascorrect)(reportforum)(crtag)(crcommunity)(vtcrtag)(vtcrcomm)(
              vtdeltag)(vtdelcomm)(followcomm)(unfollowcomm)(init)(reportprof))
    }
  }
}
}