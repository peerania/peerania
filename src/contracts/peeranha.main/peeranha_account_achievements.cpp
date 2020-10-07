#include "peeranha.hpp"
#include "account_achievements.hpp"
#include <stdint.h>
#include "property.hpp"

void peeranha::update_achievement(eosio::name user, uint32_t id_achievement, uint64_t value, bool new_value) {
  account_achievements_index account_achievements_table(_self, user.value );
  
  auto iter_account_achievements = account_achievements_table.find(id_achievement);

  if (iter_account_achievements == account_achievements_table.end()) {
    if(add_achievement_amount(id_achievement)) {
      account_achievements_table.emplace(_self, 
          [&](auto &account) {
            account.user = user;
            account.achievements_id = id_achievement;
            account.value = value;
            account.date = now();
          });
    }
  } else {
    account_achievements_table.modify(iter_account_achievements, _self,
          [&](auto &account) {
            if (new_value)
              account.value = value;
            else
              account.value += value;
          });
  } 
}


void peeranha::update_account_achievement(eosio::name user, uint32_t achievement_id) {
  switch (achievement_id) {
    case QUESTION_ASKED:
      update_question_achievement(user);
      break;
    case ANSWER_GIVEN:
      update_answer_achievement(user);
      break;
    case CORRECT_ANSWER:
      update_correct_achievement(user);
      break;
    case FIRST_10K_REGISTERED:
      achievements_first_10k_registered_users(user);
      break;
  }
}

void peeranha::update_question_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, QUESTION_ASKED, iter_account->questions_asked, true);
}

void peeranha::update_answer_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, ANSWER_GIVEN, iter_account->answers_given, true);
}

void peeranha::update_correct_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, CORRECT_ANSWER, iter_account->correct_answers, true);
}

void peeranha::update_achievement_rating(eosio::name user) {
  account_index account_table(_self, scope_all_accounts);
  auto iter_account = account_table.find(user.value);
  if(iter_account == account_table.end()) { return; }
  int rating_account = iter_account->rating;

  if(rating_account < 0 ) { return; }
  else if (rating_account >= RATING_STRANGER && rating_account < RATING_NEWBIE) { update_achievement(user, STRANGER, 1, true); }  
  else if (rating_account >= RATING_NEWBIE && rating_account < RATING_JUNIOR)   { update_achievement(user, NEWBIE, 1, true); }
  else if (rating_account >= RATING_JUNIOR && rating_account < RATING_RESIDENT) { update_achievement(user, JUNIOR, 1, true); }  
  else if (rating_account >= RATING_RESIDENT && rating_account < RATING_SENIOR) { update_achievement(user, RESIDENT, 1, true); }  
  else if (rating_account >= RATING_SENIOR && rating_account < RATING_HERO)     { update_achievement(user, SENIOR, 1, true); }  
  else if (rating_account >= RATING_HERO && rating_account < RATING_SUPERHERO)  { update_achievement(user, HERO, 1, true); }  
  else if (rating_account >= RATING_SUPERHERO) { update_achievement(user, SUPERHERO, 1, true); }  
}

void peeranha::achievements_first_10k_registered_users(eosio::name user) {
  update_achievement(user, FIRST_10K_REGISTERED, 1, true);       
}

void peeranha::init_all_accounts_achievements() {
  account_index account_table(_self, scope_all_accounts);

  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    update_account_achievement(iter_account->user, QUESTION_ASKED);
    update_account_achievement(iter_account->user, ANSWER_GIVEN);
    update_account_achievement(iter_account->user, CORRECT_ANSWER);
  }
}

void peeranha::init_achievements_first_10k_registered_users() {
  account_index account_table(_self, scope_all_accounts);
  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    update_achievement(iter_account->user, FIRST_10K_REGISTERED, 1, true);       
  }
}

void peeranha::init_achievements_rating() {
  account_index account_table(_self, scope_all_accounts);
  auto iter_account = account_table.begin();
  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    int rating_account = iter_account->rating;
    if (rating_account < 0) { continue; }
    if (rating_account >= RATING_STRANGER) { update_achievement(iter_account->user, STRANGER, 1, true); }  else { continue; }
    if (rating_account >= RATING_NEWBIE) { update_achievement(iter_account->user, NEWBIE, 1, true); }      else { continue; }
    if (rating_account >= RATING_JUNIOR) { update_achievement(iter_account->user, JUNIOR, 1, true); }      else { continue; } 
    if (rating_account >= RATING_RESIDENT) { update_achievement(iter_account->user, RESIDENT, 1, true); }  else { continue; }  
    if (rating_account >= RATING_SENIOR) { update_achievement(iter_account->user, SENIOR, 1, true); }      else { continue; } 
    if (rating_account >= RATING_HERO) { update_achievement(iter_account->user, HERO, 1, true); }          else { continue; }
    if (rating_account >= RATING_SUPERHERO) { update_achievement(iter_account->user, SUPERHERO, 1, true); }else { continue; }
  }
}