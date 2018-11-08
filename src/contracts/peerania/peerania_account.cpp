#include "account_timer.hpp"
#include "eosiolib/transaction.hpp"
#include "peerania.hpp"

void peerania::register_account(account_name owner, std::string display_name,
                                const std::string &ipfs_profile) {
  eosio_assert(account_table.find(owner) == account_table.end(),
               "Account already exists");
  assert_display_name(display_name);
  assert_ipfs(ipfs_profile);
  time current_time = now();
  account_timer moderation_points_timer;
  moderation_points_timer.last_update = current_time;
  moderation_points_timer.timer = TIMER_MODERATION_POINTS;
  account_table.emplace(_self,
                        [owner, &display_name, &ipfs_profile, current_time,
                         moderation_points_timer](auto &account) {
                          account.owner = owner;
                          account.display_name = display_name;
                          account.ipfs_profile = ipfs_profile;
                          account.rating = RATING_ON_CREATE;
                          account.pay_out_rating = RATING_ON_CREATE; //Probably pay_out_rating != RATING_ON_CREATE discuss it
                          account.registration_time = current_time;
                          account.timers.push_back(moderation_points_timer);
                        });

  add_display_name_to_map(owner, display_name);
  eosio::transaction t{};
  t.actions.emplace_back(eosio::permission_level(owner, N(active)), _self,
                         N(updateacc), std::make_tuple(owner));
  t.delay_sec = get_interval(moderation_points_timer);
  t.send(((uint128_t)owner << 32) + current_time, owner);
}

void peerania::set_account_string_property(account_name owner, uint8_t key,
                                           const std::string &value) {
  // Check is key user-changeble
  auto iter_account = find_account(owner);
  assert_allowed(*iter_account, owner, Action::SET_ACCOUNT_PROPERTY);
  account_table.modify(iter_account, _self, [&](auto &account) {
    set_property(account.string_properties, key, value);
  });
}

void peerania::set_account_integer_property(account_name owner, uint8_t key,
                                            int32_t value) {
  // Check is key user-changeble
  auto iter_account = find_account(owner);
  assert_allowed(*iter_account, owner, Action::SET_ACCOUNT_PROPERTY);
  account_table.modify(iter_account, _self, [&](auto &account) {
    set_property(account.integer_properties, key, value);
  });
}

void peerania::set_account_ipfs_profile(account_name owner,
                                        const std::string &ipfs_profile) {
  auto iter_account = find_account(owner);
  assert_ipfs(ipfs_profile);
  assert_allowed(*iter_account, owner, Action::SET_ACCOUNT_IPFS_PROFILE);
  account_table.modify(iter_account, _self, [&](auto &account) {
    account.ipfs_profile = ipfs_profile;
  });
}

void peerania::set_account_display_name(account_name owner,
                                        const std::string &display_name) {
  auto iter_account = find_account(owner);
  assert_display_name(display_name);
  assert_allowed(*iter_account, owner, Action::SET_ACCOUNT_DISPLAYNAME);
  remove_display_name_from_map(owner, iter_account->display_name);
  account_table.modify(iter_account, _self, [display_name](auto &account) {
    account.display_name = display_name;
  });
  add_display_name_to_map(owner, display_name);
}

void peerania::add_display_name_to_map(account_name owner,
                                       const std::string &display_name) {
  disp_to_acc_index table(_self, hash_display_name(display_name));
  table.emplace(_self, [&](auto &item) {
    item.owner = owner;
    item.display_name = display_name;
  });
}

void peerania::remove_display_name_from_map(account_name owner,
                                            const std::string &display_name) {
  disp_to_acc_index dtatable(_self, hash_display_name(display_name));
  auto itr_disptoacc = dtatable.find(owner);
  eosio_assert(itr_disptoacc != dtatable.end(), "display_name not found");
  dtatable.erase(itr_disptoacc);
  eosio_assert(itr_disptoacc != dtatable.end(), "Address not erased properly");
}

/*
// Calculate change of total(summ) rating
// It's important to calculate changes that happens on level
// higher than paid out rating
int16_t total_rating_change(int16_t rating, int16_t rating_change,
                            int16_t paid_out_rating) {
  int16_t total_rating_change_val = 0;
  if (rating_change < 0) {
    if (rating + rating_change > paid_out_rating)
      total_rating_change_val = rating_change;
    else if (rating > paid_out_rating)
      total_rating_change_val = paid_out_rating - rating;
  } else {
    if (rating > paid_out_rating)
      total_rating_change_val = rating_change;
    else if (rating + rating_change > paid_out_rating)
      total_rating_change_val = rating + rating_change - paid_out_rating;
  }
  return total_rating_change_val;
}
*/

