#pragma once
#include <cstdint>
#include <string>
class String {
 public:
  String() = default;
  explicit String(const char* s) : value(s) {}
  const char* c_str() const { return value.c_str(); }
  size_t write(uint8_t c) {
    value.push_back(static_cast<char>(c));
    return 1;
  }
  size_t write(const uint8_t* data, size_t n) {
    value.append(reinterpret_cast<const char*>(data), n);
    return n;
  }
  void remove(size_t) { value.clear(); }
  size_t length() const { return value.size(); }
  bool reserve(size_t n) {
    value.reserve(n);
    return true;
  }
  bool concat(const char* p, size_t n) {
    value.append(p, n);
    return true;
  }
  int read() { return pos < value.size() ? static_cast<unsigned char>(value[pos++]) : -1; }
  size_t readBytes(char* out, size_t n) {
    size_t copied = 0;
    while (copied < n && pos < value.size()) out[copied++] = value[pos++];
    return copied;
  }
  std::string value;
  size_t pos = 0;
};
