# Checked SD shutdown and TIMED Power handoff

The manifest pins CrossPoint 8ee47c4d and its SDK gitlink 77ae8c75.
Both routes include the verified transport overlay on that SDK revision.
The W06 route ends after event verification. The full route also includes
the dependent timer, Local and Plugin consumers, and host regression tests.

A TIMED wake can capture Power before the reader starts polling foreground
input. The integration retains the verified hold and lets the upstream
Power classifier own subsequent releases and fresh clicks. When SD sync
fails, the storage HAL makes one more attempt after 20 ms. A second failure
leaves the card mounted. Panel teardown, timer arming and sleep then stop.
An ordinary sleep refusal restores the open book or Home. An unattended
timer refusal boots to Home. A captured, accepted Power gesture resumes
through normal foreground handling.

A timed Local grayscale refresh decodes both gray planes to temporary PSRAM
and decodes the monochrome base before transfer. For an 800 × 480 panel the
temporary allocation is 96,000 bytes. When those planes cannot be allocated,
a complete monochrome decode can still be shown. An SD read error during
staging leaves the previous displayed image in place. Plugin delivery keeps
the checked file replacement and synchronous transfer. A later hardware
transfer fault and a power loss during SD replacement have separate failure
semantics.

Run the following from the packet directory with Python 3, Git, a C++20 host
compiler and the ArduinoJson headers used by the firmware. Use an empty
destination for each replay.

```sh
python3 replay.py /tmp/cp-w06 --through w06
python3 /tmp/cp-w06/test/plugin_verified_http/run.py --arduinojson /path/to/ArduinoJson/src --sanitize

python3 replay.py /tmp/cp-timed --through timed
export CROSSPOINT_ARDUINOJSON_INCLUDE=/path/to/ArduinoJson/src
python3 test-sd.py --cp /tmp/cp-timed
python3 /tmp/cp-timed/test/test_remote_button_input.py
python3 /tmp/cp-timed/test/timed_wake_guard/run.py --sanitize
python3 /tmp/cp-timed/test/timed_sync/run.py --sanitize
python3 /tmp/cp-timed/test/timed_sync/run.py --sanitize --usb-only
python3 /tmp/cp-timed/test/timed_local/run.py
```

Picking up a reader during a background refresh should resume reading at the
saved place. The host tests use controlled SD, Power and display boundaries.
P8's physical result belongs to its recorded earlier binary. Physical gesture
timing, panel quality, C3 heap and the energy cost of recovery remain open.

Timer credit belongs to kivarun. The Local refresh work retains its upstream
credits, including jadehawk. The SDK overlay builds on SDK #65 and retains
jpirnay's contribution to retry classification. AI tools assisted integration
and testing. CP and SDK license notices accompany the source patches.
