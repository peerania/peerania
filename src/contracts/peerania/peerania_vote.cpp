#include "peerania.hpp"

namespace eosio {

// Split into upvote_for_item / downvote_for_item??
template <typename T>
void vote_for_item(T &item, account_name user, bool is_upvote) {
  auto itr_history =
      linear_find(item.history.begin(), item.history.end(), user);
  if (itr_history == item.history.end()) {
    history_item hst_item;
    hst_item.user = user;
    if (is_upvote) {
      hst_item.set_flag(HISTORY_UPVOTED_FLG);
      item.rating += 1;
    } else {
      hst_item.set_flag(HISTORY_DOWNVOTED_FLG);
      item.rating -= 1;
    }
    item.history.push_back(hst_item);
  } else {
    if (is_upvote) {
      if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
        item.rating -= 1;
        itr_history->remove_flag(HISTORY_UPVOTED_FLG);
      } else {
        if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
          item.rating += 2;
          itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
        } else
          item.rating += 1;
        itr_history->set_flag(HISTORY_UPVOTED_FLG);
      }
    } else {
      if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
        item.rating += 1;
        itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
      } else {
        if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
          item.rating -= 2;
          itr_history->remove_flag(HISTORY_UPVOTED_FLG);
        } else
          item.rating -= 1;
        itr_history->set_flag(HISTORY_DOWNVOTED_FLG);
      }
    }
  }
}

void peerania::vote(account_name user, uint64_t question_id, uint16_t answer_id,
                    bool is_upvote) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, Action::VOTE);
  question_table.modify(iter_question, _self,
                        [answer_id, is_upvote, user](auto &question) {
                          if (answer_id == APPLY_TO_QUESTION) {
                            vote_for_item(question, user, is_upvote);
                          } else {
                            auto itr_answer = find_answer(question, answer_id);
                            vote_for_item(*itr_answer, user, is_upvote);
                          }
                        });
}

// Help function check history
template <typename T>
bool vote_for_delete_history(T &item, const account &user, uint16_t limit) {
  //Do not allow vote for deletion your own item
  assert_allowed(user, item.user, Action::VOTE_FOR_DELETION);
  auto itr_history =
      linear_find(item.history.begin(), item.history.end(), user.owner);
  if (itr_history == item.history.end()) {
    history_item hst_item;
    hst_item.user = user.owner;
    hst_item.set_flag(HISTORY_DELETE_VOTED_FLG);
    item.history.push_back(hst_item);
  } else {
    eosio_assert(!(itr_history->is_flag_set(HISTORY_DELETE_VOTED_FLG)),
                 "Already voted for deletion!");
    itr_history->set_flag(HISTORY_DELETE_VOTED_FLG);
  }
  int deletion_votes =
      get_property_d(item.properties, PROPERTY_DELETION_VOTES, 0);
  if (deletion_votes + user.rating > limit) return true;
  set_property_d(item.properties, PROPERTY_DELETION_VOTES,
                 deletion_votes + user.rating, 0);
  return false;
}

void peerania::vote_for_deletion(account_name user, uint64_t question_id,
                                 uint16_t answer_id, uint16_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio_assert(iter_account->moderation_points > 0,
               "Not enought moderation points");
  
  // If this flag == true the question will erased
  bool bad_question = false;
  question_table.modify(
      iter_question, _self,
      [&iter_account, answer_id, comment_id, &bad_question](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          if (comment_id == APPLY_TO_ANSWER) {
            // Delete question
            // Question could not be deleted inside modify lambda
            // vote_for_delete_history - modify question
            bad_question = vote_for_delete_history(question, *iter_account,
                                                   DELETION_VOTES_QUESTION);
          } else {
            // Delete comment to question by vote (answer_id == 0)
            auto iter_comment = find_comment(question, comment_id);
            if (vote_for_delete_history(*iter_comment, *iter_account,
                                        DELETION_VOTES_COMMENT))
              question.comments.erase(iter_comment);
          }
          return;
        }
        auto iter_answer = find_answer(question, answer_id);
        if (comment_id == APPLY_TO_ANSWER) {
          // Delete answer to question by vote (comment_id == 0)
          if (vote_for_delete_history(*iter_answer, *iter_account,
                                      DELETION_VOTES_ANSWER))
            question.answers.erase(iter_answer);
        } else {
          // Delete comment to answer
          auto iter_comment = find_comment(*iter_answer, comment_id);
          if (vote_for_delete_history(*iter_comment, *iter_account,
                                      DELETION_VOTES_COMMENT))
            iter_answer->comments.erase(iter_comment);
        }
      });
  if (bad_question) {
    question_table.erase(iter_question);
    eosio_assert(iter_question != question_table.end(),
                 "Address not erased properly");
  }
  account_table.modify(iter_account, _self,
                       [](auto &account) { account.moderation_points -= 1; });
}

}  // namespace eosio