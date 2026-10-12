# Validation of the pinned consumer

The ordered series produces the same tracked source bytes as the previously
qualified current-installer candidate: 1015 CP files and 987 SDK files compared.
The new boundary split changes no runtime behavior. Existing source reviews and
tests remain applicable to that exact source; they are not a review of every
unmodified upstream file.

The permission reader validates the full bounded settings object, including
fields that are not used during timer boot. Host tests
exercise enabled/disabled and legacy permissions, malformed unrelated fields,
read/mount/cap errors, root priority and quarantine, and ordinary-sleep RAM state.
The no-bootstrap baseline fails the expected case. Existing TIMED, Power/guard,
verified/bounded-event and PaperMono host tests pass. The current assembled
transport passed 12 real loopback TLS cases. SD/radio/EPD boundaries remain
controlled in host tests.

A single Sticky build of this source passed with two jobs. Static RAM: 70168 B;
flash: 5865387 B. App SHA256:
`7d92b33927d8e794225fd92abc2496275b2fc78a7903ac3b0c859187aaaa06c2`.
The binary is not included. No additional firmware build was needed for this
source-identical packaging change. These figures are not runtime heap or energy.

The ordered series reproduced successfully in a fresh directory using the
documented command and public refs. Its checks do not simulate a full Arduino boot
or establish physical panel pixels, battery wake, button timing or three-model
acceptance. The new neutral binary has not been flashed as part of this handoff.

Upstream SDK verification, timer/installer review, final device acceptance and an
official release remain independent gates. Plugin catalog capability names must
not be used to claim a released timer/verified-event capability before the
accepted integration advertises it. No server-specific capability is introduced.
