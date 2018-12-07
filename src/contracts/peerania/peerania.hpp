#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>
#include <string>
#include "access.hpp"
#include "account.hpp"
#include "communities_and_tags.hpp"
#include "economy.h"
#include "history.hpp"
#include "peerania_types.h"
#include "property.hpp"
#include "question_container.hpp"
#include "token_common.hpp"
#include "utils.hpp"

#ifdef DEBUG
extern time START_PERIOD_TIME;
#endif

class[[eosio::contract]] peerania : public eosio::contract {
 public:
  peerania(eosio::name receiver, eosio::name code,
           eosio::datastream<const char *> ds)
      : contract(receiver, code, ds),
        account_table(receiver, scope_all_accounts),
        question_table(receiver, scope_all_questions),
        total_rating_table(receiver, scope_all_periods) {
#ifdef DEBUG
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
      tag_community_index community_table(_self, scope_all_communities);
      community_table.emplace(
          _self, [](auto &community) {
            community.id = 1;
            community.name = "DEBUG";
            community.ipfs_description = "DEBUG_COMMUNITY_IPFS";
            community.popularity = 0;
          });
      tag_community_index tag_table(_self, get_tag_scope(1));
      for (int i = 0; i < 10; ++i) {
        tag_table.emplace(
            _self, [i](auto &tag) {
              tag.id = i;
              tag.name = "Tag " + std::to_string(i);
              tag.ipfs_description = "DEBUG_COMMUNITY1_TAG " + std::to_string(i);
              tag.popularity = 0;
            });
      }
    }
#endif
  };

  // Register new user
  [[eosio::action]] void registeracc(
      eosio::name owner, std::string display_name, std::string ipfs_profile);

  // Set(or add) property to account
  [[eosio::action]] void setaccstrprp(eosio::name owner, uint8_t key,
                                      std::string value);

  // Set(or add) property to account
  [[eosio::action]] void setaccintprp(eosio::name owner, uint8_t key,
                                      int32_t value);

  // Set user profile (IPFS link)
  [[eosio::action]] void setaccprof(eosio::name owner, std::string ipfs_profile,
                                    std::string display_name);

  // Post question
  [[eosio::action]] void postquestion(eosio::name user, uint16_t community_id,
                                      const std::vector<uint32_t> tags,
                                      std::string title, std::string ipfs_link);

  // Post answer(answer question)
  [[eosio::action]] void postanswer(eosio::name user, uint64_t question_id,
                                    std::string ipfs_link);

  // Post comment
  // If the answer_id set to 0 comment question, otherwise comment question
  // with passed answer_id
  [[eosio::action]] void postcomment(eosio::name user, uint64_t question_id,
                                     uint16_t answer_id,
                                     const std::string &ipfs_link);

  // Delete question
  [[eosio::action]] void delquestion(eosio::name user, uint64_t question_id);

  // Delete answer
  [[eosio::action]] void delanswer(eosio::name user, uint64_t question_id,
                                   uint16_t answer_id);

  // Delete comment
  [[eosio::action]] void delcomment(eosio::name user, uint64_t question_id,
                                    uint16_t answer_id, uint16_t comment_id);

  // Modify question
  [[eosio::action]] void modquestion(eosio::name user, uint64_t question_id,
                                     const std::string &title,
                                     const std::string &ipfs_link);

  // Modify answer
  [[eosio::action]] void modanswer(eosio::name user, uint64_t question_id,
                                   uint16_t answer_id,
                                   const std::string &ipfs_link);

  // Modify comment
  [[eosio::action]] void modcomment(eosio::name user, uint64_t question_id,
                                    uint16_t answer_id, uint16_t comment_id,
                                    const std::string &ipfs_link);

  // Upvote question/answer
  [[eosio::action]] void upvote(eosio::name user, uint64_t question_id,
                                uint16_t answer_id);

  // Downvote question/answer
  [[eosio::action]] void downvote(eosio::name user, uint64_t question_id,
                                  uint16_t answer_id);

  // Vote for deletion
  // if (answer_id == 0) delete question(by question_id)
  // elif (comment_id == 0) delete answer question(question_id)->answer(by
  // answer_id) elif delete comment
  // question(question_id)->answer(answer_id)->comment(by comment_id)
  [[eosio::action]] void votedelete(eosio::name user, uint64_t question_id,
                                    uint16_t answer_id, uint16_t comment_id);

  // Vote for moderation
  // if (answer_id == 0) delete question(by question_id)
  // elif (comment_id == 0) delete answer question(question_id)->answer(by
  // answer_id) elif delete comment
  // question(question_id)->answer(answer_id)->comment(by comment_id)
  [[eosio::action]] void votemoderate(eosio::name user, uint64_t question_id,
                                      uint16_t answer_id, uint16_t comment_id);

  // Mark answer as correct
  [[eosio::action]] void mrkascorrect(eosio::name user, uint64_t question_id,
                                      uint16_t answer_id);

  // Tags and communities
  [[eosio::action]] void crcommunity(eosio::name user, const std::string &name,
                                     const std::string &ipfs_description);

  [[eosio::action]] void crtag(eosio::name user, uint16_t community_id,
                               std::string name, std::string ipfs_description);

  [[eosio::action]] void vtcrcomm(eosio::name user, uint16_t community_id);

  [[eosio::action]] void vtcrtag(eosio::name user, uint16_t community_id,
                                 uint32_t tag_id);

  [[eosio::action]] void vtdelcomm(eosio::name user, uint16_t community_id);

  [[eosio::action]] void vtdeltag(eosio::name user, uint16_t community_id,
                                  uint32_t tag_id);

  // Debug methoods
