#include "peerania.hpp"

namespace eosio
{
    void peerania::addaccount(account_name user)
    {
        require_auth(user);
        
        print("Registring user by name ", user, ".\n");

        auto existing = _accounts.find(user);
        eosio_assert(existing == _accounts.end(), "Account already exists");

        _accounts.emplace(_self, [&](auto &a) {
            a.owner = user;
        });
        
        for (auto i = _accounts.begin(); i != _accounts.end(); ++i)
        {
            print((*i).owner, " is now in table.\n");
        }
        
        print("Registered account successfully.");
    }

} // namespace eosio

EOSIO_ABI(eosio::peerania, (addaccount))