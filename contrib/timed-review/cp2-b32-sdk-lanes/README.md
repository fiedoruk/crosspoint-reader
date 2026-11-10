# W06 and TIMED: dependent compatibility packet

This is local integration material, not an official release or a standalone plugin. CrossPoint `b32f907e5b6bcdaf80dad5b2fb52a3b3ef869802` already contains the earlier token-storage prerequisite; it is intentionally not reapplied. Five existing patches follow, then the distinct published P1 Wi-Fi fallback overlay and its tests. The last-used saved credential has priority; if absent or empty, one attempt uses the first saved entry. No scanning or subsequent retry is added.

Both lanes require proposed, unmerged verification changes. `official-pin` means CP's existing SDK gitlink `6a208c0c46cce99bafa334bc4f171f5e558c5195` plus that patch; it does not mean verified transport is an official feature. `future-qualification` checks SDK `5f0d52196a770947f7f27f15701c2b1430569697` with the adapted patch. CP's gitlink remains `6a208c0c` even in this lane: the actual nested SDK HEAD differs and a dirty submodule is expected in both lanes. No CP dependency pin is updated. The future header keeps upstream streaming `BodyReader`, the response-header budget, deadline and abort logic.

## Replay

Requires Git and Python 3. Supply a fresh destination. Public pinned objects are fetched by default; local mirrors may be supplied via `--cp-source` and `--sdk-source`.

```sh
python3 replay.py /tmp/w06 --lane official-pin --through w06
python3 replay.py /tmp/timed-pin --lane official-pin
python3 replay.py /tmp/timed-future --lane future-qualification
```

`--through w04`, `prerequisites`, `w06` and `timed` stop before the final P1 overlay. In particular W06 alone does not include P1's ordinary-sleep Wi-Fi fallback. The default `p1` is the full TIMED integration plus P1 and its tests. Stage tree IDs and patch SHA-256 are in `manifest.json`; replay checks each. No build, flash, commit, push or CI is started.

HOST fixtures do not establish a physical device, runtime memory, reading, Power recovery, radio, RTC or panel result. Cancellation and deadline checks are cooperative; DNS/TCP can block. No new TLS 1.3 MFL or constrained runtime-heap qualification is claimed for these exact revisions; earlier G12 results remain separate dated evidence. Upstream acceptance, device qualification and release remain separate. Timer authorship remains Michael Kazakov/kivarun; local refresh builds on jadehawk's work and the PaperMono path on FreeInk RTC/PMIC work. SDK verification reuses proposed #65. Licenses and notice accompany this packet. AI assistance was used.

See `VALIDATION.md` for commands, the old-pin negative control and the exact evidence boundaries. The 64-field and complete response-header accounting hardening is supplied by future SDK `5f0d` only; the official-pin lane retains the older parser.


The final future-qualification full P1 stage passed one C3/default firmware build
at CP tree `22c67de7a62e37a02bf43263bc6413fc95c91336` and SDK tree
`942814decb094f492771ce63aed20161dcd1c7e3`. The official-pin lane and standalone
W06 stage were not separately firmware-built in this update. See `BUILD.json`.
Four independent source-review axes completed; a stale Wi-Fi selection paragraph
was corrected in the final P1 documentation stage, without a firmware-code change.


Earlier material remains available at the immutable
[CP36bd packet](https://github.com/fiedoruk/crosspoint-reader/tree/8b4d847e8419abf3600b46661b8d3d8c07339983/contrib/timed-review/cp2-36bd)
and [Wi-Fi fallback support for garciacd's #3867](https://github.com/fiedoruk/crosspoint-reader/tree/638d919d1d0c905e3ccefa0a838275e175491b3f/contrib/timed-review/p1-wifi-3867).
Those dated results are preserved, not reassigned to the new firmware or SDK.
