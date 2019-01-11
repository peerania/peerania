#include "peerania.hpp"

void peerania::update_popularity(uint16_t commuinty_id,
                                 const std::vector<uint32_t> &tags,
                                 bool increase) {
  if (increase) {
    eosio_assert(tags.size() <= MAX_TAG_COUNT, "Too many tags");
    // sort - unique
    for (int i = 0; i < tags.size(); ++i)
      for (int j = i + 1; j < tags.size(); ++j)
        if (tags[i] == tags[j]) eosio_assert(false, "Duplicate tag");
  }
  tag_community_index community_table(_self, scope_all_communities);
  auto iter_community = community_table.find(commuinty_id);
  eosio_assert(iter_community != community_table.end(), "Community not found");
  tag_community_index tag_table(_self, get_tag_scope(commuinty_id));
  int8_t popularity_change = increase ? 1 : -1;
  for (auto iter_tag_id = tags.begin(); iter_tag_id != tags.end();
       ++iter_tag_id) {
    auto iter_tag = tag_table.find(*iter_tag_id);
    eosio_assert(iter_tag != tag_table.end(), "Tag not found");
    tag_table.modify(iter_tag, _self, [popularity_change](auto &tag) {
      tag.popularity += popularity_change;
    });
  }
  community_table.modify(iter_community, _self,
                         [popularity_change](auto &community) {
                           community.popularity += popularity_change;
                         });
}

void peerania::assert_community_exist(uint16_t community_id) {
  tag_community_index community_table(_self, scope_all_communities);
  eosio_assert(community_table.find(community_id) != community_table.end(),
               "Community not found");
}

uint64_t peerania::get_tag_scope(uint16_t community_id) {
  return scope_all_communities + community_id;
}

void peerania::create_community(eosio::name user, const std::string &name,
                                const std::string &ipfs_description) {
  assert_community_name(name);
  auto iter_account = find_account(user);
  reduce_moderation_points(iter_account, MODERATION_POINTS_CREATE_COMMUNITY);
  assert_allowed(*iter_account, user, Action::CREATE_COMMUNITY);
  create_community_or_tag(iter_account, scope_all_communities, name,
                          ipfs_description);
}

void peerania::create_tag(eosio::name user, uint16_t commuinty_id,
                          const std::string &name,
                          const std::string &ipfs_description) {
  assert_tag_name(name);
  auto iter_account = find_account(user);
  assert_community_exist(commuinty_id);
  reduce_moderation_points(iter_account, MODERATION_POINTS_CREATE_TAG);
  assert_allowed(*iter_account, user, Action::CREATE_TAG);
  create_community_or_tag(iter_account, get_tag_scope(commuinty_id), name,
                          ipfs_description);
}

void peerania::create_community_or_tag(
    account_index::const_iterator iter_account, uint64_t scope,
    const std::string &name, const std::string &ipfs_description) {
  assert_ipfs(ipfs_description);
  create_tag_community_index create_tag_community_table(_self, scope);
  create_tag_community_table.emplace(
      _self, [&iter_account, &name, &ipfs_description,
              &create_tag_community_table](auto &new_tag_or_community) {
        new_tag_or_community.id = get_reversive_pk(create_tag_community_table,
                                                   MAX_TAG_COMMUNITY_CREATE_ID);
        new_tag_or_community.creator = iter_account->user;
        new_tag_or_community.name = name;
        new_tag_or_community.ipfs_description = ipfs_description;
        new_tag_or_community.votes = 1;
      });
}

void peerania::vote_create_community(eosio::name user, uint32_t community_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_CREATE_COMMUNITY);
  vote_create_comm_or_tag(iter_account, community_id, scope_all_communities,
                          VOTES_TO_CREATE_COMMUNITY, MAX_COMMUNITY_ID,
                          COMMUNITY_CREATED_REWARD);
}

void peerania::vote_create_tag(eosio::name user, uint16_t community_id,
                               uint32_t tag_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_CREATE_TAG);
  assert_community_exist(community_id);
  vote_create_comm_or_tag(iter_account, tag_id, get_tag_scope(community_id),
                          VOTES_TO_CREATE_TAG, MAX_TAG_ID, TAG_CREATED_REWARD);
}

