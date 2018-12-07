#include <eosiolib/name.hpp>
#include <vector>
#include "history.hpp"
#include "account.hpp"
#include "utils.hpp"

template <typename T, typename T_iter_acc>
void upvote_item(T &item, T_iter_acc iter_account, eosio::name &item_owner,
                 int8_t &owner_rating_change, int8_t &caller_rating_change,
                 const int8_t upvote_cost_owner,
                 const int8_t upvote_cost_caller,
                 const int8_t downvote_cost_owner,
                 const int8_t downvote_cost_caller) {
  item_owner = item.user;
  assert_allowed(*iter_account, item_owner, Action::UPVOTE);
  bool is_new;
  auto itr_history =
      get_history_item_iter(item.history, iter_account->owner, is_new);
  if (is_new) {
    /*The user isn't do any actions with item
    (i.e. the user isn't in history) add user to history,
    with mark {upvote}*/
    itr_history->set_flag(HISTORY_UPVOTED_FLG);
    item.rating += 1;
    caller_rating_change += upvote_cost_caller;
    owner_rating_change += upvote_cost_owner;
  } else {
    eosio_assert(!(itr_history->is_flag_set(HISTORY_DELETE_VOTED_FLG)), "You couldn't upvote reported item");
    if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
      /*The item was upvoted by user, but user call
      upvote again, this action remove upvote(now
      user has no upvote/dovnvote effect to item)*/
      item.rating -= 1;
      itr_history->remove_flag(HISTORY_UPVOTED_FLG);
      caller_rating_change -= upvote_cost_caller;
      owner_rating_change -= upvote_cost_owner;
    } else {
      if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
        /*The item was downvoted by user, but after user
        call upvote, this action equal to
        {remove downvote} + {upvote}*/
        item.rating += 2;
        itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
        caller_rating_change += upvote_cost_caller - downvote_cost_caller;
        owner_rating_change += upvote_cost_owner - downvote_cost_owner;
      } else {
        // There was item in history but it is not ralated
        // to upvoting / downvoting(simple upvote)
        item.rating += 1;
        caller_rating_change += upvote_cost_caller;
        owner_rating_change += upvote_cost_owner;
      }
      itr_history->set_flag(HISTORY_UPVOTED_FLG);
    }
    // If the history item does not carry any information, delete it
    if (itr_history->is_empty()) item.history.erase(itr_history);
  }
}

template <typename T, typename T_iter_acc>
void downvote_item(T &item, T_iter_acc iter_account, eosio::name &item_owner,
                   int8_t &owner_rating_change, int8_t &caller_rating_change,
                   const int8_t upvote_cost_owner,
                   const int8_t upvote_cost_caller,
                   const int8_t downvote_cost_owner,
                   const int8_t downvote_cost_caller) {
  item_owner = item.user;
  assert_allowed(*iter_account, item_owner, Action::DOWNVOTE);
  bool is_new;
  auto itr_history =
      get_history_item_iter(item.history, iter_account->owner, is_new);
  if (is_new) {
    /*The user isn't do any actions with item
    (i.e. the user isn't in history) add user to history
    with mark {downvote}*/
    itr_history->set_flag(HISTORY_DOWNVOTED_FLG);
    item.rating -= 1;
    caller_rating_change += downvote_cost_caller;
    owner_rating_change += downvote_cost_owner;
  } else {
    if (itr_history->is_flag_set(HISTORY_DOWNVOTED_FLG)) {
      /*The item was downvoted by user, but user call
      downvote again, this action remove downvote(now
      user has no upvote/dovnvote effect to item)*/
      item.rating += 1;
      itr_history->remove_flag(HISTORY_DOWNVOTED_FLG);
      caller_rating_change -= downvote_cost_caller;
      owner_rating_change -= downvote_cost_owner;
    } else {
      if (itr_history->is_flag_set(HISTORY_UPVOTED_FLG)) {
        /*The item was upvoted by user, but after user
        call downvote, this action equal to
        {remove upvote} + {downvote}*/
        item.rating -= 2;
        itr_history->remove_flag(HISTORY_UPVOTED_FLG);
        caller_rating_change += downvote_cost_caller - upvote_cost_caller;
        owner_rating_change += downvote_cost_owner - upvote_cost_owner;
      } else {
        // There was item in history but it is not ralated
        // to upvoting / downvoting (simple downwote)
        item.rating -= 1;
        caller_rating_change += downvote_cost_caller;
        owner_rating_change += downvote_cost_owner;
      }
      itr_history->set_flag(HISTORY_DOWNVOTED_FLG);
    }
    // If the history item does not carry any information, delete it
    if (itr_history->is_empty()) item.history.erase(itr_history);
  }
}

// Help function check history
template <typename T>
bool set_deletion_votes_and_history(T &item, const account &user, uint16_t limit) {
  // Do not allow vote for deletion your own item
  assert_allowed(user, item.user, Action::VOTE_FOR_DELETION);
  bool is_new;
  auto itr_history =
      get_history_item_iter(item.history, user.owner, is_new);
  if (is_new) {
    itr_history->set_flag(HISTORY_DELETE_VOTED_FLG);
  } else {
    eosio_assert(!(itr_history->is_flag_set(HISTORY_UPVOTED_FLG)), "Can't report upvoted item");
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

// return number of upvotes
int upvote_count(const std::vector<history_item> &history) {
  int upvote_count = 0;
  std::for_each(history.begin(), history.end(), [&upvote_count](auto hst) {
    if (hst.is_flag_set(HISTORY_UPVOTED_FLG)) upvote_count += 1;
  });
  return upvote_count;
}