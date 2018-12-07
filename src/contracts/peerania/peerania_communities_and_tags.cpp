#include "peerania.hpp"

#define is_create_community(x) ((x) == ID_CREATE_COMMUNITY)

void peerania::update_popularity(uint16_t commuinty_id,
                                 const std::vector<uint32_t> &tags,
                                 bool increase) {
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

void peerania::create_community_or_tag(eosio::name user,
                                       const std::string &name,
                                       const std::string &ipfs_description,
                                       uint16_t commuinty_id) {
  uint64_t scope;
  int8_t moderation_points_create;
  // check if community exist
  auto iter_account = find_account(user);
  if (is_create_community(commuinty_id)) {
    assert_community_name(name);
    assert_allowed(*iter_account, user, Action::CREATE_COMMUNITY);
    scope = scope_all_communities;
    moderation_points_create = MODERATION_POINTS_CREATE_COMMUNITY;
  } else {
    assert_tag_name(name);
    assert_community_exist(commuinty_id);
    scope = get_tag_scope(commuinty_id);
    assert_allowed(*iter_account, user, Action::CREATE_TAG);
    moderation_points_create = MODERATION_POINTS_CREATE_TAG;
  }
  account_table.modify(iter_account, _self, [moderation_points_create](auto &account) {
    account.update();
    eosio_assert(account.moderation_points >= moderation_points_create, "Not enought moderation point");
    account.moderation_points -= moderation_points_create;
  });
  create_tag_community_index create_tag_community_table(_self, scope);
  create_tag_community_table.emplace(
      _self, [&iter_account, &name, &ipfs_description,
              &create_tag_community_table](auto &new_tag_or_community) {
        new_tag_or_community.id = get_reversive_pk(create_tag_community_table,
                                                   MAX_TAG_COMMUNITY_CREATE_ID);
        new_tag_or_community.creator = iter_account->owner;
        new_tag_or_community.name = name;
        new_tag_or_community.ipfs_description = ipfs_description;
        new_tag_or_community.rating = iter_account->rating;
      });
  
}

void peerania::vote_create_community_or_tag(eosio::name user, uint32_t tag_or_community_id,
                                            uint16_t commuinty_id) {
  uint64_t scope;
  // Used to generate primary key, if votes to create enough;
  int32_t rating_to_create;
  // check if community exist
  
  auto iter_account = find_account(user);
  if (is_create_community(commuinty_id)) {
    assert_allowed(*iter_account, user, Action::VOTE_CREATE_COMMUNITY);
    scope = scope_all_communities;
    rating_to_create = TagsAndCommunities::VOTES_TO_CREATE_COMMUNITY;
  } else {
    assert_allowed(*iter_account, user, Action::VOTE_CREATE_TAG);
    assert_community_exist(commuinty_id);
    scope = get_tag_scope(commuinty_id);
    rating_to_create = TagsAndCommunities::VOTES_TO_CREATE_TAG;
  }

  create_tag_community_index create_tag_community_table(_self, scope);
  auto iter_create_or_tag_community = create_tag_community_table.find(tag_or_community_id);
  eosio_assert(iter_create_or_tag_community != create_tag_community_table.end(),
               "Tag or community not found");
  create_tag_community_table.modify(
      iter_create_or_tag_community, _self,
      [&iter_account](auto &tag_or_community) {
        eosio_assert(
            std::find(tag_or_community.voted.begin(),
                      tag_or_community.voted.end(),
                      iter_account->owner) == tag_or_community.voted.end(),
            "You alredy vote this item");
        tag_or_community.voted.push_back(iter_account->owner);
        tag_or_community.rating += iter_account->rating;
      });

  if (iter_create_or_tag_community->rating >= rating_to_create) {
    uint32_t max_pk;
    int16_t reward;
    if (is_create_community(commuinty_id)) {
      max_pk = MAX_COMMUNITY_ID; 
      reward = COMMUNITY_CREATED_REWARD;
    } else {
      max_pk = MAX_TAG_ID; 
      reward = TAG_CREATED_REWARD;
    }
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
    create_tag_community_table.erase(iter_create_or_tag_community);
    eosio_assert(
        iter_create_or_tag_community != create_tag_community_table.end(),
        "Address not erased properly");
    update_rating(iter_account, reward);
  }
}

void peerania::vote_delete_community_or_tag(eosio::name user, uint32_t tag_or_community_id,
                                            uint16_t commuinty_id) {
  uint64_t scope;
  int32_t rating_to_delete;
  // check if community exist
  auto iter_account = find_account(user);
  if (is_create_community(commuinty_id)) {
    assert_allowed(*iter_account, user, Action::VOTE_CREATE_COMMUNITY);
    scope = scope_all_communities;
    rating_to_delete = TagsAndCommunities::VOTES_TO_DELETE_COMMUNITY;
  } else {
    assert_allowed(*iter_account, user, Action::VOTE_CREATE_TAG);
    assert_community_exist(commuinty_id);
    scope = get_tag_scope(commuinty_id);
    rating_to_delete = TagsAndCommunities::VOTES_TO_DELETE_TAG;
  }

  create_tag_community_index create_tag_community_table(_self, scope);
  auto iter_create_or_tag_community = create_tag_community_table.find(tag_or_community_id);
  eosio_assert(iter_create_or_tag_community != create_tag_community_table.end(),
               "Tag or community not found");
  create_tag_community_table.modify(
      iter_create_or_tag_community, _self,
      [&iter_account](auto &tag_or_community) {
        eosio_assert(
            std::find(tag_or_community.voted.begin(),
                      tag_or_community.voted.end(),
                      iter_account->owner) == tag_or_community.voted.end(),
            "You alredy vote this item");
        tag_or_community.voted.push_back(iter_account->owner);
        tag_or_community.rating -= iter_account->rating;
      });

  if (iter_create_or_tag_community->rating <= rating_to_delete) {
    const int16_t reward = is_create_community(commuinty_id)
                               ? COMMUNITY_DELETED_REWARD
                               : TAG_DELETED_REWARD;
    create_tag_community_table.erase(iter_create_or_tag_community);
    eosio_assert(
        iter_create_or_tag_community != create_tag_community_table.end(),
        "Address not erased properly");
    update_rating(iter_account, reward);
  }
}