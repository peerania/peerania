#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
//#include "../peerania/peerania.hpp" //fix by understanding compile params

namespace eosio
{
class testaction : public contract
{
  private:
    struct account
    {
        account_name owner;
        std::string name;
        uint64_t primary_key() const { return owner; }
        uint64_t secondary_index() const { return std::hash<std::string>{}(name); }
    };

    struct test_struct_param
    {
        account_name owner;
        std::string name;
        uint32_t add_test_prop;

        EOSLIB_SERIALIZE(test_struct_param, (owner)(name)(add_test_prop))
    };

    typedef multi_index<N(account), account> account_index;

  public:
    testaction(account_name self) : contract(self) {}

    ///@abi action
    void tactfunc(std::string input)
    {
        //require_auth(_self);
        print("\nTest success, get string =", input);
    }

    ///@abi action
    void trdanother(table_name table, account_name scope)
    { //there must be scope_name instead account_name, but scope isn't cast str to uint64_t automaticly
        print("\nTest read from table of another contract:\n");
        account_index _accounts(table, scope);
        for (auto i = _accounts.begin(); i != _accounts.end(); ++i)
            print("{id = ", (*i).owner, ", name=", (*i).name, "} is now in table.\n");
    }

    ///@abi action
    void taddanother(table_name table, account_name scope, test_struct_param user)
    {
        print("\nTest modify another table(error is expected):\n");
        account_index _accounts(table, scope);
        auto itr = _accounts.find(user.owner);
        _accounts.modify(itr, table, [&](auto &a) {
            a.owner = user.owner;
            a.name = user.name;
        });
    }
};
} // namespace eosio
EOSIO_ABI(eosio::testaction, (tactfunc)(trdanother)(taddanother))
