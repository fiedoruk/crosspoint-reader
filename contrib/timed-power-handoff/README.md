# Power handoff during timed wallpaper refresh

This patch targets Jadehawk's experimental timedwake-r1, not raw CrossPoint develop. It preserves the existing local wallpaper consumer and X3 rail behavior. It does not add online delivery. Hardware results and limitations are in NOTES.en.md.

## Apply

```sh
git clone https://github.com/jadehawk/crosspoint-reader.git
cd crosspoint-reader
git checkout --detach 59555361aef55608cc56fdb5a9fccc167c37db34
git submodule update --init freeink-sdk
git apply --check ../t1-power.patch
git apply ../t1-power.patch
python3 test/timed_power_wake/run.py --baseline 59555361aef55608cc56fdb5a9fccc167c37db34
python3 test/timer_wake_arm/run.py
```

SDK must remain at `7fcd3b34c108f28c086ade3b433924022dbc0998`. Host checks use Python3 and Clang with C++20/ASan/UBSan. Use the repository's existing board build environment for firmware. A fresh local receiver reproduced apply and host checks from the pinned base; it reused Git objects without repeating the network clone.

The patch includes five production files, regression tests and a device procedure. No firmware image, private bench control or service implementation is included. Existing project license and attribution remain applicable; see LICENSE.
