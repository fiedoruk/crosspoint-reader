# Validation and limits

Measured on 18 October 2026. These results apply to one PaperMono and the pinned candidate below.

## Host and build

- The unmodified base fails the qualified RTC wake and PaperMono interval controls with the expected exit 42.
- ASan/UBSan checks pass 13 wake/reset cases, RTC arm/cancel/rollback, 10 shutdown/handoff paths, PMIC held/read-clear/failure/cleanup, and Off/invalid interval handling. Existing T1 GPIO and ESP arm/rail regressions pass.
- The build uses Arduino 3.3.11, IDF 5.5.5 and matching prebuilt `dio_opi` headers and libraries, with brownout detection enabled. Linked PSRAM initialization and heap registration were checked. RAM: 120,704 bytes; flash: 6,051,054 bytes. These are build totals, not runtime heap deltas.
- A fresh local receiver applied 595 + T1 + T2 and passed the advertised host checks. The final documentation-only revision was applied in a separate clean Git index, and all 17 resulting files matched the candidate. Code and tests were unchanged, so their checks and firmware build were not repeated.

Tested firmware SHA256: `87b9f6207997fadc15979f3dbd23a1bfabca90da979a6e897c8a17289db972ef`.

## Device checks

With USB connected, consecutive boots classified as RTC Timer, loaded local images and rearmed the 60-second sleep interval. Independent camera observations confirmed A→B on the panel. USB reappeared roughly 63 seconds apart, including rendering and enumeration; this is not an RTC accuracy measurement.

After the owner confirmed USB was disconnected, camera observations showed A→B→A without requested button input. Supply state was owner-confirmed, not measured electrically. Current, capacity, endurance and exact wake timing were not measured.

For Power handoff, a local host cue was issued when the neutral firmware logged loading the timed image. The owner pressed the physical Power button. The log shows a software reset after panel transfer, without an intervening USB power cut, followed by the reader loading the same saved position. An independent camera reading confirmed the same page 2/6 and 4% progress. This is one physical handoff trial, not an exhaustive measurement of every pulse width or the final PMIC power-cut interval.

After earlier armed cycles, Off was saved and read back, then the same neutral firmware was installed. It entered normal sleep and did not reappear for 166.5 seconds, spanning more than two previously observed refresh periods. An owner Power press then restored an ordinary boot with USB present and opened the reader. This is a functional Off check, not a power-consumption measurement.

## Remaining limits

The returned-shutdown guard is covered by host fault tests. PMIC shutdown did not return on the tested USB connection, so that branch was not exercised on hardware. USB Drive was not qualified in this campaign; companion diagnostic attempts returned Home without exposing a disk. No USB Drive fix is claimed.

No network delivery, other board, battery endurance or official release is qualified by these checks. The device was returned to compatible official firmware after restoring saved stores and removing test fixtures. Firmware images, private bench controls, credentials, service code and internal costs are excluded from this bundle.

AI assistance was used for implementation, tests and review.
