#pragma once

#include <eosiolib/asset.hpp>
#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include <string>
namespace eosio
{
//properties

//system properties

//system constants
#define SYSTEM_PROP_START 250

uint64_t prop_mkprimary(account_name owner, uint8_t prop)
{
    return owner + 1000007L * prop;
}

struct prop_key_value
{
    uint8_t key;
    std::string value;
    EOSLIB_SERIALIZE(prop_key_value, (key)(value))
};

///@abi table
struct userproperty
{
    account_name owner;
    prop_key_value kv;
    uint64_t primary_key() const { return prop_mkprimary(owner, kv.key); }
    EOSLIB_SERIALIZE(userproperty, (owner)(kv))
};

typedef multi_index<N(userproperty), userproperty> userproperty_index;

}; // namespace eosio