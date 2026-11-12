#include <cassert>
#include <cstdint>
#include <cstring>
#include <memory>
#include <string>
#include <vector>
#define LOG_ERR(...) ((void)0)
std::vector<uint8_t> output;
struct HalFile {
  size_t write(const uint8_t* p, size_t n) {
    output.insert(output.end(), p, p + n);
    return n;
  }
  void close() {}
};
struct {
  bool exists(const char*) { return true; }
  bool mkdir(const char*) { return true; }
  bool remove(const char*) {
    output.clear();
    return true;
  }
  bool openFileForWrite(const char*, const char*, HalFile&) {
    output.clear();
    return true;
  }
} Storage;
template <class T>
auto makeUniqueNoThrow(size_t n) {
  return std::make_unique<T>(n);
}
struct GfxRenderer {
  enum Orientation { Portrait, LandscapeClockwise, PortraitInverted, LandscapeCounterClockwise };
  Orientation orientation;
  int panelWidth, panelHeight, panelWidthBytes;
  std::vector<uint8_t> buffer;
  uint8_t* frameBuffer;
  bool _stripActive = false;
  int _stripY0 = 0, _stripRows = 0;
  uint8_t* _stripBuf = nullptr;
  int clipLeft_ = 0, clipTop_ = 0, clipRight_, clipBottom_;
  GfxRenderer(Orientation o, int w, int h)
      : orientation(o),
        panelWidth(w),
        panelHeight(h),
        panelWidthBytes((w + 7) / 8),
        buffer(panelWidthBytes * h, 255),
        frameBuffer(buffer.data()),
        clipRight_(getScreenWidth()),
        clipBottom_(getScreenHeight()) {}
  int getScreenWidth() const {
    return orientation == Portrait || orientation == PortraitInverted ? panelHeight : panelWidth;
  }
  int getScreenHeight() const {
    return orientation == Portrait || orientation == PortraitInverted ? panelWidth : panelHeight;
  }
  int getDisplayWidth() const { return panelWidth; }
  int getDisplayHeight() const { return panelHeight; }
  int getDisplayWidthBytes() const { return panelWidthBytes; }
  Orientation getOrientation() const { return orientation; }
  const uint8_t* getFrameBuffer() const { return frameBuffer; }
  void drawPixel(int, int, bool) const;
};
struct ScreenshotUtil {
  static bool saveFramebufferAsBmp(const char*, const GfxRenderer&);
};
PRODUCTION_METHODS
int main() {
  for (int o = 0; o < 4; ++o)
    for (auto dimensions : {std::pair{800, 480}, std::pair{17, 9}}) {
      GfxRenderer r(static_cast<GfxRenderer::Orientation>(o), dimensions.first, dimensions.second);
      int w = r.getScreenWidth(), h = r.getScreenHeight();
      for (int y = 0; y < h; ++y)
        for (int x = 0; x < w; ++x)
          if ((x * 3 + y * 5) % 17 == 0) r.drawPixel(x, y, true);
      assert(ScreenshotUtil::saveFramebufferAsBmp("/test.bmp", r));
      BmpHeader header;
      std::memcpy(&header, output.data(), sizeof(header));
      assert(header.infoHeader.biWidth == w && header.infoHeader.biHeight == h && header.infoHeader.biBitCount == 1);
      size_t stride = ((w + 31) / 32) * 4;
      assert(output.size() == header.fileHeader.bfOffBits + stride * h);
      for (int y = 0; y < h; ++y)
        for (int x = 0; x < w; ++x) {
          uint8_t byte = output[header.fileHeader.bfOffBits + (h - 1 - y) * stride + x / 8];
          bool white = (byte >> (7 - x % 8)) & 1;
          assert(white != ((x * 3 + y * 5) % 17 == 0));
        }
    }
}
