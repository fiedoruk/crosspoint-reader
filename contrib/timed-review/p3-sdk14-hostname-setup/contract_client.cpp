#include <SecureClient.h>
#include <wolfssl/ssl.h>
#include <wolfssl/internal.h>
#include <wolfssl/error-ssl.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iterator>
#include <string>

static bool setupFault = false;
static int domainCalls = 0, connectCalls = 0, lastError = 0;
extern "C" int p3Domain(WOLFSSL* ssl, const char* host) {
  ++domainCalls;
  if (setupFault) {
    // Mirror the return and state of ssl.c's failed domain-name allocation.
    // No heap-size or allocation-pressure measurement is implied.
    ssl->error = MEMORY_ERROR;
    return WOLFSSL_FAILURE;
  }
  return wolfSSL_check_domain_name(ssl, host);
}
extern "C" int p3Connect(WOLFSSL* ssl) {
  ++connectCalls;
  const int result = wolfSSL_connect(ssl);
  if (result != WOLFSSL_SUCCESS) lastError = wolfSSL_get_error(ssl, result);
  return result;
}
int main(int argc, char** argv) {
  if (argc != 5) return 2;
  setupFault = std::strcmp(argv[3], "fault") == 0;
  std::ifstream file(argv[2]);
  const std::string ca{std::istreambuf_iterator<char>(file), {}};
  freeink::SecureClient client;
  client.setTimeout(300);
  client.setCACert(ca.c_str());
  if (std::strcmp(argv[4], "insecure") == 0) client.setInsecure();
  const bool connected = client.connect("good.test", static_cast<uint16_t>(std::atoi(argv[1]))) == 1;
  if (connected) {
    const char request[] = "GET /G10_PROTECTED/P3/1 HTTP/1.1\r\nHost: good.test\r\nConnection: close\r\n\r\n";
    client.write(reinterpret_cast<const uint8_t*>(request), sizeof(request)-1);
  }
  const uint32_t deadline = millis()+2000;
  char response[256] = {}; size_t received = 0;
  while (connected && millis()<deadline && received+1<sizeof(response)) {
    const int n = client.read(reinterpret_cast<uint8_t*>(response)+received, sizeof(response)-received-1);
    if (n > 0) received += n;
    else if (n < 0 || !client.connected()) break;
    delay(2);
  }
  printf("{\"connected\":%s,\"tcp_attempts\":%u,\"wolfssl_connect_calls\":%d,\"domain_calls\":%d,\"last_error\":%d,\"response_ok\":%s",
         connected?"true":"false", p3TcpAttempts, connectCalls, domainCalls, lastError,
         std::strstr(response,"G10_OK")?"true":"false");
#ifdef P3_PR14
  printf(",\"lastConnectWasInsecure\":%s,\"sampled_heap\":%zu", client.lastConnectWasInsecure()?"true":"false", client.handshakeMinFree());
#endif
  puts("}");
  client.stop();
}
