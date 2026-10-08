# Timer-arm error handling for PR #3820

This four-file patch applies to the author's `3678609ff49a6a082c5181f1366ebf14038a836c`
head. It handles a rejected `esp_sleep_enable_timer_wakeup()` call before serial
and board teardown, without changing the existing board power policy or callers.

A nonzero interval is armed before teardown. On rejection, the existing logger
records the error and the timer source is disabled. Successful cleanup or an
already-inactive source continues through the existing button sleep path. An
unexpected cleanup error restarts before peripherals are shut down. Zero skips
these new operations. Builds that omit logging do not gain persistent diagnostics.

The patch does not change GPIO13 battery cutoff, add a scheduler, or incorporate
the downstream timed panel caller. It does not establish timer wake on C3 battery
power. Original timer authorship remains with Michael Kazakov (@kivarun).

## Reproduce the host checks

Use a new directory, Git, Python3 and a C++20 compiler supporting AddressSanitizer
and UndefinedBehaviorSanitizer. Inspect the patch before applying it.

```sh
mkdir timer-arm-review
cd timer-arm-review
git init
git fetch --depth=1 https://github.com/crosspoint-reader/crosspoint-reader.git 3678609ff49a6a082c5181f1366ebf14038a836c
git checkout --detach FETCH_HEAD
git apply --check /path/to/timer-arm-error.patch
git apply /path/to/timer-arm-error.patch
python3 test/timer_wake_arm/run.py --negative-control
```

The runner extracts the actual `startDeepSleep` function and compiles it with
controlled IDF/board boundaries. Five cases run for each of the two EXT1 macro
values: zero, successful arm, rejected arm, already-inactive cleanup, and failed
cleanup. The original head must fail the rejected-arm regression case. It does
not run on a reader or simulate all board-specific branches. The extraction
uses the following `getBatteryPercentage()` function as its end marker; moving
that code requires updating the test. Temporary compiled files are removed.

The test is also registered as `TimerWakeArm` in the existing CMake/CTest suite.
Configuring that entire suite requires its normal dependencies, including the
pinned SDK and GoogleTest; the direct command above does not fetch them.

See `VALIDATION.en.md` for measured checks and limitations. `LICENSE-CP` retains
the upstream MIT terms for CP-derived code and the accompanying test material.
AI tools assisted the scoped implementation, tests, review and factual notes.

## Separate hardware handoff

After explicit device approval, identify one X4 Pro and retain its data/recovery
path. Check ordinary zero-interval sleep and Power wake, then one valid timer
request through a reviewed temporary test caller. Confirm book/settings retention.
For a controlled IDF rejection, verify that the diagnostic occurs before serial
teardown and that the button still wakes the reader. Unexpected timer-clear
failure is covered by host fault injection; it is not a routine device procedure.
These checks have not been performed for this patch. A source package does not
authorize a test installation or certify C3 battery wake.
