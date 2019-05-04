#include "peerania.hpp"

void peerania::update_community_statistics(uint16_t community_id,
                                           int8_t questions_asked,
                                           int8_t answers_given,
                                           int8_t correct_answers,
                                           int8_t users_subscribed) {
  community_table_index community_table(_self, scope_all_communities);
  auto iter_community = community_table.find(community_id);
  eosio_assert(iter_community != community_table.end(), "Community not found");
  printf("Call update %d %d", questions_asked, community_id);
  community_table.modify(iter_community, _self,
                         [questions_asked, answers_given, correct_answers,
                          users_subscribed](auto &community) {
                           community.questions_asked += questions_asked;
                           community.answers_given += answers_given;
                           community.correct_answers += correct_answers;
                           community.users_subscribed += users_subscribed;
                         });
}

void peerania::update_tags_statistics(uint16_t community_id,
                                      std::vector<uint32_t> tags_id,
                                      int8_t questions_asked) {
  printf("Call tag statistic update %d %d for:", community_id, questions_asked);
  tag_table_index tag_table(_self, get_tag_scope(community_id));
  for (auto tag_id_iter = tags_id.begin(); tag_id_iter != tags_id.end();
       tag_id_iter++) {
    printf("%d, ", *tag_id_iter);
    auto iter_tag = tag_table.find(*tag_id_iter);
    eosio_assert(iter_tag != tag_table.end(), "Tag not found");
    tag_table.modify(iter_tag, _self, [questions_asked](auto &tag) {
      tag.questions_asked += questions_asked;
    });
  }
}

void peerania::assert_community_exist(uint16_t community_id) {
  community_table_index community_table(_self, scope_all_communities);
  eosio_assert(community_table.find(community_id) != community_table.end(),
               "Community not found");
}

uint64_t peerania::get_tag_scope(uint16_t community_id) {
  return scope_all_communities + community_id;
}

void peerania::create_community(
    eosio::name user, const std::string &name,
    const std::string &ipfs_description,
    const std::vector<suggest_tag> &suggested_tags) {
  assert_community_name(name);
  auto iter_account = find_account(user);
  update_rating(iter_account, 0, [](auto &account) {
    eosio_assert(
        account.moderation_points >= MODERATION_POINTS_CREATE_COMMUNITY,
        "Not enought moderation points");
    account.moderation_points -= MODERATION_POINTS_CREATE_COMMUNITY;
  });
  assert_allowed(*iter_account, user, Action::CREATE_COMMUNITY);
  assert_ipfs(ipfs_description);
  eosio_assert(suggested_tags.size() >= MIN_SUGGESTED_TAG &&
                   suggested_tags.size() <= MAX_SUGGESTED_TAG,
               "Invalid tag count");
  create_community_index create_community_table(_self, scope_all_communities);
  create_community_table.emplace(
      _self, [&iter_account, &name, &ipfs_description, &create_community_table,
              &suggested_tags](auto &new_community) {
        new_community.id = get_reversive_pk(create_community_table,
                                            MAX_TAG_COMMUNITY_CREATE_ID);
        new_community.creator = iter_account->user;
        new_community.name = name;
        new_community.ipfs_description = ipfs_description;
        new_community.suggested_tags = suggested_tags;
      });
}

void peerania::create_tag(eosio::name user, uint16_t commuinty_id,
                          const std::string &name,
                          const std::string &ipfs_description) {
  assert_tag_name(name);
  assert_community_exist(commuinty_id);
  auto iter_account = find_account(user);
  update_rating(iter_account, 0, [](auto &account) {
    eosio_assert(
        account.moderation_points >= MODERATION_POINTS_CREATE_TAG,
        "Not enought moderation points");
    account.moderation_points -= MODERATION_POINTS_CREATE_TAG;
  });
  assert_allowed(*iter_account, user, Action::CREATE_TAG);
  assert_ipfs(ipfs_description);
  create_tag_index create_tag_table(_self, get_tag_scope(commuinty_id));
  create_tag_table.emplace(_self, [&iter_account, &name, &ipfs_description,
                                   &create_tag_table](auto &new_tag) {
    new_tag.id =
        get_reversive_pk(create_tag_table, MAX_TAG_COMMUNITY_CREATE_ID);
    new_tag.creator = iter_account->user;
    new_tag.name = name;
    new_tag.ipfs_description = ipfs_description;
  });
}

