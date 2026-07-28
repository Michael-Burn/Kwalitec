# FV-001 — Product Metrics

**Programme:** FV-001 — Founder Validation & Dogfooding  
**Authority:** Observational — RI-002 + LP-001 + mission rows + FV process telemetry  
**Refresh:** After meaningful study days via `flask fv-metrics`  
**Rule:** Record measured values only. Do not invent rates.

---

## Baseline board

| Metric | Definition | Current | Source | Notes |
|---|---|---|---|---|
| Onboarding completion | Completed LP onboard / (completed + failed) | — | `llp_lifecycle_operations` · FV telemetry | Awaiting dogfood |
| SCI creation success | Active-plan students with ≥1 active SCI | — | RI-002 `sci_coverage` | Awaiting dogfood |
| Experience Model generation | RIS EI-path / total RIS | — | RI-002 telemetry | Awaiting dogfood |
| Runtime A fallback frequency | RIS fallback / total RIS | — | RI-002 telemetry | Awaiting dogfood |
| Session completion rate | Missions Completed / all missions | — | `missions.status` | Awaiting dogfood |
| Evidence recording success | Completed evidence_refresh / (completed + failed) | — | LP-001 · FV telemetry | Awaiting dogfood |
| Decision refresh latency | Mean / P95 ms of `educational_decisions` stage | — | FV process telemetry | Awaiting dogfood |
| System failures | Fail-open exceptions on enrolment/evidence hooks | **0** | FV telemetry | Process-local |

---

## Snapshot log

| Date | Onboard % | SCI % | ExpModel % | Fallback % | Session % | Evidence % | Decision ms (mean) | Failures | Note |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2026-07-28 | — | — | — | — | — | — | — | 0 | Instrumentation live; no founder sessions yet |

---

## Operator command

```bash
flask fv-metrics
```

Paste relevant fields into the snapshot log. Full JSON is process/DB state — not a marketing claim.

---

## Interpretation rules

1. Empty denominators mean “no samples yet”, not 0% product quality.  
2. Process-scoped FV telemetry resets on process restart — prefer LP-001 / mission persistence for durable rates.  
3. High Runtime A fallback during CS1 exclusive OS use is a **Major** signal if Preferred Authority was expected (published CKG + SCI).  
4. Do not inflate Engineering CRI from these numbers alone.

---

**End of Product Metrics**
