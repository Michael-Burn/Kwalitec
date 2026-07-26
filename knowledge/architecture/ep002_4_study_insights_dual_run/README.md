# EP-002.4 — Study Insights Dual-Run

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.4 — Study Insights Dual-Run  
**Nature:** First student-surface **activation under observation** — legacy recommendations remain authoritative; Twin `build_study_insights` runs alongside for comparison only  
**Date:** 2026-07-26

---

## Mission (one line)

Execute Twin-backed Study Insights beside Runtime A `generate_recommendations` in approved non-production environments, capture structured comparisons, and leave student-visible HTTP behaviour unchanged.

---

## Artefacts

| Artefact | Path | Role |
|---|---|---|
| Discovery Report | [`DISCOVERY_REPORT.md`](DISCOVERY_REPORT.md) | Mandatory architecture discovery |
| Dual-Run Design | [`DUAL_RUN_DESIGN.md`](DUAL_RUN_DESIGN.md) | Behaviour, wiring, comparison fields |
| Gap Analysis | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) | What EP-002.1–3 left vs what EP-002.4 closes |
| Rollback Plan | [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md) | Kill switch and verification |
| Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Authoritative review document |

---

## Constraints (binding)

- No production cutover  
- No HTTP response / template student-visible changes  
- No schema changes  
- No new feature flags unless discovery proves need (**discovery: not needed**)  
- No ownership changes; no new recommendation engines  
- Production Twin / Authority defaults remain OFF  

---

## Predecessor gates

| Gate | Status |
|---|---|
| EP-002.1 consumer-chain observability | Complete |
| EP-002.2 shared Foundation DI | Complete |
| EP-002.3 Twin + Authority soak | Complete — dual-run **planning** authorised |
| EP-002.5 HTTP cutover | **Out of scope** for this milestone |
