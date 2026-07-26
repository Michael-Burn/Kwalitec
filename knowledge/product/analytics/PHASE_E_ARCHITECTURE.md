# PRD-001 Phase E — Architecture

**ADR:** [`docs/adr/ADR-025-analytics-event-infrastructure.md`](../../../docs/adr/ADR-025-analytics-event-infrastructure.md) (Phase E amendment) · [`ADR-026`](../../../docs/adr/ADR-026-phase-e-journey-twin-observation.md)  
**Catalogue:** [`EVENT_CATALOGUE.md`](EVENT_CATALOGUE.md)

## Diagram — Twin

```
Twin Update / Calibration
  │
  ▼
TwinRepository.persist_birth_twin / persist_successor_twin
  │  encode_twin → durable commit
  ▼
snapshot_hash = SHA-256(codec JSON)   ← Twin persist authority
  │
  ▼
_observe_twin_evolved (fail-open)
  │  twin_snapshot_id + twin_version + evolution_reason + snapshot_hash
  ▼
twin_events builders (metadata + hash — no Twin payload)
  ▼
AnalyticsEventDispatcher
  │  feature flag ANALYTICS_EVENTS_V1 (default OFF → no-op)
  ▼
Registry allowlist → Validator → Serializer → Outbox
```

## Diagram — Journey (contract; production emit deferred)

```
LearningJourneyEngine (progression authority — never persists)
  │
  ▼
Caller / future durable LearningJourneyRepository.save
  │  successful persistence
  ▼
observe_journey_progressed (fail-open)   ← ADR-026 post-save contract
  │  journey_id + curriculum_node_id + transition_id
  ▼
journey_events builders → Dispatcher → Registry → Outbox
```

## Authority boundary

| Layer | Owns |
|---|---|
| TwinRepository | Sole durable Twin snapshot persistence |
| Twin `content_hash` / snapshot_hash helper | Deterministic hash of codec JSON |
| Learning Journey Engine | Educational progression (unchanged; no persist) |
| Analytics | Observation after successful Twin persist / Journey save only |

## Twin snapshot content (allowed)

| Field | Location | Notes |
|---|---|---|
| `twin_snapshot_id` | Payload | Durable opaque snapshot id |
| `twin_version` | Payload | Durable sequence as string |
| `evolution_reason` | Payload | Canonical enum: `birth` \| `successor` |
| `snapshot_hash` | Payload | SHA-256 hex of codec JSON |
| `user_id` | Envelope | Privacy-compliant student identifier |
| `schema_version` | Envelope | Analytics event schema |
| `occurred_at` | Envelope | Timestamp |
| `correlation_id` | Envelope | Auto-filled if omitted |

**Forbidden:** Twin payload, Twin metrics, mastery/readiness, Learning Evidence, Educational State, recommendations.

## Journey content (allowed)

| Field | Location | Notes |
|---|---|---|
| `journey_id` | Payload | Journey aggregate identity |
| `curriculum_node_id` | Payload | Topic / curriculum node identity |
| `transition_id` | Payload | Canonical JourneyTransitionEvent value |
| Envelope fields | Envelope | timestamp, correlation_id, schema_version, user_id |

## Fail-open

Dispatcher / registry / validation / outbox / hash failures are caught and logged. Twin persist and Journey save always retain educational success when domain work succeeds.
