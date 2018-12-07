#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>
#include <string>
#include <vector>
#include "history.hpp"
#include "status.hpp"


#define ID_CREATE_COMMUNITY 0

#define MODERATION_POINTS_CREATE_COMMUNITY 5
#define MODERATION_POINTS_CREATE_TAG 2

#define MAX_TAG_COMMUNITY_CREATE_ID 0xFFFFFFFF
#define MAX_TAG_COUNT 5

#define MAX_COMMUNITY_ID 0xFFFF
#define MAX_TAG_ID 0xFFFFFFFF

struct [[eosio::table("crttagcomm")]] crttagcomm {
  uint32_t id;
  eosio::name creator;
  std::string name;
  std::string ipfs_description;
  int32_t rating;
  std::vector<eosio::name> voted;
  uint64_t primary_key() const {
    return id;
  }
};
typedef eosio::multi_index<"crttagcomm"_n, crttagcomm> create_tag_community_index;
const uint64_t scope_all_communities = "allcomm"_n.value;


struct [[eosio::table("tagandcomm")]] tagandcomm {
  uint32_t id;
  std::string name;
  std::string ipfs_description;
  uint32_t popularity;
  uint64_t primary_key() const {
    return id;
  }
};

typedef eosio::multi_index<"tagandcomm"_n, tagandcomm> tag_community_index;


void assert_tag_name(const std::string name) {
  eosio_assert(name.size() >= 2 && name.size() < 15, "Invalid tag name");
}

void assert_community_name(const std::string name) {
  eosio_assert(name.size() >= 2 && name.size() < 25, "Invalid tag name");
}


