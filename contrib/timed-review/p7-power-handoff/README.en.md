# TIMED with upstream Power input handling

This dependent integration moves the existing W06/TIMED material onto CrossPoint
`0333cbbe` and SDK `4101b64c`. It preserves upstream's PowerButtonInput and
MappedInputManager behavior from #4435. It is not a standalone SD plugin or an
official firmware release. The timer and verification prerequisites remain unmerged.

No new production input handler is added. Normal Power wake verification now
initializes the GPIO path's debounced input even when TIMED has already verified the gesture.
The captured hold still permits wake if the button has since been released.
Previously that shortcut could leave the first foreground sample uninitialized.
The existing wake-release guard could then clear before the physical release.
The previous patches also require one
translation-context adjustment: the TIMED strings follow upstream's new controls
strings rather than replacing them. Existing P6 retry behavior is retained.

The additional host regression extends the upstream remote-input test. It executes
the actual main-loop wake-release and screenshot dispatch blocks with the real
MappedInputManager methods and PowerButtonInput. It checks that a consumed gesture
does not leave a delayed page, confirmation or sleep action. A negative control
removes only the wake-release reset and must fail the designated assertion.
Existing single/double-click tests remain in the same runner.
The timed_sync test separately checks that setup invokes normal Power wake
verification even after a verified capture, and still accepts that capture
after the button has been released. The PMIC shortcut remains unchanged.

This matters when picking up a reader after an automatic panel refresh: the gesture
used to resume reading must not also change the page or put the reader back to sleep.
The production input policy and its authorship remain upstream's.

## Reproduce

Use Python3, Git, a C++20 compiler with ASan/UBSan support and existing ArduinoJson 7.4.2 headers.
Run from this packet directory, with a destination that does not exist:

```sh
python3 replay.py /tmp/p7-cp
python3 /tmp/p7-cp/test/test_remote_button_input.py --sanitize
python3 /tmp/p7-cp/test/timed_wake_guard/run.py --sanitize
CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src python3 /tmp/p7-cp/test/timed_sync/run.py --sanitize
```

The intentional negative control is:

```sh
ulimit -c 0
python3 /tmp/p7-cp/test/test_remote_button_input.py --sanitize --negative-control
```

It must compile and fail with `wake release leaked`. An unrelated failure does
not validate the negative control. The mutant exists only in a temporary host
translation unit; production files are unchanged.

P5 remains a [separate test supplement](https://github.com/fiedoruk/crosspoint-reader/tree/cd3255bc53a02238dbae8b44e1c10905abb0707a/contrib/timed-review/p5-timed-busy-headers).
Run its `test/run.py`
with `--cp /tmp/p7-cp --arduinojson /path/to/ArduinoJson/src`.
P6's [immutable tests and instructions](https://github.com/fiedoruk/crosspoint-reader/tree/67bdb4bd64919cfcb82d9099697db5b60e382156/contrib/timed-review/p6-tls-retry) remain separate. P7 retains identical SecureClient sources;
the earlier real-wolfSSL test is not a new hardware measurement here.

## Evidence and remaining work

See VALIDATION.json for the exact executed checks and build result. Host GPIO,
clock, storage, Wi-Fi and panel boundaries do not establish physical Power,
PMIC timing, page restoration on glass, battery energy or C3 heap headroom.
The test executes a bounded section of main, not the complete Arduino main loop.
The selected SDK differs from CP's recorded gitlink deliberately; it is a
qualification dependency, not a proposal to silently update CP's pin.

Hardware acceptance requires an authorized reader: Power during a timed download
returns to the saved book position; releasing it causes no extra page or sleep;
fresh single/double clicks retain their configured behavior; with Sleep refresh
source set to Off, no refresh is armed.
Check applicable orientations/remappings and the PMIC path separately.

The timer remains kivarun's work; local refresh and RTC/PMIC contributions retain
their notices. SDK verification is based on #65, and P6 credits jpirnay's error
classification. Existing licenses/notices accompany the reused patches.
AI tools assisted integration, host tests and documentation.
