#pragma once
#include "property_community.hpp"

int get_property_d_(const std::vector<key_admin_community> &properties, uint16_t key,
                     int default_value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);
  if (itr_property == properties.end()) return default_value;
  return itr_property->value;
}

bool is_moderation_availble_() {
#if STAGE == 2
  constants_index all_constants_table("peeranhamain"_n, scope_all_constants);
  auto settings = all_constants_table.rbegin();
  time START_PERIOD_TIME = settings->start_period_time;
#endif

  return now() < START_PERIOD_TIME + MODERATION_AVAILABLE_PERIOD;
}


bool property_community::has_community_moderation_flag(int mask,  uint16_t community_id)const {
  if (is_moderation_availble_()) {

    int moderator_flags =
        get_property_d_(properties, community_id, 0);
    return moderator_flags & mask;
  }
  return false;
}