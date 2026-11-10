# TIMED busy-header host test

This test runs the actual TIMED consumer, PluginHttp, SDK HTTP parser, bitmap validation and paint caller. The SDK FakeNet transport is adapted to count open connections. SecureClient is a scripted transport stub and reports peer-verification capability; this test does not perform TLS or certificate verification. Storage, clock and panel are host fixtures. The test does not measure a physical device, DNS/TCP blocking, real FAT, or a 15-second wall-clock deadline.

Use an assembled P4 future-lane CP tree with its actual future SDK applied, and ArduinoJson 7.4.2 headers. A C++20 compiler with ASan/UBSan is required. The P4 source bundle is in public commit `f7dbdb3c673526b15b4732f2fa6e7849452dea29`, under `contrib/timed-review/cp2-b32-sdk-lanes`. Its instructions and patches define the prerequisites; this test does not apply them. The CP base is `b32f907e5b6bcdaf80dad5b2fb52a3b3ef869802`, CP full tree `22c67de7a62e37a02bf43263bc6413fc95c91336`, actual SDK base `5f0d52196a770947f7f27f15701c2b1430569697`, SDK full tree `942814decb094f492771ce63aed20161dcd1c7e3`; CP gitlink remains `6a208c0c46cce99bafa334bc4f171f5e558c5195`. Check the inventory before running.

```sh
python3 test/run.py --cp /path/to/assembled-cp --arduinojson /path/to/ArduinoJson/src
ulimit -c 0
python3 test/run.py --cp /path/to/assembled-cp --arduinojson /path/to/ArduinoJson/src --negative-control
```

The negative control builds a temporary shadow copy of the SDK header with its inner busy-loop abort poll removed. Both abort and budget cases must reject that mutation via the progress oracle. The temporary copy is deleted after the run; the CP and SDK trees are never modified.

The stream is a 401 response with an overlong CSP followed by complete headers. The trigger is byte 4300, within the discarded portion, while further bytes remain immediately available. The abort case polls a callback; the budget case advances the independent budget clock at that threshold. The response also configures a password grant so that additional authentication or retry would be visible in the recorded requests. Before any fixture cleanup, assertions check the return, byte progress, one request, no rename/draw/paint, old bytes, the entire private file map (including token, manifest, CA, outbox and reader state), exactly one write-open of `.part`, its removal, and closed transport. A fresh prepare then successfully stages, commits and paints a valid BMP. A valid response is also tested independently first.

The FakeNet, Client and base64 stubs are based on the SDK host suite. WString and HalStorage derive from the CP host suite; additions are `c_str()`, write-open counting and open-connection counting. `Arduino.h` combines the existing virtual-clock and WString host surfaces.
