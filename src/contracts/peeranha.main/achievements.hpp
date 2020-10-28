#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <map>

#define COMMON_VALUE 50000

#define RATING_NEWBIE 100
#define RATING_JUNIOR 500
#define RATING_RESIDENT 1000
#define RATING_SENIOR 2500
#define RATING_HERO 5000
#define RATING_SUPERHERO 10000


#define TEST_BRONZE_QUESTION 2
#define TEST_SILVER_QUESTION 5
#define TEST_GOLD_QUESTION 10

#define TEST_BRONZE_ANSWER 2
#define TEST_SILVER_ANSWER 5
#define TEST_GOLD_ANSWER 10

#define TEST_BRONZE_CORRECT 1
#define TEST_SILVER_CORRECT 3
#define TEST_GOLD_CORRECT 5

#define TEST_BRONZE_15_MINUTES 1
#define TEST_SILVER_15_MINUTES 3
#define TEST_GOLD_15_MINUTEST 5

#define TEST_BRONZE_FIRST_ANSWER 1
#define TEST_SILVER_FIRST_ANSWER 3
#define TEST_GOLD_FIRST_ANSWER 5


enum Achievements { QUESTION_BRONZE = 1,
                    QUESTION_SILVER,
                    QUESTION_GOLD,

                    ANSWER_BRONZE = 10,
                    ANSWER_SILVER,
                    ANSWER_GOLD,

                    CORRECT_ANSWER_BRONZE = 20,
                    CORRECT_ANSWER_SILVER,
                    CORRECT_ANSWER_GOLD,

                    FIRST_10K_REGISTERED = 30, 
                    LIMITED_NEWBIE, 
                    LIMITED_JUNIOR, 
                    LIMITED_RESIDENT, 
                    LIMITED_SENIOR, 
                    LIMITED_HERO, 
                    LIMITED_SUPERHERO,

                    USER_REGISTERED = 40, 
                    COMMON_NEWBIE, 
                    COMMON_JUNIOR, 
                    COMMON_RESIDENT, 
                    COMMON_SENIOR, 
                    COMMON_HERO, 
                    COMMON_SUPERHERO,

                    ANSWER_15_MINUTES_BRONZE = 50,
                    ANSWER_15_MINUTES_SILVER,
                    ANSWER_15_MINUTES_GOLD,

                    FIRST_ANSWER_BRONZE = 60,
                    FIRST_ANSWER_SILVER,
                    FIRST_ANSWER_GOLD,
                  };

enum Type_achievement { LIMITED_EDITION = 0, COMMON };
enum Group_achievement { QUESTION = 0, ANSWER, CORRECT_ANSWER, REGISTERED, RATING, ANSWER_15_MINUTES, FIRST_ANSWER};

struct achievement {
  achievement(uint32_t community_id, uint64_t limit, uint64_t lower_bound, Type_achievement type, Group_achievement group) :
    community_id(community_id), 
    limit(limit),
    lower_bound(lower_bound),
    type(type),
    group(group)
  {}

  const std::string name;
  const uint32_t community_id;                        //0 - for all
  const uint64_t limit;
  const uint64_t lower_bound;
  const Type_achievement type;                        //uniqe -false | level = true
  const Group_achievement group;
};

