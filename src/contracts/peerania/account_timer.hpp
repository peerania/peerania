#pragma once
#include "account.hpp"

#define INFINITY 0xFFFFFFFF
// Timer add moderaion point to an account
// begin
#define TIMER1_MDP 1
#ifdef DEBUG
#define TIMER1_MDP_INTERVAL 6
#else
#define TIMER1_MDP_INTERVAL 86400 * 7
#endif
bool on_timer1_mdp_tick(account& acc) {
  if (acc.rating > 0) acc.moderation_points += 3;
  return true;
}
// end
bool on_tick(account_timer timer, account& acc) {
  //eosio::print("Tick: ", int(timer.timer), "\n");
  switch (timer.timer) {
    case TIMER1_MDP:
      return on_timer1_mdp_tick(acc);
    default:
      return false;
  }
}

time get_interval(account_timer timer) {
  switch (timer.timer) {
    case TIMER1_MDP:
      return TIMER1_MDP_INTERVAL;
    default:
      return INFINITY;
  }
}