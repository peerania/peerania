#include "peeranha.hpp"
#include "account_achievements.hpp"
#include <stdint.h>
#include "property.hpp"

void peeranha::update_achievement(eosio::name user, Achievements id_achievement, uint64_t value) {
  account_achievements_index account_achievements_table(_self, scope_all_account_achievements);
  auto iter_account_achievements = account_achievements_table.find(user.value);

  if (iter_account_achievements == account_achievements_table.end()) {
      account_achievements_table.emplace(_self, 
          [&](auto &account) {
            account.user = user;
            set_property_achieve(account.user_achievements, id_achievement, value);
          });
  } else {
    account_achievements_table.modify(iter_account_achievements, _self,
          [&](auto &account) {
            set_property_achieve(account.user_achievements, id_achievement, value);
          });
  } 
}

void peeranha::set_property_achieve(std::vector<user_achievement> &properties, uint8_t key,
                  const uint64_t value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);

  if (itr_property == properties.end()) {
    user_achievement key_value;
    key_value.achievements_id = key;
    key_value.value = value;
    key_value.date = now();

    if(up_achievement(key))
      properties.push_back(key_value);
  } else {
    itr_property->value = value;
  }
}

void peeranha::update_account_achievement(eosio::name user, uint32_t achievement_id) {
  account_achievements_index account_achievements_table(_self, scope_all_account_achievements);

  auto iter_account = find_account(user);

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
  update_achievement(user, QUESTION_ASKED, iter_account->questions_asked);
}

void peeranha::update_answer_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, ANSWER_GIVEN, iter_account->answers_given);
}

void peeranha::update_correct_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, CORRECT_ANSWER, iter_account->correct_answers);
}

void peeranha::update_achievement_rating(eosio::name user) {
  account_index account_table(_self, scope_all_accounts);
  auto iter_account = account_table.find(user.value);
  if(iter_account == account_table.end()) { return; }
  int rating_account = iter_account->rating;

  if(rating_account < 0 ) { return; }
  else if (rating_account >= RATING_STRANGER && rating_account < RATING_NEWBIE) { update_achievement(user, STRANGER, 1); }  
  else if (rating_account >= RATING_NEWBIE && rating_account < RATING_JUNIOR)   { update_achievement(user, NEWBIE, 1); }
  else if (rating_account >= RATING_JUNIOR && rating_account < RATING_RESIDENT) { update_achievement(user, JUNIOR, 1); }  
  else if (rating_account >= RATING_RESIDENT && rating_account < RATING_SENIOR) { update_achievement(user, RESIDENT, 1); }  
  else if (rating_account >= RATING_SENIOR && rating_account < RATING_HERO)     { update_achievement(user, SENIOR, 1); }  
  else if (rating_account >= RATING_HERO && rating_account < RATING_SUPERHERO)  { update_achievement(user, HERO, 1); }  
  else if (rating_account >= RATING_SUPERHERO) { update_achievement(user, SUPERHERO, 1); }  
}

void peeranha::achievements_first_10k_registered_users(eosio::name user) {
  update_achievement(user, FIRST_10K_REGISTERED, 1);       
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
    update_achievement(iter_account->user, FIRST_10K_REGISTERED, 1);       
  }
}

void peeranha::init_achievements_rating() {
  account_index account_table(_self, scope_all_accounts);
  auto iter_account = account_table.begin();
  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    int rating_account = iter_account->rating;
    if (rating_account < 0) { continue; }
    if (rating_account >= RATING_STRANGER) { update_achievement(iter_account->user, STRANGER, 1); }  else { continue; }
    if (rating_account >= RATING_NEWBIE) { update_achievement(iter_account->user, NEWBIE, 1); }      else { continue; }
    if (rating_account >= RATING_JUNIOR) { update_achievement(iter_account->user, JUNIOR, 1); }      else { continue; } 
    if (rating_account >= RATING_RESIDENT) { update_achievement(iter_account->user, RESIDENT, 1); }  else { continue; }  
    if (rating_account >= RATING_SENIOR) { update_achievement(iter_account->user, SENIOR, 1); }      else { continue; } 
    if (rating_account >= RATING_HERO) { update_achievement(iter_account->user, HERO, 1); }          else { continue; }
    if (rating_account >= RATING_SUPERHERO) { update_achievement(iter_account->user, SUPERHERO, 1); }else { continue; }
  }
}