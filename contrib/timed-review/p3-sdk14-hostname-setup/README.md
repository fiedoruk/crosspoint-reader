# Hostname setup failure: SDK PR #14 support

A focused proposal for SDK PR #14 at
`34aabdf2c8045dc90df6ec1b95f974224d8fcf37`. The verification/retry feature remains
its author's work. Apply `pr14-hostname-setup-suggestion.patch` to that exact
SDK checkout; it checks the hostname-setup return and uses existing cleanup.

The included raw/fixed SecureClient source files match that head plus only this
patch. This package is not a rebase onto current SDK main or a firmware release.
The native test includes copied CP host transport/fixture helpers and their
license; SDK license/notice are retained separately. No wolfSSL source or binary
is distributed here; use Arduino-wolfSSL 5.7.2 with its own license.

## Reproduce

Requirements: Python3 with `cryptography`, C/C++20 compilers, `ar`, and an existing
Arduino-wolfSSL5.7.2 source package (library.json and src/). Do not install these
implicitly. From this directory:

```sh
python3 build_wolfssl.py --wolf-root /path/to/Arduino-wolfSSL --output-dir ./host-build
P3_WOLFSSL_SRC=/path/to/Arduino-wolfSSL/src \
P3_WOLFSSL_ARCHIVE="$PWD/host-build/libwolfssl-host.a" python3 run.py
```

The library builder uses two jobs and nice10. This host configuration omits ESP
hardware acceleration, MFL and retained-input-buffer flags; it is not an MCU
heap test. The test binds only loopback and uses temporary certificates and a
synthetic request. Fixture workers are joined and temporary executables removed.
`host-build` is disposable after preserving its receipt.

Six cases: valid host, ordinary wrong host, and injected hostname-setup failure,
for raw and patched sources. Raw14 with the injected failure connects and sends
the synthetic request; the patched source makes zero handshake calls and sends
zero requests. Valid-host and ordinary wrong-host behavior is retained. PASS
means the expected observations, including the unsafe raw negative control,
were reproduced; it does not certify raw14.

The wrapper models WOLFSSL_FAILURE/MEMORY_ERROR with no hostname installed.
It does not induce or measure an ESP32 allocation failure. Conditions are CERTS
defined, CA supplied, verification requested, insecure fallback disabled.
Existing TLS1.2 retry and opt-in insecure fallback policy are unchanged; this
patch must not be read as making insecure fallback acceptable for private data.
No board build/device test/merge approval is claimed. AI tools assisted this
support patch and test preparation.
