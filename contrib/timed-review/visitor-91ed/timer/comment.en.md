@kivarun, this reference now replays your `1bc4975` timer on CP `91ed3ef8` and the
pinned SDK `f9cc1bed`. It retains the previous timer/HAL behavior and refreshes the
CMake test-registration context without dropping the newer upstream test.

The held-button flag remains second and the interval third. This is support
for updating your existing branch with its history intact, not a separate
timer implementation. The packet records replay and host evidence; the full
companion integration has its own build result and SDK adaptation.

Our idle-screen work relies on this shared primitive while ordinary reading
and charging remain intact. Device and upstream acceptance gates stay separate.
