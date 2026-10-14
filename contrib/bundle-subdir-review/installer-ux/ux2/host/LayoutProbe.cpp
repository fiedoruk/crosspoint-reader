#include <EpdFont.h>
#include <FreeInkApp.h>
#include <FreeInkUI.h>
#include <FreeInkUIDisplayTarget.h>
#include <Utf8.h>
#include <builtinFonts/notoserif_18_regular.h>
#include <builtinFonts/ubuntu_12_regular.h>

#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
namespace fui = freeink::ui;
struct ThemeMetrics {
  int contentSidePadding = 20, sideButtonHintsWidth = 30, buttonHintsHeight = 40, topPadding = 5, headerHeight = 84,
      verticalSpacing = 10;
};
struct UITheme {
  ThemeMetrics metrics;
  static UITheme& getInstance() {
    static UITheme t;
    return t;
  }
  const ThemeMetrics& getMetrics() const { return metrics; }
};
struct Gpio {
  bool touch = false;
  bool hasTouch() const { return touch; }
} gpio;
struct Settings {
  int getReaderFontId() const { return 0; }
} SETTINGS;
struct EpdFontFamily {
  enum Style { REGULAR };
};
struct GfxRenderer {
  enum class Orientation { Portrait, PortraitInverted, LandscapeClockwise, LandscapeCounterClockwise };
  int width = 480, height = 800;
  Orientation orientation = Orientation::Portrait;
  mutable std::vector<unsigned char> pixels;
  EpdFont font{&ubuntu_12_regular};
  int getScreenWidth() const { return width; }
  int getScreenHeight() const { return height; }
  Orientation getOrientation() const { return orientation; }
  void getOrientedViewableTRBL(int* t, int* r, int* b, int* l) const { *t = *r = *b = *l = 0; }
  void ensureSdCardFontReady(int, const char*, int) const {}
  int getLineHeight(int, float spacing) const { return static_cast<int>(font.data->advanceY * spacing); }
  int getSpaceWidth(int, EpdFontFamily::Style) const { return fp4::toPixel(font.getGlyph(' ')->advanceX); }
  int advance(const char* text, bool draw = false, int x = 0, int y = 0) const {
    int pen = 0;
    int32_t previousAdvance = 0;
    uint32_t previous = 0;
    while (uint32_t cp = utf8NextCodepoint(reinterpret_cast<const unsigned char**>(&text))) {
      cp = font.applyLigatures(cp, text);
      const auto* g = font.getGlyph(cp);
      if (!g) continue;
      pen += fp4::toPixel(previousAdvance + font.getKerning(previous, cp));
      if (draw)
        for (int gy = 0; gy < g->height; ++gy)
          for (int gx = 0; gx < g->width; ++gx) {
            const int bit = gy * g->width + gx;
            const bool ink = (font.data->bitmap[g->dataOffset + (bit >> 3)] >> (7 - (bit & 7))) & 1;
            const int px = x + pen + g->left + gx, py = y + font.data->ascender - g->top + gy;
            if (ink && px >= 0 && py >= 0 && px < width && py < height) pixels[py * width + px] = 0;
          }
      previousAdvance = g->advanceX;
      previous = cp;
    }
    return pen + fp4::toPixel(previousAdvance);
  }
  int getTextAdvanceX(int, const char* t, EpdFontFamily::Style) const { return advance(t); }
  void drawText(int, int x, int y, const char* t) const { advance(t, true, x, y); }
};
struct UiAppHost {
  struct App {
    struct Theme {
      int rowHeight = 45;
    };
    Theme theme() const { return {}; }
  } app;
};
constexpr size_t MAX_LINE_BYTES = 191;
constexpr float PLAIN_TEXT_LINE_SPACING = 1.5f;
class DictionaryDefinitionActivity {
 public:
  struct Line {
    uint32_t start;
    uint16_t len;
  };
  struct BodyArea {
    int x, y, width, height;
  };
  struct PageStub {
    void render(const GfxRenderer&, int, int, int) {}
  };
  GfxRenderer renderer;
  std::unique_ptr<UiAppHost> confirmationUi;
  std::string definition;
  std::vector<Line> lines;
  std::vector<std::unique_ptr<PageStub>> pages;
  int currentPage = 0, totalPages = 1, linesPerPage = 1;
  BodyArea bodyArea() const;
  int measureSpan(int, const char*, size_t) const;
  void wrapText();
  void drawBody(int, int, int) const;
};
#include "LayoutMethods.inc"

