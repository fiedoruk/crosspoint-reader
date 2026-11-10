# Avoid redundant TLS version retries

This patch is an overlay on the future-qualification lane of P4, not a standalone SDK PR or official firmware. The proposed verification changes from SDK #65 remain prerequisites.

A connected TCP socket previously allowed a second TLS attempt even when loading the CA or configuring the hostname had failed. Recognized certificate errors and handshake timeouts could also trigger it. The patch retains a retry decision only for a fatal handshake error outside the eight certificate-error codes adapted from jpirnay's SDK #14. It preserves the explicit TLS1.2 fallback for other fatal handshake errors. This list is intentionally bounded, not a complete taxonomy of certificate or allocation failures.

The decision replaces one existing per-client boolean. It is reset at the start of each attempt, preserved through cleanup for connect() to inspect, and introduces no allocation or public API. Cancellation is still polled before retry; consumer deadlines remain cooperative and cannot interrupt blocking DNS/TCP. No insecure downgrade is added.

Host tests compare the original and patched sources with actual wolfSSL and local certificates. They cover TLS1.2/1.3 success, wrong host, unknown/malformed CA, injected hostname-setup failure, an injected first negotiation failure followed by a real TLS1.2 handshake, cancellation/budget before and during the second attempt, timeout and object reuse. The static wolfSSL archive itself is not sanitizer-instrumented. Panel, storage and device-memory evidence remain separate.

This reduces avoidable connection work when an idle-screen download fails, while keeping ordinary reading and compatible servers unchanged. It does not establish battery savings, C3 heap headroom, official SDK support, hardware acceptance or release readiness. AI assistance was used for this patch and its tests. Existing SDK verification and retry authorship is retained.
