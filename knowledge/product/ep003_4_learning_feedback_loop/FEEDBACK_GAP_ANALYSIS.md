# EP-003.4 — Feedback Gap Analysis

**Programme:** EP-003.4 — Learning Feedback Loop  
**Date:** 2026-07-26  

---

## 1. Required evidence (programme brief)

| Evidence | Pre-EP-003.4 | Gap | EP-003.4 treatment |
|---|---|---|---|
| Plan completion | Mission status in SQL; no feedback event | No canonical feedback event | `plan_completed` via PlanningService |
| Recommendation acceptance | Decision Journal (underused) | Not in learning-feedback stream | `recommendation_accepted` |
| Recommendation dismissal | Decision Journal (underused) | Same | `recommendation_dismissed` |
| Missed sessions | `mission_missed_count` in planner inputs | Not emitted as feedback | `session_missed` |
| Recovery events | Recovery mode in plan explainability | Not emitted | `recovery_applied` |
| Revision adherence | Revision missions exist | No adherence event | `revision_adhered` on completion when revision/review titled |
| Study consistency | Streak helpers in ReadinessService | No observation event | `study_consistency_observed` |

## 2. Distinctions enforced

| Class | Examples | EP-003.4 rule |
|---|---|---|
| Observed evidence | Accepted tip, completed mission, missed count | Record |
| Operational telemetry | Dual-run latency, cutover health | Unchanged; separate |
| Educational conclusions | Mastery, readiness judgement, tip quality | Forbidden on feedback payloads |
| Twin estimates | Facet synthesis | Must not write from feedback |

## 3. Remaining gaps (intentional)

- No durable cross-process store (process-local buffer).
- No automatic Twin recomputation subscriber.
- No causal educational-effectiveness proof.
- No feedback → ranking / readiness / planning closed loop (constitutionally deferred).
