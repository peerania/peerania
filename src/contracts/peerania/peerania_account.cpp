#include "account_timer.hpp"
#include "eosiolib/transaction.hpp"
#include "peerania.hpp"
namespace eosio {

void peerania::register_account(account_name owner, std::string display_name,
                                const std::string &ipfs_profile) {
  eosio_assert(account_table.find(owner) == account_table.end(),
               "Account already exists");
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  time current_time = current_time_in_sec();
  account_timer mdp;
  mdp.last_update = current_time;
  mdp.timer = TIMER1_MDP;
  account_table.emplace(_self, [owner, &display_name, &ipfs_profile,
                                current_time, mdp](auto &account) {
    account.owner = owner;
    account.display_name = display_name;
    account.ipfs_profile = ipfs_profile;
    account.rating = RATING_ON_CREATE;
    account.registration_time = current_time;
    account.timers.push_back(mdp);

  });

  add_display_name_to_map(owner, display_name);
  transaction t{};
  t.actions.emplace_back(permission_level(owner, N(active)), _self,
                         N(updateacc), std::make_tuple(owner));
  t.delay_sec = get_interval(mdp);
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
  assert_allowed(*iter_account, owner, Action::SET_ACCOUNT_IPFS_PROFILE);
  account_table.modify(iter_account, _self, [&](auto &account) {
    account.ipfs_profile = ipfs_profile;
  });
}

void peerania::set_account_display_name(account_name owner,
                                        const std::string &display_name) {
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  auto iter_account = find_account(owner);
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

void peerania::update_rating(account_index::const_iterator iter_account,
                             int rating_change) {
  if (rating_change == 0) return;
  account_table.modify(iter_account, _self, [rating_change](auto &account) {
    account.rating += rating_change;
  });
}

void peerania::update_rating(account_name user, int rating_change) {
  if (rating_change == 0) return;
  account_table.modify(
      find_account(user), _self,
      [rating_change](auto &account) { account.rating += rating_change; });

}

void peerania::update_account(account_name user) {
  //print("Call update\n");
  auto iter_account = find_account(user);

  bool create_deferred = false;
  time current_time = current_time_in_sec();

  account_table.modify(iter_account, _self,
                       [&create_deferred, current_time](auto &account) {
                         auto iter_timer = account.timers.begin();
                         while (iter_timer != account.timers.end()) {
                           if (current_time - iter_timer->last_update >=
                               get_interval(*iter_timer)) {
                             create_deferred = true;
                             if (on_tick(*iter_timer, account)) {
                               iter_timer->last_update = current_time;
                               iter_timer++;
                             } else {
                               iter_timer = account.timers.erase(iter_timer);
                             }
                           } else
                             iter_timer++;
                         }
                       });
  if (create_deferred) {
    time min_update = INFINITY;
    for (auto iter_timer = iter_account->timers.begin();
         iter_timer != iter_account->timers.end(); iter_timer++) {
      if (current_time - iter_timer->last_update == 0) {
        if (min_update > get_interval(*iter_timer))
          min_update = get_interval(*iter_timer);
      } else {
        if (min_update > get_interval(*iter_timer) - current_time + iter_timer->last_update)
          min_update = get_interval(*iter_timer) - current_time + iter_timer->last_update;
      }
    }
    if (min_update != INFINITY) {
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
}

multi_index<N(account), account>::const_iterator peerania::find_account(
    account_name owner) {
  auto iter_user = account_table.find(owner);
  eosio_assert(iter_user != account_table.end(), "Account not registered");
  return iter_user;
}

}  // namespace eosio