# Validation

The unmodified CP #3877 head `5e8b503f` fails the new repeated-trailing-slashes
case. With the one-line patch, all 12 cases pass under ASan/UBSan. A separate
receiver fetched the pinned public refs and reproduced the expected failure,
patch application and passing result. The actual bundle method and discovery
source are compiled; storage and downloads use host stubs.

Four independent reviews covered correctness, architecture, embedded behavior
and documentation. No runtime finding remained. The source lock's SDK metadata
was corrected to the actual CP gitlink `7fcd3b34`; the host reproducer does not
check out or use SDK code.

The patched `default` C3 firmware target built once with the pinned platform
55.03.311, Arduino 3.3.11 and ESP-IDF 5.5.5, two jobs and reduced priority.
Tracked sources stayed unchanged during compilation. Firmware SHA-256:
`cbfe3956a6247848c7332ef95d6f15655238f7e3161d6187a519f95993f90a13`.
Static RAM is 59,264 bytes and linked flash is 5,939,949 bytes. These are whole-build
figures, not a measured patch delta or runtime heap. No firmware is distributed.

No physical-device test was performed for this patch. These results do not
qualify real SD/FAT failures, multi-file atomicity, power-loss recovery or the
separate UX proposals. They support review of this small correction; they do
not claim merge approval or an official release.
