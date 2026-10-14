# Validation

Base: CP `5e8b503f4ddefe94abe90b3b67ec3812b9a8273f`, SDK `7fcd3b34c108f28c086ade3b433924022dbc0998`. UX1 patch only; no root-normalization patch.

- **HOST:** 9 passing extracted-production tests with ASan/UBSan.
- **BUILD:** default ESP32-C3 build passed with Arduino 3.3.11 / ESP-IDF 5.5.5. The combined patches also build for Sticky; see DEVICE.md. No firmware binary is included.
- **DEVICE:** scoped automated Sticky checks are recorded in [DEVICE.md](DEVICE.md). Physical touch-controller and button-only C3 runtime acceptance remain open.

The harness covers discovery ordering, Hub presence, equal titles and selection restoration. Root precedence is unchanged in source; the scan itself is mocked. SD discovery, metadata parsing and moveSelectionTo are mocked. No pixel layout changed. Physical-button and touch selection remain acceptance checks.
