# TIMED integration on timer 1bc4975

This updates the existing W06/TIMED review material to timer PR #3820 at
`1bc497520f6efacd09920225d5bf319b8f4a9df6`. It keeps the new upstream settings
layout and reader font fix. The existing Source/interval definitions move to
`SettingsList.cpp`; the timer, transport and Power behavior stay unchanged.

The aim is to let a reader show useful information while idle and return to
the book when needed. A shared, bounded path also lets other SD plugins use
these capabilities without each implementing its own wake cycle.

This is dependent integration material, not a new proposal to expand #3820.
SDK #65 and the combined Off/Local/Plugin contract still require upstream
agreement. The package is not an official release or a firmware distribution.

## Reproduce

Requires Git and Python 3. From this directory:

```sh
python3 replay.py /path/to/new-checkout
```

The script fetches the exact public CP and SDK commits in `manifest.json`,
verifies patch hashes, applies them and verifies both result trees. Optional
`--cp-source` and `--sdk-source` can point to local mirrors. It does not build,
flash, push or run CI. The SDK gitlink stays at `084fdfb`; its verification
patch is applied separately. Existing destination directories are rejected.

`cp-integration.patch` includes the current #3956 token-storage prerequisite,
checked BMP and bounded event prerequisites from #3907/#3908, W06 verified
events, and the existing TIMED consumer. It is one replay patch so the new
timer primitive is not applied twice. The W06 and TIMED review scopes remain
separate; this package does not replace their existing upstream discussions.
`changes-from-t3.patch` is a comparison with the published T3 result, provided
for review only. Do not apply it after replay.

## Validation

The compatibility pass checked 1,024 wake/reset/USB/cold combinations against
the pinned timer classifier under ASan/UBSan. The HAL, main timer path and
host-test registration are byte-identical to the previously published T3.
The bounded settings harness passed 21 cases, its existing path/quarantine
checks and source assertions for the relocated shared settings list.

To run the settings check from the resulting checkout:

```sh
python3 test/timer_plugin_permission/run.py --arduinojson /path/to/ArduinoJson/src
```

One Sticky build passed with the pinned pioarduino 55.03.311 toolchain and
two jobs: static RAM 80,220 bytes, flash 5,270,547 bytes. These are linker
figures, not runtime TLS headroom. No new device test was performed on this
revision. The earlier T3 Sticky observations belong to its earlier binary;
they do not qualify this build or the new upstream font/settings behavior.

## Credit

The timer is kivarun's [#3820](https://github.com/crosspoint-reader/crosspoint-reader/pull/3820).
Local rotation and X3 SD-rail handling build on
[jadehawk's work](https://github.com/jadehawk/crosspoint-reader/commit/59555361aef55608cc56fdb5a9fccc167c37db34).
This update preserves the prior T1/T2 Power handoff and FreeInk RTC work.
CrossPoint and FreeInk licenses and the SDK notice are included unchanged.
Code and tests were developed with AI assistance; evidence is limited to
the checks described above.
