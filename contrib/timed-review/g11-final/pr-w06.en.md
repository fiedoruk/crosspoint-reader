## Summary

Add opt-in certificate and hostname verification to existing plugin event
requests. A handler supplies `tls.ca_file` beneath its own plugin directory.
Malformed trust settings, unavailable SDK verification, insecure URLs and a
missing fresh time sample fail before credentials are sent. Redirects and
caller-owned sessions are not allowed on this path. Legacy requests retain
their current behavior.

This lets an SD plugin protect authenticated background delivery without
adding a service-specific connector or changing other clients' TLS policy.
The event and its credential refresh use the same trust requirement.

## Scope Check

- [x] Read SCOPE.md and ROADMAP.md.
- [x] No new theme, interactive app or service-specific connector.
- [x] Reuses the existing event drain, HTTP helper, clock and SDK transport.
- [ ] The proposed SDK verification API/ref still needs maintainer agreement.

This dependent candidate follows #3907, #3908 and #3956. The separate SDK #65
adaptation is a prerequisite, not a hidden SDK bump in this CP patch. Catalog
requests with the new TLS field are rejected rather than silently treating them
as verified. The timer consumer is a separate review scope.

## Validation and limits

Host checks cover actual event/HTTP paths with an older SDK, verification
disabled and verification enabled, plus fresh-clock cancellation and timeout.
Twelve loopback cases use the real CP helper and SDK TLS implementation,
including wrong hostname, invalid/untrusted CA, expired certificate, stale
clock, invalid BMP, auth and legacy compatibility. Exact results and build
figures are in VALIDATION.md.

The time sample is fresh SNTP, not authenticated UTC. Network cancellation is
cooperative; this does not impose a hard bound on every socket operation.
C3 runtime heap remains unmeasured. No new device test is claimed for this
revision, and shared storage's power-loss/remove-rename limits remain unchanged.

### AI Usage

**YES.** AI assistance was used for implementation, review and this description.
