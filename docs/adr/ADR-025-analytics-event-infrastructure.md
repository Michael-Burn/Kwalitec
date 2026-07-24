# ADR-025 — Analytics Event Infrastructure

**Status:** Accepted  
**Date:** 2026-07-24  
**Milestone:** EP-001 / PRD-001 Phase A  
**Authority:** Architectural · Privacy · Product Analytics  
**PRD:** [`knowledge/prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md`](../../knowledge/prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md) v1.1  

---

## Context

PRD-001 requires first-party learning analytics events for private-beta educational validation (O1, O2, O7, journey/state observation). No collectors exist today. Before any Session, reflection, journey, Educational State, or Twin observation emits, the platform needs a **passive** event pipeline: schema, validation, registry, versioning, serialization, correlation, idempotency, audit metadata, outbox, retention skeleton, and a kill switch.

Educational authorities (Twin, Evidence, Mission, Journey, Reflection, EducationalStateService) must remain the only sources of educational truth. Analytics must **observe only**.

## Decision

### 1. Bounded context

Analytics event infrastructure lives under:

```
app/infrastructure/analytics/
```

It is operational observation infrastructure — **not** an educational engine and **not** a second Educational State.

Version 2 `app/infrastructure/events/` (IntegrationEvent) remains the V2 educational-integration bus. PRD-001 analytics events are a **separate** catalogue and store.

### 2. Envelope contract

Every analytics event carries:

| Field | Role |
|---|---|
| `event_id` | Stable UUID identity |
| `event_type` | Allowlisted type string |
| `schema_version` | Integer schema version (`AnalyticsEventVersion`) |
| `user_id` | Owning student (opaque integer id) |
| `occurred_at` | Event time (UTC) |
| `idempotency_key` | Unique per `(user_id, event_type, entity_key)` |
| `correlation_id` | Request / pipeline linkage |
| `payload` | Metadata-only dict (≤ 8 KiB serialized) |
| `audit` | Emit-path audit metadata (source, flag state, sink) |

### 3. Persistence

Alembic adds append-only tables:

- `analytics_events` — durable event rows (no application UPDATE of body)
- `analytics_outbox` — fail-open enqueue / retry queue
- `analytics_audit_log` — purge, deletion, export, emit-failure audits (36-month policy)

Idempotency: unique constraint on `(user_id, event_type, idempotency_key)`.

### 4. Dispatch path (fail-open, low overhead)

```
caller → AnalyticsEventDispatcher.dispatch(event)
       → feature flag gate (ANALYTICS_EVENTS_V1)
       → validator + registry allowlist
       → serialize
       → outbox enqueue (approved write contract)
       → return DispatchResult (never raises into educational UX)
```

- Feature flag **defaults OFF** → dispatcher is a pure no-op.
- Phase A ships **no domain emitters** (no Session / reflection / journey / ESS / Twin hooks).
- Synchronous educational request paths must not perform analytics DB work beyond the approved outbox contract when the flag is later enabled; Phase A keeps the flag off so runtime behaviour is unchanged.

### 5. Authority boundaries (binding)

Analytics **must never**:

- calculate readiness, mastery, recommendations, or missions
- modify Twin, EducationalState, or Learning Evidence
- store free-text reflection bodies or exam PII
- import Twin belief calculators or recommendation ranking modules

Architecture tests enforce import guards.

### 6. Feature flag

| Name | Default | Effect |
|---|---|---|
| `ANALYTICS_EVENTS_V1` | **off** | When off, `dispatch` returns `DISABLED` and writes nothing |

Environment: truthy `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1`.

### 7. Retention / purge

Purge job **skeleton** only in Phase A (callable, batch-sized, audited). Enforcement of 18-month raw / 36-month aggregate windows runs before cohort expansion beyond dogfood (PRD §7.1).

## Alternatives considered

1. **Reuse V2 IntegrationEvent bus for PRD-001** — rejected. Different catalogue, privacy payload rules, retention, and idempotency semantics; risk of coupling educational integration to product analytics.
2. **Synchronous insert on educational commit without outbox** — deferred. Outbox is the approved write contract for fail-open retry (PRD §9).
3. **Client-side beacons** — rejected (PRD §9 authenticity; no public ingest).

## Consequences

**Benefits:** Passive, flag-gated pipeline ready for Phases B–E; One Educational Truth preserved; measurable emit budgets.

**Trade-offs:** Two event systems (V2 integration vs analytics) until a future consolidation ADR; Phase A adds schema without product metrics yet.

**Rollback:** Leave flag off (default). Do not drop Twin / ESS / mission tables.

## Related

- PRD-001 v1.1 §§7–11, §16 Phase A, §19
- [`PRODUCT_ANALYTICS_ARCHITECTURE.md`](../../knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md)
- Implementation: `app/infrastructure/analytics/`
- Tests: `tests/infrastructure/analytics/`, `tests/architecture/test_analytics_import_guard.py`

## Governance Alignment

Consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — learning over vanity; privacy; auditable
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — outcomes before engagement; One Runtime
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — evidence before opinion; no second brain
