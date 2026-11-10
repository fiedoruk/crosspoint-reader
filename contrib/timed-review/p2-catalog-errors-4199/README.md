# Keep server error detail on screen, out of download logs

Support for osteotek's CrossPoint PR #4199. The HTTP error-display feature and
its original implementation belong to the PR author. This package proposes one
line of additional log minimization plus a host regression fixture.

Exact PR head: `83be676044276c3f13bd6485758739bd38814151`.
SDK gitlink: `a5d5332e82502198ad1bc5a6236eca57afab39d9`.
This is not a rebase onto current develop.

`CatalogActivity::finishDownload` logs a numeric download error and passes its
optional detail to the error screen. The patch removes server-provided detail
from the log call, preserving both the numeric code and the screen text. It does
not scrub previous logs, other diagnostic entries, or content shown on screen.
The service must still return concise, user-safe text, without secrets or
personal data, in `error` and `message`.

## Reproduction

From this package directory:

```sh
git clone https://github.com/crosspoint-reader/crosspoint-reader.git source
git -C source fetch origin 83be676044276c3f13bd6485758739bd38814151
git -C source checkout --detach 83be676044276c3f13bd6485758739bd38814151
python3 tests/run.py /path/to/ArduinoJson-7.4.2/src
git -C source apply ../candidate.patch
python3 tests/run.py /path/to/ArduinoJson-7.4.2/src
```

The first run fails when a synthetic response marker reaches the captured logger.
After applying the patch, both signed-char and unsigned-char variants pass. The
runner requires Python 3, a C++17 compiler and ArduinoJson 7.4.2 headers; it does
not need firmware dependencies or a device for the host test.

The fixture extracts the actual HTTP-detail formatter, fail/finishDownload and
error-screen consumer bodies. It tests HTTP401/403/404/422/429/503, error/message
precedence, missing/empty/non-string/malformed JSON, valid UTF-8 at the 120-byte
boundary, a large selected field, generic/cancel behavior, the UI text and the
log output. It substitutes the logger and screen model; it does not execute the
complete activity lifecycle, transport, renderer, pixels or a physical device.
The numeric values of the test enum are substitutes; assertions check behavior,
not ABI or real logger output. Temporary host executables are removed on exit.

## Evidence limits

The 120-byte cap bounds the resulting reason text, not parser peak memory.
A filtered JSON document can retain a long selected value before truncation.
This package does not change that parser or demonstrate device heap behavior.

If cached-catalog reparsing fails after a transfer, that existing failure path
can replace the download error. Existing rendering synchronization also needs
separate analysis before any lock change. Neither is repaired or reproduced as
a device failure by this logging-only patch.

No new strings, translations, firmware setting, API or dependency is introduced.
AI assistance was used for this support patch and test preparation. No firmware
binary is included. Hardware acceptance and the author's integration decision
remain separate from the host regression.

For a physical follow-up on the same patched firmware, have a test service return
an HTTP422 JSON error with a synthetic marker. Confirm the useful status/reason
on the reader, the numeric failure in diagnostics without the marker, and retry
and cancellation. Do not use real account data as test content. This follow-up
has not been performed by this package's host test.
