# Keep bundle updates in place with repeated trailing separators

On PR #3877 at `5e8b503f`, a manifest destination such as
`/.crosspoint/plugins///` bypasses the existing-installation lookup. With `foo`
already in `/plugins/foo`, an update creates another copy under
`/.crosspoint/plugins/foo`. Discovery then prefers that new copy, leaving the
original grant/configuration in the shadowed directory.

The bundle path removes only one trailing slash before checking whether the
root is a plugin root. User configuration overrides already strip every trailing
slash; an absolute `download.dest_dir` from a manifest reaches this method
unchanged. The patch uses the same bounded normalization at the bundle boundary:
one `if` becomes `while`. Discovery order, nested bundles, validation, staging
and file replacement are unchanged. There is no new helper, setting or SDK change.

## Reproduce

Requirements: Python 3, Git and a C++20 compiler with ASan/UBSan. From this folder:

```sh
python3 reproduce.py ../bundle-root-check
```

The destination must not exist. The script fetches pinned public CP and
GoogleTest refs, verifies packet hashes, runs the actual bundle/discovery code
with host storage/download stubs, applies the patch and runs it again. The raw
CP run must fail only `RepeatedTrailingSlashesStillUpdateInstalledPlugin`;
the patched run must pass all 12 cases. This includes the nine combinations of
plugin roots, private files, failed/cancelled downloads and invalid subdirectories.
No SDK checkout, firmware build, upload or CI is run by the reproducer.

These tests do not establish real FAT/SD atomicity, device behavior or complete
installer acceptance. Multi-file replacement failures remain a separate
limitation. The existing installer and directory-reuse design remain jadehawk's
work; this is a narrow follow-up to our earlier support. CrossPoint's license is
included, and fetched GoogleTest keeps its own license. AI tools assisted the
regression, correction and review notes.
