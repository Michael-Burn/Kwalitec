# EP-004.3 — Constitutional Impact Assessment

**Programme:** EP-004.3 — Adaptive Planning Personalisation  
**Date:** 2026-07-26  

---

## 1. Ownership map (before → after)

| Component | Before | After | Risk |
|---|---|---|---|
| PlanningService | Sole Runtime A planning authority | Still sole authority; may use profile as evidence | Low if bounded |
| Personal Learning Profile | Evidence summary only | Still evidence only — no planning API | Must not grow decision methods |
| planning_quality | Schema + readiness/rec labels | Schema + calls personalisation | Keep profile as optional input |
| planning_personalisation | N/A | Pacing / duration / recovery / revision helpers | Must not invent missions or reorder educational priorities |
| Adaptive study planner | Slot construction | Unchanged as educational owner of slot types | Personalisation may adjust minutes / equivalent repair topic only |
| RuntimeAPresentationAdapter | Pass-through | Pass-through of personalisation fields | Must not personalise |
| RecommendationService / ReadinessService | Unchanged by this programme | Unchanged | No cross-authority bleed |

---

## 2. Lawful influence model

```
Profile attributes (evidence)
        │  Port / consume (fail-open)
        ▼
PlanningService.build_daily_study_plan /
        get_dashboard_mission_surface
        │
        ▼
apply_planning_quality_contract (EP-003.3 schema)
        │
        ▼
apply_profile_personalisation (bounded adaptations)
        │
        ▼
Student-facing plan (schema + personalisation factors)
```

**Hard stop if:** profile invents missions, presentation invents personalisation, educational slot order is violated, or accept/dismiss becomes a plan driver.

---

## 3. Educational Constitution checks

| Rule | Impact |
|---|---|
| Evidence ≠ advice | Profile remains summary; PlanningService authors the plan |
| Plan coherence | review → recovery/weak → progression order preserved; abort on violation |
| Explainability | Personalisation factors + evidence lines required when applied |
| Fail-open | Missing/unsupported/low-confidence profile → baseline EP-003.3 plan |
| Sibling authorities | Readiness / Recommendation maths untouched |

---

## 4. Verdict

**Proceed** — constitutional ownership preserved if implementation stays within bounded adaptations and PlanningService authority.
