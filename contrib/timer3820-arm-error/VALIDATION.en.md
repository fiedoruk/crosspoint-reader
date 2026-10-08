# Validation facts

Base: PR #3820 at `3678609ff49a6a082c5181f1366ebf14038a836c`.
Unmodified SDK: `425d200a8ea447326b4b9696e4e47dc84ad9d7f6`.

- Five scenarios passed under each of the two EXT1 macro settings with ASan/UBSan:
  zero, successful arm, rejected arm, inactive cleanup and failed cleanup.
- The original function failed the rejected-arm regression under both settings,
  as expected. The harness uses the production function with controlled hardware
  boundaries; it does not claim complete board or IDF implementation coverage.
- CMake/CTest discovers and passes `TimerWakeArm` (3.231 seconds including configure).
- A fresh public-source checkout applied the patch, matched all four result files,
  and passed candidate and negative-control checks in 7.814 seconds.
- Four independent read-only review axes completed: correctness, architecture,
  embedded constraints and i18n/docs. The test output wording was narrowed to its
  actual EXT1 coverage. The main reviewer checked the complete diff and notes.
- The repository formatter and `git diff --check` passed.
- One X4 Pro build passed in 88.757 seconds, with two jobs, nice 10 and the existing
  cache. No retry or clean build. All 902 CP and 890 SDK tracked source hashes
  remained unchanged; all 20 SDK links resolved inside this checkout.
- Linker figures: static RAM 103,328 / 327,680 bytes; flash 5,826,074 / 6,553,600
  bytes. These are not runtime heap or a measured footprint delta.

Not performed: device tests, real invalid-duration injection on ESP, power or
battery measurements, a firmware matrix, public CI, maintainer acceptance or
release. C3 battery cutoff remains unchanged. Error logging follows the existing
build configuration; slim builds do not gain a persistent diagnostic. A human
hardware/maintenance handoff remains necessary before a new PR under current CP
rules. This package supports the existing author's PR and opens no new one.
