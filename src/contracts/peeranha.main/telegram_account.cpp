#include "telegram_account.hpp"

void peeranha::approve_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  eosio::check(iter_telegram_account->confirmed != CONFIRMED_TELEGRAM_ACCOUNT, "This telos account already has a Telegram account");
  eosio::check(iter_telegram_account != telegram_account_table.end(), "Account not found");

  telegram_account_table.modify(
      iter_telegram_account, _self, [](auto &telegram_account) {
        telegram_account.confirmed = CONFIRMED_TELEGRAM_ACCOUNT;
      });
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  for(auto iter_telegram_account_user_id = telegram_account_table_user_id.begin(); iter_telegram_account_user_id != telegram_account_table_user_id.end(); ++iter_telegram_account_user_id) {
    if (iter_telegram_account_user_id->confirmed == EMPTY_TELEGRAM_ACCOUNT && iter_telegram_account_user_id->telegram_id == iter_telegram_account->telegram_id) {
      eosio::name old_user = iter_telegram_account_user_id->user;
      telegram_account_table_user_id.erase(iter_telegram_account_user_id);    //delete empty account
      swap_account(old_user, user);
      break;
    }
  }
}

void peeranha::disapprove_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);

  for (auto iter_telegram_account = telegram_account_table.begin(); iter_telegram_account != telegram_account_table.end(); ++iter_telegram_account) {
    if (iter_telegram_account->user == user && iter_telegram_account->confirmed != EMPTY_TELEGRAM_ACCOUNT) {
      telegram_account_table.erase(iter_telegram_account);
      return;
    }
  }
  
  eosio::check(false, "Telegram account not found");
}

void peeranha::add_telegram_account(eosio::name user, uint64_t telegram_id, bool new_account) { 
  find_account(user);
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  eosio::check(iter_telegram_account == telegram_account_table.end(), "This telos account already has a Telegram account");
  eosio::check(iter_telegram_account_user_id == telegram_account_table_user_id.end() || iter_telegram_account_user_id->confirmed == EMPTY_TELEGRAM_ACCOUNT, "This Telegram account already has a telos account");

  telegram_account_table.emplace(
    _self, [&user, telegram_id, new_account](auto &telegram_account) {
      telegram_account.user = user;
      telegram_account.telegram_id = telegram_id;
      telegram_account.confirmed = NOT_CONFIRMED_TELEGRAM_ACCOUNT;
      if (new_account) {
        telegram_account.confirmed = EMPTY_TELEGRAM_ACCOUNT;
      }
    });
}

void peeranha::add_empty_telegram_account(uint64_t telegram_id, std::string display_name, const IpfsHash ipfs_profile, const IpfsHash ipfs_avatar) {
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts); 
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  eosio::check(iter_telegram_account_user_id == telegram_account_table_user_id.end(), "This Telegram account already has a telos account");
  
  eosio::name user = generate_temp_telegram_account();

  register_account(user, display_name, ipfs_profile, ipfs_avatar);
  add_telegram_account(user, telegram_id, true);

  auto iter_account = account_table.find(user.value);
  eosio::check(iter_account != account_table.end(), "Error register empty account");
  account_table.modify(
      iter_account, _self,
      [](auto &account) {
        set_property(account.integer_properties, PROPERTY_EMPTY_ACCOUNT, 1);
  });
}

eosio::name peeranha::generate_temp_telegram_account() {
  std::string new_account = "tgm";
  eosio::name user;
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
  return user;
}

void peeranha::update_display_name(uint64_t telegram_id, std::string display_name) { 
  assert_display_name(display_name);
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();

  eosio::name item_user = eosio::name(0);
  for(auto iter_telegram_account_user_id = telegram_account_table_user_id.begin(); iter_telegram_account_user_id != telegram_account_table_user_id.end(); ++iter_telegram_account_user_id) {  
    if (iter_telegram_account_user_id->telegram_id == telegram_id) {
      eosio::check(iter_telegram_account_user_id->confirmed != NOT_CONFIRMED_TELEGRAM_ACCOUNT, "Account not confirmed");
      item_user = iter_telegram_account_user_id->user;
    }
  }
  eosio::check(item_user != eosio::name(0), "Telegram account not found");
  
  auto iter_account = find_account(item_user);
  account_table.modify(iter_account, _self,
                        [display_name](auto &account) {
                          account.display_name = display_name;
                        });
}

eosio::name peeranha::get_telegram_action_account(uint64_t telegram_id) {
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts); 
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  eosio::check(iter_telegram_account_user_id != telegram_account_table_user_id.end(), "Telegram account not found"); // add text error
  eosio::check(iter_telegram_account_user_id->confirmed == CONFIRMED_TELEGRAM_ACCOUNT || iter_telegram_account_user_id->confirmed == EMPTY_TELEGRAM_ACCOUNT, "Account not confirmed"); // add text error
  
  return iter_telegram_account_user_id->user;
}

