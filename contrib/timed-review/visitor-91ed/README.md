# Settings visitor checkpoint — 19 October 2026

- [Timer reference](timer/README.md) and [archive](timer/timer-3820-rebase-support.zip).
- [W06/TIMED series](g11/README.md) and [archive](g11/g11-visitor-compatibility-support.zip).

These immutable packets are the completed CP `91ed3ef8` / SDK `f9cc1bed`
checkpoint. The TIMED entries now use upstream's settings visitor and StaticEnum,
with the same keys, values and model exclusions. Eight selected Release CTests,
fresh replay and one full integration C3 build passed. The individual validation
files separate those results from hardware and older TLS evidence.

## New timer head observed before publication

PR #3820 now has head `e926eac8`, rebased by its author onto `91ed3ef8`. It uses
`startDeepSleep(gpio, timerWakeUs, wakeOnHeldButton)`, and its ordinary sleep
caller passes `(gpio, 0, wakeOnHeldButton)`. Our frozen checkpoint still has the
earlier held-button-first order. Its timer packet is retained as a dated test
and integration reference, not a patch to apply over the author's new branch.
The next consumer update should follow the author's current argument order.
No new APPROVE or hardware qualification of `e926eac8` is implied.

Develop also advanced to `0fcdb3ec`, which changes hidden-file deletion in the
web UI and its documentation. SDK remains `f9cc1bed`. The inspected change does
not overlap this visitor/timer/transport adaptation, but the recorded build
remains tied to `91ed3ef8`; it is not a build of the later commit.

The aim is a shared timer and authenticated transport for SD plugins while
ordinary reading remains intact. Timer authorship stays with kivarun; the
consumer, SDK/API decision, C3 runtime evidence and release gates stay separate.
No firmware, private service or test-device controller is distributed here.
