# Validation of the CP 2.0-era integration

The packet was reconstructed from its public pinned refs in fresh directories.
The W06 and full TIMED result trees matched the manifest. The full TIMED receiver
matched all 1,162 tracked CP files and 1,040 SDK files in the build source snapshot.

## Firmware builds

The full TIMED integration, including W06, built for the C3 baseline and the three
network-consumer profiles. These are compilation results, not device acceptance.
The standalone W06 stage was replayed and host/TLS-tested; it was not separately
built as a firmware image in this cycle.

| Target | Static RAM | Flash | Firmware SHA-256 |
|---|---:|---:|---|
| default | 66944 B | 5597349 B | `19baf654ee5da3d1209ce2e3a713b602a61200b4f7f54b67c8cf03a63bdd0994` |
| sticky | 78508 B | 5331583 B | `ffd8af49977700b0561beb2f69de63a3eb5c9aa0ac5c0e949fbd8718dd58e1cc` |
| x4pro | 111596 B | 5439382 B | `72992916505e7fc5215af104cfd2d79782b969ff64f9b3019be37fc6fa206331` |
| papermono | 127908 B | 5438722 B | `9204fa7f3900e0b7e2b53cd0f1dc8ed7565943c7ca429d183fffc237e7ee2f77` |

Build inputs remained unchanged. The SDK dependency links resolved to the
reviewed SDK checkout. No firmware binary is distributed in this packet.

## Host checks

- W04-stage BMP helper, production event drain and decoder: ASan/UBSan.
- W06 actual HTTP/event code: old, disabled and verified backend contracts,
  early-connect failure/cancellation, response-stream and known/unknown length cases.
- Shared event operation/time budget and retained-event cases.
- Full timer selection, boot/USB handling, paint/decode and captured Power paths.
- Local wallpaper selection/rendering without reader-state writes; ordinary
  LCG state updates and monochrome fallback/overlay delegation.
- Timer settings reader, root/quarantine limits, actual descriptors and
  persistence callbacks for enabled, Picco and Metalio profiles.
- Actual PaperMono HAL/SDK RTC path over a simulated bus: seven wake origins,
  arming/cancellation and rollback.
- PaperMono sleep-function regression: RTC unavailable with a working PMIC
  permits button-only shutdown only after the RTC wake route is disabled;
  an unknown PMIC route still restarts.
- Actual CP/SDK TLS over POSIX loopback: 12 verification/legacy cases, plus
  the composed TIMED TLS/bitmap cases.
- Existing SDK SecureNet host suites for resumable transfers and bulk request timing.
- Eight selected CTest checks: wake classification, fresh time, timer arming,
  wake guard and timer permission.

The standalone test fixtures and recorded command scope are described in README.md.
The tests use synthetic content and temporary credentials. They do not prove
Wi-Fi, DNS, NTP, SD power-loss behavior, or display/PMIC behavior on hardware.

## Remaining gates

- SDK #65 contract/ref acceptance and original X4/C3 runtime heap measurements.
- Maintainer acceptance of the complete consumer, not just the timer primitive.
- Physical panel, Power, energy and repeat-cycle acceptance for this exact revision.
- Official release and the separate service/onboarding implementation.

The optional wolfSSL proactive input-buffer reservation is not enabled by this
consumer configuration. Do not infer device-memory acceptance from a host test
or from the presence of that SDK API. The 15-second budget remains cooperative.
Earlier device results belong to their earlier binaries and are not transferred here.

No upstream comment, push, pull request, CI run or device flash was performed
as part of preparing this packet.
