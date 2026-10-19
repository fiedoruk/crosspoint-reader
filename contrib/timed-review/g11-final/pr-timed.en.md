## Summary

Use one timer owner for Off, local wallpaper rotation or one SD-plugin refresh.
A qualified timer boot reads only the required settings, selects the source,
performs its bounded work and returns to sleep. Ordinary reading does not run
this path. Power takes precedence and returns through normal reader wake
handling without rewriting book progress during autonomous selection.

A reader left on a desk can show current information and still behave like a
reader when picked up. The shared mechanism keeps scheduling, Power handling
and last-good image behavior out of individual SD plugins.

## Scope Check

- [x] Read SCOPE.md and ROADMAP.md.
- [x] No theme, interactive app, browser or service-specific connector.
- [x] Reuses kivarun's timer, jadehawk's Local work and the existing verified transport.
- [ ] Maintainer acceptance of the autonomous network consumer, settings contract
      and HAL integration is still required.

This is a dependent candidate after W06 and #3820 at 1bc4975. It does not ask
the timer PR to absorb the network consumer. The network prototype is limited
to Sticky, X4 Pro and PaperMono; an unsupported model or missing/conflicting
configuration keeps Plugin refresh off. The source defaults to Off. An older
saved local interval migrates to Local only if the source field is absent.

## Behavior and validation

The Local renderer keeps its Bitmap off the small call stack using the existing
checked allocation helper. Allocation failure leaves the panel and reader state
untouched; the temporary object is released before its file handle.

Local uses the existing Custom BMP renderer without Wi-Fi or saved wallpaper
history updates during autonomous wake. Plugin uses one verified `sleep.timer`
handler: fetch a staged BMP, validate/decode before replacing last-good, transfer
the panel, rearm and sleep. Failure never switches to a different source.
Power capture, a 20% network-source battery threshold and fail-closed arm/returned
shutdown handling are shared with the previously tested integration.

Host checks cover source/settings parsing, actual boot orchestration, GPIO and
PMIC capture, RTC/arm/cancel, Off, USB cold-start rearm, Local state preservation
and four real TLS-to-BMP cases. Exact results and build figures are in
VALIDATION.md. Hardware results for an earlier Sticky image are historical;
they do not qualify this revision or another model.

The interval is sleep time; boot, fetch and panel work add to the cycle.
Cancellation budgets are cooperative. A later pass of the existing grayscale
renderer can leave its completed monochrome base. SD power-loss durability,
physical Power timing on every blocking boundary and battery lifetime are not
claimed. SDK verification and official release remain separate gates.

### AI Usage

**YES.** AI assistance was used for implementation, review and this description.
