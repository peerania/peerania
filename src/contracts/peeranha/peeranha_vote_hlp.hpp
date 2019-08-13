#include <eosio/name.hpp>
#include <vector>
#include "account.hpp"
#include "history.hpp"
#include "utils.hpp"

template <typename T, typename T_iter_acc>
void upvote_item(T &item, T_iter_acc iter_account, int8_t &energy,
                 int8_t &caller_rating, int8_t &target_user_rating,
                 VoteItem::vote_resources_t item_type) {
  assert_allowed(*iter_account, item.user, Action::UPVOTE);
  bool is_new;
  auto itr_history =
      get_history_item_iter(item.history, iter_account->user, is_new);
  if (is_new) {
    /*The user isn't do any actions with item
    (i.e. the user isn't in history) add user to history,
    with mark {upvote}*/
    itr_history->set_flag(HISTORY_UPVOTED_FLG);
    item.rating += 1;
    caller_rating = item_type.upvote_reward;
    target_user_rating = item_type.upvoted_reward;
    energy = item_type.energy_upvote;
  } else {
    eosio::check(!(itr_history->is_flag_set(HISTORY_DELETE_VOTED_FLG)),
                 "You couldn't upvote reported item");
    if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
      /*The item was upvoted by user, but user call
      upvote again, this action remove upvote(now
      user has no upvote/dovnvote effect to item)*/
      item.rating -= 1;
      itr_history->remove_flag(HISTORY_UPVOTED_FLG);
      caller_rating = -item_type.upvote_reward;
      target_user_rating = -item_type.upvoted_reward;
      energy = ENERGY_FORUM_VOTE_CHANGE;
    } else {
      if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
        /*The item was downvoted by user, but after user
        call upvote, this action equal to
        {remove downvote} + {upvote}*/
        item.rating += 2;
        itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
        caller_rating = item_type.upvote_reward - item_type.downvote_reward;
        target_user_rating =
            item_type.upvoted_reward - item_type.downvoted_reward;
        energy = ENERGY_FORUM_VOTE_CHANGE;
      } else {
        // There was item in history but it is not ralated
        // to upvoting / downvoting(simple upvote)
        item.rating += 1;
        caller_rating = item_type.upvote_reward;
        target_user_rating = item_type.upvoted_reward;
        energy = item_type.energy_upvote;
      }
      itr_history->set_flag(HISTORY_UPVOTED_FLG);
    }
    // If the history item does not carry any information, delete it
    if (itr_history->is_empty()) item.history.erase(itr_history);
  }
}

template <typename T, typename T_iter_acc>
void downvote_item(T &item, T_iter_acc iter_account, int8_t &energy,
                   int8_t &caller_rating, int8_t &target_user_rating,
                   VoteItem::vote_resources_t item_type) {
  assert_allowed(*iter_account, item.user, Action::DOWNVOTE);
  bool is_new;
  auto itr_history =
      get_history_item_iter(item.history, iter_account->user, is_new);
  if (is_new) {
    /*The user isn't do any actions with item
    (i.e. the user isn't in history) add user to history
    with mark {downvote}*/
    itr_history->set_flag(HISTORY_DOWNVOTED_FLG);
    item.rating -= 1;
    caller_rating += item_type.downvote_reward;
    target_user_rating += item_type.downvoted_reward;
    energy = item_type.energy_downvote;
  } else {
    if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
      /*The item was downvoted by user, but user call
      downvote again, this action remove downvote(now
      user has no upvote/dovnvote effect to item)*/
      itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
      item.rating += 1;
      caller_rating -= item_type.downvote_reward;
      target_user_rating -= item_type.downvoted_reward;
      energy = ENERGY_FORUM_VOTE_CHANGE;
    } else {
      if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
        /*The item was upvoted by user, but after user
        call downvote, this action equal to
        {remove upvote} + {downvote}*/
        item.rating -= 2;
        itr_history->remove_flag(HISTORY_UPVOTED_FLG);
        caller_rating += item_type.downvote_reward;
        target_user_rating += item_type.downvoted_reward - item_type.upvoted_reward;
        energy = item_type.energy_downvote;
      } else {
        // There was item in history but it is not ralated
        // to upvoting / downvoting (simple downwote)
        item.rating -= 1;
        caller_rating += item_type.downvote_reward;
        target_user_rating += item_type.downvoted_reward;
        energy = item_type.energy_downvote;
      }
      itr_history->set_flag(HISTORY_DOWNVOTED_FLG);
    }
    // If the history item does not carry any information, delete it
    if (itr_history->is_empty()) item.history.erase(itr_history);
  }
}

// Help function check history
template <typename T>
bool set_deletion_votes_and_history(T &item, const account &user,
                                    uint16_t limit) {
  // Do not allow vote for deletion your own item
  assert_allowed(user, item.user, Action::VOTE_FOR_DELETION);
  bool is_new;
  auto itr_history = get_history_item_iter(item.history, user.user, is_new);
  if (is_new) {
    itr_history->set_flag(HISTORY_DELETE_VOTED_FLG);
  } else {
    eosio::check(!(itr_history->is_flag_set(HISTORY_UPVOTED_FLG)),
                 "Can't report upvoted item");
    eosio::check(!(itr_history->is_flag_set(HISTORY_DELETE_VOTED_FLG)),
                 "Already voted for deletion!");
    itr_history->set_flag(HISTORY_DELETE_VOTED_FLG);
  }
  int current_question_report_points =
      get_property_d(item.properties, PROPERTY_REPORT_POINTS, 0);
  int snitch_report_points = status_moderation_impact(user.rating);
  if (current_question_report_points + snitch_report_points > limit) return true;
  set_property_d(item.properties, PROPERTY_REPORT_POINTS,
                 current_question_report_points + snitch_report_points, 0);
  return false;
}

// return number of upvotes
int upvote_count(const std::vector<history_item> &history) {
  int upvote_count = 0;
  std::for_each(history.begin(), history.end(), [&upvote_count](auto hst) {
    if (hst.is_flag_set(HISTORY_UPVOTED_FLG)) upvote_count += 1;
  });
  return upvote_count;
}