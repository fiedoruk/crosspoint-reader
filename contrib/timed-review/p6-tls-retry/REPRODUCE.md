# Reproduce

Obtain `contrib/timed-review/cp2-b32-sdk-lanes` from fiedoruk/crosspoint-reader commit `f7dbdb3c673526b15b4732f2fa6e7849452dea29`. Obtain this complete packet separately. Python3, Git, a C++20 compiler and Python cryptography are required. Reuse the P4 instructions for Arduino-wolfSSL 5.7.2 and its native static archive; do not substitute a different ABI or feature configuration. The retry harness uses the non-MFL archive configuration listed in its runner; the TIMED harness uses P4's MFL-enabled archive separately.

```
python3 replay.py --p4-packet /path/to/cp2-b32-sdk-lanes /tmp/p6
python3 build_wolfssl.py --wolf-root /path/to/Arduino-wolfSSL --output-dir /tmp/p6-native-wolf
python3 test/run.py --cp /tmp/p6 --baseline baseline --fixture fixture --wolf-root /path/to/Arduino-wolfSSL/src --wolf-archive /tmp/p6-native-wolf/libwolfssl-host.a --output /tmp/p6-retry.json
sh /tmp/p6/freeink-sdk/libs/network/SecureNet/test/host/run.sh
```

For wrong-host, unknown CA, malformed CA, hostname-setup failure and handshake timeout, the baseline is expected to make two TCP attempts and the patch one. Cancellation/budget before retry uses one attempt in both variants; cancellation/budget during retry uses two in both. The controlled protocol failure must still use two. Both variants must send no protected request on rejected paths, close sockets and allow a new valid connection on the same object. Timeout, setup and first protocol failures are injected; normal TLS and certificate checks are real. ASan/UBSan cover the harness and client, not the prebuilt wolfSSL archive. Temporary keys, binaries and sockets are cleaned automatically.

For actual TIMED integration, use `/tmp/p6/test/timed_sync/real_tls.py` with the P4-documented wolf-root, MFL archive, ArduinoJson include and output arguments. It checks delivery, invalid image, revocation and a wrong-host certificate with fake storage/panel; it is not a physical reader result.

No commands here build firmware, flash, push, publish, or start CI. Hardware acceptance and human ownership remain separate.

The reused Arduino-wolfSSL 5.7.2 user_settings.h SHA-256 is `82fa06f8b7ded750a95acdb5bb0c9eef08247ea3d8b54f753a924fe7608e572b`. No wolfSSL binary or private fixture key is redistributed. The included build script preserves the original G10 non-MFL host flags and bounds compilation to two workers at nice10.
