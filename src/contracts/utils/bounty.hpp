#pragma once
#include <eosio/eosio.hpp>
#include <eosio/system.hpp>
#include <string>

const uint64_t scope_all_bounties = eosio::name("allbounties").value;
const uint64_t scope_all_user_bounties = eosio::name("userbounties").value;

struct [[
    eosio::table("bounty"), eosio::contract("peeranha.token")
]]  bounty {
    eosio::name user;
    eosio::asset amount;
    uint64_t question_id;
    uint8_t status;
    uint64_t timestamp;

    uint64_t primary_key() const { return question_id; }

    EOSLIB_SERIALIZE(
              bounty,
              (user)(amount)(question_id)(status)(timestamp))
};

  typedef eosio::multi_index<"bounty"_n, bounty> question_bounty;