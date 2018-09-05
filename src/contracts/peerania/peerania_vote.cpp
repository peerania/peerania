#include "peerania.hpp"

namespace eosio {

template <typename T, typename T_iter_acc>
void upvote_for_item(T &item, T_iter_acc iter_account, account_name &item_owner,
                     int8_t &owner_rating_change, int8_t &caller_rating_change,
                     const int8_t upvote_cost_owner,
                     const int8_t upvote_cost_caller,
                     const int8_t downvote_cost_owner,
                     const int8_t downvote_cost_caller) {
  item_owner = item.user;
  assert_allowed(*iter_account, item_owner, Action::UPVOTE);
  auto itr_history = linear_find(item.history.begin(), item.history.end(),
                                 iter_account->owner);
  if (itr_history == item.history.end()) {
    history_item hst_item;
    hst_item.user = iter_account->owner;
    hst_item.set_flag(HISTORY_UPVOTED_FLG);
    item.rating += 1;
    item.history.push_back(hst_item);
    caller_rating_change += upvote_cost_caller;
    owner_rating_change += upvote_cost_owner;
  } else {
    if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
      item.rating -= 1;
      itr_history->remove_flag(HISTORY_UPVOTED_FLG);
      caller_rating_change -= upvote_cost_caller;
      owner_rating_change -= upvote_cost_owner;
    } else {
      if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
        item.rating += 2;
        itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
        caller_rating_change += upvote_cost_caller - downvote_cost_caller;
        owner_rating_change += upvote_cost_owner - downvote_cost_owner;
      } else {
        item.rating += 1;
        caller_rating_change += upvote_cost_caller;
        owner_rating_change += upvote_cost_owner;
      }
      itr_history->set_flag(HISTORY_UPVOTED_FLG);
    }
    if (itr_history->is_empty()) item.history.erase(itr_history);
  }
}

template <typename T, typename T_iter_acc>
void downvote_for_item(T &item, T_iter_acc iter_account, account_name &item_owner,
                       int8_t &owner_rating_change,
                       int8_t &caller_rating_change,
                       const int8_t upvote_cost_owner,
                       const int8_t upvote_cost_caller,
                       const int8_t downvote_cost_owner,
                       const int8_t downvote_cost_caller) {
  item_owner = item.user;
  assert_allowed(*iter_account, item_owner, Action::UPVOTE);
  auto itr_history = linear_find(item.history.begin(), item.history.end(),
                                 iter_account->owner);
  if (itr_history == item.history.end()) {
    history_item hst_item;
    hst_item.user = iter_account->owner;
    hst_item.set_flag(HISTORY_DOWNVOTED_FLG);
    item.rating -= 1;
    item.history.push_back(hst_item);
    caller_rating_change += downvote_cost_caller;
    owner_rating_change += downvote_cost_owner;
  } else {
    if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
      item.rating += 1;
      itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
      caller_rating_change -= downvote_cost_caller;
      owner_rating_change -= downvote_cost_owner;
    } else {
      if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
        item.rating -= 2;
        itr_history->remove_flag(HISTORY_UPVOTED_FLG);
        caller_rating_change += downvote_cost_caller - upvote_cost_caller;
        owner_rating_change += downvote_cost_owner - upvote_cost_owner;
      } else {
        item.rating -= 1;
        caller_rating_change += downvote_cost_caller;
        owner_rating_change += downvote_cost_owner;
      }
      itr_history->set_flag(HISTORY_DOWNVOTED_FLG);
    }

    if (itr_history->is_empty()) item.history.erase(itr_history);
  }
}

void peerania::vote(account_name user, uint64_t question_id, uint16_t answer_id,
                    bool is_upvote) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  account_name item_owner;
  int8_t owner_rating_change;
  int8_t caller_rating_change;
  question_table.modify(
      iter_question, _self,
      [answer_id, is_upvote, iter_account, &item_owner, &owner_rating_change,
       &caller_rating_change](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          if (is_upvote) {
            upvote_for_item(question, iter_account, item_owner, owner_rating_change,
                            caller_rating_change, QUESTION_UPVOTED_REWARD,
                            UPVOTE_QUESTION_REWARD, QUESTION_DOWNVOTED_REWARD,
                            DOWNVOTE_QUESTION_REWARD);
          } else
            downvote_for_item(question, iter_account, item_owner, owner_rating_change,
                              caller_rating_change, QUESTION_UPVOTED_REWARD,
                              UPVOTE_QUESTION_REWARD, QUESTION_DOWNVOTED_REWARD,
                              DOWNVOTE_QUESTION_REWARD);
        } else {
          auto itr_answer = find_answer(question, answer_id);
          if (is_upvote)
            upvote_for_item(*itr_answer, iter_account, item_owner, owner_rating_change,
                            caller_rating_change, ANSWER_UPVOTED_REWARD,
                            UPVOTE_ANSWER_REWARD, ANSWER_DOWNVOTED_REWARD,
                            DOWNVOTE_ANSWER_REWARD);
          else
            downvote_for_item(*itr_answer, iter_account, item_owner,
                              owner_rating_change, caller_rating_change,
                              ANSWER_UPVOTED_REWARD, UPVOTE_ANSWER_REWARD,
                              ANSWER_DOWNVOTED_REWARD, DOWNVOTE_ANSWER_REWARD);
        }
      });
  update_rating(iter_account, caller_rating_change);
  update_rating(item_owner, owner_rating_change);
}

