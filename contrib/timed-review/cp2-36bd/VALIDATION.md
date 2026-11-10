# Validation — CP 36bd / SDK6a208

CP base `36bd50d089a8b3f14b0cfc29dd5ae6ffeb197254`; SDK pin
`6a208c0c46cce99bafa334bc4f171f5e558c5195`. Timer prerequisite remains `a38095cf`.

The delta from the preceding CP 8276 integration contains two upstream fixes:
WebDAV credential protection and complete PageLink href initialization. The
existing production patch series applies unchanged. Only a focused host fixture
and its README were added.

## New HOST evidence

Seven upstream PageLink/ProtectedPaths tests passed with ASan/UBSan. The new
PageLink test fails against the old constructor on poisoned object storage.
The actual-source WebDAV fixture passed 14 PROPFIND denial cases at depths 0/1
before storage existence/open calls, plus three ordinary-path controls. Its
negative control on CP 8276 reports 207 and storage access for /.crosspoint.

The fixture compiles extracted production methods. URL decoding and storage
are host fakes: real HTTP routing, FAT alias resolution, directory enumeration
and device behavior are not established. Other WebDAV methods were inspected
at SOURCE level, including both endpoints of MOVE/COPY and PUT upload stages.

## Retained evidence

SDK, TLS, event budget, TIMED sources, test fixtures and build flags are byte-
identical to the preceding CP 8276 packet. Its 18 TLS and 4 composed TIMED results
are retained evidence, not newly repeated runs. TLS 1.2 MFL 2 KiB and full-size
record fallback were observed there; TLS 1.3 MFL/device heap remain unmeasured.

## Limits

The shared policy covers CP's named credential stores and conservative shallow
8.3 aliases. It does not imply WebDAV protection for all visible plugin files.
PageLink zeroing applies to new objects; older cache contents are not scrubbed.
No cache format, product storage policy or network ownership was changed here.
No new DEVICE, physical FAT, energy, display or C3 runtime-heap claim is made.
SDK contract, consumer scope and official release are still separate gates.

## Final BUILD and replay

One default ESP32-C3 build passed after four independent source-review axes.
Static RAM: 66,944 B, unchanged from the prior candidate. Flash: 5,598,199 B
(+164 B). Wall time: 111.442 s; CPU: 187.97 s; peak RSS: 783,990,784 B.
It used two workers and nice10. SDK dependency links matched this checkout.

Fresh W06 and TIMED directories, using local mirrors of the exact public refs,
replayed to the manifest trees. Full TIMED source files matched the built
checkout byte-for-byte. The standalone W06 recipient also ran the new WebDAV
host fixture successfully. No BIN or private service code is distributed.

