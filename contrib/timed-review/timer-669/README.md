# W06 and TIMED with the bool-second timer API

This series aligns the existing full TIMED consumer with kivarun's updated
#3820 at `669642d2` on CP `0fcdb3ec` / SDK `f9cc1bed`. The held-button flag
is the second argument and the timer interval is third. The consumer keeps its existing
fourth argument for captured-Power recovery during timer teardown.

Ordinary sleep passes the held-button flag and interval in that order. Timer
rearm and recovery standby pass `false`, the interval, and the existing recovery
context. Default button-only calls stay unchanged. The newer author head `a38095cf`
has an identical source tree; it does not change this contract. No new state, task, network
policy, setting or allocation is introduced by this alignment.

The visitor settings, bounded early reader, Off/Local/Plugin selection and
PaperMono adapter remain from the previous consumer. The SDK verification
patch is unchanged. Picco/Metalio consumer exclusions remain in place.

## Replay

Requires Git and Python 3. Use a destination path that does not exist for each scope:

```sh
python3 replay.py /path/to/w06-checkout --through w06
python3 replay.py /path/to/timed-checkout --through timed
```

Replay fetches the public CP/SDK refs and checks patch hashes and result trees.
Optional local mirrors use --cp-source and --sdk-source. It does not build,
flash, commit, push or start CI.

Patches 00–02 are token/BMP/budget prerequisites; 03 is W06. Patch 04 carries
kivarun's 669 timer with only CMake registration context adjusted for W06.
Patch 05 is the full consumer on that prerequisite. Do not layer the previous
visitor-era timer patch over this one. The SDK patch remains explicit and
pending acceptance of its API/ref.

## Host checks

From the full TIMED checkout, with ArduinoJson 7.4.2 headers:

```sh
export CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src
python3 test/timed_sync/run.py --sanitize
python3 test/timed_sync/run.py --sanitize --usb-only
python3 test/timer_wake_arm/run.py
python3 test/timer_plugin_permission/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE"
```

The timer tests exercise the extracted production sleep function across C3,
EXT1, PaperMono and Picco host boundaries. They check exact intervals, zero
interval with a held button, timer plus held button, arming failures, cleanup
and Power handoff. The boot tests run production orchestration with WiFi,
storage and display boundaries stubbed; ordinary sleep wiring has a separate
source assertion. These are host checks, not physical power measurements.

The existing CMake path preserves the upstream tests:

```sh
cmake -S test -B /path/to/host-build -DCMAKE_BUILD_TYPE=Release
cmake --build /path/to/host-build --target WakeupClassifyTest --parallel 2
ctest --test-dir /path/to/host-build -R 'WakeupClassify|TrustedTimeFresh|TimerWakeArm|TimedWakeGuard|TimerPluginPermission' --output-on-failure --parallel 1
```

Existing dependency sources can be supplied with FETCHCONTENT_SOURCE_DIR_GOOGLETEST,
FETCHCONTENT_SOURCE_DIR_ARDUINOJSON and ANIMATEDGIF_SOURCE_DIR. Use an owned copy
of AnimatedGIF because its CMake path applies a dependency patch. If ctest is
not on PATH, use CMAKE_CTEST_COMMAND from the generated CMakeCache.txt.
See VALIDATION.md for measured results and remaining limits.

This keeps one shared wake primitive for useful idle screens and SD plugins
while preserving normal reading. SDK acceptance, physical C3 memory evidence,
consumer scope and official release remain separate requirements.

The timer belongs to Michael Kazakov/kivarun. Local refresh builds on jadehawk's
work; PaperMono uses the FreeInk RTC/PMIC work. SDK verification reuses #65.
Licenses and notices are retained. AI assistance was used for code, tests and
descriptions. No firmware or private service code is included.