#ifdef DEBUG
  // Set account rating and moderation points count
  [[eosio::action]] void setaccrtmpc(eosio::name user, int16_t rating,
                                     uint16_t moderation_points);

  [[eosio::action]] void resettables();

  [[eosio::action]] void chnguserrt(eosio::name user, int16_t rating_change);

#endif

 private:
  question_index question_table;
  account_index account_table;
  total_rating_index total_rating_table;
  void register_account(eosio::name owner, std::string display_name,
                        const std::string &ipfs_profile);

  void set_account_profile(eosio::name owner, const std::string &ipfs_profile,
                           const std::string &display_name);

  void set_account_string_property(eosio::name owner, uint8_t key,
                                   const std::string &value);

  void set_account_integer_property(eosio::name owner, uint8_t key,
                                    int32_t value);

  account_index::const_iterator find_account(eosio::name owner);

  question_index::const_iterator find_question(uint64_t question_id);

  void post_question(eosio::name user, uint16_t community_id,
                     const std::vector<uint32_t> tags, const std::string &title,
                     const std::string &ipfs_link);

  void post_answer(eosio::name user, uint64_t question_id,
                   const std::string &ipfs_link);

  void post_comment(eosio::name user, uint64_t question_id, uint16_t answer_id,
                    const std::string &ipfs_link);

  void delete_question(eosio::name user, uint64_t question_id);

  void delete_answer(eosio::name user, uint64_t question_id,
                     uint16_t answer_id);

  void delete_comment(eosio::name user, uint64_t question_id,
                      uint16_t answer_id, uint64_t comment_id);

  void modify_question(eosio::name user, uint64_t question_id,
                       const std::string &title, const std::string &ipfs_link);

  void modify_answer(eosio::name user, uint64_t question_id, uint16_t answer_id,
                     const std::string &ipfs_link);

  void modify_comment(eosio::name user, uint64_t question_id,
                      uint16_t answer_id, uint16_t comment_id,
                      const std::string &ipfs_link);

  void create_community_or_tag(eosio::name user, const std::string &name,
                               const std::string &ipfs_description,
                               uint16_t commuinty_id);

  void vote_create_community_or_tag(eosio::name user, uint32_t tag_id,
                                    uint16_t commuinty_id);

  void vote_delete_community_or_tag(eosio::name user, uint32_t tag_id,
                                    uint16_t commuinty_id);

  void vote_forum_item(eosio::name user, uint64_t question_id,
                       uint16_t answer_id, bool is_upvote);

  void mark_answer_as_correct(eosio::name user, uint64_t question_id,
                              uint16_t answer_id);

  void vote_for_deletion(eosio::name user, uint64_t question_id,
                         uint16_t answer_id, uint16_t comment_id);

  void update_rating(account_index::const_iterator iter_account,
                     int rating_change);

  void update_rating(eosio::name user, int rating_change);

  void update_popularity(uint16_t commuinty_id,
                         const std::vector<uint32_t> &tags, bool increase);

  uint64_t get_tag_scope(uint16_t community_id);

  void assert_community_exist(uint16_t community_id);

  void remove_user_question_or_answer(eosio::name user, uint64_t question_id, uint16_t answer_id);
};
