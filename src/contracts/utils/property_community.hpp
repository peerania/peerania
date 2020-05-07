#pragma once
#include <eosio/eosio.hpp>
#include <vector>

struct key_admin_community{
  int community;
  int value;
  uint8_t lkey() const { return community; }
};

struct [[eosio::table("propertycomm"), eosio::contract("peeranha.main")]] property_community {
  eosio::name user;
  std::vector<key_admin_community> properties;

  bool has_community_moderation_flag(int mask, uint16_t community_id) const;
  uint64_t primary_key() const { return user.value; }
};
typedef eosio::multi_index<"propertycomm"_n, property_community> property_community_index;
const uint64_t scope_all_property_community = eosio::name("allprprtcomm").value;

bool find_account_property_community(eosio::name user, int mask,  uint16_t community_id) {
    property_community_index property_community_table("peeranhamain"_n, scope_all_property_community);
    auto iter_user = property_community_table.find(user.value);
    if(iter_user == property_community_table.end()) {return false;}

    return iter_user->has_community_moderation_flag(mask, community_id);
}