#include <gtest/gtest.h>
#include <strings.h>

#include <algorithm>
#include <string>
#include <utility>
#include <vector>

// The extracted production type depends on PluginLocations.
// clang-format off
#include "util/PluginLocations.h"
#include "PluginRef.inc"
// clang-format on

namespace {
std::vector<PluginLocations::Entry> entries;
std::vector<std::pair<std::string, std::string>> titles;
struct StorageStub {
  bool exists(const char*) const { return false; }
} Storage;
void readPluginMetadata(const std::string& path, PluginRef& ref, bool = false) {
  for (const auto& [name, title] : titles)
    if (path == "/plugins/" + name + "/device.json") ref.title = title;
}
void setEntries(std::initializer_list<std::pair<std::string, std::string>> values) {
  entries.clear();
  titles.assign(values);
  for (const auto& [name, title] : titles) {
    PluginLocations::Entry e;
    e.name = name;
    e.dir = "/plugins/" + name;
    e.hasDevice = true;
    entries.push_back(std::move(e));
  }
}
std::vector<std::string> names(const std::vector<PluginRef>& plugins) {
  std::vector<std::string> result;
  for (const auto& p : plugins) result.push_back(p.name);
  return result;
}
}  // namespace
namespace PluginLocations {
std::vector<Entry> scanPlugins() { return entries; }
}  // namespace PluginLocations
#include "DiscoverPlugins.inc"

class PickerRestore {
 public:
  std::vector<PluginRef> installedPlugins;
  std::string pickerReturnName;
  bool showOpds = false;
  bool showPluginHubInstallRow = false;
  int selected = 0;
  void moveSelectionTo(int row) { selected = row; }
  void restore() {
#include "RestoreSelection.inc"
  }
};

TEST(PickerOrder, HubStaysFirstThenTitlesIgnoreCase) {
  setEntries({{"z", "Zulu"}, {"b", "beta"}, {"pluginhub", "Plugin Hub"}, {"a", "Alpha"}});
  EXPECT_EQ(names(discoverPlugins()), (std::vector<std::string>{"pluginhub", "a", "b", "z"}));
}
TEST(PickerOrder, SdEnumerationDoesNotChoosePresentationOrder) {
  setEntries({{"z", "Zulu"}, {"pluginhub", "Zzz translated hub"}, {"a", "Alpha"}});
  const auto expected = names(discoverPlugins());
  std::reverse(entries.begin(), entries.end());
  EXPECT_EQ(names(discoverPlugins()), expected);
}
TEST(PickerOrder, DuplicateTitlesUseFolderIdentity) {
  setEntries({{"z", "Same"}, {"a", "same"}, {"b", "SAME"}});
  EXPECT_EQ(names(discoverPlugins()), (std::vector<std::string>{"a", "b", "z"}));
}
TEST(PickerOrder, MissingMetadataFallsBackToFolderAndPathsStayAttached) {
  setEntries({{"z", "Zulu"}, {"a", "Alpha"}});
  titles.clear();
  const auto result = discoverPlugins();
  ASSERT_EQ(result.size(), 2u);
  EXPECT_EQ(result[0].title, "a");
  EXPECT_EQ(result[0].manifestPath, "/plugins/a/device.json");
}
TEST(PickerOrder, EmptyAndMissingHubRemainValid) {
  setEntries({});
  EXPECT_TRUE(discoverPlugins().empty());
  setEntries({{"b", "Beta"}, {"a", "Alpha"}});
  EXPECT_EQ(names(discoverPlugins()), (std::vector<std::string>{"a", "b"}));
}
TEST(PickerOrder, LongLocalizedTitlesRemainIntact) {
  const std::string title = "Żółta kartka — wiadomość dla rodziny " + std::string(400, 'x');
  setEntries({{"long", title}, {"pluginhub", "Centrum wtyczek"}});
  const auto result = discoverPlugins();
  ASSERT_EQ(result.size(), 2u);
  EXPECT_EQ(result[0].name, "pluginhub");
  EXPECT_EQ(result[1].title, title);
}
TEST(PickerRestore, IdentitySurvivesInsertionAheadOfPreviousRow) {
  setEntries({{"z", "Zulu"}, {"a", "Alpha"}, {"pluginhub", "Hub"}});
  PickerRestore p;
  p.installedPlugins = discoverPlugins();
  p.pickerReturnName = "z";
  p.showOpds = true;
  p.restore();
  EXPECT_EQ(p.selected, 3);
  EXPECT_EQ(p.installedPlugins[p.selected - 1].name, "z");
}
TEST(PickerRestore, EveryPrefixMapsToSamePlugin) {
  setEntries({{"b", "Beta"}, {"a", "Alpha"}});
  for (const bool opds : {false, true})
    for (const bool install : {false, true}) {
      PickerRestore p;
      p.installedPlugins = discoverPlugins();
      p.pickerReturnName = "b";
      p.showOpds = opds;
      p.showPluginHubInstallRow = install;
      p.restore();
      EXPECT_EQ(p.selected, 1 + static_cast<int>(opds) + static_cast<int>(install));
    }
}
TEST(PickerRestore, FirstRowAndRemovedPluginDoNotSelectWrongIdentity) {
  setEntries({{"a", "Alpha"}});
  PickerRestore p;
  p.installedPlugins = discoverPlugins();
  p.pickerReturnName = "a";
  p.restore();
  EXPECT_EQ(p.selected, 0);
  p.pickerReturnName = "removed";
  p.restore();
  EXPECT_EQ(p.selected, 0);
}
