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
        a.name = "test";
        //Empty constructor for class 'string' exists, so it's not necessary to initialize 'a.name'
        //But I
    });

    for (auto i = _accounts.begin(); i != _accounts.end(); ++i)
    {
        print((*i).owner, " is now in table.\n");
    }

    print("Registered account successfully.\n");
}

void peerania::taddaccs(test_struct_param user)
{
    print("Testing pass struct as a param, expand table\n");
    require_auth(user.owner);
    print("{id = ", user.owner, ", name=", user.name, "} is come.\n");

    auto existing = _accounts.find(user.owner);
    eosio_assert(existing == _accounts.end(), "Account already exists\n");

    _accounts.emplace(_self, [&](auto &a) {
        a.owner = user.owner;
        a.name = user.name;
    });

    for (auto i = _accounts.begin(); i != _accounts.end(); ++i)
    {
        print("{id = ", (*i).owner, ", name=", (*i).name, "} is now in table.\n");
    }

    print("Additional test paroperty is uint32_t; val=", user.add_test_prop);

    print("\nTesting pass struct as a param, expand table - OK\n");
}

void peerania::tupdatedata(test_struct_param user)
{
    print("Testing modify method(modify table data)\n");
    require_auth(user.owner); //For example, you can only modify your account.

    auto itr = _accounts.find(user.owner);
    eosio_assert(itr != _accounts.end(), "Address for account not found");
    print("{id = ", (*itr).owner, ", name=", (*itr).name, "} is now in table.\n");
    print("New name: ", user.name, "\nTry to modify.\n");

    _accounts.modify(itr, _self, [&](auto &a) {
        a.owner = user.owner;
        a.name = user.name;
    });
    print("Table after modifying");
    for (auto i = _accounts.begin(); i != _accounts.end(); ++i)
    {
        print("{id = ", (*i).owner, ", name=", (*i).name, "} is now in table.\n");
    }

    print("Additional test paroperty is uint32_t; val=", user.add_test_prop);
    print("\nTesting modify data - OK\n");
}

void peerania::tremovedata(account_name user)
{
    require_auth(user); //For example, you can only delete your account.
    auto itr = _accounts.find(user);
    eosio_assert(itr != _accounts.end(), "Address for account not found");
    _accounts.erase(itr);
    eosio_assert(itr != _accounts.end(), "Address not erased properly");
    print("\nTesting remove data - OK\n");
}

void peerania::tcallcontr(account_name user, std::string input)
{
    require_auth(user);
    print("Test call another method, get string: ", input, "\n");
    
    action(
        permission_level{_self , N(eosio.code)},
        N(talice),              //contract _self
        N(tactfunc),
        std::make_tuple(input) //put arguments here
    ).send();
        
    //tremovedata(user);
    //SEND_INLINE_ACTION( *this, tremovedata, {user /*what I requre in require_auth()*/,N(active)}, {user} ); //OK - success;
}



} // namespace eosio
EOSIO_ABI(eosio::peerania, (addaccount)(taddaccs)(tupdatedata)(tremovedata)(tcallcontr))