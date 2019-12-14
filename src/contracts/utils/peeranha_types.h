#pragma once
#include <eosio/system.hpp>
#include <string>
typedef uint32_t time;

time now(){
    return eosio::current_time_point().sec_since_epoch();
}

inline void assert_readble_string(const std::string &str, int min_len, int max_len, const char* message){
    bool ok = true;
    int str_len = str.size();
    if (str_len < min_len || str_len > max_len){
        ok = false;
    } else if (std::isspace(str[0]) || std::isspace(str[str.size() - 1])){
        ok = false;
    } else {
        for (int i = 1 ; i < str.size() - 1; ++i){
            if (std::isspace(str[i]) && std::isspace(str[i + 1])){
                ok = false;
            }
        }
    }
    eosio::check(ok, message);
}