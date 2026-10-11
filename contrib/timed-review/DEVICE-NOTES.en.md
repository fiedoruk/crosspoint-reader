# Validation scope

## Source and host

Tests exercise the
actual RTC/PMIC helpers with a recording bus and ASan/UBSan: 18 RTC fault
positions, 26 PMIC positions, disabled-RTC fallback and seven wake origins.
The affected boot, Power capture, wake guard and shutdown/abort host checks pass.

The package was reconstructed from its public refs in a fresh directory;
all output hashes matched. The two new RTC/HAL test runners also passed there.
The unchanged transport has separate TLS evidence from the previous series; it is
not presented as a new physical PaperMono test.

## Build

The neutral candidate builds in the `papermono` environment. Static RAM use is 120,912 B;
flash use is 5,955,066 B of 6,553,600 B. The app image is 5,960,032 B,
SHA-256 `dcf3689e14d2d60b8a931fe5fc895d3cd73e658a790d529b10207e66acf0f9c7`.
These figures do not measure runtime heap or energy.

## Device — scoped bench evidence

A separate private PaperMono bench image retains the same RTC/PMIC and TIMED
core, with a three-entry limit and a fixture provisioning interface. Its SHA-256
is `8041bf1a12b265018fe623ba0366fc7cad4549d725292dcbd77c4525aaa2430b`.
It is not included in this packet and is not the identical neutral build above.

Three consecutive USB-powered cycles reported external PMIC wake 0x20,
GPIO0-only wake enable 0x01 and a qualified RTC timer. Each fetched a 200 response
through verified TLS 1.3, refreshed the panel and rearmed. Independent camera
reading confirmed the physical A→B change. A controlled 503 preserved the
last-good file checksum and performed no panel transfer in the captured cycle.
The reader was outside camera view for that particular 503 observation.

On battery, with the USB plug visibly disconnected and the owner confirming
removal, a fresh request delivered frame B and independent camera readings
confirmed A→B. A subsequent request at the configured cadence demonstrated
rearm. Reconnecting USB reported PMIC source 0x02 and did not enter TIMED.
The owner also pressed Power while unplugged and then reconnected; the observed
result was ordinary Home with a cold-boot reset. The exact button edge timing
was not captured.

The route uses the existing Clock Sync path. One 5-second NTP initialization
attempt timed out; a second bounded attempt succeeded. This does not waive the
RTC initialization prerequisite. The LDO is held during PMIC shutdown; standby
current is not measured. Intervals above 65,535 seconds round up to minutes;
the first countdown period can be up to one second short.

## Limits before broader hardware acceptance

The private bench result is not a full qualification of the neutral binary.
Physical Power during blocking work and the final check-to-shutdown interval
remain to be tested, as do a real book session and long-run current/energy.
A controlled wrong Wi-Fi credential produced three bounded wake attempts with
no server requests and the same last-good file checksum. The correct credential
was restored and a successful join confirmed. Fixture files and the private NVS
budget were removed before official recovery. Official CP 1.6.5 was restored
and verified. Its runtime mounted SD, returned
a complete 48,000-byte framebuffer over USB, and displayed normal Home in a
fresh camera capture. Brownout protection remained enabled. Battery percentage does not measure energy use.

Scope/API acceptance, human maintenance ownership, the final supported-model
matrix, upstream merge and official release remain separate gates.
