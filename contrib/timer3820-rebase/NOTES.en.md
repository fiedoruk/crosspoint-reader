# Review facts for PR #3820

- Original implementation: Michael Kazakov (@kivarun), commit `46a7e3968c73a918e29a7615191c016fdfcdbf05`.
- Comparison base: `6d2cd3a1c16cb9bdff5a52f6ec657d24f401b0a8` on CrossPoint `develop`.
- The cherry-pick conflicts only at `HalPowerManager::startDeepSleep`. The adaptation retains the EEGO A4 frontlight/touch shutdown and adds the original timer parameter. Current power-rail, PMIC and Metalio shutdown paths remain intact.
- The optional timer defaults to zero. All three current callers omit the argument, so this patch does not enable timed wake in normal use. Timer boots follow normal startup; no download, background refresh, scheduler or rearm is added.
- The classifier requires both an ESP deep-sleep reset and timer wake cause. Timer wakes remain in the display resync path. The classifier is tested without an ESP device; firmware assertions check the IDF values.
- Four original host tests pass. A separate ASan/UBSan comparison against the actual pinned pre-change classifier checks 1,024 input combinations: only the four timer/deep-sleep combinations change.
- Four independent AI-assisted review axes covered correctness, architecture, embedded constraints and i18n/docs. A misleading cross-board timer comment was corrected; no runtime change was needed after review.
- `esp_sleep_enable_timer_wakeup()` still has no checked return, as in the original PR. No existing caller supplies a nonzero interval. A future caller needs an accepted interval and explicit failure policy; this adaptation does not promise successful arming for arbitrary values.
- Timer wake requires the ESP to stay powered. Battery-latch shutdown, the PaperMono PMIC and Metalio power-off may remove that power. Device wake, display state and energy have not been measured for this adaptation.

The original author retains ownership of PR #3820. These are factual handoff notes, not a new PR description. The adaptation and checks used AI assistance. Human review, maintenance ownership and hardware acceptance remain outstanding; maintainer acceptance is not implied.
