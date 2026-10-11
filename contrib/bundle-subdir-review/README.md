# Bundle subdirectory checks for PR #3877

This small patch applies to jadehawk's PR #3877 at
44626dd5bcc289b0c6b4a0615232e74e1a1d2a8e. It keeps that PR's installer,
discovery order and ownership. It is supporting material, not a replacement PR.

The bundle method currently accepts `.` as a subdirectory, which resolves to
the selected root. It also accepts backslashes. The patch rejects both before
directory creation or downloading and logs the existing error return without
printing catalog-controlled content. Existing nested paths using `/` remain
supported. No new helper, task, allocation or persistent setting is added.

## Run the regression

Requirements: Git, Python 3 and a C++20 compiler with ASan/UBSan. From this folder:

```sh
python3 reproduce.py ../bundle-review
```

Use a new destination. The script fetches the pinned public CP and GoogleTest
sources, runs the unpatched case, applies the small patch, and runs it again.
The first run must fail only `InvalidSubdirectoriesDoNotWrite`; the patched
run must pass all 11 tests. An expected red test in the first run is the
negative control. No SDK checkout or firmware build is required for these tests.

The harness compiles the actual `downloadBundle` body and `PluginLocations.cpp`.
Storage and downloads use host stubs. Coverage includes all nine combinations
of plugin roots, nested and non-plugin bundles, retained grant/config files,
cancelled/failed downloads, disabled plugins and quarantine discovery.
Invalid subdirectories must cause no download or storage mutation.

These tests do not qualify FAT/SD failure behavior or make multi-file replacement
atomic. Replacement failure midway through a bundle remains a separate known
limitation. No device test or full installer acceptance is claimed here.

CrossPoint's license is included. GoogleTest is fetched from its public revision
with its own license. AI tools assisted the patch, test harness and review.
