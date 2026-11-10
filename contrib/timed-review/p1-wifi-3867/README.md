# Saved Wi-Fi fallback for sleep events

Support for garciacd's CrossPoint PR #3867. The original fallback proposal is
credited to its author; this update narrows it to CP develop
`36bd50d089a8b3f14b0cfc29dd5ae6ffeb197254`, which already loads the store.

A missing last-connected SSID can occur after adding a network through the web
interface or deleting the last-used network while other saved entries remain.
Use the last-used entry when it exists; otherwise use the first saved entry.
An empty SSID ends the attempt. This does not scan for networks, skip malformed
entries, or try another credential when connection fails. No persistent state
or SDK API is added. The existing join timeout and plugin gates remain.

## Stock CrossPoint

1. Check out the CP commit above in a fresh working directory.
2. Apply `stock-3867.patch` with `git apply`.
3. Copy this package's `test/wifi_fallback` directory into `test/`.
4. Set `CROSSPOINT_ARDUINOJSON_INCLUDE` to ArduinoJson 7.4.2's `src` directory.
5. Run `CROSSPOINT_STOCK_MAIN=src/main.cpp python3 test/wifi_fallback/run.py`.

The unpatched revision fails the expected-join assertion for a missing last SSID.
The patched revision passes. The test uses ASan/UBSan and a C++20 host compiler.
See the test README for the mocked boundaries and individual cases.

## Existing W06/TIMED support candidate

This is a separate integration delta, not a prerequisite for the stock fix.
Start from the `cp2-36bd` support packet at commit
`8b4d847e8419abf3600b46661b8d3d8c07339983` in
https://github.com/fiedoruk/crosspoint-reader/tree/8b4d847e8419abf3600b46661b8d3d8c07339983/contrib/timed-review/cp2-36bd
and follow its replay instructions. Its CP tree before this change is
`dde9bbf15a5f893e43677b365b7084c3956ba69f`; SDK tree is
`6fbe86ea33fce1cd0907e99f3a8354df61de18c2` on pinned SDK `6a208c0c`.

Apply `timed-3867.patch` and `timed-harness.patch`, then copy the test directory.
Do not apply `stock-3867.patch` to this integration. Run the fallback test without
`CROSSPOINT_STOCK_MAIN`, and run the existing `test/timed_sync/run.py`.

HOST checks compile real credential-store code and extracted production callers;
file IO, obfuscation, radio, clock, display and plugin boundaries are simulated.
They do not demonstrate physical radio, SD or panel operation. Hardware validation
on this revision remains outstanding. No firmware binary is distributed here.

The unchanged loader can reload persisted state over in-memory edits after a
failed save; this packet does not change persistence semantics. Selection uses
existing separate store locks, not an atomic transaction with concurrent edits.

Code and tests were prepared with AI assistance. This is support material for
the existing PR, not an upstream approval or release.
