#include "peeranha.hpp"

void peeranha::update_community_statistics(uint16_t community_id,
                                           int8_t questions_asked,
                                           int8_t answers_given,
                                           int8_t correct_answers,
                                           int8_t users_subscribed) {
  community_table_index community_table(_self, scope_all_communities);
  auto iter_community = community_table.find(community_id);
  community_table.modify(iter_community, _self,
                         [questions_asked, answers_given, correct_answers,
                          users_subscribed](auto &community) {
                           community.questions_asked += questions_asked;
                           community.answers_given += answers_given;
                           community.correct_answers += correct_answers;
                           community.users_subscribed += users_subscribed;
                         });
}

void peeranha::update_tags_statistics(uint16_t community_id,
                                      std::vector<uint32_t> tags_id,
                                      int8_t questions_asked) {
  tag_table_index tag_table(_self, get_tag_scope(community_id));
  for (auto tag_id_iter = tags_id.begin(); tag_id_iter != tags_id.end();
       tag_id_iter++) {
    auto iter_tag = tag_table.find(*tag_id_iter);
    eosio::check(iter_tag != tag_table.end(), "Tag not found");
    tag_table.modify(iter_tag, _self, [questions_asked](auto &tag) {
      tag.questions_asked += questions_asked;
    });
  }
}

void peeranha::assert_community_exist(uint16_t community_id) {
  community_table_index community_table(_self, scope_all_communities);
  eosio::check(community_table.find(community_id) != community_table.end(),
               "Community not found");
}

void peeranha::assert_community_questions_type(const uint16_t community_id, const uint8_t question_type) {
  community_table_index community_table(_self, scope_all_communities);
  auto iter_community = community_table.find(community_id);
  auto property = get_property_d(iter_community->integer_properties, ID_QUESTIONS_TYPE, ANY_QUESTIONS_TYPE);
  if (property != ANY_QUESTIONS_TYPE){
    eosio::check(property == question_type, "Illegal question type");
  }
}

uint64_t peeranha::get_tag_scope(uint16_t community_id) {
  return scope_all_communities + community_id;
}

void peeranha::create_community(
    eosio::name user, const std::string &name,
    const uint16_t &allowed_question_type,
    const IpfsHash &ipfs_description,
    const std::vector<suggest_tag> &suggested_tags) {
  auto iter_account = find_account(user);
  assert_community_name(name);
  assert_community_type(allowed_question_type);
  assert_ipfs(ipfs_description);
  assert_question_type_allowed(*iter_account, allowed_question_type);
  eosio::check(suggested_tags.size() >= MIN_SUGGESTED_TAG &&
                   suggested_tags.size() <= MAX_SUGGESTED_TAG,
               "Invalid tag count");
  if (iter_account->has_moderation_flag(MODERATOR_FLG_CREATE_COMMUNITY)
          || iter_account->has_invited_blogger_flag()) {
    // Directly create new community with tags
    community_table_index community_table(_self, scope_all_communities);
    uint16_t community_pk = get_direct_pk(community_table, MAX_COMMUNITY_ID);
    community_table.emplace(_self, [&](auto &community) {
      community.id = community_pk;
      community.name = name;
      community.ipfs_description = ipfs_description;
      community.creation_time = now();
      set_property(community.integer_properties, ID_QUESTIONS_TYPE, allowed_question_type);
      community.questions_asked = 0;
      community.answers_given = 0;
      community.correct_answers = 0;
      community.users_subscribed = 0;
    });
    tag_table_index tag_table(_self, get_tag_scope(community_pk));
    for (auto suggested_tag_iter = suggested_tags.begin();
         suggested_tag_iter != suggested_tags.end(); suggested_tag_iter++) {
      uint32_t tag_pk = get_direct_pk(tag_table, MAX_TAG_ID);
      tag_table.emplace(_self, [&suggested_tag_iter, tag_pk](auto &tag) {
        tag.id = tag_pk;
        tag.name = suggested_tag_iter->name;
        tag.ipfs_description = suggested_tag_iter->ipfs_description;
        tag.questions_asked = 0;
      });
    }
    global_stat_index global_stat_table(_self, scope_all_stat);
    auto iter_global_stat = global_stat_table.rbegin();
    eosio::check(iter_global_stat != global_stat_table.rend() &&
                     iter_global_stat->version == version,
                 "Init contract first");
    global_stat_table.modify(
        --global_stat_table.end(), _self,
        [](auto &global_stat) { global_stat.communities_count += 1; });
    if (iter_account->has_invited_blogger_flag()){
      givecommuflg(user, ALL_COMMUNITY_ADMIN_FLG, community_pk);
    }
    return;
    // End
  }
  update_rating(iter_account, 0, [](auto &account) {
    account.reduce_energy(ENERGY_CREATE_COMMUNITY);
  });
  assert_allowed(*iter_account, user, Action::CREATE_COMMUNITY);
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
        new_community.creation_time = now();
      });
}

