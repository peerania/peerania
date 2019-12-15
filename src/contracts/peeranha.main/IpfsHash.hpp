#pragma once
#include <vector>

typedef std::vector<uint8_t> IpfsHash;

// Replace with more strict
inline void assert_ipfs(const IpfsHash &ipfs_link) {
  eosio::check(ipfs_link.size() >= 2 && ipfs_link.size() < 48,
               "Incorrect ipfs");
}