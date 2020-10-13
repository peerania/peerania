#include "telegram_account.hpp"

void peeranha::approve_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  eosio::check(iter_telegram_account->confirmed != 1, "This telos account already has a Telegram account");
  eosio::check(iter_telegram_account != telegram_account_table.end(), "Account not found");

  telegram_account_table.modify(
      iter_telegram_account, _self, [](auto &telegram_account) {
        telegram_account.confirmed = 1;
      });
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  for(auto iter_telegram_account_user_id = telegram_account_table_user_id.begin(); iter_telegram_account_user_id != telegram_account_table_user_id.end(); ++iter_telegram_account_user_id) {
    if (iter_telegram_account_user_id->confirmed == 2 && iter_telegram_account_user_id->telegram_id == iter_telegram_account->telegram_id) {
      eosio::name old_user = iter_telegram_account_user_id->user;
      telegram_account_table_user_id.erase(iter_telegram_account_user_id);    //delete empty account
      swap_account(old_user, user);
      break;
    }
  }
}

void peeranha::disapprove_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  eosio::check(iter_telegram_account != telegram_account_table.end(), "Account not found");

  telegram_account_table.erase(iter_telegram_account);
}

void peeranha::add_telegram_account(eosio::name user, uint64_t telegram_id, bool new_account) { 
  find_account(user);
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);

  eosio::check(iter_telegram_account == telegram_account_table.end(), "This telos account already has a Telegram account");
  eosio::check(iter_telegram_account_user_id == telegram_account_table_user_id.end() || iter_telegram_account_user_id->confirmed == 2, "This Telegram account already has a telos account");

  telegram_account_table.emplace(
    _self, [&user, telegram_id, new_account](auto &telegram_account) {
      telegram_account.user = user;
      telegram_account.telegram_id = telegram_id;
      telegram_account.confirmed = 0;
      if (new_account) {
        telegram_account.confirmed = 2;
      }
    });
}

void peeranha::add_empty_telegram_account(uint64_t telegram_id, std::string display_name, const IpfsHash ipfs_profile, const IpfsHash ipfs_avatar) {
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts); 
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  eosio::check(iter_telegram_account_user_id == telegram_account_table_user_id.end(), "This Telegram account already has a telos account");
  
  eosio::name user;
  std::string new_account = "tgm";
  do {
    uint64_t value;
    uint64_t buf = now();
    for (int i = 0; i < 9; i++) {
      value = buf;
      buf = (value / 10) *10;
      value -= buf;
      if (value > 5) {
        value -= 5;
      } else if (value == 0) {
        value = 5;
      }
      new_account += std::to_string(value);
      buf /= 10;
    }
    user = eosio::name(new_account);
  }
  while (account_table.find(user.value) != account_table.end());
  register_account(user, display_name, ipfs_avatar, ipfs_avatar);
  add_telegram_account(user, telegram_id, true);

  auto iter_account = account_table.find(user.value);
  eosio::check(iter_account != account_table.end(), "Error register empty account");
  account_table.modify(
      iter_account, _self,
      [](auto &account) {
        set_property(account.integer_properties, PROPERTY_EMPTY_ACCOUNT, 1);
  });
}

eosio::name peeranha::telegram_post_action(uint64_t telegram_id) {
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts); 
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  eosio::check(iter_telegram_account_user_id != telegram_account_table_user_id.end(), "Account not found"); // add text error
  eosio::check(iter_telegram_account_user_id->confirmed == 1 || iter_telegram_account_user_id->confirmed == 2, "Account not confirmed"); // add text error
  
  return iter_telegram_account_user_id->user;
}

void peeranha::swap_account(eosio::name old_user, eosio::name new_user) {    //telegram id????
  move_table_usranswers(old_user, new_user);
  move_table_usrquestions(old_user, new_user);
  move_table_achive(old_user, new_user);
  delete_table_property_community(old_user, new_user);
  delete_table_period_rating(old_user, new_user);
  move_table_statistik(old_user, new_user);
}

