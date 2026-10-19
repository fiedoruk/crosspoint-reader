# W06 and TIMED on develop ad971c8a / SDK25cd

This updates the previously supplied W06/TIMED series to the same CP/SDK base
as the accompanying timer resolution. The existing SDK verification adaptation
applies unchanged: the relevant SecureNet files did not change between the two
SDK pins. All new SDK board, battery and power behavior is retained.

W06 remains a separate verified-event scope. TIMED adds one Off/Local/Plugin
consumer on the reconciled timer. Its internal calls pass the upstream
held-button flag, then the interval, then the timer-Power handoff flag explicitly.
The previous checked Local Bitmap allocation and its failure behavior remain.

Picco's ordinary charging hold, slide-switch, recovery exclusion and USB wake
behavior are retained. This packet does not enable the autonomous consumer or
its settings on Picco. That requires separate device qualification; the
network consumer continues to target Sticky, X4 Pro and PaperMono.

## Replay

Requires Git and Python 3, from this directory:

```sh
python3 replay.py /path/to/w06-checkout --through w06
python3 replay.py /path/to/timed-checkout --through timed
```

The scripts fetch the public refs in manifest.json, verify patch hashes and
check each intermediate result tree. Local mirrors can be supplied using
`--cp-source` and `--sdk-source`. No build, commit, flash, push or CI is started.

Patches00–02 are the existing token/BMP/budget prerequisites. Patch03 is W06,
patch04 is the original timer with the accompanying conflict resolution, and
patch05 is TIMED. The SDK verification patch is explicit; it does not replace
current SDK board/power changes or claim acceptance of SDK #65.

The reader should be able to show useful information while idle, through one
shared transport and timer, without losing ordinary reading behavior. This
series provides a reviewable integration of those capabilities, not an official
release or a service-specific firmware.

## Checks and scope

The preserved host runners cover event budgets, three verification-capability
modes, clock freshness, actual TLS loopback, timer configuration and boot,
GPIO/PMIC capture, Local rendering, arm/RTC and USB-cold-boot behavior. The
new checks keep Picco's ordinary USB path awake while its timer consumer stays
off. The timer harness also exercises the held-button argument separately from
the timer interval.

With ArduinoJson7.4.2 headers available, run from a replayed checkout:

```sh
python3 test/plugin_verified_http/run.py --arduinojson /path/to/ArduinoJson/src --sanitize
python3 test/trusted_time_fresh/run.py
export CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src
# Full TIMED stage:
python3 test/timed_sync/run.py --boot-only --sanitize
python3 test/timed_sync/run.py --usb-only --sanitize
python3 test/timer_wake_arm/run.py
python3 test/papermono_timer/run.py
python3 test/timed_local/run.py
python3 test/timer_plugin_permission/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE"
```

Actual TLS loopback uses the existing `build_wolfssl.py` helper and the commands
in `test/plugin_verified_tls/README.md`. The TIMED companion is
`test/timed_sync/real_tls.py`, with the same `--wolf-root`, `--wolf-archive`,
`--arduinojson` and `--output` options. Synthetic credentials are temporary.
Neither host TLS nor a firmware build measures C3 runtime heap or physical glass.

VALIDATION.md records exact checks and limitations. SDK API/ref acceptance,
C3 runtime evidence, consumer scope/HAL agreement and required hardware
acceptance remain open before proper upstream PRs. Existing prerequisites must
be reconciled after landing rather than added again.

## Credit

The timer belongs to Michael Kazakov/kivarun. Local refresh and X3 rail work
build on jadehawk's implementation; PaperMono uses the FreeInk RTC/PMIC work.
This update preserves those credits and the CP/SDK licenses and notices.
The verification adaptation reuses the SDK #65 work. AI assistance was used for
the code adaptation, tests and descriptions. No firmware or private service
implementation is included.

## Four-commit compatibility update

The patch bytes are unchanged from the preceding CP261726f6 checkpoint.
This replay includes the upstream home-cover fix, out-of-line ActivityManager
constructor/destructor, width-based Wi-Fi SSID truncation and tilt-setting
persistence fix. Applying the upstream delta before or after the support
series gives the same tree. VALIDATION.md separates this source result from
host, firmware and device evidence.
