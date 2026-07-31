# RF-002 — Educational Lifecycle Verification

**Programme:** Release Verification Programme RF-002  
**Phase:** Educational System Acceptance — Phase 1  
**Date:** 2026-07-31  
**Authority:** RF-001 PASS · BF-001 PASS · RF-001A GO WITH ACCEPTED DEBT · SB-001A PASS  
**Method:** Verification only (Flask test client suites + smoke end-to-end; no product redesign)

---

## Core question (this phase)

Can a student begin studying today, continue naturally over time, recover from interruptions, and complete a subject without the Educational Runtime entering an inconsistent state?

**Answer on the RF-002 candidate:** **Yes** — for the Runtime A (JSON-bundled) happy path that SB-001A ships as the primary student origin. Transitions are gated; Baseline is required before Home; Twin birth precedes plan creation; history is not destroyed by Baseline restart.

---

## Lifecycle diagram

```text
Student account (admin/startup; no public registration)
        ↓
Login
        ↓
Exam Selection          /study-plan/wizard/1
        ↓
Exam Date               /study-plan/wizard/2
        ↓
Availability            /study-plan/wizard/3
        ↓
SB-001 Baseline         /baseline  (6 progressive steps)
  Experience → Position → Exam history → Objective → Confidence → Confirm
        ↓
Digital Twin Birth      BaselineFinalizeCoordinator → BaselineTwinBirth
        ↓
Study Plan / Runtime Entry
  Runtime A: StudyPlanService.create_study_plan
  Runtime C: FounderStudentEnrolmentBridge.enrol (thin bridge)
        ↓
Dashboard / Home        /student/   (Baseline gate)
        ↓
Today's Mission         Home / mission handoff
        ↓
Study Session           /session/*  (pause / resume / activity)
        ↓
Reflection              session reflection + decision journal
        ↓
Completion              session complete → Sitting Report / summary
        ↓
Revision                /student/revision
        ↓
Return Tomorrow         Home mission generation (no duplicate active mission)
        ↓
Continue Study          open-session resume + retained topic progress
        ↓
Subject Completion      plan lifecycle / mission completion invariants
```

---

## Transition verification

| # | Transition | Result | Evidence |
|---|------------|--------|----------|
| 1 | Login → exam path | **PASS** | Auth + wizard smoke; no public registration by design |
| 2 | Exam Selection → Exam Date | **PASS** | `tests/test_smoke.py` wizard; PX-002 route suite |
| 3 | Exam Date → Availability | **PASS** | Same |
| 4 | Availability → Baseline | **PASS** | `test_availability_redirects_to_baseline`; wizard step 4 → `/baseline` |
| 5 | Baseline progressive capture | **PASS** | `test_progressive_experience_step`; autosave per step |
| 6 | Confirm → Twin birth | **PASS** | Finalize coordinator births Twin before plan/enrol |
| 7 | Twin → Study Plan (Runtime A) | **PASS** | `test_runtime_a_finalize_creates_plan`; smoke one active plan |
| 8 | Twin → Runtime C enrol | **PASS** | Bridge ordering spy: enrol only after Baseline ready |
| 9 | Entry → Dashboard | **PASS** | Home reachable; no “Baseline 1 of 6” re-ask |
| 10 | Dashboard → Mission / Session | **PASS** | RF-001A student ops + session ownership/regression (majority) |
| 11 | Session → Reflection → Completion | **PASS*** | Session happy-path substance retained; finish lands on Sitting Report (intentional RC-002) |
| 12 | Completion → Revision / History | **PASS** | History / revision surfaces 200 in smoke + RF-001A ops |
| 13 | Return tomorrow / continue | **PASS** | Mission duplicate validator; open-session resume; MissionAlreadyCompleted |
| 14 | Logout / login continuity | **PASS** | Baseline + plan + Twin pointer survive (service + smoke persistence) |

\*Presentation tests that assert finish → `/student` remain red; product correctly lands on `/session/.../summary` (RF-001A Category D debt — not an educational state defect).

---

## Manual intervention

**None required** on the verified candidate path. Wizard → Baseline → finalize → Home is fully automated. Founder intervention is optional (inspect / reset) and does not delete study history.

---

## Educational judgement

The learner is met once at Baseline, then guided forward. The system does not force a second intake questionnaire after entry. Progress artefacts (attempts, plans, Twin snapshots) are retained across Baseline restart. That is the educational continuity the Head of Education requires for G1 validation of the candidate.

---

## Known educational caveats (not lifecycle blockers)

1. **Live production** still serves RF-001 tip (`e4d5a1b`) without `/baseline` — Founder Validation on live must wait for cutover (see Deployment Verification).
2. **Runtime C Twin birth** may honestly skip when curriculum id cannot be resolved; enrolment and Baseline still complete (thin-bridge debt).
3. **Baseline Home gate** is plan-centric; Runtime-C-only enrolments rely on finalize-before-Home ordering rather than the same gate.
