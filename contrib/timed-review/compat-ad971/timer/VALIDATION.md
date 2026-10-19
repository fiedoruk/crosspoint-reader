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

The production sleep-method harness is the existing regression for zero/default
sleep, explicit timers, held-button wake, arm/cleanup failures and board teardown.
It passed from the fresh replayed checkout. The standalone timer
has no SDK verification patch or refresh consumer.

No new standalone-timer firmware build is claimed for this base. The companion
full G11 integration receives one C3 compile/link check; that image includes
additional dependencies and is not a standalone-timer build.

No hardware was accessed. C3 runtime heap, physical Power, RTC timing, glass,
orientations and energy remain unmeasured on this base. Prior builds and
hardware results keep their earlier hashes. This is source/host review support
for updating the original author's branch, not merge or release acceptance.
