# PX-004 — Regression Report

**Programme:** PX-004 Phase 2  
**Date:** 2026-08-04  
**Log:** `knowledge/evidence/releases/PX004/regression/pytest_phase2.txt`

## Suites executed

| Suite | Result |
|-------|--------|
| `tests/presentation/student/test_px004_phase2_home_mobile_a11y.py` | Pass |
| `tests/test_rc001_contrast.py` | Pass |
| `tests/presentation/student/test_templates.py` | Pass |
| `tests/presentation/student/test_accessibility.py` | Pass |
| `tests/presentation/student/test_responsive.py` | Pass |
| `tests/presentation/test_sop001_student_os.py` | Pass |
| `tests/presentation/session/test_px003_session_workflow.py` | Pass |
| `tests/presentation/session/test_accessibility.py` | Pass |
| `tests/application/educational_packages/test_px003_phase1_trust_revision.py` | Pass |

**Total:** **153 passed**

## Verification classes

| Class | Outcome |
|-------|---------|
| Existing regression | Pass (templates, SOP-001, PX-003 trust/session) |
| Accessibility | Pass (expanded Phase 2 + contrast) |
| Mobile | Pass (nav markers + CSS breakpoints); live PNG residual |
| Responsive layout | Pass (`test_responsive.py`) |
| Cross-browser | Sanity via Bootstrap/student shell markers — full matrix residual |
| Performance sanity | No new assets; notes in evidence/performance |
| Educational regression | PX-003 package chrome suite Pass; bodies unmodified |

## Educational / recommendation regression

- No package JSON edits  
- No selection / ranking / Twin / Runtime authority edits  
- Force-R1 / continuity regenerate code paths untouched this phase  

## Failures resolved during exit

| Issue | Resolution |
|-------|------------|
| Responsive `student-page-title` on Home/Settings | Added class to greeting / Settings h1 |
| SOP-001 Progress assertion with folded strip | Progress disclosure remains in DOM when signals exist |
| A11y “Start” CTA string | Accept Start/Continue/primary CTA (PX-003 verbs) |
| Session “Technical details” hard-code | Assert dynamic `ds_disclosure` / `item.title` |
