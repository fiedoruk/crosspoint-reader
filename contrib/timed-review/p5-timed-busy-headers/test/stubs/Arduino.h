#pragma once
#include <WString.h>

#include <cstddef>
#include <cstdint>
#include <cstring>
inline unsigned long& fakeNow() {
  static unsigned long now = 0;
  return now;
}
inline unsigned long millis() { return fakeNow(); }
inline void delay(unsigned long ms) { fakeNow() += ms; }
class IPAddress {};
