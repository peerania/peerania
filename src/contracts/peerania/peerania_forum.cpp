#include "peerania.hpp"

namespace eosio {

question_index::const_iterator peerania::find_question(uint64_t question_id) {
  auto iter_question = question_table.find(question_id);
  eosio_assert(iter_question != question_table.end(), "Question not found!");
  return iter_question;
}

void peerania::post_question(account_name user,
                                 const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, Action::POST_QUESTION);
  question_table.emplace(_self, [&](auto &question) {
    question.id = question_table.available_primary_key();
    question.user = user;
    question.ipfs_link = ipfs_link;
    question.post_time = current_time_in_sec();
  });
}

void peerania::post_answer(account_name user, uint64_t question_id,
                               const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, Action::POST_ANSWER);
  auto iter_question = find_question(question_id);
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
      new_answer.id = 1;
    else
      new_answer.id = question.answers.back().id + 1;
    question.answers.push_back(new_answer);
  });
}

void peerania::post_comment(account_name user, uint64_t question_id,
                                uint16_t answer_id,
                                const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, Action::POST_COMMENT);
  auto iter_question = find_question(question_id);
  // check if number of comments more than 2^16
  comment new_comment;
  new_comment.user = user;
  new_comment.ipfs_link = ipfs_link;
  new_comment.post_time = current_time_in_sec();
  question_table.modify(
      iter_question, _self, [answer_id, &new_comment](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          if (question.comments.empty())
            new_comment.id = 1;
          else
            new_comment.id = question.comments.back().id + 1;
          question.comments.push_back(new_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          if (iter_answer->comments.empty())
            new_comment.id = 1;
          else
            new_comment.id = iter_answer->comments.back().id + 1;
          iter_answer->comments.push_back(new_comment);
        }
      });
}

void peerania::delete_question(account_name user, uint64_t question_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::DELETE_QUESTION);
  question_table.erase(iter_question);
  eosio_assert(iter_question != question_table.end(),
               "Address not erased properly");
}

void peerania::delete_answer(account_name user, uint64_t question_id,
                             uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(
      iter_question, _self, [iter_account, answer_id](auto &question) {
        auto iter_answer = find_answer(question, answer_id);
        assert_allowed(*iter_account, iter_answer->user, Action::DELETE_ANSWER);
        question.answers.erase(iter_answer);
      });
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
          assert_allowed(*iter_account, iter_comment->user, Action::DELETE_COMMENT);
          question.comments.erase(iter_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user, Action::DELETE_COMMENT);
          iter_answer->comments.erase(iter_comment);
        }
      });
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
                          assert_allowed(*iter_account, iter_answer->user, Action::MODIFY_ANSWER);
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
          assert_allowed(*iter_account, iter_comment->user, Action::MODIFY_COMMENT);
          iter_comment->ipfs_link = ipfs_link;
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user, Action::MODIFY_COMMENT);
          iter_comment->ipfs_link = ipfs_link;
        }
      });
}

void peerania::mark_answer_as_correct(account_name user, uint64_t question_id,
                                      uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto itr_question = find_question(question_id);
  assert_allowed(*iter_account, itr_question->user, Action::MARK_ANSWER_AS_CORRECT);
  if (answer_id != APPLY_TO_QUESTION) {
    eosio_assert(binary_find(itr_question->answers.begin(), itr_question->answers.end(), answer_id) !=
                     itr_question->answers.end(),
                 "Answer not found");
  }
  question_table.modify(itr_question, _self, [answer_id](auto &question) {
    question.correct_answer_id = (question.correct_answer_id == answer_id)
                                     ? APPLY_TO_QUESTION
                                     : answer_id;
  });
}

}  // namespace eosio