int main(int argc, char** argv) {
  assert(argc == 2);
  const std::string out = argv[1];
  int cases = 0;
  const char* shortPl =
      "Przykładowa wtyczka\nv1.2.3\n\nWiadomości od rodziny, zakupy i przypomnienia na ekranie czytnika. Pełny opis "
      "możesz przeczytać przed instalacją.";
  const char* shortEn =
      "Example Plugin\nv1.2.3\n\nMessages, shopping lists and reminders from people you choose. Read the complete "
      "description before installing.";
  for (bool touch : {false, true})
    for (bool landscape : {false, true})
      for (bool inverted : {false, true})
        for (bool longText : {false, true}) {
          DictionaryDefinitionActivity a;
          a.confirmationUi = std::make_unique<UiAppHost>();
          gpio.touch = touch;
          UITheme::getInstance().metrics.buttonHintsHeight = touch ? 0 : 40;
          a.renderer.width = landscape ? 800 : 480;
          a.renderer.height = landscape ? 480 : 800;
          a.renderer.orientation =
              landscape ? (inverted ? GfxRenderer::Orientation::LandscapeCounterClockwise
                                    : GfxRenderer::Orientation::LandscapeClockwise)
                        : (inverted ? GfxRenderer::Orientation::PortraitInverted : GfxRenderer::Orientation::Portrait);
          a.definition = touch ? shortPl : shortEn;
          if (longText)
            for (int i = 0; i < 9; ++i)
              a.definition +=
                  "\n\nDługi opis zachowuje polskie znaki: zażółć gęślą jaźń. Każda kolejna strona ma ten sam przycisk "
                  "instalacji i możliwość powrotu.";
          a.wrapText();
          const auto area = a.bodyArea();
          assert(area.width > 0 && area.height > 0);
          assert(area.x >= 0 && area.y >= 0 && area.x + area.width <= a.renderer.width &&
                 area.y + area.height <= a.renderer.height);
          assert(a.totalPages >= 1);
          if (longText) assert(a.totalPages > 1);
          for (const auto& line : a.lines) {
            assert(line.start + line.len <= a.definition.size());
            const std::string t = a.definition.substr(line.start, line.len);
            assert(a.renderer.advance(t.c_str()) <= area.width);
          }
          for (int page = 0; page < a.totalPages; ++page) {
            a.currentPage = page;
            a.renderer.pixels.assign(a.renderer.width * a.renderer.height, 255);
            a.drawBody(0, area.x, area.y);
          }
          if (!inverted && !longText) {
            a.currentPage = 0;
            a.renderer.pixels.assign(a.renderer.width * a.renderer.height, 255);
            a.renderer.drawText(0, 20, 22, touch ? "Wtyczki" : "Plugins");
            a.drawBody(0, area.x, area.y);
            if (touch) {
              std::vector<uint8_t> fb((a.renderer.width + 7) / 8 * a.renderer.height, 255);
              fui::DisplayTarget target(fb.data(), a.renderer.width, a.renderer.height, (a.renderer.width + 7) / 8,
                                        fui::Orientation::LandscapeCounterClockwise);
              std::vector<fui::FontGlyph> glyphs;
              for (uint32_t cp = 32; cp <= 383; ++cp) {
                auto* g = a.renderer.font.getGlyph(cp);
                assert(g && g->dataOffset <= 65535);
                glyphs.push_back({static_cast<uint16_t>(g->dataOffset), g->width, g->height,
                                  static_cast<uint8_t>(fp4::toPixel(g->advanceX)), static_cast<int8_t>(g->left),
                                  static_cast<int8_t>(-g->top)});
              }
              fui::BitmapFont f{a.renderer.font.data->bitmap, glyphs.data(), 32, 383, 29, 24, 40, 40, 1};
              target.setFont(f);
              fui::FreeInkApp<24, 6> app(target, target.deviceContext());
              fui::Rect button{static_cast<int16_t>(area.x), static_cast<int16_t>(area.y + area.height + 10),
                               static_cast<int16_t>(area.width), 45};
              assert(button.y >= area.y + area.height && button.y + button.height <= a.renderer.height);
              struct Context {
                fui::Rect button;
              };
              Context context{button};
              app.setScreen(
                  [](auto& screen, void* data) {
                    fui::ButtonProps p;
                    p.label = "Zainstaluj";
                    p.action = 1;
                    screen.button(p, static_cast<Context*>(data)->button);
                  },
                  &context);
              app.render();
              for (int y = 0; y < a.renderer.height; y++)
                for (int x = 0; x < a.renderer.width; x++)
                  if (!(fb[y * ((a.renderer.width + 7) / 8) + (x >> 3)] & (0x80 >> (x & 7))))
                    a.renderer.pixels[y * a.renderer.width + x] = 0;
            } else
              a.renderer.drawText(0, 20, a.renderer.height - 35, "Back    Install     <     >");
            const std::string name = out + "/details-" + (touch ? "touch-pl-" : "buttons-en-") +
                                     (landscape ? "landscape" : "portrait") + ".pgm";
            std::ofstream image(name, std::ios::binary);
            image << "P5\n" << a.renderer.width << " " << a.renderer.height << "\n255\n";
            image.write(reinterpret_cast<const char*>(a.renderer.pixels.data()), a.renderer.pixels.size());
          }
          ++cases;
        }
  // Explicit-linebreak amplification: real wrapText, largest built-in font,
  // narrowest body in these profiles. SD fonts and real C3 heap are not measured.
  std::ofstream resources(out + "/span-budget.jsonl");
  for (int shape = 0; shape < 3; ++shape) {
    DictionaryDefinitionActivity a;
    a.confirmationUi = std::make_unique<UiAppHost>();
    gpio.touch = true;
    a.renderer.font = EpdFont(&notoserif_18_regular);
    a.renderer.width = 480;
    a.renderer.height = 800;
    a.definition = std::string(64, '\n');
    if (shape == 0) a.definition += std::string(4024, 'W');
    if (shape == 1)
      for (int n = 0; n < 2012; ++n) a.definition += "W ";
    if (shape == 2)
      a.definition = std::string(2040, 'T') + "\nv" + "v" + "\n\n" + std::string(64, '\0') + std::string(1983, 'x');
    // The exact onEnter method is covered separately in FlowTest; it normalizes NULs.
    std::replace(a.definition.begin(), a.definition.end(), '\0', '\n');
    a.wrapText();
    assert(a.lines.size() < 512);
    assert(a.lines.capacity() <= 544);
    resources << "{\"shape\":" << shape << ",\"bytes\":" << a.definition.size() << ",\"spans\":" << a.lines.size()
              << ",\"capacity\":" << a.lines.capacity()
              << ",\"spanBytes\":" << a.lines.capacity() * sizeof(DictionaryDefinitionActivity::Line) << "}\n";
  }
  std::cout << "PASS " << cases
            << " layout/pagination cases; host body font and native button component, not device rendering\n";
}
