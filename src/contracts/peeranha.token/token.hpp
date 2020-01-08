/**
 *  @file
 *  @copyright defined in eos/LICENSE.txt
 */
#pragma once
#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <string>
#include "token_period.hpp"
#include "peeranha_types.h"
#include "token_common.hpp"
#include "account.hpp"

namespace eosio
{

using std::string;

class[[eosio::contract("peeranha.token")]] token : public contract
{
public:
  token(eosio::name receiver, eosio::name code,
        eosio::datastream<const char *> ds)
      : contract(receiver, code, ds){};
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

  [[eosio::action]] void rewardrefer(name invited_user);

  static asset get_supply(name token_contract_account, symbol_code sym_code)
  {
    stats statstable(token_contract_account, sym_code.raw());
    const auto &st = statstable.get(sym_code.raw());
    return st.supply;
  }

  static asset get_balance(name token_contract_account, name user,
                           symbol_code sym_code)
  {
    accounts accountstable(token_contract_account, user.value);
    const auto &ac = accountstable.get(sym_code.raw());
    return ac.balance;
  }

#if STAGE == 1
  [[eosio::action]] void resettables(std::vector<eosio::name> allaccs);
#endif

protected:
  const string peeranha_asset_symbol = "PEER";

  struct [[
    eosio::table("account"), eosio::contract("peeranha.token")
  ]] account
  {
    asset balance;

    uint64_t primary_key() const { return balance.symbol.code().raw(); }
  };

  struct [[
    eosio::table("stat"), , eosio::contract("peeranha.token")
  ]] currency_stats
  {
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
  ]] invited_users
  {
    name invited_user;
    name inviter;
    asset common_reward;

    uint64_t primary_key() const { return invited_user.value; }
  };
  typedef eosio::multi_index<"invited"_n, invited_users> invited_users_index;

  typedef eosio::multi_index<"accounts"_n, account> accounts;
  typedef eosio::multi_index<"stat"_n, currency_stats> stats;

  void sub_balance(name user, asset value);
  void add_balance(name user, asset value, name ram_payer);

  asset create_reward_pool(uint16_t period, int total_rating);
  asset get_user_reward(asset total_reward, int rating_to_reward, int total_rating);
};

} // namespace eosio