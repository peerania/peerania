#include "peeranha.hpp"
#include <stdint.h>

void peeranha::add_configuration(uint64_t key, uint64_t value) {
  configuration_index configuration_table(_self, scope_all_config);
  auto iter_configuration = configuration_table.find(key);
  eosio::check(iter_configuration == configuration_table.end(), "Configuration has already been added");

  configuration_table.emplace(
      _self, [key, value](auto &configuration) {
        configuration.key = key;
        configuration.value = value;
      });
}

uint64_t peeranha::get_configuration(uint64_t key) {
  configuration_index configuration_table(_self, scope_all_config);
  auto iter_configuration = configuration_table.find(key);
  eosio::check(iter_configuration != configuration_table.end(), "Configuration not found");

  return iter_configuration->value;
}

void peeranha::update_configuration(uint64_t key, uint64_t value) {
  configuration_index configuration_table(_self, scope_all_config);
  auto iter_configuration = configuration_table.find(key);
  eosio::check(iter_configuration != configuration_table.end(), "Configuration not found");

  configuration_table.modify(
      iter_configuration, _self, [value](auto &configuration) {
        configuration.value = value;
      });
}