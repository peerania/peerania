#pragma once
#include <eosio/eosio.hpp>
#include <iterator>

namespace std {
template <class Iter>
Iter binary_find(Iter begin, Iter end, int id) {
  Iter it;
  auto count = distance(begin, end);
  while (count > 0) {
    it = begin;
    auto step = count / 2;
    advance(it, step);
    if (it->bkey() < id) {
      begin = ++it;
      count -= step + 1;
    } else
      count = step;
  }
  if (begin != end && begin->bkey() == id) return begin;
  return end;
}

template <class Iter, typename t_key>
Iter linear_find(Iter begin, Iter end, t_key key) {
  while (begin != end) {
    if (begin->lkey() == key) return begin;
    begin++;
  }
  return end;
}
}  // namespace std

// Replace with more strict
inline void assert_ipfs(const std::string &ipfs_link) {
  eosio::check(ipfs_link.size() >= 2 && ipfs_link.size() < 65,
               "Incorrect ipfs");
}

template <typename table_index>
uint64_t get_reversive_pk(const table_index &table, uint64_t max_pk) {
  if (table.begin() == table.end()) {
    return max_pk;
  } else {
    // largest primary key currently in table
    auto pk = table.begin()->primary_key();
    eosio::check(pk > 0, "No available primary key");
    return --pk;
  }
}

template <typename table_index>
uint64_t get_direct_pk(const table_index &table, uint64_t max_pk) {
  if (table.begin() == table.end()) {
    return 1;
  } else {
    // largest primary key currently in table
    auto pk = table.rbegin()->primary_key();
    eosio::check(pk < max_pk, "No available primary key");
    return ++pk;
  }
}