void peeranha::create_tag(eosio::name user, uint16_t community_id,
                          const std::string &name,
                          const IpfsHash &ipfs_description) {
  auto iter_account = find_account(user);
  assert_tag_name(name);
  assert_community_exist(community_id);
  assert_ipfs(ipfs_description);

  bool check_moderator = iter_account->has_moderation_flag(MODERATOR_FLG_CREATE_TAG);
  bool check_moderator_community = find_account_property_community(user, COMMUNITY_ADMIN_FLG_CREATE_TAG, community_id);
  if (check_moderator || check_moderator_community) {
    tag_table_index tag_table(_self, get_tag_scope(community_id));
    uint32_t tag_pk = get_direct_pk(tag_table, MAX_TAG_ID);
    tag_table.emplace(_self, [&](auto &tag) {
      tag.id = tag_pk;
      tag.name = name;
      tag.ipfs_description = ipfs_description;
      tag.questions_asked = 0;
    });
    return;
  }
  
  update_rating(iter_account, [](auto &account) {
    account.reduce_energy(ENERGY_CREATE_TAG);
  });
  assert_allowed(*iter_account, user, Action::CREATE_TAG, community_id);
  create_tag_index create_tag_table(_self, get_tag_scope(community_id));
  create_tag_table.emplace(_self, [&iter_account, &name, &ipfs_description,
                                   &create_tag_table](auto &new_tag) {
    new_tag.id =
        get_reversive_pk(create_tag_table, MAX_TAG_COMMUNITY_CREATE_ID);
    new_tag.creator = iter_account->user;
    new_tag.name = name;
    new_tag.ipfs_description = ipfs_description;
  });
}

void peeranha::vote_create_community(eosio::name user, uint32_t community_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_CREATE_COMMUNITY);
  update_rating(iter_account, [](auto &account) {
    account.reduce_energy(ENERGY_VOTE_COMMUNITY);
  });
  create_community_index create_community_table(_self, scope_all_communities);
  auto iter_create_community = create_community_table.find(community_id);
  eosio::check(iter_create_community != create_community_table.end(),
               "Community not found");
  eosio::check(iter_create_community->creator != iter_account->user,
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
          eosio::check(false, "Fatal internal error");
        }
      });
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
    eosio::check(iter_create_community != create_community_table.end(),
                 "Address not erased properly");

    global_stat_index global_stat_table(_self, scope_all_stat);
    auto iter_global_stat = global_stat_table.rbegin();
    eosio::check(iter_global_stat != global_stat_table.rend() &&
                     iter_global_stat->version == version,
                 "Init contract first");
    global_stat_table.modify(
        --global_stat_table.end(), _self,
        [](auto &global_stat) { global_stat.communities_count += 1; });
  }
}

void peeranha::vote_create_tag(eosio::name user, uint16_t community_id,
                               uint32_t tag_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_CREATE_TAG, community_id);
  update_rating(iter_account,
                [](auto &account) { account.reduce_energy(ENERGY_VOTE_TAG); });
  create_tag_index create_tag_table(_self, get_tag_scope(community_id));
  auto iter_create_tag = create_tag_table.find(tag_id);
  eosio::check(iter_create_tag != create_tag_table.end(), "Tag not found");
  eosio::check(iter_create_tag->creator != iter_account->user,
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
      eosio::check(false, "Fatal internal error");
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
    eosio::check(iter_create_tag != create_tag_table.end(),
                 "Address not erased properly");
  }
}

void peeranha::vote_delete_community(eosio::name user, uint32_t community_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_DELETE_COMMUNITY);
  update_rating(iter_account, 0, [](auto &account) {
    account.reduce_energy(ENERGY_VOTE_COMMUNITY);
  });
  create_community_index create_community_table(_self, scope_all_communities);
  auto iter_create_community = create_community_table.find(community_id);
  eosio::check(iter_create_community != create_community_table.end(),
               "Community not found");
  if (iter_create_community->creator == iter_account->user) {
    int report_count = (int)iter_create_community->upvotes.size() -
                       (int)iter_create_community->downvotes.size();
    if (report_count < 0) {
      update_rating(iter_account, COMMUNITY_DELETED_REWARD * report_count /
                                      VOTES_TO_DELETE_COMMUNITY);
    }
    create_community_table.erase(iter_create_community);
    eosio::check(iter_create_community != create_community_table.end(),
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
            eosio::check(false, "Fatal internal error");
          }
        });
    if (VOTES_TO_DELETE_COMMUNITY +
            (int)iter_create_community->downvotes.size() >=
        0) {
      update_rating(iter_create_community->creator, COMMUNITY_DELETED_REWARD);
      create_community_table.erase(iter_create_community);
      eosio::check(iter_create_community != create_community_table.end(),
                   "Address not erased properly");
    }
  }
}

