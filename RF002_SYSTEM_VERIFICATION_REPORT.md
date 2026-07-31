# RF-002 — System Verification Report

**Programme:** Release Verification Programme RF-002  
**Phase:** Educational System Acceptance  
**Date:** 2026-07-31  
**Authority:** RF-001 PASS · BF-001 PASS · RF-001A GO WITH ACCEPTED DEBT · SB-001A PASS  
**Method:** Verification only — no Runtime C / SCI / recommendation / Study Plan / Twin redesign  
**Candidate:** Working tree with SB-001A Baseline integration + BF-001 Studio remediation

---

## Executive summary

RF-002 asked one educational question: **Can a student begin studying today, continue naturally over time, recover from interruptions, and complete a subject without the Educational Runtime entering an inconsistent state?**

On the **candidate build**, the answer is **yes**.

Student Baseline is now the single educational origin. Twin birth precedes Runtime A plan creation and Runtime C enrolment. Neither runtime re-asks onboarding. Study history survives Baseline restart and Founder reset. Mission and plan duplicate guards remain intact. Founder Baseline inspect/reset and Curriculum Studio lifecycle (post BF-001) remain operationally sound.

**Live production** still serves the RF-001 tip (`e4d5a1b`) **without** Baseline (`/baseline` → 404) and without BF-001 Studio JS. Educational continuity claims for Baseline therefore apply to the **candidate**, not yet to live.

**Verdict:** **PASS** (candidate educational system)  
**Recommendation:** **GO FOR G1 FOUNDER VALIDATION** with deployment preconditions (Alembic merge + Manual Deploy of SB-001A/BF-001). See `RF002_RELEASE_RECOMMENDATION.md`.

---

## Core principle judgement

> Every decision made by Kwalitec should reinforce the student's educational continuity.

| Principle test | Holds? |
|----------------|--------|
| Platform remembers where the student is | **Yes** — Baseline + Twin + Study Plan / enrolment |
| Understands where they want to go | **Yes** — objective / confidence captured once |
| Guides without unnecessary repetition | **Yes** — no second questionnaire; resume summary |
| Progress not lost on interruption | **Yes** — attempts, plans, Twin snapshots retained |
| One coherent educational origin | **Yes** — one complete Baseline per user×subject (app-enforced) |

---

## Phase results

| Phase | Focus | Result |
|-------|-------|--------|
| 1 | Educational lifecycle | **PASS** — `RF002_EDUCATIONAL_LIFECYCLE.md` |
| 2 | Baseline paths | **PASS** — all declaration modes verified |
| 3 | Runtime A / C consistency | **PASS** — `RF002_RUNTIME_CONSISTENCY.md` |
| 4 | Digital Twin | **PASS** (A) / conditional TwinAbsent (C) — `RF002_DIGITAL_TWIN_AUDIT.md` |
| 5 | Educational continuity | **PASS** |
| 6 | Founder operations | **PASS** |
| 7 | Deployment | **LIVE HEALTHY; BASELINE NOT CUT OVER** — `RF002_DEPLOYMENT_VERIFICATION.md` |
| 8 | Cross-system integrity | **PASS** on candidate |
| 9 | Educational invariants | **PASS** |
| 10 | Risk review | Complete — `RF002_RISK_REGISTER.md` |

---

## Phase 2 — Baseline path evidence

| Path | Result | Evidence |
|------|--------|----------|
| Brand New Student | **PASS** | Finalize → not_started stage; Twin FIRST_TIME posture |
| Started / Halfway / Mostly done | **PASS** | Mapper experience → position |
| Revision Student | **PASS** | Stage revising |
| Continue From Topic | **PASS** | `curriculum_topic_code` set; prior topics seeded |
| Restart From Beginning | **PASS** | Objective restart clears topics |
| Recommend Starting Point | **PASS** | Maps to structural FIRST_SIT default |
| Returning resume | **PASS** | No re-ask; restart CTA |
| Twin initialises | **PASS** (A) | Birth before plan |
| Study Plan respects Baseline | **PASS** | Plan fields from mapper |
| Dashboard respects Baseline | **PASS** | Home gate + no questionnaire |
| Mission generation respects Baseline | **PASS** | Entry after plan/enrol from Baseline posture |

Suites: `tests/application/student_baseline/`, `tests/presentation/student_baseline/`, SB-001A regression matrix reconfirmed.

---

## Phase 5 — Continuity evidence

| Check | Result |
|-------|--------|
| Leave mid-session / resume | **PASS** — session ownership + open-session idempotency |
| Return tomorrow | **PASS** — MissionAlreadyCompleted; no duplicate active mission |
| Current topic retained | **PASS** — plan topic + Twin knowledge priors |
| Progress retained | **PASS** — TopicProgress / StudyAttempt survive Baseline restart |
| Reflection / analytics retained | **PASS** — history-safe supersede; continuity service on plan delete |
| No duplicated missions | **PASS** — mission validators |
| No duplicated study plans | **PASS** — deactivate prior actives on create; smoke asserts one active |

