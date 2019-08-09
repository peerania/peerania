#pragma once
#include <eosio/system.hpp>

typedef uint32_t time;

time now(){
    return eosio::current_time_point().sec_since_epoch();
}
