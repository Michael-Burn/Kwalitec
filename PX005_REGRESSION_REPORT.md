# PX-005 — Regression Report

**Programme:** PX-005 Phase 3 (WS-07 · WS-08)  
**Date:** 2026-08-04  
**Evidence log:** `knowledge/evidence/releases/PX005/regression/pytest_phase3.txt`

## Headline

**204 passed** in the Phase 3 evidence pack.

## Suites included

| Suite | Role |
|-------|------|
| `test_px005_phase3_microcopy_reliability.py` | WS-07/08 contracts |
| `test_px004_phase2_home_mobile_a11y.py` | Phase 2 home/mobile/a11y guard |
| `test_px003_phase1_trust_revision.py` | Phase 1 trust/revision guard |
| `test_px003_session_workflow.py` | Session workflow guard |
| `test_px001_brand_identity.py` | Brand descriptor |
| `test_iahf004b_brand_experience.py` | Shell identity |
| `test_rr001b_internal_alpha_onboarding.py` | Login welcome copy |
| LXP-002 / LXP-003 / LXP-004 | Session / practice / feedback |
| `test_ptp002_single_source_of_truth.py` | Closure path |
| Student + session accessibility | A11y sanity |
| `test_rc001_contrast.py` | Contrast |
| `test_dx006b_student_home.py` | Home |
| `test_rip001_daily_checkin.py` | Product Check-in entry |

## Reliability / recovery

| Check | Result |
|-------|--------|
| Continue contention flash present | Pass (static + message constants) |
| Resume optimistic-lock retry | Pass (coordinator contract) |
| Campaign stale-package retire (PX-B-006) | Pass (service contract) |
| Session error boundary | Pass (routes contract) |
| LIVE parallel contention re-measure | Residual PX5-R2 |

## Session recovery / error handling

Calm `continue_contention` flash → Home; infra failures not scored as educational. Generic 500 path retained for non-contention bugs.

## Accessibility sanity

Student + session accessibility suites green in pack. Copy changes preserve meaningful labels.

## Educational regression

No educational package JSON modified. Selection ranking policy unchanged. PX-B-006 is timing/invalidation of mismatched persisted missions only.

## Known flakes / residuals

String-pinned legacy LXP assertions updated for “Finish Session” (PX-003) and Practice results (PX-005). RIP-001 sidebar Check-in assertion redirected to Profile/Settings under sole-runtime nav.
