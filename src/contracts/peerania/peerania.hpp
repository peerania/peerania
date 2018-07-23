#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
#include <vector>

namespace eosio
{
class peerania : public contract
{
public:
  peerania(account_name self) : contract(self), _accounts(self, global_scope_name) {}

  /// @abi table
  struct account
  {
    account_name owner;
    std::string name;
    uint64_t primary_key() const { return owner; }
    uint64_t secondary_index() const {return  std::hash<std::string>{}(name); }
  };

  struct test_struct_param
  {
    account_name owner;
    std::string name;
    uint32_t add_test_prop;

    EOSLIB_SERIALIZE( test_struct_param, (owner)(name)(add_test_prop) )
  };

  typedef multi_index<N(account), account> account_index;

  //typedef multi_index<N(nameindex), account, indexed_by<N(name), const_mem_fun<account, uint64_t, &account::secondary_index>>> by_name_index;

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
