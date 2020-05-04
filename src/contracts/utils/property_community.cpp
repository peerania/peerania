#pragma once
#include "peeranha.hpp"
//#include "property_community.hpp"


void peeranha::give_moderator_flag(eosio::name user, int flags, uint16_t community_id) {
  assert_community_exist(community_id);
  property_community_index property_community_table(_self, scope_all_property_community);

  auto iter_user = property_community_table.find(user.value);
  if (iter_user == property_community_table.end()) {
    property_community_table.emplace(
    _self, [user, flags, community_id](auto &property_community) {
      key_community key_value;
      property_community.user = user;
      key_value.community = community_id;
      key_value.value =  flags;
      property_community.properties.push_back(key_value);
    });
  }
  else {
    property_community_table.modify(
        iter_user, _self, [flags, community_id](auto &property_community) {
          auto iter_community = find(property_community.properties.begin(), property_community.properties.end(), community_id);
          if(iter_community == property_community.properties.end()){
            key_community key_value;
            key_value.community = community_id;
            key_value.value =  flags;
            property_community.properties.push_back(key_value);
          }
          else{
            iter_community->value =  flags; 
          }
        });

  }
}