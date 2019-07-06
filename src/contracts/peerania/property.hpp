#pragma once

#include <eosio/asset.hpp>
#include <eosio/eosio.hpp>
#include <eosio/name.hpp>
#include <string>
#include "utils.hpp"

// system constants
#define SYSTEM_PROP_START 200

struct str_key_value {
  uint8_t key;
  std::string value;
  uint8_t lkey() const { return key; }
};

struct int_key_value {
  uint8_t key;
  int32_t value;
  uint8_t lkey() const { return key; }
};

template <typename prop_t, typename val_t>
void set_property(std::vector<prop_t> &properties, uint8_t key,
                  const val_t &value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);
  if (itr_property == properties.end()) {
    prop_t key_value;
    key_value.key = key;
    key_value.value = value;
    properties.push_back(key_value);
  } else {
    itr_property->value = value;
  }
}

template <typename prop, typename val_t>
bool get_property(const std::vector<prop> &properties, uint8_t key,
                  const val_t &value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);
  if (itr_property == properties.end()) {
    return false;
    value = itr_property->value;
    return true;
  }
}

template <typename prop_t, typename val_t>
void set_property_d(std::vector<prop_t> &properties, uint8_t key,
                    const val_t &value, val_t default_value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);
  if (itr_property == properties.end()) {
    if (value == default_value) return;
    prop_t key_value;
    key_value.key = key;
    key_value.value = value;
    properties.push_back(key_value);
  } else {
    if (value == default_value)
      properties.erase(itr_property);
    else
      itr_property->value = value;
  }
}

template <typename prop, typename val_t>
val_t get_property_d(const std::vector<prop> &properties, uint8_t key,
                     val_t default_value) {
  auto itr_property = linear_find(properties.begin(), properties.end(), key);
  if (itr_property == properties.end()) return default_value;
  return itr_property->value;
}