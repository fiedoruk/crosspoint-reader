# Timed sleep-panel caller — dependent review series

This series connects the optional deep-sleep timer to the existing plugin
image-download path, then returns to sleep without loading reader state. It
is source material for review and scope coordination, not a released feature,
firmware distribution, or an SD package for an existing CrossPoint install.

The timer primitive remains the work in [PR #3820](https://github.com/crosspoint-reader/crosspoint-reader/pull/3820)
by @kivarun (kivarum). This caller is a downstream integration example; it is
not a request to expand that low-level PR. SDK/HAL scope and stock/fork
alternatives still need maintainer review before a separate CrossPoint PR.

## Reproduce from public sources

Requirements: Git, Python 3.9 or later, a C++20 compiler with AddressSanitizer
and UndefinedBehaviorSanitizer support, and HTTPS access to GitHub. The checked
host run used macOS and Apple Clang. Python packages and PlatformIO are not
required for these host checks.

From this directory:

```sh
python3 reproduce.py ../timed-review-check --test
```

Use a destination that does not exist. The script refuses an existing path,
fetches exact public commits, checks patch hashes, applies the series, verifies
result hashes and runs five host test groups. It does not read another local
checkout, install packages, build firmware, start CI, flash, or publish anything.
The resulting `reproduction.json` records the checks. Omit `--test` to inspect
the assembled sources without fetching ArduinoJson or compiling tests.

| Order | Patch | Role |
|---|---|---|
| 1 | `01-checked-bmp.diff` | Original runtime patch from [PR #3907](https://github.com/crosspoint-reader/crosspoint-reader/pull/3907), commit `db9a382c` |
| 2 | `02-bounded-events-after-bmp.diff` | [PR #3908](https://github.com/crosspoint-reader/crosspoint-reader/pull/3908), `f443af33`, adapted over checked BMP delivery |
| 3 | `03-verified-http-fresh-clock.diff` | Required, separately reviewable verified HTTP and fresh-clock caller |
| 4 | `04-timed-sleep-panel.diff` | Timer integration, panel transfer, rearm and manual wake handling |
| 5 | `05-sdk65-verification.diff` | Compatible SDK verification hunks, applied to the separate SDK checkout |

Start reviewing at patch 4. Patches 1–3 supply its required CP preimages;
the entire series is not presented as one new CP change. `series.json` pins
CP `43694c9018d26446ab30cce2fa65ee608355ae50`, SDK
`425d200a8ea447326b4b9696e4e47dc84ad9d7f6`, ArduinoJson 7.4.2 and every patch.
No inaccessible local base is needed. The later CI-only update to PR3907 is
not part of this runtime source series.

## Behavior and current boundaries

A qualifying timer wake snapshots one SD handler and grant, joins saved Wi-Fi,
requires a fresh clock callback, then fetches and validates a full-native BMP.
Clock wait, authentication and image retry share one cooperative attempt
budget. A checked file replacement and decoder success precede an explicit
panel transfer. Failure does not request a new transfer. Manual Power follows
the saved click/hold preference; a rejected tap re-arms the timer and returns
to standby after peripheral cleanup. The autonomous path does not drain reader
events or write book position, reading history or saved settings.

The proposed `sleep.timer` handler requires an integer `interval_seconds`
from 60 to 86400, HTTPS GET, explicit `tls.ca_file`, a read grant, `format:
"bmp"`, destination `/sleep.bmp`, and native dimensions. One timer owner is
allowed. Missing or invalid configuration disables the route. These bounds
are prototype policy, not an accepted cadence or battery-life promise.
The current panel path is Portrait/BW; full saved Custom preference parity
and other render modes have not been established.

**Verified requests remain disabled in an ordinary build of this series.**
`CROSSPOINT_SDK65_VERIFIED_PEER` is a provisional compile fence, not a public
SDK capability or an SD setting. The host suites exercise both the disabled
path and verified transport stubs. This package does not enable that fence
for firmware or include the private build qualification mechanism. An accepted
SDK contract must replace the provisional fence before product integration.
The two verification hunks alone are not a claim that the SDK API is accepted.

## Evidence and limitations

The fresh public-source reconstruction and all five host groups passed:
fresh time, verified HTTP/event trust, cooperative event budget, timer guard,
and timed fetch/Bitmap/paint/boot I/O. Sanitizers were enabled. These harnesses
execute production functions with controlled I/O boundaries, including an
extracted main boot caller; they do not execute the complete Arduino setup.
They cover two cycles, failures, shared deadlines, last-good file handling,
manual Power and rearm. Transport, Wi-Fi, SD and EPD boundaries are stubbed.
The older standalone checked-BMP runner belongs to its standalone PR base;
the integrated decoder/last-good checks here run through the timed suite.

The corresponding integration previously compiled for X4 Pro with verified
support qualified locally. That build passed after one targeted correction
for a missing event label. This series changes three C++ line comments in two
files relative to that runtime; no executable statements changed. Those new
source bytes have not been rebuilt as firmware. The fresh host run tests the
public series itself, not a copied result from that compile.

Separate [SDK65 support](https://github.com/Free-Ink/freeink-sdk/pull/65#issuecomment-6053836656)
contains real host TLS tests. Those results do not establish real MCU SNTP/TLS,
DNS/TCP hard cancellation, physical Power/pixel retention, energy, or C3 heap.
PaperMono is disabled pending PMIC/BOD evidence; Sticky is a source candidate,
and the prior compile was X4 Pro only. No device or release claim is made.

## Provenance and licensing

The timer and wake classification adapt PR3820 at
`46a7e3968c73a918e29a7615191c016fdfcdbf05`; credit remains with @kivarun.
SDK patch 5 adapts the CA-load and hostname checks by @sfoulad / Sameh Foulad
from [SDK PR #65](https://github.com/Free-Ink/freeink-sdk/pull/65).
The compatible patch was already published in the
[SDK support package](https://github.com/fiedoruk/freeink-sdk/tree/cddb06ee5ac6bd39bb577098b11dfbea3b9b7b39/contrib/sdk65-verification).
No second timer or TLS implementation is introduced.

`LICENSE-CP` covers CP-derived patches; `LICENSE-SDK` and `NOTICE-SDK` retain
the SDK terms. ArduinoJson is fetched separately with its own notices.
The newly written reconstruction script and documentation are offered under
the terms of `LICENSE-CP`. No service, renderer, template, account code or
firmware binary is included. AI tools assisted implementation, testing,
packaging and review.
