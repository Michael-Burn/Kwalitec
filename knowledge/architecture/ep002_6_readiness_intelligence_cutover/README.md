# EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover

**Programme:** EP-002 — Student Intelligence Surface  
**Workstream:** WS5 — Readiness intelligence surface  
**Date:** 2026-07-26  
**Nature:** Dual-run diagnostics + gated HTTP cutover for Runtime A readiness surfaces

## Intent

Activate EP-001.3 `build_readiness_intelligence` beside legacy readiness on
dashboard and analytics, then allow eligible non-production requests to receive
a Twin projection — with legacy fail-open retained.

## Kill switches

1. `KWALITEC_READINESS_INTELLIGENCE_CUTOVER=0` (or unset)
2. `KWALITEC_DIGITAL_TWIN=0` (or unset)
3. Production / `prod` `APP_ENV` (always ineligible)

## Artefacts

| File | Role |
|---|---|
| `DISCOVERY_REPORT.md` | Mandatory architecture discovery |
| `CUTOVER_DESIGN.md` | Dual-run + cutover orchestration |
| `ELIGIBILITY_MATRIX.md` | Binding flag × env × limitation matrix |
| `ROLLBACK_PLAN.md` | Kill-switch rollback drill |
| `STUDENT_IMPACT_ASSESSMENT.md` | Student-visible impact scope |
| `RISK_ASSESSMENT.md` | Risk register |
| `COMPLETION_REPORT.md` | Authoritative completion record |

## Constraints

- No schema changes
- No ownership changes
- No production-wide activation
- No new readiness engines
- No Twin redesign
- No recursion into Runtime A collectors (`get_overall_readiness` stays pure)
