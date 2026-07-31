# PX-002 — Micro-interaction Report

**Programme:** PX-002 Founder Console Experience Elevation  
**Date:** 2026-07-31

---

## Interactions reviewed

| Interaction | Status | Notes |
|-------------|--------|-------|
| Mobile nav toggle / backdrop / Escape | Intact | Existing console shell behaviour |
| Focus trap while nav open | Intact | Sidebar Tab cycle |
| Nav hover / active / focus-visible | Polished | Transition + existing outline |
| Feedback inbox item hover / selected / focus | Polished | Transition + focus-visible |
| Filters disclosure | Added | `<details>` summary with marker + focus ring |
| Patterns disclosure (Check-in) | Added | Collapses Insight engine without removing content |
| Flash dismiss (Close) | Intact | Shared flash partial |
| Doc upload toasts | Intact | Existing toast styles |
| Buttons / dropdowns (forms) | Intact | Bootstrap + DS buttons; no behaviour change |
| Success messaging / redirects | Intact | No workflow changes |
| Loading states | Unchanged | No new async surfaces |

---

## Intentional motion

- Nav link background/colour 150ms ease
- Inbox border/background 150ms ease
- Disclosure chevron rotate 150ms
- All gated by `prefers-reduced-motion: reduce`

---

## Completeness checklist

- [x] Modal / overlay dismissal (nav backdrop, Escape)
- [x] Toast behaviour (existing upload toasts)
- [x] Close buttons (flash stack)
- [x] Hover states (nav, inbox, settings links)
- [x] Focus states (nav, disclosure, inbox, search)
- [x] Button hierarchy (primary Create / Apply vs ghost)
- [x] Keyboard (disclosure native; nav trap)
- [x] Error empty states (No matches / No submissions)

---

## Remaining interaction debt

- No dedicated loading skeletons on Founder list pages (server-rendered; acceptable)
- Check-in action buttons lack progressive grouping (all remain visible — workflow requirement)
- Some legacy command-card pages lack the newer disclosure pattern
