#pragma once
#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include "userproperty.hpp"
#include "displayname.hpp"

namespace eosio
{
class peerania : public contract
{
public:
  peerania(account_name self) : contract(self), _accounts(self, allaccounts) {}

  //Register new user
  ///@abi action
  void registeracc(account_name owner, std::string displayname, std::string ipfsprofile);

  //Admin function
  //Delete account
  ///@abi action
  void adeleteacc(account_name todelete);

  //Set(or add) property to account
  ///@abi action
  void setaccparam(account_name owner, prop_key_value property);

  //Admin function
  ///@abi action
  void asetaccparam(account_name owner, prop_key_value property);

  //Set user profile (IPFS link)
  ///@abi action
  void setipfspro(account_name owner, std::string ipfsprofile);

  //Admin function
  ///@abi action
  void asetipfspro(account_name owner, std::string ipfsprofile);
  
  //Set user display name
  ///@abi action
  void setdispname(account_name owner, std::string displayname);

private:
  static const scope_name allaccounts = N(allaccounts);

  ///@abi table
  struct account
  {
    account_name owner;
    //mandatory fields
    std::string displayname;
    std::string ipfsprofile;
    uint64_t primary_key() const { return owner; }
    EOSLIB_SERIALIZE(account, (owner)(displayname)(ipfsprofile))
  };
  multi_index<N(account), account> _accounts;

  void set_account_parameter(account_name owner, const prop_key_value &keyvalue);

  inline void set_account_ipfs_profile(account_name owner, const std::string &ipfsprofile);

  inline void add_displayname_to_map(account_name owner, const std::string &displayname);

  inline void remove_display_name_from_map(account_name owner, const std::string &displayname);

  //Checking that the account does exist
  inline void require_for_an_account(account_name owner);
};
} // namespace eosio
