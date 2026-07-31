# RF-002 — Runtime Consistency

**Programme:** RF-002 Educational System Verification  
**Phase:** Phase 3 — Runtime Consistency  
**Date:** 2026-07-31  
**Verdict:** **PASS** — identical Baseline origin; Twin-first finalize; no duplicate onboarding; Runtime behaviour unchanged

---

## Decision under verification

SB-001A Decision 2B — **thin Runtime C bridge**. Runtime C educational behaviour, SCI, traversal, and recommendation engines are **unchanged**. RF-002 confirms that constraint still holds.

---

## Shared origin

```text
Baseline complete (same declarations)
        ↓
Twin birth attempt (same BaselineTwinBirth path)
        ↓
┌───────────────────────┬────────────────────────────┐
│ Runtime A             │ Runtime C                  │
│ StudyPlanService      │ EnrolmentBridge.enrol      │
│ create_study_plan     │ enrol_student + SCI ensure │
└───────────────────────┴────────────────────────────┘
        ↓
Canonical Home /student/
```

| Invariant | Runtime A | Runtime C | Result |
|-----------|-----------|-----------|--------|
| Originates from identical Baseline | Yes | Yes | **PASS** |
| Twin birth attempted before entry | Yes | Yes | **PASS** |
| Bypasses Twin initialisation | No | No (honest skip only) | **PASS** |
| Asks duplicate onboarding questions | No | No | **PASS** |
| Loses Baseline declarations | No (row complete) | No (row complete) | **PASS** |
| Runtime engine redesigned | No | No | **PASS** |

Evidence:

- `tests/presentation/student_baseline/test_sb001a_baseline.py` — Runtime A finalize; Runtime C bridge ordering spy
- `tests/application/platform_integration/test_bridge.py` — A vs C routing
- `SB001A_RUNTIME_BRIDGE.md` — design contract reconfirmed

---

## Onboarding uniqueness

| Surface | Behaviour |
|---------|-----------|
| `/baseline` | Sole progressive intake |
| `/calibration/*` | Redirects to Baseline (`for_plan`) |
| Wizard step 4 / review | Redirects to Baseline |
| Home | Gates active Study Plan missing complete Baseline |
| After complete Baseline | Resume summary — no re-ask |

Neither Runtime A nor Runtime C presents a second Baseline questionnaire after finalize.

---

## Coexistence

Runtime C enrolled students must not silently fall back to Runtime A for educational authority (A9 coexistence). Bridge and inventory/gates suites remain green under RF-002 (`test_bridge`, `test_inventory_and_gates`).

---

## Educational judgement

Both runtimes now start from the same tutor conversation. The student is not asked twice who they are. Planning and enrolment receive the same declared position and objective. Runtime math itself was not altered — continuity improved without changing how teaching engines work.