void peeranha::move_table_statistik(eosio::name old_user, eosio::name new_user) {
  auto iter_new_account = find_account(new_user);
  auto iter_old_account = find_account(old_user);

  account_table.modify(iter_new_account, _self,
                       [&iter_old_account](auto &account) {
                          account.rating += iter_old_account->rating - RATING_ON_CREATE;
                          account.pay_out_rating += iter_old_account->pay_out_rating - RATING_ON_CREATE;
                          account.report_power += iter_old_account->report_power;
                          account.questions_asked += iter_old_account->questions_asked;
                          account.answers_given += iter_old_account->answers_given;
                          account.correct_answers += iter_old_account->correct_answers;
                       });
  account_table.erase(iter_old_account);
}

void peeranha::move_table_usrquestions(eosio::name old_user, eosio::name new_user) {
  user_questions_index new_user_questions_table(_self, new_user.value);                                 //move table usranswers
  user_questions_index old_user_questions_table(_self, old_user.value);
  auto iter_old_user_questions = old_user_questions_table.begin();
  while (iter_old_user_questions != old_user_questions_table.end()) {
    new_user_questions_table.emplace(_self, [&iter_old_user_questions](auto &usr_question) {
      usr_question.question_id = iter_old_user_questions->question_id;
    });
    auto iter_question = find_question(iter_old_user_questions->question_id);                       //change author question
    question_table.modify(iter_question, _self,
                        [new_user](auto &question) {
                          question.user = new_user;
                        });
    iter_old_user_questions = old_user_questions_table.erase(iter_old_user_questions);
  }
}

void peeranha::move_table_usranswers(eosio::name old_user, eosio::name new_user) {
  user_answers_index new_user_answer_table(_self, new_user.value);                                  //move table usrquestions
  user_answers_index old_user_answer_table(_self, old_user.value);
  auto iter_old_user_answer = old_user_answer_table.begin();
  while (iter_old_user_answer != old_user_answer_table.end()) {
    new_user_answer_table.emplace(_self, [&iter_old_user_answer](auto &usr_question) {
      usr_question.question_id = iter_old_user_answer->question_id;
      usr_question.answer_id = iter_old_user_answer->answer_id;
    });
    auto iter_question = find_question(iter_old_user_answer->question_id);                       //change author answer
    question_table.modify(iter_question, _self,
                        [new_user, &iter_old_user_answer, &iter_question](auto &question) {
                          auto iter_answer = find_answer(question, iter_old_user_answer->answer_id);
                          iter_answer->user = new_user;
                        });

    iter_old_user_answer = old_user_answer_table.erase(iter_old_user_answer);
  }
}

void peeranha::move_table_achive(eosio::name old_user, eosio::name new_user) {
  account_achievements_index old_account_achievements_table(_self, old_user.value);               //achive
  auto iter_account_achievements = old_account_achievements_table.begin();
  while (iter_account_achievements != old_account_achievements_table.end()) {
    auto achieve = achievements.find(iter_account_achievements->achievements_id);
    if (achieve->second.type == UNIQE && iter_account_achievements->value == 1) {
      update_achievement(new_user, iter_account_achievements->achievements_id, iter_account_achievements->value, true);
    }
    else if (achieve->second.type == LEVEL) {
      update_achievement(new_user, iter_account_achievements->achievements_id, iter_account_achievements->value, true);
    }
    del_achievement_amount(iter_account_achievements->achievements_id);
    iter_account_achievements = old_account_achievements_table.erase(iter_account_achievements);
  }
}

void peeranha::delete_table_property_community(eosio::name old_user, eosio::name new_user) {
  property_community_index property_community_table(_self, scope_all_property_community);             //property_community
  auto iter_property_community = property_community_table.find(old_user.value);
  if (iter_property_community != property_community_table.end())
    property_community_table.erase(iter_property_community);
}

void peeranha::delete_table_period_rating(eosio::name old_user, eosio::name new_user) {
  period_rating_index period_rating_table(_self, old_user.value);                                     //period_rating
  auto iter_period_rating = period_rating_table.begin();
  while (iter_period_rating != period_rating_table.end()) {
    iter_period_rating = period_rating_table.erase(iter_period_rating);
  }
}