# Hardware acceptance still required

The current CrossPoint firmware-handoff requires human review of the diff, understanding of its behavior/architecture and maintenance ownership. It also requires hardware testing before a new PR is opened. No such approval or result is recorded for this adaptation. This package supports the author's existing PR; it does not open a replacement PR.

1. Select one exact X4 Pro unit and record its firmware, power source and recovery/backup plan. Do not infer identity from an old USB port. The proposed first target has a retained power rail; it does not stand in for PaperMono or other boards.
2. With the unchanged zero/default path, verify sleep and power-button wake on USB and battery, short and held button behavior, saved book/progress, and normal display recovery. Check the four orientations when returning to reading. Watch for cold boots, unintended wake, backlight remaining on or a stuck screen.
3. The patch has no nonzero production caller. A timer demonstration therefore needs a separately reviewed temporary test caller or the author's existing harness. Record its exact diff; do not claim that ordinary installation alone activates the timer. Request a short valid interval once, release the button, verify timer wake classification, then test an earlier button wake. The current primitive resumes ordinary boot; it is not expected to preserve a background screen and re-sleep.
4. Compare repeated zero-path sleep/wake and the temporary one-shot path for battery current, temperature, runtime heap and panel behavior. No numeric energy or runtime heap result is available yet. No claim of unchanged energy follows from a successful build.
5. PaperMono PMIC/BOD and boards that cut ESP power need their own power-topology evidence. Do not disable brownout protection or bypass shutdown as part of this rebase.

A failure to wake, unexpected power-off, reset loop, abnormal current or display corruption blocks a device-ready claim. Remove any temporary test caller from the final contribution and keep its results tied to the tested source hashes. Device tests and installation require a separate explicit scope from the owner.
