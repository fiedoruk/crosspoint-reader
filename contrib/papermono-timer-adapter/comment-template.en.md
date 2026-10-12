I isolated the PaperMono HAL portion on your current `c3568c7` head: ARTIFACT_URL.

It uses the RTC/PMIC APIs merged in FreeInk SDK #138. The SDK prerequisite is explicit in the patch. The adapter arms and cancels the board wake route, recognises a qualified RTC cold boot, and avoids falling into ESP-only sleep if PMIC shutdown returns. It keeps your optional timer API and zero default; there is no timed network consumer or Power-input capture in this delta.

The PaperMono build passes. Host tests cover 13 wake/reset cases and six shutdown paths, plus RTC error/rollback cases and the existing ESP timer regressions. The script replays the patch from public refs. These tests simulate the bus and power removal; this binary still needs a fresh PaperMono device check.

Your timer remains the base of this work. AI assistance was used for the adapter, tests and review.
