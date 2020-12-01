#include "peeranha.hpp"
#include "account_achievements.hpp"
#include <stdint.h>
#include "property.hpp"

void peeranha::update_achievement(eosio::name user, Group_achievement group, int value) {
  account_achievements_index account_achievements_table(_self, user.value );

  for (const auto& buf_achievement : achievements) {
    auto iter_account_achievements = account_achievements_table.find(buf_achievement.first);
    if (buf_achievement.second.group == group && iter_account_achievements == account_achievements_table.end()) {
      auto lower_bound = value >= buf_achievement.second.lower_bound;
      if (lower_bound && increment_achievement_count(buf_achievement.first)) {
        account_achievements_table.emplace(_self, [&](auto &account) {
          account.user = user;
          account.achievements_id = buf_achievement.first;
          account.date = now();
        });
      }
    }
  }
}

void peeranha::init_users_achievements() {
  account_index account_table(_self, scope_all_accounts);
  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    update_achievement(iter_account->user, REGISTERED, 1);
    update_achievement(iter_account->user, QUESTION, iter_account->questions_asked);
    update_achievement(iter_account->user, ANSWER, iter_account->answers_given);
    update_achievement(iter_account->user, CORRECT_ANSWER, iter_account->correct_answers);
    update_achievement(iter_account->user, RATING, iter_account->rating);       
  }
}