#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include "access.hpp"
#include "account.hpp"
#include "display_name.hpp"
#include "economy.h"
#include "history.hpp"
#include "property.hpp"
#include "question_container.hpp"
#include "utils.hpp"

namespace eosio {
class peerania : public contract {
 public:
  peerania(account_name self)
      : contract(self),
        account_table(self, all_accounts),
        question_table(self, all_questions) {}

  // Register new user
  ///@abi action
  void registeracc(account_name owner, std::string display_name,
                   std::string ipfs_profile);

  // Set(or add) property to account
  ///@abi action
  void setaccstrprp(account_name owner, uint8_t key, std::string value);

  // Set(or add) property to account
  ///@abi action
  void setaccintprp(account_name owner, uint8_t key, int32_t value);

  // Set user profile (IPFS link)
  ///@abi action
  void setipfspro(account_name owner, std::string ipfs_profile);

  // Set user display name
  ///@abi action
  void setdispname(account_name owner, std::string display_name);

  // Post question
  ///@abi action
  void postquestion(account_name user, std::string ipfs_link);

  // Post answer(answer question)
  ///@abi action
  void postanswer(account_name user, uint64_t question_id,
                 std::string ipfs_link);

  // Post comment
  // If the answer_id set to 0 comment question, otherwise comment question with
  // passed answer_id
  ///@abi action
  void postcomment(account_name user, uint64_t question_id, uint16_t answer_id,
                  const std::string &ipfs_link);

  // Delete question
  ///@abi action
  void delquestion(account_name user, uint64_t question_id);

  // Delete answer
  ///@abi action
  void delanswer(account_name user, uint64_t question_id, uint16_t answer_id);

  // Delete comment
  ///@abi action
  void delcomment(account_name user, uint64_t question_id, uint16_t answer_id,
                  uint16_t comment_id);

  // Modify question
  ///@abi action
  void modquestion(account_name user, uint64_t question_id,
                   const std::string &ipfs_link);

  // Modify answer
  ///@abi action
  void modanswer(account_name user, uint64_t question_id, uint16_t answer_id,
                 const std::string &ipfs_link);

  // Modify comment
  ///@abi action
  void modcomment(account_name user, uint64_t question_id, uint16_t answer_id,
                  uint16_t comment_id, const std::string &ipfs_link);

  // Upvote question/answer
  ///@abi action
  void upvote(account_name user, uint64_t question_id, uint16_t answer_id);

  // Downvote question/answer
  ///@abi action
  void downvote(account_name user, uint64_t question_id, uint16_t answer_id);

  // Vote for deletion
  // if (answer_id == 0) delete question(by question_id)
  // elif (comment_id == 0) delete answer question(question_id)->answer(by
  // answer_id) elif delete comment
  // question(question_id)->answer(answer_id)->comment(by comment_id)
  ///@abi action
  void votedelete(account_name user, uint64_t question_id, uint16_t answer_id,
                  uint16_t comment_id);

  // Vote for moderation
  // if (answer_id == 0) delete question(by question_id)
  // elif (comment_id == 0) delete answer question(question_id)->answer(by
  // answer_id) elif delete comment
  // question(question_id)->answer(answer_id)->comment(by comment_id)
  ///@abi action
  void votemoderate(account_name user, uint64_t question_id, uint16_t answer_id,
                    uint16_t comment_id);

  // Mark answer as correct
  ///@abi action
  void mrkascorrect(account_name user, uint64_t question_id,
                    uint16_t answer_id);

  // Debug methoods
#ifdef DEBUG
  // Set account rating and moderation points count
  ///@abi action
  void setaccrtmpc(account_name user, int16_t rating,
                   uint16_t moderation_points);
#endif

 private:
  question_index question_table;

  account_index account_table;

  void register_account(account_name owner, std::string display_name,
                        const std::string &ipfs_profile);

  void set_account_ipfs_profile(account_name owner,
                                const std::string &ipfs_profile);

  void set_account_display_name(account_name owner,
                                const std::string &display_name);

  void set_account_string_property(account_name owner, uint8_t key,
                                   const std::string &value);

  void set_account_integer_property(account_name owner, uint8_t key,
                                    int32_t value);

  inline void add_display_name_to_map(account_name owner,
                                      const std::string &display_name);

  inline void remove_display_name_from_map(account_name owner,
                                           const std::string &display_name);

  inline account_index::const_iterator find_account(account_name owner);

  inline question_index::const_iterator find_question(uint64_t question_id);

  inline void post_question(account_name user,
                                const std::string &ipfs_link);

  void post_answer(account_name user, uint64_t question_id,
                       const std::string &ipfs_link);

  void post_comment(account_name user, uint64_t question_id,
                        uint16_t answer_id, const std::string &ipfs_link);

  void delete_question(account_name user, uint64_t question_id);

  void delete_answer(account_name user, uint64_t question_id,
                     uint16_t answer_id);

  void delete_comment(account_name user, uint64_t question_id,
                      uint16_t answer_id, uint64_t comment_id);

  void modify_question(account_name user, uint64_t question_id,
                       const std::string &ipfs_link);

  void modify_answer(account_name user, uint64_t question_id,
                     uint16_t answer_id, const std::string &ipfs_link);

  void modify_comment(account_name user, uint64_t question_id,
                      uint16_t answer_id, uint16_t comment_id,
                      const std::string &ipfs_link);

  void vote(account_name user, uint64_t question_id, uint16_t answer_id,
            bool is_upvote);

  void mark_answer_as_correct(account_name user, uint64_t question_id,
                              uint16_t answer_id);

  void vote_for_deletion(account_name user, uint64_t question_id,
                         uint16_t answer_id, uint16_t comment_id);

  inline void update_rating(account_index::const_iterator iter_account, int rating_change);

  inline void update_rating(account_name user, int rating_change);

};
}  // namespace eosio


