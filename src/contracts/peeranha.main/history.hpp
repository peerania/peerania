#pragma once

#include <eosio/eosio.hpp>
#include <vector>
#include "utils.hpp"
// Flags
#define HISTORY_UPVOTED_FLG 1       // 0b0000000000000001
#define HISTORY_DOWNVOTED_FLG 2     // 0b0000000000000010
#define HISTORY_DELETE_VOTED_FLG 4  // 0b0000000000000100

/**
 * Bit description
 * |  15-3  |      2     |    1    |   0   |
 * |Reserved|DELETE_VOTED|DOWNVOTED|UPVOTED|
 */

typedef uint16_t flag_type;

struct history_item {
  eosio::name user;
  flag_type flag = 0;
  void set_flag(flag_type flg) { flag |= flg; }

  void remove_flag(flag_type flg) { flag &= ~flg; }

  bool is_flag_set(flag_type flg) const { return flag & flg; }

  bool is_empty() const { return flag == 0; }

  eosio::name lkey() const { return user; }
};

/*
If history contain the history item with passed user
return iterator to this history item(is_new = false) else
insert history item into history, return the iterator to
new element(is_new = true).
*/
std::vector<history_item>::iterator get_history_item_iter(
    std::vector<history_item> &history, eosio::name user, bool &is_new) {
  auto itr_history = linear_find(history.begin(), history.end(), user);
  if (itr_history == history.end()) {
    history_item hst_item;
    hst_item.user = user;
    history.push_back(hst_item);
    is_new = true;
    return (history.end() - 1);
  } else {
    is_new = false;
    return itr_history;
  }
}

// return number of upvotes
int upvote_count(const std::vector<history_item> &history) {
  int upvote_count = 0;
  std::for_each(history.begin(), history.end(), [&upvote_count](auto hst) {
    if (hst.is_flag_set(HISTORY_UPVOTED_FLG)) upvote_count += 1;
  });
  return upvote_count;
}