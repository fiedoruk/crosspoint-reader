The W06/TIMED series now replays on CP `91ed3ef8` / SDK `f9cc1bed`. The compatibility
change moves the two timer settings into upstream's visitor and uses StaticEnum
for their immutable labels. It keeps the same keys/values and preserves the
memory-saving persistence path. CMake keeps the newer upstream registration.

The focused host checks cover source/interval round trips, migration, invalid
values and excluded boards, with the recorded Release/CTest and final C3 build
results in VALIDATION.md. Earlier device and TLS evidence keeps its original pin.
The SDK verification patch is unchanged; API/ref, physical C3 memory and consumer
scope still require their own decisions.

This lets us maintain one idle-screen consumer through normal reader changes,
with shared transport and timer behavior for SD plugins. It does not add a
service-specific connector or another scheduler.
