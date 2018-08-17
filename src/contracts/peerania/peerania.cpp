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
  access action_access(*itr, access::ACTION::DELETE_QUESTION);
  delete_question(question_id, action_access);
}
void peerania::delanswer(account_name user, uint64_t question_id,
                         uint16_t answer_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::DELETE_ANSWER);
  delete_answer(question_id, answer_id, action_access);
}

void peerania::delcomment(account_name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::DELETE_COMMENT);
  delete_comment(question_id, answer_id, comment_id, action_access);
}
void peerania::modquestion(account_name user, uint64_t question_id,
                           const std::string &ipfs_link) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::MODIFY_QUESTION);
  modify_question(question_id, ipfs_link, action_access);
}

void peerania::modanswer(account_name user, uint64_t question_id,
                         uint16_t answer_id, const std::string &ipfs_link) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::MODIFY_ANSWER);
  modify_answer(question_id, answer_id, ipfs_link, action_access);
}
void peerania::modcomment(account_name user, uint64_t question_id,
                          uint16_t answer_id, uint16_t comment_id,
                          const std::string &ipfs_link) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::MODIFY_COMMENT);
  modify_comment(question_id, answer_id, comment_id, ipfs_link, action_access);
}

void peerania::upvote(account_name user, uint64_t question_id,
                      uint16_t answer_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::UPVOTE);
  vote(question_id, answer_id, action_access, true);
}

void peerania::downvote(account_name user, uint64_t question_id,
                        uint16_t answer_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::DOWNVOTE);
  vote(question_id, answer_id, action_access, false);
}

void peerania::mrkascorrect(account_name user, uint64_t question_id,
                            uint16_t answer_id) {
  require_auth(user);
  auto itr = account_table.find(user);
  eosio_assert(itr != account_table.end(), "Account not registered");
  access action_access(*itr, access::ACTION::MARK_ANSWER_AS_CORRECT);
  mark_answer_as_correct(question_id, answer_id, action_access);
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
      property_iter->value = value;
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
      property_iter->value = value;
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
  // Linear check
  // eosio_assert(none_of(iter->answers.begin(), iter->answers.end(),
  //                     [user](const answer &a) { return a.user == user; }),
  //             "Answer with this username alredy registered");
  history history_table(_self, user);
  auto itr_history =
      history_table.find(hash_history(question_id, COMMENT_TO_QUESTION));
  if (itr_history != history_table.end()) {
    eosio_assert(!(itr_history->is_flag_set(HISTORY_ALREADY_ANSWERED)),
                 "Answer with this username alredy registered");
  } else {
    history_table.emplace(_self, [question_id](auto &history_item) {
      history_item.hash_id = hash_history(question_id, COMMENT_TO_QUESTION);
      history_item.set_flag(HISTORY_ALREADY_ANSWERED);
    });
  }
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
      if (iter_answer->comments.empty())
        new_comment.id = 1;
      else
        new_comment.id = iter_answer->comments.back().id + 1;
      iter_answer->comments.push_back(new_comment);
    }
  });
}

void peerania::delete_question(uint64_t question_id,
                               const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  eosio_assert(action_access.is_allowed(iter->user), "Action not allowed");
  question_table.erase(iter);
  eosio_assert(iter != question_table.end(), "Address not erased properly");
}

void peerania::delete_answer(uint64_t question_id, uint16_t answer_id,
                             const access &action_access) {
  auto iter = question_table.find(question_id);
  eosio_assert(iter != question_table.end(), "Question not found");
  account_name owner;
  question_table.modify(iter, _self, [&owner, answer_id, &action_access](auto &question) {
    auto iter_answer =
        binary_find(question.answers.begin(), question.answers.end(), answer_id,
                    [](const answer &a) { return a.id; });
    owner = iter_answer->user;
    eosio_assert(iter_answer != question.answers.end(), "Answer not found");
    eosio_assert(action_access.is_allowed(iter_answer->user),
                 "Action not allowed");
    question.answers.erase(iter_answer);
  });
  history history_table(_self, owner);
  auto itr_history =  history_table.find(hash_history(question_id, COMMENT_TO_QUESTION));
  eosio_assert(itr_history != history_table.end(), "History error");
  history_table.erase(itr_history);
  eosio_assert(itr_history != history_table.end(), "Address not erased properly");
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
      eosio_assert(action_access.is_allowed(iter_comment->user),
                   "Action not allowed");
      question.comments.erase(iter_comment);
    } else {
      auto iter_answer =
          binary_find(question.answers.begin(), question.answers.end(),
                      answer_id, [](const answer &a) { return a.id; });
      eosio_assert(iter_answer != question.answers.end(), "Answer not found");
      auto iter_comment = binary_find(iter_answer->comments.begin(),
                                      iter_answer->comments.end(), comment_id,
                                      [](const comment &c) { return c.id; });
      eosio_assert(iter_comment != question.comments.end(),
                   "Comment not found");
      eosio_assert(action_access.is_allowed(iter_comment->user),
                   "Action not allowed");
      iter_answer->comments.erase(iter_comment);
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
    eosio_assert(action_access.is_allowed(iter_answer->user),
                 "Action not allowed");
    iter_answer->ipfs_link = ipfs_link;
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
      eosio_assert(action_access.is_allowed(iter_comment->user),
                   "Action not allowed");
      iter_comment->ipfs_link = ipfs_link;
    } else {
      auto iter_answer =
          binary_find(question.answers.begin(), question.answers.end(),
                      answer_id, [](const answer &a) { return a.id; });
      eosio_assert(iter_answer != question.answers.end(), "Answer not found");
      auto iter_comment = binary_find(iter_answer->comments.begin(),
                                      iter_answer->comments.end(), comment_id,
                                      [](const comment &c) { return c.id; });
      eosio_assert(iter_comment != question.comments.end(),
                   "Comment not found");
      eosio_assert(action_access.is_allowed(iter_comment->user),
                   "Action not allowed");
      iter_comment->ipfs_link = ipfs_link;
    }
  });
}

