@kivarun, the conflict-resolution packet now replays on develop `ad971c8a`.
It keeps the four intervening upstream fixes, including tilt-setting persistence;
the timer patch itself did not need another change.

The resolution still preserves `startDeepSleep(gpio, true)` as held-button wake
and puts the timer interval third. Your arming/cleanup, C3 latch and classifier
remain intact. This is material for updating your existing branch with its
history and authorship preserved, not a separate timer PR.

The packet includes the pinned replay and scoped validation. The full companion
integration gets a C3 compile/link check; this is not a new standalone-timer
firmware or hardware result. Our idle-screen work needs a shared wake primitive
that leaves ordinary reading and charging intact.
