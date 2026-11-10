#include "WifiCredentialStore.h"
#ifndef STOCK_ONLY
#include "util/TimedSource.h"
#endif
#include <cassert>
#include <functional>
#include <iostream>
#include <string>

static std::string disk;
static int loads = 0;
bool PersistableStoreBase::writeDocToFile(const char*, const JsonDocument& doc) {
  disk.clear();
  serializeJson(doc, disk);
  return true;
}
bool PersistableStoreBase::readDocFromFile(const char*, JsonDocument& doc) {
  ++loads;
  return !deserializeJson(doc, disk);
}
std::string PersistableStoreBase::extractPassword(JsonVariantConst d, bool&, size_t, bool& valid) {
  valid = true;
  return d["password_obf"] | "";
}
static unsigned long now = 0;
unsigned long millis() { return now; }
void delay(unsigned long n) { now += n; }
struct ScreenshotInfo {
  enum class ReaderType { None, Book };
  ReaderType readerType = ReaderType::None;
  int progressPercent = 0, endProgressPercent = 0;
};
struct {
  void prepareForSleep() {}
  ScreenshotInfo getScreenshotInfo() { return {}; }
} activityManager;
struct {
  std::string openEpubPath;
} APP_STATE;
struct {
  int getBatteryPercentage() { return 80; }
} powerManager;
namespace pluginevents {
struct Var {
  const char* name;
  const char* value;
};
enum class Event { SleepEnter };
bool handler = true, prepared = false;
int drains = 0;
void emit(Event, Var*, size_t) {}
bool wantsConnectAny() { return handler; }
void drain(int*, int, std::initializer_list<int>) { ++drains; }
#ifdef STOCK_ONLY
void drain(int*) { ++drains; }
#endif
void discardTimed() { prepared = false; }
void refreshSubscriptions() {}
uint64_t prepareTimed(int, int) {
  prepared = handler;
  return handler ? 60000000 : 0;
}
enum class TimedState { NoHandler, Staged, Failure };
struct Result {
  TimedState state;
  std::string asset;
};
}  // namespace pluginevents
static int renderer = 0;
struct {
  void drawPopup(int&, const char*) {}
} GUI;
const char* tr(int) { return ""; }
constexpr int STR_LOADING_POPUP = 0;
constexpr int WL_CONNECTED = 1, WIFI_STA = 1, WIFI_OFF = 0;
struct {
  int begins = 0;
  bool online = false, canJoin = true;
  std::string ssid;
  int status() { return online ? WL_CONNECTED : 0; }
  void mode(int) {}
  void begin(const char* s, const char*) {
    ++begins;
    ssid = s;
    online = canJoin;
  }
  void disconnect(bool) { online = false; }
} WiFi;
namespace trustedtime {
void startSync() {}
void init() {}
bool syncFresh(uint32_t, const std::function<bool()>&) { return true; }
bool hasFreshSync() { return true; }
}  // namespace trustedtime
#ifndef STOCK_ONLY
static bool timerStorageReady = false, timerDisplayReady = false;
struct {
  bool ready() { return true; }
  bool begin() { return true; }
  bool remove(const char*) { return true; }
} Storage;
bool timerModelSupported() { return true; }
static timedsource::Source source = timedsource::Source::Plugin, preparedTimerSource = timedsource::Source::Off;
timedsource::Source selectedTimerSource() { return source; }
struct CrossPointSettings {
  static constexpr int CUSTOM = 1;
  int sleepScreen = CUSTOM;
  bool pluginsEnabled = true;
  uint64_t getTimedSleepScreenRefreshUs() { return 120000000; }
} SETTINGS;
namespace BoardConfig {
struct Profile {
  int displayHeight = 480, displayWidth = 800;
};
Profile ACTIVE;
}  // namespace BoardConfig
struct {
  void begin() {}
} halClock;
namespace HalGPIO {
enum class PowerWakeRequest { None };
}
struct {
  HalGPIO::PowerWakeRequest powerWakeRequest() { return HalGPIO::PowerWakeRequest::None; }
} gpio;
struct {
  void setInverted(bool) {}
} display;
static int mappedInputManager = 0;
void setupBitmapDisplay(bool) { timerDisplayReady = true; }
struct SleepActivity {
  SleepActivity(int&, int&) {}
  void renderTimedSleepScreen() {}
};
#include "util/PluginDrainBudget.h"
namespace pluginevents {
Result timedSync(DrainBudget&, const std::function<bool()>&) { return {TimedState::Failure, {}}; }
}  // namespace pluginevents
namespace timedsleeppaint {
bool paint(int&, const std::string&, const std::function<bool()>&) { return true; }
}  // namespace timedsleeppaint
#endif
#include "Callers.inc"
static void reset(const char* last, bool networks = true) {
  JsonDocument d;
  d["lastConnectedSsid"] = last;
  if (networks) {
    auto a = d["credentials"].to<JsonArray>();
    auto x = a.add<JsonObject>();
    x["ssid"] = "first";
    x["password_obf"] = "";
    auto y = a.add<JsonObject>();
    y["ssid"] = "second";
    y["password_obf"] = "";
  }
  disk.clear();
  serializeJson(d, disk);
  WiFi.online = false;
  WiFi.canJoin = true;
  WiFi.begins = 0;
  WiFi.ssid.clear();
  pluginevents::handler = true;
  pluginevents::drains = 0;
  loads = 0;
#ifndef STOCK_ONLY
  source = timedsource::Source::Plugin;
  SETTINGS.pluginsEnabled = true;
#endif
}
static void check(const char* last, const char* expected) {
  reset(last);
  deliverSleepPluginEvents(true);
  assert(WiFi.begins == 1 && WiFi.ssid == expected && pluginevents::drains == 1);
#ifndef STOCK_ONLY
  reset(last);
  assert(prepareTimerPanel() == 60000000);
  assert(!syncTimerPanel());
  assert(WiFi.begins == 1 && WiFi.ssid == expected);
#endif
}
int main() {
  check("", "first");
  check("stale", "first");
  check("second", "second");
  reset("", false);
  deliverSleepPluginEvents(true);
  assert(WiFi.begins == 0);
#ifndef STOCK_ONLY
  assert(prepareTimerPanel() == 0);
  reset("");
  source = timedsource::Source::Off;
  assert(prepareTimerPanel() == 0 && WiFi.begins == 0 && loads == 0);
  reset("");
  SETTINGS.pluginsEnabled = false;
  assert(prepareTimerPanel() == 0 && WiFi.begins == 0 && loads == 0);
#endif
  reset("");
  pluginevents::handler = false;
  deliverSleepPluginEvents(true);
  assert(WiFi.begins == 0 && loads == 0);
#ifndef STOCK_ONLY
  assert(prepareTimerPanel() == 0 && loads == 0);
#endif
  reset("");
  deliverSleepPluginEvents(false);
  assert(WiFi.begins == 0);
  reset("");
  WiFi.canJoin = false;
  now = 0;
  deliverSleepPluginEvents(true);
  assert(WiFi.begins == 1 && now == 10000 && pluginevents::drains == 0);
#ifndef STOCK_ONLY
  reset("");
  WiFi.canJoin = false;
  now = 0;
  assert(prepareTimerPanel() == 60000000);
  assert(!syncTimerPanel());
  assert(WiFi.begins == 1 && now == 10000);
#endif
  // Real deletion clears the selected SSID but preserves the other saved network.
  reset("second");
  assert(WIFI_STORE.loadFromFile());
  assert(WIFI_STORE.removeCredential("second"));
  assert(WIFI_STORE.getLastConnectedSsid().empty());
  WiFi.online = false;
  WiFi.begins = 0;
  deliverSleepPluginEvents(true);
  assert(WiFi.begins == 1 && WiFi.ssid == "first");
  // An empty stored SSID must never be submitted to WiFi.begin.
  reset("");
  JsonDocument bad;
  bad["lastConnectedSsid"] = "";
  auto a = bad["credentials"].to<JsonArray>();
  auto x = a.add<JsonObject>();
  x["ssid"] = "";
  x["password_obf"] = "";
  disk.clear();
  serializeJson(bad, disk);
  deliverSleepPluginEvents(true);
  assert(WiFi.begins == 0);
#ifndef STOCK_ONLY
  assert(prepareTimerPanel() == 0);
#endif
  std::cout << "real store + sleep/timer callers: empty/stale/valid/none/off/no-handler PASS\n";
}
