# W06 and TIMED on the CP 2.0 development base

This packet adapts the existing review series to CrossPoint `36bd50d0` and its
pinned FreeInk SDK `6a208c0c`. It is dependent integration material, not a
plugin that adds missing firmware capabilities to an installed release.

The shared primitives let an explicitly enabled sleep-screen consumer refresh
information while the reader is idle. Content, account policy and rendering
remain outside the firmware; ordinary reading remains on the existing path.

## Contents and ownership

- `00`–`02`: token persistence, checked BMP promotion and shared sleep-event
  budget, corresponding to the existing #3956, #3907 and #3908 work.
- `03`: W06 verified event transport and fresh time, using the proposed SDK #65
  capability contract. The explicit SDK patch retains current upstream memory
  ownership; it does not enable optional wolfSSL input-buffer retention.
- `04`: kivarun's timer primitive, with registration/context adaptation.
- `05`: the full Local/SD-plugin consumer, including the PaperMono RTC adapter
  and captured-Power recovery. There is one timer owner and one panel owner.

Local rotation includes BMPs from both `/.sleep` and `/sleep`, without writing
reader history on a timer wake. The network consumer remains limited to Sticky,
X4 Pro and PaperMono. The PMIC wake route must be disabled before PaperMono can
fall back to button-only shutdown when RTC setup fails. Unknown route state
still restarts instead of shutting down.

## Replay

Requires Git and Python 3. Use a new destination for each command:

```sh
python3 replay.py /path/to/w06 --through w06
python3 replay.py /path/to/timed --through timed
```

The script fetches public pinned refs, checks every patch hash and verifies
result trees. `--through w04` and `--through prerequisites` provide the isolated
prerequisite stages. Local source mirrors can be supplied with `--cp-source`
and `--sdk-source`. No build, flash, commit, push or CI is started by replay.

## Host checks

Set the path to existing ArduinoJson 7.4.2 headers. From the W06 checkout:

```sh
export CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src
python3 test/plugin_verified_http/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --sanitize
python3 test/plugin_event_budget/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --sanitize
```

From the TIMED checkout, with the same environment variable:

```sh
python3 test/timed_sync/run.py --sanitize
python3 test/timed_sync/run.py --sanitize --usb-only
python3 test/timed_local/run.py
python3 test/timer_wake_arm/run.py
python3 test/timer_plugin_permission/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE"
python3 test/papermono_timer/run.py
```

The standalone W04 test is for the W04 replay stage, before the later event-drain
overloads. From that checkout:

```sh
ARDUINOJSON_SRC="$CROSSPOINT_ARDUINOJSON_INCLUDE" python3 test/plugin_event_asset/run.py
```

For actual TLS over POSIX loopback, use the existing Arduino-wolfSSL 5.7.2
package and Python `cryptography`. The supplied host-library builder uses two
workers, records the archive hash and does not install dependencies:

```sh
python3 /path/to/packet/build_wolfssl.py --wolf-root /path/to/Arduino-wolfSSL --output-dir /path/to/client-build
python3 /path/to/packet/build_wolfssl.py --wolf-root /path/to/Arduino-wolfSSL --output-dir /path/to/server-build --server-no-mfl
```

Then, from W06 or TIMED:

```sh
python3 test/plugin_verified_tls/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --wolf-root /path/to/Arduino-wolfSSL --wolf-archive /path/to/client-build/libwolfssl-host.a --wolf-server-archive /path/to/server-build/libwolfssl-host.a --output /path/to/tls-results.json
```

The full network consumer also has a composed loopback check, from TIMED:

```sh
python3 test/timed_sync/real_tls.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --wolf-root /path/to/Arduino-wolfSSL --wolf-archive /path/to/client-build/libwolfssl-host.a --output /path/to/timed-tls-results.json
```

## Limits

The 15-second attempt budget is cooperative. DNS/TCP can block without polling
cancellation; it is not a guaranteed wake-to-sleep or Power-response deadline.
Certificate, transport and BMP failures retain the last-good network image.
A later local grayscale failure can leave the completed monochrome base.

Routine content updates can use the same endpoint and scoped credential.
Automatic credential/CA-root rotation and server-controlled cadence are not
implemented by this packet. A 204/304 response is not a successful no-change
cycle. Do not promise those properties from server caching alone.

See VALIDATION.md for measured builds, host results and remaining device gates.
No physical panel, Power, energy or C3 runtime-heap acceptance is claimed for
this revision. SDK acceptance, consumer scope and an official release remain
separate. No firmware binary or private service code is included.

Timer authorship remains with Michael Kazakov/kivarun; local refresh builds on
jadehawk's work, and PaperMono uses the FreeInk RTC/PMIC work. SDK verification
reuses #65. Original licenses and notices are included. AI assistance was used
for code, tests and documentation.

## Compatibility checkpoint — 10 November 2026

This packet carries the existing W06/TIMED code onto CP `36bd50d0` and its SDK
pin `6a208c0c`. It retains upstream MFL and bounded CSP parsing; it adds host
coverage rather than another production transport. The host helper enables
HAVE_MAX_FRAGMENT, matching the firmware flag. TLS 1.2 tests observe negotiated
2 KiB records and a peer ignoring MFL that sends full-size records. TLS 1.3 MFL
negotiation and constrained device heap are not measured by those cases.

Home thumbnail generation can still paint progress popups on a cache miss;
the upstream Home change is not a general single-refresh guarantee. TIMED
host painting checks do not qualify Home on the physical panel. Earlier
PaperMono acceptance belongs to its exact prior image, not to this revision.

## Security compatibility checkpoint

This revision retains upstream WebDAV credential-path guards and complete
PageLink href initialization. No additional production fix was required when
applying the existing W06/TIMED series. From W06 or TIMED, run:

```sh
python3 test/webdav_guard/run.py
```

The focused host fixture extracts the production path and PROPFIND methods,
with a fake URL decoder and storage. It is not a full HTTP/FAT or device test.
The built-in credential-store policy is not a blanket policy for every plugin
file; visible plugin roots need their own access contract. PageLink construction
does not scrub bytes already stored by an older firmware.
