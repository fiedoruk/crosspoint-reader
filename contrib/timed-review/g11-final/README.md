# Verified plugin events, then timed sleep refresh

Two review scopes, in order: W06 adds an opt-in verified transport to existing
plugin events; TIMED uses it for one autonomous sleep-screen consumer. The aim
is useful information while the reader is idle, without taking over reading or
requiring each SD plugin to implement a wake cycle.

These are dependent candidates, not two ready-to-merge PRs against unmodified
develop. The existing prerequisites are supplied for reproduction and keep their
authors and PRs. The SDK verification API and the timer consumer's scope still
need maintainer agreement. No firmware or private service code is included.

## Reproduce either scope

Use Git and Python 3, from this directory, with a new destination:

```sh
python3 replay.py /path/to/w06-checkout --through w06
python3 replay.py /path/to/timed-checkout --through timed
```

Each command fetches public CP `b64d797c` and SDK `084fdfb`, checks patch hashes,
applies the required steps and checks every result tree. Full hashes are in
`manifest.json`. The SDK gitlink stays unchanged; its adaptation is applied
separately. Optional `--cp-source` and `--sdk-source` accept local mirrors of
those public commits. No build, flash, push or CI is started.

| Patch | Role |
|---|---|
| 00-token-storage | Existing #3956 at bb3460bc |
| 01-checked-bmp | Existing #3907 |
| 02-bounded-events | Existing #3908 |
| 03-verified-events | W06 candidate; no timer, HAL or sleep-screen UI |
| 04-timer-prerequisite | kivarun's #3820 at 1bc4975; test registration context adapted |
| 05-timed-source | TIMED candidate on W06 and the timer prerequisite |
| sdk-verified | Existing SDK #65 adaptation to the pinned SDK |

Only patches 03 and 05 are the proposed CP PR scopes. Do not apply a whole
prerequisite again after its upstream merge. Rebase the relevant candidate and
verify the resulting delta when the accepted refs become available. The full
series preserves current develop changes, including its static GIF support.

## Check the result

Host checks require a C++20 compiler and ArduinoJson 7.4.2 headers. In the
replayed checkout, replace `/path/to/ArduinoJson/src` with that include directory:

```sh
python3 test/plugin_event_budget/run.py --arduinojson /path/to/ArduinoJson/src --sanitize
python3 test/plugin_verified_http/run.py --arduinojson /path/to/ArduinoJson/src --sanitize
python3 test/trusted_time_fresh/run.py
```

For the full TIMED stage:

```sh
export CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src
python3 test/timed_sync/run.py --sanitize
python3 test/timed_sync/run.py --boot-only --sanitize
python3 test/timed_sync/run.py --capture-only --sanitize
python3 test/timed_sync/run.py --usb-only --sanitize
python3 test/timed_local/run.py
python3 test/timed_wake_guard/run.py
python3 test/timer_wake_arm/run.py
python3 test/papermono_timer/run.py
python3 test/timer_plugin_permission/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE"
```

Real TLS checks also require Python `cryptography`, OpenSSL-backed `ssl`, and
Arduino-wolfSSL 5.7.2. The package includes the existing `build_wolfssl.py` helper
for its POSIX host archive, with two compiler jobs and reduced priority:

```sh
python3 /path/to/packet/build_wolfssl.py --wolf-root /path/to/Arduino-wolfSSL
python3 test/plugin_verified_tls/run.py --wolf-root /path/to/Arduino-wolfSSL --wolf-archive /path/to/packet/build/libwolfssl-host.a --arduinojson /path/to/ArduinoJson/src --output /path/to/w06-tls.json
# Full TIMED stage only:
python3 test/timed_sync/real_tls.py --wolf-root /path/to/Arduino-wolfSSL --wolf-archive /path/to/packet/build/libwolfssl-host.a --arduinojson /path/to/ArduinoJson/src --output /path/to/timed-tls.json
```

These use loopback and temporary synthetic credentials. They do not measure
radio, C3 heap, real SD durability or displayed pixels. `VALIDATION.md` separates
current results from earlier device evidence. Firmware builds use the normal
pinned project toolchain; `PLATFORMIO_RUN_JOBS=2 nice -n 10 pio run -e default -j2`
builds the C3 baseline. Never flash it onto an X4 Pro, Sticky or PaperMono.

## Credit and scope

The timer is Michael Kazakov/kivarun's #3820. Local rotation and X3 SD-rail
handling build on jadehawk's Razor-Crest work. The PaperMono adapter uses the
FreeInk RTC implementation. W06 reuses the SDK #65 verification work; existing
licenses and attribution are included in LICENSE, LICENSE-SDK and NOTICE-SDK.
Code, tests and these notes were developed with AI assistance. The reader
remains the primary application; the proposed idle-screen policy is not an
accepted upstream capability or an official release.
