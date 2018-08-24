#include "peerania.hpp"

namespace eosio {

void peerania::register_account(account_name owner, std::string display_name,
                                const std::string &ipfs_profile) {
  eosio_assert(account_table.find(owner) == account_table.end(),
               "Account already exists");
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  account_table.emplace(_self, [&](auto &account) {
    account.owner = owner;
    account.display_name = display_name;
    account.ipfs_profile = ipfs_profile;
    account.registration_time = current_time_in_sec();
  });
  add_display_name_to_map(owner, display_name);
}

void peerania::set_account_string_property(account_name owner, uint8_t key,
                                            const std::string &value) {
  // Check is key user-changeble
  auto iter_account = find_account(owner);
  assert_allowed(*iter_account, Action::SET_ACCOUNT_PROPERTY);
  account_table.modify(iter_account, _self, [&](auto &account) {
    set_property(account.string_properties, key, value);
  });
}

void peerania::set_account_integer_property(account_name owner, uint8_t key,
                                            int32_t value) {
  // Check is key user-changeble
  auto iter_account = find_account(owner);
  assert_allowed(*iter_account, Action::SET_ACCOUNT_PROPERTY);
  account_table.modify(iter_account, _self, [&](auto &account) {
    set_property(account.integer_properties, key, value);
  });
}

void peerania::set_account_ipfs_profile(account_name owner,
                                        const std::string &ipfs_profile) {
  auto iter_account = find_account(owner);
  assert_allowed(*iter_account, Action::SET_ACCOUNT_IPFS_PROFILE);
  account_table.modify(iter_account, _self, [&](auto &account) {
    account.ipfs_profile = ipfs_profile;
  });
}

void peerania::set_account_display_name(account_name owner, const std::string &display_name){
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  auto iter_account = find_account(owner);
  assert_allowed(*iter_account, Action::SET_ACCOUNT_DISPLAYNAME);
  remove_display_name_from_map(owner, iter_account->display_name);
  account_table.modify(iter_account, _self,
                       [display_name](auto &account) { account.display_name = display_name; });
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

multi_index<N(account), account>::const_iterator peerania::find_account(
    account_name owner) {
  auto iter_user = account_table.find(owner);
  eosio_assert(iter_user != account_table.end(), "Account not registered");
  return iter_user;
}

}  // namespace eosio