# ADR-026 — Phase E Journey & Twin Evolution Observation

**Status:** Accepted  
**Date:** 2026-07-24  
**Milestone:** EP-001 / PRD-001 Phase E  
**Authority:** Architectural · Privacy · Product Analytics  
**PRD:** [`knowledge/prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md`](../../knowledge/prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md) v1.1  
**Supersedes naming (journey only):** PRD-001 §7.4 `journey.milestone_reached` → Phase E authorised `journey.progressed`

---

## Context

Phase E authorises observe-only analytics for:

| Event | Metadata (authorised) |
|---|---|
| `journey.progressed` | journey id, curriculum node id, transition id, timestamp, correlation_id, schema_version |
| `twin.evolved` | twin_version, evolution_reason (canonical enum), snapshot_hash (if approved), timestamp, correlation_id |

Lifecycle mandate:

```text
Journey / Twin → business logic → persistence → successful completion → Analytics Dispatcher
```

Analytics must never derive or modify Twin or Journey state. Twin remains sole Twin truth. Journey remains authoritative for progression.

### Journey blocker

`LearningJourneyEngine` is the educational progression authority but **never persists**.  
`LearningJourneyRepository` is an ABC with **no production infrastructure adapter** (in-memory test helper only).

Emitting `journey.progressed` from the engine (pre-persist) would violate the mandated lifecycle. Inventing a parallel curriculum-completion emit path would undermine Journey authority.

### Twin path (approved)

Durable Twin succession already commits via `TwinRepository.persist_birth_twin` / `persist_successor_twin`. The codec already produces canonical JSON (`encode_twin`). Hashing that encoded string at the Twin persist boundary yields an opaque `snapshot_hash` **without** passing Twin aggregates or beliefs into analytics — same pattern as Phase D ESS `content_hash`.

### Naming

Phase E programme authorisation uses `journey.progressed` (transition + curriculum node). PRD-001 §7.4 still lists `journey.milestone_reached`. This ADR adopts the authorised Phase E name; PRD catalogue docs are amended accordingly. Milestone-style product metrics remain out of scope.

---

## Decision

### 1. Twin — ship observe-only emit

- Register and emit `twin.evolved` **after** successful Twin snapshot commit (SQLAlchemy and in-memory adapters).
- Payload (metadata only): `twin_snapshot_id`, `twin_version` (= durable `sequence` as string), `evolution_reason` (`birth` \| `successor`), `snapshot_hash` (SHA-256 hex of codec JSON).
- Hash computed in `app/application/twin_repository/` — analytics receives digest only.
- Analytics never imports Twin domain / belief calculators.
- Fail-open; feature flag `ANALYTICS_EVENTS_V1` default OFF.

### 2. Journey — builders + post-persist contract; production emit deferred

- Register `journey.progressed` and ship builders / validators / unit tests.
- Provide Application-layer `observe_journey_progressed(...)` for callers to invoke **only after** durable `LearningJourneyRepository.save` succeeds, with explicit `transition_id`.
- **Do not** hook `LearningJourneyEngine` (no persistence).
- **Do not** invent a production repository in this phase.
- Production emit remains **deferred** until a durable Journey repository adapter lands and calls the observe helper after save.

### 3. STOP condition satisfaction

Phase E does **not** require exposing Twin internals to analytics. Hash-at-boundary is approved. Work continues for Twin; Journey production wiring waits on persistence.

---

## Consequences

**Benefits:** Twin evolution observable without second Twin brain; Journey catalogue ready without false emits; One Educational Truth preserved.

**Trade-offs:** Journey progression is not observed in production until repository adapter ships; PRD name `journey.milestone_reached` retired for Phase E.

**Rollback:** Leave `ANALYTICS_EVENTS_V1` off. Twin/Journey educational algorithms unchanged.

---

## Related

- ADR-025 Phase E amendment
- [`EVENT_CATALOGUE.md`](../../knowledge/product/analytics/EVENT_CATALOGUE.md)
- Implementation: `app/infrastructure/analytics/twin_events.py`, `journey_events.py`
