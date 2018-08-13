#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <map>
#include <string>
#include "access.hpp"
#include "account.hpp"
#include "display_name.hpp"
#include "peerania_utils.hpp"
#include "question_container.hpp"
#include "user_property.hpp"

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

  // Register question
  ///@abi action
  void regquestion(account_name user, std::string ipfs_link);

  // Register answer(answer question)
  ///@abi action
  void reganswer(account_name user, uint64_t question_id,
                 std::string ipfs_link);

  // Register comment
  // If the answer_id set to 0 comment question, otherwise comment question with
  // passed answer_id
  ///@abi action
  void regcomment(account_name user, uint64_t question_id, uint16_t answer_id,
                  const std::string &ipfs_link);

  // Delete question
  ///@abi action
  void delquestion(account_name user, uint64_t question_id);

  // Delete answer
  ///@abi action
  void delanswer(account_name user, uint64_t question_id, uint16_t answer_id);

  // Delete comment
  //@abi action
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
  //@abi action
  void modcomment(account_name user, uint64_t question_id, uint16_t answer_id,
                  uint16_t comment_id, const std::string &ipfs_link);

 private:
  static const scope_name all_questions = N(allquestions);

  multi_index<N(account), account> account_table;

  question_index question_table;

  void set_account_string_property(account_name owner, uint8_t key,
                                   const std::string &value);

  void set_account_integer_property(account_name owner, uint8_t key,
                                    int32_t value);

  inline void set_account_ipfs_profile(account_name owner,
                                       const std::string &ipfs_profile);

  inline void add_display_name_to_map(account_name owner,
                                      const std::string &display_name);

  inline void remove_display_name_from_map(account_name owner,
                                           const std::string &display_name);

  // Checking that the account does exist
  inline void require_for_an_account(account_name owner);

  inline void register_question(account_name user,
                                const std::string &ipfs_link);

  void register_answer(account_name user, uint64_t question_id,
                       const std::string &ipfs_link);

  void register_comment(account_name user, uint64_t question_id,
                        uint16_t answer_id, const std::string &ipfs_link);

  void delete_question(uint64_t question_id, const access &action_access);

  void delete_answer(uint64_t question_id, uint16_t answer_id,
                     const access &action_access);

  void delete_comment(uint64_t question_id, uint16_t answer_id,
                      uint64_t comment_id, const access &action_access);

  void modify_question(uint64_t question_id, const std::string &ipfs_link,
                       const access &action_access);

  void modify_answer(uint64_t question_id, uint16_t answer_id,
                     const std::string &ipfs_link, const access &action_access);

  void modify_comment(uint64_t question_id, uint16_t answer_id,
                      uint16_t comment_id, const std::string &ipfs_link,
                      const access &action_access);
};

}  // namespace eosio
