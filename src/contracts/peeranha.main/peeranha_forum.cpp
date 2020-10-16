#include "peeranha.hpp"

question_index::const_iterator peeranha::find_question(uint64_t question_id) {
  auto iter_question = question_table.find(question_id);
  eosio::check(iter_question != question_table.end(), "Question not found!");
  return iter_question;
}

void peeranha::post_question(eosio::name user, uint16_t community_id,
                             const std::vector<uint32_t> tags,
                             const std::string &title,
                             const IpfsHash &ipfs_link, const uint8_t type) {
  assert_ipfs(ipfs_link);
  assert_title(title);
  assert_question_type(type);
  auto iter_account = find_account(user);
  update_rating(iter_account, POST_QUESTION_REWARD, [community_id](auto &account) {
    account.reduce_energy(ENERGY_POST_QUESTION, community_id);
    account.questions_asked += 1;
  });
  assert_allowed(*iter_account, user, Action::POST_QUESTION, community_id);
  uint64_t question_id = get_reversive_pk(question_table, MAX_QUESTION_ID);
  // sort - unique
  for (int i = 0; i < tags.size(); ++i)
    for (int j = i + 1; j < tags.size(); ++j)
      if (tags[i] == tags[j]) eosio::check(false, "Duplicate tag");
  question_table.emplace(_self, [&](auto &question) {
    question.id = question_id;
    question.community_id = community_id;
    question.tags = tags;
    question.user = user;
    question.title = title;
    question.ipfs_link = ipfs_link;
    question.post_time = now();
    set_property_d(question.properties, PROPERTY_QUESTION_TYPE, (int)type,
                   QUESTION_TYPE_EXPERT);
  });
#ifdef SUPERFLUOUS_INDEX
  user_questions_index user_questions_table(_self, user.value);
  user_questions_table.emplace(_self, [question_id](auto &usr_question) {
    usr_question.question_id = question_id;
  });
#endif
  update_community_statistics(community_id, 1, 0, 0, 0);
  update_tags_statistics(community_id, tags, 1);
  update_account_achievement(iter_account->user, QUESTION_ASKED);
}

void peeranha::post_answer(eosio::name user, uint64_t question_id,
                           const IpfsHash &ipfs_link, bool official_answer) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio::check(iter_question->answers.size() < MAX_ANSWER_COUNT,
               "For this question reached answer count limit");
  assert_allowed(*iter_account, iter_question->user, Action::POST_ANSWER, iter_question->community_id);
  eosio::check(
      none_of(iter_question->answers.begin(), iter_question->answers.end(),
              [user](const answer &a) { return a.user == user; }),
      "Answer with this username already posted");
  answer new_answer;
  new_answer.user = user;
  new_answer.ipfs_link = ipfs_link;
  new_answer.post_time = now();
  
  if(official_answer && find_account_property_community(user, COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER, iter_question->community_id)){
    new_answer.properties.push_back(add_official_answer());
  }

  auto vote_answer_res = VoteItem::answer;
  switch (get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                            QUESTION_TYPE_EXPERT)) {
    case QUESTION_TYPE_GENERAL: {
        vote_answer_res = VoteItem::common_answer;
    } break;
    default:
    break;
  }
  int8_t rating_change = 0;
  if (now() - iter_question->post_time <= TIME_15_MINUTES) {
    int_key_value key_value;
    key_value.key = PROPERTY_ANSWER_15_MINUTES;
    key_value.value = 1;
    new_answer.properties.push_back(key_value);
    rating_change += vote_answer_res.upvoted_reward;
    update_achievement(iter_account->user, ANSWER_15_MINUTES, 1, false);  
  }
  if (iter_question->answers.size() == 0) {
    int_key_value key_value;
    key_value.key = PROPERTY_FIRST_ANSWER;
    key_value.value = 1;
    new_answer.properties.push_back(key_value);
    rating_change += vote_answer_res.upvoted_reward;
    update_achievement(iter_account->user, FIRST_ANSWER, 1, false);
  }

  uint16_t answer_id;
  question_table.modify(iter_question, _self,
                        [&new_answer, &answer_id](auto &question) {
                          push_new_forum_item(question.answers, new_answer);
                          answer_id = new_answer.id;
                        });

#ifdef SUPERFLUOUS_INDEX
  user_answers_index user_answers_table(_self, user.value);
  user_answers_table.emplace(_self, [question_id, answer_id](auto &usr_answer) {
    usr_answer.question_id = question_id;
    usr_answer.answer_id = answer_id;
  });