void peerania::vote_create_community(eosio::name user, uint32_t community_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_CREATE_COMMUNITY);
  create_community_index create_community_table(_self, scope_all_communities);
  auto iter_create_community = create_community_table.find(community_id);
  eosio_assert(iter_create_community != create_community_table.end(),
               "Community not found");
  eosio_assert(iter_create_community->creator != iter_account->user,
               "You can't vote own item");
  create_community_table.modify(
      iter_create_community, _self, [&iter_account](auto &community) {
        auto iter_upvoter =
            std::find(community.upvotes.begin(), community.upvotes.end(),
                      iter_account->user);
        auto iter_downvoter =
            std::find(community.downvotes.begin(), community.downvotes.end(),
                      iter_account->user);
        if (iter_upvoter == community.upvotes.end() &&
            iter_downvoter == community.downvotes.end()) {
          community.upvotes.push_back(iter_account->user);
        } else if (iter_upvoter != community.upvotes.end() &&
                   iter_downvoter == community.downvotes.end()) {
          community.upvotes.erase(iter_upvoter);
        } else if (iter_upvoter == community.upvotes.end() &&
                   iter_downvoter != community.downvotes.end()) {
          community.downvotes.erase(iter_downvoter);
          community.upvotes.push_back(iter_account->user);
        } else {
          eosio_assert(false, "Fatal internal error");
        }
      });
  // add tag transfer
  if (iter_create_community->upvotes.size() >= VOTES_TO_CREATE_COMMUNITY) {
    community_table_index community_table(_self, scope_all_communities);
    uint16_t community_pk = get_direct_pk(community_table, MAX_COMMUNITY_ID);
    community_table.emplace(
        _self, [&iter_create_community, community_pk](auto &community) {
          community.id = community_pk;
          community.name = iter_create_community->name;
          community.ipfs_description = iter_create_community->ipfs_description;
          community.creation_time = now();
          community.questions_asked = 0;
          community.answers_given = 0;
          community.correct_answers = 0;
          community.users_subscribed = 0;
        });
    tag_table_index tag_table(_self, get_tag_scope(community_pk));
    for (auto suggested_tag_iter =
             iter_create_community->suggested_tags.begin();
         suggested_tag_iter != iter_create_community->suggested_tags.end();
         suggested_tag_iter++) {
      uint32_t tag_pk = get_direct_pk(tag_table, MAX_TAG_ID);
      tag_table.emplace(_self, [&suggested_tag_iter, tag_pk](auto &tag) {
        tag.id = tag_pk;
        tag.name = suggested_tag_iter->name;
        tag.ipfs_description = suggested_tag_iter->ipfs_description;
        tag.questions_asked = 0;
      });
    }
    update_rating(iter_create_community->creator, COMMUNITY_CREATED_REWARD);
    create_community_table.erase(iter_create_community);
    eosio_assert(iter_create_community != create_community_table.end(),
                 "Address not erased properly");
  }
}

void peerania::vote_create_tag(eosio::name user, uint16_t community_id,
                               uint32_t tag_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_CREATE_TAG);
  create_tag_index create_tag_table(_self, get_tag_scope(community_id));
  auto iter_create_tag = create_tag_table.find(tag_id);
  eosio_assert(iter_create_tag != create_tag_table.end(), "Tag not found");
  eosio_assert(iter_create_tag->creator != iter_account->user,
               "You can't vote own item");
  create_tag_table.modify(iter_create_tag, _self, [&iter_account](auto &tag) {
    auto iter_upvoter =
        std::find(tag.upvotes.begin(), tag.upvotes.end(), iter_account->user);
    auto iter_downvoter = std::find(tag.downvotes.begin(), tag.downvotes.end(),
                                    iter_account->user);
    if (iter_upvoter == tag.upvotes.end() &&
        iter_downvoter == tag.downvotes.end()) {
      tag.upvotes.push_back(iter_account->user);
    } else if (iter_upvoter != tag.upvotes.end() &&
               iter_downvoter == tag.downvotes.end()) {
      tag.upvotes.erase(iter_upvoter);
    } else if (iter_upvoter == tag.upvotes.end() &&
               iter_downvoter != tag.downvotes.end()) {
      tag.downvotes.erase(iter_downvoter);
      tag.upvotes.push_back(iter_account->user);
    } else {
      eosio_assert(false, "Fatal internal error");
    }
  });
  if (iter_create_tag->upvotes.size() >= VOTES_TO_CREATE_TAG) {
    tag_table_index tag_table(_self, get_tag_scope(community_id));
    uint32_t tag_pk = get_direct_pk(tag_table, MAX_TAG_ID);
    tag_table.emplace(_self, [&iter_create_tag, tag_pk](auto &tag) {
      tag.id = tag_pk;
      tag.name = iter_create_tag->name;
      tag.ipfs_description = iter_create_tag->ipfs_description;
      tag.questions_asked = 0;
    });
    update_rating(iter_create_tag->creator, TAG_CREATED_REWARD);
    create_tag_table.erase(iter_create_tag);
    eosio_assert(iter_create_tag != create_tag_table.end(),
                 "Address not erased properly");
  }
}

