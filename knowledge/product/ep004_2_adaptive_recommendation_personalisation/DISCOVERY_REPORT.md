# EP-004.2 — Discovery Report

**Programme:** EP-004.2 — Adaptive Recommendation Personalisation  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| Product Vision / Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Transparent, evidence-based recommendations; Final Test |
| Architecture Constitution | `docs/ARCHITECTURE_CONSTITUTION.md`, `.cursor/rules/00-CONSTITUTION.md` | Layering; no second educational brain |
| EP-002.9 ownership baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Runtime A guidance ownership |
| P-001.2 Explainability Standard | `knowledge/product/p001_2_explainability_standard/` | Mandatory schema; confidence honesty |
| P-001.3 Recommendation Quality | `knowledge/product/p001_3_recommendation_quality_standard/` | Decision Framework; Q1–Q10; personalisation principle |
| EP-003.1–EP-004.1 | `knowledge/product/ep003_*/`, `ep004_1_*` | Quality contract → feedback → profile substrate |
| RecommendationService | `app/services/recommendation_service.py`, `recommendation_quality.py` | Sole Runtime A ranking authority |
| Personal Learning Profile | `app/infrastructure/adapters/personal_learning_profile/` | Evidence Port; confidence; unsupported states |
| RuntimeAPresentationAdapter | `app/presentation/intelligence_surface/adapter.py` | Presentation-only pass-through |

---

## 2. Current behaviour (pre-EP-004.2)

1. EP-003.1 Decision Framework ranks candidates by ladder + legacy priority + title.
2. EP-004.1 Profile Port exists; services may resolve a consumer view.
3. `RecommendationService.consume_personal_learning_profile` refreshed the profile after decisions but **discarded** the return value for ranking.
4. No profile attribute changed ordering, session sizing, cadence, or explanations.
5. Accept/dismiss remained preference history only (correct constitutional boundary).
6. Presentation already pass-throughs schema-complete rows without re-ranking.

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| Profile is ready as evidence, not as authority | Consume via Port inside RecommendationService only |
| Decision Framework must remain primary | Personalisation = tie-breaks / framing / cadence after ladder |
| Accept rate ≠ educational correctness | Must never promote categories from accept/dismiss alone |
| Many attributes often unsupported / thin | Graceful degrade; confidence gates required |
| K4 personalisation is still thin in KSI | EP-004.2 is the lawful closed-loop for recommendations |
| Presentation must not personalise | Attach explanations at RecommendationService boundary |

---

## 4. Recommended implementation shape

1. Add `recommendation_personalisation.py` owned/called only via RecommendationService quality path.
2. Resolve profile in `_finalise_recommendations`; pass consumer view into `apply_quality_contract`.
3. Apply bounded rules after hard gates + ladder assignment; never reclassify ranks 1–3.
4. Emit `personalisation_applied`, `personalisation_factors`, and student-safe evidence lines.
5. Keep `RuntimeAPresentationAdapter` pass-through; no profile inspection in presentation.
6. Preserve fail-open and `ENABLE_PERSONAL_LEARNING_PROFILE` default OFF.

---

## 5. Out of scope (explicit)

- Readiness or Planning personalisation loops (separate programmes).
- Promoting tips from accept rate / inventing study windows.
- Durable cross-process profile store.
- Live Scorecard cohort instrumentation (follow-on).
- Twin Knowledge State writes.
