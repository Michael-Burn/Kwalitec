# EP-002.5 — Study Insights Gated HTTP Cutover

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.5  
**Date:** 2026-07-26  
**Nature:** First controlled student-facing activation of Twin-backed Study Insights on the dashboard/home recommendation surface — **legacy fail-open fallback retained**; **no production-wide activation**

---

## Artefacts

| Artefact | Path |
|---|---|
| Discovery Report | [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) |
| Cutover Design | [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md) |
| Eligibility Matrix | [`ELIGIBILITY_MATRIX.md`](ELIGIBILITY_MATRIX.md) |
| Rollback Plan | [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) |
| Risk Assessment | [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md) |
| Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) |

---

## One-line intent

Eligible non-production dashboard requests may receive a Study Insights projection from `build_study_insights`; every other case returns legacy `generate_recommendations` unchanged.

---

## Kill switches

1. `KWALITEC_STUDY_INSIGHTS_CUTOVER=0` (or unset)  
2. `KWALITEC_DIGITAL_TWIN=0` (or unset)  
3. `APP_ENV=production` / `prod` (cutover always ineligible)

---

## Predecessors

- EP-002.4 Study Insights dual-run (legacy authoritative; structured compare)  
- EP-002.3 Twin + Authority non-prod soak  
- EP-002.1–2 observability + Foundation DI  
- EP-001.5 Architectural Integration Review  
