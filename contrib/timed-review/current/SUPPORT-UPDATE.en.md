The [updated consumer package](ARTIFACT_URL) now separates the complete TIMED caller from its six dependency layers. It reconstructs against the installer at `fc3aed12` and SDK `1a5448df`; the old installer patch is omitted.

The primary diff contains timer selection, verified image delivery, native decode/commit/transfer, Power handling and rearm, including PaperMono and the early global-plugin-permission read. It preserves explicit plugin disable and installation quarantine. Cache/304 and server-suggested cadence remain separate follow-ups.

One command replays the public series and its host checks. The final source is unchanged from the recorded Sticky build and current transport tests; this packaging pass did not add another firmware build or device claim. A new neutral-binary device run and accepted dependency refs are still required before merge/release.

The timer and installer remain separate author-owned prerequisites. This is updated review material for the consumer, not a request to fold it into the timer primitive. AI tools assisted implementation, tests and documentation.
