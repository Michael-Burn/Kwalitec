# PX-003 — Regression Report

**Programme:** PX-003 Phase 1  
**Date:** 2026-08-04  

## Suites executed

| Suite | Result |
|-------|--------|
| `tests/application/educational_packages/test_px003_phase1_trust_revision.py` | **14 passed** |
| `tests/presentation/session/test_px003_session_workflow.py` | **4 passed** |
| `tests/application/educational_packages/test_ro1r1_tomorrow_chrome.py` | **7 passed** |
| `tests/application/educational_packages/test_pb002_package_selection.py` | **32 passed** |
| `tests/application/educational_packages/` (full) + session matrix + cq002 + view_models + kwp005 + sr002 | **207 passed** |
| `tests/presentation/student/test_cq003_daily_habit_fit.py` + `test_dx006b_student_home.py` + `test_cq005_guidance_trust.py` | **26 passed** (verb assertions updated to canonical **Continue**) |
| Captured Phase 1 pack | `knowledge/evidence/releases/PX003/regression/pytest_phase1.txt` — **80 passed** |

## Educational / recommendation integrity

- No educational package JSON edits  
- Package selection chain tests (including Rho → CR-R1) green  
- RO1-R1 tomorrow chrome tests green  
- Session spine / Sitting Report tests green  

## Known test updates (intentional)

String-pinned Home resume CTAs updated from `Continue Session` → `Continue` (PX-B-034).

## Not run in this exit

- Full `tests/` monolith wall-clock suite  
- LIVE PB-017 Rho force-R1 cohort re-simulation (residual — see residual register)  
- Device / axe / Lighthouse (WS-05 / WS-06)
