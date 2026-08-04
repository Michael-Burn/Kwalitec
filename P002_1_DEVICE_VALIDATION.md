# P-002.1 — Device Validation

**Programme:** P-002.1  
**Date:** 2026-08-04  
**Verdict:** **PASS WITH RESIDUAL**

---

## 1. Scope

Cross-device primary path:

| Form factor | Orientation |
|-------------|-------------|
| Desktop | — |
| Tablet | Portrait / Landscape |
| Mobile | Portrait / Landscape |

Evidence expected: device gallery (PNG / video).

---

## 2. Automated responsive / mobile contracts — PASS

| Suite | Result | Evidence |
|-------|--------|----------|
| `tests/presentation/student/test_responsive.py` | Included in session/nav pack | `regression/pytest_session_nav_a11y.txt` |
| PX-004 mobile drawer + touch targets | Green | `pytest_premium_core.txt` |
| Pattern | Topbar drawer (`D-MOBILE-NAV` provisional) | PX-007 / PX-004 |

Touch token: `--touch-target-min: 2.75rem` (44px) retained.

---

## 3. LIVE device gallery — RESIDUAL

| Item | Status |
|------|--------|
| Phone + tablet screenshot/video gallery | **Not captured this programme** |
| Residual | **P0021-R2** (carry **PX7-R2 / PX4-R1**) |
| Founder PNG gallery (general) | **P0021-R1** (carry **PX7-R1**) |

Code pattern for mobile primary path: **Closed**. Device evidence completes unconditional mobile Target claim language.

---

## 4. Defects

| Class | Count |
|-------|------:|
| Critical device defects | **0** |
| Major device defects | **0** |

---

## 5. Disposition

| Claim | Allowed? |
|-------|----------|
| Mobile primary path contracts held | **Yes** |
| Unconditional multi-device Target without gallery | **No** |
| Premium Experience Conditional PASS (PX-007) | Unchanged — device residual owned |

Signed: P-002.1 Device Validation · 2026-08-04
