# PR #3820: minimal adaptation to current develop

This source-only package helps the existing optional timer-wake PR. It is not firmware to install and does not contain a background delivery caller.

Use a separate clean checkout. Inspect `source-refs.json`, `NOTES.en.md` and the patch first. Commands below do not create a commit, push, or install anything.

```sh
git clone https://github.com/crosspoint-reader/crosspoint-reader.git crosspoint-timer-review
cd crosspoint-timer-review
git checkout --detach 6d2cd3a1c16cb9bdff5a52f6ec657d24f401b0a8
git submodule update --init freeink-sdk
git apply --check /path/to/timer-3820-rebased.patch
git apply /path/to/timer-3820-rebased.patch
cmake -S test -B build/timer-review
cmake --build build/timer-review --target WakeupClassifyTest -j2
./build/timer-review/wakeup_classify/WakeupClassifyTest
python3 /path/to/verify-classifier.py .
```

Host prerequisites: Git, Python3, CMake, a C++20 compiler with ASan/UBSan, and GoogleTest v1.17.0 (CMake can fetch it). To reuse a local checkout of GoogleTest, pass `-DFETCHCONTENT_SOURCE_DIR_GOOGLETEST=/path/to/googletest` when configuring CMake. SDK revision is pinned by the CP gitlink. No SDK #65 adaptation is required for this timer-only patch.

`verify-classifier.py` reads the actual baseline policy with `git show`, compiles it alongside the patched classifier and compares all inputs in a bounded table. Temporary files are removed when it exits. It does not test HAL GPIO, timer arming, PMIC or panel hardware.

Keep the original implementation attributed to Michael Kazakov (@kivarun). If an adapted commit is made by another person, retain his Git authorship or add his original `Co-authored-by` identity from `source-refs.json`. Do not attribute the original timer implementation to the adaptation author. `UPSTREAM-LICENSE.txt` preserves CrossPoint's license; repository history carries the original contribution.

Before any hardware work, agree on one exact device and retain its current data and firmware recovery path. See `HARDWARE.en.md`; no test installation is authorized by this package.
