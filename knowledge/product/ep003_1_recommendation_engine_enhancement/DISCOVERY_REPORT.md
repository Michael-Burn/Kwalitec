# EP-003.1 — Discovery Report

**Programme:** EP-003.1 — Recommendation Engine Enhancement  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| P-001.1 KSI Framework | `knowledge/product/p001_1_ksi_baseline/` | K2 baseline **48**; V1-K2 floor ≥ 50 |
| P-001.2 Explainability Standard | `knowledge/product/p001_2_explainability_standard/` | Mandatory Explanation Schema; confidence honesty |
| P-001.3 Recommendation Quality Standard | `knowledge/product/p001_3_recommendation_quality_standard/` | Q1–Q10 principles; Decision Framework ladder |
| Product Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Final Test; transparent / explainable recommendations |
| Governance | `knowledge/GOVERNANCE.md` §4.2–4.3 | Dual checklist mandate |
| EP-002.9 baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Ownership: Insight communicates; presentation does not evaluate |
| RecommendationService | `app/services/recommendation_service.py` | Runtime A selection authority (legacy dict rules) |
| RuntimeAPresentationAdapter | `app/presentation/intelligence_surface/adapter.py` | Presentation selection only |
| Domain RecommendationEngine | `app/domain/recommendation/` | Structural packaging (EI path); not Runtime A selection |

---

## 2. Current Runtime A behaviour (pre-EP-003.1)

1. Rule generators call Readiness / Burnout / ExamTimeline signals and emit flat dicts (`title`, `category`, `priority`, `reason`, `expected_benefit`, `generated_at`).
2. Ranking used a four-level `PRIORITY_ORDER` sort — **not** the P-001.3 Decision Framework ladder.
3. Explanation speech for legacy rows was applied **post-hoc** by `EducationalExplainabilityService` via `RuntimeAPresentationAdapter`.
4. No mandatory confidence field, review point, supporting-evidence list, or honest-refusal sentinel on cold start.
5. Plan coherence with Today’s Mission was not labelled on competing tips (weak-topic / review could appear as “today” peers without advice labelling).
6. Study Insights cutover (EP-002.5) already carried richer fields when Twin-served; presentation pass-through preserved Twin communication ownership.

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| K2 is the lowest KSI pillar (48) | Implementation must target educational usefulness of guidance, not tip volume |
| Standards exist but were docs-only (P-001.2 / P-001.3) | EP-003.1 is the first Runtime A implementation programme for those standards |
| Domain `Recommendation` dataclass is rich but unwired to Runtime A | Do **not** split authority; enhance service contract and optionally project later |
| Ownership chain is settled (EP-002.9) | Enhance communication quality inside RecommendationService; do not invent readiness/plans |
| Presentation enrichment was compensating for missing service schema | Move schema attachment into RecommendationService; adapter becomes pass-through when complete |

---

## 4. Recommended implementation shape

1. Add `app/services/recommendation_quality.py` as the quality contract module **owned and called only by** `RecommendationService`.
2. Apply Decision Framework ladder ranking, hard gates G4/G6, plan-coherence labelling, confidence, and Mandatory Explanation Schema before return.
3. Emit honest refusal (`No recommendation yet`) when evidence is too thin for a confident primary tip.
4. Keep `RuntimeAPresentationAdapter` presentation-only: skip EIP-003 re-narration when schema is already complete.
5. Preserve fail-open advisory / policy / dual-run hooks and feature-flag cutovers.

---

## 5. Out of scope (explicit)

- Reopening EP-001.1–4 ownership or Twin Ready (T7) claims.
- Marketing claims of recommendation effectiveness beyond approved freezes.
- Moving selection into presentation, bridges, or Planning/Readiness services.
- Full Scorecard instrumentation (acceptance / completion telemetry) — follow-on.
