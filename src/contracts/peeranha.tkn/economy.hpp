#pragma once

#include <eosio/eosio.hpp>
#include <cmath>

#define INFLATION_PERIOD 52 //52 periods(52 weeks)
#define START_POOL 30000
#define POOL_REDUSE_COEFFICIENT 0.9f

#define USER_SHARES 60

#define RATING_TOKEN_COFICIENT 8

#define MAX_SUPPLY 100000000

#define TOKEN_PRECISION 6

constexpr inline const int64_t int64_to_peer(const int64_t quantity){
    int64_t peer = quantity;
    for (int i = 0; i < TOKEN_PRECISION; ++i)
        peer *= 10;
    return peer;
}