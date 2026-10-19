# Timer #3820 on CP 91ed / SDK f9

This is rebase support for Michael Kazakov/kivarun's timer PR at `1bc4975`,
pinned to CP `91ed3ef8` and the official SDK `f9cc1bed`. The timer runtime and prior
HAL conflict resolution are retained. Only the CMake registration context was
refreshed, keeping the upstream recursive-dictionary test.

The held-button argument stays second and the explicit interval third:

```cpp
startDeepSleep(gpio);
startDeepSleep(gpio, true);
startDeepSleep(gpio, false, timerWakeUs);
```

This keeps existing held-button wake separate from the timer interval. Original
arming, cleanup, C3 latch and wake classification are preserved. No consumer
or SDK verification patch is included in this standalone packet.

## Replay and checks

With Git and Python 3, use a new directory:

```sh
python3 replay.py /path/to/timer-checkout
cd /path/to/timer-checkout
python3 test/timer_wake_arm/run.py
```

The public refs, patch hashes and expected trees are in manifest.json.
Optional local mirrors use --cp-source and --sdk-source. Replay never builds,
flashes, commits, pushes or starts CI. Do not apply this aggregate patch on top
of an already merged timer implementation; use it as a reference for updating
the original author's branch while preserving its history.

VALIDATION.md separates SOURCE/HOST from firmware and device evidence. Our
idle-screen work needs one shared wake primitive that preserves normal reading
and charging. The full W06/TIMED consumer is a separate review scope.

CP/SDK licenses and notices are retained. AI assistance was used for adaptation,
tests and documentation. No firmware or private service implementation is shipped.
