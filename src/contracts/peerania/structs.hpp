#include <eosiolib/types.hpp>
#include <eosiolib/currency.hpp>
#include <string>

namespace eosio
{
/// @abi table
struct account
{
    account_name owner;
    std::string name;
    uint64_t primary_key() const { return owner; }
    uint64_t secondary_index() const { return std::hash<std::string>{}(name); }
};

typedef multi_index<N(account), account> account_index;

//typedef multi_index<N(nameindex), account, indexed_by<N(name), const_mem_fun<account, uint64_t, &account::secondary_index>>> by_name_index;

}; // namespace eosio