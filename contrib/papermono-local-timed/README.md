# PaperMono local timed refresh and Power handoff

This candidate ports the existing RTC/PMIC adapter to Razor-Crest timedwake-r1 (`59555361`) plus the [Power handoff prerequisite](https://github.com/fiedoruk/crosspoint-reader/tree/3529a9dadea4a93cb9e6e9ef87712331c750d7db/contrib/timed-power-handoff). SDK `7fcd3b34` already includes FreeInk #138 and is unchanged. The timer primitive remains Michael Kazakov's work; local wallpaper rotation remains Jadehawk's work.

It enables the existing Custom sleep-screen refresh on PaperMono with a qualified RTC cold wake, RTC cancellation for Off/error, and PMIC Power capture during maintenance. The SDK abort callback checks Power immediately before its shutdown command. A returned shutdown cancels the RTC route and restarts instead of falling into ESP-only sleep without a button wake source. No network consumer or new RTC driver is added.

The goal is the same reader-first behavior across boards: an idle screen can update, while a request to read takes priority. PaperMono needs its PMIC event latch for this; the GPIO capture used by other boards does not implement that contract.

## Reproduce

Run `python3 replay.py /absolute/path/to/new-receiver` on macOS or Linux with Git, Python3 and a Clang-compatible C++20 compiler supporting ASan/UBSan. The destination must not exist. The script fetches public exact refs and the hash-locked T1 prerequisite, applies this patch, and runs scoped host checks. It does not build firmware, flash, run CI or send data from a reader.

Use the repository's existing PaperMono build environment for firmware, with matching prebuilt `dio_opi` libraries and headers. Confirm PSRAM is available on the device; package version numbers alone do not establish a matching configuration. See NOTES.en.md for dated evidence and remaining device checks. The scoped PaperMono checks are complete; limitations are recorded in NOTES.en.md. This is support for the pinned branch and T1 prerequisite, not a standalone patch for current develop. Source files inherit the included CrossPoint MIT notice.
