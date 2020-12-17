#include "peeranha.hpp"
#include "peeranha_vote_hlp.hpp"

void peeranha::vote_forum_item(eosio::name user, uint64_t question_id,
                               uint16_t answer_id, bool is_upvote) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio::name target_user;
  int8_t target_user_rating_change;
  int8_t caller_rating_change;
  int8_t energy;
  int8_t within_15_minutes = 0;
  int8_t first_answer = 0;
  question_table.modify(
      iter_question, _self,
      [answer_id, is_upvote, iter_account, &target_user,
       &target_user_rating_change, &caller_rating_change,
       &energy, &within_15_minutes, &first_answer](auto &question) {
        auto vote_question_res = VoteItem::question;
        auto vote_answer_res = VoteItem::answer;
        switch (get_property_d(question.properties, PROPERTY_QUESTION_TYPE,
                               QUESTION_TYPE_EXPERT)) {
          case QUESTION_TYPE_GENERAL: {
            vote_question_res = VoteItem::common_question;
            vote_answer_res = VoteItem::common_answer;
          } break;
          default:
            break;
        }
        uint16_t community_id = question.community_id;
        if (apply_to_question(answer_id)) {
          target_user = question.user;
          if (is_upvote)
            upvote_item(question, iter_account, energy, caller_rating_change,
                        target_user_rating_change, vote_question_res, community_id);
          else
            downvote_item(question, iter_account, energy, caller_rating_change,
                          target_user_rating_change, vote_question_res, community_id);
        } else {
          auto iter_answer = find_answer(question, answer_id);
          target_user = iter_answer->user;
          if (is_upvote)
            upvote_item(*iter_answer, iter_account, energy,
                        caller_rating_change, target_user_rating_change,
                        vote_answer_res, community_id);
          else
            downvote_item(*iter_answer, iter_account, energy,
                          caller_rating_change, target_user_rating_change,
                          vote_answer_res, community_id);
        
          auto within_15_minutes_property = get_property_d(iter_answer->properties, PROPERTY_ANSWER_15_MINUTES, -2);
          if (iter_answer->rating >= 0 && within_15_minutes_property == 0) {
            target_user_rating_change += vote_answer_res.upvoted_reward;
            set_property(iter_answer->properties, PROPERTY_ANSWER_15_MINUTES, 1);
            within_15_minutes = 1;
          } else if (iter_answer->rating <= -1 && within_15_minutes_property == 1) {
            target_user_rating_change -= vote_answer_res.upvoted_reward;
            set_property(iter_answer->properties, PROPERTY_ANSWER_15_MINUTES, 0);
            within_15_minutes = -1;
          }

          auto firs_answer_property = get_property_d(iter_answer->properties, PROPERTY_FIRST_ANSWER, -2);
          if (iter_answer->rating >= 0 && firs_answer_property == 0) {
            target_user_rating_change += vote_answer_res.upvoted_reward;
            set_property(iter_answer->properties, PROPERTY_FIRST_ANSWER, 1);
            first_answer = 1;
          } else if (iter_answer->rating <= -1 && firs_answer_property == 1) {
            target_user_rating_change -= vote_answer_res.upvoted_reward;
            set_property(iter_answer->properties, PROPERTY_FIRST_ANSWER, 0);
            first_answer = -1;
          }
        }
      });
  auto iter_answer_account = find_account(target_user);
  int32_t sum_answer_15_minutes = 0;
  if (within_15_minutes) {
    sum_answer_15_minutes = get_property_d(iter_answer_account->integer_properties, PROPERTY_ANSWER_15_MINUTES, 0) + within_15_minutes;
    update_achievement(target_user, ANSWER_15_MINUTES, sum_answer_15_minutes);
  }
  int32_t sum_first_answer = 0;
  if (first_answer) {
    sum_first_answer = get_property_d(iter_answer_account->integer_properties, PROPERTY_FIRST_ANSWER, 0) + first_answer;
    update_achievement(target_user, FIRST_ANSWER, sum_first_answer);
  }

  update_rating(iter_account, caller_rating_change,
                [energy](auto &account) { 
                  account.reduce_energy(energy);
                });
  update_rating(iter_answer_account, caller_rating_change,
                [sum_answer_15_minutes, sum_first_answer](auto &account) { 
                  set_property(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, sum_answer_15_minutes);
                  set_property(account.integer_properties, PROPERTY_FIRST_ANSWER, sum_first_answer);
                });
  update_rating(target_user, target_user_rating_change);
}

