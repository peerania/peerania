#include "telegram_account.hpp"

void peeranha::approve_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);

  telegram_account_table.modify(
      iter_telegram_account, _self, [](auto &telegram_account) {
        telegram_account.confirmed = true;
      });
}

void peeranha::disapprove_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);

  telegram_account_table.erase(iter_telegram_account);
}

void peeranha::add_telegram_account(eosio::name user, uint64_t telegram_id) { 
  find_account(user);
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);

  eosio::check(iter_telegram_account == telegram_account_table.end(), "This telos account already has a Telegram account");
  eosio::check(iter_telegram_account_user_id == telegram_account_table_user_id.end(), "This Telegram account already has a telos account");

  telegram_account_table.emplace(
    _self, [&user, telegram_id](auto &telegram_account) {
      telegram_account.user = user;
      telegram_account.telegram_id = telegram_id;
      telegram_account.confirmed = false;
    });
}