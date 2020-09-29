#include "telegram_account.hpp"

void peeranha::approve_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);

  telegram_account_table.modify(
      iter_telegram_account, _self, [](auto &telegram_account) {
        telegram_account.confirmed = 1;
      });
  // auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  // for(auto iter_telegram_account_user_id = telegram_account_table_user_id.begin(); iter_telegram_account_user_id != telegram_account_table_user_id.end(); ++iter_telegram_account_user_id) {
  //   if (iter_telegram_account_user_id->confirmed == 2) {
  //     swap_account(iter_telegram_account_user_id->telegram_id);
  //   }
  // }
}

void peeranha::disapprove_account(eosio::name user) { 
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);

  telegram_account_table.erase(iter_telegram_account);
}

void peeranha::add_telegram_account(eosio::name user, uint64_t telegram_id, bool new_account) { 
  find_account(user);
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts);
  auto iter_telegram_account = telegram_account_table.find(user.value);
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);

  eosio::check(iter_telegram_account == telegram_account_table.end(), "This telos account already has a Telegram account");
  eosio::check(iter_telegram_account_user_id == telegram_account_table_user_id.end() || iter_telegram_account_user_id->confirmed == 2, "This Telegram account already has a telos account");

  telegram_account_table.emplace(
    _self, [&user, telegram_id, new_account](auto &telegram_account) {
      telegram_account.user = user;
      telegram_account.telegram_id = telegram_id;
      telegram_account.confirmed = 0;
      if (new_account) {
        telegram_account.confirmed = 2;
      }
    });
}

void peeranha::telegram_post_question(uint64_t telegram_id, uint16_t community_id,
                            std::vector<uint32_t> tags, std::string title,
                            IpfsHash ipfs_link, const uint8_t type) {
  telegram_account_index telegram_account_table(_self, scope_all_telegram_accounts); 
  auto telegram_account_table_user_id = telegram_account_table.get_index<"userid"_n>();
  auto iter_telegram_account_user_id = telegram_account_table_user_id.find(telegram_id);
  
  eosio::name user;
  if (iter_telegram_account_user_id != telegram_account_table_user_id.end()) {
    bool check = iter_telegram_account_user_id->confirmed == 1 ||iter_telegram_account_user_id->confirmed == 2;
    eosio::check(check, "Account not confirmed"); // add text error
    user = iter_telegram_account_user_id->user;
  } else {
    std::string new_account = "TelegramAccount" + std::to_string(telegram_id);
    user = eosio::name(new_account);

    const IpfsHash ipfs_profile = {18, 146, 53, 121, 7, 101, 88, 171, 43, 255, 166, 154, 112, 155, 254, 238, 241, 197, 250, 5, 183, 51, 57, 127, 15, 44, 227, 202, 75, 179, 99, 224, 50};
    const IpfsHash ipfs_avatar = {18, 254, 86, 251, 60, 165, 231, 126, 138, 64, 117, 29, 190, 91, 185, 94, 90, 25, 235, 76, 6, 26, 74, 178, 119, 211, 158, 57, 68, 171, 203, 116, 79};
    register_account(user, new_account, ipfs_avatar, ipfs_avatar);
    add_telegram_account(user, telegram_id, true);
  }
  
  post_question(user, community_id, tags, title, ipfs_link, type);
}

// void peeranha::swap_account(int telegram_id) {

// }