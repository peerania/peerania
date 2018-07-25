#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <vector>
#include "structs.hpp"

namespace eosio
{
class peerania : public contract
{
public:
  peerania(account_name self) : contract(self), _accounts(self, global_scope_name) {}

 
  struct test_struct_param
  {
    account_name owner;
    std::string name;
    uint32_t add_test_prop;

    EOSLIB_SERIALIZE( test_struct_param, (owner)(name)(add_test_prop) )
  };

  /// @abi action
  void addaccount(account_name user);

  /// @abi action
  void taddaccs(test_struct_param user);

  /// @abi action
  void tupdatedata(test_struct_param user);

  /// @abi action
  void tremovedata(account_name user);

  /// @abi action
  void tcallcontr(account_name user, std::string input);
  
private:
  static const int64_t global_scope_name = N(main);

  account_index _accounts;
};
} // namespace eosio
