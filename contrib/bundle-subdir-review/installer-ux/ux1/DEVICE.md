# Sticky checks — 14 October 2026

CP `5e8b503f4ddefe94abe90b3b67ec3812b9a8273f`, SDK `7fcd3b34c108f28c086ade3b433924022dbc0998`; both UX patches applied.

Scripted input was exercised on one Seeed reTerminal Sticky. The reader used the unchanged production UI, renderer, network and SD paths. Camera observations were checked independently against OCR; bundle contents were read back byte-for-byte.

| Check | Observed result |
| --- | --- |
| Installed picker | OPDS, Hub, then Alpha/beta/Zulu in title order. |
| Return from a catalog | Alpha selection retained after Back, including after a new plugin appeared in the list. |
| Details | Title, version, Polish text and Update visible; page1/6 advanced to2/6 without overlap. A short English description showed Install. |
| Cancellation | Opening details, paging and Back caused no bundle-file request. |
| Explicit Update | Only the subsequent Update action fetched both expected files; the screen reported completion and the updated files matched. |
| Explicit Install | Install fetched both new-plugin files; their contents matched and the new entry appeared in sorted order. |

This covers scripted on-device interaction and the observed panel. It does not qualify the physical touch controller, button-only C3 runtime, RTL, SD fonts, energy use or every device profile. The on-device picker was checked with OPDS visible; host tests also cover the prefix variants.

Test-image SHA256: `735f72898ec79d752367c0d08b9791059d0210a867299284710c4962f7ed7473`.
The device checks used temporary test controls; these are not part of either patch. All test files are removed after the run. The normal combined-patch build is `820befa4fe51ae81159f3f3e3ee4762d7cce27a9bac1b7d4c7f0616e2f8e717d`.

The temporary files were removed and the original plugin-system setting restored. The normal image was restored and verified in flash.
