The W06/TIMED support now replays on CP `ad971c8a` and SDK `25cd36c7`.
All firmware and SDK patch bytes are unchanged from the preceding CP261 checkpoint;
the four new upstream fixes are preserved. W06 and TIMED remain separate patches
and replay stops.

The targeted checks cover settings and boot integration; the full C3 build checks
the new ActivityManager linkage as well. Exact results and the limits of reused
older evidence are in VALIDATION.md. SDK #65 API/ref acceptance, physical C3
memory measurements and consumer scope still need their own decisions.

We want the same reader to remain useful on a desk between reading sessions,
without separate schedulers or transport code in every SD plugin. Keeping this
series small and compatible with ordinary reader updates helps that path.
