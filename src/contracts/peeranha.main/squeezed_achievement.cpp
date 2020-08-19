#pragma once
#include <eosio/eosio.hpp>
#include <string>
#include <vector>
#include "peeranha.hpp"

bool peeranha::up_achievement(uint32_t id_achievement) {
  squeezed_achievement_index squeezed_achievement_table(_self, scope_all_squeezed_achievements);

  auto achieve = std::find(achievements.begin(), achievements.end(), id_achievement);
  auto iter_squeezed_achievement = squeezed_achievement_table.find(id_achievement);

  if(achieve ==  achievements.end()) return false;  //"Achievement not found");

  if (iter_squeezed_achievement == squeezed_achievement_table.end()) {
    if(achieve->limit <= 0)
      return false;
    squeezed_achievement_table.emplace(
      _self, [id_achievement, &achieve](auto &achievement) {
        achievement.id = id_achievement;
          achievement.count = 1;
      });
  } else {
    if(achieve->limit <= iter_squeezed_achievement->count)
      return false;
    squeezed_achievement_table.modify(
      iter_squeezed_achievement, _self,[id_achievement, &achieve](auto &achievement) {
        achievement.count++;
      });
  }

  return true;
}
