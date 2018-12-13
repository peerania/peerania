#include "peerania.hpp"
#include "peerania_vote_hlp.hpp"

void peerania::vote_forum_item(eosio::name user, uint64_t question_id, uint16_t answer_id,
                    bool is_upvote) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);
  eosio::name item_owner;
  int8_t owner_rating_change;
  int8_t caller_rating_change;
  question_table.modify(
      iter_question, _self,
      [answer_id, is_upvote, iter_account, &item_owner, &owner_rating_change,
       &caller_rating_change](auto &question) {
        if (apply_to_question(answer_id)) {
          if (is_upvote)
            upvote_item(question, iter_account, item_owner, owner_rating_change,
                        caller_rating_change, QUESTION_UPVOTED_REWARD,
                        UPVOTE_QUESTION_REWARD, QUESTION_DOWNVOTED_REWARD,
                        DOWNVOTE_QUESTION_REWARD);
          else
            downvote_item(question, iter_account, item_owner,
                          owner_rating_change, caller_rating_change,
                          QUESTION_UPVOTED_REWARD, UPVOTE_QUESTION_REWARD,
                          QUESTION_DOWNVOTED_REWARD, DOWNVOTE_QUESTION_REWARD);
        } else {
          auto itr_answer = find_answer(question, answer_id);
          if (is_upvote)
            upvote_item(*itr_answer, iter_account, item_owner,
                        owner_rating_change, caller_rating_change,
                        ANSWER_UPVOTED_REWARD, UPVOTE_ANSWER_REWARD,
                        ANSWER_DOWNVOTED_REWARD, DOWNVOTE_ANSWER_REWARD);
          else
            downvote_item(*itr_answer, iter_account, item_owner,
                          owner_rating_change, caller_rating_change,
                          ANSWER_UPVOTED_REWARD, UPVOTE_ANSWER_REWARD,
                          ANSWER_DOWNVOTED_REWARD, DOWNVOTE_ANSWER_REWARD);
        }
      });
  update_rating(iter_account, caller_rating_change);
  update_rating(item_owner, owner_rating_change);
}

void peerania::vote_for_deletion(eosio::name user, uint64_t question_id,
                                 uint16_t answer_id, uint16_t comment_id) {
  auto iter_account = find_account(user);
  auto iter_question = find_question(question_id);

  //How to move it to the end?
  account_table.modify(iter_account, _self, [](auto &account) {
    account.update();
    eosio_assert(account.moderation_points > 0, "Not enought moderation point");
    account.moderation_points -= 1;
  });

  int owner_rating_change = 0;
  // Remember old correct_answer_id to detect correct answer_deletion
  uint16_t old_correct_answer_id = iter_question->correct_answer_id;
  eosio::name item_owner;
  // If this flag == true the question will erased
  bool delete_question = false;
  bool delete_answer = false;
  question_table.modify(
      iter_question, _self,
      [&iter_account, answer_id, comment_id, &delete_question,
       &owner_rating_change, &item_owner, &delete_answer](auto &question) {
        if (apply_to_question(answer_id)) {
          if (apply_to_answer(comment_id)) {
            // Delete question
            // Question could not be deleted inside modify lambda
            // set_deletion_votes_and_history - modify question
            delete_question =
                set_deletion_votes_and_history(question, *iter_account,
                                        DeletionVotes::DELETION_VOTES_QUESTION);
            if (delete_question) {
              item_owner = question.user;
              owner_rating_change -=
                  upvote_count(question.history) * QUESTION_UPVOTED_REWARD;
              owner_rating_change += QUESTION_DELETED_REWARD;
            }
          } else {
            // Delete comment to question by vote (answer_id == 0)
            auto iter_comment = find_comment(question, comment_id);

            if (set_deletion_votes_and_history(
                    *iter_comment, *iter_account,
                    DeletionVotes::DELETION_VOTES_COMMENT)) {
              item_owner = iter_comment->user;
              owner_rating_change += COMMENT_DELETED_REWARD;
              question.comments.erase(iter_comment);
            }
          }
          return;
        }
        auto iter_answer = find_answer(question, answer_id);
        if (apply_to_answer(comment_id)) {
          // Delete answer to question by vote (comment_id == 0)
          if (set_deletion_votes_and_history(*iter_answer, *iter_account,
                                      DeletionVotes::DELETION_VOTES_ANSWER)) {
            // Get for mark as correct
            item_owner = iter_answer->user;
            if (question.correct_answer_id == iter_answer->id) {
              owner_rating_change -= ANSWER_ACCEPTED_AS_CORRECT_REWARD;
              question.correct_answer_id = EMPTY_ANSWER_ID;
            }
            owner_rating_change -=
                upvote_count(iter_answer->history) * ANSWER_UPVOTED_REWARD;
            owner_rating_change += ANSWER_DELETED_REWARD;
            question.answers.erase(iter_answer);
            delete_answer = true;
          }
          
        } else {
          // Delete comment to answer
          auto iter_comment = find_comment(*iter_answer, comment_id);
          if (set_deletion_votes_and_history(*iter_comment, *iter_account,
                                      DeletionVotes::DELETION_VOTES_COMMENT)) {
            item_owner = iter_comment->user;
            owner_rating_change += COMMENT_DELETED_REWARD;
            iter_answer->comments.erase(iter_comment);
          }
        }
      });

  // Means that answer, marked as correct was deleted
  if (iter_question->correct_answer_id != old_correct_answer_id) {
    update_rating(iter_question->user, -ACCEPT_ANSWER_AS_CORRECT_REWARD);
  }
  if(delete_answer){
    remove_user_question_or_answer(item_owner, iter_question->id, false);
  }

  if (delete_question) {
    update_popularity(iter_question->community_id, iter_question->tags, false);
    remove_user_question_or_answer(iter_question->user, iter_question->id, true);
    if (iter_question->correct_answer_id != EMPTY_ANSWER_ID)
      owner_rating_change -= ACCEPT_ANSWER_AS_CORRECT_REWARD;
    for (auto answer = iter_question->answers.begin();
         answer != iter_question->answers.end(); answer++) {
      int rating_change = 0;
      rating_change -= upvote_count(answer->history) * ANSWER_UPVOTED_REWARD;
      if (answer->id == iter_question->correct_answer_id)
        rating_change -= ANSWER_ACCEPTED_AS_CORRECT_REWARD;
      update_rating(answer->user, rating_change);
      remove_user_question_or_answer(answer->user, iter_question->id, false);
    }
    question_table.erase(iter_question);
    eosio_assert(iter_question != question_table.end(),
                 "Address not erased properly");
  }
  //owner_rating_change = 0 also means that item_owner was not found
  if(owner_rating_change != 0)
    update_rating(item_owner, owner_rating_change);
}