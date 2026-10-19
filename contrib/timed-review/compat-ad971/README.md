# Timer, W06 and TIMED compatibility reference — 19 October 2026

- [Timer support for the existing #3820](timer/README.md), with its
  [source archive](timer/timer-3820-rebase-support.zip).
- [W06 and TIMED review series](g11/README.md), with its
  [source archive](g11/g11-sdk25-compatibility-support.zip).

These frozen packets replay CP `ad971c8a` and SDK `25cd36c7`. All patch bytes
are unchanged from the preceding CP261 compatibility checkpoint. Four upstream
fixes are preserved; targeted host checks, fresh replay and one full integration
C3 build passed. The standalone timer has source/host evidence on this base,
not a separate new firmware build. Each packet states its exact limits.

## Current develop is ahead of this checkpoint

The publication check observed CP `91ed3ef8` and SDK `f9cc1bed`. Direct patch
application now needs a `test/CMakeLists.txt` context refresh. With that file
excluded for diagnosis, the timer and W06 patches apply; TIMED additionally
needs its settings entries ported to the `forEachBaseSetting` visitor introduced
by #4085. The SDK verification patch applies to `f9cc1bed`, but this is a source
check only. The remaining newer changes include book/dictionary/clipping work
and Picco display/input support. None is covered by the older build result.

Use the pinned replay commands for this reference. Do not treat these archives
as ready-to-apply patches against current develop, or as tested firmware for the
new SDK. The forward port must preserve the new settings memory behavior.

The goal is shared authenticated delivery and a single timer owner for SD
plugins, while ordinary reading remains intact. The timer stays with its
original author; the consumer remains separate. SDK API/ref agreement, C3
runtime measurements, consumer scope and required device acceptance are open.
No firmware, private service or device-test controller is distributed here.
