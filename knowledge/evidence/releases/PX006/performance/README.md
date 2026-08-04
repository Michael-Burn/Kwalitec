# PX-006 — Performance measurements (WS-09)

**Date:** 2026-08-04  
**Scope:** Local static asset hygiene on sole-runtime student shell. Not a LIVE Core Web Vitals claim.

## Local asset baseline (bytes)

| Asset | Bytes |
|-------|------:|
| `css/tokens.css` | 12,016 |
| `css/student/student.css` | 46,466 |
| `css/design_system.css` | 39,750 |
| `css/app.css` | 67,206 |
| `css/brand.css` | 2,436 |
| `css/fonts.css` | 1,624 |
| `js/student.js` | 5,814 |
| `js/theme.js` | 6,139 |
| `js/app.js` | 8,809 |
| `js/confirm-modal.js` | 2,658 |
| **Listed total** | **192,918** |

Bootstrap CSS/JS remain CDN (not in local total).

## Interventions (PX-B-031)

1. Defer Bootstrap JS, `app.js`, `confirm-modal.js`, `student.js` on `eos_student.html` — unblocks first paint of student chrome.  
2. Optimistic `data-nav-pending` extended to primary CTAs (`ds-btn--primary`, `data-student-cta`) — perceived immediacy on Home → Mission/Plan.  
3. Session path continues to omit `app.css` (uses `design_system.css` only).  
4. Soft CSS budget guard in automated tests (`student.css` + `tokens.css` < 450 KB).

## Loading honesty (PX-B-032)

| Surface | Craft |
|---------|-------|
| Home quiet/preparing | `skeleton_student_home` + support copy |
| Mission / Session | `skeleton_mission_hero` + `data-px006="mission-surface"` |
| Study Plan | `skeleton_study_plan` ref + plan surface markers |
| Nav transitions | `skeleton_nav_pending` revealed under `body[data-nav-pending]` |

Reduced motion: skeleton pulse and nav opacity transitions disabled under `prefers-reduced-motion`.

## Core Web Vitals

**Not measured on LIVE this exit.** Residual **PX6-R2** — Founder/ops Lighthouse or CrUX when capacity allows. Local claims limited to asset hygiene + loading craft.

## Known limitations

- CDN Bootstrap still dominates transfer on cold path.  
- Study Plan empty-state skeleton is reference-wired (SSR empty is a real empty state; nav-pending covers transitions).  
- No claim of Target PF-1 on production broadband without field evidence.
