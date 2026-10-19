# Current TIMED consumer: bool-second timer API

The [timer-669 packet](timer-669/README.md) follows the author's `669642d2`
contract on CP `0fcdb3ec` / SDK `f9cc1bed`: held-button second, interval third.
The newer author head `a38095cf` has an identical source tree. The consumer
keeps its existing fourth recovery argument and the argument-regression checks.

Eight selected CTests, TIMED host checks, one full C3 build and fresh W06/TIMED
replays passed. [Validation](timer-669/VALIDATION.md) distinguishes those results
from hardware, C3 runtime heap and earlier TLS evidence. This is dependent
integration support, not an official firmware release or a new timer PR.

Earlier checkpoints remain below with their original refs and evidence.

---

## Settings visitor checkpoint — 19 October 2026

The [latest published checkpoint](visitor-91ed/README.md) contains the timer
reference and W06/TIMED series on CP `91ed3ef8` / SDK `f9cc1bed`. It completes
the settings-visitor and CMake adaptation, with scoped host/replay evidence
and one full C3 build.

The author has since rebased #3820 to `e926eac8` with timer interval second
and held-button flag third. The frozen checkpoint uses the previous order;
consumer alignment is the next step. The compatibility note records that
difference and the later web-UI-only develop commit `0fcdb3ec`.

---

## Timer/W06/TIMED compatibility reference — 19 October 2026

The [current reference](compat-ad971/README.md) contains separate timer and
W06/TIMED packets pinned to CP `ad971c8a` / SDK `25cd36c7`. Their validation
includes targeted host checks, fresh replay and one full integration C3 build.
Newer develop `91ed3ef8` / SDK `f9cc1bed` needs a test-registration refresh and
TIMED settings visitor adaptation; that newer base is not build-qualified here.
Earlier checkpoints below keep their original evidence and limits.

---

## Separate W06 and TIMED review scopes — 19 October 2026

The [current source packet](g11-final/README.md) separates verified plugin events
from their timed consumer. It replays W06 on its own, then adds the existing
upstream timer and TIMED. [Validation](g11-final/VALIDATION.md),
[W06 scope](g11-final/pr-w06.en.md), [TIMED scope](g11-final/pr-timed.en.md)
and the [ZIP](g11-final/g11-final-review.zip) are included.

This packet is pinned to CP `b64d797c` and SDK `084fdfb` with its explicit
verification adaptation. Develop has since advanced to `261726f6` with BOOX
Picco and shared SDK/HAL changes; that newer base is not qualified by this packet.
SDK/API acceptance, C3 runtime evidence and the consumer's scope remain open.
Earlier packages below retain their original evidence and limitations.

---

# Verified downloads and timed sleep-screen integration

The [current compatibility package](t4a/README.md) reconstructs the existing
W06/TIMED integration on timer PR #3820 at `1bc4975`. It preserves the new
upstream settings/font fixes and moves the Source/interval definitions to the
shared settings list. The timer, transport and Power behavior stay unchanged.

- [Source ZIP](t4a/t4a-support.zip), pinned refs and replay instructions are included.
- Classifier comparison, settings host checks and one Sticky build passed.
- This revision has not been tested on a device. The earlier T3 hardware
  observations remain tied to its previous binary.

The SDK verification and combined source-selection contracts still need upstream
agreement. This is dependent review material; no firmware is distributed here.

<details>
<summary>Previous packages and device evidence</summary>

# Verified downloads and timed sleep-screen integration

Updated 18 October 2026. The [T3 review package](t3/README.md) separates verified
event downloads (W06) from the shared Off/Local/Plugin timer consumer. It includes
pinned public prerequisites, replay commands and [validation notes](t3/NOTES.en.md).

- [Download the T3 source package](t3/t3-support.zip).
- Replay W06 alone with `--through w06`, or the whole integration with the default.
- The recorded neutral Sticky image passed online/Local/Off cases, physical
  Power during a paced response and two functional battery cycles.

CP `7a76e124` and SDK `084fdfb2` are the tested bases. Accepted SDK/source-selection
contracts and compatible upstream refs are still needed for separate CP PRs.
The current timer PR remains independently reviewable. No firmware is distributed here.

<details>
<summary>Previous review packages and device notes</summary>

# SD-configured timer image consumer

Updated 12 October 2026. The complete consumer is available in the
[current review package](current/README.md), separately from its prerequisites.

- Start with [07-timed-panel.patch](current/patches/07-timed-panel.patch):
  timer selection, verified image delivery, native decode/commit/transfer,
  Power handling, rearm, PaperMono integration and the early permission read.
- [Series and public refs](current/series.json) identify the six dependency
  layers. The base is installer PR #3877 at `fc3aed12`, with SDK `1a5448df`.
- [Download the complete package](GH06-full-timed-review.zip), extract it and
  run `python3 replay.py /absolute/path/to/new-empty-receiver` from the extracted
  directory. [Requirements and commands](current/README.md#reproduce).
- [Validation and remaining limits](current/VALIDATION.md) distinguish host,
  build and device evidence from the source-packaging snapshot.
- [Sticky device results — 12 October](device/STICKY-2026-10-12.md) qualify the
  exact neutral binary on one unit: USB and battery refresh, failure retention,
  certificate rejection and return to the same book position. The source series
  and its packaged files are unchanged; other device and release gates remain.

This remains dependent source-review material, not a merge-ready patch against
raw develop. SDK verification and dependency integration need accepted refs.
The timer remains Michael Kazakov / @kivarun's work, the installer @jadehawk's,
and SDK verification builds on @sfoulad's changes. This does not ask to fold
the consumer into the timer primitive. AI tools assisted code, tests and notes.

## Earlier snapshot

The top-level `W06.diff`, `TIMED.diff`, `PAPERMONO.diff`, `SDK-PAPERMONO.diff`,
`DEVICE-NOTES.en.md` and `source-review.zip` are retained as historical material.
Do not combine that older series with `current/`. Its original README and
artifact set remain available in the [11 October snapshot](https://github.com/fiedoruk/crosspoint-reader/tree/9b33c55d2273108a3e46786d4fe6e893fec9f431/contrib/timed-review).
The SDK RTC/PMIC changes from that snapshot are already in the current SDK base.

The [standalone PaperMono timer adapter](../papermono-timer-adapter/README.md)
remains separate support for PR #3820; this update leaves those files unchanged.

</details>

</details>
