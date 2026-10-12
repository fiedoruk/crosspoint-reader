# SD-configured timer image consumer

Start review with [07-timed-panel.patch](patches/07-timed-panel.patch). It contains
the complete consumer, PaperMono HAL integration and early plugin-permission
bootstrap. The other six patches are explicitly identified prerequisites, not
additional new contributions in this submission. The series reconstructs the
already tested candidate; splitting it did not change firmware source.

A qualified timer wake selects one opted-in SD handler, joins saved Wi-Fi,
obtains fresh clock evidence, fetches a verified native-size BMP, validates and
decodes it, replaces the last-good file, transfers the frame and rearms sleep.
Power takes priority. The normal reader path keeps its book state and outbox.
Failed network, auth or decode work preserves the previous file and performs no
new panel transfer. Timed wake requires sufficient battery and a qualified handler.

## Review boundaries

| Patch | Role |
|---|---|
| 01 | Existing token-write recovery, CP #3956 |
| 02 | Existing checked BMP replacement, CP #3907 |
| 03 | Existing bounded event requests, CP #3908 |
| 04 | Existing compatible SDK #65 verification and proposed capability API |
| 05 | Existing verified-event transport (W06), adapted around the current installer |
| 06 | Existing timer primitive from Michael Kazakov / @kivarun, CP #3820 |
| 07 | Complete TIMED consumer and PaperMono/permission integration for review |

The base is the current installer PR #3877 head `fc3aed12`; the old W08 installer
patch is not applied over it. The SDK base is official `1a5448df`, which includes
the merged RTC/PMIC work from #138. The explicit SDK patch is still necessary for
verified requests; selecting the official base alone does not provide that contract.
The SDK checkout is pinned by the reproducer. A plain submodule update is not a
substitute for these explicit dependencies.

The primary patch has three runtime responsibilities: qualified event/preflight,
boot and Power/sleep ownership, and native image decode/commit/transfer. It also
adds the timer event label and host tests. The tiny trust-anchor preflight helper
reuses the existing CA loader. It introduces no second network or rendering stack.

## Reproduce

Run `python3 replay.py /absolute/path/to/new-empty-receiver` with Git, Python3 and
a C++20 compiler supporting ASan/UBSan. It fetches exact public CP/SDK/ArduinoJson
refs, applies all seven patches in order and checks the final source hashes.
It derives the original no-bootstrap preflight in a separate scratch directory,
checks that baseline hash, and runs permission checks including the negative
result, followed by clock, verified/bounded-event, TIMED and PaperMono host checks.
No firmware build, device operation, CI request or publication is started.

## Scope and limits

The early permission read validates a settings object capped at 16 KiB and assigns
only pluginsEnabled. Missing, malformed or unreadable input keeps timer work off.
The existing absent/null migration rule and discovery quarantine remain in force;
ordinary sleep uses the in-memory decision. This does not load general reader
preferences or resave them. The file limit is not a cap on total parser heap.

The renderer uses native portrait dimensions and BW projection. Saved Custom
orientation/grayscale, conditional 304 delivery and server-selected cadence are
not part of this minimal consumer. The latter two remain separate follow-ups.

Read [VALIDATION.md](VALIDATION.md) for exact evidence and unmeasured hardware
conditions. This is dependent source-review material on unmerged refs, not a
standalone merge-ready PR against raw develop or a product release.

The timer remains @kivarun's work, the installer remains @jadehawk's, and SDK
verification builds on @sfoulad's changes. Their source notices are retained.
AI tools assisted implementation, tests and documentation. No service code,
private templates, credentials or firmware binaries are included.
