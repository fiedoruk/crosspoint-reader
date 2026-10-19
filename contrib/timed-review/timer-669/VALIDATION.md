# Validation scope

CP `0fcdb3ec504619f5cbda430614642ed8a666b0b1`; SDK `f9cc1beda45f4d2d3dade69fc444165727424f53`;
author timer `669642d243c3feec5644e21abe71f1ee760348ab`. The manifest records all result trees.

## Host and source checks

- Eight selected CTests passed in a Release configuration, including wake
  classification, arm/cleanup, guard, trusted time and timer permissions.
  This is not a claim that the complete CTest suite was run.
- Full TIMED tests passed with ASan/UBSan: older/disabled/verified SDK paths,
  checked bitmap commit and paint, boot orchestration and GPIO/PMIC capture.
- USB boot checks passed for the existing host profiles. Hardware is stubbed.
- The final rearm assertion checks the requested interval, held-button flag
  and recovery context. Reintroducing the old argument order is rejected at
  standby and rearm runtime boundaries. Ordinary sleep has a separate source
  assertion, not a full Arduino boot test.
- The timer-arm tests cover C3, EXT1, PaperMono and Picco host boundaries,
  including timer plus held button, zero interval, arm/cleanup failures,
  captured Power and returned-shutdown recovery.
- The unchanged visitor fixture checks 27 source/interval round trips and the
  existing missing/invalid/migration and excluded-board cases. It omits other
  settings and uses synthetic string IDs; it does not qualify the physical UI.
- Four independent review axes completed once. One README wording issue was
  fixed; no substantive firmware change followed review.

## Build and replay

One full consumer `default` (ESP32-C3) build passed after review, on the existing
pioarduino 55.03.311 / Arduino 3.3.11 environment. No retry was needed.
The build result reported:

- RAM:   [==        ]  21.3% (used 69784 bytes from 327680 bytes)
- Flash: [========  ]  85.0% (used 5567651 bytes from 6553600 bytes)

The source did not change during the build. Both W06 and TIMED replayed from
public refs into fresh destinations. The full receiver passed all four README
host commands; 1112 tracked CP files and 991 SDK files matched the build sources.
The package contains no firmware binary.

The new production delta from the previous consumer is the HAL argument order
and its three explicit call sites. Default calls, state ownership, timeouts,
transport and display behavior remain unchanged. No new allocation or task was
introduced. The prerequisite preserves kivarun's timer production implementation;
CMake context is adjusted only for the separate W06 test registration.

## Limits

No new hardware test, physical panel observation, battery measurement or C3
runtime heap qualification was performed. Static linked RAM is not free heap.
Previous TLS/device results retain their original revisions; no new TLS run is
claimed for this unchanged transport. There is no separate new W06-only firmware
build, no new APPROVE of #3820, and no official-release claim. SDK API/ref and
consumer scope remain open before proper upstream PRs.
