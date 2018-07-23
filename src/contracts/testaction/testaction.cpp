#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>

namespace eosio
{
class testaction : public contract
{
  public:
    testaction(account_name self) : contract(self) {}

    ///@abi action
    void tactfunc(std::string input){
        //require_auth(_self);
        print("\nTest success, get string =", input);
    }
};
} // namespace eosio
EOSIO_ABI(eosio::testaction, (tactfunc))
