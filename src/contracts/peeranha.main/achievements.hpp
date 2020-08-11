#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "property.hpp"

//enum Rarity { common, rare, epic, legendary, unique};

struct [[eosio::table("achieve"), eosio::contract("peeranha.main")]] achievements {
  uint32_t id;
  std::string name;
  uint32_t community_id;                        //0 - for all
  std::vector<str_key_value> string_properties;
  std::vector<int_key_value> integer_properties;
  uint64_t issued;
  uint64_t limit;
  bool type;                                    //uniqe -false | level = true
  time creation_time;

  uint64_t primary_key() const { return id; }
  uint32_t community_key() const { return community_id; }
};
const uint64_t scope_all_achievements = eosio::name("allachieve").value;
typedef eosio::multi_index<
    "achieve"_n, achievements
    ,
    eosio::indexed_by<"commun"_n, eosio::const_mem_fun<achievements, uint32_t,
                                                      &achievements::community_key>>
    > achievements_index;