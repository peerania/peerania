#include "peerania.hpp"

namespace eosio {

void peerania::registeracc(account_name owner, std::string display_name,
                           std::string ipfs_profile) {
  require_auth(owner);
  eosio_assert(account_table.find(owner) == account_table.end(),
               "Account already exists");
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  account_table.emplace(_self, [&](auto &account) {
    account.owner = owner;
    account.display_name = display_name;
    account.ipfs_profile = ipfs_profile;
    account.registration_time = current_time_in_sec();
  });
  add_display_name_to_map(owner, display_name);
}

void peerania::setaccstrprp(account_name owner, uint8_t key,
                            std::string value) {
  require_auth(owner);
  set_account_string_property(owner, key, value);
}

void peerania::setaccintprp(account_name owner, uint8_t key, int32_t value) {
  require_auth(owner);
  set_account_integer_property(owner, key, value);
}

void peerania::setipfspro(account_name owner, std::string ipfs_profile) {
  require_auth(owner);
  set_account_ipfs_profile(owner, ipfs_profile);
}

void peerania::setdispname(account_name owner, std::string display_name) {
  require_auth(owner);
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  auto itraccs = account_table.find(owner);
  eosio_assert(itraccs != account_table.end(), "Account not found");
  remove_display_name_from_map(owner, itraccs->display_name);
  account_table.modify(itraccs, _self,
                       [&](auto &acc) { acc.display_name = display_name; });
  add_display_name_to_map(owner, display_name);
}

void peerania::regquestion(account_name user, std::string ipfs_link) {
  require_auth(user);
  require_for_an_account(user);
  register_question(user, ipfs_link);
}

void peerania::reganswer(account_name user, uint64_t question_id,
                         std::string ipfs_link) {
  require_auth(user);
  require_for_an_account(user);
  register_answer(user, question_id, ipfs_link);
}

void peerania::regcomment(account_name user, uint64_t question_id,
                          uint16_t answer_id, const std::string &ipfs_link) {
  require_auth(user);
  require_for_an_account(user);
  register_comment(user, question_id, answer_id, ipfs_link);
}

void peerania::delquestion(account_name user, uint64_t question_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access((*itr), access::ACTION::DELETE_QUESTION);
  delete_question(question_id, action_access);
}
void peerania::delanswer(account_name user, uint64_t question_id,
                         uint16_t answer_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access((*itr), access::ACTION::DELETE_ANSWER);
  delete_answer(question_id, answer_id, action_access);
}

void peerania::delcomment(account_name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access((*itr), access::ACTION::DELETE_COMMENT);
  delete_comment(question_id, answer_id, comment_id, action_access);
}
void peerania::modquestion(account_name user, uint64_t question_id,
                           const std::string &ipfs_link) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access((*itr), access::ACTION::MODIFY_QUESTION);
  modify_question(question_id, ipfs_link, action_access);
}

void peerania::modanswer(account_name user, uint64_t question_id,
                         uint16_t answer_id, const std::string &ipfs_link) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access((*itr), access::ACTION::MODIFY_ANSWER);
  modify_answer(question_id, answer_id, ipfs_link, action_access);
}
void peerania::modcomment(account_name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id,
                          const std::string &ipfs_link) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access((*itr), access::ACTION::MODIFY_COMMENT);
  modify_comment(question_id, answer_id, comment_id, ipfs_link, action_access);
}

void peerania::set_account_string_property(account_name owner, uint8_t key,
                                           const std::string &value) {
  auto itr = account_table.find(owner);
  eosio_assert(itr != account_table.end(), "Account not found");
  account_table.modify(itr, _self, [&](auto &account) {
    auto property_iter = linear_find(
        account.string_properties.begin(), account.string_properties.end(), key,
        [](const str_key_value &skv) { return skv.key; });
    if (property_iter == account.string_properties.end()) {
      str_key_value skv;
      skv.key = key;
      skv.value = value;
      account.string_properties.push_back(skv);
    } else
      (*property_iter).value = value;
  });
}

