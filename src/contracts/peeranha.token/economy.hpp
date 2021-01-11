#pragma once

#include <eosio/eosio.hpp>
#include <cmath>

#if STAGE == 1 
#define INFLATION_PERIOD 12 //12 periods (1)
#define START_POOL 350
#define POOL_REDUSE_COEFFICIENT 0.95f
#define RATING_TOKEN_COEFFICIENT 7

#define REFERAL_REWARD 5
#define ONE_HOUR 3600
#elif STAGE == 2
#define INFLATION_PERIOD 2  // 2 secs
#define START_POOL 40
#define POOL_REDUSE_COEFFICIENT 0.5f
#define RATING_TOKEN_COEFFICIENT 8

#define REFERAL_REWARD 10
#define ONE_HOUR 4
#else
#define INFLATION_PERIOD 52 //52 periods(52 weeks)
#define START_POOL 100000
#define POOL_REDUSE_COEFFICIENT 0.9f
#define RATING_TOKEN_COEFFICIENT 10

#define REFERAL_REWARD 200 // The referal program reward
#define ONE_HOUR 3600
#endif

#define TOKEN_PROMOTED_QUESTION 2
#define USER_SHARES 60

#define REFERAL_SPLIT_COEFFICIENT 50  // The percentage passing to inviter


#define REFERAL_TARGET_RATING_REACHED 35

#define TOKEN_PRECISION 6

constexpr inline const int64_t int64_to_peer(const int64_t quantity){
    int64_t peer = quantity;
    for (int i = 0; i < TOKEN_PRECISION; ++i)
        peer *= 10;
    return peer;
}