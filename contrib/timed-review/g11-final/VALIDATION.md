# Validation boundaries

This candidate separates the existing integration into W06, the upstream timer
prerequisite and the TIMED consumer on CP `b64d797c`. The SDK stays at `084fdfb`
with the previously supplied three-file verification adaptation. Full stage
identities are in the manifest. Both stages have passed separate C3 builds and fresh-directory replay with
their expected result trees. W06 fetched the base commits directly from GitHub;
the final TIMED replay used local mirrors of the same public commits.

## Current host checks

W06 was checked at its own intermediate tree, without the timer or TIMED:
cooperative event budget, actual HTTP/event paths in three SDK capability modes,
production clock freshness tests with ASan/UBSan, and twelve real TLS loopback
cases. Those cases cover verified request/download/token mint, wrong hostname,
untrusted or malformed CA, expired certificate, stale clock, invalid BMP,
unsupported/disabled verification and unchanged legacy behavior.

The final TIMED tree passed settings parsing and source wiring, all three SDK
modes and paint tests, actual boot orchestration, typed GPIO/PMIC capture,
USB cold-start handling, Local selection/render state preservation, guard,
arm/cancel, PaperMono RTC and four actual TLS-to-BMP cases. Sanitizers were used
where supported by the existing runners. The loopback cases cover delivery,
invalid BMP, revoked authorization and wrong hostname.

Existing host warnings in the arm/RTC fixtures remain; no new warning was
introduced in these production paths. SD iteration, PMIC/input, network lifecycle
and the panel are host boundaries. A called display method is not observed glass.
The native wolfSSL archive was reused, not rebuilt; its host configuration
omits ESP acceleration and allocators. These checks do not answer C3 peak heap.

## Local allocation regression

Review found a Local Bitmap object larger than the repository's 256-byte local
variable limit. The final candidate uses the existing checked allocation helper,
with the same function-scoped ownership. An injected allocation failure test
failed against the prior implementation and passed against the final extracted
production method under ASan/UBSan. No parse, draw, transfer or reader-state write
occurs on failure. This removes the large stack object; it is not a measured
claim about device stack headroom or heap fragmentation.

## Current builds

Both stages built once for `default` (ESP32-C3), with the repository's pinned
pioarduino 55.03.311, SDK084 plus the verification adaptation, two jobs and
reduced priority. Sources remained unchanged during each build. No build retry
was needed. TIMED reused the same checkout and build cache.

| Stage | Static RAM | Application flash | Build wall time |
|---|---:|---:|---:|
| W06 | 69,392 / 327,680 B | 5,544,743 / 6,553,600 B | 179.189 s |
| TIMED | 69,792 / 327,680 B | 5,558,691 / 6,553,600 B | 83.891 s |

The final C3 image adds 400 B static RAM and 13,948 B flash relative to W06;
that includes the timer prerequisite as well as the consumer. It is not a
runtime heap or energy measurement, nor a cross-board size claim. The repeated wolfSSL macro-redefinition warning remains. TIMED also retains
the earlier HAL GPIO IRAM section-attribute warning; its GPIO source is unchanged
from the previous integration. No compiler warning originated in the touched
Local allocation change.

W06 image SHA-256: `c99a0dced7bf929d5c58f9947108353bacdc48a9bd1364859a0ea87d82e3ee2b`.
TIMED image SHA-256: `64437a7b609d99d9598c628a785cb0dff4f5de77ee7a54d33357c3f2e6d504dd`.
The packet does not distribute either image. These C3 images are not for the
three S3 reader models. No new device acceptance is claimed.

## Earlier evidence

The preceding T3 Sticky image had scoped physical tests of Plugin A/B delivery,
503/invalid-BMP/server-offline preservation, Local without network delivery,
Off, Power returning to the saved book page and two battery-only cycles.
That evidence is in the existing TIMED support thread and belongs to that
binary. This new candidate has no device qualification. No C3 runtime result,
PaperMono or X4 Pro result is inferred from the Sticky observations.

## Open upstream decisions

The SDK API/ref and C3 runtime evidence remain open in SDK #65. The CP timer
primitive, prerequisites and consumer have separate review scopes. The
Off/Local/Plugin policy and autonomous network caller are proposals; accepted
contracts, final dependency refs and the official release remain external gates.
W06/TIMED do not strengthen the shared token writer's remove/rename durability.