void peerania::set_account_integer_property(account_name owner, uint8_t key,
                                            int32_t value) {
  auto itr = account_table.find(owner);
  eosio_assert(itr != account_table.end(), "Account not found");
  account_table.modify(itr, _self, [&](auto &account) {
    auto property_iter = linear_find(
        account.integer_properties.begin(), account.integer_properties.end(),
        key, [](const int_key_value &skv) { return skv.key; });
    if (property_iter == account.integer_properties.end()) {
      int_key_value ikv;
      ikv.key = key;
      ikv.value = value;
      account.integer_properties.push_back(ikv);
    } else
      (*property_iter).value = value;
  });
}

void peerania::set_account_ipfs_profile(account_name owner,
                                        const std::string &ipfs_profile) {
  auto itr = account_table.find(owner);
  eosio_assert(itr != account_table.end(), "Account not found");
  account_table.modify(
      itr, _self, [&](auto &account) { account.ipfs_profile = ipfs_profile; });
}

void peerania::add_display_name_to_map(account_name owner,
                                       const std::string &display_name) {
  disp_to_acc_index table(_self, hash_display_name(display_name));
  table.emplace(_self, [&](auto &item) {
    item.owner = owner;
    item.display_name = display_name;
  });
}

void peerania::remove_display_name_from_map(account_name owner,
                                            const std::string &display_name) {
  disp_to_acc_index dtatable(_self, hash_display_name(display_name));
  auto itr_disptoacc = dtatable.find(owner);
  eosio_assert(itr_disptoacc != dtatable.end(), "display_name not found");
  dtatable.erase(itr_disptoacc);
  eosio_assert(itr_disptoacc != dtatable.end(), "Address not erased properly");
}

void peerania::require_for_an_account(account_name owner) {
  eosio_assert(account_table.find(owner) != account_table.end(),
               "Account not registered");
}

void peerania::register_question(account_name user,
                                 const std::string &ipfs_link) {
  question_table.emplace(_self, [&](auto &question) {
    question.id = question_table.available_primary_key();
    question.user = user;
    question.ipfs_link = ipfs_link;
    question.registration_time = current_time_in_sec();
  });
}

void peerania::register_answer(account_name user, uint64_t question_id,
                               const std::string &ipfs_link) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  // check if number of answers more than 2^16
  // not implemented
  // chect duplicate answer
  eosio_assert(none_of((*iter).answers.begin(), (*iter).answers.end(),
                       [user](const answer &a) { return a.user == user; }),
               "Answer with this username alredy registered");
  answer new_answer;
  new_answer.user = user;
  new_answer.ipfs_link = ipfs_link;
  new_answer.registration_time = current_time_in_sec();
  question_table.modify(iter, _self, [&](auto &question) {
    if (question.answers.empty())
      new_answer.id = 1;
    else
      new_answer.id = question.answers.back().id + 1;
    question.answers.push_back(new_answer);
  });
}

void peerania::register_comment(account_name user, uint64_t question_id,
                                uint16_t answer_id,
                                const std::string &ipfs_link) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  // check if number of comments more than 2^16
  comment new_comment;
  new_comment.user = user;
  new_comment.ipfs_link = ipfs_link;
  new_comment.registration_time = current_time_in_sec();
  question_table.modify(iter, _self, [&](auto &question) {
    if (answer_id == COMMENT_TO_QUESTION) {
      if (question.comments.empty())
        new_comment.id = 1;
      else
        new_comment.id = question.comments.back().id + 1;
      question.comments.push_back(new_comment);
    } else {
      auto iter_answer =
          binary_find(question.answers.begin(), question.answers.end(),
                      answer_id, [](const answer &a) { return a.id; });
      eosio_assert(iter_answer != question.answers.end(), "Answer not found");
      if ((*iter_answer).comments.empty())
        new_comment.id = 1;
      else
        new_comment.id = (*iter_answer).comments.back().id + 1;
      (*iter_answer).comments.push_back(new_comment);
    }
  });
}

void peerania::delete_question(uint64_t question_id,
                               const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  eosio_assert(action_access.is_allowed((*iter).user), "Action not allowed");
  question_table.erase(iter);
  eosio_assert(iter != question_table.end(), "Address not erased properly");
}

