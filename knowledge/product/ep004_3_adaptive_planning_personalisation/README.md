# EP-004.3 — Adaptive Planning Personalisation

**Programme:** EP-004.3  
**Status:** Complete  
**Date:** 2026-07-26  
**Authority:** PlanningService (Personal Learning Profile = evidence only)

## Purpose

Enhance PlanningService so daily plans adapt to Personal Learning Profile evidence — session duration, workload pacing, recovery sequencing, revision timing, and equivalent repair-topic selection — without changing educational priorities or constitutional ownership.

## Artefacts

| Document | Role |
|---|---|
| [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) | Discovery Phase |
| [`CONSTITUTIONAL_IMPACT_ASSESSMENT.md`](CONSTITUTIONAL_IMPACT_ASSESSMENT.md) | Ownership impact |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student value |
| [`PLANNING_PERSONALISATION_GAP_ANALYSIS.md`](PLANNING_PERSONALISATION_GAP_ANALYSIS.md) | Gap analysis |
| [`PERSONALISATION_RULES.md`](PERSONALISATION_RULES.md) | Bounded adaptation rules |
| [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md) | Risks |
| [`EXPLAINABILITY_REVIEW.md`](EXPLAINABILITY_REVIEW.md) | P-001.2 gate |
| [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md) | Estimated ΔKSI |
| [`CONSTITUTIONAL_VERIFICATION.md`](CONSTITUTIONAL_VERIFICATION.md) | Exit verification |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion |

## Implementation

- `app/services/planning_personalisation.py`
- Wired via `planning_quality.py` after EP-003.3 schema attachment
- Consumed from `PlanningService.build_daily_study_plan` / `get_dashboard_mission_surface`
- Tests: `tests/services/test_planning_personalisation_ep004_3.py`

## Activation

Gated by `KWALITEC_PERSONAL_LEARNING_PROFILE` / `ENABLE_PERSONAL_LEARNING_PROFILE` (default **OFF**). Fail-open when profile unavailable.
