# PRD-001 Phase D — Architecture

**ADR:** [`docs/adr/ADR-025-analytics-event-infrastructure.md`](../../../docs/adr/ADR-025-analytics-event-infrastructure.md) (Phase D amendment)  
**Catalogue:** [`EVENT_CATALOGUE.md`](EVENT_CATALOGUE.md)

## Diagram

```
Experience surface (Home / Journey / Revision / …)
  │
  ▼
EducationalStateService.load
  │  instance cache miss
  ▼
_assemble from Twin / Adaptive / Mission / Journey ports  ← AUTHORITATIVE
  │  Educational State calculated (assembler only — no new math)
  ▼
content_hash = SHA-256(canonical snapshot)   ← ESS authority
  │  compare to process-scoped last-emitted hash
  │  skip if unchanged (material-change gate)
  ▼
_observe_snapshot_if_material (fail-open)
  │  snapshot_id + content_hash only
  ▼
educational_state_events builders (metadata + hash — no ESS payload)
  ▼
AnalyticsEventDispatcher
  │  feature flag ANALYTICS_EVENTS_V1 (default OFF → no-op)
  ▼
Registry allowlist → Validator → Serializer → Outbox
```

## Authority boundary

| Layer | Owns |
|---|---|
| EducationalStateService | Sole Educational State assembly for experience |
| Twin / Adaptive / Mission / Journey | Educational port truth (unchanged) |
| ESS `content_hash` helper | Deterministic hash of assembled snapshot |
| Analytics | Observation after successful assembly only — never derives ESS |

## Snapshot content (allowed)

| Field | Location | Notes |
|---|---|---|
| `snapshot_id` | Payload | New id per material change |
| `content_hash` | Payload | SHA-256 hex (PRD-001 §7.4) |
| `user_id` | Envelope | Privacy-compliant student identifier |
| `schema_version` | Envelope | Analytics event schema |
| `occurred_at` | Envelope | Timestamp |
| `correlation_id` | Envelope | Auto-filled if omitted |
| `idempotency_key` | Envelope | `(user_id, event_type, snapshot_id)` |

**Forbidden in analytics store:** Educational State payload, Twin payload, Learning Evidence, recommendations, mastery/readiness values as educational scores.

## Emit points

| Lifecycle | Event | When |
|---|---|---|
| Material ESS assembly | `educational_state.snapshot` | After `_assemble` on cache miss when content hash differs from last successful/disabled observation |

Cache hits within a request do not re-hash or re-emit. Identical content after `clear_cache` does not re-emit.

## Fail-open

Dispatcher / registry / validation / outbox / hash failures are caught and logged (`analytics.emit_failed`). Educational State `load()` always returns the assembled snapshot when ports succeed.
