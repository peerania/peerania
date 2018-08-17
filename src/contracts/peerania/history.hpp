#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp>

//Flags
#define HISTORY_UPVOTED 1
#define HISTORY_DOWNVOTED 2
#define HISTORY_ALREADY_ANSWERED 4

//Macros
#define setFlag(var, flg) var |= flg
#define rmFalg(var, flg) var &= ~flg
#define isFlagSet(var, flg) (var & flg)

typedef uint32_t flag_type;

//Is id generated one by one? If true we have uint_48 questions it is 2.8e14
uint64_t hash_history(uint64_t question_id, uint16_t answer_id){
    return (question_id << 16) + answer_id;
}

///@abi table history
struct history_item{
    uint64_t hash_id;
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

    uint64_t primary_key() const { return hash_id; }
    EOSLIB_SERIALIZE(history_item, (hash_id)(flag))
};

typedef eosio::multi_index<N(history), history_item> history;
