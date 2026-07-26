# PRD-001 Phase C — Architecture

**ADR:** [`docs/adr/ADR-025-analytics-event-infrastructure.md`](../../../docs/adr/ADR-025-analytics-event-infrastructure.md) (Phase C amendment)  
**Catalogue:** [`EVENT_CATALOGUE.md`](EVENT_CATALOGUE.md)

## Diagram

```
Student
  │
  ▼
ReflectionManager / LearningSessionRuntime.collect_reflection
  │  business validation (ReflectionPolicy)
  ▼
Authoritative capture onto LearningSession  ← AUTHORITATIVE
  │  reflection posture → CAPTURED
  ▼
_observe_reflection_captured (fail-open wrapper)
  │  requires user_id (opaque int) for analytics identity
  ▼
reflection_events builders (metadata only — no body text)
  │  reflection.submitted + reflection.completed (shared correlation_id)
  ▼
AnalyticsEventDispatcher
  │  feature flag ANALYTICS_EVENTS_V1 (default OFF → no-op)
  ▼
Registry allowlist → Validator → Serializer → Outbox
```

## Authority boundary

| Layer | Owns |
|---|---|
| ReflectionManager | Educational reflection validation + capture |
| Learning Session / Journey | Session aggregate truth |
| EducationalStateService | Experience Educational State assembly (unchanged) |
| Twin / Recommendation | Unchanged — no emits, no imports |
| Analytics | Observation after successful capture only |

## Emit points (authoritative only)

| Lifecycle | Event | When |
|---|---|---|
| Submit | `reflection.submitted` | After successful `capture` attaches CAPTURED reflection |
| Complete | `reflection.completed` (`processing_status=completed`) | Same successful capture transaction |

Failed validation / capture does **not** emit. Capture without `user_id` does not emit (callers remain responsible for providing opaque analytics identity).

## Fail-open

Dispatcher / registry / validation / outbox failures are caught and logged (`analytics.emit_failed`). Reflection capture always succeeds for the student when educational rules pass.
