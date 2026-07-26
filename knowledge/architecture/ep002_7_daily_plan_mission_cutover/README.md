# EP-002.7 — README

**Milestone:** EP-002.7 — Daily Plan & Mission Dual-Run and Gated HTTP Cutover  
**Programme:** EP-002 — Student Intelligence Surface (WS6)  
**Date:** 2026-07-26  
**Status:** Complete (gated non-prod activation; production remain OFF)

## Artefacts

| Document | Role |
|---|---|
| [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) | Mandatory architecture discovery |
| [`CONSTITUTIONAL_IMPACT_ASSESSMENT.md`](CONSTITUTIONAL_IMPACT_ASSESSMENT.md) | Ownership / quarantine impact |
| [`CONSTITUTIONAL_GAP_ANALYSIS.md`](CONSTITUTIONAL_GAP_ANALYSIS.md) | Gaps closed vs open |
| [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Cohort blast radius |
| [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md) | Binding dual-run + cutover design |
| [`ELIGIBILITY_MATRIX.md`](ELIGIBILITY_MATRIX.md) | Flag × env matrix |
| [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) | Kill switches |
| [`RISK_ASSESSMENT.md`](RISK_ASSESSMENT.md) | Risks and mitigations |
| [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Authoritative exit report |

## One-line outcome

Eligible non-production dashboard/mission requests may receive a Twin `build_daily_study_plan` projection into the mission surface DTO; legacy `generate_today_mission` remains fail-open; MissionOptimizer stays quarantined.
