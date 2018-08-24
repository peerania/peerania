#pragma once

#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>

//Flags
#define HISTORY_UPVOTED_FLG 1        //0b0000000000000001
#define HISTORY_DOWNVOTED_FLG 2      //0b0000000000000010
#define HISTORY_DELETE_VOTED_FLG 4   //0b0000000000000100

/**
 * Bit description
 * |  15-3  |      2     |    1    |   0   |
 * |Reserved|DELETE_VOTED|DOWNVOTED|UPVOTED|
 */

typedef uint16_t flag_type;
uint8_t get_count_of_codes(flag_type mask, uint8_t offset){
    return (mask >> offset) + 1;
} 

struct history_item{
    account_name user;
    flag_type flag = 0;
    void set_flag(flag_type flg){
        flag |= flg;
    }

    void remove_flag(flag_type flg){
        flag &= ~flg;
    }

    bool is_flag_set(flag_type flg) const {
        return flag & flg;
    }
    
    bool is_empty() const {
        return flag == 0;
    }

    account_name lkey() const {
        return user;
    }
};