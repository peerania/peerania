#include "peerania.hpp"

question_index::const_iterator peerania::find_question(uint64_t question_id) {
  auto iter_question = question_table.find(question_id);
  eosio_assert(iter_question != question_table.end(), "Question not found!");
  return iter_question;
}

void peerania::post_question(eosio::name user, const std::string &title,
                             const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  assert_title(title);
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::POST_QUESTION);

  account_table.modify(iter_account, _self, [](auto &account) {
    account.update();
    eosio_assert(account.questions_left > 0, "Reached weekly question limit");
    account.questions_left -= 1;
  });

  question_table.emplace(_self, [&](auto &question) {
    question.id = get_quiestion_pk(question_table);
    question.user = user;
    question.title = title;
    question.ipfs_link = ipfs_link;
    question.post_time = now();
  });

  update_rating(iter_account, POST_QUESTION_REWARD);
}

void peerania::post_answer(eosio::name user, uint64_t question_id,
                           const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio_assert(iter_question->answers.size() < MAX_ANSWER_COUNT,
               "For this question reached answer count limit");
  assert_allowed(*iter_account, iter_question->user, Action::POST_ANSWER);
  eosio_assert(
      none_of(iter_question->answers.begin(), iter_question->answers.end(),
              [user](const answer &a) { return a.user == user; }),
      "Answer with this username alredy posted");
  answer new_answer;
  new_answer.user = user;
  new_answer.ipfs_link = ipfs_link;
  new_answer.post_time = now();
  question_table.modify(iter_question, _self, [&new_answer](auto &question) {
    push_new_forum_item(question.answers, new_answer);
  });
  update_rating(iter_account, POST_ANSWER_REWARD);
}

void peerania::post_comment(eosio::name user, uint64_t question_id,
                            uint16_t answer_id, const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  comment new_comment;
  new_comment.user = user;
  new_comment.ipfs_link = ipfs_link;
  new_comment.post_time = now();
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, &new_comment](auto &question) {
        if (apply_to_question(answer_id)) {
          assert_allowed(*iter_account, question.user, Action::POST_COMMENT);
          eosio_assert(question.comments.size() < MAX_COMMENT_COUNT,
                       "For this question reached comment count limit");
          assert_comment_limit(*iter_account, question.user,
                               question.comments);
          push_new_forum_item(question.comments, new_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          eosio_assert(iter_answer->comments.size() < MAX_COMMENT_COUNT,
                       "For this answer reached comment count limit");
          auto global_item_owner = question.user == iter_account->owner
                                       ? question.user
                                       : iter_answer->user;
          assert_allowed(*iter_account, global_item_owner,
                         Action::POST_COMMENT);
          assert_comment_limit(*iter_account, global_item_owner,
                               question.comments);
          push_new_forum_item(iter_answer->comments, new_comment);
        }
      });
  update_rating(iter_account, POST_COMMENT_REWARD);
}

void peerania::delete_question(eosio::name user, uint64_t question_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::DELETE_QUESTION);
  eosio_assert(iter_question->answers.empty(),
               "You can't delete not empty question");
  question_table.erase(iter_question);
  eosio_assert(iter_question != question_table.end(),
               "Address not erased properly");
  update_rating(iter_account, DELETE_OWN_QUESTION_REWARD);
}

void peerania::delete_answer(eosio::name user, uint64_t question_id,
                             uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio_assert(iter_question->correct_answer_id != answer_id,
               "You can't delete this answer");
  question_table.modify(
      iter_question, _self, [iter_account, answer_id](auto &question) {
        auto iter_answer = find_answer(question, answer_id);
        assert_allowed(*iter_account, iter_answer->user, Action::DELETE_ANSWER);
        question.answers.erase(iter_answer);
      });
  update_rating(iter_account, DELETE_OWN_ANSWER_REWARD);
}

void peerania::delete_comment(eosio::name user, uint64_t question_id,
                              uint16_t answer_id, uint64_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, comment_id](auto &question) {
        if (apply_to_question(answer_id)) {
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

void peerania::modify_question(eosio::name user, uint64_t question_id,
                               const std::string &title,
                               const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  assert_title(title);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::MODIFY_QUESTION);
  question_table.modify(
      iter_question, _self, [&ipfs_link, &title](auto &question) {
        question.ipfs_link = ipfs_link;
        question.title = title;
        set_property(question.properties, PROPERTY_LAST_MODIFIED, now());
      });
}

void peerania::modify_answer(eosio::name user, uint64_t question_id,
                             uint16_t answer_id, const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, &ipfs_link](auto &question) {
        auto iter_answer = find_answer(question, answer_id);
        assert_allowed(*iter_account, iter_answer->user, Action::MODIFY_ANSWER);
        iter_answer->ipfs_link = ipfs_link;
        set_property(iter_answer->properties, PROPERTY_LAST_MODIFIED, now());
      });
}

void peerania::modify_comment(eosio::name user, uint64_t question_id,
                              uint16_t answer_id, uint16_t comment_id,
                              const std::string &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, comment_id, &ipfs_link](auto &question) {
        if (apply_to_question(answer_id)) {
          auto iter_comment = find_comment(question, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::MODIFY_COMMENT);
          iter_comment->ipfs_link = ipfs_link;
          set_property(iter_comment->properties, PROPERTY_LAST_MODIFIED, now());
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::MODIFY_COMMENT);
          iter_comment->ipfs_link = ipfs_link;
          set_property(iter_comment->properties, PROPERTY_LAST_MODIFIED, now());
        }
      });
}

void peerania::mark_answer_as_correct(eosio::name user, uint64_t question_id,
                                      uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user,
                 Action::MARK_ANSWER_AS_CORRECT);
  if (answer_id != EMPTY_ANSWER_ID) {
    eosio_assert(iter_question->correct_answer_id != answer_id,
                 "This answer already marked as correct");
    auto iter_answer = binary_find(iter_question->answers.begin(),
                                   iter_question->answers.end(), answer_id);
    eosio_assert(iter_answer != iter_question->answers.end(),
                 "Answer not found");
    if (iter_question->correct_answer_id == EMPTY_ANSWER_ID) {
      // No one answer has not been marked as correct yet
      update_rating(iter_account, ACCEPT_ANSWER_AS_CORRECT_REWARD);
      update_rating(iter_answer->user, ANSWER_ACCEPTED_AS_CORRECT_REWARD);
    } else {
      // One of answers is marked as correct. Find this one,
      // pick up the reward of past owner and give it to new
      auto iter_old_answer = binary_find(iter_question->answers.begin(),
                                         iter_question->answers.end(),
                                         iter_question->correct_answer_id);
      // check internal error iter_old_answer
      update_rating(iter_old_answer->user, -ANSWER_ACCEPTED_AS_CORRECT_REWARD);
      update_rating(iter_answer->user, ANSWER_ACCEPTED_AS_CORRECT_REWARD);
    }
  } else {
    // Set question to "without answer"
    eosio_assert(
        iter_question->correct_answer_id != EMPTY_ANSWER_ID,
        "You can\'t reset correct answer for question without correct answer");
    auto iter_old_answer = binary_find(iter_question->answers.begin(),
                                       iter_question->answers.end(),
                                       iter_question->correct_answer_id);
    // pick up reward
    // check internal error iter_old_answer
    update_rating(iter_account, -ACCEPT_ANSWER_AS_CORRECT_REWARD);
    update_rating(iter_old_answer->user, -ANSWER_ACCEPTED_AS_CORRECT_REWARD);
  }

  question_table.modify(iter_question, _self, [answer_id](auto &question) {
    question.correct_answer_id = answer_id;
  });
}
