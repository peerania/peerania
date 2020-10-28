#include "peeranha.hpp"

void peeranha::register_account(eosio::name user, std::string display_name,
                                const IpfsHash &ipfs_profile,
                                const IpfsHash &ipfs_avatar) {
  eosio::check(account_table.find(user.value) == account_table.end(),
               "Account already exists");
  assert_display_name(display_name);
  assert_ipfs(ipfs_profile);
  time current_time = now();
  account_table.emplace(_self, [user, &display_name, &ipfs_profile,
                                &ipfs_avatar, current_time](auto &account) {
    account.user = user;
    account.display_name = display_name;
    account.ipfs_profile = ipfs_profile;
    account.rating = RATING_ON_CREATE;
    account.pay_out_rating = RATING_ON_CREATE;  // Probably pay_out_rating !=
                                                // RATING_ON_CREATE discuss it
    account.registration_time = current_time;
    account.last_update_period = 0;
    account.ipfs_avatar = ipfs_avatar;
    account.energy = account.get_status_energy();
    account.report_power = 0;
    account.last_freeze = current_time;
    account.is_frozen = false;
  });

  global_stat_index global_stat_table(_self, scope_all_stat);
  auto iter_global_stat = global_stat_table.rbegin();
  eosio::check(iter_global_stat != global_stat_table.rend() &&
                   iter_global_stat->version == version,
               "Init contract first");
  global_stat_table.modify(
      --global_stat_table.end(), _self,
      [](auto &global_stat) { global_stat.user_count += 1; });
  
  testAchievement(user, REGISTERED, 1);
}

// ACTION BODY
void peeranha::set_account_profile(eosio::name user,
                                   const IpfsHash &ipfs_profile,
                                   const std::string &display_name,
                                   const IpfsHash &ipfs_avatar) {
  auto iter_account = find_account(user);
  assert_ipfs(ipfs_profile);
  assert_ipfs(ipfs_avatar);
  assert_display_name(display_name);
  assert_allowed(*iter_account, user, Action::SET_ACCOUNT_PROFILE);
  update_rating(iter_account, [&](auto &account) {
    account.reduce_energy(ENERGY_UPDATE_PROFILE);
    account.ipfs_profile = ipfs_profile;
    account.display_name = display_name;
    account.ipfs_avatar = ipfs_avatar;
  });
}

void peeranha::report_profile(eosio::name user, eosio::name user_to_report) {
  auto iter_snitch = find_account(user);
  auto iter_user_to_report = find_account(user_to_report);
  assert_allowed(*iter_snitch, user_to_report, Action::VOTE_REPORT_PROFILE);
  update_rating(iter_snitch, [&](auto &account) {
    account.reduce_energy(ENERGY_REPORT_PROFILE);
  });
  update_rating(iter_user_to_report, [&](auto &account) {
    account.update();
    eosio::check(!account.is_frozen, "Profile is already frozen");
    uint16_t total_report_points = 0;
    for (auto iter_reports = account.reports.begin();
         iter_reports != account.reports.end(); iter_reports++) {
      total_report_points += iter_reports->report_points;
      eosio::check(iter_reports->user != iter_snitch->user,
                   "You have already reported");
    }
    report r;
    r.report_time = now();
    r.user = iter_snitch->user;
    r.report_points = iter_snitch->get_status_moderation_impact();
    total_report_points += r.report_points;
    account.reports.push_back(r);
    if (total_report_points >= POINTS_TO_FREEZE) {
      if (account.report_power <
          MAX_FREEZE_PERIOD_MULTIPLIER)  // Max freeze period is 32 weeks
        account.report_power += 1;
      account.last_freeze = r.report_time;
      account.is_frozen = true;
    }
  });
}

void peeranha::update_account(eosio::name user) {
  auto iter_account = find_account(user);
  update_rating_base(iter_account, 0, [](auto &acc) { acc.update(); }, true,
                     false);
}

void peeranha::give_moderator_flag(eosio::name user, int flags) {
  auto iter_account = find_account(user);
  update_rating(iter_account, [flags](auto &account) {
    set_property_d(account.integer_properties, PROPERTY_MODERATOR_FLAGS, flags,
                   0);
  });
}

