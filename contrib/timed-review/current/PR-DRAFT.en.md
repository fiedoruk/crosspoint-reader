# Add an opt-in timer consumer for SD sleep images

An installed SD plugin can select a verified native-size sleep image and a local
polling interval. On a qualified timer wake, the reader fetches and decodes that
image, updates the panel and returns to sleep. A failed download or invalid BMP
preserves the last-good image; Power takeover follows the existing reader path.

The consumer handles Sticky, X4 Pro and PaperMono through their existing HAL
routes. On cold timer boot it restores only the global plugin permission before
discovery, preserving explicit disable, legacy detection and installation
quarantine without loading or resaving general reader settings. Timed work does
not drain reading outboxes or change book position.

Review patch 07 contains the consumer. The package separately identifies token
storage, BMP/budget, verified transport, SDK and timer prerequisites. It is based
on #3877 at `fc3aed12`; it must target accepted dependency refs before becoming a
clean develop PR. The timer, installer and original SDK verification remain
credited to their authors.

Validation: host sanitizer suites cover selection, budgets, image handling,
permission and Power/sleep routing; actual verified HTTP has loopback TLS evidence.
The final source matches the recorded Sticky build, and the ordered public series
is replayed in a fresh directory. New-binary device acceptance, runtime heap and
energy remain unmeasured. Historical scoped bench results do not qualify this
exact binary or all three models. Native portrait/BW is the current rendering
contract. Cache/304 and remotely suggested cadence are separate follow-ups.

AI tools assisted implementation, tests and documentation.