// Help function check history
template <typename T>
bool vote_for_delete_history(T &item, const account &user, uint16_t limit) {
  // Do not allow vote for deletion your own item
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

int upvote_count(const vector<history_item> &history) {
  int upvote_count = 0;
  std::for_each(history.begin(), history.end(), [&upvote_count](auto hst) {
    if (hst.is_flag_set(HISTORY_UPVOTED_FLG)) upvote_count += 1;
  });
  return upvote_count;
}

void peerania::vote_for_deletion(account_name user, uint64_t question_id,
                                 uint16_t answer_id, uint16_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio_assert(iter_account->moderation_points > 0,
               "Not enought moderation points");

  int owner_rating_change = 0;
  // Remember old correct_answer_id to detect correct answer_deletion
  uint16_t old_correct_answer_id = iter_question->correct_answer_id;
  account_name item_owner;
  // If this flag == true the question will erased
  bool bad_question = false;
  question_table.modify(
      iter_question, _self,
      [&iter_account, answer_id, comment_id, &bad_question,
       &owner_rating_change, &item_owner](auto &question) {
        if (answer_id == APPLY_TO_QUESTION) {
          if (comment_id == APPLY_TO_ANSWER) {
            // Delete question
            // Question could not be deleted inside modify lambda
            // vote_for_delete_history - modify question
            bad_question = vote_for_delete_history(question, *iter_account,
                                                   DELETION_VOTES_QUESTION);
            if (bad_question) {
              item_owner = question.user;
              owner_rating_change -=
                  upvote_count(question.history) * QUESTION_UPVOTED_REWARD;
              owner_rating_change += QUESTION_DELETED_REWARD;
            }
          } else {
            // Delete comment to question by vote (answer_id == 0)
            auto iter_comment = find_comment(question, comment_id);

            if (vote_for_delete_history(*iter_comment, *iter_account,
                                        DELETION_VOTES_COMMENT)) {
              item_owner = iter_comment->user;
              owner_rating_change += COMMENT_DELETED_REWARD;
              question.comments.erase(iter_comment);
            }
          }
          return;
        }
        auto iter_answer = find_answer(question, answer_id);
        if (comment_id == APPLY_TO_ANSWER) {
          // Delete answer to question by vote (comment_id == 0)
          if (vote_for_delete_history(*iter_answer, *iter_account,
                                      DELETION_VOTES_ANSWER)) {
            // Get for mar as correct
            item_owner = iter_answer->user;
            if (question.correct_answer_id == iter_answer->id) {
              owner_rating_change -= ANSWER_ACCEPTED_AS_CORRECT_REWARD;
              question.correct_answer_id = APPLY_TO_QUESTION;
            }
            owner_rating_change -=
                upvote_count(iter_answer->history) * ANSWER_UPVOTED_REWARD;
            owner_rating_change += ANSWER_DELETED_REWARD;
            question.answers.erase(iter_answer);
          }
        } else {
          // Delete comment to answer
          auto iter_comment = find_comment(*iter_answer, comment_id);
          if (vote_for_delete_history(*iter_comment, *iter_account,
                                      DELETION_VOTES_COMMENT)) {
            item_owner = iter_comment->user;
            owner_rating_change += COMMENT_DELETED_REWARD;
            iter_answer->comments.erase(iter_comment);
          }
        }
      });

  // Means that answer, marked as correct was deleted
  if (iter_question->correct_answer_id != old_correct_answer_id) {
    update_rating(iter_question->user, -ACCEPT_ANSWER_AS_CORRECT_REWARD);
  }

  if (bad_question) {
    if (iter_question->correct_answer_id != APPLY_TO_QUESTION)
      owner_rating_change -= ACCEPT_ANSWER_AS_CORRECT_REWARD;
    for (auto answer = iter_question->answers.begin();
         answer != iter_question->answers.end(); answer++) {
      int rating_change = 0;
      rating_change -= upvote_count(answer->history) * ANSWER_UPVOTED_REWARD;
      if (answer->id == iter_question->correct_answer_id)
        rating_change -= ANSWER_ACCEPTED_AS_CORRECT_REWARD;
      update_rating(answer->user, rating_change);
    }
    question_table.erase(iter_question);
    eosio_assert(iter_question != question_table.end(),
                 "Address not erased properly");
  }
  update_rating(item_owner, owner_rating_change);
  account_table.modify(iter_account, _self,
                       [](auto &account) { account.moderation_points -= 1; });
}

}  // namespace eosio