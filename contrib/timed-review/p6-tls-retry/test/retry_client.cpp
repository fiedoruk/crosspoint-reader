#include <SecureClient.h>
#include <wolfssl/error-ssl.h>
#include <wolfssl/internal.h>
#include <wolfssl/ssl.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iterator>
#include <string>

static std::string mode;
static unsigned handshakes = 0;
static bool injected = false;
extern "C" int p6Domain(WOLFSSL* ssl, const char* host) {
  if (mode == "setup") {
    ssl->error = MEMORY_ERROR;
    return WOLFSSL_FAILURE;
  }
  return wolfSSL_check_domain_name(ssl, host);
}
extern "C" int p6Connect(WOLFSSL* ssl) {
  ++handshakes;
  if (mode == "timeout" || ((mode == "cancel-second" || mode == "budget-second") && injected)) {
    if (mode == "budget-second") delay(40);
    ssl->error = WANT_READ;
    return WOLFSSL_FATAL_ERROR;
  }
  if (!injected && (mode == "fallback" || mode == "cancel" || mode == "budget" || mode == "cancel-second" ||
                    mode == "budget-second")) {
    injected = true;
    // Inject a failed first negotiation; the second handshake is real TLS.
    ssl->error = VERSION_ERROR;
    if (mode == "budget") delay(40);
    return WOLFSSL_FATAL_ERROR;
  }
  return wolfSSL_connect(ssl);
}
int main(int argc, char** argv) {
  if (argc != 6) return 2;
  mode = argv[3];
  std::ifstream file(argv[2]);
  const std::string ca{std::istreambuf_iterator<char>(file), {}};
  freeink::SecureClient client;
  client.setTimeout(50);
  client.setCACert(ca.c_str());
  const auto start = millis();
  if (mode == "cancel-second") client.setAbortCallback([] { return handshakes >= 2; });
  if (mode == "cancel") client.setAbortCallback([] { return injected; });
  if (mode == "budget" || mode == "budget-second") client.setAbortCallback([start] { return millis() - start >= 30; });
  bool ok = client.connect("good.test", static_cast<uint16_t>(std::atoi(argv[1]))) == 1;
  if (ok) {
    const char request[] = "GET /G10_PROTECTED/P6 HTTP/1.1\r\nHost: good.test\r\nConnection: close\r\n\r\n";
    client.write(reinterpret_cast<const uint8_t*>(request), sizeof(request) - 1);
    const auto end = millis() + 1000;
    uint8_t buffer[256];
    while (millis() < end && client.connected()) {
      if (client.read(buffer, sizeof(buffer)) < 0) break;
      delay(1);
    }
  }
  const unsigned attempts = p6TcpAttempts, calls = handshakes;
  const bool aborted = client.aborted();
  client.stop();
  const bool closed = !client.connected() && p6OpenSockets == 0;
  mode = "normal";
  client.setAbortCallback(nullptr);
  // Reuse the same object with a good CA and endpoint after every failure.
  std::ifstream goodFile(argv[4]);
  const std::string goodCA{std::istreambuf_iterator<char>(goodFile), {}};
  client.setCACert(goodCA.c_str());
  client.setTimeout(1000);
  const bool recovered = client.connect("good.test", static_cast<uint16_t>(std::atoi(argv[5]))) == 1;
  client.stop();
  printf(
      "{\"connected\":%s,\"tcp\":%u,\"handshakes\":%u,\"aborted\":%s,\"closed\":%s,\"recovered\":%s,\"open_sockets\":%"
      "d}\n",
      ok ? "true" : "false", attempts, calls, aborted ? "true" : "false", closed ? "true" : "false",
      recovered ? "true" : "false", p6OpenSockets);
}
