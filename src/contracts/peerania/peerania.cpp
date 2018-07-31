#include "peerania.hpp"

namespace eosio {

void peerania::registeracc(account_name owner, std::string display_name,
                           std::string ipfs_profile) {
  require_auth(owner);
  eosio_assert(_accounts.find(owner) == _accounts.end(),
               "Account already exists");
  eosio_assert(display_name.length() > MIN_DISPLAY_NAME_LEN,
               "The display name too short.");
  _accounts.emplace(_self, [&](auto &account) {
    account.owner = owner;
    account.display_name = display_name;
    account.ipfs_profile = ipfs_profile;
  });
  add_display_name_to_map(owner, display_name);
}

void peerania::adeleteacc(account_name account_to_delete) {
  require_auth(_self);
  auto itr = _accounts.find(account_to_delete);
  eosio_assert(itr != _accounts.end(), "Account not found");
  _accounts.erase(itr);
  eosio_assert(itr != _accounts.end(), "Address not erased properly");
}

void peerania::set_account_parameter(account_name owner,
                                     const prop_key_value &key_value) {
  require_for_an_account(owner);
  eosio_assert(key_value.key < SYSTEM_PROP_START, "Incorrect key");
  user_property_index user_property_table(_self, owner);
  auto itr = user_property_table.find(prop_mkprimary(owner, key_value.key));
  if (itr == user_property_table.end()) {
    user_property_table.emplace(_self, [&](auto &prop) {
      prop.owner = owner;
      prop.key_value = key_value;
    });
  } else {
    user_property_table.modify(itr, _self,
                   [&](auto &prop) { prop.key_value.value = key_value.value; });
  }
}

void peerania::setaccparam(account_name owner, prop_key_value property) {
  require_auth(owner);
  set_account_parameter(owner, property);
}

void peerania::asetaccparam(account_name owner, prop_key_value property) {
  require_auth(_self);
  set_account_parameter(owner, property);
}

void peerania::set_account_ipfs_profile(account_name owner,
                                        const std::string &ipfs_profile) {
  auto itr = _accounts.find(owner);
  eosio_assert(itr != _accounts.end(), "Account not found");
  _accounts.modify(itr, _self,
                   [&](auto &account) { account.ipfs_profile = ipfs_profile; });
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
  auto itraccs = _accounts.find(owner);
  eosio_assert(itraccs != _accounts.end(), "Account not found");
  remove_display_name_from_map(owner, itraccs->display_name);
  _accounts.modify(itraccs, _self,
                   [&](auto &acc) { acc.display_name = display_name; });
  add_display_name_to_map(owner, display_name);
}

void peerania::add_display_name_to_map(account_name owner,
                                       const std::string &display_name) {
  disptoacc_index table(_self, hash_display_name(display_name));
  table.emplace(_self, [&](auto &item) {
    item.owner = owner;
    item.display_name = display_name;
  });
}

void peerania::remove_display_name_from_map(account_name owner,
                                            const std::string &display_name) {
  disptoacc_index dtatable(_self, hash_display_name(display_name));
  auto itr_disptoacc = dtatable.find(owner);
  eosio_assert(itr_disptoacc != dtatable.end(), "display_name not found");
  dtatable.erase(itr_disptoacc);
  eosio_assert(itr_disptoacc != dtatable.end(), "Address not erased properly");
}

void peerania::require_for_an_account(account_name owner) {
  eosio_assert(_accounts.find(owner) != _accounts.end(),
               "Account not registered");
}

};  // namespace eosio
EOSIO_ABI(eosio::peerania, (adeleteacc)(registeracc)(setaccparam)(asetaccparam)(
                               asetipfspro)(setipfspro)(setdispname))
