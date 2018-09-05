#include "peerania.hpp"

namespace eosio {

question_index::const_iterator peerania::find_question(uint64_t question_id) {
  auto iter_question = question_table.find(question_id);
  eosio_assert(iter_question != question_table.end(), "Question not found!");
  return iter_question;
}

void peerania::post_question(account_name user, const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, Action::POST_QUESTION);
  question_table.emplace(_self, [&](auto &question) {
    question.id = question_table.available_primary_key();
    question.user = user;
    question.ipfs_link = ipfs_link;
    question.post_time = current_time_in_sec();
  });
  update_rating(iter_account, POST_QUESTION_REWARD);
}

void peerania::post_answer(account_name user, uint64_t question_id,
                           const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, Action::POST_ANSWER);
  auto iter_question = find_question(question_id);
  eosio_assert(iter_question->answers.size() < MAX_ANSWER_COUNT,
               "For this question reached answer count limit");
  eosio_assert(
      none_of(iter_question->answers.begin(), iter_question->answers.end(),
              [user](const answer &a) { return a.user == user; }),
      "Answer with this username alredy posted");
  answer new_answer;
  new_answer.user = user;
  new_answer.ipfs_link = ipfs_link;
  new_answer.post_time = current_time_in_sec();
  question_table.modify(iter_question, _self, [&new_answer](auto &question) {
    if (question.answers.empty())
      new_answer.id = ANSWER_INDEX_START;
    else
      new_answer.id = question.answers.back().id + 1;
    question.answers.push_back(new_answer);
  });
  update_rating(iter_account, POST_ANSWER_REWARD);
}

void peerania::post_comment(account_name user, uint64_t question_id,
                            uint16_t answer_id, const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, Action::POST_COMMENT);
  auto iter_question = find_question(question_id);
  comment new_comment;
  new_comment.user = user;
  new_comment.ipfs_link = ipfs_link;
  new_comment.post_time = current_time_in_sec();
  question_table.modify(
      iter_question, _self, [answer_id, &new_comment](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          eosio_assert(question.comments.size() < MAX_ANSWER_COUNT,
                       "For this question reached comment count limit");
          if (question.comments.empty())
            new_comment.id = COMMENT_INDEX_START;
          else
            new_comment.id = question.comments.back().id + 1;
          question.comments.push_back(new_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          eosio_assert(iter_answer->comments.size() < MAX_ANSWER_COUNT,
                       "For this answer reached comment count limit");
          if (iter_answer->comments.empty())
            new_comment.id = COMMENT_INDEX_START;
          else
            new_comment.id = iter_answer->comments.back().id + 1;
          iter_answer->comments.push_back(new_comment);
        }
      });
  update_rating(iter_account, POST_COMMENT_REWARD);
}

void peerania::delete_question(account_name user, uint64_t question_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::DELETE_QUESTION);
  eosio_assert(iter_question->answers.empty(), "You can't delete not empty question");
  question_table.erase(iter_question);
  eosio_assert(iter_question != question_table.end(),
               "Address not erased properly");
  update_rating(iter_account, DELETE_OWN_QUESTION_REWARD);
}

void peerania::delete_answer(account_name user, uint64_t question_id,
                             uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio_assert(iter_question->correct_answer_id != answer_id, "You can't delete this answer");
  question_table.modify(
      iter_question, _self, [iter_account, answer_id](auto &question) {
        auto iter_answer = find_answer(question, answer_id);
        assert_allowed(*iter_account, iter_answer->user, Action::DELETE_ANSWER);
        question.answers.erase(iter_answer);
      });
  update_rating(iter_account, DELETE_OWN_ANSWER_REWARD);
}

void peerania::delete_comment(account_name user, uint64_t question_id,
                              uint16_t answer_id, uint64_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, comment_id](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          auto iter_comment = find_comment(question, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::DELETE_COMMENT);
          question.comments.erase(iter_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::DELETE_COMMENT);
          iter_answer->comments.erase(iter_comment);
        }
      });
  update_rating(iter_account, DELETE_OWN_COMMENT_REWARD);
}

void peerania::modify_question(account_name user, uint64_t question_id,
                               const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::MODIFY_QUESTION);
  question_table.modify(iter_question, _self, [&ipfs_link](auto &question) {
    question.ipfs_link = ipfs_link;
  });
}

void peerania::modify_answer(account_name user, uint64_t question_id,
                             uint16_t answer_id, const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(iter_question, _self,
                        [iter_account, answer_id, &ipfs_link](auto &question) {
                          auto iter_answer = find_answer(question, answer_id);
                          assert_allowed(*iter_account, iter_answer->user,
                                         Action::MODIFY_ANSWER);
                          iter_answer->ipfs_link = ipfs_link;
                        });
}

void peerania::modify_comment(account_name user, uint64_t question_id,
                              uint16_t answer_id, uint16_t comment_id,
                              const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, comment_id, &ipfs_link](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          auto iter_comment = find_comment(question, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::MODIFY_COMMENT);
          iter_comment->ipfs_link = ipfs_link;
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::MODIFY_COMMENT);
          iter_comment->ipfs_link = ipfs_link;
        }
      });
}

void peerania::mark_answer_as_correct(account_name user, uint64_t question_id,
                                      uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user,
                 Action::MARK_ANSWER_AS_CORRECT);
  if (answer_id != APPLY_TO_QUESTION) {
    eosio_assert(iter_question->correct_answer_id != answer_id,
                 "This answer already marked as correct");
    // Using const iterator; probably better rewrrite find_answer as template
    auto iter_answer = binary_find(iter_question->answers.begin(),
                                   iter_question->answers.end(), answer_id);
    eosio_assert(iter_answer != iter_question->answers.end(),
                 "Answer not found");
    if (iter_question->correct_answer_id == APPLY_TO_QUESTION) {
      update_rating(iter_account, ACCEPT_ANSWER_AS_CORRECT_REWARD);
      update_rating(iter_answer->user,
                    ANSWER_ACCEPTED_AS_CORRECT_REWARD);
    } else {
      auto iter_old_answer = binary_find(iter_question->answers.begin(),
                                         iter_question->answers.end(),
                                         iter_question->correct_answer_id);
      // check internal error iter_old_answer
      update_rating(iter_old_answer->user,
                    -ANSWER_ACCEPTED_AS_CORRECT_REWARD);
      update_rating(iter_answer->user,
                    ANSWER_ACCEPTED_AS_CORRECT_REWARD);
    }
  } else {
    eosio_assert(
        iter_question->correct_answer_id != APPLY_TO_QUESTION,
        "You can\'t reset correct answer for question without correct answer");
    auto iter_old_answer = binary_find(iter_question->answers.begin(),
                                         iter_question->answers.end(),
                                         iter_question->correct_answer_id);
    // check internal error iter_old_answer
    update_rating(iter_account, -ACCEPT_ANSWER_AS_CORRECT_REWARD);
    update_rating(iter_old_answer->user,
                    -ANSWER_ACCEPTED_AS_CORRECT_REWARD);
  }
  question_table.modify(iter_question, _self, [answer_id](auto &question) {
    question.correct_answer_id = (question.correct_answer_id == answer_id)
                                     ? APPLY_TO_QUESTION
                                     : answer_id;
  });
}

}  // namespace eosio