# Saved Wi-Fi selection host test

Set `CROSSPOINT_ARDUINOJSON_INCLUDE` to ArduinoJson 7.4.2 `src/`, then run:

```sh
CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src python3 test/wifi_fallback/run.py
```

This tests the full W06/TIMED candidate. To run the sleep-entry subset on a raw
CrossPoint 36bd checkout, copy this `test/wifi_fallback` directory there and run:

```sh
CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src \
CROSSPOINT_STOCK_MAIN=src/main.cpp python3 test/wifi_fallback/run.py
```

The harness compiles the actual WifiCredentialStore.cpp, actual JSON parsing and
production function bodies extracted from main.cpp. JSON file IO and password
obfuscation are substituted in memory; Wi-Fi, display, timing, clock and plugin
boundaries are stubs. Thus this demonstrates selection and caller control flow,
not actual SD, radio, network delivery, firmware or device behavior. ASan and
UBSan are enabled, requiring a supported C++20 host compiler.

Cases: empty and stale last SSID with saved networks, valid last SSID precedence,
no saved networks, removed last network, malformed empty SSID, no handler,
network-disabled sleep, Off and disabled plugin (TIMED only), and one failed
join with the 10-second cooperative timeout. It does not scan for alternatives or
retry a second credential when a chosen network is unreachable.
