# Verified downloads and one timed sleep-screen consumer

This review series adds verified event downloads and then joins local wallpaper
rotation and an SD-plugin refresh under one timer owner. The reader can show
updated information while idle and still return to the book when Power is used.
Shared firmware capabilities also let other SD plugins use the same path.

This is dependent integration material. The SDK verification API and the
Off/Local/Plugin setting still need upstream agreement. It is not an official
release, a replacement firmware distribution, or a claim of support on every
CrossPoint model.

## Replay

Requires Git and Python 3. No build or flash is started by this command:

```sh
python3 replay.py /path/to/new-checkout
```

`replay.py` verifies patch hashes, checks out public CP commit
`7a76e1244b758acf5f1ced41cea9ecffdbd4ac44` and SDK commit
`084fdfb24b16e890844ca5cb44951694ba8d6c56`, then applies the series and verifies
the resulting CP tree. The CP base is the revised #3956 on develop
`089e7ae5f9bebc96973b07802815a81cf4715bbe`. The SDK gitlink is unchanged;
the SDK patch is applied to that checkout separately.

| Material | Role |
| --- | --- |
| `01-checked-bmp.patch` | Existing #3907 prerequisite, adapted to this base |
| `02-bounded-events.patch` | Existing #3908 prerequisite, adapted to this base |
| `sdk-verified.patch` | Existing SDK #65 verification adaptation |
| `03-verified-events.patch` | W06: trust, time and authenticated event requests |
| `04-timed-source.patch` | TIMED: one owner, Off/Local/Plugin, Power and sleep |

Use `--through w06` to stop before the timer integration. Optional `--cp-source`
and `--sdk-source` accept local mirrors; the pinned commits and tree checks remain
mandatory. Local reconstruction used mirrors of these public objects.

The first two patches are included so the integration can be reviewed and
replayed. They do not create replacement PRs for #3907 or #3908. The final two
are distinct review scopes, not two timers to arm independently.

## Checks

See `NOTES.en.md` for the recorded results and their limits. Host tests require
a C++20 compiler and ArduinoJson 7 headers. With the include directory supplied:

```sh
python3 test/plugin_verified_http/run.py --arduinojson /path/to/ArduinoJson/src --sanitize
CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src python3 test/timed_sync/run.py --boot-only --sanitize
python3 test/timed_local/run.py
CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src python3 test/timed_sync/run.py --usb-only --sanitize
```

The TIMED commands require the full series. They exercise production
methods with specified host boundaries; they do not emulate a physical panel,
button or SD card. A firmware build uses the normal project toolchain, for
example `pio run -e sticky -j2`. Hardware validation needs the exact built image.

## Credit and scope

The timer originates in [CP #3820](https://github.com/crosspoint-reader/crosspoint-reader/pull/3820).
The Local consumer and X3 SD-rail behavior come from
[jadehawk's Razor-Crest work](https://github.com/jadehawk/crosspoint-reader/commit/59555361aef55608cc56fdb5a9fccc167c37db34). This integration reuses the previous
TIMED transport and T1/T2 Power handoff; PaperMono RTC behavior builds on the
Free-Ink SDK work. Existing authorship and licenses remain in the source.
`LICENSE` retains the CrossPoint license; `LICENSE-SDK` and `NOTICE-SDK`
retain the pinned FreeInk SDK license and attribution. The package contains
only upstream integration material.

Code and tests were developed with AI assistance and reviewed for the stated
scope. Host, build and hardware evidence are reported separately.
