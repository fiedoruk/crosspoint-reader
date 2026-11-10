# Validation and limits

Both `official-pin` and `future-qualification` replays passed at the full P1 stage; the official-pin W06-only stage was also replayed separately. These are dependent patched source trees. SDK `5f0d` contains its upstream response-header byte/count/deadline changes and streaming-body API; the adapter adds the existing verification contract without replacing that header.

On the future lane, the upstream SecureNet host suite passed its resumable-fetch, streaming/bulk and response-header tests. The header suite exercises status and terminator accounting, discarded/malformed fields, 64 fields, 8 KiB, deadline with continuously available bytes, cancellation and redirects. These SDK tests use a scripted transport.

On both lanes the test in `test-transport.py` uses actual CP PluginHttp, SDK HTTP parser and wolfSSL on a synthetic loopback server with simulated SD and time. Future lane: six cases pass: 5 KiB CSP, excessive single CSP, aggregate limit, 65 malformed lines, cancellation with paused CSP, and token response. Failure keeps the last-good file. Pinned SDK: the first three cases pass, but the strict 65-malformed-line expectation fails: it accepts the response and commits the valid image. This negative control shows the new count hardening is qualified only on the future lane. Earlier pin host tests do not establish this property. The two lanes do not share a blanket HTTP hardening PASS.

Actual TIMED event selection, future SDK TLS and BMP decoding were tested against four synthetic loopback cases: valid, invalid BMP, revoked access and wrong host. Tests use simulated storage, clock and display. Timed cancellation during a continuously available CSP stream, physical radio, DNS blocking, hardware Power latency, heap, energy and panel remain unmeasured. The 15-second attempt budget is cooperative, not a hard end-to-end deadline.

Host commands (set environment paths to existing ArduinoJson 7.4.2 and Arduino-wolfSSL 5.7.2):

```sh
# Inside the future replay checkout
nice -n 10 sh freeink-sdk/libs/network/SecureNet/test/host/run.sh
nice -n 10 python3 test/wifi_fallback/run.py
nice -n 10 python3 test/plugin_verified_http/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --sanitize
nice -n 10 python3 test/plugin_event_budget/run.py --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --sanitize
nice -n 10 python3 test/timed_sync/run.py --sanitize
python3 /path/to/packet/build_wolfssl.py --wolf-root "$WOLF_ROOT" --output-dir /tmp/p4-wolf
python3 /path/to/packet/test-transport.py "$PWD" --wolf-root "$WOLF_ROOT" --wolf-archive /tmp/p4-wolf/libwolfssl-host.a --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE"
nice -n 10 python3 test/timed_sync/real_tls.py --wolf-root "$WOLF_ROOT" --wolf-archive /tmp/p4-wolf/libwolfssl-host.a --arduinojson "$CROSSPOINT_ARDUINOJSON_INCLUDE" --output /tmp/p4-timed.json
```

The old TLS security suite and physical observations belong to earlier exact revisions; this packet does not promote those to new-device acceptance. Four independent source-review axes completed. One final C3/default build passed for the future-qualification full P1 stage (see BUILD.json). No separate official-pin or W06-only firmware build, device test or runtime heap measurement is claimed.
