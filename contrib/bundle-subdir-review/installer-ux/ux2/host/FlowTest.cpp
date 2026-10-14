#include <gtest/gtest.h>

#include <algorithm>
#include <cstdint>
#include <functional>
#include <memory>
#include <optional>
#include <string>
#include <utility>
#include <vector>
#define LOG_ERR(...) ((void)0)
#define LOG_INF(...) ((void)0)
struct StrId {
  enum Value { STR_MEMORY_ERROR, STR_UPDATE_AVAILABLE, STR_UPDATE, STR_INSTALL, STR_PLUGINS };
};
using Label = StrId::Value;
inline constexpr Label STR_UPDATE_AVAILABLE = Label::STR_UPDATE_AVAILABLE;
inline constexpr Label STR_PLUGINS = Label::STR_PLUGINS;
const char* tr(Label v) {
  return v == StrId::STR_UPDATE_AVAILABLE ? "Update" : v == StrId::STR_PLUGINS ? "Plugins" : "Install";
}
struct Translator {
  const char* get(Label l) const { return tr(l); }
} I18N;
#define StrId Label
struct ActivityResult {
  bool isCancelled = false;
};
struct Input {
  enum class Button { Back, Confirm };
  bool back = false, confirm = false, held = false, tap = false;
  int x = 0, y = 0;
  bool wasReleased(Button b) const { return b == Button::Back ? back : confirm; }
  bool isPressed(Button) const { return held; }
  bool wasScreenTapped(int& tx, int& ty) const {
    tx = x;
    ty = y;
    return tap;
  }
};
using MappedInputManager = Input;
struct Renderer {
  int getScreenWidth() const { return 480; }
};
namespace haptic_feedback {
void touchAction() {}
}  // namespace haptic_feedback
struct Nav {
  template <class F>
  void onNext(F) {}
  template <class F>
  void onPrevious(F) {}
};
struct Gpio {
  bool touch = true;
  bool hasTouch() const { return touch; }
} gpio;
struct UITheme {
  struct Metrics {
    int verticalSpacing = 10;
  } metrics;
  static UITheme& getInstance() {
    static UITheme t;
    return t;
  }
  const Metrics& getMetrics() const { return metrics; }
};
namespace freeink::ui {
struct ButtonProps {
  const char* label = nullptr;
  int action = 0;
};
}  // namespace freeink::ui
struct UiStub {
  UiStub() = default;
  explicit UiStub(Renderer&) {}
  struct Route {
    struct Event {
      int action = 0;
    } event;
    bool routed = false;
  };
  struct UiScreen {
    struct Rect {
      int16_t x, y, width, height;
    };
    struct Theme {
      int16_t rowHeight = 45;
    };
    void button(freeink::ui::ButtonProps, Rect) {}
    Theme theme() const { return {}; }
  };
  void resetUi() { ready = false; }
  bool ready = false, invalid = false;
  Route next;
  struct App {
    UiStub* self;
    bool invalidated() const { return self->invalid; }
    void setScreen(void (*)(UiScreen&, void*), void*) {}
  } app{this};
  Route routeTouch(Input&) { return ready ? next : Route{}; }
  bool routingReady() const { return ready; }
};
using UiAppHost = UiStub;
struct Activity {
  void onEnter() {}
};
constexpr size_t MAX_STYLED_HTML_BYTES = 16 * 1024;
std::string htmlToPlainText(const std::string& s) { return s; }
constexpr int CONFIRM_ACTION = 1;
class DictionaryDefinitionActivity : public Activity {
 public:
  Input mappedInput;
  Renderer renderer;
  Nav buttonNavigator;
  std::unique_ptr<UiStub> confirmationUi;
  bool confirmHeldOnEntry = false;
  ActivityResult result;
  int currentPage = 0, totalPages = 3, updates = 0;
  bool finished = false;
  std::string headword, definition;
  std::optional<Label> confirmLabel;
  DictionaryDefinitionActivity() = default;
  DictionaryDefinitionActivity(Renderer&, Input&, std::string title, std::string text, bool, std::optional<Label> label)
      : headword(std::move(title)), definition(std::move(text)), confirmLabel(label) {}
  void finish() { finished = true; }
  void requestUpdate() { ++updates; }
  bool htmlDefinition = false;
  int wraps = 0;
  std::vector<int> pages;
  struct BodyArea {
    int x, y, width, height;
  };
  BodyArea bodyArea() const { return {20, 100, 440, 600}; }
  bool layoutHtmlPages() { return false; }
  void wrapText() { ++wraps; }
  void onEnter();
  void loop();
};
#include "ViewerLoop.inc"
static bool allocationFails = false;
template <class T, class... Args>
std::unique_ptr<T> makeUniqueNoThrow(Args&&... a) {
  if (allocationFails) return {};
  return std::make_unique<T>(std::forward<Args>(a)...);
}
#include "ViewerEnter.inc"
class PluginCatalogActivity {
 public:
  enum class State { BROWSING, OTHER };
  State state = State::BROWSING;
  struct Item {
    std::string title, author, version, id, status, url;
    std::vector<std::string> files;
    bool isDir = false;
  };
  struct Manifest {
    bool xml = false;
    bool isXmlList() const { return xml; }
  } manifest;
  bool pluginBundleCatalog = true;
  std::vector<Item> items;
  std::vector<std::string> browseHistory;
  std::string browseCurrentUrl;
  int page = 1;
  Input mappedInput;
  Renderer renderer;
  int downloads = 0, fetches = 0;
  bool failed = false;
  std::unique_ptr<DictionaryDefinitionActivity> child;
  std::function<void(const ActivityResult&)> callback;
  void beginLoading() {}
  void fetchPage(int) { ++fetches; }
  void fail(Label) { failed = true; }
  void downloadItem(int) { ++downloads; }
  void startActivityForResult(std::unique_ptr<DictionaryDefinitionActivity> v,
                              std::function<void(const ActivityResult&)> cb) {
    child = std::move(v);
    callback = std::move(cb);
  }
  void activateItem(int itemIndex);
};
#include "ActivateItem.inc"
static PluginCatalogActivity catalog() {
  allocationFails = false;
  PluginCatalogActivity p;
  p.items.push_back(
      {"Przykład", "Zażółć gęślą jaźń — rodzinny opis", "1.2.3", "example", "Update", "", {"device.json"}, false});
  return p;
}
static DictionaryDefinitionActivity viewer() {
  DictionaryDefinitionActivity v;
  v.confirmationUi = std::make_unique<UiStub>();
  v.result.isCancelled = true;
  return v;
}
TEST(DetailsFlow, OpenShowsOwnedTextAndDoesNotDownload) {
  auto p = catalog();
  p.activateItem(0);
  ASSERT_TRUE(p.child);
  EXPECT_EQ(p.downloads, 0);
  EXPECT_EQ(p.child->headword, "Plugins");
  EXPECT_EQ(p.child->definition, "Przykład\nv1.2.3\n\nZażółć gęślą jaźń — rodzinny opis");
  EXPECT_EQ(p.child->confirmLabel, Label::STR_UPDATE);
  p.items[0].author = "changed";
  EXPECT_NE(p.child->definition, "changed");
}
TEST(DetailsFlow, CancelAndExplicitAcceptAreSeparate) {
  auto p = catalog();
  p.activateItem(0);
  ASSERT_TRUE(p.callback);
  p.callback({true});
  EXPECT_EQ(p.downloads, 0);
  p.callback({false});
  EXPECT_EQ(p.downloads, 1);
}
TEST(DetailsFlow, ChangedParentOrIdentityDoesNotDownload) {
  auto p = catalog();
  p.activateItem(0);
  p.items[0].id = "different";
  p.callback({false});
  EXPECT_EQ(p.downloads, 0);
  p.items.clear();
  p.callback({false});
  EXPECT_EQ(p.downloads, 0);
  p = catalog();
  p.activateItem(0);
  p.state = PluginCatalogActivity::State::OTHER;
  p.callback({false});
  EXPECT_EQ(p.downloads, 0);
}
TEST(DetailsFlow, EmptyDescriptionAndVersionRemainUsable) {
  auto p = catalog();
  p.items[0].author.clear();
  p.items[0].version.clear();
  p.items[0].status.clear();
  p.activateItem(0);
  ASSERT_TRUE(p.child);
  EXPECT_EQ(p.child->definition, "Przykład\n\n");
  EXPECT_EQ(p.child->confirmLabel, Label::STR_INSTALL);
}
TEST(DetailsFlow, OversizeAndObjectAllocationFailureDoNotDownload) {
  auto p = catalog();
  p.items[0].author = std::string(4096, 'x');
  p.activateItem(0);
  EXPECT_TRUE(p.failed);
  EXPECT_FALSE(p.child);
  EXPECT_EQ(p.downloads, 0);
  p = catalog();
  allocationFails = true;
  p.activateItem(0);
  EXPECT_TRUE(p.failed);
  EXPECT_EQ(p.downloads, 0);
  allocationFails = false;
}
TEST(DetailsFlow, OrdinaryBooksAndOtherBundlesKeepFetch) {
  auto p = catalog();
  p.pluginBundleCatalog = false;
  p.activateItem(0);
  EXPECT_EQ(p.downloads, 1);
  EXPECT_FALSE(p.child);
  p = catalog();
  p.items[0].files.clear();
  p.activateItem(0);
  EXPECT_EQ(p.downloads, 1);
}
TEST(DetailsFlow, XmlFoldersStillNavigate) {
  auto p = catalog();
  p.manifest.xml = true;
  p.items[0].isDir = true;
  p.items[0].url = "folder";
  p.activateItem(0);
  EXPECT_EQ(p.fetches, 1);
  EXPECT_EQ(p.downloads, 0);
  EXPECT_FALSE(p.child);
}
TEST(DetailsFlow, InvalidIndexIsIgnored) {
  auto p = catalog();
  p.activateItem(-1);
  p.activateItem(2);
  EXPECT_FALSE(p.child);
  EXPECT_EQ(p.downloads, 0);
}
TEST(ViewerConfirmation, BackCancelsBeforeAccept) {
  auto v = viewer();
  v.mappedInput.back = true;
  v.mappedInput.confirm = true;
  v.confirmationUi->ready = true;
  v.loop();
  EXPECT_TRUE(v.finished);
  EXPECT_TRUE(v.result.isCancelled);
}
TEST(ViewerConfirmation, CannotAcceptBeforeFirstRender) {
  auto v = viewer();
  v.mappedInput.confirm = true;
  v.loop();
  EXPECT_FALSE(v.finished);
  EXPECT_TRUE(v.result.isCancelled);
}
TEST(ViewerConfirmation, EntryHoldConsumesItsReleaseThenAcceptsNextGesture) {
  auto v = viewer();
  v.confirmationUi->ready = true;
  v.confirmHeldOnEntry = true;
  v.mappedInput.held = true;
  v.loop();
  EXPECT_FALSE(v.finished);
  v.mappedInput.held = false;
  v.mappedInput.confirm = true;
  v.loop();
  EXPECT_FALSE(v.finished);
  EXPECT_FALSE(v.confirmHeldOnEntry);
  v.loop();
  EXPECT_TRUE(v.finished);
  EXPECT_FALSE(v.result.isCancelled);
}
TEST(ViewerConfirmation, TouchAcceptRemainsIndependentOfHeldButton) {
  auto v = viewer();
  v.confirmationUi->ready = true;
  v.confirmHeldOnEntry = true;
  v.mappedInput.held = true;
  v.confirmationUi->next = {{CONFIRM_ACTION}, true};
  v.loop();
  EXPECT_TRUE(v.finished);
  EXPECT_FALSE(v.result.isCancelled);
}
TEST(ViewerConfirmation, BodyTapStillTurnsPage) {
  auto v = viewer();
  v.confirmationUi->ready = true;
  v.mappedInput.tap = true;
  v.mappedInput.x = 400;
  v.loop();
  EXPECT_EQ(v.currentPage, 1);
  EXPECT_FALSE(v.finished);
}
TEST(ViewerConfirmation, ButtonFeedbackDoesNotAlsoTurnPage) {
  auto v = viewer();
  v.confirmationUi->ready = true;
  v.confirmationUi->invalid = true;
  v.confirmationUi->next = {{0}, true};
  v.mappedInput.tap = true;
  v.mappedInput.x = 400;
  v.loop();
  EXPECT_EQ(v.currentPage, 0);
  EXPECT_EQ(v.updates, 1);
}
TEST(ViewerConfirmation, DefaultDictionaryAndReadmeIgnoreConfirm) {
  DictionaryDefinitionActivity v;
  v.mappedInput.confirm = true;
  v.loop();
  EXPECT_FALSE(v.finished);
  v.mappedInput.back = true;
  v.loop();
  EXPECT_TRUE(v.finished);
}

