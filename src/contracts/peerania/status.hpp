#pragma once
#include <eosiolib/name.hpp>
#include "economy.h"
/*
1 - Stranger - 0
100 - Newbie - 1
500 - Junior Resident - 5
1000 - Resident - 10
2500 - Senior Resident - 25
5000 - Hero Resident - 50
10000 - Legendary Resident - 100
*/

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


uint8_t status_moderation_points(int rating) {
  if (rating < 100) return 0;
  switch (rating) {
    STATUS1(STATUS1_MODERATION_POINTS);
    STATUS2(STATUS2_MODERATION_POINTS);
    STATUS3(STATUS3_MODERATION_POINTS);
    STATUS4(STATUS4_MODERATION_POINTS);
    STATUS5(STATUS5_MODERATION_POINTS);
    STATUS6(STATUS6_MODERATION_POINTS);
  }
}

uint8_t status_question_limit(int rating) {
  if (rating < 0) return 0;
  switch (rating) {
    STATUS0(STATUS0_QUESTION_LIMIT);
    STATUS1(STATUS1_QUESTION_LIMIT);
    STATUS2(STATUS2_QUESTION_LIMIT);
    STATUS3(STATUS3_QUESTION_LIMIT);
    STATUS4(STATUS4_QUESTION_LIMIT);
    STATUS5(STATUS5_QUESTION_LIMIT);
    STATUS6(STATUS6_QUESTION_LIMIT);
  }
}


/*
Comments are limited only for commenting other users questions. Limits are
within one a single question. 1 - Stranger - 6 100 - Newbie - 10 500 - Junior
Resident - 14 1000 - Resident - 18 2500 - Senior Resident - 22 5000 - Hero
Resident - 26 10000 - Legendary Resident - 30
*/
uint8_t status_comments_limit(int16_t rating) {
  if (rating < 0) return 0;
  switch (rating) {
    STATUS0(STATUS0_COMMENT_LIMIT);
    STATUS1(STATUS1_COMMENT_LIMIT);
    STATUS2(STATUS2_COMMENT_LIMIT);
    STATUS3(STATUS3_COMMENT_LIMIT);
    STATUS4(STATUS4_COMMENT_LIMIT);
    STATUS5(STATUS5_COMMENT_LIMIT);
    STATUS6(STATUS6_COMMENT_LIMIT);
  }
}