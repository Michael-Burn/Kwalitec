# PRD-001 Phase A — Architecture

**ADR:** [`docs/adr/ADR-025-analytics-event-infrastructure.md`](../../../docs/adr/ADR-025-analytics-event-infrastructure.md)

## Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│ Educational authorities (UNCHANGED in Phase A)                    │
│ Twin · Evidence · Mission · Journey · Reflection · ESS assembler  │
└───────────────────────────────┬──────────────────────────────────┘
                                │ (no emit hooks yet — Phases B–E)
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ AnalyticsEventDispatcher                                          │
│  1. Feature flag ANALYTICS_EVENTS_V1 (default OFF → no-op)        │
│  2. AnalyticsEventValidator + AnalyticsEventRegistry              │
│  3. AnalyticsEventSerializer                                      │
│  4. Outbox enqueue (approved write contract)                      │
└───────────────┬───────────────────────────────┬──────────────────┘
                │ flag OFF                      │ flag ON (tests)
                ▼                               ▼
         NullOutboxSink                  MemoryOutboxSink
         (zero writes)                   / SQL outbox table
                                                │
                                                ▼ (future worker)
                                         analytics_events
                                         (append-only store)
                                                │
                                                ▼
                                         AnalyticsPurgeJob
                                         (skeleton, dry-run default)
```

## Authority boundary

```
Educational truth ──► Twin / Evidence / Mission / Journey / ESS
Observation only  ──► analytics_* tables + dispatcher
```

Analytics **must not** import Twin calculators, recommendation rankers, or mastery math (enforced by `tests/architecture/test_analytics_import_guard.py`).

## Component map

| Component | Module |
|---|---|
| `AnalyticsEvent` | `contracts.py` |
| `AnalyticsEventVersion` | `versioning.py` |
| `AnalyticsEventRegistry` | `registry.py` |
| `AnalyticsEventValidator` | `validator.py` |
| `AnalyticsEventSerializer` | `serialization.py` |
| `AnalyticsEventDispatcher` | `dispatcher.py` |
| `AnalyticsFeatureFlag` | `feature_flag.py` |
| Correlation IDs | `correlation.py` |
| Idempotency | `idempotency.py` |
| Audit metadata | `audit.py` |
| Outbox | `outbox.py` + `analytics_outbox` |
| Purge skeleton | `purge.py` |