#if STAGE == 1 || STAGE == 2
  std::map<uint32_t, achievement> achievements = {
    { QUESTION_BRONZE,              achievement(0, COMMON_VALUE, TEST_BRONZE_QUESTION, LIMITED_EDITION, QUESTION) },
    { QUESTION_SILVER,              achievement(0, COMMON_VALUE, TEST_SILVER_QUESTION, LIMITED_EDITION, QUESTION) },
    { QUESTION_GOLD,                achievement(0, COMMON_VALUE, TEST_GOLD_QUESTION, LIMITED_EDITION, QUESTION) },

    { ANSWER_BRONZE,                achievement(0, COMMON_VALUE, TEST_BRONZE_ANSWER, LIMITED_EDITION, ANSWER) },
    { ANSWER_SILVER,                achievement(0, COMMON_VALUE, TEST_SILVER_ANSWER, LIMITED_EDITION, ANSWER) },
    { ANSWER_GOLD,                  achievement(0, COMMON_VALUE, TEST_GOLD_ANSWER, LIMITED_EDITION, ANSWER) },

    { CORRECT_ANSWER_BRONZE,        achievement(0, COMMON_VALUE, TEST_BRONZE_CORRECT, LIMITED_EDITION, CORRECT_ANSWER) },
    { CORRECT_ANSWER_SILVER,        achievement(0, COMMON_VALUE, TEST_SILVER_CORRECT, LIMITED_EDITION, CORRECT_ANSWER) },
    { CORRECT_ANSWER_GOLD,          achievement(0, COMMON_VALUE, TEST_GOLD_CORRECT, LIMITED_EDITION, CORRECT_ANSWER) },

    { FIRST_10K_REGISTERED,         achievement(0, 10000, 1, LIMITED_EDITION, REGISTERED) },
    { LIMITED_NEWBIE,               achievement(0, 700, RATING_NEWBIE, LIMITED_EDITION, RATING) },
    { LIMITED_JUNIOR,               achievement(0, 500, RATING_JUNIOR, LIMITED_EDITION, RATING) },
    { LIMITED_RESIDENT,             achievement(0, 300, RATING_RESIDENT, LIMITED_EDITION, RATING) },
    { LIMITED_SENIOR,               achievement(0, 150, RATING_SENIOR, LIMITED_EDITION, RATING) },
    { LIMITED_HERO,                 achievement(0, 50, RATING_HERO, LIMITED_EDITION, RATING) },
    { LIMITED_SUPERHERO,            achievement(0, 10, RATING_SUPERHERO, LIMITED_EDITION, RATING) },

    { USER_REGISTERED,              achievement(0, COMMON_VALUE, 1, COMMON, REGISTERED) },
    { COMMON_NEWBIE,                achievement(0, COMMON_VALUE, RATING_NEWBIE, COMMON, RATING) },
    { COMMON_JUNIOR,                achievement(0, COMMON_VALUE, RATING_JUNIOR, COMMON, RATING) },
    { COMMON_RESIDENT,              achievement(0, COMMON_VALUE, RATING_RESIDENT, COMMON, RATING) },
    { COMMON_SENIOR,                achievement(0, COMMON_VALUE, RATING_SENIOR, COMMON, RATING) },
    { COMMON_HERO,                  achievement(0, COMMON_VALUE, RATING_HERO, COMMON, RATING) },
    { COMMON_SUPERHERO,             achievement(0, COMMON_VALUE, RATING_SUPERHERO, COMMON, RATING) },

    { ANSWER_15_MINUTES_BRONZE,     achievement(0, COMMON_VALUE, TEST_BRONZE_15_MINUTES, LIMITED_EDITION, ANSWER_15_MINUTES) },
    { ANSWER_15_MINUTES_SILVER,     achievement(0, COMMON_VALUE, TEST_SILVER_15_MINUTES, LIMITED_EDITION, ANSWER_15_MINUTES) },
    { ANSWER_15_MINUTES_GOLD,       achievement(0, COMMON_VALUE, TEST_GOLD_15_MINUTEST, LIMITED_EDITION, ANSWER_15_MINUTES) },

    { FIRST_ANSWER_BRONZE,          achievement(0, COMMON_VALUE, TEST_BRONZE_FIRST_ANSWER, LIMITED_EDITION, FIRST_ANSWER) },
    { FIRST_ANSWER_SILVER,          achievement(0, COMMON_VALUE, TEST_SILVER_FIRST_ANSWER, LIMITED_EDITION, FIRST_ANSWER) },
    { FIRST_ANSWER_GOLD,            achievement(0, COMMON_VALUE, TEST_GOLD_FIRST_ANSWER, LIMITED_EDITION, FIRST_ANSWER) },
  };

