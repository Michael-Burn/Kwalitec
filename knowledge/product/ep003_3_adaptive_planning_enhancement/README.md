# EP-003.3 — Adaptive Planning Enhancement

**Programme:** EP-003.3  
**Status:** Complete  
**Date:** 2026-07-26  
**Authority:** Product (Runtime A planning quality)

## Purpose

Enhance `PlanningService` so daily study plans become more personalised, evidence-driven, and educationally effective while preserving constitutional ownership (Planning plans; Readiness evaluates; Recommendation recommends; presentation only presents).

## Contents

| Artefact | Role |
|---|---|
| [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) | Discovery sources and conclusions |
| [`CONSTITUTIONAL_IMPACT_ASSESSMENT.md`](CONSTITUTIONAL_IMPACT_ASSESSMENT.md) | Ownership impact before change |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student value assessment |
| [`PLANNING_GAP_ANALYSIS.md`](PLANNING_GAP_ANALYSIS.md) | Audit gaps vs desired capabilities |
| [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md) | Risks and mitigations |
| [`EXPLAINABILITY_REVIEW.md`](EXPLAINABILITY_REVIEW.md) | P-001.2 checklist |
| [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md) | Estimated ΔKSI |
| [`CONSTITUTIONAL_VERIFICATION.md`](CONSTITUTIONAL_VERIFICATION.md) | Post-change ownership verification |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme completion report |

## Constraints (honoured)

- PlanningService remains the sole planning authority.
- RecommendationService remains recommendation authority.
- ReadinessService remains readiness authority.
- RuntimeAPresentationAdapter remains presentation-only.
- Fail-open behaviour and existing feature flags preserved.
- STOP if constitutional ownership would be violated — not triggered.
