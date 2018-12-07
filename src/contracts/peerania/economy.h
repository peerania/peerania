#pragma once
#include <eosiolib/name.hpp>
#include "peerania_types.h"
// Limit to delte
namespace DeletionVotes {
const int DELETION_VOTES_QUESTION = 1700;
const int DELETION_VOTES_ANSWER = 1500;
const int DELETION_VOTES_COMMENT = 1000;
}  // namespace DeletionVotes

namespace TagsAndCommunities {
const int VOTES_TO_CREATE_COMMUNITY = 40000;
const int VOTES_TO_DELETE_COMMUNITY = -2000;
const int VOTES_TO_CREATE_TAG = 10000;
const int VOTES_TO_DELETE_TAG = -500;
}  // namespace TagsAndCommunities

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
#define MAX_RATING 32767
#define RATING_ON_CREATE 10

#define POST_QUESTION_ALLOWED 0
#define POST_ANSWER_OWN_ALLOWED 0
#define POST_ANSWER_ALLOWED 10
#define POST_COMMENT_OWN_ALLOWED 0
#define POST_COMMENT_ALLOWED 35
#define UPVOTE_ALLOWED 35
#define DOWNVOTE_ALLOWED 100
#define VOTE_FOR_DELETION_ALLOWED 100

#define CREATE_TAG_ALLOWED 500
#define CREATE_COMMUNITY_ALLOWED 2500
#define VOTE_CREATE_TAG_ALLOWED 35
#define VOTE_CREATE_COMMUNITY_ALLOWED 100
#define VOTE_DELETE_TAG_ALLOWED 35
#define VOTE_DELETE_COMMUNITY_ALLOWED 100


#define MODERATION_POINTS_PER_TAG 3
#define MODERATION_POINTS_PER_COMMUNITY 5

#define TAG_CREATED_REWARD 75
#define TAG_DELETED_REWARD -50

#define COMMUNITY_CREATED_REWARD 200
#define COMMUNITY_DELETED_REWARD -150




#ifdef DEBUG
struct [[eosio::table("constants")]] constants {
  uint64_t id;
  time start_period_time;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<"constants"_n, constants> constants_index;
const uint64_t scope_all_constants = "allconstants"_n.value;
#endif