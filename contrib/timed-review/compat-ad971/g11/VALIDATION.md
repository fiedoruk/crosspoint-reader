# Validation checkpoint

Pinned CP base: `ad971c8ac03c9765e3835b3b54ee56f0b0332abe`.
SDK: `25cd36c7c28192991f11ba99c1f520d19ff12fa5`.

This update retains four upstream commits: home-cover buffer validity,
out-of-line ActivityManager construction/destruction, width-based SSID text
truncation and keeping tilt settings when an IMU probe fails. No new firmware
patch was needed. All supplied patch bytes are unchanged from the previous
CP261726f6 checkpoint.

Applying the four commits after the previous candidate produces exactly the
same trees as applying the support patches to the new base, separately for
the timer, W06 and TIMED. Six upstream files are identical to the new base;
SettingsList.cpp preserves both the upstream tilt fix and the existing timer
entries. HAL, SDK, network transport and build configuration did not change
in these four commits.

The actual bounded settings reader and source preparation passed 21 cases plus
roots, quarantine, limits and missing-file checks under ASan/UBSan. The actual
boot orchestration also passed with Wi-Fi/display boundaries stubbed. These are
host checks; they do not observe a screen or a physical Power press.

The earlier TLS, RTC, arm, Local and USB suites retain their original checkpoint.
Their production source and SDK implementation are unchanged here. Those suites
were not repeated just to update the base; their prior result is not presented
as a new run on this candidate.

## Firmware compile/link checkpoint

One full TIMED `default` / ESP32-C3 build passed after review, using the
existing pioarduino 55.03.311 environment, SDK25 plus the explicit verification
patch, and two compiler jobs. Static RAM is 69,800 / 327,680 B; application flash
is 5,557,467 / 6,553,600 B. The image SHA-256 is
`2949b7067d57227f5cb92f481dd71efa85e7362561f96ca929fad2b9c8cd9ec1`.
The build source snapshot matches the fresh TIMED replay, including the SDK.
No standalone W06 or Picco build is claimed on this base. The full integration
build covers the changed common activity
lifecycle and settings code; Picco-specific paths are unchanged and its timer
consumer stays disabled.

No hardware was accessed. C3 runtime heap/largest block, physical Power,
RTC timing, glass, orientations and energy remain unmeasured for this revision.
SDK API/ref acceptance, C3 runtime evidence, consumer scope/HAL agreement and
required hardware acceptance remain open before proper upstream PRs. No firmware
or private service code is included in this packet.
