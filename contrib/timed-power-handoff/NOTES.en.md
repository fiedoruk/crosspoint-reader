# T1 — retain Power during timed sleep-screen refresh

A Power press can finish while the timer branch is rendering a wallpaper. The
original path returns to sleep and can consume the press while waiting for release.
This patch retains Power edges during maintenance, including the existing 10 ms
stability result, and resumes through the ordinary boot path after a software restart.
The current panel transfer may finish before the reader resumes.

The purpose is to keep a reader usable between reading sessions: an optional
background refresh must yield when its owner asks to read. The patch preserves
local wallpaper rotation and the board-specific X3 SD-rail handling; it adds no
network client, scheduler, plugin capability or PaperMono timer support.

Base: Razor-Crest timedwake-r1, `59555361aef55608cc56fdb5a9fccc167c37db34`.
SDK: `7fcd3b34c108f28c086ade3b433924022dbc0998`, unchanged.

## Validation

- The actual unpatched timer branch reproduces the lost press (expected exit 42).
- The patched branch and handoff pass ASan/UBSan checks for Power before/during
  rendering and at display/storage/sleep boundaries, one-shot reset stamps,
  short-press preferences and disabled/interrupted cycles.
- Production HAL capture methods pass controlled GPIO tests for both polarities,
  released/held contacts, delayed release, coalesced edges, timestamp wrap, setup
  failures and a timer callback left pending after cleanup.
- The production sleep function passes arm/cleanup and rail checks with and
  without EXT1, including Power during teardown, Power-wake arming and explicit zero-interval cleanup.
- Four independent review axes are complete. The Sticky build passed with the
  pinned SDK unchanged; capture and timer ISR calls were checked in the ELF.
- On one USB-powered reTerminal Sticky, a real Power press during a timed
  refresh produced the software handoff and returned to the same book position
  (page 1/6, 2%). The reader remained awake after release. Ordinary held-Power
  wake also passed. The configured short-press preference was Ignore.
- This does not qualify battery-only behavior, both short-press preferences,
  all orientations, other boards or the final SDK sleep-entry timing window.
  The device procedure is in `docs/timed-wake-testing.md`.

The existing main wake path checks Power stability for 10 ms; this is distinct
from the longer press used to put an awake reader to sleep. A press verified while still held
remains retained after release. A shorter contact still follows the
saved Short Power Button Press preference. This is not a guarantee that arbitrarily
short electrical pulses can be timed while interrupts are masked.

The change uses fixed HAL state, one RTC handoff word and one static verification
timer on the existing FreeRTOS timer daemon. It samples a still-held contact
during blocking I/O; a delayed release alone cannot verify its duration. Registering the shared
GPIO ISR service can allocate SDK-owned storage; failure disables periodic refresh.
No second framebuffer or new task is added. Static resource deltas, timer-task stack high-water and device energy have not
been measured. Internal free heap after reader resume was 242,644 bytes, with
a largest block of 188,404 bytes; these are observations, not a baseline delta. Snapshot/app state is not written by the handoff.

AI assistance was used for implementation, tests and review.

A final capture check follows Power-wake arming. Pulses completed wholly inside
the subsequent SDK sleep-entry operation remain an unqualified timing boundary.
