# PX-007 — Accessibility verification

**Date:** 2026-08-04  
**Claim rule:** No WCAG conformance level asserted.

## Automated (green in aggregate)

| Suite | Role |
|-------|------|
| `tests/presentation/student/test_accessibility.py` | Student a11y |
| `tests/presentation/session/test_accessibility.py` | Session a11y |
| `tests/test_rc001_contrast.py` | Contrast |
| PX-004 phase 2 a11y contracts | Focus / touch / reduced-motion |

## Contracts verified

- Skip link on student shell  
- `:focus-visible` discipline  
- `prefers-reduced-motion` honours house motions + skeletons  
- Session timer polite live region  
- Confirm modal resilience pattern  
- Touch targets ≥44px token  

## Residuals

| ID | Item |
|----|------|
| PX4-R2 / PX7-R3 | axe/Lighthouse CI gate |
| PX4-R3 / PX7-R4 | Recorded VoiceOver or NVDA pass |
