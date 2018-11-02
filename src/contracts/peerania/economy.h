#pragma once
#include <eosiolib/types.hpp>

// Limit to delte
namespace DeletionVotes {
const int DELETION_VOTES_QUESTION = 1700;
const int DELETION_VOTES_ANSWER = 1500;
const int DELETION_VOTES_COMMENT = 1000;
}  // namespace DeletionVotes

#define POST_QUESTION_REWARD 0
#define POST_ANSWER_REWARD 0
#define POST_COMMENT_REWARD 0
#define DELETE_OWN_QUESTION_REWARD -10
#define DELETE_OWN_ANSWER_REWARD -5
#define DELETE_OWN_COMMENT_REWARD 0
#define ACCEPT_ANSWER_AS_CORRECT_REWARD 2
#define UPVOTE_QUESTION_REWARD 0
#define DOWNVOTE_QUESTION_REWARD -1
#define UPVOTE_ANSWER_REWARD 0
#define DOWNVOTE_ANSWER_REWARD -1
#define VOTE_TO_DELETE_QUESTION_REWARD 0
#define VOTE_TO_DELETE_ANSWER_REWARD 0

#define QUESTION_UPVOTED_REWARD 5
#define ANSWER_UPVOTED_REWARD 10
#define ANSWER_ACCEPTED_AS_CORRECT_REWARD 15
#define QUESTION_DOWNVOTED_REWARD -2
#define ANSWER_DOWNVOTED_REWARD -2

#define QUESTION_DELETED_REWARD -15
#define ANSWER_DELETED_REWARD -10
#define COMMENT_DELETED_REWARD -5

#define MIN_RATING -100
#define RATING_ON_CREATE 10

#define POST_QUESTION_ALLOWED 0
#define POST_ANSWER_OWN_ALLOWED 0
#define POST_ANSWER_ALLOWED 10
#define POST_COMMENT_OWN_ALLOWED 0
#define POST_COMMENT_ALLOWED 30
#define UPVOTE_ALLOWED 35
#define DOWNVOTE_ALLOWED 100
#define VOTE_FOR_DELETION_ALLOWED 100

#ifdef DEBUG
struct [[eosio::table("constants")]] constants {
  uint64_t id;
  time start_period_time;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<N(constants), constants> constants_index;
const scope_name all_constants = N(allconstants);
#endif