int8_t modify_vote_history(history_item &item, bool is_upvote) {
  int8_t rating_change;
  if (is_upvote) {
    if (item.is_flag_set(HISTORY_UPVOTED)) {
      rating_change = -1;
      item.remove_flag(HISTORY_UPVOTED);
    } else {
      if (item.is_flag_set(HISTORY_DOWNVOTED)) {
        rating_change = 2;
        item.remove_flag(HISTORY_DOWNVOTED);
      } else
        rating_change = 1;
      item.set_flag(HISTORY_UPVOTED);
    }
  } else {
    if (item.is_flag_set(HISTORY_DOWNVOTED)) {
      rating_change = 1;
      item.remove_flag(HISTORY_DOWNVOTED);
    } else {
      if (item.is_flag_set(HISTORY_UPVOTED)) {
        rating_change = -2;
        item.remove_flag(HISTORY_UPVOTED);
      } else
        rating_change = -1;
      item.set_flag(HISTORY_DOWNVOTED);
    }
  }
  return rating_change;
}

template <typename T>
void check_answer_exist(T itr_question, uint16_t answer_id) {
  if (answer_id != COMMENT_TO_QUESTION) {
    auto iter_answer =
        binary_find(itr_question->answers.begin(), itr_question->answers.end(),
                    answer_id, [](const answer &a) { return a.id; });
    eosio_assert(iter_answer != itr_question->answers.end(),
                 "Answer not found");  // vulnerability
  }
}

void peerania::vote(uint64_t question_id, uint16_t answer_id,
                    const access &action_access, bool is_upvote) {
  eosio_assert(action_access.is_allowed(), "Action not allowed");
  auto itr_question = question_table.find(question_id);
  eosio_assert(itr_question != question_table.end(), "Question not found");
  check_answer_exist(itr_question, answer_id);
  history history_table(_self, action_access.get_account_name());
  auto itr_history = history_table.find(hash_history(question_id, answer_id));
  int8_t rating_change;
  if (itr_history != history_table.end()) {
    history_table.modify(itr_history, _self,
                         [&rating_change, is_upvote](auto &item) {
                           rating_change = modify_vote_history(item, is_upvote);
                         });
  } else {
    history_table.emplace(_self, [is_upvote, question_id, answer_id,
                                  &rating_change](auto &history_item) {
      history_item.hash_id = hash_history(question_id, answer_id);
      if (is_upvote) {
        history_item.set_flag(HISTORY_UPVOTED);
        rating_change = 1;
      } else {
        history_item.set_flag(HISTORY_DOWNVOTED);
        rating_change = -1;
      }
    });
  }
  question_table.modify(
      itr_question, _self, [rating_change, answer_id](auto &question) {
        if (answer_id == COMMENT_TO_QUESTION) {
          question.rating += rating_change;
        } else {
          auto itr_answer =
              binary_find(question.answers.begin(), question.answers.end(),
                          answer_id, [](answer &a) { return a.id; });
          (itr_answer->rating) += rating_change;
        }
      });
}

void peerania::mark_answer_as_correct(uint64_t question_id, uint16_t answer_id,
                                      const access &action_access) {
  auto itr_question = question_table.find(question_id);
  eosio_assert(itr_question != question_table.end(), "Question not found");
  eosio_assert(action_access.is_allowed(itr_question->user),
               "Action not allowed");
  check_answer_exist(itr_question, answer_id);
  question_table.modify(itr_question, _self, [answer_id](auto &question) {
    question.correct_answer_id =
        (question.correct_answer_id == answer_id)
            ? COMMENT_TO_QUESTION : answer_id;
  });
}

}  // namespace eosio
EOSIO_ABI(
    eosio::peerania,
    (registeracc)(setaccintprp)(setaccstrprp)(setipfspro)(setdispname)(
        regquestion)(reganswer)(regcomment)(delquestion)(delanswer)(delcomment)(
        modanswer)(modquestion)(modcomment)(upvote)(downvote)(mrkascorrect))
