# W06 and TIMED on CP 91ed / SDK f9

This series reuses the existing verified-event transport and Off/Local/Plugin
consumer on CP `91ed3ef8` / SDK `f9cc1bed`. It ports the two timer settings entries to
upstream's forEachBaseSetting visitor, keeping the same keys, values and board
exclusions. StaticEnum borrows immutable labels; persistence does not recreate
the old retained settings list. UI callers keep using the upstream collector.

The narrow early timer settings read and source migration are preserved.
CMake retains the new recursive-dictionary test and registers our existing
host tests once. The SDK verification patch remains unchanged. Current SDK
book, display and input changes remain on the pinned upstream implementation.

## Replay

Requires Git and Python 3:

```sh
python3 replay.py /path/to/w06-checkout --through w06
python3 replay.py /path/to/timed-checkout --through timed
```

Replay fetches public commits, verifies every patch and checks intermediate
trees. Optional local mirrors use --cp-source and --sdk-source. It does not
build, flash, commit, push or start CI.

Patches 00–02 are token/BMP/budget prerequisites; 03 is W06, 04 the existing timer
with its compatible HAL arguments, 05 the TIMED consumer and visitor adaptation.
The SDK verification patch is explicit, pending the SDK API/ref decision.
Picco/Metalio consumer exclusions remain; this adds no product model.

## Host checks

From the full TIMED checkout, with ArduinoJson 7.4.2 headers:

```sh
python3 test/timer_plugin_permission/run.py --arduinojson /path/to/ArduinoJson/src
```

This runs the actual bounded reader and preparation, followed by a fixture of
the actual TIMED descriptors, generic persistence callbacks and UI collector.
It checks 27 round trips, defaults/migration, invalid data and excluded boards.
Other registry entries and physical UI are outside that fixture.

The ordinary CMake path also registers these tests:

```sh
cmake -S test -B /path/to/host-build -DCMAKE_BUILD_TYPE=Release
cmake --build /path/to/host-build --target WakeupClassifyTest --parallel 2
ctest --test-dir /path/to/host-build -R 'WakeupClassify|TrustedTimeFresh|TimerWakeArm|TimedWakeGuard|TimerPluginPermission' --output-on-failure --parallel 1
```

CMake can use existing dependency sources through FETCHCONTENT_SOURCE_DIR_GOOGLETEST,
FETCHCONTENT_SOURCE_DIR_ARDUINOJSON and ANIMATEDGIF_SOURCE_DIR; the AnimatedGIF
host path runs upstream's dependency patch, so use an owned copy for it.
If a wrapper exposes only cmake on PATH, use the CMAKE_CTEST_COMMAND path
recorded in the generated CMakeCache.txt for the matching ctest executable.
See VALIDATION.md for recorded results and the distinction from previous TLS
and device evidence. No new hardware qualification follows from host tests.

The aim remains useful information between reading sessions, with one timer
owner and shared authenticated transport for SD plugins. The reader keeps its
ordinary role. SDK acceptance, physical C3 memory evidence and consumer scope
remain open before proper upstream PRs and release.

The timer belongs to Michael Kazakov/kivarun. Local refresh builds on jadehawk's
work; PaperMono uses the FreeInk RTC/PMIC work. SDK verification reuses #65.
Licenses/notices and these credits are retained. AI assistance was used for
code, tests and descriptions. No firmware or private service code is included.
