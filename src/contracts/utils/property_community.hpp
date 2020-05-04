#pragma once
#include <eosio/eosio.hpp>
#include <vector>

struct key_community{
  int community;
  int value;
  bool operator == (const int& other){
    return community == other;
  }
};

struct [[eosio::table("propertycomm"), eosio::contract("peeranha.main")]] property_community {
  eosio::name user;
  std::vector<key_community> properties;
  uint64_t primary_key() const { return user.value; }

  void give_moderator_flag(eosio::name user, int flags, uint16_t community_id);
};
typedef eosio::multi_index<"propertycomm"_n, property_community> property_community_index;
const uint64_t scope_all_property_community = eosio::name("allpropertycomm").value;

