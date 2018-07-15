#include <eosiolib/eosio.hpp>
#include <eosiolib/multi_index.hpp>

using namespace eosio;

class peerania : public eosio::contract {
  public:
    peerania(account_name s):contract(s), _accounts(s, s)
    {}

    /// @abi action
    void addaccount(account_name user) {
      require_auth(user);

      print("Registring user by name ", user);

      _accounts.emplace(get_self(), [&](auto& a)
      {
        a.owner = user;
      });

      print("Registered account successfully.");
    }

  private:
    
    /// @abi table
    struct peeraccount {
      account_name owner;
      uint64_t primary_key() const { return owner; }
      EOSLIB_SERIALIZE( peeraccount, (owner) )
    };

    typedef eosio::multi_index<N(peeraccounts), peeraccount> peeraccounts;

    //local instance of accounts
    peeraccounts _accounts;
};

EOSIO_ABI( peerania, (addaccount) )