void peeranha::vote_delete_tag(eosio::name user, uint16_t community_id,
                               uint32_t tag_id) {
  auto iter_account = find_account(user);
  assert_allowed(*iter_account, user, Action::VOTE_DELETE_TAG, community_id);
  update_rating(iter_account, 0,
                [](auto &account) { account.reduce_energy(ENERGY_VOTE_TAG); });
  create_tag_index create_tag_table(_self, get_tag_scope(community_id));
  auto iter_create_tag = create_tag_table.find(tag_id);
  eosio::check(iter_create_tag != create_tag_table.end(), "Tag not found");
  if (iter_create_tag->creator == iter_account->user) {
    int report_count = (int)iter_create_tag->upvotes.size() -
                       (int)iter_create_tag->downvotes.size();
    if (report_count < 0) {
      update_rating(iter_account,
                    TAG_DELETED_REWARD * report_count / VOTES_TO_DELETE_TAG);
    }
    create_tag_table.erase(iter_create_tag);
    eosio::check(iter_create_tag != create_tag_table.end(),
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
        eosio::check(false, "Fatal internal error");
      }
    });
    if (VOTES_TO_DELETE_TAG + (int)iter_create_tag->downvotes.size() >= 0) {
      update_rating(iter_create_tag->creator, TAG_DELETED_REWARD);
      create_tag_table.erase(iter_create_tag);
      eosio::check(iter_create_tag != create_tag_table.end(),
                   "Address not erased properly");
    }
  }
}

void peeranha::follow_community(eosio::name user, uint16_t community_id) {
  update_community_statistics(community_id, 0, 0, 0, 1);
  auto iter_account = find_account(user);
  eosio::check(
      std::find(iter_account->followed_communities.begin(),
                iter_account->followed_communities.end(),
                community_id) == iter_account->followed_communities.end(),
      "You are already followed this community");
  update_rating(iter_account, [community_id](auto &account) {
    account.reduce_energy(ENERGY_FOLLOW_COMMUNITY);
    account.followed_communities.push_back(community_id);
  });
}

void peeranha::unfollow_community(eosio::name user, uint16_t community_id) {
  update_community_statistics(community_id, 0, 0, 0, -1);
  auto iter_account = find_account(user);
  update_rating(iter_account, [community_id](auto &account) {
    auto community =
        std::find(account.followed_communities.begin(),
                  account.followed_communities.end(), community_id);
    eosio::check(community != account.followed_communities.end(),
                 "You are not followed this community");
    account.followed_communities.erase(community);
  });
}

void peeranha::edit_community(eosio::name user, uint16_t community_id, 
                              const std::string &name, const IpfsHash &ipfs_description, 
                              const uint16_t &type) {
  assert_community_name(name);
  assert_ipfs(ipfs_description);

  auto iter_account = find_account(user);

  eosio::check(iter_account->has_moderation_flag(MODERATOR_FLG_CREATE_COMMUNITY) || 
  find_account_property_community(user, ALL_COMMUNITY_ADMIN_FLG, community_id), "User must to be moderator (FLG_CREATE_COMMUNITY or MODERATION_FLG)");

  community_table_index community_table(_self, scope_all_communities);
  auto iter_community = community_table.find(community_id);
  eosio::check(iter_community != community_table.end(), "Community not found");
  
  community_table.modify(iter_community, _self,
                         [&](auto &community) {
                           community.name = name;
                           community.ipfs_description = ipfs_description;
                           set_property(community.integer_properties, ID_QUESTIONS_TYPE, type);
                         });
}

void peeranha::edit_tag(eosio::name user, uint16_t community_id, 
                        uint32_t tag_id, const std::string &name, 
                        const IpfsHash &ipfs_description) {
  assert_tag_name(name);
  assert_community_exist(community_id);
  assert_ipfs(ipfs_description);

  auto iter_account = find_account(user);
  bool check_moderator = iter_account->has_moderation_flag(MODERATOR_FLG_CREATE_TAG);
  bool check_moderator_community = find_account_property_community(user, COMMUNITY_ADMIN_FLG_CREATE_TAG, community_id);
  eosio::check(check_moderator || check_moderator_community, "User must to be moderator (FLG_CREATE_TAG)");

  tag_table_index tag_table(_self, get_tag_scope(community_id));
  auto iter_tag = tag_table.find(tag_id);
  eosio::check(iter_tag != tag_table.end(), "Tag not found");

  tag_table.modify(iter_tag, _self,
                    [name, ipfs_description](auto &tag) {
                      tag.name = name;
                      tag.ipfs_description = ipfs_description;
                    });
}