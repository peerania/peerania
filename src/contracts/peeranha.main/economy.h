#pragma once
#include <eosio/name.hpp>

// Limit to delte
#if STAGE == 1
#define REPORT_POINTS_QUESTION 7
#define REPORT_POINTS_ANSWER 5
#define REPORT_POINTS_COMMENT 3
#else
#define REPORT_POINTS_QUESTION 150
#define REPORT_POINTS_ANSWER 125
#define REPORT_POINTS_COMMENT 50
#endif


#define ANSWER_ACCEPTED_AS_CORRECT_REWARD 15
#define UPVOTE_QUESTION_REWARD 0
#define DOWNVOTE_QUESTION_REWARD -1
#define UPVOTE_ANSWER_REWARD 0
#define DOWNVOTE_ANSWER_REWARD -1
#define QUESTION_UPVOTED_REWARD 5
#define ANSWER_UPVOTED_REWARD 10
#define QUESTION_DOWNVOTED_REWARD -2
#define ANSWER_DOWNVOTED_REWARD -2

// Stub solution
#if STAGE == 1

#define VOTES_TO_CREATE_COMMUNITY 4
#define VOTES_TO_DELETE_COMMUNITY -3
#define VOTES_TO_CREATE_TAG 3
#define VOTES_TO_DELETE_TAG -2

#else

#define VOTES_TO_CREATE_COMMUNITY 100
#define VOTES_TO_DELETE_COMMUNITY -35
#define VOTES_TO_CREATE_TAG 10
#define VOTES_TO_DELETE_TAG -10

#endif


#define POST_QUESTION_REWARD 0
#define POST_ANSWER_REWARD 0
#define POST_COMMENT_REWARD 0
#define DELETE_OWN_QUESTION_REWARD -2
#define DELETE_OWN_ANSWER_REWARD -2
#define DELETE_OWN_COMMENT_REWARD 0
#define ACCEPT_ANSWER_AS_CORRECT_REWARD 2
#define VOTE_TO_DELETE_QUESTION_REWARD 0
#define VOTE_TO_DELETE_ANSWER_REWARD 0

#define QUESTION_DELETED_REWARD -5
#define ANSWER_DELETED_REWARD -5
#define COMMENT_DELETED_REWARD -2

#define MIN_RATING -100
#define MAX_RATING 2000000000
#define RATING_ON_CREATE 10

#define POST_QUESTION_ALLOWED 0
#define POST_ANSWER_OWN_ALLOWED 0
#define POST_ANSWER_ALLOWED 0
#define POST_COMMENT_OWN_ALLOWED 0
#define POST_COMMENT_ALLOWED 35
#define UPVOTE_ALLOWED 35
#define DOWNVOTE_ALLOWED 100
#define VOTE_FOR_DELETION_ALLOWED 100


#define CREATE_TAG_ALLOWED 100
#define CREATE_COMMUNITY_ALLOWED 500
#define VOTE_CREATE_TAG_ALLOWED 35
#define VOTE_CREATE_COMMUNITY_ALLOWED 100
#define VOTE_DELETE_TAG_ALLOWED 35
#define VOTE_DELETE_COMMUNITY_ALLOWED 100
#define REPORT_PROFILE_ALLOWED 50

#define TAG_CREATED_REWARD 75
#define TAG_DELETED_REWARD -50

#define COMMUNITY_CREATED_REWARD 200
#define COMMUNITY_DELETED_REWARD -150