void peeranha::swap_account(eosio::name old_user, eosio::name new_user) {    //telegram id????
  move_table_usranswers(old_user, new_user);
  move_table_usrquestions(old_user, new_user);
  move_table_achieve(old_user, new_user);
  delete_table_property_community(old_user, new_user);
  delete_table_period_rating(old_user, new_user);
  move_table_statistic(old_user, new_user);
}

void peeranha::move_table_statistic(eosio::name old_user, eosio::name new_user) {
  auto iter_new_account = find_account(new_user);
  auto iter_old_account = find_account(old_user);

  account_table.modify(iter_new_account, _self,
                       [&iter_old_account](auto &account) {
                          if(iter_old_account->rating  >= RATING_ON_CREATE) {
                            account.rating += iter_old_account->rating - RATING_ON_CREATE;
                            account.pay_out_rating += iter_old_account->pay_out_rating - RATING_ON_CREATE;
                          }
                          account.report_power += iter_old_account->report_power;
                          account.questions_asked += iter_old_account->questions_asked;
                          account.answers_given += iter_old_account->answers_given;
                          account.correct_answers += iter_old_account->correct_answers;

                          int32_t sum_first_answer = get_property_d(iter_old_account->integer_properties, PROPERTY_FIRST_ANSWER, 0);
                          sum_first_answer += get_property_d(account.integer_properties, PROPERTY_FIRST_ANSWER, 0);
                          set_property(account.integer_properties, PROPERTY_FIRST_ANSWER, sum_first_answer);

                          int32_t sum_answer_15_minutes = get_property_d(iter_old_account->integer_properties, PROPERTY_ANSWER_15_MINUTES, 0);
                          sum_answer_15_minutes += get_property_d(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, 0);
                          set_property(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, sum_answer_15_minutes);
                       });
  global_stat_index global_stat_table(_self, scope_all_stat);
  global_stat_table.modify(
      --global_stat_table.end(), _self,
      [](auto &global_stat) { global_stat.user_count -= 1; });
  account_table.erase(iter_old_account);
}

void peeranha::move_table_usrquestions(eosio::name old_user, eosio::name new_user) {
  user_questions_index new_user_questions_table(_self, new_user.value);                                 //move table usranswers
  user_questions_index old_user_questions_table(_self, old_user.value);
  auto iter_old_user_questions = old_user_questions_table.begin();

  int8_t rating_change = 0;
  int32_t delete_first_answer = 0;
  int32_t delete_answer_15_minutes = 0;
  while (iter_old_user_questions != old_user_questions_table.end()) {
    new_user_questions_table.emplace(_self, [&iter_old_user_questions](auto &usr_question) {
      usr_question.question_id = iter_old_user_questions->question_id;
    });
    auto iter_question = find_question(iter_old_user_questions->question_id);                       //change author question  
    auto vote_question = QUESTION_UPVOTED_REWARD;
    auto vote_answer_res = VoteItem::answer;
    switch (get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                         QUESTION_TYPE_EXPERT)) {
      case QUESTION_TYPE_GENERAL:
        vote_question = COMMON_QUESTION_UPVOTED_REWARD;
        vote_answer_res = VoteItem::common_answer;
        break;
      }

    std::for_each(iter_question->history.begin(), iter_question->history.end(), [&new_user, &rating_change, vote_question](auto hst) {
      if (hst.is_flag_set(HISTORY_UPVOTED_FLG) && hst.user == new_user) {
        rating_change -= vote_question;
      }
    });

    std::for_each(iter_question->answers.begin(), iter_question->answers.end(), [new_user, &delete_answer_15_minutes, &delete_first_answer, vote_answer_res, &rating_change](auto answer) {
      if (get_property_d(answer.properties, PROPERTY_ANSWER_15_MINUTES, -2) == 1 && answer.user == new_user) {
        rating_change -= vote_answer_res.answer_15_minutes;
        delete_answer_15_minutes++;
      }
      if (get_property_d(answer.properties, PROPERTY_FIRST_ANSWER, -2) == 1 && answer.user == new_user) {
        rating_change -= vote_answer_res.first_answer;
        delete_first_answer++;
      }
    });

    question_table.modify(iter_question, _self,
                        [new_user](auto &question) {
                          question.user = new_user;
                          set_property(question.properties, PROPERTY_EMPTY_QUESTION, 0);
                        });
    iter_old_user_questions = old_user_questions_table.erase(iter_old_user_questions);
  }
  update_rating(new_user, rating_change, [delete_first_answer, delete_answer_15_minutes](auto &account) {
    int32_t first_answer = get_property_d(account.integer_properties, PROPERTY_FIRST_ANSWER, 0);
    set_property(account.integer_properties, PROPERTY_FIRST_ANSWER, first_answer - delete_first_answer);

    int32_t answer_15_minutes = get_property_d(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, 0);
    set_property(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, answer_15_minutes - delete_answer_15_minutes);
  });
}

