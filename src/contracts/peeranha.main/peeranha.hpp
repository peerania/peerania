#pragma once
#include <string>
#include <unordered_map>
#include "access.hpp"
#include "account.hpp"
#include "communities_and_tags.hpp"
#include "economy.h"
#include "global_statistics.hpp"
#include "history.hpp"
#include "peeranha_types.h"
#include "property.hpp"
#include "question_container.hpp"
#include "utils.hpp"
#include "property_community.hpp"
#include "top_question.hpp"
#include "telegram_account.hpp"
#include "achievements.hpp"
#include "account_achievements.hpp"
#include "squeezed_achievement.hpp"

#include "token_common.hpp"

class[[eosio::contract("peeranha.main")]] peeranha : public eosio::contract {
 public:
  const int version = 1;

  peeranha(eosio::name receiver, eosio::name code,
           eosio::datastream<const char *> ds)
      : contract(receiver, code, ds),
        account_table(receiver, scope_all_accounts),
        question_table(receiver, scope_all_questions),
        total_rating_table(receiver, scope_all_periods) {
#if STAGE == 2
    // Initializte some constants for debug
    // could be moved to a separate method
    constants_index all_constants_table(_self, scope_all_constants);
    auto settings = all_constants_table.rbegin();
    if (settings == all_constants_table.rend()) {
      time current_time = now();
      all_constants_table.emplace(
          _self, [&all_constants_table, current_time](auto &constants) {
            constants.id = all_constants_table.available_primary_key();
            constants.start_period_time = current_time;
          });
    }
#endif
    };

    // Register new user
    ACTION registeracc(eosio::name user, std::string display_name,
                       IpfsHash ipfs_profile, IpfsHash ipfs_avatar);

    // Set user profile (IPFS link)
    ACTION setaccprof(eosio::name user, IpfsHash ipfs_profile,
                      std::string display_name, IpfsHash ipfs_avatar);

    // Post question
    ACTION postquestion(eosio::name user, uint16_t community_id,
                        std::vector<uint32_t> tags, std::string title,
                        IpfsHash ipfs_link, uint8_t type);

    // Telegram post question
    ACTION telpostqstn(eosio::name bot, uint64_t telegram_id, uint16_t community_id, 
                        std::vector<uint32_t> tags, std::string title,
                        IpfsHash ipfs_link, uint8_t type);

    // Post answer(answer question)
    ACTION postanswer(eosio::name user, uint64_t question_id,
                      IpfsHash ipfs_link, uint8_t official_answer);
    
    // Telegram post answer(answer question)
    ACTION telpostansw(eosio::name bot, uint64_t telegram_id, uint64_t question_id,
                          IpfsHash ipfs_link, uint8_t official_answer);

    // Post comment
    // If the answer_id set to 0 comment question, otherwise comment question
    // with passed answer_id
    ACTION postcomment(eosio::name user, uint64_t question_id,
                       uint16_t answer_id, IpfsHash ipfs_link);

    // Delete question
    ACTION delquestion(eosio::name user, uint64_t question_id);

    // Delete answer
    ACTION delanswer(eosio::name user, uint64_t question_id,
                     uint16_t answer_id);

    // Delete comment
    ACTION delcomment(eosio::name user, uint64_t question_id,
                      uint16_t answer_id, uint16_t comment_id);

    // Modify question
    ACTION modquestion(eosio::name user, uint64_t question_id,
                       uint16_t community_id, std::vector<uint32_t> tags,
                       std::string title, IpfsHash ipfs_link);

    // Modify answer
    ACTION modanswer(eosio::name user, uint64_t question_id, uint16_t answer_id,
                     IpfsHash ipfs_link, uint8_t official_answer);

    // Modify comment
    ACTION modcomment(eosio::name user, uint64_t question_id,
                      uint16_t answer_id, uint16_t comment_id,
                      IpfsHash ipfs_link);

    // Upvote question/answer
    ACTION upvote(eosio::name user, uint64_t question_id, uint16_t answer_id);

    // Downvote question/answer
    ACTION downvote(eosio::name user, uint64_t question_id, uint16_t answer_id);