#else
std::map<uint32_t, achievement> achievements = {
    { QUESTION_BRONZE,              achievement(0, COMMON_VALUE, 10, LIMITED_EDITION, QUESTION) },
    { QUESTION_SILVER,              achievement(0, COMMON_VALUE, 50, LIMITED_EDITION, QUESTION) },
    { QUESTION_GOLD,                achievement(0, COMMON_VALUE, 100, LIMITED_EDITION, QUESTION) },

    { ANSWER_BRONZE,                achievement(0, COMMON_VALUE, 20, LIMITED_EDITION, ANSWER) },
    { ANSWER_SILVER,                achievement(0, COMMON_VALUE, 100, LIMITED_EDITION, ANSWER) },
    { ANSWER_GOLD,                  achievement(0, COMMON_VALUE, 200, LIMITED_EDITION, ANSWER) },

    { CORRECT_ANSWER_BRONZE,        achievement(0, COMMON_VALUE, 5, LIMITED_EDITION, CORRECT_ANSWER) },
    { CORRECT_ANSWER_SILVER,        achievement(0, COMMON_VALUE, 25, LIMITED_EDITION, CORRECT_ANSWER) },
    { CORRECT_ANSWER_GOLD,          achievement(0, COMMON_VALUE, 50, LIMITED_EDITION, CORRECT_ANSWER) },

    { FIRST_10K_REGISTERED,         achievement(0, 10000, 1, LIMITED_EDITION, REGISTERED) },
    { LIMITED_NEWBIE,               achievement(0, 700, RATING_NEWBIE, LIMITED_EDITION, RATING) },
    { LIMITED_JUNIOR,               achievement(0, 500, RATING_JUNIOR, LIMITED_EDITION, RATING) },
    { LIMITED_RESIDENT,             achievement(0, 300, RATING_RESIDENT, LIMITED_EDITION, RATING) },
    { LIMITED_SENIOR,               achievement(0, 150, RATING_SENIOR, LIMITED_EDITION, RATING) },
    { LIMITED_HERO,                 achievement(0, 50, RATING_HERO, LIMITED_EDITION, RATING) },
    { LIMITED_SUPERHERO,            achievement(0, 10, RATING_SUPERHERO, LIMITED_EDITION, RATING) },

    { USER_REGISTERED,              achievement(0, COMMON_VALUE, 1, COMMON, REGISTERED) },
    { COMMON_NEWBIE,                achievement(0, COMMON_VALUE, RATING_NEWBIE, COMMON, RATING) },
    { COMMON_JUNIOR,                achievement(0, COMMON_VALUE, RATING_JUNIOR, COMMON, RATING) },
    { COMMON_RESIDENT,              achievement(0, COMMON_VALUE, RATING_RESIDENT, COMMON, RATING) },
    { COMMON_SENIOR,                achievement(0, COMMON_VALUE, RATING_SENIOR, COMMON, RATING) },
    { COMMON_HERO,                  achievement(0, COMMON_VALUE, RATING_HERO, COMMON, RATING) },
    { COMMON_SUPERHERO,             achievement(0, COMMON_VALUE, RATING_SUPERHERO, COMMON, RATING) },

    { ANSWER_15_MINUTES_BRONZE,     achievement(0, COMMON_VALUE, 5, LIMITED_EDITION, ANSWER_15_MINUTES) },
    { ANSWER_15_MINUTES_SILVER,     achievement(0, COMMON_VALUE, 10, LIMITED_EDITION, ANSWER_15_MINUTES) },
    { ANSWER_15_MINUTES_GOLD,       achievement(0, COMMON_VALUE, 20, LIMITED_EDITION, ANSWER_15_MINUTES) },

    { FIRST_ANSWER_BRONZE,          achievement(0, COMMON_VALUE, 10, LIMITED_EDITION, FIRST_ANSWER) },
    { FIRST_ANSWER_SILVER,          achievement(0, COMMON_VALUE, 25, LIMITED_EDITION, FIRST_ANSWER) },
    { FIRST_ANSWER_GOLD,            achievement(0, COMMON_VALUE, 50, LIMITED_EDITION, FIRST_ANSWER) },
  };
#endif