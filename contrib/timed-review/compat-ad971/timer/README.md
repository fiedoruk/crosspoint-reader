# Timer #3820 on develop ad971c8a

This is rebase support for Michael Kazakov/kivarun's timer PR #3820 at `1bc4975`.
It preserves the author's one-shot timer, arm-failure handling, C3 latch policy
and wake classifier, while keeping the new upstream SDK/HAL and Picco paths.
It is not a competing timer PR or a refresh consumer.

The merge conflicts are in `HalPowerManager.cpp` and `.h`. Both branches added
an argument in the second position. Current develop uses that position for
`wakeOnHeldButton`; the timer branch used it for a microsecond interval. The
resolution preserves the existing boolean argument and appends the duration:

```cpp
startDeepSleep(gpio);                       // ordinary button-only sleep
startDeepSleep(gpio, true);                 // preserve upstream held-button wake
startDeepSleep(gpio, false, timerWakeUs);    // explicit timer request
```

This prevents the existing `true` argument from becoming a one-microsecond
timer request. Picco's USB charging hold, frontlight/touch teardown and normal
wake path remain in place. The timer requests still happen before teardown.
The usefulness of an idle-screen consumer depends on this shared primitive
preserving ordinary reading and wake behavior first.

## Reproduce and review

Requires Git and Python 3. Use a new destination:

```sh
python3 replay.py /path/to/timer-checkout
```

The script checks out public CP `ad971c8a` and its SDK `25cd36c7`, applies the
one patch and checks both result trees. Full refs and hashes are in the
manifest. `--cp-source` and `--sdk-source` may point to local mirrors. It does
not build, commit, flash or publish. There is no SDK adaptation in this packet.

The result is a reference for updating the original author's branch. Keep its
history and authorship; do not replace it with a separately authored timer PR.
The two conflicted HAL files and the two adapted timer test files are the
manual reconciliation scope. The other timer files are the existing PR changes
merged with current develop. Do not apply the whole patch on top of an already
merged timer implementation.

The production sleep-function harness now covers the existing held-button call,
explicit timer requests, arm/disable errors, EXT1 and the Picco frontlight/touch
order. Run it in the resulting checkout:

```sh
python3 test/timer_wake_arm/run.py
```

See VALIDATION.md for the actual build and test results. Host boundaries do not
qualify physical buttons, power consumption or a new device. A disabled timer
preserves the primitive's existing zero-default contract; the separate TIMED
consumer manages its own arming/cancellation policy.

CrossPoint and SDK licenses/notices are included unchanged. Code adaptation,
tests and notes were developed with AI assistance. Publication and upstream
acceptance remain separate from this pinned local result.

## Four-commit compatibility update

The patch bytes are unchanged from the preceding CP261726f6 checkpoint.
This replay includes the upstream home-cover fix, out-of-line ActivityManager
constructor/destructor, width-based Wi-Fi SSID truncation and tilt-setting
persistence fix. Applying the upstream delta before or after the support
series gives the same tree. VALIDATION.md separates this source result from
host, firmware and device evidence.
