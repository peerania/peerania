#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <map>

#define RATING_STRANGER 35
#define RATING_NEWBIE 100
#define RATING_JUNIOR 500
#define RATING_RESIDENT 1000
#define RATING_SENIOR 2500
#define RATING_HERO 5000
#define RATING_SUPERHERO 10000

enum Achievements { QUESTION_ASKED = 1, 
                    ANSWER_GIVEN, 
                    CORRECT_ANSWER, 
                    FIRST_10K_REGISTERED, 
                    STRANGER, 
                    NEWBIE, 
                    JUNIOR, 
                    RESIDENT, 
                    SENIOR, 
                    HERO, 
                    SUPERHERO,
                    ANSWER_15_MINUTES,
                    FIRST_ANSWER,};

enum Type_achievement { UNIQE = 0, LEVEL};

struct achievement {
  achievement(uint32_t community_id, uint64_t limit, Type_achievement type) :
    community_id(community_id), 
    limit(limit), 
    type(type) 
  {}

  const std::string name;
  const uint32_t community_id;                        //0 - for all
  const uint64_t limit;
  const Type_achievement type;                        //uniqe -false | level = true
};

#if STAGE == 1 || STAGE == 2
 std::map<uint32_t, achievement> achievements = {
    { QUESTION_ASKED,       achievement(0, 50000, LEVEL) },
    { ANSWER_GIVEN,         achievement(0, 50000, LEVEL) }, 
    { CORRECT_ANSWER,       achievement(0, 50000, LEVEL) },
    { FIRST_10K_REGISTERED, achievement(0, 10000, UNIQE) },
    { STRANGER,             achievement(0, 1000, UNIQE) },
    { NEWBIE,               achievement(0, 700, UNIQE) },
    { JUNIOR,               achievement(0, 500, UNIQE) },
    { RESIDENT,             achievement(0, 300, UNIQE) },
    { SENIOR,               achievement(0, 150, UNIQE) },
    { HERO,                 achievement(0, 50, UNIQE) },
    { SUPERHERO,            achievement(0, 10, UNIQE) },
    { ANSWER_15_MINUTES,    achievement(0, 500000, LEVEL) },
    { FIRST_ANSWER,         achievement(0, 500000, LEVEL) },
};

#else
std::map<uint32_t, achievement> achievements = {
    { QUESTION_ASKED,       achievement(0, 500000, LEVEL) },
    { ANSWER_GIVEN,         achievement(0, 500000, LEVEL) },  
    { CORRECT_ANSWER,       achievement(0, 500000, LEVEL) },
    { FIRST_10K_REGISTERED, achievement(0, 10000, UNIQE) },
    { STRANGER,             achievement(0, 1000, UNIQE) },
    { NEWBIE,               achievement(0, 700, UNIQE) },
    { JUNIOR,               achievement(0, 500, UNIQE) },
    { RESIDENT,             achievement(0, 300, UNIQE) },
    { SENIOR,               achievement(0, 150, UNIQE) },
    { HERO,                 achievement(0, 50, UNIQE) },
    { SUPERHERO,            achievement(0, 10, UNIQE) },
    { ANSWER_15_MINUTES,    achievement(0, 500000, LEVEL) },
    { FIRST_ANSWER,         achievement(0, 500000, LEVEL) }, 
};
#endif