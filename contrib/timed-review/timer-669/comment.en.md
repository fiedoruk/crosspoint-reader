@kivarun, thanks for preserving the second argument's held-button meaning.
The separate TIMED consumer now follows `669642d2`: held-button second,
interval third, with its existing recovery context fourth. I also checked
`a38095cf`; its source tree is identical.

The O142 regression checks remain: timer plus held button, and the actual
interval and flags passed during rearm. This keeps the compatibility fix
without losing that coverage. The consumer remains separate from your timer PR.

Our aim is useful information on an idle reader, configured through SD, while
normal reading and Power recovery keep their behavior. The packet records
exact refs and validation; SDK acceptance and hardware qualification remain open.