#endif
  uint64_t community_id = iter_question->community_id;
  update_community_statistics(iter_question->community_id, 0, 1, 0, 0);
  update_rating(iter_account, rating_change + POST_ANSWER_REWARD, [community_id](auto &account) {
    account.reduce_energy(ENERGY_POST_ANSWER, community_id);
    account.answers_given += 1;
  });
  update_account_achievement(iter_account->user, ANSWER_GIVEN);
}
#ifdef SUPERFLUOUS_INDEX
void peeranha::remove_user_question(eosio::name user, uint64_t question_id) {
  user_questions_index user_questions_table(_self, user.value);
  auto iter_user_question = user_questions_table.find(question_id);
  eosio::check(iter_user_question != user_questions_table.end(),
               "Question not found");
  user_questions_table.erase(iter_user_question);
  eosio::check(iter_user_question != user_questions_table.end(),
               "Address not erased properly");
}

void peeranha::remove_user_answer(eosio::name user, uint64_t question_id) {
  user_answers_index user_answers_table(_self, user.value);
  auto iter_user_answer = user_answers_table.find(question_id);
  eosio::check(iter_user_answer != user_answers_table.end(),
               "Answer not found");
  user_answers_table.erase(iter_user_answer);
  eosio::check(iter_user_answer != user_answers_table.end(),
               "Address not erased properly");
}
#endif

void peeranha::post_comment(eosio::name user, uint64_t question_id,
                            uint16_t answer_id, const IpfsHash &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  comment new_comment;
  new_comment.user = user;
  new_comment.ipfs_link = ipfs_link;
  new_comment.post_time = now();
  uint64_t community_id = iter_question->community_id;
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, &new_comment, community_id](auto &question) {
        if (apply_to_question(answer_id)) {
          assert_allowed(*iter_account, question.user, Action::POST_COMMENT, community_id);
          push_new_forum_item(question.comments, new_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto global_item_user = question.user == iter_account->user
                                      ? question.user
                                      : iter_answer->user;
          assert_allowed(*iter_account, global_item_user, Action::POST_COMMENT, community_id);
          push_new_forum_item(iter_answer->comments, new_comment);
        }
      });
  update_rating(iter_account, POST_COMMENT_REWARD, [community_id](auto &account) {
    account.reduce_energy(ENERGY_POST_COMMENT, community_id);
  });
}

void peeranha::delete_question(eosio::name user, uint64_t question_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::DELETE_QUESTION, iter_question->community_id);
  eosio::check(iter_question->answers.empty(),
               "You can't delete not empty question");
  update_community_statistics(iter_question->community_id, -1, 0, 0, 0);
  update_tags_statistics(iter_question->community_id, iter_question->tags, -1);
  delete_top_question(iter_question->community_id, question_id);
#ifdef SUPERFLUOUS_INDEX
  remove_user_question(user, question_id);
#endif
  int upvote_mul = QUESTION_UPVOTED_REWARD;
  switch (get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                         QUESTION_TYPE_EXPERT)) {
    case QUESTION_TYPE_GENERAL:
      upvote_mul = COMMON_QUESTION_UPVOTED_REWARD;
      break;
  }
  update_rating(iter_account,
                -upvote_count(iter_question->history) * upvote_mul + DELETE_OWN_QUESTION_REWARD,
                [](auto &account) {
                  account.reduce_energy(ENERGY_DELETE_QUESTION);
                  account.questions_asked -= 1;
                });
  update_account_achievement(user, QUESTION_ASKED);
  question_table.erase(iter_question);
  eosio::check(iter_question != question_table.end(),
               "Address not erased properly");
}

void peeranha::delete_answer(eosio::name user, uint64_t question_id,
                             uint16_t answer_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio::check(iter_question->correct_answer_id != answer_id,
               "You can't delete this answer");
  int rating_change = DELETE_OWN_ANSWER_REWARD;
  uint16_t community_id = iter_question->community_id;
  bool within_15_minutes;
  bool first_answer;
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, &rating_change, community_id, &within_15_minutes, &first_answer](auto &question) {
        int upvote_mul = ANSWER_UPVOTED_REWARD;
        switch (get_property_d(question.properties, PROPERTY_QUESTION_TYPE,
                               QUESTION_TYPE_EXPERT)) {
          case QUESTION_TYPE_GENERAL:
            upvote_mul = COMMON_ANSWER_UPVOTED_REWARD;
            break;
        }

        auto iter_answer = find_answer(question, answer_id);
        rating_change -= upvote_count(iter_answer->history) * upvote_mul;
        assert_allowed(*iter_account, iter_answer->user, Action::DELETE_ANSWER, community_id);

        auto within_15_minutes_property = get_property_d(iter_answer->properties, PROPERTY_ANSWER_15_MINUTES, -1);
        if(within_15_minutes_property == 1) {
          rating_change -= upvote_mul;
          within_15_minutes = true;
        }

        auto first_answer_property = get_property_d(iter_answer->properties, PROPERTY_FIRST_ANSWER, -1);
        if(first_answer_property == 1) {
          rating_change -= upvote_mul;
          first_answer = true;
        }
        question.answers.erase(iter_answer);
      });
