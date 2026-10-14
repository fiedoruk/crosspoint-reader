# Validation

Base: CP `5e8b503f4ddefe94abe90b3b67ec3812b9a8273f`, SDK `7fcd3b34c108f28c086ade3b433924022dbc0998`. UX1 prerequisite plus UX2 patch; no root-normalization patch.

- **HOST:** 20 passing extracted-production tests with ASan/UBSan.
- **BUILD:** default ESP32-C3 build passed with Arduino 3.3.11 / ESP-IDF 5.5.5. The combined patches also build for Sticky; see DEVICE.md. No firmware binary is included.
- **DEVICE:** scoped automated Sticky checks are recorded in [DEVICE.md](DEVICE.md). Physical touch-controller and button-only C3 runtime acceptance remain open.

The flow harness uses actual onEnter, loop and activateItem methods; input snapshots, UI routing, download/callback boundaries and checked object/control allocation failures are mocked. Cancellation, acceptance, inherited button hold, first-render gating, identity checks, default callers and byte/line-break limits are covered.

The layout probe runs actual bodyArea, measureSpan, wrapText and drawBody with CP bitmap glyphs and the native FreeInkUI button. Sixteen layout/pagination cases and three span stress cases pass. Renderer metrics/header are modeled; this is not a whole-firmware screenshot. PL/EN and both orientations are represented. RTL and SD fonts are not qualified.

The received fields allow at most 64 newline/NUL breaks; the viewer adds up to 3 separators. A 4092-byte fixture with the Noto Serif 18 bitmap font produced at most 444 spans. Measured host vector capacity was 540 entries / 4320 bytes, with 6480 bytes estimated during growth. This closes the explicit-linebreak amplification found in review; it does not prove handling of arbitrary std::string/vector allocation failure or C3 heap fragmentation.

Before rollout, test physical Confirm/Back and touch, page navigation, small/large reader fonts, return to the selected row, and low-memory behavior on the actual firmware. Dictionary, clipping and README callers retain their default read-only mode.
