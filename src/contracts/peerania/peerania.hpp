#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>

namespace eosio
{
  class peerania : public contract
  {
    public:
      peerania(account_name self) : contract(self), _accounts(self, global_scope_name) {}

      /// @abi action
      void addaccount(account_name user);

      /// @abi table
      struct account
      {
        account_name owner;

        uint64_t primary_key() const { return owner; }
      };

      typedef eosio::multi_index<N(account), account> account_index;
    
    private:
      static const int64_t global_scope_name = N(main); 

      account_index _accounts;
  };
} 