#ifdef SUPERFLUOUS_INDEX
  remove_user_answer(user, question_id);
#endif
  update_community_statistics(iter_question->community_id, 0, -1, 0, 0);
  update_rating(iter_account,
                rating_change,
                [](auto &account) {
                  account.reduce_energy(ENERGY_DELETE_ANSWER);
                  account.answers_given -= 1;
                });
  if(within_15_minutes)
    update_achievement(iter_account->user, ANSWER_15_MINUTES, -1, false);
  if(first_answer)
    update_achievement(iter_account->user, FIRST_ANSWER, -1, false);
  update_account_achievement(user, ANSWER_GIVEN);
}

void peeranha::delete_comment(eosio::name user, uint64_t question_id,
                              uint16_t answer_id, uint64_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  uint64_t community_id = iter_question->community_id;
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, comment_id, community_id](auto &question) {
        if (apply_to_question(answer_id)) {
          auto iter_comment = find_comment(question, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::DELETE_COMMENT, community_id);
          question.comments.erase(iter_comment);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::DELETE_COMMENT, community_id);
          iter_answer->comments.erase(iter_comment);
        }
      });
  update_rating(iter_account, DELETE_OWN_COMMENT_REWARD, [](auto &account) {
    account.reduce_energy(ENERGY_DELETE_COMMENT);
  });
}

void peeranha::modify_question(eosio::name user, uint64_t question_id,
                               uint16_t community_id,
                               const std::vector<uint32_t> &tags,
                               const std::string &title,
                               const IpfsHash &ipfs_link) {
  assert_ipfs(ipfs_link);
  assert_title(title);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  assert_allowed(*iter_account, iter_question->user, Action::MODIFY_QUESTION, community_id);
  for (int i = 0; i < tags.size(); ++i)
    for (int j = i + 1; j < tags.size(); ++j)
      if (tags[i] == tags[j]) eosio::check(false, "Duplicate tag");
  eosio::check(tags.size() <= MAX_TAG_COUNT, "Too many tags");
  update_community_statistics(iter_question->community_id, -1, 0, 0, 0);
  update_tags_statistics(iter_question->community_id, iter_question->tags, -1);
  update_community_statistics(community_id, 1, 0, 0, 0);
  update_tags_statistics(community_id, tags, 1);
  question_table.modify(
      iter_question, _self,
      [&ipfs_link, &title, community_id, &tags](auto &question) {
        question.ipfs_link = ipfs_link;
        question.title = title;
        question.community_id = community_id;
        question.tags = tags;
        set_property(question.properties, PROPERTY_LAST_MODIFIED, now());
      });
  update_rating(iter_account, 0, [](auto &account) {
    account.reduce_energy(ENERGY_MODIFY_QUESTION);
  });
}

void peeranha::modify_answer(eosio::name user, uint64_t question_id,
                             uint16_t answer_id, const IpfsHash &ipfs_link, bool official_answer) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  auto community_id = iter_question->community_id;
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, &ipfs_link, official_answer, community_id, user](auto &question) {
        auto iter_answer = find_answer(question, answer_id);
        assert_allowed(*iter_account, iter_answer->user, Action::MODIFY_ANSWER, community_id);
        iter_answer->ipfs_link = ipfs_link;
        set_property(iter_answer->properties, PROPERTY_LAST_MODIFIED, now());

        if(find_account_property_community(user, COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER, community_id)){
          auto iter_key = linear_find(iter_answer->properties.begin(), iter_answer->properties.end(), PROPERTY_OFFICIAL_ANSWER);
          if(official_answer && iter_key == iter_answer->properties.end()){
            iter_answer->properties.push_back(add_official_answer());
          }
          else if(!official_answer && iter_key != iter_answer->properties.end()){
            iter_answer->properties.erase(iter_key);
          }
        }
      });
  update_rating(iter_account, 0, [](auto &account) {
    account.reduce_energy(ENERGY_MODIFY_ANSWER);
  });
}

