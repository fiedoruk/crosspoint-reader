This updates the verified-download material to the pinned CP/SDK base, including the revised token-storage path in [CrossPoint #3956](https://github.com/crosspoint-reader/crosspoint-reader/pull/3956). It keeps trust-anchor and hostname verification, fresh time, authentication, bounded attempts and fail-closed behavior in the shared transport.

We want an idle reader to fetch useful information without putting service-specific logic in the firmware. Keeping this capability shared also gives other SD plugins the same verified download path. The proposed SDK API still needs agreement; this is integration evidence, not a replacement for #65 or an official release.

The packet separates W06 from the timer consumer and includes its exact prerequisites, replay commands and scoped test results. Code and tests were developed with AI assistance; the notes distinguish host checks from the tested device image.