    // Vote for deletion
    // if (answer_id == 0) delete question(by question_id)
    // elif (comment_id == 0) delete answer question(question_id)->answer(by
    // answer_id) elif delete comment
    // question(question_id)->answer(answer_id)->comment(by comment_id)
    ACTION reportforum(eosio::name user, uint64_t question_id,
                       uint16_t answer_id, uint16_t comment_id);

    // Mark answer as correct
    ACTION mrkascorrect(eosio::name user, uint64_t question_id,
                        uint16_t answer_id);

    // Tags and communities
    ACTION crcommunity(eosio::name user, std::string name,
                       IpfsHash ipfs_description,
                       std::vector<suggest_tag> suggested_tags);

    ACTION crtag(eosio::name user, uint16_t community_id, std::string name,
                 IpfsHash ipfs_description);

    ACTION vtcrcomm(eosio::name user, uint32_t community_id);

    ACTION vtcrtag(eosio::name user, uint16_t community_id, uint32_t tag_id);

    ACTION vtdelcomm(eosio::name user, uint32_t community_id);

    ACTION vtdeltag(eosio::name user, uint16_t community_id, uint32_t tag_id);

    ACTION followcomm(eosio::name user, uint16_t community_id);

    ACTION unfollowcomm(eosio::name user, uint16_t community_id);

    // Perform update to account
    ACTION updateacc(eosio::name user);

    // Report user profile
    ACTION reportprof(eosio::name user, eosio::name user_to_report);

    // Action give moderator flags
    ACTION givemoderflg(eosio::name user, int flags);
    
    // Action give community moderator flags
    ACTION givecommuflg(eosio::name user, int flags, uint16_t community_id);
    
    ACTION editcomm(eosio::name user, uint16_t community_id, std::string name, IpfsHash ipfs_description);

    ACTION chgqsttype(eosio::name user, uint64_t question_id, int type, bool restore_rating);

    ACTION addtotopcomm(eosio::name user, uint16_t community_id, uint64_t question_id);

    ACTION remfrmtopcom(eosio::name user, uint16_t community_id, uint64_t question_id);

    ACTION upquestion(eosio::name user, uint16_t community_id, uint64_t question_id);

    ACTION downquestion(eosio::name user, uint16_t community_id, uint64_t question_id);
    
    ACTION movequestion(eosio::name user, uint16_t community_id, uint64_t question_id, uint16_t new_position);

    ACTION apprvacc(eosio::name user);

    ACTION dsapprvacc(eosio::name user);

    ACTION addtelacc(eosio::name bot_name, eosio::name user, uint64_t telegram_id);

    ACTION addemptelacc(eosio::name bot_name, uint64_t telegram_id, std::string display_name, const IpfsHash ipfs_profile, const IpfsHash ipfs_avatar);

    //init achievements first 10k registered users
    ACTION intachregist();

#ifdef SUPERFLUOUS_INDEX
    // Delete @count@ items from superfluous index tebles
    ACTION freeindex(int count);
#endif

    ACTION init();

    ACTION payforcpu(){};

#if STAGE == 1 || STAGE == 2
    ACTION setaccrten(eosio::name user, int rating, int16_t energy);

    ACTION resettables();

