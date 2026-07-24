# EP-002 — Analytics Operational Readiness

**Programme ID:** EP-002  
**Status:** Complete (flag remains OFF)  
**Authority:** Engineering · Privacy · Product Analytics  
**Depends on:** EP-001 / PRD-001 Phases A–E, ADR-025, ADR-026  

## Mission

Prepare the analytics platform for safe production activation without changing educational behaviour. `ANALYTICS_EVENTS_V1` remains **OFF** throughout EP-002.

## Workstreams

| WS | Objective | Primary artefacts |
|---|---|---|
| 1 | Durable outbox | SQL adapters, worker, replay, DLQ, cleanup |
| 2 | Observability | Infrastructure metrics only |
| 3 | Reliability | Restart / retry / duplicate / fail-open tests |
| 4 | Privacy ops | Retention, deletion, export, audit, consent |
| 5 | Feature flag strategy | Staged rollout + kill switch |
| 6 | Runbooks | Ops / incident / replay / recovery / monitoring / go-live |

## Deliverables index

| Deliverable | Path |
|---|---|
| Operational Readiness Report | [`OPERATIONAL_READINESS_REPORT.md`](OPERATIONAL_READINESS_REPORT.md) |
| Production / Operational Runbook | [`PRODUCTION_RUNBOOK.md`](PRODUCTION_RUNBOOK.md) |
| Incident Response Guide | [`INCIDENT_RESPONSE.md`](INCIDENT_RESPONSE.md) |
| Replay Specification | [`REPLAY_SPECIFICATION.md`](REPLAY_SPECIFICATION.md) |
| Recovery Guide | [`RECOVERY_GUIDE.md`](RECOVERY_GUIDE.md) |
| Monitoring Specification | [`MONITORING_SPECIFICATION.md`](MONITORING_SPECIFICATION.md) |
| Privacy Operations Guide | [`PRIVACY_OPERATIONS_GUIDE.md`](PRIVACY_OPERATIONS_GUIDE.md) |
| Feature Flag Strategy | [`FEATURE_FLAG_STRATEGY.md`](FEATURE_FLAG_STRATEGY.md) |
| Reliability Test Report | [`RELIABILITY_TEST_REPORT.md`](RELIABILITY_TEST_REPORT.md) |
| Go-Live Checklist | [`GO_LIVE_CHECKLIST.md`](GO_LIVE_CHECKLIST.md) |
| Release Checklist | [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) |

## Exit criteria

- [x] Analytics remains OFF by default
- [x] Durable SQL outbox + worker + replay + dead-letter
- [x] Operational metrics available (infra only)
- [x] Reliability tests green
- [x] Privacy workflows executable (PRD-001 §7–§8)
- [x] Runbooks complete
- [x] Ready for staged activation (see Go-Live Checklist)
