#pragma once

#define PROPERTY_MODERATOR_FLAGS 48
#define MODERATOR_FLG_INFINITE_ENERGY (1 << 0)
#define MODERATOR_FLG_INFINITE_IMPACT (1 << 1)
#define MODERATOR_FLG_IGNORE_RATING (1 << 2)
#define MODERATOR_FLG_CREATE_COMMUNITY (1 << 3)
#define MODERATOR_FLG_CREATE_TAG (1 << 4)
#define MODERATOR_FLG_CHANGE_QUESTION_STATUS (1 << 5)

#define COMMUNITY_ADMIN_FLG_INFINITE_ENERGY (1 << 0)
#define COMMUNITY_ADMIN_FLG_INFINITE_IMPACT (1 << 1)
#define COMMUNITY_ADMIN_FLG_IGNORE_RATING (1 << 2)
#define COMMUNITY_ADMIN_FLG_CREATE_TAG (1 << 4)
#define COMMUNITY_ADMIN_FLG_CHANGE_QUESTION_STATUS (1 << 5)
#define COMMUNITY_ADMIN_FLG_CHANGE_TOP_QUESTION (1 << 6)
#define COMMUNITY_ADMIN_FLG_OFFICIAL_ANSWER  (1 << 7)

#define ALL_COMMUNITY_ADMIN_FLG 255

#define MODERATION_IMPACT_INFINITE 255

#define PROPERTY_EMPTY_ACCOUNT 15

#if STAGE == 1
#define MODERATION_AVAILABLE_PERIOD 31536000 // 8 week
#else
#define MODERATION_AVAILABLE_PERIOD 31536000  // One year
#endif

#if STAGE == 1
#define TIME_15_MINUTES 900 // 15 seconds
#else
#define TIME_15_MINUTES 900  // 15 minutes
#endif

#define MULTIPLICATION_TOTAL_RATING 1000     // value for boost
#define MAX_MULTIPLICATION_TOTAL_RATING 3000 //

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

#define STATUS0_ENERGY 300
#define STATUS1_ENERGY 600
#define STATUS2_ENERGY 900
#define STATUS3_ENERGY 1200
#define STATUS4_ENERGY 1500
#define STATUS5_ENERGY 1800
#define STATUS6_ENERGY 2100

#define BAN_RATING_INCREMENT_PER_PERIOD 6
#define MAX_FREEZE_PERIOD_MULTIPLIER 6

enum Bounty_status { 
  ACTIVE = 1, 
  PAID, 
  PENDING, 
  DELETED 
};

#if STAGE == 1 
// Account period
#define ACCOUNT_STAT_RESET_PERIOD 1800 // 30 Minutes

// Account report reset time
#define MIN_FREEZE_PERIOD 7200           // 2 hour
#define REPORT_RESET_PERIOD 7200         // 2 hour
#define REPORT_POWER_RESET_PERIOD 14400  // 4 hour
#define POINTS_TO_FREEZE 9

#define MODERATION_POINTS_REPORT_PROFILE 2

#elif STAGE == 2
#define ACCOUNT_STAT_RESET_PERIOD 3  // 3 sec

#define MIN_FREEZE_PERIOD 3
#define REPORT_RESET_PERIOD 2
#define REPORT_POWER_RESET_PERIOD 4
#define POINTS_TO_FREEZE 10

#define MODERATION_POINTS_REPORT_PROFILE 2
#else

// Account period
#define ACCOUNT_STAT_RESET_PERIOD 259200 // 3 Days

// Account report reset time
#define MIN_FREEZE_PERIOD 302400           // 3.5 Days
#define REPORT_RESET_PERIOD 2592000        // 30 Days
#define REPORT_POWER_RESET_PERIOD 10368000 // 120 Days

#define POINTS_TO_FREEZE 90
#define MODERATION_POINTS_REPORT_PROFILE 2
#endif