    ACTION chnguserrt(eosio::name user, int16_t rating_change);
#endif

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
        bool hasLambda, bool zero_rating_forbidden);

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
                          const IpfsHash &ipfs_profile,
                          const IpfsHash &ipfs_avatar);

    void set_account_profile(eosio::name user, const IpfsHash &ipfs_profile,
                             const std::string &display_name,
                             const IpfsHash &ipfs_avatar);

    void report_profile(eosio::name user, eosio::name user_to_report);

    void post_question(eosio::name user, uint16_t community_id,
                       const std::vector<uint32_t> tags,
                       const std::string &title, const IpfsHash &ipfs_link,
                       const uint8_t type);
    
    eosio::name get_telegram_action_account(uint64_t telegram_id);

    void post_answer(eosio::name user, uint64_t question_id,
                     const IpfsHash &ipfs_link, bool official_answer);

    void post_comment(eosio::name user, uint64_t question_id,
                      uint16_t answer_id, const IpfsHash &ipfs_link);

    void delete_question(eosio::name user, uint64_t question_id);

    void delete_answer(eosio::name user, uint64_t question_id,
                       uint16_t answer_id);

    void delete_comment(eosio::name user, uint64_t question_id,
                        uint16_t answer_id, uint64_t comment_id);

    void modify_question(eosio::name user, uint64_t question_id,
                         uint16_t community_id,
                         const std::vector<uint32_t> &tags,
                         const std::string &title, const IpfsHash &ipfs_link);

    void modify_answer(eosio::name user, uint64_t question_id,
                       uint16_t answer_id, const IpfsHash &ipfs_link, bool official_answer);

    void modify_comment(eosio::name user, uint64_t question_id,
                        uint16_t answer_id, uint16_t comment_id,
                        const IpfsHash &ipfs_link);

    void create_community(eosio::name user, const std::string &name,
                          const IpfsHash &ipfs_description,
                          const std::vector<suggest_tag> &suggested_tags);

    void create_tag(eosio::name user, uint16_t commuinty_id,
                    const std::string &name, const IpfsHash &ipfs_description);

    void vote_create_community(eosio::name user, uint32_t community_id);

    void vote_create_tag(eosio::name user, uint16_t community_id,
                         uint32_t tag_id);

    void vote_delete_community(eosio::name user, uint32_t community_id);

    void vote_delete_tag(eosio::name user, uint16_t community_id,
                         uint32_t tag_id);

    void create_community_or_tag(account_index::const_iterator iter_account,
                                 uint64_t scope, const std::string &name,
                                 const IpfsHash &ipfs_description);

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

    void add_empty_telegram_account(uint64_t telegram_id, std::string display_name, IpfsHash ipfs_profile, IpfsHash ipfs_avatar);

    eosio::name generate_temp_telegram_account();
#ifdef SUPERFLUOUS_INDEX
    void remove_user_question(eosio::name user, uint64_t question_id);

    void remove_user_answer(eosio::name user, uint64_t question_id);
#endif
    void follow_community(eosio::name user, uint16_t community_id);

    void unfollow_community(eosio::name user, uint16_t community_id);

    void update_account(eosio::name user);

    void give_moderator_flag(eosio::name user, int flags);

    void give_moderator_flag(eosio::name user, int flags, uint16_t community_id);

    void edit_community(eosio::name user, uint16_t community_id, const std::string &name, const IpfsHash &ipfs_description);

    void change_question_type(eosio::name user, uint64_t question_id, int type, bool restore_rating);

    void add_top_question(eosio::name user, uint16_t community_id, uint64_t id_question);

    void remove_top_question(eosio::name user, uint16_t community_id, uint64_t question_id);

    void delete_top_question(uint16_t community_id, uint64_t question_id);

    void up_top_question(eosio::name user, uint16_t community_id, uint64_t question_id);

    void down_top_question(eosio::name user, uint16_t community_id, uint64_t question_id);

    void move_top_question(eosio::name user, uint16_t community_id, uint64_t question_id, uint16_t newposition);

    void approve_account(eosio::name user);

    void disapprove_account(eosio::name user);

    void add_telegram_account(eosio::name user, uint64_t telegram_id, bool new_account);

    void move_account_statistik(eosio::name old_user, eosio::name new_user);

    void delete_table_property_community(eosio::name old_user, eosio::name new_user);

    void delete_table_period_rating(eosio::name old_user, eosio::name new_user);

    void swap_account(eosio::name old_user, eosio::name new_user);

    void move_table_statistic(eosio::name old_user, eosio::name new_user);

    void move_table_usranswers(eosio::name old_user, eosio::name new_user);

    void move_table_usrquestions(eosio::name old_user, eosio::name new_user);

    void move_table_achieve(eosio::name old_user, eosio::name new_user);

    void update_achievement (eosio::name user, Group_achievement group, int value);

    bool increment_achievement_count(uint32_t id_achievement);

    void decrement_achievement_count(uint32_t id_achievement);

    void init_achievements_first_10k_registered_users();
};
