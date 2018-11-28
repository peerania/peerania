#pragma once
#include <eosiolib/eosio.hpp>
#include <eosiolib/name.hpp>
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

//Replace with more strict
inline void assert_ipfs(const std::string &ipfs_link){
  eosio_assert(ipfs_link.size() >= 2 && ipfs_link.size() < 65, "Incorrect ipfs");
}

inline void assert_title(const std::string &title){
  eosio_assert(title.size() > 2 && title.size() < 129, "Invalid title length");
}