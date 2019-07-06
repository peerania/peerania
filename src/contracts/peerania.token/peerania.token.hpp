/**
 *  @file
 *  @copyright defined in eos/LICENSE.txt
 */
#pragma once

#include <eosio/eosio.hpp>
#include <eosio/system.hpp>
#include <string>
#include "peerania.token.period.hpp"
#include "peerania_types.h"
#include "token_common.hpp"

namespace eosio {

using std::string;

class[[eosio::contract("peerania.tkn")]] token : public contract {
 public:
  token(eosio::name receiver, eosio::name code,
        eosio::datastream<const char*> ds)
      : contract(receiver, code, ds){};
  name peerania_main = name("peerania.dev");
  [[eosio::action]] void create(name issuer, asset maximum_supply);

  [[eosio::action]] void issue(name to, asset quantity, string memo);

  [[eosio::action]] void retire(asset quantity, string memo);

  [[eosio::action]] void transfer(name from, name to, asset quantity,
                                  string memo);

  [[eosio::action]] void open(name user, const symbol& symbol, name ram_payer);

  [[eosio::action]] void close(name user, const symbol& symbol);

  [[eosio::action]] void pickupreward(name user, const uint16_t period);

  static asset get_supply(name token_contract_account, symbol_code sym_code) {
    stats statstable(token_contract_account, sym_code.raw());
    const auto& st = statstable.get(sym_code.raw());
    return st.supply;
  }

  static asset get_balance(name token_contract_account, name user,
                           symbol_code sym_code) {
    accounts accountstable(token_contract_account, user.value);
    const auto& ac = accountstable.get(sym_code.raw());
    return ac.balance;
  }

 protected:
  const string peerania_asset_symbol = "PEER";

  struct [[eosio::table]] account {
    asset balance;

    uint64_t primary_key() const { return balance.symbol.code().raw(); }
  };

  struct [[eosio::table]] currency_stats {
    asset supply;
    asset max_supply;
    name issuer;

    uint64_t primary_key() const { return supply.symbol.code().raw(); }
  };

  typedef eosio::multi_index<"accounts"_n, account> accounts;
  typedef eosio::multi_index<"stat"_n, currency_stats> stats;

  void sub_balance(name user, asset value);
  void add_balance(name user, asset value, name ram_payer);

 private:
  asset get_inflation(uint16_t period);
  asset get_reward(asset total_reward, int rating_to_reward, int total_rating);
};

}  // namespace eosio