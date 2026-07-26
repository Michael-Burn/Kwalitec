# EP-004.2 — Constitutional Impact Assessment

**Programme:** EP-004.2 — Adaptive Recommendation Personalisation  
**Date:** 2026-07-26  

---

## 1. Ownership map (before → after)

| Component | Before | After | Risk |
|---|---|---|---|
| RecommendationService | Sole Runtime A ranking authority | Still sole authority; may use profile as evidence | Low if bounded |
| Personal Learning Profile | Evidence summary only | Still evidence only — no ranking API | Must not grow decision methods |
| recommendation_quality | Ladder + schema | Ladder + schema + calls personalisation | Keep profile as optional input |
| recommendation_personalisation | N/A | Tie-breaks / sizing / cadence helpers | Must not invent warrants |
| RuntimeAPresentationAdapter | Pass-through | Pass-through of personalisation fields | Must not personalise |
| ReadinessService / PlanningService | Unchanged by this programme | Unchanged | No cross-authority bleed |

---

## 2. Lawful influence model

```
Profile attributes (evidence)
        │  Port / consume (fail-open)
        ▼
RecommendationService._finalise_recommendations
        │
        ▼
apply_quality_contract (Decision Framework + gates)
        │
        ▼
apply_profile_personalisation (bounded tie-breaks only)
        │
        ▼
Student-facing rows (schema + personalisation factors)
```

**Hard stop if:** profile ranks candidates, presentation invents personalisation, or accept/dismiss becomes mastery evidence.

---

## 3. Educational Constitution checks

| Rule | Impact |
|---|---|
| Evidence ≠ advice | Profile remains summary; RecommendationService authors advice |
| Accept/dismiss ≠ mastery | Responsiveness used only for cadence softening, never category promotion |
| Plan coherence | Mission / safety / blocking ranks protected from personalisation |
| Explainability | Personalisation factors + evidence lines required when applied |
| Fail-open | Missing/unsupported/low-confidence profile → baseline ranking |

---

## 4. Verdict

**Proceed** — constitutional ownership preserved if implementation stays within bounded tie-breaks and RecommendationService authority.
