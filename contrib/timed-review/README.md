# Verified plugin HTTP and a timed SD consumer

Updated 11 October 2026. This is source material for two proposed CrossPoint
changes, provided separately from the timer primitive in PR #3820.

- [W06.diff](W06.diff): verified requests, downloads and token refresh,
  after the checked-BMP and event-budget prerequisites (#3907 and #3908).
- [TIMED.diff](TIMED.diff): the SD-configured timer consumer, after verified
  HTTP, the existing timer primitive and the bundle-installation fix.
- [source-review.zip](source-review.zip): the complete series, pinned public
  refs, tests, reproduction script, validation notes and licenses.
- [DEVICE-NOTES.en.md](DEVICE-NOTES.en.md): older, limited X4 Pro observations
  on separate images. They do not qualify this candidate.

The tested base is CP `26ccbe2816dd8a9b2b4f5c89ffaac6f1afbdaedd` with SDK pin
`32a265fa86498c014e13a5bc16133bb021cb620c`. The SDK verification/capability patch
is still an explicit proposal above that pin. Both CP diffs need their
prerequisites and do not apply independently to raw develop.

This update preserves current upstream Metalio wake and power-off behavior,
adds eight host wake-hold cases and fixes a stale timeout expectation in the
existing test. It does not enable the full consumer on Metalio or PaperMono.
Verified HTTP and the SDK proposal are unchanged.

The source reconstructs from public commits. Six host groups, 16 CTest cases,
12 verified TLS cases and four TIMED/TLS/BMP loopback cases passed. The composed
series builds for X4 Pro. The ZIP's validation notes document the existing
wolfSSL warning, exact build hash and untested hardware behavior.

The consumer remains opt-in and source-enabled for X4 Pro and Sticky only.
SDK API acceptance, CP's periodic-networking scope, prerequisite integration
and new-candidate hardware acceptance remain open. The timer primitive can
be reviewed and merged independently; this material does not ask to fold
the full consumer into that PR.

Michael Kazakov (@kivarun) authored the timer; Sameh Foulad (@sfoulad) supplied
the SDK verification work. CP-derived diffs retain LICENSE-CP, and the ZIP
retains SDK licenses and notices. AI tools assisted code, tests, review and
these notes. No firmware binary, account system or service implementation
is included.