void peerania::vote_create_comm_or_tag(
    account_index::const_iterator iter_account, uint32_t id, uint64_t scope,
    int32_t votes_to_create, uint32_t max_pk, int16_t reward) {
  create_tag_community_index create_tag_community_table(_self, scope);
  auto iter_create_or_tag_community = create_tag_community_table.find(id);
  eosio_assert(iter_create_or_tag_community != create_tag_community_table.end(),
               "Tag or community not found");
  eosio_assert(iter_create_or_tag_community->creator != iter_account->user,
               "You can't vote own item");
  create_tag_community_table.modify(
      iter_create_or_tag_community, _self,
      [&iter_account](auto &tag_or_community) {
        eosio_assert(
            std::find(tag_or_community.voters.begin(),
                      tag_or_community.voters.end(),
                      iter_account->user) == tag_or_community.voters.end(),
            "You already voted for this item");
        tag_or_community.voters.push_back(iter_account->user);
        tag_or_community.votes += 1;
      });
  if (iter_create_or_tag_community->votes >= votes_to_create) {
    uint32_t pk;
    tag_community_index tag_community_table(_self, scope);
    if (tag_community_table.begin() == tag_community_table.end()) {
      pk = 1;
    } else {
      auto iter_pk = --(tag_community_table.end());
      pk = iter_pk->primary_key() + 1;
      eosio_assert(pk < max_pk, "No available primary key");
    }
    tag_community_table.emplace(
        _self, [&iter_create_or_tag_community, pk](auto &tag_or_community) {
          tag_or_community.id = pk;
          tag_or_community.name = iter_create_or_tag_community->name;
          tag_or_community.ipfs_description =
              iter_create_or_tag_community->ipfs_description;
          tag_or_community.popularity = 0;
        });
    update_rating(iter_create_or_tag_community->creator, reward);
    create_tag_community_table.erase(iter_create_or_tag_community);
    eosio_assert(
        iter_create_or_tag_community != create_tag_community_table.end(),
        "Address not erased properly");
  }
}

void peerania::vote_delete_community(eosio::name user, uint32_t community_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_DELETE_COMMUNITY);
  vote_delete_comm_or_tag(iter_account, community_id, scope_all_communities,
                          VOTES_TO_DELETE_COMMUNITY, COMMUNITY_DELETED_REWARD);
}

void peerania::vote_delete_tag(eosio::name user, uint16_t community_id,
                               uint32_t tag_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_DELETE_TAG);
  assert_community_exist(community_id);
  vote_delete_comm_or_tag(iter_account, tag_id, get_tag_scope(community_id),
                          VOTES_TO_DELETE_TAG, TAG_DELETED_REWARD);
}

void peerania::vote_delete_comm_or_tag(
    account_index::const_iterator iter_account, uint32_t id, uint64_t scope,
    int32_t votes_to_delete, int16_t reward) {
  create_tag_community_index create_tag_community_table(_self, scope);
  auto iter_create_or_tag_community = create_tag_community_table.find(id);
  eosio_assert(iter_create_or_tag_community != create_tag_community_table.end(),
               "Tag or community not found");
  if (iter_create_or_tag_community->creator == iter_account->user) {
    if (iter_create_or_tag_community->votes < 0) {
      update_rating(iter_account, reward * iter_create_or_tag_community->votes /
                                      votes_to_delete);
    }
    create_tag_community_table.erase(iter_create_or_tag_community);
    eosio_assert(
        iter_create_or_tag_community != create_tag_community_table.end(),
        "Address not erased properly");
  } else {
    create_tag_community_table.modify(
        iter_create_or_tag_community, _self,
        [&iter_account](auto &tag_or_community) {
          eosio_assert(
              std::find(tag_or_community.voters.begin(),
                        tag_or_community.voters.end(),
                        iter_account->user) == tag_or_community.voters.end(),
              "You already voted for this item");
          tag_or_community.voters.push_back(iter_account->user);
          tag_or_community.votes -= 1;
        });
    if (iter_create_or_tag_community->votes <= votes_to_delete) {
      update_rating(iter_create_or_tag_community->creator, reward);
      eosio_assert(
          iter_create_or_tag_community != create_tag_community_table.end(),
          "Address not erased properly");
    }
  }
}

void peerania::follow_community(eosio::name user, uint16_t community_id) {
  assert_community_exist(community_id);
  auto iter_acc = find_account(user);
  eosio_assert(std::find(iter_acc->followed_communities.begin(),
                         iter_acc->followed_communities.end(),
                         community_id) == iter_acc->followed_communities.end(),
               "You are already followed this community");
  account_table.modify(iter_acc, _self, [community_id](auto &account) {
    account.followed_communities.push_back(community_id);
  });
}

void peerania::unfollow_community(eosio::name user, uint16_t community_id) {
  assert_community_exist(community_id);
  auto iter_acc = find_account(user);
  account_table.modify(iter_acc, _self, [community_id](auto &account) {
    auto community =
        std::find(account.followed_communities.begin(),
                  account.followed_communities.end(), community_id);
    eosio_assert(community != account.followed_communities.end(),
                 "You are not followed this community");
    account.followed_communities.erase(community);             
  });
}