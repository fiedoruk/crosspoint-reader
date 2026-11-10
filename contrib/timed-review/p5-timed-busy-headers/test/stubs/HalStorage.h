#pragma once
#include <WString.h>
#include <fcntl.h>

#include <cstdint>
#include <functional>
#include <string>
#include <unordered_map>
struct HalFile {
  std::string* data = nullptr;
  size_t pos = 0;
  size_t readStop = SIZE_MAX;
  bool seek(uint64_t n) {
    if (!data || n > data->size()) return false;
    pos = n;
    return true;
  }
  bool seekCur(int64_t n) { return seek(pos + n); }
  int read() {
    return !data || pos >= data->size() || pos >= readStop ? -1 : static_cast<unsigned char>((*data)[pos++]);
  }
  size_t read(void* out, size_t count) {
    auto* b = static_cast<uint8_t*>(out);
    size_t n = 0;
    for (; n < count; ++n) {
      int c = read();
      if (c < 0) break;
      b[n] = c;
    }
    return n;
  }
  bool isOpen() const { return data != nullptr; }
  explicit operator bool() const { return isOpen(); }
  size_t write(const char* p, size_t n) {
    if (!data) return 0;
    data->append(p, n);
    return n;
  }
  size_t write(const uint8_t* p, size_t n) { return write(reinterpret_cast<const char*>(p), n); }
  void flush() {}
  bool close() {
    data = nullptr;
    return true;
  }
  uint64_t fileSize64() const { return data ? data->size() : 0; }
  size_t fileSize() const { return static_cast<size_t>(fileSize64()); }
  void truncate(uint64_t n) {
    if (data) data->resize(n);
  }
};
struct StorageStub {
  std::unordered_map<std::string, std::string> files;
  std::unordered_map<std::string, size_t> reads;
  std::string failRead, failRenameFrom, failRenameTo, failRemove;
  std::function<void()> afterRename;
  bool failWrite = false;
  size_t writeOpens = 0;
  std::string lastWritePath;
  size_t readStop = SIZE_MAX;
  bool openFileForRead(const char*, const std::string& path, HalFile& out) {
    auto it = files.find(path);
    if (it == files.end() || path == failRead) return false;
    out.data = &it->second;
    out.pos = 0;
    out.readStop = readStop;
    return true;
  }
  bool readFileToString(const char*, const std::string& path, size_t cap, std::string& out) {
    ++reads[path];
    const auto it = files.find(path);
    if (it == files.end() || it->second.size() > cap) return false;
    out = it->second;
    return true;
  }
  bool openFileForWrite(const char*, const std::string& path, HalFile& f) {
    if (failWrite) return false;
    ++writeOpens;
    lastWritePath = path;
    files[path].clear();
    f.data = &files[path];
    return true;
  }
  bool openFileForWrite(const char* t, const char* p, HalFile& f) { return openFileForWrite(t, std::string(p), f); }
  HalFile open(const char* path, int) { return HalFile{&files[path]}; }
  bool remove(const char* path) { return failRemove == path ? false : files.erase(path) != 0; }
  bool exists(const char* path) const { return files.find(path) != files.end(); }
  bool rename(const char* from, const char* to) {
    if (failRenameFrom == from || failRenameTo == to) return false;
    auto it = files.find(from);
    if (it == files.end() || exists(to)) return false;
    files[to] = it->second;
    files.erase(it);
    if (afterRename) afterRename();
    return true;
  }
  bool writeFile(const char* path, const String& value) {
    files[path] = value.value;
    return true;
  }
};
inline StorageStub Storage;
