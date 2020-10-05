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
    if (iter_telegram_account_user_id->confirmed == 2) {
      swap_account(iter_telegram_account_user_id->telegram_id, iter_telegram_account_user_id->user,  user);
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

eosio::name peeranha::telegram_post_action(uint64_t telegram_id) {
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts); 
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  
  eosio::name user;
  if (iter_telegram_account_user_id != telegram_account_table_user_id.end()) {
    bool check = iter_telegram_account_user_id->confirmed == 1 || iter_telegram_account_user_id->confirmed == 2;
    eosio::check(check, "Account not confirmed"); // add text error
    user = iter_telegram_account_user_id->user;
  } else {
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

    // const IpfsHash ipfs_profile = {18, 177, 253, 234, 86, 53, 221, 27, 4, 142, 68, 133, 172, 104, 26, 17, 244, 156, 224, 197, 231, 159, 178, 167, 245, 112, 1, 139, 232, 198, 124, 225, 162};
    // const IpfsHash ipfs_avatar = {18, 254, 86, 251, 60, 165, 231, 126, 138, 64, 117, 29, 190, 91, 185, 94, 90, 25, 235, 76, 6, 26, 74, 178, 119, 211, 158, 57, 68, 171, 203, 116, 79};
    
    const IpfsHash ipfs_profile = {'q', 'w', 's'};
    const IpfsHash ipfs_avatar = {'w', 'd', 'r'};
    register_account(user, new_account, ipfs_avatar, ipfs_avatar);
    add_telegram_account(user, telegram_id, true);
  }
  return user;
}

void peeranha::swap_account(int telegram_id, eosio::name old_user, eosio::name new_user) {
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
  update_achievement_rating(iter_new_account->user);

  user_questions_index new_user_questions_table(_self, new_user.value);   //move table usranswers
  user_questions_index old_user_questions_table(_self, old_user.value);
  auto iter_old_user_questions = old_user_questions_table.begin();
  while (iter_old_user_questions != old_user_questions_table.end()) {
    new_user_questions_table.emplace(_self, [&iter_old_user_questions](auto &usr_question) {
      usr_question.question_id = iter_old_user_questions->question_id;
    });
    auto iter_question = find_question(iter_old_user_questions->question_id); //change author question
    question_table.modify(iter_question, _self,
                        [new_user](auto &question) {
                          question.user = new_user;
                        });
    iter_old_user_questions = old_user_questions_table.erase(iter_old_user_questions);
  }

  user_answers_index new_user_answer_table(_self, new_user.value);        //move table usrquestions
  user_answers_index old_user_answer_table(_self, old_user.value);
  auto iter_old_user_answer = old_user_answer_table.begin();
  while (iter_old_user_answer != old_user_answer_table.end()) {
    new_user_answer_table.emplace(_self, [&iter_old_user_answer](auto &usr_question) {
      usr_question.question_id = iter_old_user_answer->question_id;
      usr_question.answer_id = iter_old_user_answer->answer_id;
    });
    auto iter_question = find_question(iter_old_user_answer->question_id);  //change author answer
    question_table.modify(iter_question, _self,
                        [new_user, &iter_old_user_answer, &iter_question](auto &question) {
                          auto iter_answer = find_answer(question, iter_old_user_answer->answer_id);
                          iter_answer->user = new_user;
                        });

    iter_old_user_answer = old_user_answer_table.erase(iter_old_user_answer);
  }
}