# EP-008.3 — Recommendation Commitment & Follow-through

**Programme:** EP-008.3  
**Title:** Recommendation Commitment & Follow-through  
**Date:** 2026-07-26  
**Status:** Design + EP-008.3A delivery complete — **EP-008.3B Tier B filed** (K2 hold **68**; K7 **60**; Strong-band / rates still open)  
**Production activation:** Student Home / Mission / History commitment layer (preference/intent only)  
**Runtime / ranking / algorithm changes:** None  
**Maps to:** P-004.1 **IMP-02**; EP-008.1B residual Strong-band / acceptance KPI  
**Upstream:** [`../ep008_1_recommendation_trust/`](../ep008_1_recommendation_trust/) · [`../ep008_1b_recommendation_trust_validation/`](../ep008_1b_recommendation_trust_validation/)  
**Successor validation:** [`../ep008_3b_recommendation_commitment_validation/`](../ep008_3b_recommendation_commitment_validation/)  

---

## Purpose

Increase **recommendation commitment and follow-through** while preserving Runtime A authority — so a student consistently experiences:

1. I understand why this is today’s priority.  
2. I chose to do it.  
3. I know what changed afterwards.

Success is measured by educational execution and observational follow-through metrics — **not** by recommendation complexity or ranking changes.

**Do not improve recommendation intelligence. Improve recommendation execution.**

---

## Authority chain

```
Vision 2030
  → Educational Constitution + EIP-002 / EIP-003
  → Architecture Constitution Art. IV
  → P-001.2 Explainability + P-001.3 Recommendation Quality
  → P-004.1 IMP-02 / GAP-06
  → EP-008.1 Trust (permanent) + EP-008.1B (K2 68 / KSI 64)
  → This programme (commitment / defer / reflection / history / research metrics)
  → EP-008.3 delivery (successor) → Tier B / KPI validation
```

---

## Deliverables

| Artefact | Role |
|---|---|
| [`ENGINEERING_DESIGN.md`](ENGINEERING_DESIGN.md) | Commitment contract, state machine, data model, constraints |
| [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) | Phased delivery, file touchpoints, DoD, STOP checks |
| [`UI_SPECIFICATION.md`](UI_SPECIFICATION.md) | Home / Mission / reflection / History copy & layout |
| [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md) | CF-A0*, behavioural floors, Tier B, K2 ≥ 75 claim rules |
| [`EXPECTED_KSI_MOVEMENT.md`](EXPECTED_KSI_MOVEMENT.md) | Category deltas and net ΔKSI (planning only) |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student problem, benefit, metrics, risks |
| [`IMPLEMENTATION_COMPLETION_REPORT.md`](IMPLEMENTATION_COMPLETION_REPORT.md) | EP-008.3A delivery completion |
| [`TEST_REPORT.md`](TEST_REPORT.md) | Tier A / CF-A0* results |
| [`IMPLEMENTATION_NOTES.md`](IMPLEMENTATION_NOTES.md) | Pattern A choice + emit notes |

---

## Design areas (summary)

| Area | Student outcome |
|---|---|
| Commitment | “I’m doing this next.” |
| Deferred commitment | Honest reasons; never punish |
| Completion reflection | What changed / why / what next |
| Recommendation history | Educational narrative, not audit log |
| Plan continuity | One continuous study plan |
| Behaviour metrics | Observational research only |

---

## Constraint summary

- Do **not** change Runtime A, RecommendationService ranking, PlanningService, or ReadinessService educational reasoning.  
- Do **not** introduce LLMs, conversational AI, Learning Twin authority, streaks, or gamification.  
- Preference / intent ≠ mastery.  
- Trust Contract T1–T11 remains permanent.  
- Metrics must not feed ranking.  
- No commits in this design programme.

---

## Validation goals

| Goal | Target |
|---|---|
| Primary | K2 ≥ **75** |
| Secondary | K7 improvement |
| Hold | No K8 regression; no cognitive-load increase |
| Hard | No educational reasoning changes |

---

**End of README**
