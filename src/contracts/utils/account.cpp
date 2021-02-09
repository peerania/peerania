#include "account.hpp"

void assert_display_name(const std::string &display_name) {
  assert_readble_string(display_name, 3, 40, "Invalid dispaly name");
}

void account::reduce_energy(uint8_t value, uint16_t community_id = 0) {
  if (has_moderation_flag(MODERATOR_FLG_INFINITE_ENERGY)) {
    return;
  }
  if (community_id != 0) {
    if(find_account_property_community(user, COMMUNITY_ADMIN_FLG_INFINITE_ENERGY, community_id)){
      return;
    }  
  }
  eosio::check(energy >= value, "Not enought energy!");
  energy -= value;
}

void account::update() { 
  time current_time = now();
  uint16_t current_period =
      (current_time - registration_time) / ACCOUNT_STAT_RESET_PERIOD;
  uint16_t periods_have_passed = current_period - last_update_period;
  if (periods_have_passed > 0) {
    if (rating <= 0) {
      rating += periods_have_passed * BAN_RATING_INCREMENT_PER_PERIOD;
      if (rating > 0) rating = 1;
    }
    last_update_period = current_period;
  }

  if (is_frozen) {
    if ((current_time - last_freeze) >=
        (MIN_FREEZE_PERIOD * (1 << (report_power - 1)))) {
      reports.clear();
      is_frozen = false;
      last_freeze = current_time;
    }
  } else {
    if (report_power != 0 &&
        (current_time - last_freeze) >= REPORT_POWER_RESET_PERIOD) {
      report_power = 0;
    }
    auto iter_report = reports.begin();
    while (iter_report != reports.end() &&
           current_time - iter_report->report_time >= REPORT_RESET_PERIOD) {
      iter_report = reports.erase(iter_report);
    }
  }
}

uint16_t account::get_status_energy() const {
  if (rating < 0) return 0;
  switch (rating) {
    STATUS0(STATUS0_ENERGY);
    STATUS1(STATUS1_ENERGY);
    STATUS2(STATUS2_ENERGY);
    STATUS3(STATUS3_ENERGY);
    STATUS4(STATUS4_ENERGY);
    STATUS5(STATUS5_ENERGY);
    STATUS6(STATUS6_ENERGY);
  }
}

bool is_moderation_availble() {
#if STAGE == 2
  constants_index all_constants_table("peeranhamain"_n, scope_all_constants);
  auto settings = all_constants_table.rbegin();
  time START_PERIOD_TIME = settings->start_period_time;
#endif

  return now() < START_PERIOD_TIME + MODERATION_AVAILABLE_PERIOD;
}

bool account::has_moderation_flag(int mask) const {
  if (is_moderation_availble()) {

    int moderator_flags =
        get_property_d(integer_properties, PROPERTY_MODERATOR_FLAGS, 0);
    return moderator_flags & mask;
  }
  return false;
}

uint8_t account::get_status_moderation_impact(uint16_t community_id = 0) const {
  if (has_moderation_flag(MODERATOR_FLG_INFINITE_IMPACT))
    return MODERATION_IMPACT_INFINITE;

   if (find_account_property_community(user, COMMUNITY_ADMIN_FLG_INFINITE_IMPACT, community_id)) {
    return MODERATION_IMPACT_INFINITE;
  }

  if (rating < 100) return 0;
  switch (rating) {
    STATUS1(1);
    STATUS2(2);
    STATUS3(3);
    STATUS4(4);
    STATUS5(5);
    STATUS6(6);
  }
}