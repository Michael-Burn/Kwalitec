# PRD-001 Phase B — Architecture

**ADR:** [`docs/adr/ADR-025-analytics-event-infrastructure.md`](../../../docs/adr/ADR-025-analytics-event-infrastructure.md) (Phase B amendment)  
**Catalogue:** [`EVENT_CATALOGUE.md`](EVENT_CATALOGUE.md)

## Diagram

```
Student
  │
  ▼
Study Session (LXP) — StudySessionService
  │  start_session / finish_session / record_practice_outcome
  ▼
Educational persistence (Mission / StudyAttempt)  ← AUTHORITATIVE
  │  transaction success
  ▼
_observe_session_* (fail-open wrappers)
  │
  ▼
session_events builders (metadata only)
  │
  ▼
AnalyticsEventDispatcher
  │  feature flag ANALYTICS_EVENTS_V1 (default OFF → no-op)
  ▼
Registry allowlist → Validator → Serializer → Outbox
```

## Authority boundary

| Layer | Owns |
|---|---|
| Study Session / Mission / Evidence | Educational truth and persistence |
| EducationalStateService | Experience Educational State assembly (unchanged) |
| Twin / Recommendation | Unchanged — no emits, no imports |
| Analytics | Observation after success only |

## Emit points (authoritative only)

| Lifecycle | Event | When |
|---|---|---|
| Start | `session.started` | After Pending→In Progress commit (not on idempotent re-entry) |
| Finish yes/partial | `session.completed` (`completed`) | After finish persistence |
| Finish no | `session.completed` (`abandoned_after_start`) | After finish persistence (mission left open) |
| Practice outcome | `session.completed` (`completed`) | After practice persistence (idempotent with finish) |

Navigation-only views do **not** emit.

## Fail-open

Dispatcher / registry / validation / outbox failures are caught and logged (`analytics.emit_failed`). The Study Session always succeeds for the student.
