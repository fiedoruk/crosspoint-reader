# Recorded checks

- Exact public CP PR3877 head: 44626dd5bcc289b0c6b4a0615232e74e1a1d2a8e.
- SDK pin: 425d200a8ea447326b4b9696e4e47dc84ad9d7f6, unchanged.
- Public-source recipient: expected negative control, then 11/11 ASan/UBSan PASS.
- Formatting wrapper and diff whitespace check: PASS.
- Four independent reviews: correctness, architecture, embedded, i18n/docs; no findings, one round.
- Firmware: default ESP32-C3, one build after final edit, 149.791 seconds wall time; two jobs requested at the top-level PlatformIO command. Static RAM 59168 bytes; flash 5922777 bytes.
- No device operation or hardware acceptance, no publication or CI triggered.

The underlying C3 custom-core rebuild ran inside this invocation; its CPU cost is
separate from the host tests. These are source/host/build results, not merge or
release approval. Human design/maintenance acceptance remains a separate handoff.
