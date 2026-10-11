# Verified plugin HTTP, timed panels and PaperMono RTC wake

Updated 11 October 2026. These are dependent source changes for review,
provided separately from the timer primitive in PR #3820.

- [W06.diff](W06.diff): verified plugin requests, downloads and token refresh.
- [TIMED.diff](TIMED.diff): the existing SD-configured timer consumer.
- [SDK-PAPERMONO.diff](SDK-PAPERMONO.diff): RX8130 countdown operations and register-map correction, retained PMIC wake state and GPIO0 configuration.
- [PAPERMONO.diff](PAPERMONO.diff): the CP adapter using that SDK API and the shared consumer.
- [source-review.zip](source-review.zip): all nine patches, public refs, tests, reproduction script and licenses.
- [DEVICE-NOTES.en.md](DEVICE-NOTES.en.md): executed checks and hardware limitations.

The final two patches add PaperMono support. It shuts down the ESP32 through
its PMIC, so an ESP deep-sleep timer cannot wake it. The new path qualifies the
RX8130/PMIC cold boot before entering the shared consumer; ordinary button,
USB, software and brownout boots do not qualify. It retains the LDO during
shutdown following M5Stack's RTC example; standby current remains unmeasured.

The series uses CP `d1f5d1eca4a114086c88d4764a66b7703a1c626c` and its SDK pin
`32a265fa86498c014e13a5bc16133bb021cb620c`. Patches 01–07 are unchanged from
the previous material. The SDK verification/capability and RTC/PMIC APIs remain
proposals above that pin. The CP gitlink is not advanced to an unaccepted ref.

Sources reconstruct from the pinned public commits. RTC/PMIC fault tests,
boot/Power/guard checks and a PaperMono build pass. A separate bench image
with the same public core completed repeated cycles on one PaperMono; physical
A-to-B changes were observed on USB and battery, with last-good retention
after a 503 response and failed Wi-Fi joins. Official CP was restored afterward.
The neutral binary itself, final-window Power behavior, a real book session,
standby current and other models still need hardware acceptance. USB Drive did
not expose a volume during the private bench; console and SD access worked.

The timer primitive can be reviewed independently. This material does not ask
to fold the consumer or PaperMono adapter into that PR. Separate CP integration
needs its prerequisites, accepted SDK contracts and periodic-networking scope.
The RTC/PMIC change is separate from SDK #65's TLS work.

Michael Kazakov (@kivarun) authored the timer primitive. Sameh Foulad (@sfoulad)
supplied the SDK verification work. CP-derived code retains LICENSE-CP;
SDK-derived code retains LICENSE-SDK and NOTICE-SDK. AI tools assisted code,
tests, review and documentation. No firmware binaries, service code or private
bench controls are included.
