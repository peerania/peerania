#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>
#include "token_common.hpp"

//scoped by N(allperiods)
struct [[eosio::table("rewardpool")]] rewardpool{
    uint16_t period;
    eosio::asset reward;
    uint64_t primary_key() const {
        return period;
    }
};

typedef eosio::multi_index<N(rewardpool), rewardpool> rewardpool_index;
//const scope_name all_periods = N(allperiods);