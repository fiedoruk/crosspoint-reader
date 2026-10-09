# Verified plugin HTTP and a timed SD consumer — review material

This is source material for two separate proposed CP changes, not a firmware
release or a request to add the full consumer to the timer primitive PR.

- W06.diff: 37 owned CP paths after the checked-BMP and event-budget changes
  in PR #3907 and PR #3908. It adds verified requests/downloads/auth using the
  separately proposed SDK capability contract.
- TIMED.diff: 38 owned CP paths after W06, PR #3820's timer and PR #3916's bundle
  installation behavior. The original timer remains Michael Kazakov's
  (@kivarun) work; SDK verification retains Sameh Foulad's (@sfoulad) credit.
- source-review.zip: the complete reproducible series, pinned public refs,
  tests, English facts, validation notes and CP/SDK licenses/notices.
  Extract it and use its README/reproduce.py. No private base is required.
- DEVICE-NOTES.en.md: limited automated X4 Pro bench observations, separated
  by image hash and not presented as hardware acceptance of this new build.

The qualified CP base is 3a03be8902479c4240f083aec4e7f61562a4beb2; its SDK pin
remains 425d200a8ea447326b4b9696e4e47dc84ad9d7f6. Both own diffs need their
prerequisites and do not apply to raw develop alone. The full composed source
reconstructed from public refs and built once for X4 Pro in 75.807 seconds,
with two compile jobs and no retry. The compiled SDK capability is active
only with the explicit proposal included in the series.

## Status addendum — 9 October 2026

The author has now acknowledged the architecture and maintenance ownership.
This supersedes the pending ownership wording in the earlier source ZIP.
The SDK API/ref is still proposed. CP's periodic networking/HAL scope decision,
prerequisite integration, human-written PR description, required hardware
acceptance, energy, C3 heap and other models remain separate open gates.

The caller is limited in source to X4 Pro and Sticky; the bench evidence is
X4 Pro only. PaperMono is excluded. The consumer is opt-in, uses one SD-owned
handler and preserves the normal
reader path. SCOPE.md's active-connectivity restriction and ROADMAP.md's SD
plugin direction still need a maintainer decision for this periodic route.
Existing sleep.enter and the timer author's acknowledgment do not settle it.

These files contain no account system, service implementation, renderer,
image templates, firmware binary, private bench harness or raw device logs.
CP-derived diffs retain LICENSE-CP; the ZIP retains SDK notices and licenses.
AI tools assisted implementation, tests, review, packaging and these notes.
