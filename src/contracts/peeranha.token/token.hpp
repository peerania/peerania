/**
 *  @file
 *  @copyright defined in eos/LICENSE.txt
 */
#pragma once
#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <string>
#include "account.hpp"
#include "bounty.hpp"
#include "peeranha_types.h"
#include "token_period.hpp"
#include "../peeranha.main/question_container.hpp"
#include "../peeranha.main/communities_and_tags.hpp"


namespace eosio {

using std::string;

#if STAGE == 2
struct [[
  eosio::table("dbginfl"), eosio::contract("peeranha.token")
]] dbginfl {
  uint64_t id;
  asset inflation;
  uint64_t primary_key() const { return id; }
};
typedef eosio::multi_index<eosio::name("dbginfl"), dbginfl> dbginfl_index;
#endif

#include "token_common.hpp"

class[[eosio::contract("peeranha.token")]] token : public contract {
 public:
  token(eosio::name receiver, eosio::name code,
        eosio::datastream<const char *> ds)
      : contract(receiver, code, ds) {};
  name peeranha_main = name("peeranhamain");
  [[eosio::action]] void create(name issuer, asset maximum_supply);

  [[eosio::action]] void issue(name to, asset quantity, string memo);

  [[eosio::action]] void retire(asset quantity, string memo);

  [[eosio::action]] void transfer(name from, name to, asset quantity,
                                  string memo);

  [[eosio::action]] void open(name user, const symbol &symbol, name ram_payer);

  [[eosio::action]] void close(name user, const symbol &symbol);

  [[eosio::action]] void pickupreward(name user, const uint16_t period);

  [[eosio::action]] void inviteuser(name inviter, name invited_user);

  [[eosio::action]] void addboost(name user, asset tokens);

  void update_statistics_boost(asset tokens, name user);
  
  void get_value_statistic_boost(asset &new_tokens, asset &max_stake, name &user_max_stake, name user);

  int64_t getstakedbalance(name user);

  uint64_t getvalboost(name user, uint64_t period);

  asset get_award(uint64_t rating_to_award, uint32_t total_rating_to_reward, uint64_t period);

  [[eosio::action]] void setbounty(name user, asset bounty, uint64_t question_id, uint64_t timestamp);

  [[eosio::action]] void editbounty(name user, asset bounty, uint64_t question_id, uint64_t timestamp);

  [[eosio::action]] void paybounty(name user, uint64_t question_id, uint8_t on_delete);

  [[eosio::action]] void rewardrefer(name invited_user);

  [[eosio::action]] void addhotquestn(name user, uint64_t question_id, int hours);

  [[eosio::action]] void delhotquestn(name user, uint64_t question_id);

  [[eosio::action]] void payforcpu(){};

  static asset get_supply(name token_contract_account, symbol_code sym_code) {

    stats statstable(token_contract_account, sym_code.raw());
    const auto &st = statstable.get(sym_code.raw());
    return st.supply;
  }

  static asset get_balance(name token_contract_account, name user,
                           symbol_code sym_code) {
    accounts accountstable(token_contract_account, user.value);
    const auto &ac = accountstable.get(sym_code.raw());
    return ac.balance;
  }

#if STAGE == 1 || STAGE == 2
  [[eosio::action]] void resettables();

#if STAGE == 2
  [[eosio::action("mapcrrwpool")]] void mapcrrwpool(
      uint64_t id, uint16_t period, int total_rating) {
    auto dbginfl_table = dbginfl_index(_self, scope_all_constants);
    auto inflation = create_reward_pool(period, total_rating);
    dbginfl_table.emplace(_self, [inflation, id](auto &dbginfl) {
      dbginfl.id = id;
      dbginfl.inflation = inflation;
    });
  }
#endif

#endif

  protected : const string peeranha_asset_symbol = "PEER";

  struct [[
    eosio::table("account"), eosio::contract("peeranha.token")
  ]] account {
    asset balance;

    uint64_t primary_key() const { return balance.symbol.code().raw(); }
  };

  struct [[
    eosio::table("stat"), , eosio::contract("peeranha.token")
  ]] currency_stats {
    asset supply;
    asset max_supply;
    asset user_supply;
    asset user_max_supply;
    asset funding_supply;
    asset funding_max_supply;
    name issuer;

    uint64_t primary_key() const { return supply.symbol.code().raw(); }
  };

  // scoped by allinvited
  const uint64_t all_invited = name("allinvited").value;
  struct [[
    eosio::table("invited"), , eosio::contract("peeranha.token")
  ]] invited_users {

    name invited_user;
    name inviter;
    asset common_reward;

    uint64_t primary_key() const { return invited_user.value; }
  };
  typedef eosio::multi_index<"invited"_n, invited_users> invited_users_index;

struct [[eosio::table("promquestion"), eosio::contract("peeranha.token")]] promoted_questions {
  uint64_t question_id;
  time start_time;
  time ends_time;

  uint64_t primary_key() const { return question_id; }
};
typedef eosio::multi_index<"promquestion"_n, promoted_questions> promoted_questions_index;

struct [[eosio::table("tokenawards"), eosio::contract("peeranha.token")]] token_awards {
  asset sum_token;
  uint64_t period;

  uint64_t primary_key() const { return period; }
};
typedef eosio::multi_index<"tokenawards"_n, token_awards> token_awards_index;
const uint64_t scope_all_token_awards = eosio::name("allawards").value;

  typedef eosio::multi_index<"accounts"_n, account> accounts;
  typedef eosio::multi_index<"stat"_n, currency_stats> stats;

  void sub_balance(name user, asset value);
  void add_balance(name user, asset value, name ram_payer);
  void return_promoted_tokens(promoted_questions_index::const_iterator &iter_promoted_questions, name user);

  asset create_reward_pool(uint16_t period, int total_rating);
  asset get_user_reward(asset total_reward, int rating_to_reward,
                        int total_rating);
};

}  // namespace eosio