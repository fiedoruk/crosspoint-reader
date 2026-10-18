# Validation notes

Host checks, the Sticky build and the scoped device checks below are complete.
This is dependent review material; merge and release remain separate gates.

## Source and host

The main integration issue was a Local timer wake calling wallpaper selection before
reader state was loaded: selection could save the default state over the book
path. The regression fails on that revision and passes after autonomous
selection stops updating persisted wallpaper history. Normal sleep retains its
existing history behavior; autonomous random selection can repeat an image.

The first bitmap decode failure now returns before panel transfer. The existing
gray pipeline is still multi-pass: a later gray decode failure can leave the
completed black-and-white base. This series does not claim atomic grayscale
output or SD power-loss durability.

Recorded host coverage includes:

- Real bounded event/HTTP paths and six verified-transport configurations.
- The bounded settings reader, source selection, configuration conflicts and
  missing/quarantined plugin cases; normal migration wiring is source-checked.
- Actual timer orchestration, typed GPIO/PMIC Power capture, timer arm/cancel,
  returned-shutdown behavior and PaperMono RTC boundary tests.
- Twelve real CP/SDK TLS loopback cases and four real TIMED-to-TLS/BMP cases.
- Local selection/render state-preservation and initial decode-failure regression.
- Fresh-directory patch replay, standalone W06 host tests, then the TIMED Local
  and boot checks. All public files match the neutral build's source.

SD, GPIO, PMIC, network lifecycle and panel boundaries remain stubbed where
stated by each harness. TLS loopback uses the actual transport; it does not
measure C3 runtime memory or radio behavior. The ordinary X4/C3 qualification
requested in SDK #65 remains external.

## Build

The neutral Sticky candidate built with the pinned pioarduino 55.03.311 toolchain,
SDK084 plus the verification adaptation, and two jobs. Its SHA-256 is
`07c40144de809637c720a3cb6feb7db1b534c0f210c2d59054d50e27ba6fe0aa`.
Static RAM use is 80,220 / 327,680 bytes; application flash use is
5,268,903 / 6,553,600 bytes. These are linker figures, not TLS runtime headroom.

The build emitted existing third-party const-qualification warnings and the
T1/T2 duplicate IRAM section-attribute warning. No firmware binary or
private bench code is included in this packet.

## Device

The neutral image above has been exercised on one Sticky. Authenticated HTTPS
changed the visible panel from A to B over successive autonomous cycles. Two
HTTP 503 responses, an HTTP 200 body that was not a BMP, and an unavailable test
server left the visible last-good B content intact. Delivery resumed after the
server returned. The offline case stopped the server, not the access point.
The blocked connection made that attempt take about 24 seconds, including fresh
time acquisition; the cooperative transport budget is not a hard end-to-end
15-second deadline.

With Source Local selected, the same valid online plugin remained enabled.
The reader displayed the SD image through the Local timer path; two timer boots
were recorded without another request reaching the test server. The subsequent readback preserved the open book path. Ordinary Home sleep
changed its own resume flag; this is not a byte-for-byte state claim.

With Source Off and the same valid plugin still enabled, the reader stayed
asleep for 142.7 observed seconds, longer than two preceding one-minute
intervals. No new boot output or request was recorded while the server remained
available. This is a functional observation, not an energy measurement.

On USB, physical Power during a paced HTTPS response interrupted the transfer
and entered the ordinary reader path in the same timer boot. The book returned
to the recorded spine 0, offset 541, page index 1; the visible text matched the
baseline. Ordinary Power from sleep also returned to that page. This does not
qualify every blocking DNS, TLS, SD or panel boundary.

After the owner disconnected USB and the bound USB interface disappeared, two
consecutive requests displayed B and then A. Camera observations and request
records agree. This qualifies those functional battery cycles, not battery
lifetime or power consumption.

These visual observations cover the unobstructed region of a shared camera
view, not every pixel. Private service firmware used for snapshots or navigation
is not TIMED acceptance. No PaperMono, X4 Pro or C3 result is inherited from
earlier images. The original fixed-path data was restored and checked across 17 paths before
normal CP format migration. The verified neutral image was left on the device;
it loaded the restored settings and returned to sleep under the original
held-Power preference. The retained image is not a fresh Home-screen check.
Test files, cache, bench servers and the temporary timing page were removed or
closed, and USB was released.

## Upstream gates

The SDK verification contract and the Off/Local/Plugin setting are proposed.
The timer PR moved to `1bc497520f6efacd09920225d5bf319b8f4a9df6` during
this validation. This packet remains pinned to the CP/SDK refs in its manifest;
it has not been rebased or device-tested on that newer timer head.

The series depends on the token-storage revision and the existing checked-BMP
and bounded-event changes. Integration on pinned prerequisites can be reviewed
before merge; a clean PR on upstream develop needs compatible accepted refs.
Official installation support and release are separate gates.
