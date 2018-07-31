#include "peerania.hpp"

namespace eosio {

void peerania::registeracc(account_name owner, std::string displayname,
                           std::string ipfsprofile) {
  require_auth(owner);
  eosio_assert(_accounts.find(owner) == _accounts.end(),
               "Account already exists");
  eosio_assert(displayname.length() > MIN_DISPLAYNAME_LEN,
               "The displayname too short.");
  _accounts.emplace(_self, [&](auto &account) {
    account.owner = owner;
    account.displayname = displayname;
    account.ipfsprofile = ipfsprofile;
  });
  add_displayname_to_map(owner, displayname);
}

void peerania::adeleteacc(account_name todelete) {
  require_auth(_self);
  auto itr = _accounts.find(todelete);
  eosio_assert(itr != _accounts.end(), "Account not found");
  _accounts.erase(itr);
  eosio_assert(itr != _accounts.end(), "Address not erased properly");
}

void peerania::set_account_parameter(account_name owner,
                                     const prop_key_value &keyvalue) {
  require_for_an_account(owner);
  eosio_assert(keyvalue.key < SYSTEM_PROP_START, "Incorrect key");
  userproperty_index uptable(_self, owner);
  auto itr = uptable.find(prop_mkprimary(owner, keyvalue.key));
  if (itr == uptable.end()) {
    uptable.emplace(_self, [&](auto &prop) {
      prop.owner = owner;
      prop.kv = keyvalue;
    });
  } else {
    uptable.modify(itr, _self,
                   [&](auto &prop) { prop.kv.value = keyvalue.value; });
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
                                        const std::string &ipfsprofile) {
  auto itr = _accounts.find(owner);
  eosio_assert(itr != _accounts.end(), "Account not found");
  _accounts.modify(itr, _self,
                   [&](auto &account) { account.ipfsprofile = ipfsprofile; });
}

void peerania::setipfspro(account_name owner, std::string ipfsprofile) {
  require_auth(owner);
  set_account_ipfs_profile(owner, ipfsprofile);
}

void peerania::asetipfspro(account_name owner, std::string ipfsprofile) {
  require_auth(_self);
  set_account_ipfs_profile(owner, ipfsprofile);
}

void peerania::setdispname(account_name owner, std::string displayname) {
  require_auth(owner);
  auto itraccs = _accounts.find(owner);
  eosio_assert(itraccs != _accounts.end(), "Account not found");
  remove_display_name_from_map(owner, itraccs->displayname);
  _accounts.modify(itraccs, _self,
                   [&](auto &acc) { acc.displayname = displayname; });
  add_displayname_to_map(owner, displayname);
}

void peerania::add_displayname_to_map(account_name owner,
                                      const std::string &displayname) {
  disptoacc_index table(_self, hash_display_name(displayname));
  table.emplace(_self, [&](auto &item) {
    item.owner = owner;
    item.displayname = displayname;
  });
}

void peerania::remove_display_name_from_map(account_name owner,
                                            const std::string &displayname) {
  disptoacc_index dtatable(_self, hash_display_name(displayname));
  auto itr_disptoacc = dtatable.find(owner);
  eosio_assert(itr_disptoacc != dtatable.end(), "Displayname not found");
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
