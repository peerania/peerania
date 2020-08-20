#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "property.hpp"

#define LOW_STRANGER 35
#define HIGH_STRANGER 99
#define LOW_NEWBIE 100
#define HIGH_NEWBIE 499
#define LOW_JUNIOR 500
#define HIGH_JUNIOR 999
#define LOW_RESIDENT 1000
#define HIGH_RESIDENT 2499
#define LOW_SENIOR 2500
#define HIGH_SENIOR 4999
#define LOW_HERO 5000
#define HIGH_HERO 9999
#define LOW_SUPERHERO 10000

enum Achievements { questions_asked = 1, 
                    answers_given, 
                    correct_answers, 
                    first_10k_registered, 
                    stranger, 
                    newbie, 
                    junior, 
                    resident, 
                    senior, 
                    hero, 
                    superhero};

struct achievement {
  achievement(uint32_t id, uint32_t community_id, uint64_t limit, bool type) :
    id(id), 
    community_id(community_id), 
    limit(limit), 
    type(type) 
  {} 

  const uint32_t id;
  const std::string name;
  const uint32_t community_id;                        //0 - for all
  const uint64_t limit;
  const bool type;                                    //uniqe -false | level = true

  bool operator == (const uint32_t &other) {
    return this->id == other;
  }

  bool operator != (const uint32_t &other) {
    return this->id != other;
  }
};
#if STAGE == 1 || STAGE == 2
std::vector<achievement> achievements = {
    achievement(questions_asked,        0, 2, true), 
    achievement(answers_given,          0, 10, true),   
    achievement(correct_answers,        0, 5, true),
    achievement(first_10k_registered,   0, 10000, false),

    achievement(stranger,               0, 1000, false),
    achievement(newbie,                 0, 5, false),
    achievement(junior,                 0, 5, false),
    achievement(resident,               0, 5, false),
    achievement(senior,                 0, 5, false),
    achievement(hero,                   0, 5, false),
    achievement(superhero,              0, 10, false),
};
#else
std::vector<achievement> achievements = {
    achievement(questions_asked,        0, 500000, true), 
    achievement(answers_given,          0, 500000, true),   
    achievement(correct_answers,        0, 500000, true),
    achievement(first_10k_registered,   0, 10000, false),

    achievement(stranger,               0, 1000, false),
    achievement(newbie,                 0, 700, false),
    achievement(junior,                 0, 500, false),
    achievement(resident,               0, 300, false),
    achievement(senior,                 0, 150, false),
    achievement(hero,                   0, 50, false),
    achievement(superhero,              0, 10, false),
};
#endif