void peeranha::modify_comment(eosio::name user, uint64_t question_id,
                              uint16_t answer_id, uint16_t comment_id,
                              const IpfsHash &ipfs_link) {
  assert_ipfs(ipfs_link);
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  auto community_id = iter_question->community_id;
  question_table.modify(
      iter_question, _self,
      [iter_account, answer_id, comment_id, &ipfs_link, community_id](auto &question) {
        time current_time = now();
        if (apply_to_question(answer_id)) {
          auto iter_comment = find_comment(question, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::MODIFY_COMMENT, community_id);
          iter_comment->ipfs_link = ipfs_link;
          set_property(iter_comment->properties, PROPERTY_LAST_MODIFIED,
                       current_time);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          auto iter_comment = find_comment(*iter_answer, comment_id);
          assert_allowed(*iter_account, iter_comment->user,
                         Action::MODIFY_COMMENT, community_id);
          iter_comment->ipfs_link = ipfs_link;
          set_property(iter_comment->properties, PROPERTY_LAST_MODIFIED,
                       current_time);
        }
      });
  update_rating(iter_account, 0, [](auto &account) {
    account.reduce_energy(ENERGY_MODIFY_COMMENT);
  });
}
void peeranha::mark_answer_as_correct(eosio::name user, uint64_t question_id,
                                      uint16_t answer_id) {
  auto iter_question = find_question(question_id);

  int accept_answer_as_correct_reward, answer_accepted_as_correct_reward;
  switch (get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                         QUESTION_TYPE_EXPERT)) {
    case QUESTION_TYPE_GENERAL:
      accept_answer_as_correct_reward = ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD;
      answer_accepted_as_correct_reward =
          COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD;
      break;
    case QUESTION_TYPE_EXPERT:
      accept_answer_as_correct_reward = ACCEPT_ANSWER_AS_CORRECT_REWARD;
      answer_accepted_as_correct_reward = ANSWER_ACCEPTED_AS_CORRECT_REWARD;
      break;
  }

  auto iter_account = find_account(user);
  assert_allowed(*iter_account, iter_question->user,
                 Action::MARK_ANSWER_AS_CORRECT, iter_question->community_id);
  if (answer_id != EMPTY_ANSWER_ID) {
    eosio::check(iter_question->correct_answer_id != answer_id,
                 "This answer already marked as correct");
    auto iter_answer = binary_find(iter_question->answers.begin(),
                                   iter_question->answers.end(), answer_id);
    eosio::check(iter_answer != iter_question->answers.end(),
                 "Answer not found");
    if (iter_question->correct_answer_id == EMPTY_ANSWER_ID) {
      // No one answer has not been marked as correct yet
      // Reward question and answer users
      if (iter_answer->user != user) {
        update_rating(iter_account, accept_answer_as_correct_reward,
                      [](auto &account) {
                        account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
                      });
        update_rating(iter_answer->user, answer_accepted_as_correct_reward,
                      [](auto &account) { account.correct_answers += 1; });
      } else {
        update_rating(iter_account, [](auto &account) {
          account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
          account.correct_answers += 1;
        });
      }
      update_account_achievement(iter_answer->user, CORRECT_ANSWER);
    } else {
      // One of answers is marked as correct. Find this one,
      // pick up the reward of past user and give it to new
      auto iter_old_answer = binary_find(iter_question->answers.begin(),
                                         iter_question->answers.end(),
                                         iter_question->correct_answer_id);
      // check internal error iter_old_answer

      if (iter_old_answer->user != user) {
        update_rating(iter_old_answer->user, -answer_accepted_as_correct_reward,
                      [](auto &account) { account.correct_answers -= 1; });
        update_account_achievement(iter_old_answer->user, CORRECT_ANSWER);
      }
      else 
        update_rating(iter_account, accept_answer_as_correct_reward,
                      [](auto &account) {
                        account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
                        account.correct_answers -= 1;
                      });

      if (iter_answer->user != user)
        update_rating(iter_answer->user, answer_accepted_as_correct_reward,
                      [](auto &account) { account.correct_answers += 1; });
      else
        update_rating(iter_account, -accept_answer_as_correct_reward,
                      [](auto &account) {
                        account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
                        account.correct_answers += 1;
                      });

      if (iter_old_answer->user != user && iter_answer->user != user) {
        update_rating(iter_account, [](auto &account) {
          account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
        });
      }
      update_account_achievement(iter_old_answer->user, CORRECT_ANSWER);
      update_account_achievement(iter_answer->user, CORRECT_ANSWER);
      update_account_achievement(iter_account->user, CORRECT_ANSWER);
    }
  } else {
    // Set question to "without answer"
    eosio::check(
        iter_question->correct_answer_id != EMPTY_ANSWER_ID,
        "You can\'t reset correct answer for question without correct answer");
    auto iter_old_answer = binary_find(iter_question->answers.begin(),
                                       iter_question->answers.end(),
                                       iter_question->correct_answer_id);
    // pick up reward if question author isn't answer author
    // check internal error iter_old_answer
    if (iter_old_answer->user != user) {
      update_rating(iter_account, -accept_answer_as_correct_reward,
                    [](auto &account) {
                      account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
                    });
      update_rating(iter_old_answer->user, -answer_accepted_as_correct_reward,
                    [](auto &account) { account.correct_answers -= 1; });
    } else {
      update_rating(iter_account, [](auto &account) {
        account.reduce_energy(ENERGY_MARK_ANSWER_AS_CORRECT);
      });
    }
    update_account_achievement(iter_old_answer->user, CORRECT_ANSWER);
  }
  if (iter_question->correct_answer_id == EMPTY_ANSWER_ID &&
      answer_id != EMPTY_ANSWER_ID)
    update_community_statistics(iter_question->community_id, 0, 0, 1, 0);
  else if (iter_question->correct_answer_id != EMPTY_ANSWER_ID &&
           answer_id == EMPTY_ANSWER_ID)
    update_community_statistics(iter_question->community_id, 0, 0, -1, 0);
  question_table.modify(iter_question, _self, [answer_id](auto &question) {
    question.correct_answer_id = answer_id;
  });
}

