#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <optional>
#include <string>
#include <vector>

#include "ReaderRenderSpec.h"
#define LOG_DBG(...) ((void)0)
#define LOG_ERR(...) ((void)0)
struct HalFile {
  std::vector<uint8_t>* bytes = nullptr;
  size_t pos = 0;
  bool closed = false;
  explicit operator bool() const { return bytes && !closed; }
  size_t size() const { return bytes->size(); }
  bool seek(size_t n) {
    if (n > size()) return false;
    pos = n;
    return true;
  }
  int read(void* dst, size_t n) {
    n = std::min(n, size() - pos);
    std::memcpy(dst, bytes->data() + pos, n);
    pos += n;
    return n;
  }
  size_t write(const void* src, size_t n) {
    if (pos + n > size()) bytes->resize(pos + n);
    std::memcpy(bytes->data() + pos, src, n);
    pos += n;
    return n;
  }
  void close() { closed = true; }
};
std::vector<uint8_t> disk;
std::vector<uint8_t> progress;
struct {
  bool openFileForRead(const char*, const std::string& path, HalFile& f) {
    f = {path.ends_with("progress.bin") ? &progress : &disk, 0, false};
    return true;
  }
} Storage;
namespace serialization {
template <class T>
void readPod(HalFile& f, T& v) {
  assert(f.read(&v, sizeof(v)) == sizeof(v));
}
template <class T>
void writePod(HalFile& f, const T& v) {
  assert(f.write(&v, sizeof(v)) == sizeof(v));
}
}  // namespace serialization
PRODUCTION_CONSTANTS
struct Entry {
  uint32_t visibleTextOffset;
};
struct Build {
  std::vector<Entry> lut;
};
struct Section {
  HalFile file{&disk, 0, false};
  std::string filePath = "section";
  uint16_t pageCount = 0;
  int currentPage = 0;
  bool cleared = false, partial_ = false;
  uint32_t partialBytesConsumed_ = 0, partialTotalBytes_ = 0;
  uint16_t partialPageCount_ = 0;
  Build* build_ = nullptr;
  bool clearCache() {
    cleared = true;
    return true;
  }
  bool isBuilding() const { return false; }
  void writeSectionFileHeader(const ReaderRenderSpec&);
  bool loadSectionFile(const ReaderRenderSpec&);
  std::optional<uint16_t> getPageForVisibleTextOffset(uint32_t, bool = false) const;
};
struct Book {
  std::string getCachePath() const { return "/book"; }
} book;
struct Settings {
  int screenMargin = 5;
} SETTINGS;
struct UITheme {
  struct Metrics {
    int statusBarVerticalMargin = 2;
  };
  static UITheme& getInstance() {
    static UITheme theme;
    return theme;
  }
  int getProgressBarHeight() const { return 8; }
  Metrics getMetrics() const { return {}; }
};
struct EpubReaderActivity {
  Book* epub = &book;
  int nextPageNumber = 0;
  std::optional<int> pendingPageJump;
  std::optional<uint32_t> pendingOffsetJump;
  std::string pendingAnchor;
  void loadProgress();
  void resumeLoadedSection();
  Section* section;
  std::optional<uint32_t> cachedVisibleTextOffset;
  int cachedChapterTotalPageCount = 0;
  int currentSpineIndex = 0, cachedSpineIndex = 0;
  bool applyDeferredReposition();
  void clearDeferredReposition();
};
PRODUCTION_METHODS
void fixture(Section& section, const ReaderRenderSpec& spec, std::vector<uint32_t> starts) {
  disk.clear();
  section.file = {&disk, 0, false};
  section.pageCount = starts.size();
  section.writeSectionFileHeader(spec);
  assert(disk.size() == HEADER_SIZE);
  disk[0] = SECTION_FILE_VERSION;
  uint32_t lut = HEADER_SIZE;
  std::memcpy(disk.data() + HEADER_SIZE - 4, &lut, 4);
  section.file.seek(HEADER_SIZE);
  for (auto start : starts) serialization::writePod(section.file, start);
}
int main() {
  ReaderRenderSpec spec;
  spec.viewportWidth = 460;
  spec.viewportHeight = 740;
  Section section;
  EpubReaderActivity reader;
  reader.section = &section;
  // Persisted P8-format progress: spine0/page2/count5/offset1157, not an injected field.
  progress = {0, 0, 2, 0, 5, 0, 0x85, 4, 0, 0};
  reader.loadProgress();
  assert(reader.nextPageNumber == 2 && reader.cachedVisibleTextOffset == 1157);
  fixture(section, spec, {0, 575, 1157, 1784, 2336});
  disk[0] = 74;
  assert(!section.loadSectionFile(spec) && section.cleared);
  fixture(section, spec, {0, 575, 1157, 1784, 2336});
  assert(section.loadSectionFile(spec));
  reader.resumeLoadedSection();
  assert(section.currentPage == 2 && !reader.cachedVisibleTextOffset.has_value());
  assert(bottomMargin(false, 12) == 17 && bottomMargin(true, 8) == 15);
  auto smaller = spec;
  smaller.viewportHeight -= bottomMargin(false, 12);
  section.cleared = false;
  assert(!section.loadSectionFile(smaller) && section.cleared);
  // Rebuilt layout is a boundary fixture; the full font/layout build is not run here.
  fixture(section, smaller, {0, 300, 600, 900, 1200, 1600});
  assert(section.loadSectionFile(smaller));
  reader.loadProgress();
  reader.resumeLoadedSection();
  assert(section.currentPage == 3 && "normal resume lost text anchor");
  assert(!reader.cachedVisibleTextOffset.has_value());
  assert(section.getPageForVisibleTextOffset(1157) == 3);
  assert(section.getPageForVisibleTextOffset(1200) == 4);
  reader.loadProgress();
  section.currentPage = 2;
  assert(reader.applyDeferredReposition() && section.currentPage == 3);
  reader.loadProgress();
  reader.currentSpineIndex = 1;
  reader.resumeLoadedSection();
  assert(section.currentPage == 2);
}
