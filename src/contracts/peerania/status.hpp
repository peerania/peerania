#pragma once
#include <eosiolib/name.hpp>
#include "economy.h"
/*
1 - Stranger - 0
100 - Newbie - 1
500 - Junior Resident - 5
1000 - Resident - 10
2500 - Senior Resident - 25
5000 - Hero Resident - 50
10000 - Legendary Resident - 100
*/

#define STATUS0(X) \
  case 0 ... 99:   \
    return (X)
#define STATUS1(X)  \
  case 100 ... 499: \
    return (X)
#define STATUS2(X)  \
  case 500 ... 999: \
    return (X)
#define STATUS3(X)    \
  case 1000 ... 2499: \
    return (X)
#define STATUS4(X)    \
  case 2500 ... 4999: \
    return (X)
#define STATUS5(X)    \
  case 5000 ... 9999: \
    return (X)
#define STATUS6(X) \
  default:         \
    return (X)

uint16_t status_energy(int rating){
  if (rating < 0) return 0;
  switch (rating) {
    STATUS0(50);
    STATUS1(100);
    STATUS2(200);
    STATUS3(300);
    STATUS4(400);
    STATUS5(500);
    STATUS6(600);
  }
}

uint8_t status_moderation_impact(int rating) {
  if (rating < 100) return 0;
  switch (rating) {
    STATUS1(1);
    STATUS2(2);
    STATUS3(3);
    STATUS4(4);
    STATUS5(5);
    STATUS6(6);
  }
}