TEST(ViewerEntry, OptInStartsCancelledAndWaitsForRender) {
  DictionaryDefinitionActivity v;
  v.confirmLabel = Label::STR_INSTALL;
  v.definition = "a";
  v.mappedInput.held = true;
  allocationFails = false;
  v.onEnter();
  EXPECT_TRUE(v.confirmationUi);
  EXPECT_TRUE(v.result.isCancelled);
  EXPECT_TRUE(v.confirmHeldOnEntry);
  EXPECT_EQ(v.wraps, 1);
  EXPECT_FALSE(v.confirmationUi->routingReady());
}
TEST(ViewerEntry, ReadOnlyDoesNotAllocateControls) {
  DictionaryDefinitionActivity v;
  allocationFails = true;
  v.definition = "a";
  v.onEnter();
  EXPECT_FALSE(v.confirmationUi);
  EXPECT_FALSE(v.finished);
  EXPECT_EQ(v.wraps, 1);
  allocationFails = false;
}
TEST(ViewerEntry, ControlsAllocationFailureCancels) {
  DictionaryDefinitionActivity v;
  v.confirmLabel = Label::STR_INSTALL;
  allocationFails = true;
  v.onEnter();
  EXPECT_TRUE(v.finished);
  EXPECT_TRUE(v.result.isCancelled);
  EXPECT_EQ(v.wraps, 0);
  allocationFails = false;
}