Known residual: presentation tests asserting finish → `/student` (product → Sitting Report) — Category D, not continuity loss.

---

## Phase 6 — Founder verification

| Capability | Result | Evidence |
|------------|--------|----------|
| Inspect Baseline | **PASS** | `/founder/participants/<id>/baseline` |
| Reset Baseline | **PASS** | Supersede; StudyPlan intact (`test_founder_reset_does_not_delete_plan`) |
| Inspect Twin | **PASS*** | Via `twin_snapshot_id` on Baseline inspect (*no dedicated Twin UI*) |
| Publish Curriculum | **PASS** | BF-001 + bridge e2e demo |
| Archive Curriculum | **PASS** | BF-001 archive remediation |
| Resume Curriculum | **PASS** | Studio retreat/reset recovery |
| No operational regressions | **PASS** | BF-001 + PR-001A recovery suites |

---

## Phase 8 — Cross-system integrity

```text
Student → Baseline → Digital Twin → Runtime → Study Plan → Mission Engine → Dashboard → History
```

| Agreement | Result |
|-----------|--------|
| Baseline is educational origin | **PASS** |
| Twin births from Baseline (not Calibration UI) | **PASS** |
| Runtime entry after Twin attempt | **PASS** |
| Study Plan / enrol uses Baseline fields | **PASS** |
| Mission engine does not invent second origin | **PASS** |
| Dashboard gated on Baseline for active plans | **PASS** |
| History not rewritten by Baseline restart | **PASS** |
| No conflicting sources of truth on happy path | **PASS** |

Legacy Calibration UI is deprecated (redirect only) — not a competing origin.

---

## Phase 9 — Educational invariants

| Invariant | Result |
|-----------|--------|
| Student never forced to restart learning | **PASS** — resume; restart voluntary |
| Historical study data never destroyed | **PASS** — supersede-only |
| Future planning respects Baseline | **PASS** |
| Twin remains authoritative snapshot chain | **PASS** (when birthed) |
| Runtime never bypasses educational state | **PASS** on student wizard path |
| One student / one active educational origin | **PASS** — one complete Baseline per subject_key |
| No duplicate study plans (active) | **PASS** |
| No duplicate Twins (birth scope) | **PASS** |
| No duplicate Baselines (current complete) | **PASS** (app-enforced; historical superseded rows allowed) |

---

## Tests executed (RF-002)

```text
Educational / Twin / Baseline / smoke / PX-002:
  210 passed  (knowledge/evidence/releases/RF002/educational_tests.txt)

Bridge / Runtime C / continuity delete / BF-001 / founder recovery:
  61 passed   (knowledge/evidence/releases/RF002/runtime_founder_tests.txt)

Mission invariants + session ownership / majority regression:
  104 passed / 4 failed  — failures = finish→/student assertion drift (Category D)
  (knowledge/evidence/releases/RF002/continuity_mission_tests.txt)

Core lifecycle slice (Baseline + smoke journey + wizard):
  29 passed
```

**Category A educational defects in candidate:** **0**

---

## Deliverable index

| Artefact | Path |
|----------|------|
| This report | `RF002_SYSTEM_VERIFICATION_REPORT.md` |
| Lifecycle | `RF002_EDUCATIONAL_LIFECYCLE.md` |
| Twin audit | `RF002_DIGITAL_TWIN_AUDIT.md` |
| Runtime consistency | `RF002_RUNTIME_CONSISTENCY.md` |
| Deployment | `RF002_DEPLOYMENT_VERIFICATION.md` |
| Risks | `RF002_RISK_REGISTER.md` |
| Release recommendation | `RF002_RELEASE_RECOMMENDATION.md` |
| Evidence pack | `knowledge/evidence/releases/RF002/` |

---

## Success criteria

| Criterion | Status |
|-----------|--------|
| Educational lifecycle completes end-to-end | ✓ PASS (candidate) |
| Baseline is the single educational origin | ✓ PASS |
| Twin initialises correctly | ✓ PASS (Runtime A); honest skip possible (Runtime C) |
| Runtime A behaves correctly | ✓ PASS |
| Runtime C behaves correctly | ✓ PASS (thin bridge; engine unchanged) |
| Educational continuity preserved | ✓ PASS |
| Founder operations remain stable | ✓ PASS |
| Student history preserved | ✓ PASS |
| No duplicate educational state created | ✓ PASS |
| No Category A educational defects remain | ✓ PASS |

---

## Architecture compliance (verification note)

- No application redesign performed under RF-002.
- Curriculum V1/V2 traversal not altered.
- Layering Baseline → Twin Builder → StudyPlan / EnrolmentBridge preserved.
- Migration impact for cutover: Alembic merge required before production apply of `202607310001`.
