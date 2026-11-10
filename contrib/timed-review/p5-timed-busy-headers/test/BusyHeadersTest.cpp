// Real TIMED caller and SDK HTTP parser; TLS, clock, SD and display are host fakes.
#include <GfxRenderer.h>
#include <HalStorage.h>
#include <SecureHttpClient.h>
#include <TrustedTime.h>

#include <cassert>
#include <cstdio>
#include <cstring>
#include <string>

#include "util/PluginDrainBudget.h"
#include "util/PluginEvents.h"
#include "util/PluginLocations.h"
#include "util/TimedSleepPaint.h"

namespace freeink {
SecureClient::~SecureClient() = default;
void SecureClient::setCACert(const char*) {}
void SecureClient::setInsecure() {}
int SecureClient::connect(IPAddress ip, uint16_t port) { return _transport.connect(ip, port); }
int SecureClient::connect(const char* host, uint16_t port) { return _transport.connect(host, port); }
size_t SecureClient::write(uint8_t b) { return _transport.write(b); }
size_t SecureClient::write(const uint8_t* p, size_t n) { return _transport.write(p, n); }
int SecureClient::available() { return _transport.available(); }
int SecureClient::read() { return _transport.read(); }
int SecureClient::read(uint8_t* p, size_t n) { return _transport.read(p, n); }
int SecureClient::peek() { return _transport.peek(); }
void SecureClient::flush() {}
void SecureClient::stop() { _transport.stop(); }
uint8_t SecureClient::connected() { return _transport.connected(); }
bool SecureClient::tls13Available() { return false; }
bool SecureClient::peerVerificationAvailable() { return true; }  // Capability only; no TLS verification here.
bool hostResolves(const char*) { return true; }
}  // namespace freeink
namespace PluginLocations {
std::vector<Entry> scanPlugins() { return {{"fixture", "/plugins/fixture", false, true, false}}; }
std::string findPluginDir(const char*) { return {}; }
}  // namespace PluginLocations
static constexpr size_t trigger = 4300;  // Inside an overlong CSP, before its end.
static size_t triggerAt = 0;
static int renames = 0;
static uint32_t budgetClock() {
  if (FakeNet::bytesRead() >= trigger) {
    if (!triggerAt) triggerAt = FakeNet::bytesRead();
    return 15000;
  }
  return 0;
}
static std::string bmp() {
  std::string b(94, '\0');
  auto put = [&](int at, unsigned n) {
    for (int i = 0; i < 4; ++i) b[at + i] = static_cast<char>(n >> (8 * i));
  };
  b[0] = 'B';
  b[1] = 'M';
  put(2, 94);
  put(10, 62);
  put(14, 40);
  put(18, 8);
  put(22, 8);
  b[26] = b[28] = 1;
  b[58] = b[59] = b[60] = static_cast<char>(255);
  return b;
}
static std::string response() { return "HTTP/1.1 200 OK\r\nContent-Length: 94\r\n\r\n" + bmp(); }
static std::string busy() {
  return "HTTP/1.1 401 Unauthorized\r\nContent-Security-Policy: " + std::string(6000, 'x') +
         "\r\nContent-Length: 0\r\n\r\n";
}
static void setup() {
  Storage = StorageStub{};
  renames = 0;
  Storage.afterRename = [] { ++renames; };
  Storage.files["/sleep.bmp"] = bmp();
  Storage.files["/sleep.bmp"].back() ^= 0x55;
  Storage.files["/plugins/fixture/ca.pem"] =
      "-----BEGIN CERTIFICATE-----\nfixture-not-a-real-certificate-pad\n-----END CERTIFICATE-----";
  Storage.files["/plugins/fixture/token.json"] = R"({"token":"fixture-token"})";
  Storage.files["/plugins/fixture/events.jsonl"] = "private-reader-outbox";
  Storage.files["/.crosspoint/state.json"] = "private-reader-position";
  Storage.files["/plugins/fixture/device.json"] =
      R"({"auth":{"type":"password","request":{"url":"https://fixture.invalid/auth","tls":{"ca_file":"ca.pem"}}},"token":{"file":"token.json"},"events":{"sleep.timer":{"interval_seconds":60,"download":{"url":"https://fixture.invalid/frame","dest":"/sleep.bmp","format":"bmp","width":8,"height":8,"tls":{"ca_file":"ca.pem"}}}}})";
  trustedtime::now = trustedtime::systemNow = 1800000000;
  trustedtime::fresh = true;
  FakeNet::replies().clear();
  FakeNet::requests().clear();
  FakeNet::hosts().clear();
  FakeNet::readDelay() = 0;
  FakeNet::bytesRead() = 0;
  FakeNet::holdOpen() = false;
  fakeNow() = 0;
  triggerAt = 0;
  assert(FakeNet::openCount() == 0);
  pluginevents::refreshSubscriptions();
}
static void success() {
  const auto expected = bmp();
  FakeNet::replies().push_back(response());
  assert(pluginevents::prepareTimed(8, 8) == 60000000);
  pluginevents::DrainBudget budget(4, 15000, []() -> uint32_t { return 0; });
  auto result = pluginevents::timedSync(budget, {});
  assert(result.state == pluginevents::TimedState::Staged);
  GfxRenderer renderer;
  assert(timedsleeppaint::paint(renderer, result.asset, {}));
  assert(renderer.paints == 1 && Storage.files.at("/sleep.bmp") == expected);
  assert(!Storage.exists("/sleep.bmp.part") && FakeNet::openCount() == 0);
}
static void stopped(bool deadline) {
  setup();
  const auto old = Storage.files.at("/sleep.bmp");
  const auto privateFiles = Storage.files;
  FakeNet::replies().push_back(busy());
  FakeNet::replies().push_back(response());
  assert(pluginevents::prepareTimed(8, 8) == 60000000);
  pluginevents::DrainBudget budget(4, 15000, deadline ? &budgetClock : +[]() -> uint32_t { return 0; });
  auto abort = [] {
    if (FakeNet::bytesRead() < trigger) return false;
    if (!triggerAt) triggerAt = FakeNet::bytesRead();
    return true;
  };
  auto result = pluginevents::timedSync(budget, deadline ? std::function<bool()>{} : abort);
  GfxRenderer renderer;
  if (result.state == pluginevents::TimedState::Staged) timedsleeppaint::paint(renderer, result.asset, {});
  const auto after = FakeNet::bytesRead() - trigger;
  std::fprintf(stderr, "progress: trigger=%zu poll=%zu post-trigger=%zu total=%zu\n", trigger, triggerAt, after,
               FakeNet::bytesRead());
  assert(triggerAt == trigger && FakeNet::bytesRead() < busy().size() && after == 0);
  assert(result.state == pluginevents::TimedState::Failure && renderer.paints == 0 && renderer.draws == 0);
  assert(Storage.writeOpens == 1 && Storage.lastWritePath == "/sleep.bmp.part" && renames == 0);
  assert(Storage.files.at("/sleep.bmp") == old && !Storage.exists("/sleep.bmp.part"));
  assert(Storage.files == privateFiles);
  assert(FakeNet::requests().size() == 1 && FakeNet::requests()[0].find("GET /frame ") == 0);
  assert(FakeNet::openCount() == 0);
  std::printf("%s: trigger=%zu post-trigger=%zu unread=%zu requests=%zu closed=yes part-absent=yes old-unchanged=yes\n",
              deadline ? "budget" : "abort", triggerAt, after, busy().size() - FakeNet::bytesRead(),
              FakeNet::requests().size());
  FakeNet::replies().clear();
  success();  // A fresh prepare works after failure.
}
int main(int argc, char** argv) {
  if (argc == 2 && std::strcmp(argv[1], "abort") == 0) {
    stopped(false);
    return 0;
  }
  if (argc == 2 && std::strcmp(argv[1], "budget") == 0) {
    stopped(true);
    return 0;
  }
  setup();
  success();
  std::puts("valid: staged, committed and painted");
  stopped(false);
  stopped(true);
  std::puts("fresh prepare after each failure: PASS");
}
