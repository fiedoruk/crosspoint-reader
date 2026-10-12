# PaperMono adapter for the existing timer primitive

Base: CrossPoint PR [#3820](https://github.com/crosspoint-reader/crosspoint-reader/pull/3820),
head `c3568c7abaaedb427f35421e73a712ac77fcc996` by Michael Kazakov (@kivarun).
SDK prerequisite: official PR #138 merge `1a5448dfa705d6499fbff20371539bf553865dd2`.
The original PR's SDK pin is `425d200a`; this package explicitly advances it.
That range includes other official SDK changes (38 commits, 143 changed paths),
not only the RTC change. This is a scoped adapter qualification, not a complete
SDK audit or a clean patch against current CrossPoint develop.

The adapter is extracted from the previously shared PaperMono support. It uses
RX8130 and PMIC GPIO0, consumes the boot evidence once, and prevents a returned
PMIC shutdown from falling into ESP-only sleep without a Power wake source.
It keeps the optional timer API and zero default. It adds no network consumer,
schedule setting or Power-input capture; the reader still boots normally on Timer.

## Reproduce

On macOS or Linux with Git, Python 3, CMake and a C++20 compiler supporting
ASan/UBSan, run in a new directory:

```sh
python3 replay.py /absolute/path/to/new-papermono-receiver
```

The script fetches public exact refs, applies the patch including its SDK gitlink,
checks out that SDK revision, and runs the real HAL/SDK host cases, the original
negative control and ESP regressions. It also verifies the registered CTest entry.
It performs no firmware build, flash, CI request or network request from a reader.

## Recorded checks and limits

The local PaperMono firmware build passed with two jobs. Host checks cover 13
wake/reset cases, six shutdown paths, arm/cancel/rollback and SDK duration limits.
The original PR lacks RTC classification and returns the expected negative result.
The recording bus simulates I2C, and shutdown tests simulate removal of power.
A fresh physical PaperMono run was not performed for this binary. Before merging
this board behavior, verify battery RTC wake, zero after an armed timer, the
shortest supported interval, the next normal Power boot and returned shutdown on USB.

The material is intended for the existing timer author. It is not a competing
timer implementation or a claim that the full timed network consumer has landed.
MIT notice retained from CrossPoint. No private service or firmware binary is included.