void peeranha::give_moderator_flag(eosio::name user, int flags, uint16_t community_id) {
  assert_community_exist(community_id);
  find_account(user);
  property_community_index property_community_table(_self, scope_all_property_community);

  auto iter_user = property_community_table.find(user.value);
  if (iter_user == property_community_table.end()) {
    property_community_table.emplace(
    _self, [user, flags, community_id](auto &property_community) {
      key_admin_community key_value;
      property_community.user = user;
      key_value.community = community_id;
      key_value.value =  flags;
      property_community.properties.push_back(key_value);
    });
  }
  else {
    property_community_table.modify(
        iter_user, _self, [flags, community_id](auto &property_community) {
          auto iter_community = linear_find(property_community.properties.begin(), property_community.properties.end(), community_id);
          if(iter_community == property_community.properties.end()){
            key_admin_community key_value;
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

void peeranha::update_rating_base(
    account_index::const_iterator iter_account, int rating_change,
    const std::function<void(account &)> account_modifying_lambda,
    bool hasLambda, bool zero_rating_forbidden) {
  if (rating_change == 0 && zero_rating_forbidden) {
    if (hasLambda)
      account_table.modify(
          iter_account, _self, [account_modifying_lambda](auto &account) {
            account.update();
            auto const rating_before = account.rating;
            account_modifying_lambda(account);
            eosio::check(account.rating == rating_before,
                         "Change rating in lambda is forbidden");
          });
    return;
  }
  const uint16_t current_period = get_period(now());
  int new_rating = iter_account->rating + rating_change;
  if (new_rating < MIN_RATING) new_rating = MIN_RATING;
  if (new_rating > MAX_RATING) new_rating = MAX_RATING;
  auto period_rating_table =
      period_rating_index(_self, iter_account->user.value);
  auto iter_this_week_rating = period_rating_table.find(current_period);

  // iter_this_week_rating == period_rating_table.end() Means that it's first
  // transaction on this week
  const bool is_first_transaction_on_this_week =
      (iter_this_week_rating == period_rating_table.end());
  const int rating_to_award = is_first_transaction_on_this_week
                                  ? 0
                                  : iter_this_week_rating->rating_to_award;

  int rating_to_award_change = 0;
  const int pay_out_rating = iter_account->pay_out_rating;

  // Very bad code.
  auto iter_previous_week_rating = period_rating_table.find(current_period - 1);
  if (iter_previous_week_rating == period_rating_table.end()) {
    auto riter_previous_week_rating = period_rating_table.rbegin();
    if (!is_first_transaction_on_this_week) {
      riter_previous_week_rating++;
    }
    if (riter_previous_week_rating == period_rating_table.rend())
      iter_previous_week_rating = period_rating_table.end();
    else
      iter_previous_week_rating =
          period_rating_table.find(riter_previous_week_rating->period);
  }
  // Very bad code ends

  // Test 1(no information about previous week)
  if (iter_previous_week_rating != period_rating_table.end()) {
    int paid_out_rating = pay_out_rating - rating_to_award;
    int user_week_rating_after_change =
        std::min(iter_previous_week_rating->rating, new_rating);
    rating_to_award_change =
        (user_week_rating_after_change - paid_out_rating) -
        rating_to_award;  // equal user_week_rating_after_change -
                          // pay_out_rating;
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
  account_table.modify(iter_account, _self,
                       [rating_to_award_change, new_rating, hasLambda,
                        account_modifying_lambda](auto &account) {
                         // Real value of paid out rating for this week is
                         // paid_out_rating - rating_to_award Proof
                         // paid_out_rating on week_{n-1} <= paid_out_rating on
                         // week_{n} for any n Each week
                         account.pay_out_rating += rating_to_award_change;
                         account.rating = new_rating;
                         account.update();

                         auto const rating_before = account.rating;
                         if (hasLambda) account_modifying_lambda(account);
                         eosio::check(account.rating == rating_before,
                                      "Change rating in lambda is forbidden");
                       });
  testAchievement(iter_account->user, RATING, iter_account->rating);
}

void peeranha::update_rating(eosio::name user, int rating_change) {
  update_rating_base(find_account(user), rating_change, nullptr, false, true);
}

void peeranha::update_rating(
    account_index::const_iterator iter_account, int rating_change,
    const std::function<void(account &)> account_modifying_lambda) {
  update_rating_base(iter_account, rating_change, account_modifying_lambda,
                     true, true);
}

void peeranha::update_rating(
    account_index::const_iterator iter_account,
    const std::function<void(account &)> account_modifying_lambda) {
  account_table.modify(iter_account, _self,
                       [account_modifying_lambda](auto &account) {
                         account.update();
                         auto const rating_before = account.rating;
                         account_modifying_lambda(account);
                         eosio::check(account.rating == rating_before,
                                      "Change rating in lambda is forbidden");
                       });
}

void peeranha::update_rating(
    eosio::name user, int rating_change,
    const std::function<void(account &)> account_modifying_lambda) {
  update_rating_base(find_account(user), rating_change,
                     account_modifying_lambda, true, true);
}

void peeranha::update_rating(account_index::const_iterator iter_account,
                             int rating_change) {
  update_rating_base(iter_account, rating_change, nullptr, false, true);
}

account_index::const_iterator peeranha::find_account(eosio::name user) {
  auto iter_user = account_table.find(user.value);
  eosio::check(iter_user != account_table.end(), "Account not registered");
  return iter_user;
}
