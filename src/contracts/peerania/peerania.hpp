#pragma once
#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include "display_name.hpp"
#include "user_property.hpp"

namespace eosio {

class peerania : public contract {
 public:
  peerania(account_name self) : contract(self), _accounts(self, all_accounts) {}

  // Register new user
  ///@abi action
  void registeracc(account_name owner, std::string display_name,
                   std::string ipfs_profile);

  // Admin function
  // Delete account
  ///@abi action
  void adeleteacc(account_name account_to_delete);

  // Set(or add) property to account
  ///@abi action
  void setaccparam(account_name owner, prop_key_value property);

  // Admin function
  ///@abi action
  void asetaccparam(account_name owner, prop_key_value property);

  // Set user profile (IPFS link)
  ///@abi action
  void setipfspro(account_name owner, std::string ipfs_profile);

  // Admin function
  ///@abi action
  void asetipfspro(account_name owner, std::string ipfs_profile);

  // Set user display name
  ///@abi action
  void setdispname(account_name owner, std::string display_name);

 private:
  static const scope_name all_accounts = N(allaccounts);

  ///@abi table
  struct account {
    account_name owner;
    // mandatory fields
    std::string display_name;
    std::string ipfs_profile;
    uint64_t primary_key() const { return owner; }
    EOSLIB_SERIALIZE(account, (owner)(display_name)(ipfs_profile))
  };

  multi_index<N(account), account> _accounts;

  void set_account_parameter(account_name owner,
                             const prop_key_value &key_value);

  inline void set_account_ipfs_profile(account_name owner,
                                       const std::string &ipfs_profile);

  inline void add_display_name_to_map(account_name owner,
                                      const std::string &display_name);

  inline void remove_display_name_from_map(account_name owner,
                                           const std::string &display_name);

  // Checking that the account does exist
  inline void require_for_an_account(account_name owner);
};
}  // namespace eosio
