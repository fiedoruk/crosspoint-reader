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
  build and device evidence. The packaged sources match the recorded Sticky
  build; this update adds no firmware build or new device qualification.

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
