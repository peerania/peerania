#pragma once
#include <string>
#include "access.hpp"
#include "account.hpp"
#include "communities_and_tags.hpp"
#include "economy.h"
#include "global_statistics.hpp"
#include "history.hpp"
#include "peeranha_types.h"
#include "property.hpp"
#include "question_container.hpp"
#include "token_common.hpp"
#include "utils.hpp"

CONTRACT peeranha : public eosio::contract {
 public:
  const int version = 1;

  peeranha(eosio::name receiver, eosio::name code,
           eosio::datastream<const char *> ds)
      : contract(receiver, code, ds),
        account_table(receiver, scope_all_accounts),
        question_table(receiver, scope_all_questions),
        total_rating_table(receiver, scope_all_periods){};

  // Register new user
  ACTION registeracc(eosio::name user, std::string display_name,
                     std::string ipfs_profile, std::string ipfs_avatar);

  // Set user profile (IPFS link)
  ACTION setaccprof(eosio::name user, std::string ipfs_profile,
                    std::string display_name, std::string ipfs_avatar);

  // Post question
  ACTION postquestion(eosio::name user, uint16_t community_id,
                      std::vector<uint32_t> tags, std::string title,
                      std::string ipfs_link);

  // Post answer(answer question)
  ACTION postanswer(eosio::name user, uint64_t question_id,
                    std::string ipfs_link);

  // Post comment
  // If the answer_id set to 0 comment question, otherwise comment question
  // with passed answer_id
  ACTION postcomment(eosio::name user, uint64_t question_id, uint16_t answer_id,
                     std::string ipfs_link);

  // Delete question
  ACTION delquestion(eosio::name user, uint64_t question_id);

  // Delete answer
  ACTION delanswer(eosio::name user, uint64_t question_id, uint16_t answer_id);

  // Delete comment
  ACTION delcomment(eosio::name user, uint64_t question_id, uint16_t answer_id,
                    uint16_t comment_id);

  // Modify question
  ACTION modquestion(eosio::name user, uint64_t question_id,
                     uint16_t community_id, std::vector<uint32_t> tags,
                     std::string title, std::string ipfs_link);

  // Modify answer
  ACTION modanswer(eosio::name user, uint64_t question_id, uint16_t answer_id,
                   std::string ipfs_link);

  // Modify comment
  ACTION modcomment(eosio::name user, uint64_t question_id, uint16_t answer_id,
                    uint16_t comment_id, std::string ipfs_link);

  // Upvote question/answer
  ACTION upvote(eosio::name user, uint64_t question_id, uint16_t answer_id);

  // Downvote question/answer
  ACTION downvote(eosio::name user, uint64_t question_id, uint16_t answer_id);

  // Vote for deletion
  // if (answer_id == 0) delete question(by question_id)
  // elif (comment_id == 0) delete answer question(question_id)->answer(by
  // answer_id) elif delete comment
  // question(question_id)->answer(answer_id)->comment(by comment_id)
  ACTION reportforum(eosio::name user, uint64_t question_id, uint16_t answer_id,
                    uint16_t comment_id);

  // Mark answer as correct
  ACTION mrkascorrect(eosio::name user, uint64_t question_id,
                      uint16_t answer_id);

  // Tags and communities
  ACTION crcommunity(eosio::name user, std::string name,
                     std::string ipfs_description,
                     std::vector<suggest_tag> suggested_tags);

  ACTION crtag(eosio::name user, uint16_t community_id, std::string name,
               std::string ipfs_description);

  ACTION vtcrcomm(eosio::name user, uint32_t community_id);

  ACTION vtcrtag(eosio::name user, uint16_t community_id, uint32_t tag_id);

  ACTION vtdelcomm(eosio::name user, uint32_t community_id);

  ACTION vtdeltag(eosio::name user, uint16_t community_id, uint32_t tag_id);

  ACTION followcomm(eosio::name user, uint16_t community_id);

  ACTION unfollowcomm(eosio::name user, uint16_t community_id);

  // Report user profile
  ACTION reportprof(eosio::name user, eosio::name user_to_report);

  ACTION init();

 protected:
  question_index question_table;
  account_index account_table;
  total_rating_index total_rating_table;

  account_index::const_iterator find_account(eosio::name user);
  question_index::const_iterator find_question(uint64_t question_id);
  uint64_t get_tag_scope(uint16_t community_id);

  void update_rating_base(
      account_index::const_iterator iter_account, int rating_change,
      const std::function<void(account &)> account_modifying_lambda,
      bool hasLambda);

  void update_rating(eosio::name user, int rating_change);

  void update_rating(
      eosio::name user, int rating_change,
      const std::function<void(account &)> account_modifying_lambda);

  void update_rating(account_index::const_iterator iter_account,
                     int rating_change);

  void update_rating(
      account_index::const_iterator iter_account, int rating_change,
      const std::function<void(account &)> account_modifying_lambda);

  void update_rating(
      account_index::const_iterator iter_account,
      const std::function<void(account &)> account_modifying_lambda);
      
  // private:
  void register_account(eosio::name user, std::string display_name,
                        const std::string &ipfs_profile,
                        const std::string &ipfs_avatar);

  void set_account_profile(eosio::name user, const std::string &ipfs_profile,
                           const std::string &display_name,
                           const std::string &ipfs_avatar);

  void report_profile(eosio::name user, eosio::name user_to_report);

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
                       uint16_t community_id, const std::vector<uint32_t> &tags,
                       const std::string &title, const std::string &ipfs_link);

  void modify_answer(eosio::name user, uint64_t question_id, uint16_t answer_id,
                     const std::string &ipfs_link);

  void modify_comment(eosio::name user, uint64_t question_id,
                      uint16_t answer_id, uint16_t comment_id,
                      const std::string &ipfs_link);

  void create_community(eosio::name user, const std::string &name,
                        const std::string &ipfs_description,
                        const std::vector<suggest_tag> &suggested_tags);

  void create_tag(eosio::name user, uint16_t commuinty_id,
                  const std::string &name, const std::string &ipfs_description);

  void vote_create_community(eosio::name user, uint32_t community_id);

  void vote_create_tag(eosio::name user, uint16_t community_id,
                       uint32_t tag_id);

  void vote_delete_community(eosio::name user, uint32_t community_id);

  void vote_delete_tag(eosio::name user, uint16_t community_id,
                       uint32_t tag_id);

  void create_community_or_tag(account_index::const_iterator iter_account,
                               uint64_t scope, const std::string &name,
                               const std::string &ipfs_description);

  void vote_create_comm_or_tag(
      account_index::const_iterator iter_account, uint32_t id, uint64_t scope,
      int32_t votes_to_create, uint32_t max_pk, int16_t reward);

  void vote_delete_comm_or_tag(account_index::const_iterator iter_account,
                               uint32_t id, uint64_t scope,
                               int32_t votes_to_delete, int16_t reward);

  void vote_forum_item(eosio::name user, uint64_t question_id,
                       uint16_t answer_id, bool is_upvote);

  void mark_answer_as_correct(eosio::name user, uint64_t question_id,
                              uint16_t answer_id);

  void report_forum_item(eosio::name user, uint64_t question_id,
                         uint16_t answer_id, uint16_t comment_id);

  void update_community_statistics(
      uint16_t commuinty_id, int8_t questions_asked, int8_t answers_given,
      int8_t correct_answers, int8_t users_subscribed);

  void update_tags_statistics(uint16_t community_id,
                              std::vector<uint32_t> tags_id,
                              int8_t questions_asked);

  void assert_community_exist(uint16_t community_id);

  void remove_user_question(eosio::name user, uint64_t question_id);

  void remove_user_answer(eosio::name user, uint64_t question_id);

  void follow_community(eosio::name user, uint16_t community_id);

  void unfollow_community(eosio::name user, uint16_t community_id);
};