void peeranha::change_question_type(eosio::name user, uint64_t question_id,
                                    int type, bool restore_rating) {
  assert_question_type(type);
  auto iter_moderator = find_account(user);
  auto iter_question = find_question(question_id);
  auto community_id = iter_question->community_id;
  bool global_moderator_flag = iter_moderator->has_moderation_flag(MODERATOR_FLG_CHANGE_QUESTION_STATUS);
  bool community_moderator_flag = find_account_property_community(user, COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS, community_id);
  eosio::check(global_moderator_flag || community_moderator_flag,
        "You don't have permission to change qustion status");

  eosio::check(get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                              QUESTION_TYPE_EXPERT) != type,
               "The question already has this type");
  std::map<uint64_t, int> rating_change;

  question_table.modify(
      iter_question, _self,
      [restore_rating, type, &rating_change](auto &question) {
        set_property_d(question.properties, PROPERTY_QUESTION_TYPE, type,
                       QUESTION_TYPE_EXPERT);
        if (!restore_rating) return;
        // TODO: Rewrite with switch case set var from and to

        // Claculate rating of switch from expert -> general
        // If reverse switch, just invert calculated rating
        int question_owner_rating_change = 0;
        for_each(question.history.begin(), question.history.end(),
                 [&question_owner_rating_change](auto history_item) {
                   if (history_item.is_flag_set(HISTORY_UPVOTED_FLG)) {
                     question_owner_rating_change +=
                         COMMON_QUESTION_UPVOTED_REWARD -
                         QUESTION_UPVOTED_REWARD;
                   }
                 });
        rating_change[question.user.value] = question_owner_rating_change;

        for_each(question.answers.begin(), question.answers.end(),
                 [&rating_change, &question,
                  question_owner_rating_change](auto answer_item) {
                   int answer_owner_rating_change = 0;
                   if (answer_item.user == question.user) {
                     answer_owner_rating_change = question_owner_rating_change;
                   } else if (question.correct_answer_id == answer_item.id) {
                     answer_owner_rating_change =
                         COMMON_ANSWER_ACCEPTED_AS_CORRECT_REWARD -
                         ANSWER_ACCEPTED_AS_CORRECT_REWARD;
                     rating_change[question.user.value] +=
                         ACCEPT_COMMON_ANSWER_AS_CORRECT_REWARD -
                         ACCEPT_ANSWER_AS_CORRECT_REWARD;
                   }

                   for_each(
                       answer_item.history.begin(), answer_item.history.end(),
                       [&answer_owner_rating_change](auto history_item) {
                         if (history_item.is_flag_set(HISTORY_UPVOTED_FLG)) {
                           answer_owner_rating_change +=
                               COMMON_ANSWER_UPVOTED_REWARD -
                               ANSWER_UPVOTED_REWARD;
                         }
                       });
                   rating_change[answer_item.user.value] =
                       answer_owner_rating_change;
                 });
      });
  for (std::pair<uint64_t, int> user_rating_change : rating_change) {
    if (type == QUESTION_TYPE_GENERAL)
      update_rating(eosio::name(user_rating_change.first),
                    user_rating_change.second);
    else
      update_rating(eosio::name(user_rating_change.first),
                    -user_rating_change.second);
  }
}