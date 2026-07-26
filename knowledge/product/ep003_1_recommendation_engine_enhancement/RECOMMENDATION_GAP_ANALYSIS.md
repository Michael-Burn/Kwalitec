# EP-003.1 — Recommendation Gap Analysis

**Programme:** EP-003.1 — Recommendation Engine Enhancement  
**Date:** 2026-07-26  
**Against:** P-001.3 principles + Decision Framework; P-001.2 Mandatory Explanation Schema  

---

## 1. Pre-enhancement gaps

| Gap | Standard | Pre-EP-003.1 state | Severity |
|---|---|---|---|
| Flat priority sort | Decision Framework ladder ranks 1–9 | `PRIORITY_ORDER` only | High |
| Missing Mandatory Explanation Schema | P-001.2 §7 | Prose `reason` / `expected_benefit` only; schema filled in presentation | High |
| Missing confidence | P-001.2 §7.1; Q8 | Absent on legacy rows | High |
| Weak plan coherence | Q9 / G3 | Competing tips not labelled as advice vs Mission | High |
| No honest refusal | Q10 / G6 | Empty list / silent absence | Medium |
| Generic tips on thin history | Q1 / Q3 / G6 | Mock / technique tips could still emit | Medium |
| Duplicated narration | Architecture (one communication owner) | Service + EIP-003 adapter both narrated | Medium |
| Domain explanation chain unused | Capability 2.9 packaging | Parallel EI path only | Low (out of Runtime A scope) |

---

## 2. Duplicated logic inventory (consume, do not re-own)

| Signal | Owner | RecommendationService use | EP-003.1 disposition |
|---|---|---|---|
| Weak topics | ReadinessService | Rule generator | Unchanged consume |
| Review backlog | ReadinessService | Rule generator | Unchanged consume |
| Coverage / readiness score | ReadinessService | Rule generator + density band | Density band only added |
| Today’s Mission title | PlanningService | Not used for coherence | **Label-only read** via mission surface |
| Burnout | BurnoutMonitor | Rule generator | Unchanged |
| Exam timeline | ExamTimeline | Rule generator | Unchanged |

No Planning mission generation or readiness recalculation introduced.

---

## 3. Post-enhancement closure

| Gap | Closed by |
|---|---|
| Ladder ranking | `decision_ladder_rank` + sort in `recommendation_quality.apply_quality_contract` |
| Explanation schema | Fields: `why_recommended`, `supporting_evidence`, `confidence_level`, `suggested_next_action`, `review_point`, schema version/level |
| Confidence | Density-aware labels; thin → Low / Cannot yet be estimated |
| Plan coherence | `plan_coherence` / label; advisory reason suffix when Mission active |
| Honest refusal | `honest_refusal` sentinel row |
| Thin-history mock/technique | Hard gate G6 filters |
| Presentation re-narration | Adapter pass-through when `has_complete_explanation_schema` |

---

## 4. Remaining gaps (known limitations)

- Full P-001.3 Scorecard instrumentation (acceptance, completion, educational effectiveness) not wired.
- Domain `ExplanationChainPresentation` still not the Runtime A wire format (dict contract retained for template compatibility).
- Proportionality vs available session minutes (G5) uses category heuristics, not live duration budgets.
- EI `RecommendationCardBuilder` static family maps remain a parallel presentation path when orchestrator flag is on.