void peerania::update_rating(account_index::const_iterator iter_account,
                             int rating_change) {
  if (rating_change == 0) return;
  const uint16_t current_period = get_period(now());
  const int16_t new_rating =
      iter_account->rating + rating_change;  // verify higher than -100;
  auto period_rating_table = period_rating_index(_self, iter_account->owner);
  auto iter_this_week_rating = period_rating_table.find(current_period);

  // iter_this_week_rating == period_rating_table.end() Means that it's first
  // transaction on this week
  const bool is_first_transaction_on_this_week =
      (iter_this_week_rating == period_rating_table.end());
  const uint16_t rating_to_award = is_first_transaction_on_this_week
                                       ? 0
                                       : iter_this_week_rating->rating_to_award;

  int16_t rating_to_award_change = 0;
  const uint16_t pay_out_rating = iter_account->pay_out_rating;
  auto iter_previous_week_rating = period_rating_table.find(current_period - 1);
  // Test 1(no information about previous week)
  if (iter_previous_week_rating != period_rating_table.end()) {
    uint16_t paid_out_rating = pay_out_rating - rating_to_award;
    int16_t user_week_rating_after_change =
        std::min(iter_previous_week_rating->rating, new_rating);
    rating_to_award_change =
        (user_week_rating_after_change - paid_out_rating) -
        rating_to_award; //equal user_week_rating_after_change - pay_out_rating;
    // Test 2
    if (rating_to_award_change + rating_to_award < 0)
      rating_to_award_change = -rating_to_award;

    auto iter_total_rating_change = total_rating_table.find(current_period);
    if (iter_total_rating_change == total_rating_table.end()) {
      total_rating_table.emplace(
          _self, [current_period, rating_to_award_change](auto &total_rating) {
            // If there is no record about this week in the table yet, a new
            // week has begun. That means rating_to_award = 0 for any user(first
            // rating transaction on this week); Test 2 guarantees the value of
            // rating_to_award_change >= 0;
            total_rating.period = current_period;
            total_rating.total_rating_to_reward = rating_to_award_change;
          });
    } else {
      total_rating_table.modify(iter_total_rating_change, _self,
                                [rating_to_award_change](auto &total_rating) {
                                  // The invariant is total_rating_change >=0
                                  // To proof this invariant we also use Test 2.
                                  // total_rating_change value is summ of all
                                  // positive rating changes of all users Ok,
                                  // Test 2 guarantee that summ of all
                                  // ratnig_to_award_change >= 0
                                  total_rating.total_rating_to_reward +=
                                      rating_to_award_change;
                                });
    }
  }

  if (is_first_transaction_on_this_week) {
    // means that this is the first transaction on this week
    // There are two variants:
    // 1. There is no record about previous week(test 1 failed)
    //___In this case rating_to_award_change = 0;
    // 2. Record about previous week exist(test 1 succeed)
    //___The same above, Test 2 guarantees the value of
    //___ratnig_to_award_change >= 0;
    iter_this_week_rating = period_rating_table.emplace(
        _self, [current_period, new_rating,
                rating_to_award_change](auto &period_rating) {
          period_rating.period = current_period;
          period_rating.rating = new_rating;
          period_rating.rating_to_award = rating_to_award_change;
        });
  } else {
    // The same above, Test 2 guarantees the value of
    // ratnig_to_award_change >= 0;
    period_rating_table.modify(
        iter_this_week_rating, _self,
        [new_rating, rating_to_award_change](auto &period_rating) {
          period_rating.rating = new_rating;
          period_rating.rating_to_award += rating_to_award_change;
        });
  }
  account_table.modify(
      iter_account, _self,
      [rating_to_award_change, new_rating](auto &account) {
        // Real value of paid out rating for this week is paid_out_rating -
        // rating_to_award Proof paid_out_rating on week_{n-1} <=
        // paid_out_rating on week_{n} for any n Each week
        account.pay_out_rating += rating_to_award_change;
        account.rating = new_rating;
      });
}

void peerania::update_rating(account_name user, int rating_change) {
  update_rating(find_account(user), rating_change);
}

void peerania::update_account(account_name user) {
  auto iter_account = find_account(user);

  bool create_deferred = false;
  time current_time = now();
  time min_update = INFINITY;
  account_table.modify(
      iter_account, _self,
      [&create_deferred, current_time, &min_update](auto &account) {
        auto iter_timer = account.timers.begin();
        while (iter_timer != account.timers.end()) {
          time timer_interval = get_interval(*iter_timer);
          if (current_time - iter_timer->last_update >= timer_interval) {
            create_deferred = true;
            if (on_tick(*iter_timer, account)) {
              iter_timer->last_update = current_time;
              if (min_update > timer_interval) {
                min_update = timer_interval;
              }
              iter_timer++;
            } else {
              iter_timer = account.timers.erase(iter_timer);
            }
          } else {
            if (min_update >
                timer_interval - current_time + iter_timer->last_update)
              min_update =
                  timer_interval - current_time + iter_timer->last_update;
            iter_timer++;
          }
        }
      });
  if (create_deferred && min_update != INFINITY) {
    eosio::transaction t{};
    t.actions.emplace_back(
        eosio::permission_level(user,
                                N(active)),  // with `from@active` permission
        _self,                   // You're sending this to `eosio.token`
        N(updateacc),            // to their `transfer` action
        std::make_tuple(user));  // with the appropriate args
    t.delay_sec = min_update;    // Set the delay
    t.send(((uint128_t)user << 32) + current_time,
           user);  // Send the transaction with some ID derived from the memo
  }
}

eosio::multi_index<N(account), account>::const_iterator peerania::find_account(
    account_name owner) {
  auto iter_user = account_table.find(owner);
  eosio_assert(iter_user != account_table.end(), "Account not registered");
  return iter_user;
}
