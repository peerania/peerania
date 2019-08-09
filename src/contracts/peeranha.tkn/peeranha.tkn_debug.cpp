#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <string>
#include <vector>

#include "peeranha.tkn.period.hpp"
#undef INFLATION_PERIOD
#define INFLATION_PERIOD 2  // 52 periods(52 weeks)
#undef POOL_REDUSE
#define POOL_REDUSE 100000

#undef EOSIO_DISPATCH
#define EOSIO_DISPATCH(MEMBER, TYPES)
#include "peeranha.tkn.cpp"

extern time
    START_PERIOD_TIME;  // We need mechanism which change it once on deploy
extern int PERIOD_LENGTH;
namespace eosio {

using std::string;
class[[eosio::contract("peeranha.tkn")]] token_d : public token {
  using token::token;

 public:
  token_d(eosio::name receiver, eosio::name code,
          eosio::datastream<const char*> ds)
      : token(receiver, code, ds) {
    PERIOD_LENGTH = 3;
    // Initializte some constants for debug
    // could be moved to a separate method
    constants_index all_constants_table(peeranha_main, scope_all_constants);
    auto settings = all_constants_table.rbegin();
    if (settings != all_constants_table.rend())
      START_PERIOD_TIME = settings->start_period_time;
  }
  struct [[
    eosio::table("constants"), eosio::contract("peeranha")
  ]] constants {
    uint64_t id;
    time start_period_time;
    uint64_t primary_key() const { return id; }
    EOSLIB_SERIALIZE(constants, (id)(start_period_time))
  };
  typedef eosio::multi_index<eosio::name("constants"), constants>
      constants_index;

  const uint64_t scope_all_constants = eosio::name("allconstants").value;

  struct [[eosio::table("allaccs")]] allaccs {
    name user;
    uint64_t primary_key() const { return user.value; }
  };
  typedef multi_index<"allaccs"_n, allaccs> allaccs_index;

  [[eosio::action("resettables")]] void resettables() {
    allaccs_index allaccs_table(_self, _self.value);
    auto iter_acc = allaccs_table.begin();
    while (iter_acc != allaccs_table.end()) {
      accounts to_acnts(_self, iter_acc->user.value);
      auto iter_to_acnts = to_acnts.begin();
      while (iter_to_acnts != to_acnts.end()) {
        iter_to_acnts = to_acnts.erase(iter_to_acnts);
      }

      eosio::print("remove data for ", iter_acc->user);
      period_reward_index period_reward_table(_self, iter_acc->user.value);
      auto iter_period_reward = period_reward_table.begin();
      while (iter_period_reward != period_reward_table.end()) {
        iter_period_reward = period_reward_table.erase(iter_period_reward);
      }

      iter_acc = allaccs_table.erase(iter_acc);
    }

    const symbol sym = symbol("PEER", 6);
    stats statstable(_self, sym.code().raw());
    auto existing = statstable.find(sym.code().raw());
    statstable.erase(existing);

    total_reward_index total_reward_table(_self, scope_all_periods);
    auto iter_total_reward = total_reward_table.begin();
    while (iter_total_reward != total_reward_table.end()) {
      iter_total_reward = total_reward_table.erase(iter_total_reward);
    }
  };


  // Stub I think about it later!!!!
  void pickupreward(name user, const uint16_t period) {
    token t(_self, _first_receiver, _ds);
    allaccs_index allaccs_table(_self, _self.value);
    if (allaccs_table.find(user.value) == allaccs_table.end())
      allaccs_table.emplace(_self, [user](auto& a) { a.user = user; });
    t.pickupreward(user, period);
  }
};

}  // namespace eosio

extern "C" {
void apply(uint64_t receiver, uint64_t code, uint64_t action) {
  if (code == receiver) {
    switch (action) {
      EOSIO_DISPATCH_HELPER(eosio::token_d,
                            (create)(issue)(transfer)(open)(close)(retire)(
                                pickupreward)(resettables))
    }
  }
}
}