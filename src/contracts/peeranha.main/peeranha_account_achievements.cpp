#include "peeranha.hpp"
#include "account_achievements.hpp"
#include <stdint.h>
#include "property.hpp"

void peeranha::init_all_accounts_achievements() {
  account_index account_table(_self, scope_all_accounts);

  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    update_account_achievement(iter_account->user, questions_asked);
    update_account_achievement(iter_account->user, answers_given);
    update_account_achievement(iter_account->user, correct_answers);
  }
}

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

void peeranha::set_property_achieve(std::vector<key_account_achievements> &properties, uint8_t key,
                  const uint64_t value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);

  if (itr_property == properties.end()) {
    key_account_achievements key_value;
    key_value.achievements_id = key;
    key_value.value = value;
    key_value.date = now();

    if(up_achievement(key))
      properties.push_back(key_value);
  } else {
    itr_property->value = value;
  }
}

void peeranha::update_account_achievements(eosio::name user) {
  account_achievements_index account_achievements_index_table(_self, scope_all_account_achievements);
  auto iter_account_achievements = account_achievements_index_table.find(user.value);
  if(iter_account_achievements == account_achievements_index_table.end()) { return; }

  for(auto i : iter_account_achievements->user_achievements) {
    update_account_achievement(user, i.achievements_id);
  }
}

void peeranha::update_account_achievement(eosio::name user, uint32_t achievement_id) {
  account_achievements_index account_achievements_table(_self, scope_all_account_achievements);

  auto iter_account = find_account(user);

  switch (achievement_id) {
    case questions_asked:
      update_question_achievement(user);
      break;
    case answers_given:
      update_answer_achievement(user);
      break;
    case correct_answers:
      update_correct_achievement(user);
      break;
  }
}

void peeranha::update_question_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, questions_asked, iter_account->questions_asked);
}

void peeranha::update_answer_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, answers_given, iter_account->answers_given);
}

void peeranha::update_correct_achievement(eosio::name user) {
  auto iter_account = find_account(user);
  update_achievement(user, correct_answers, iter_account->correct_answers);
}

void peeranha::init_achievements_first_10k_registered_users() {
  account_index account_table(_self, scope_all_accounts);
  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    update_achievement(iter_account->user, first_10k_registered, 1);       
  }
}

void peeranha::achievements_first_10k_registered_users(eosio::name user) {
  update_achievement(user, first_10k_registered, 1);       
}

void peeranha::update_achievement_rating(eosio::name user) {
  account_index account_table(_self, scope_all_accounts);
  auto iter_account = account_table.find(user.value);
  if(iter_account == account_table.end()) { return; }
  int rating_account = iter_account->rating;

//   Stranger	0 ... 99
// Newbie	100 ... 499
// Junior	500-999
// Resident	1000 ... 2499
// Senior	2500 ... 4999
// Hero	5000 ... 9999
// Superhero	10000

  if(rating_account < 0 ) { return; }
  else if (rating_account >= LOW_STRANGER && rating_account <= HIGH_STRANGER) { update_achievement(user, stranger, 1); }  
  else if (rating_account >= LOW_NEWBIE && rating_account <= HIGH_NEWBIE)     { update_achievement(user, newbie, 1); }
  else if (rating_account >= LOW_JUNIOR && rating_account <= HIGH_JUNIOR)     { update_achievement(user, junior, 1); }  
  else if (rating_account >= LOW_RESIDENT && rating_account <= HIGH_RESIDENT) { update_achievement(user, resident, 1); }  
  else if (rating_account >= LOW_SENIOR && rating_account <= HIGH_SENIOR)     { update_achievement(user, senior, 1); }  
  else if (rating_account >= LOW_HERO && rating_account <= HIGH_HERO)         { update_achievement(user, hero, 1); }  
  else if (rating_account >= LOW_SUPERHERO) { update_achievement(user, superhero, 1); }  
}

void peeranha::init_achievements_rating() {

  account_index account_table(_self, scope_all_accounts);
  auto iter_account = account_table.begin();
  for (auto iter_account = account_table.begin(); iter_account != account_table.end(); ++iter_account) {
    int rating_account = iter_account->rating;
    if (rating_account < 0) { continue; }
    if (rating_account >= LOW_STRANGER) { update_achievement(iter_account->user, stranger, 1); }  else { continue; }
    if (rating_account >= LOW_NEWBIE) { update_achievement(iter_account->user, newbie, 1); }      else { continue; }
    if (rating_account >= LOW_JUNIOR) { update_achievement(iter_account->user, junior, 1); }      else { continue; } 
    if (rating_account >= LOW_RESIDENT) { update_achievement(iter_account->user, resident, 1); }  else { continue; }  
    if (rating_account >= LOW_SENIOR) { update_achievement(iter_account->user, senior, 1); }      else { continue; } 
    if (rating_account >= LOW_HERO) { update_achievement(iter_account->user, hero, 1); }          else { continue; }
    if (rating_account >= LOW_SUPERHERO) { update_achievement(iter_account->user, superhero, 1); }else { continue; }
  }
}