void peeranha::move_table_usranswers(eosio::name old_user, eosio::name new_user) {
  user_answers_index new_user_answer_table(_self, new_user.value);                                  //move table usrquestions
  user_answers_index old_user_answer_table(_self, old_user.value);
  int32_t delete_first_answer = 0;
  int32_t delete_answer_15_minutes = 0;
  int32_t rating_change_old_user = 0;
  int32_t rating_change_new_user = 0;

  auto iter_old_user_answer = old_user_answer_table.begin();
  while (iter_old_user_answer != old_user_answer_table.end()) {
    if (new_user_answer_table.find(iter_old_user_answer->question_id) == new_user_answer_table.end()) { //duplicate object
      new_user_answer_table.emplace(_self, [&iter_old_user_answer](auto &usr_question) {
        usr_question.question_id = iter_old_user_answer->question_id;
        usr_question.answer_id = iter_old_user_answer->answer_id;
      });
    }
    
    auto iter_question = find_question(iter_old_user_answer->question_id);                       //change author answer
    auto vote_question_res = VoteItem::question;
    auto vote_answer_res = VoteItem::answer;
    switch (get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                         QUESTION_TYPE_EXPERT)) {
      case QUESTION_TYPE_GENERAL:
        vote_question_res = VoteItem::common_question;
        vote_answer_res = VoteItem::common_answer;
        break;
    }
 
    question_table.modify(iter_question, _self,
                        [new_user, &iter_old_user_answer, &rating_change_old_user, &rating_change_new_user, vote_answer_res, vote_question_res, &delete_answer_15_minutes, &delete_first_answer](auto &question) {
                          auto iter_answer = find_answer(question, iter_old_user_answer->answer_id);
                          iter_answer->user = new_user;
                          set_property(iter_answer->properties, PROPERTY_EMPTY_ANSWER, 0);

                          if (question.correct_answer_id == iter_answer->id && question.user == new_user) {
                            rating_change_old_user -= vote_answer_res.correct_answer;
                            rating_change_new_user -= vote_question_res.correct_answer;
                          }
                          if (get_property_d(iter_answer->properties, PROPERTY_ANSWER_15_MINUTES, -2) == 1 && question.user == new_user) {
                            rating_change_old_user -= vote_answer_res.answer_15_minutes;
                            delete_answer_15_minutes++;
                          }
                          if (get_property_d(iter_answer->properties, PROPERTY_FIRST_ANSWER, -2) == 1 && question.user == new_user) {
                            rating_change_old_user -= vote_answer_res.first_answer;
                            delete_first_answer++;
                          }

                          std::for_each(iter_answer->history.begin(), iter_answer->history.end(), [&new_user, &rating_change_old_user, vote_answer_res](auto hst) {
                            if (hst.is_flag_set(HISTORY_UPVOTED_FLG) && hst.user == new_user) {
                              rating_change_old_user -= vote_answer_res.upvoted_reward;
                            }
                          });
                        });

    iter_old_user_answer = old_user_answer_table.erase(iter_old_user_answer);
  }

  update_rating(old_user, rating_change_old_user, [delete_first_answer, delete_answer_15_minutes](auto &account) {
    int32_t first_answer = get_property_d(account.integer_properties, PROPERTY_FIRST_ANSWER, 0);
    set_property(account.integer_properties, PROPERTY_FIRST_ANSWER, first_answer - delete_first_answer);

    int32_t answer_15_minutes = get_property_d(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, 0);
    set_property(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, answer_15_minutes - delete_answer_15_minutes);
  });

  update_rating(new_user, rating_change_new_user);
}

void peeranha::move_table_achieve(eosio::name old_user, eosio::name new_user) {
  account_achievements_index old_account_achievements_table(_self, old_user.value);               //achive
  auto iter_account_achievements = old_account_achievements_table.begin();
  while (iter_account_achievements != old_account_achievements_table.end()) {
    auto achieve = achievements.find(iter_account_achievements->achievements_id);
    update_achievement(new_user, achieve->second.group, achieve->second.lower_bound);
    decrement_achievement_count(iter_account_achievements->achievements_id);
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