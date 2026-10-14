# Read plugin details before installing

Selecting a bundle from a catalog targeting a plugin root opens its title, optional version and supplied description in the existing paged text viewer. Install/Update explicitly starts the existing download; Back cancels. The opening button release cannot also accept the details. Books, folders, dictionary definitions, clippings and README views retain their existing behavior.

## Source and reproduction

CP PR #3877 by jadehawk, commit `5e8b503f4ddefe94abe90b3b67ec3812b9a8273f`, SDK `7fcd3b34c108f28c086ade3b433924022dbc0998`.
Apply ux1.patch first, then ux2.patch. UX1 is an explicit prerequisite of this packet; ux2.patch is only the details delta. The separate root-normalization correction is not a hidden prerequisite.
This is support for the existing work, not a replacement plugin framework.

Requirements: Git, Python 3, a C++20 compiler with AddressSanitizer/UndefinedBehaviorSanitizer.
GoogleTest is pinned to `52eb8108c5bdec04579160ae17225d66034bd723`. No firmware build or device operation runs in this command:

```sh
python3 reproduce.py /tmp/cp-ux2-review
```

The destination must not exist. The script fetches the exact public refs, checks
packet hashes, applies the ordered patches and runs the host cases. Optional
`--cp-cache`, `--sdk-cache` and `--gtest-cache` use existing Git object stores;
the pinned commits and resulting file hashes are still verified. No reset or
write to those caches occurs. The receipt records which transport was used.

See [VALIDATION.md](VALIDATION.md) for measured evidence and its limits.
CrossPoint notices are preserved. Scoped Sticky observations are in [DEVICE.md](DEVICE.md).
