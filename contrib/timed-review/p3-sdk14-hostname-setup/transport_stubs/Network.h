#pragma once
#include "Client.h"

// DNS is a fixture boundary: WiFiClient routes every host to loopback, while
// SecureClient still uses the requested host for SNI and peer-name verification.
struct NetworkStub {
  int hostByName(const char*, IPAddress&) { return 1; }
};
inline NetworkStub Network;
