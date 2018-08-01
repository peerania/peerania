#include "peerania.hpp"

namespace eosio {

void peerania::registeracc(account_name owner, std::string display_name,
                           std::string ipfs_profile) {
  require_auth(owner);
  print(current_time());
  eosio_assert(account_table.find(owner) == account_table.end(),
               "Account already exists");
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  account_table.emplace(_self, [&](auto &account) {
    account.owner = owner;
    account.display_name = display_name;
    account.ipfs_profile = ipfs_profile;
    // current_time() returns time in micros, divided by 10^6 set time in
    // seconds
    account.registration_time = current_time() / 1000000;
  });
  add_display_name_to_map(owner, display_name);
}

void peerania::adeleteacc(account_name account_to_delete) {
  require_auth(_self);
  auto itr = account_table.find(account_to_delete);
  eosio_assert(itr != account_table.end(), "Account not found");
  account_table.erase(itr);
  eosio_assert(itr != account_table.end(), "Address not erased properly");
}

void peerania::setaccparam(account_name owner, prop_key_value property) {
  require_auth(owner);
  set_account_parameter(owner, property);
}

void peerania::asetaccparam(account_name owner, prop_key_value property) {
  require_auth(_self);
  set_account_parameter(owner, property);
}

void peerania::setipfspro(account_name owner, std::string ipfs_profile) {
  require_auth(owner);
  set_account_ipfs_profile(owner, ipfs_profile);
}

void peerania::asetipfspro(account_name owner, std::string ipfs_profile) {
  require_auth(_self);
  set_account_ipfs_profile(owner, ipfs_profile);
}

void peerania::setdispname(account_name owner, std::string display_name) {
  require_auth(owner);
  eosio_assert(display_name.length() >= MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  auto itraccs = account_table.find(owner);
  eosio_assert(itraccs != account_table.end(), "Account not found");
  remove_display_name_from_map(owner, itraccs->display_name);
  account_table.modify(itraccs, _self,
                   [&](auto &acc) { acc.display_name = display_name; });
  add_display_name_to_map(owner, display_name);
}

void peerania::set_account_parameter(account_name owner,
                                     const prop_key_value &key_value) {
  require_for_an_account(owner);
  eosio_assert(key_value.key < SYSTEM_PROP_START, "Incorrect key");
  user_property_index user_property_table(_self, owner);
  auto itr = user_property_table.find(user_property_make_pk(owner, key_value.key));
  if (itr == user_property_table.end()) {
    user_property_table.emplace(_self, [&](auto &prop) {
      prop.owner = owner;
      prop.key_value = key_value;
    });
  } else {
    user_property_table.modify(itr, _self, [&](auto &prop) {
      prop.key_value.value = key_value.value;
    });
  }
}

void peerania::set_account_ipfs_profile(account_name owner,
                                        const std::string &ipfs_profile) {
  auto itr = account_table.find(owner);
  eosio_assert(itr != account_table.end(), "Account not found");
  account_table.modify(itr, _self,
                   [&](auto &account) { account.ipfs_profile = ipfs_profile; });
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

void peerania::require_for_an_account(account_name owner) {
  eosio_assert(account_table.find(owner) != account_table.end(),
               "Account not registered");
}
};  // namespace eosio
EOSIO_ABI(eosio::peerania, (adeleteacc)(registeracc)(setaccparam)(asetaccparam)(
                               asetipfspro)(setipfspro)(setdispname))
