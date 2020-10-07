#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include "peeranha.hpp"

bool peeranha::add_achievement_amount(uint32_t id_achievement) {
  squeezed_achievement_index squeezed_achievement_table(_self, scope_all_squeezed_achievements);

  auto achieve = achievements.find(id_achievement);
  auto iter_squeezed_achievement = squeezed_achievement_table.find(id_achievement);

  if(achieve ==  achievements.end()) return false;  //"Achievement not found");

  if (iter_squeezed_achievement == squeezed_achievement_table.end()) {
    if(achieve->second.limit <= 0) { return false; }
    squeezed_achievement_table.emplace(
      _self, [id_achievement](auto &achievement) {
        achievement.id = id_achievement;
        achievement.count = 1;
      });
  } else {
    if(achieve->second.limit <= iter_squeezed_achievement->count) { return false; }
    squeezed_achievement_table.modify(
      iter_squeezed_achievement, _self,[id_achievement](auto &achievement) {
        achievement.count++;
      });
  }

  return true;
}

void  peeranha::del_achievement_amount(uint32_t id_achievement) {
  squeezed_achievement_index squeezed_achievement_table(_self, scope_all_squeezed_achievements);
  auto iter_squeezed_achievement = squeezed_achievement_table.find(id_achievement);
  if (iter_squeezed_achievement != squeezed_achievement_table.end()) {
    squeezed_achievement_table.modify(
      iter_squeezed_achievement, _self,[id_achievement](auto &achievement) {
        achievement.count--;
      });
  }
}