void peerania::delete_answer(uint64_t question_id, uint16_t answer_id,
                             const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  question_table.modify(iter, _self, [&](auto &question) {
    auto iter_answer =
        binary_find(question.answers.begin(), question.answers.end(), answer_id,
                    [](const answer &a) { return a.id; });
    eosio_assert(iter_answer != question.answers.end(), "Answer not found");
    eosio_assert(action_access.is_allowed((*iter_answer).user),
                 "Action not allowed");
    question.answers.erase(iter_answer);
  });
}

void peerania::delete_comment(uint64_t question_id, uint16_t answer_id,
                              uint64_t comment_id,
                              const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  question_table.modify(iter, _self, [&](auto &question) {
    if (answer_id == COMMENT_TO_QUESTION) {
      auto iter_comment =
          binary_find(question.comments.begin(), question.comments.end(),
                      comment_id, [](const comment &c) { return c.id; });
      eosio_assert(iter_comment != question.comments.end(),
                   "Comment not found");
      eosio_assert(action_access.is_allowed((*iter_comment).user),
                   "Action not allowed");
      question.comments.erase(iter_comment);
    } else {
      auto iter_answer =
          binary_find(question.answers.begin(), question.answers.end(),
                      answer_id, [](const answer &a) { return a.id; });
      eosio_assert(iter_answer != question.answers.end(), "Answer not found");
      auto iter_comment = binary_find((*iter_answer).comments.begin(),
                                      (*iter_answer).comments.end(), comment_id,
                                      [](const comment &c) { return c.id; });
      eosio_assert(iter_comment != question.comments.end(),
                   "Comment not found");
      eosio_assert(action_access.is_allowed((*iter_comment).user),
                   "Action not allowed");
      (*iter_answer).comments.erase(iter_comment);
    }
  });
}

void peerania::modify_question(uint64_t question_id,
                               const std::string &ipfs_link,
                               const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  question_table.modify(iter, _self, [&](auto &question) {
    eosio_assert(action_access.is_allowed(question.user), "Action not allowed");
    question.ipfs_link = ipfs_link;
  });
}

void peerania::modify_answer(uint64_t question_id, uint16_t answer_id,
                             const std::string &ipfs_link,
                             const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  question_table.modify(iter, _self, [&](auto &question) {
    auto iter_answer =
        binary_find(question.answers.begin(), question.answers.end(), answer_id,
                    [](const answer &a) { return a.id; });
    eosio_assert(iter_answer != question.answers.end(), "Answer not found");
    eosio_assert(action_access.is_allowed((*iter_answer).user),
                 "Action not allowed");
    (*iter_answer).ipfs_link = ipfs_link;
  });
}

void peerania::modify_comment(uint64_t question_id, uint16_t answer_id,
                              uint16_t comment_id, const std::string &ipfs_link,
                              const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  question_table.modify(iter, _self, [&](auto &question) {
    if (answer_id == COMMENT_TO_QUESTION) {
      auto iter_comment =
          binary_find(question.comments.begin(), question.comments.end(),
                      comment_id, [](const comment &c) { return c.id; });
      eosio_assert(iter_comment != question.comments.end(),
                   "Comment not found");
      eosio_assert(action_access.is_allowed((*iter_comment).user),
                   "Action not allowed");
      (*iter_comment).ipfs_link = ipfs_link;
    } else {
      auto iter_answer =
          binary_find(question.answers.begin(), question.answers.end(),
                      answer_id, [](const answer &a) { return a.id; });
      eosio_assert(iter_answer != question.answers.end(), "Answer not found");
      auto iter_comment = binary_find((*iter_answer).comments.begin(),
                                      (*iter_answer).comments.end(), comment_id,
                                      [](const comment &c) { return c.id; });
      eosio_assert(iter_comment != question.comments.end(),
                   "Comment not found");
      eosio_assert(action_access.is_allowed((*iter_comment).user),
                   "Action not allowed");
      (*iter_comment).ipfs_link = ipfs_link;
    }
  });
}

}  // namespace eosio
EOSIO_ABI(eosio::peerania,
          (registeracc)(setaccintprp)(setaccstrprp)(setipfspro)(setdispname)(
              regquestion)(reganswer)(regcomment)(delquestion)(delanswer)(
              delcomment)(modanswer)(modquestion)(modcomment))
