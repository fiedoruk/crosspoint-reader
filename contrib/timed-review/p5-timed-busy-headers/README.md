# TIMED busy-header cancellation and budget regression

This is a test-only supplement to the existing dependent W06/TIMED packet.
Production CP and SDK code are unchanged. It does not install a plugin, build
firmware or qualify a device.

## Reproduce from public prerequisites

Use Git, Python3, a C++20 compiler with ASan/UBSan, and existing ArduinoJson7.4.2
headers. Obtain the immutable P4 material, then assemble its future lane:

```sh
git clone --single-branch --branch support/timed-review-2026-10-09 https://github.com/fiedoruk/crosspoint-reader.git support
git -C support fetch origin f7dbdb3c673526b15b4732f2fa6e7849452dea29
git -C support checkout --detach f7dbdb3c673526b15b4732f2fa6e7849452dea29
python3 support/contrib/timed-review/cp2-b32-sdk-lanes/replay.py /tmp/p5-cp --lane future-qualification
python3 test/run.py --cp /tmp/p5-cp --arduinojson /path/to/ArduinoJson-7.4.2/src
ulimit -c 0
python3 test/run.py --cp /tmp/p5-cp --arduinojson /path/to/ArduinoJson-7.4.2/src --negative-control
```

Run the final two commands from this supplement's directory; the destination
of replay must not exist. Replay validates its exact stage trees. This package's
source-inventory.json identifies the production inputs and test files used for
the recorded result. See test/README.md for the substituted boundaries.

## What the result means

The actual TIMED consumer, PluginHttp and SDK HTTP parser process a continuously
readable scripted response. At byte4300, while1775bytes remain, either an abort
callback fires or the separate simulated drain clock reaches its15000ms budget.
The normal code reads zero further bytes, closes the transport, makes only one
request, does not rename or paint, removes the specifically opened .part file,
and preserves the entire file map including private state. These checks happen
before fixture reset. A valid control and fresh preparations after both failures
stage, commit and invoke paint successfully.

The negative control removes only the inner abort polling in a temporary copy of
the SDK header. Both cases read1754extra bytes and fail the designated progress
assertion. A compile failure or unrelated runtime failure does not count as a
successful negative control. The mutant is never applied to production sources.

TLS, clock, SD and display are host substitutes. This is not a TLS/CA test,
15-second wall-clock bound, radio/FAT test, physical Power or complete boot/sleep
measurement. Earlier P4 real-TLS evidence remains separate. No firmware build
was needed because no shipped code or build configuration changed.

The underlying timer, SDK, Wi-Fi fallback and prior integration retain their
existing authorship. Reused CP/SDK host fixtures retain the accompanying license
and notice. AI assistance was used to prepare these tests and their review.
