# Limited X4 Pro bench observations — 9 October 2026

Two private test images produced separate observations on one X4 Pro:

- `db807fa64376978aef5b8d43ea57e9a6fe511404d88f014b2c2ad5776c37de3c`:
  autonomous timer wakes, verified TLS 1.3 downloads and a visible image A→B change.
- `4e6389367f2da18307703cbd9848921476a5161c86a37bb494ce1bc4e7e8079a`:
  after the clock-window correction, HTTP 200/image A followed by HTTP 503,
  with A retained on the panel and its file hash unchanged; rearming and sleep.

Camera observations, independent screen reads and SD readback supported those
limited checks. The private harness bounded each run to two timer attempts
and then returned to Home; it is not part of this source candidate. Neither
firmware binary, the harness nor the image generator is included here.

Fresh callbacks measured on the corrected image took 1750 ms and 2550 ms.
Acceptance of a callback at 7 s is host-test evidence, not a physical timing
measurement. The evidence does not identify the cause of every earlier missed
attempt or establish long-term reliability. Physical Power interruption,
energy, heap, flash endurance, other models, the service and official release
remain unqualified. The reader was restored to official CrossPoint 1.6.5.
This is contextual evidence, not DEVICE PASS for either new source package
or a binary built from it.
