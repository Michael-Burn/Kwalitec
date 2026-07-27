# PI-002A — Updated Enrolment Flow

**Programme:** PI-002A — Platform Integration: Founder → Student Bridge  
**Date:** 2026-07-27  

---

## Study Plan Wizard (unchanged chrome)

Steps 1–8 retain the existing UI. Behavioural additions:

### Step 1 — Examination

When discovery is enabled, a **Published Curriculum** category is appended to
the existing examining-body list. No redesign of cards or layout.

### Step 2 — Paper / subject

For the Published category, papers are active published subject codes with
titles from Curriculum Studio. Support badges use PTP-001
(`Supported` / `Coming Soon` / `Not Supported`) via `SubjectSupportService`.

### Steps 3–7

Unchanged for both runtimes (sitting, position, availability, preference,
target). Published subjects use Custom sitting / Pass targets.

### Step 8 — Review / create

```text
review_post
    │
    ├─ PTP-001 support gate (fail closed)
    │
    ├─ if bridge.should_use_bridge(category, subject):
    │       FounderStudentEnrolmentBridge.enrol(...)
    │         → Runtime C enrolment + audit
    │         → redirect student home
    │
    └─ else:
            StudyPlanService.create_study_plan(...)   # Runtime A unchanged
            RuntimeRoutingService.record_decision(...)  # audit Runtime A
            → redirect calibration (existing product law)
```

---

## Post-enrolment destinations

| Runtime | Destination | Rationale |
|---|---|---|
| Runtime A | Calibration (`/calibration/after-plan/<id>`) | Existing product law |
| Runtime C | Canonical student home | No StudyPlan row; Calibration is Runtime A Twin path |

Runtime C student mission UI cutover is explicitly out of scope for PI-002A;
engine enrolment and journey generation are verified in tests.
