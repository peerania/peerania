#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "property.hpp"

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
//   Stranger	0 ... 99
// Newbie	100 ... 499
// Junior	500-999
// Resident	1000 ... 2499
// Senior	2500 ... 4999
// Hero	5000 ... 9999
// Superhero	10000