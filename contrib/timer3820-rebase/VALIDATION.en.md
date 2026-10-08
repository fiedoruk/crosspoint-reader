# Validation receipt

Patch SHA256: `3488ffdee82ca717e70e53978167864322fd03ecff95874f745a919e165f33b2`.

- CrossPoint base: `6d2cd3a1c16cb9bdff5a52f6ec657d24f401b0a8`; unmodified SDK: `425d200a8ea447326b4b9696e4e47dc84ad9d7f6`.
- Original `WakeupClassifyTest`: 4 tests passed. Separate ASan/UBSan baseline comparison: 1,024 combinations passed, only 4 intended timer cases differ.
- Repository `./bin/clang-format-fix -g` and `git diff --check HEAD`: passed.
- X4 Pro build: `pio run -e x4pro -j2`, one attempt, passed after final source edits. Wall time 129.223 s, user CPU 168.35 s, system CPU 38.78 s, peak process RSS 798,408,704 bytes. Existing cache reused; no clean build or full target matrix.
- Build output: static RAM 103,328 / 327,680 bytes; flash 5,825,582 / 6,553,600 bytes. These are linker figures for this target, not runtime heap or a comparison against baseline.
- 900 CP and 890 SDK source hashes were unchanged during the build. All 20 dependency links resolved inside this checkout's pinned SDK. Local configuration was absent before and after the build.
- Four read-only review axes completed. One comment clarification was applied and rechecked. No new heap allocation, task or framebuffer was introduced by this diff.

Not performed: device tests, battery/current measurements, EEGO/PaperMono/other-board builds, full host suite, public CI, maintainer scope acceptance, release acceptance. Current-develop board preparation was preserved by source comparison; an X4 Pro build does not validate EEGO hardware. The original author's tests on the old PR head are separate evidence and are not counted here.

Fresh recipient replay from cached public pinned Git objects: patch check/apply, four original tests and 1,024-case comparison passed in 6.355 s. All ten patched files match the reviewed checkout byte-for-byte. No recipient firmware rebuild was needed.
