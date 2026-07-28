# VP-001 — User Experience Review

**Programme:** VP-001 — Version 1 Product Completion  
**Date:** 2026-07-28  
**Status:** Complete (review artefact)

---

## 1. Scope

Review consistency of the Version 1 student experience across terminology,
explainability, interaction flows, visual hierarchy, and educational messaging
— without moving educational reasoning into presentation.

---

## 2. Terminology

| Student language (required) | Internal / forbidden on student surfaces |
|-----------------------------|------------------------------------------|
| Today's focus / Mission | Digital Twin, Adaptive Decision engine |
| Why this matters | Graph node, curriculum graph |
| Study session | Learning orchestrator |
| Revision | Mastery score (raw) |
| Progress / Journey | Evidence spine |

Session and Student presentation already maintain forbidden-term lists
(`FORBIDDEN_LEARNER_TERMS`). VP-001 Experience Model adapters expose
`educational_why`, `expected_outcome`, and effort labels — student-facing
copy remains EX-001 / presentation responsibility, not EI rule math.

**Verdict:** Consistent with prior RR/CQ terminology law. No new learner-facing
engine jargon introduced by VP-001 hooks.

---

## 3. Explainability

| Surface | Explainability source when EI available | Fallback |
|---------|-----------------------------------------|----------|
| Home recommendation | EX-001 dashboard recommendation fields via RIS | Runtime A RecommendationService |
| Session overview | EX-001 session briefing (`educational_why`, outcome) | Session Experience projection |
| Revision | EX-001 revision entry (`educational_why`, steps) | Adaptive Decision options |
| Coach | RIS coach context metadata | AP-002 TutorExplanation |

Educational rationale remains authored by EI-007 → EX-001. Presentation only
maps fields. Controllers do not re-rank or invent reasons.

**Verdict:** Pass for Preferred Authority paths. Temporary compatibility paths
retain prior Runtime A explanations until SCI coverage is universal.

---

## 4. Interaction flows

Canonical sole-runtime flow:

```
Login → (Alpha onboarding) → Study Plan Wizard → Calibration*
  → Student Home → Start Session → Activity → Reflection → Complete
  → Home (refreshed)
```

\* Calibration remains the Twin-birth product law for Runtime A plans.
LP-001 onboard runs at enrolment when a published CKG edition exists so
Preferred Authority is available without founder rebuilds.

Evidence → belief → decision → experience refresh occurs automatically after
session answer/complete when an SCI exists.

**Verdict:** Coherent single journey; dual-run legacy redirects preserved under
sole-runtime flags.

---

## 5. Visual hierarchy

VP-001 does not redesign templates. Hierarchy remains:

1. Brand / Education OS shell  
2. Primary CTA (Start Session / Begin Revision)  
3. Educational why / outcome  
4. Secondary navigation (Journey, History, Profile)

No new card clusters, parallel recommendation widgets, or competing primary CTAs
were introduced.

**Verdict:** Unchanged shell; Experience Model fields enrich existing slots.

---

## 6. Educational messaging

| Principle | Status |
|-----------|--------|
| Guidance over content dumping | Preserved |
| One primary recommendation | RIS highest-value decision |
| Honest Temporary compatibility | Runtime A when no SCI |
| No LLM in core learning path | Preserved |

---

## 7. Non-moves (architecture)

- No educational reasoning in Jinja / JS  
- No parallel recommendation engine  
- No bypass of Runtime Integration on read paths  
- No new EI layers  

---

**End of User Experience Review**
