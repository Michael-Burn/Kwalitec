# EP-004.2 — Adaptive Recommendation Personalisation

**Programme:** EP-004.2 — Adaptive Recommendation Personalisation  
**Status:** Complete  
**Date:** 2026-07-26  
**Depends on:** EP-004.1 Personal Learning Profile; EP-003.1 Recommendation Quality Contract  
**Production activation:** Gated (`KWALITEC_PERSONAL_LEARNING_PROFILE` / `ENABLE_PERSONAL_LEARNING_PROFILE` default OFF)

## Purpose

Enhance `RecommendationService` so recommendation prioritisation may adapt to Personal Learning Profile evidence while preserving constitutional ownership and explainability.

## Artefacts

| Document | Role |
|---|---|
| [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) | Discovery phase |
| [`CONSTITUTIONAL_IMPACT_ASSESSMENT.md`](CONSTITUTIONAL_IMPACT_ASSESSMENT.md) | Ownership impact |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student value |
| [`PERSONALISATION_GAP_ANALYSIS.md`](PERSONALISATION_GAP_ANALYSIS.md) | Gap analysis |
| [`PERSONALISATION_RULES.md`](PERSONALISATION_RULES.md) | Design rules |
| [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md) | Risks |
| [`EXPLAINABILITY_REVIEW.md`](EXPLAINABILITY_REVIEW.md) | P-001.2 review |
| [`RECOMMENDATION_REVIEW.md`](RECOMMENDATION_REVIEW.md) | P-001.3 review |
| [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md) | K1–K8 deltas |
| [`CONSTITUTIONAL_VERIFICATION.md`](CONSTITUTIONAL_VERIFICATION.md) | Exit ownership check |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion |

## Implementation

- `app/services/recommendation_personalisation.py` — bounded personalisation rules
- `app/services/recommendation_quality.py` — applies personalisation after Decision Framework
- `app/services/recommendation_service.py` — consumes profile via Port before finalisation
- `tests/services/test_recommendation_personalisation_ep004_2.py`
