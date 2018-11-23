#pragma once
#include <eosiolib/name.hpp>
/*
1 - Stranger - 0
100 - Newbie - 1
500 - Junior Resident - 5
1000 - Resident - 10
2500 - Senior Resident - 25
5000 - Hero Resident - 50
10000 - Legendary Resident - 100
*/
uint8_t status_moderation_points(int16_t rating) {
  if (rating < 100) return 0;
  switch (rating) {
    case 100 ... 499:
      return 1;
    case 500 ... 999:
      return 5;
    case 1000 ... 2499:
      return 10;
    case 2500 ... 4999:
      return 25;
    case 5000 ... 9999:
      return 50;
    default:
      return 100;
  }
}

uint8_t status_question_limit(int16_t rating) {
  if (rating < 0) return 0;
  switch (rating) {
    case 0 ... 99:
      return 3;
    case 100 ... 499:
      return 5;
    case 500 ... 999:
      return 6;
    case 1000 ... 2499:
      return 7;
    case 2500 ... 4999:
      return 8;
    case 5000 ... 9999:
      return 9;
    default:
      return 10;
  }
}

/*
Comments are limited only for commenting other users questions. Limits are within one a single question.
1 - Stranger - 6
100 - Newbie - 10
500 - Junior Resident - 14
1000 - Resident - 18
2500 - Senior Resident - 22
5000 - Hero Resident - 26
10000 - Legendary Resident - 30
*/
uint8_t status_comments_limit(int16_t rating) {
  if (rating < 0) return 0;
  switch (rating) {
    case 0 ... 99:
      return 6;
    case 100 ... 499:
      return 10;
    case 500 ... 999:
      return 14;
    case 1000 ... 2499:
      return 18;
    case 2500 ... 4999:
      return 22;
    case 5000 ... 9999:
      return 26;
    default:
      return 30;
  }
}