#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "property.hpp"

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
                    SUPERHERO};

enum Type_achievement { UNIQE = 0, LEVEL};

struct achievement {
  achievement(uint32_t id, uint32_t community_id, uint64_t limit, Type_achievement type) :
    id(id), 
    community_id(community_id), 
    limit(limit), 
    type(type) 
  {} 

  const uint32_t id;
  const std::string name;
  const uint32_t community_id;                        //0 - for all
  const uint64_t limit;
  const Type_achievement type;                                    //uniqe -false | level = true

  bool operator == (const uint32_t &other) {
    return this->id == other;
  }

  bool operator != (const uint32_t &other) {
    return this->id != other;
  }
};
#if STAGE == 1 || STAGE == 2
std::vector<achievement> achievements = {
    achievement(QUESTION_ASKED,        0, 2, LEVEL), 
    achievement(ANSWER_GIVEN,          0, 10, LEVEL),   
    achievement(CORRECT_ANSWER,        0, 5, LEVEL),
    achievement(FIRST_10K_REGISTERED,   0, 10000, UNIQE),

    achievement(STRANGER,               0, 1000, UNIQE),
    achievement(NEWBIE,                 0, 5, UNIQE),
    achievement(JUNIOR,                 0, 5, UNIQE),
    achievement(RESIDENT,               0, 5, UNIQE),
    achievement(SENIOR,                 0, 5, UNIQE),
    achievement(HERO,                   0, 5, UNIQE),
    achievement(SUPERHERO,              0, 10, UNIQE),
};
#else
std::vector<achievement> achievements = {
    achievement(QUESTION_ASKED,        0, 500000, LEVEL), 
    achievement(ANSWER_GIVEN,          0, 500000, LEVEL),   
    achievement(CORRECT_ANSWER,        0, 500000, LEVEL),
    achievement(FIRST_10K_REGISTERED,  0, 10000, UNIQE),

    achievement(STRANGER,               0, 1000, UNIQE),
    achievement(NEWBIE,                 0, 700, UNIQE),
    achievement(JUNIOR,                 0, 500, UNIQE),
    achievement(RESIDENT,               0, 300, UNIQE),
    achievement(SENIOR,                 0, 150, UNIQE),
    achievement(HERO,                   0, 50, UNIQE),
    achievement(SUPERHERO,              0, 10, UNIQE),
};
#endif
