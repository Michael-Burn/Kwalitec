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

## Phase B amendment (2026-07-24)

Phase B registers and emits **Study Session** events only:

| Event | Authoritative lifecycle point | Notes |
|---|---|---|
| `session.started` | After `StudySessionService.start_session` Pending→In Progress commit | Idempotent start does not re-emit |
| `session.completed` | After `finish_session` / `record_practice_outcome` persistence | `completion_status`: `completed` \| `abandoned_after_start` |

Canonical cancel / abandon form is **`session.completed` + `abandoned_after_start`** (PRD-001 §7.4). No `session.cancelled` type.

Emit path remains fail-open and flag-gated. Educational algorithms, Twin, EducationalState, and recommendation engine are unchanged. Builders live in `app/infrastructure/analytics/session_events.py`.

## Phase C amendment (2026-07-24)

Phase C registers and emits **Reflection** events only (in addition to Phase B Session events):

| Event | Authoritative lifecycle point | Notes |
|---|---|---|
| `reflection.submitted` | After `ReflectionManager.capture` succeeds | Metadata only — no body text; `student_id` is opaque int |
| `reflection.completed` | Same successful capture transaction | `processing_status`: `completed` |

Emit requires an opaque integer `user_id` passed into capture / `collect_reflection` (analytics identity only). Educational reflection algorithms, Twin, EducationalState, and recommendation engine are unchanged. Builders live in `app/infrastructure/analytics/reflection_events.py`.

## Phase D amendment (2026-07-24)

Phase D registers and emits **Educational State snapshot** observation only (in addition to Phases B–C):

| Event | Authoritative lifecycle point | Notes |
|---|---|---|
| `educational_state.snapshot` | After `EducationalStateService.load` fresh `_assemble` when content hash changes | Payload: `snapshot_id` + `content_hash` only (PRD-001 §7.4) |

EducationalStateService remains the sole Educational State authority. Content hashing runs inside the ESS package; analytics never imports ESS and never stores Educational State / Twin / Learning Evidence / recommendation payloads. Emit is fail-open and flag-gated. Material-change gating uses a process-scoped last-emitted hash so identical page views do not re-emit. Twin algorithms, recommendation engine, Study Session, and Reflection are unchanged. Builders live in `app/infrastructure/analytics/educational_state_events.py`.

## Phase E amendment (2026-07-24)

Phase E registers Journey + Twin evolution observation (in addition to Phases B–D):

| Event | Authoritative lifecycle point | Notes |
|---|---|---|
| `twin.evolved` | After `TwinRepository.persist_birth_twin` / `persist_successor_twin` commit | Payload: `twin_snapshot_id`, `twin_version`, `evolution_reason` (`birth`\|`successor`), `snapshot_hash` — Twin payload FORBIDDEN |
| `journey.progressed` | After durable `LearningJourneyRepository.save` (when adapter exists) | Payload: `journey_id`, `curriculum_node_id`, `transition_id`. Production emit deferred (ADR-026) |

Twin snapshot hashing runs at the Twin persist boundary over codec JSON; analytics receives digest only. Journey builders ship; engine is not hooked (no persistence). See [`ADR-026`](ADR-026-phase-e-journey-twin-observation.md). Educational algorithms, EducationalState, recommendations, Session, and Reflection are unchanged. Builders live in `twin_events.py` / `journey_events.py`.

## EP-002 amendment (2026-07-24)

EP-002 adds **operational readiness** without enabling the flag:

| Capability | Implementation |
|---|---|
| Durable SQL outbox | `sqlalchemy_store.SqlOutboxSink` |
| Retry worker + DLQ | `worker.AnalyticsOutboxWorker` |
| Replay | `replay.AnalyticsReplayService` + CLI |
| Retention / cleanup | `cleanup.AnalyticsRetentionEnforcer` |
| Privacy ops | `privacy.AnalyticsPrivacyService` (delete / export / consent / audit) |
| Infra metrics | `metrics.AnalyticsOperationalMetrics` |
| Ops CLI | `analytics-worker-once`, `analytics-replay`, `analytics-retention`, `analytics-delete-user`, `analytics-export-user`, `analytics-export-audit`, `analytics-metrics`, `analytics-verify-consent` |

`ANALYTICS_EVENTS_V1` remains **OFF** by default. Educational behaviour unchanged. Runbooks: `knowledge/product/analytics/ep002/`.

## Related

- PRD-001 v1.1 §§7–11, §16 Phase A, §19
- [`PRODUCT_ANALYTICS_ARCHITECTURE.md`](../../knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md)
- Implementation: `app/infrastructure/analytics/`
- Tests: `tests/infrastructure/analytics/`, `tests/architecture/test_analytics_import_guard.py`
- EP-002: [`knowledge/product/analytics/ep002/`](../../knowledge/product/analytics/ep002/)

## Governance Alignment

Consistent with:

- [Product Vision 2030](../../knowledge/product/vision/PRODUCT_VISION_2030.md) — learning over vanity; privacy; auditable
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — outcomes before engagement; One Runtime
- [Educational Constitution](../../knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — evidence before opinion; no second brain