void peerania::vote_delete_community(eosio::name user, uint32_t community_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_DELETE_COMMUNITY);
  create_community_index create_community_table(_self, scope_all_communities);
  auto iter_create_community = create_community_table.find(community_id);
  eosio_assert(iter_create_community != create_community_table.end(),
               "Community not found");
  if (iter_create_community->creator == iter_account->user) {
    int report_count = (int)iter_create_community->upvotes.size() -
                       (int)iter_create_community->downvotes.size();
    if (report_count < 0) {
      update_rating(iter_account, COMMUNITY_DELETED_REWARD * report_count /
                                      VOTES_TO_DELETE_COMMUNITY);
    }
    create_community_table.erase(iter_create_community);
    eosio_assert(iter_create_community != create_community_table.end(),
                 "Address not erased properly");
  } else {
    create_community_table.modify(
        iter_create_community, _self, [&iter_account](auto &community) {
          auto iter_upvoter =
              std::find(community.upvotes.begin(), community.upvotes.end(),
                        iter_account->user);
          auto iter_downvoter =
              std::find(community.downvotes.begin(), community.downvotes.end(),
                        iter_account->user);
          if (iter_upvoter == community.upvotes.end() &&
              iter_downvoter == community.downvotes.end()) {
            community.downvotes.push_back(iter_account->user);
          } else if (iter_upvoter == community.upvotes.end() &&
                     iter_downvoter != community.downvotes.end()) {
            community.downvotes.erase(iter_downvoter);
          } else if (iter_upvoter != community.upvotes.end() &&
                     iter_downvoter == community.downvotes.end()) {
            community.upvotes.erase(iter_upvoter);
            community.downvotes.push_back(iter_account->user);
          } else {
            eosio_assert(false, "Fatal internal error");
          }
        });
    //printf("Delete community %d %d %d", iter_create_community->downvotes.size(), VOTES_TO_DELETE_COMMUNITY, (VOTES_TO_DELETE_COMMUNITY + iter_create_community->downvotes.size()) > -1);
    if (VOTES_TO_DELETE_COMMUNITY + (int)iter_create_community->downvotes.size() >=0) {
      update_rating(iter_create_community->creator, COMMUNITY_DELETED_REWARD);
      create_community_table.erase(iter_create_community);
      eosio_assert(iter_create_community != create_community_table.end(),
                   "Address not erased properly");
    }
  }
}

void peerania::vote_delete_tag(eosio::name user, uint16_t community_id,
                               uint32_t tag_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_DELETE_TAG);
  create_tag_index create_tag_table(_self, get_tag_scope(community_id));
  auto iter_create_tag = create_tag_table.find(tag_id);
  eosio_assert(iter_create_tag != create_tag_table.end(), "Tag not found");
  if (iter_create_tag->creator == iter_account->user) {
    int report_count =
        (int)iter_create_tag->upvotes.size() - (int)iter_create_tag->downvotes.size();
    if (report_count < 0) {
      update_rating(iter_account,
                    TAG_DELETED_REWARD * report_count / VOTES_TO_DELETE_TAG);
    }
    create_tag_table.erase(iter_create_tag);
    eosio_assert(iter_create_tag != create_tag_table.end(),
                 "Address not erased properly");
  } else {
    create_tag_table.modify(iter_create_tag, _self, [&iter_account](auto &tag) {
      auto iter_upvoter =
          std::find(tag.upvotes.begin(), tag.upvotes.end(), iter_account->user);
      auto iter_downvoter = std::find(tag.downvotes.begin(),
                                      tag.downvotes.end(), iter_account->user);
      if (iter_upvoter == tag.upvotes.end() &&
          iter_downvoter == tag.downvotes.end()) {
        tag.downvotes.push_back(iter_account->user);
      } else if (iter_upvoter == tag.upvotes.end() &&
                 iter_downvoter != tag.downvotes.end()) {
        tag.downvotes.erase(iter_downvoter);
      } else if (iter_upvoter != tag.upvotes.end() &&
                 iter_downvoter == tag.downvotes.end()) {
        tag.upvotes.erase(iter_upvoter);
        tag.downvotes.push_back(iter_account->user);
      } else {
        eosio_assert(false, "Fatal internal error");
      }
    });
//printf("Delete tag %d %d %d", iter_create_tag->downvotes.size(), VOTES_TO_DELETE_TAG, (VOTES_TO_DELETE_TAG + (int)iter_create_tag->downvotes.size()) > -1);
    if (VOTES_TO_DELETE_TAG + (int)iter_create_tag->downvotes.size() >= 0 ) {
      update_rating(iter_create_tag->creator, TAG_DELETED_REWARD);
      create_tag_table.erase(iter_create_tag);
      eosio_assert(iter_create_tag != create_tag_table.end(),
                   "Address not erased properly");
    }
  }
}

void peerania::follow_community(eosio::name user, uint16_t community_id) {
  update_community_statistics(community_id, 0, 0, 0, 1);
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
  update_community_statistics(community_id, 0, 0, 0, -1);
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