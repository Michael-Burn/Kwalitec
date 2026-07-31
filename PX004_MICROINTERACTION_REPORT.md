# PX-004 — Micro-interaction Report

**Programme:** Product Experience Programme PX-004 — Premium Craft & Release Polish  
**Date:** 2026-07-31

---

### Interactions reviewed

| Interaction | Status | Notes |
|-------------|--------|-------|
| Button hover | Polished | All `ds-btn` variants |
| Button active / pressed | Added | Brightness step on primary/secondary/ghost/danger |
| Button disabled | Polished | Opacity + `pointer-events: none` |
| Button busy | Added | `[aria-busy="true"]` wait cursor |
| Console button disabled/busy | Added | Matches DS affordances |
| Input / select focus | Intact | Existing DS focus ring |
| Disclosure focus | Fixed | Valid focus ring via `--focus-ring` |
| Flash appear | Polished | `ds-flash-in`; reduced-motion safe |
| Flash dismiss | Intact | Bootstrap close |
| List row hover (linked) | Added | Colour shift to primary |
| Exam catalogue row hover | Added | Border / surface elevate |
| Nav toggle / Escape | Intact | Prior PX-002 |
| Feedback inbox hover / selected | Intact | Prior PX-002 |
| Upload toasts | Intact | Prior continuity |
| Session timer / focus mode | Intact | Prior PX-003 |

### Motion audit

| Motion | Behaviour | Reduced motion |
|--------|-----------|----------------|
| Flash enter | 250ms ease translateY | `animation: none` |
| Button colour transitions | `--transition-base` | Gated |
| Exam / list hover transitions | `--transition-base` | Gated |
| Curriculum preview rows | Removed speculative `will-change` | N/A |
| Bootstrap `fade` on flash | Retained for dismiss | Acceptable; OS reduce still preferred |

### Completeness checklist

- [x] Hover
- [x] Focus
- [x] Pressed
- [x] Disabled
- [x] Busy / loading affordance
- [x] Success flash
- [x] Warning / error flash
- [x] Disclosure
- [x] Reduced-motion respect

### Remaining interaction debt

1. No skeleton loaders on server-rendered Founder lists (acceptable).
2. No full-page busy overlay on long Studio POSTs (intentionally not added).
3. Check-in multi-action button row still dense (workflow requirement).

### No behavioural changes

State machines, redirects, and form validation rules unchanged. CSS and presentation attributes only.
