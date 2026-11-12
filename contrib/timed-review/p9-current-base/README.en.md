# W06/TIMED on the November 12 upstream bases

This packet replays the existing support on CP `fa17b9ca` and SDK `e637713a`.
It adds host checks for the reader-layout and screenshot changes in that delta.
There is no new production patch: the P7 Power handoff and P6 TLS retry changes
remain unchanged, as do their prerequisites and contributor credits.

The two routes are `w06` (checked images, bounded events and verified transport)
and `timed` (the full dependent consumer, including the timer and P7).
Both use the explicit SDK qualification revision. CP's recorded SDK gitlink is
still `6a208c0c`; this packet neither updates that pin nor qualifies a separate
build using only the official pin. It is not an official release or an SD plugin.

The delta invalidates section cache v74 in favour of v75, changes the reader's
bottom margin, adds the file-extension setting, and fixes screenshot rotation.
The tests distinguish a stable page layout from repagination: a saved text anchor
can belong to a differently numbered page after layout changes. Screenshot
rotation does not change the plugin-download raster contract.

## Reproduce

Use Python 3, Git, a C++20 compiler with ASan/UBSan, and existing ArduinoJson 7.4.2
headers. Run from the packet root. Each destination must not exist. No dependencies are installed by the
host scripts. Run the two routes separately; remove an unneeded receiver before
creating the next one.

```sh
python3 replay.py /tmp/p9-w06 --through w06
python3 /tmp/p9-w06/test/plugin_verified_http/run.py --arduinojson /path/to/ArduinoJson/src --sanitize
python3 /tmp/p9-w06/test/plugin_event_budget/run.py --arduinojson /path/to/ArduinoJson/src --sanitize
sh /tmp/p9-w06/freeink-sdk/libs/network/SecureNet/test/host/run.sh

python3 replay.py /tmp/p9-timed --through timed
python3 /tmp/p9-timed/test/test_remote_button_input.py --sanitize
python3 /tmp/p9-timed/test/timed_wake_guard/run.py --sanitize
CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src python3 /tmp/p9-timed/test/timed_sync/run.py --sanitize
python3 test/reflow.py --cp /tmp/p9-timed
python3 test/screenshot.py --cp /tmp/p9-timed
python3 test/settings.py --cp /tmp/p9-timed --arduinojson /path/to/ArduinoJson/src
```

The existing P5 [busy-header supplement](https://github.com/fiedoruk/crosspoint-reader/tree/cd3255bc53a02238dbae8b44e1c10905abb0707a/contrib/timed-review/p5-timed-busy-headers)
runs with `python3 /path/to/p5-timed-busy-headers/test/run.py --cp /tmp/p9-timed --arduinojson /path/to/ArduinoJson/src`.
P6's [real-wolfSSL result](https://github.com/fiedoruk/crosspoint-reader/tree/67bdb4bd64919cfcb82d9099697db5b60e382156/contrib/timed-review/p6-tls-retry)
is prior HOST evidence reused only after source parity checks; no new real-wolfSSL run or physical TLS measurement is claimed.

For the actual upstream chapter-parser target, use existing GoogleTest 1.17.0
sources and Expat. This wrapper avoids configuring unrelated test dependencies:

```sh
cmake -S test/parser -B /tmp/p9-parser -DCP_SOURCE=/tmp/p9-timed -DGTEST_SOURCE=/path/to/googletest
nice -n 10 cmake --build /tmp/p9-parser --target ChapterHtmlSlimParserTest -j2
/tmp/p9-parser/parser/ChapterHtmlSlimParserTest
```

The reflow negative control (`test/reflow.py --cp /tmp/p9-timed --negative-control`)
must compile and fail the assertion that repagination moves the saved anchor to
page 3. It replaces only the normal resume assignment in a temporary host source.

## Boundaries

The reflow test extracts production progress.bin reading, cache validation, viewport
margin calculation, and normal/deferred resume mapping. SD is in memory and the rebuilt
page-offset LUT is synthetic. It does not execute the full renderBook/buildSomeMore
pipeline, connect parser-produced offsets to resume, or prove physical glyph placement.
The matching-layout case checks the mapper result; the production cache-hit fast
path that clears the stored offset before selection is not executed by this fixture. The upstream parser target tests
its own fixtures separately. The screenshot check round-trips production drawing
through the production BMP writer, with storage and display objects replaced by
host fixtures. The settings test extends the existing selected timer-registry
fixture with the real `showFileExtensions` descriptor; other settings/UI are not
qualified. The original timer permission fixture has no saved-network fallback
scenario; the supplement declares that API and fails if it is unexpectedly called.
P1's existing fallback tests remain separate.

P8's controlled X4 Pro result belongs to the previous P7 binary, with touch page
turns disabled. It is historical device evidence, not acceptance of this new
integration. C3 memory, touch-enabled operation, other boards and production
onboarding remain open. See VALIDATION.json for executed checks and build scope.

The purpose is to keep an idle information panel compatible with normal reading:
automatic updates should not disturb the saved place when the reader is picked up.
The timer remains kivarun's work. SDK verification is based on #65; P6 credits
jpirnay's error-classification work. Existing input and other contributor credits
are retained. AI tools assisted integration
and host tests. Existing CP/SDK licenses and notices accompany the reused patches.
