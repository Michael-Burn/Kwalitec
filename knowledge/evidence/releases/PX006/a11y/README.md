# PX-006 — Accessibility notes (performance / moments)

**Dependency:** WS-06 reduced-motion (PX-B-027) held.

| Check | Result |
|-------|--------|
| Skeleton `role="status"` / `aria-busy` | Present on macros |
| Nav skeleton polite status | Present |
| Appearance saved live region | `#appearance-saved-live` / student live region |
| Icon-only controls ≥ touch target | `.icon-btn` + `--touch-target-min` |
| Error Reference ID readable | Tokenised secondary colour + guidance |
| Reduced motion on house motions | Pass (CSS) |
| axe CI / AT recording | Residual carry PX4-R2 / PX4-R3 |

No WCAG conformance level claimed.
