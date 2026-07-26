# EP-008.1 — Recommendation Trust

**Programme:** EP-008.1  
**Title:** Recommendation Trust  
**Date:** 2026-07-26  
**Status:** Design complete; **implementation (EP-008.1A) complete — Tier A structural Pass**; **Tier B validation (EP-008.1B) complete — K2 68 / KSI 64**  
**Production activation:** Presentation defaults on sole-runtime Student Home (no new flags)  
**Runtime / ranking / algorithm changes:** None  
**Maps to:** P-004.1 IMP-01 / REM-06 (trust surfaces only; acceptance KPI = EP-008.3)  
**Successor validation:** [`../ep008_1b_recommendation_trust_validation/`](../ep008_1b_recommendation_trust_validation/)

---

## Purpose

Increase **recommendation trust** through presentation, explanation, and educational clarity — so a student immediately understands:

1. Why this recommendation exists  
2. Why it matters now  
3. What to do next  
4. What improvement to expect  
5. How completion affects future recommendations  

Success is measured by improved **trust and acceptance readiness**, not by recommendation complexity.

**Runtime A educational reasoning remains authoritative.** This programme does **not** redesign `RecommendationService`, change ranking, introduce LLMs, or invent a second educational brain.

---

## Authority chain

```
Vision 2030
  → Educational Constitution + EIP-003
  → Architecture Constitution Art. IV
  → P-001.2 Explainability Standard + P-001.3 Recommendation Quality
  → P-004.1 IMP-01 / EP-005.2 REM-06
  → This programme (trust presentation contract)
  → EP-008.1A implementation (DTO / view-model / template only) — done (Tier A)
  → EP-008.1B perception validation — done (K2 68; KSI 64)
  → EP-008.3 (commitment / follow-through design — IMP-02)
```

---

## Deliverables

| Artefact | Role |
|---|---|
| [`ENGINEERING_DESIGN.md`](ENGINEERING_DESIGN.md) | Architecture, trust contract, field inventory, constraints |
| [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) | Phased delivery, file touchpoints, DoD, non-goals |
| [`UI_SPECIFICATION.md`](UI_SPECIFICATION.md) | Home / Coach / Mission / Revision / outcome copy & layout |
| [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md) | Contract tests, Tier B perception, K2 claim rules |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student problem, benefit, metrics, risks |
| [`EXPECTED_KSI_MOVEMENT.md`](EXPECTED_KSI_MOVEMENT.md) | Category deltas and net ΔKSI (planning only) |
| [`EXPLAINABILITY_REVIEW.md`](EXPLAINABILITY_REVIEW.md) | P-001.2 checklist against the design |
| [`RECOMMENDATION_REVIEW.md`](RECOMMENDATION_REVIEW.md) | P-001.3 checklist against the design |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Design programme completion report |
| [`IMPLEMENTATION_COMPLETION_REPORT.md`](IMPLEMENTATION_COMPLETION_REPORT.md) | Delivery completion (EP-008.1A) |
| [`TEST_REPORT.md`](TEST_REPORT.md) | Tier A test evidence |

---

## Upstream / downstream

| Link | Path |
|---|---|
| Priority & IMP-01 | `../p004_1_ksi_gap_analysis/` |
| Root cause REM-06 | `../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md` |
| Engine schema (already shipped) | `../ep003_1_recommendation_engine_enhancement/` |
| MES pass-through (already shipped) | `../ep006_2_mes_delivery_implementation/` |
| Perception residual | `../ep006_3_mes_perception_validation/` |
| Acceptance / commitment successor | [`../ep008_3_recommendation_commitment_followthrough/`](../ep008_3_recommendation_commitment_followthrough/) (EP-008.3 design) |
| Explainability law | `../p001_2_explainability_standard/` |
| Recommendation quality law | `../p001_3_recommendation_quality_standard/` |

---

## Constraint summary

- Do **not** change educational reasoning, ranking, or Decision Framework ladder.  
- Do **not** introduce LLMs or speculative AI educational truth.  
- Do **not** conflate accept/dismiss telemetry with this design programme (EP-008.3).  
- Presentation adapters must **pass through** authored MES — never re-decide.  
- Compatible with Version 1 Release Framework; does not claim validated KSI lifts.

---

**End of README**