void peeranha::report_forum_item(eosio::name user, uint64_t question_id,
                                 uint16_t answer_id, uint16_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  auto community_id = iter_question->community_id;
  int snitch_reduce_energy_value = ENERGY_REPORT_COMMENT;
  int user_rating_change = 0;
  // Remember old correct_answer_id to detect correct answer_deletion
  uint16_t old_correct_answer_id = iter_question->correct_answer_id;
  eosio::name item_user = eosio::name(0);
  // If this flag == true the question will erased
  bool delete_question = false;
  bool delete_answer = false;
  bool change_rating = false;
  bool within_15_minutes = false;
  bool first_answer = false;

  auto vote_question_res = VoteItem::question;
  auto vote_answer_res = VoteItem::answer;
  switch (get_property_d(iter_question->properties, PROPERTY_QUESTION_TYPE,
                         QUESTION_TYPE_EXPERT)) {
    case QUESTION_TYPE_GENERAL: {
      vote_question_res = VoteItem::common_question;
      vote_answer_res = VoteItem::common_answer;
    } break;
  }

  question_table.modify(
      iter_question, _self,
      [community_id ,&iter_account, answer_id, comment_id, &delete_question,
       &user_rating_change, &item_user, &delete_answer,
       &snitch_reduce_energy_value, &change_rating, vote_question_res,
       vote_answer_res, &within_15_minutes, &first_answer](auto &question) {
        if (apply_to_question(answer_id)) {
          if (apply_to_answer(comment_id)) {
            // Delete question
            // Question could not be deleted inside modify lambda
            // set_report_points_and_history - modify question
            snitch_reduce_energy_value = ENERGY_REPORT_QUESTION;
            delete_question = set_report_points_and_history(
                question, *iter_account, REPORT_POINTS_QUESTION, community_id);
            if (delete_question) {
              item_user = question.user;
              user_rating_change -= upvote_count(question.history) *
                                    vote_question_res.upvoted_reward;
              user_rating_change += QUESTION_DELETED_REWARD;
            }
          } else {
            // Delete comment to question by vote (answer_id == 0)
            auto iter_comment = find_comment(question, comment_id);

            if (set_report_points_and_history(*iter_comment, *iter_account,
                                              REPORT_POINTS_COMMENT, community_id)) {
              item_user = iter_comment->user;
              user_rating_change += COMMENT_DELETED_REWARD;
              question.comments.erase(iter_comment);
            }
          }
          return;
        }
        auto iter_answer = find_answer(question, answer_id);
        if (apply_to_answer(comment_id)) {
          // Delete answer to question by vote (comment_id == 0)
          snitch_reduce_energy_value = ENERGY_REPORT_ANSWER;
          if (set_report_points_and_history(*iter_answer, *iter_account,
                                            REPORT_POINTS_ANSWER, community_id)) {
            // Get for mark as correct
            item_user = iter_answer->user;
            if (question.correct_answer_id == iter_answer->id) {
              int rating_correct_answer = vote_answer_res.correct_answer;
              
              if (iter_answer->user == question.user) {
                rating_correct_answer = 0;
                change_rating = true;
              }
              user_rating_change -= rating_correct_answer;
              question.correct_answer_id = EMPTY_ANSWER_ID;
            }
            user_rating_change -= upvote_count(iter_answer->history) *
                                  vote_answer_res.upvoted_reward;
            user_rating_change += ANSWER_DELETED_REWARD;

            auto within_15_minutes_property = get_property_d(iter_answer->properties, PROPERTY_ANSWER_15_MINUTES, -1);
            if (within_15_minutes_property == 1) {
              user_rating_change -= vote_answer_res.answer_15_minutes;
              within_15_minutes = true;
            }
            auto first_answer_property = get_property_d(iter_answer->properties, PROPERTY_FIRST_ANSWER, -1);
            if (first_answer_property == 1) {
              user_rating_change -= vote_answer_res.first_answer;
              first_answer = true;
            }

            question.answers.erase(iter_answer);
            delete_answer = true;
          }

        } else {
          // Delete comment to answer
          auto iter_comment = find_comment(*iter_answer, comment_id);
          if (set_report_points_and_history(*iter_comment, *iter_account,
                                            REPORT_POINTS_COMMENT, community_id)) {
            item_user = iter_comment->user;
            user_rating_change += COMMENT_DELETED_REWARD;
            iter_answer->comments.erase(iter_comment);
          }
        }
      });
  bool is_correct_answer_deleted = false;
  if (delete_answer) {
#ifdef SUPERFLUOUS_INDEX
    remove_user_answer(item_user, iter_question->id);
#endif
    is_correct_answer_deleted =
        iter_question->correct_answer_id != old_correct_answer_id;
    if (is_correct_answer_deleted) {
      int rating_correct_answer = vote_question_res.correct_answer;
      if (change_rating)
          rating_correct_answer = 0;
      update_rating(iter_question->user, -rating_correct_answer);
    }
    update_community_statistics(iter_question->community_id, 0, -1,
                                is_correct_answer_deleted ? -1 : 0, 0);
  }

  if (delete_question) {
    update_community_statistics(
        iter_question->community_id, -1, 0 - (int)iter_question->answers.size(),
        iter_question->correct_answer_id == EMPTY_ANSWER_ID ? 0 : -1, 0);
    update_tags_statistics(iter_question->community_id, iter_question->tags,
                           -1);
#ifdef SUPERFLUOUS_INDEX
    remove_user_question(iter_question->user, iter_question->id);
#endif
    if (iter_question->correct_answer_id != EMPTY_ANSWER_ID) {

      int rating_correct_answer = vote_question_res.correct_answer;
      auto iter_answer = binary_find(iter_question->answers.begin(), iter_question->answers.end(), iter_question->correct_answer_id);
      if (iter_answer->user == iter_question->user )
        rating_correct_answer = 0;
      user_rating_change -= rating_correct_answer;
    }
    for (auto answer = iter_question->answers.begin();
         answer != iter_question->answers.end(); answer++) {
      int rating_change = 0;
      rating_change -=
          upvote_count(answer->history) * vote_answer_res.upvoted_reward;
      bool is_correct_answer = false;
      if (answer->id == iter_question->correct_answer_id) {
        int rating_correct_answer = vote_answer_res.correct_answer;
        if (answer->user == iter_question->user )
          rating_correct_answer = 0;
        rating_change -= rating_correct_answer;   
        is_correct_answer = true;
      }

      auto within_15_minutes_user = get_property_d(answer->properties, PROPERTY_ANSWER_15_MINUTES, -1);
      if (within_15_minutes_user == 1) {
        rating_change -= vote_answer_res.answer_15_minutes;
      }

      auto first_answer_property = get_property_d(answer->properties, PROPERTY_FIRST_ANSWER, -1);
      if (first_answer_property == 1) {
        rating_change -= vote_answer_res.first_answer;
      }
      
      update_rating(answer->user, rating_change,
                    [is_correct_answer, within_15_minutes_user, first_answer_property](auto &account) {
                      account.answers_given -= 1;
                      if (is_correct_answer) account.correct_answers -= 1;
                      if (within_15_minutes_user) {
                        int32_t sum_answer_15_minutes = get_property_d(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, 1) - 1;
                        set_property(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, sum_answer_15_minutes);
                      } 
                      if (first_answer_property) {
                        int32_t sum_first_answer = get_property_d(account.integer_properties, PROPERTY_FIRST_ANSWER, 1) - 1;
                        set_property(account.integer_properties, PROPERTY_FIRST_ANSWER, sum_first_answer);
                      }
                    });

#ifdef SUPERFLUOUS_INDEX
      remove_user_answer(answer->user, iter_question->id);
#endif
    }
    question_table.erase(iter_question);
    eosio::check(iter_question != question_table.end(),
                 "Address not erased properly");
  }
  // user_rating_change = 0 also means that item_user was not found
  if (item_user.value != 0) {
    update_rating(item_user, user_rating_change,
                  [delete_question, delete_answer,
                   is_correct_answer_deleted](auto &account) {
                    if (delete_question) {
                      account.questions_asked -= 1;
                    } else if (delete_answer) {
                      account.answers_given -= 1;
                      if (is_correct_answer_deleted)
                        account.correct_answers -= 1;
                    }
                  });
  }

  update_rating(iter_account, [snitch_reduce_energy_value, within_15_minutes, first_answer](auto &account) {
    account.reduce_energy(snitch_reduce_energy_value);
    if (within_15_minutes) {
      int32_t sum_answer_15_minutes = get_property_d(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, 1) - 1;
      set_property(account.integer_properties, PROPERTY_ANSWER_15_MINUTES, sum_answer_15_minutes);
    }
    if (first_answer) {
      int32_t sum_first_answer = get_property_d(account.integer_properties, PROPERTY_FIRST_ANSWER, 1) - 1;
      set_property(account.integer_properties, PROPERTY_FIRST_ANSWER, sum_first_answer);
    }
  });
}