// Energy
#define ENERGY_DOWNVOTE_QUESTION 5
#define ENERGY_DOWNVOTE_ANSWER 3
#define ENERGY_UPVOTE_QUESTION 1
#define ENERGY_UPVOTE_ANSWER 1
#define ENERGY_FORUM_VOTE_CHANGE 1
#define ENERGY_POST_QUESTION 10
#define ENERGY_POST_ANSWER 6
#define ENERGY_POST_COMMENT 4
#define ENERGY_MODIFY_QUESTION 2
#define ENERGY_MODIFY_ANSWER 2
#define ENERGY_MODIFY_COMMENT 1
#define ENERGY_DELETE_QUESTION 2
#define ENERGY_DELETE_ANSWER 2
#define ENERGY_DELETE_COMMENT 1
#define ENERGY_MARK_ANSWER_AS_CORRECT 1
#define ENERGY_UPDATE_PROFILE 1
#define ENERGY_CREATE_TAG 75
#define ENERGY_CREATE_COMMUNITY 125
#define ENERGY_VOTE_COMMUNITY 1
#define ENERGY_VOTE_TAG 1
#define ENERGY_FOLLOW_COMMUNITY 1
#define ENERGY_REPORT_PROFILE 5
#define ENERGY_REPORT_QUESTION 3
#define ENERGY_REPORT_ANSWER 2
#define ENERGY_REPORT_COMMENT 1

#define STATUS0_ENERGY 300
#define STATUS1_ENERGY 600
#define STATUS2_ENERGY 900
#define STATUS3_ENERGY 1200
#define STATUS4_ENERGY 1500
#define STATUS5_ENERGY 1800
#define STATUS6_ENERGY 2100


#if STAGE==1 

// Account period
#define ACCOUNT_STAT_RESET_PERIOD 1800 // 30 Minutes
#define BAN_RATING_INCREMENT_PER_PERIOD 6

// Account report reset time
#define MIN_FREEZE_PERIOD 7200           // 2 hour
#define REPORT_RESET_PERIOD 7200         // 2 hour
#define REPORT_POWER_RESET_PERIOD 14400  // 4 hour

#define POINTS_TO_FREEZE 9
#define MODERATION_POINTS_REPORT_PROFILE 2
#define MAX_FREEZE_PERIOD_MULTIPLIER 6

#else

// Account period
#define ACCOUNT_STAT_RESET_PERIOD 259200 // 3 Days
#define BAN_RATING_INCREMENT_PER_PERIOD 6

// Account report reset time
#define MIN_FREEZE_PERIOD 302400           // 3.5 Days
#define REPORT_RESET_PERIOD 2592000        // 30 Days
#define REPORT_POWER_RESET_PERIOD 10368000 // 120 Days

#define POINTS_TO_FREEZE 90
#define MODERATION_POINTS_REPORT_PROFILE 2
#define MAX_FREEZE_PERIOD_MULTIPLIER 6

#endif

namespace VoteItem
{
struct vote_resources_t
{
  const int upvote_reward;
  const int downvote_reward;
  const int upvoted_reward;
  const int downvoted_reward;
  const int energy_upvote;
  const int energy_downvote;
};

const vote_resources_t question = {
    .upvote_reward = UPVOTE_QUESTION_REWARD,
    .downvote_reward = DOWNVOTE_QUESTION_REWARD,
    .upvoted_reward = QUESTION_UPVOTED_REWARD,
    .downvoted_reward = QUESTION_DOWNVOTED_REWARD,
    .energy_upvote = ENERGY_UPVOTE_QUESTION,
    .energy_downvote = ENERGY_DOWNVOTE_QUESTION,
};

const vote_resources_t answer = {
    .upvote_reward = UPVOTE_ANSWER_REWARD,
    .downvote_reward = DOWNVOTE_ANSWER_REWARD,
    .upvoted_reward = ANSWER_UPVOTED_REWARD,
    .downvoted_reward = ANSWER_DOWNVOTED_REWARD,
    .energy_upvote = ENERGY_UPVOTE_ANSWER,
    .energy_downvote = ENERGY_DOWNVOTE_ANSWER,
};
} // namespace VoteItem

// Status 

#define STATUS0(X) \
  case 0 ... 99:   \
    return (X)
#define STATUS1(X)  \
  case 100 ... 499: \
    return (X)
#define STATUS2(X)  \
  case 500 ... 999: \
    return (X)
#define STATUS3(X)    \
  case 1000 ... 2499: \
    return (X)
#define STATUS4(X)    \
  case 2500 ... 4999: \
    return (X)
#define STATUS5(X)    \
  case 5000 ... 9999: \
    return (X)
#define STATUS6(X) \
  default:         \
    return (X)