TEST(DetailsFlow, LineBreakLimitCountsAllFieldsAndEmbeddedNuls) {
  for (char separator : {'\n', '\0'}) {
    auto p = catalog();
    p.items[0].title = std::string(32, separator) + "Title";
    p.items[0].version = std::string(1, separator) + "1";
    p.items[0].author = std::string(31, separator) + std::string(1990, 'x');
    p.activateItem(0);
    ASSERT_TRUE(p.child);
    EXPECT_FALSE(p.failed);
    EXPECT_EQ(p.downloads, 0);
    p.child->onEnter();
    EXPECT_EQ(std::count(p.child->definition.begin(), p.child->definition.end(), '\n'), 67);
    EXPECT_EQ(std::count(p.child->definition.begin(), p.child->definition.end(), '\0'), 0);
    p = catalog();
    p.items[0].author = std::string(65, separator);
    p.activateItem(0);
    EXPECT_TRUE(p.failed);
    EXPECT_FALSE(p.child);
    EXPECT_EQ(p.downloads, 0);
  }
}
TEST(DetailsFlow, NearByteLimitAndSixtyFourBreaksRemainReadable) {
  auto p = catalog();
  p.items[0].title = std::string(2040, 'T');
  p.items[0].version = "v";
  p.items[0].author = std::string(64, '\n') + std::string(1983, 'x');
  p.activateItem(0);
  ASSERT_TRUE(p.child);
  EXPECT_EQ(p.child->definition.size(), 4092);
  EXPECT_EQ(p.downloads, 0);
  EXPECT_FALSE(p.failed);
}
