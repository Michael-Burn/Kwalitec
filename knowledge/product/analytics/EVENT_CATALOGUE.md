# PRD-001 Event Catalogue

**Programme:** EP-001 / PRD-001  
**Authority:** [`PRD-001_LEARNING_ANALYTICS_PHASE1.md`](../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md) v1.1 §7.4 · [`ADR-026`](../../../docs/adr/ADR-026-phase-e-journey-twin-observation.md)  
**Updated:** 2026-07-24 (Phase E)

Payloads are **metadata only**. EducationalState, Twin, Learning Evidence, and recommendation payloads are forbidden in the analytics store. Reflection **body text is never stored**. Educational State / Twin snapshot events store **hash + metadata only**.

| Event | Phase | Status | Required payload keys | Optional metadata | Notes |
|---|---|---|---|---|---|
| `analytics.infrastructure_probe` | A | Registered | — | `probe` | Infrastructure health only — not a learning metric |
| `session.started` | B | **Registered + emitted** | `session_id`, `mission_id` | `curriculum_node_id` | After Pending→In Progress commit |
| `session.completed` | B | **Registered + emitted** | `session_id`, `mission_id`, `completion_status` | `started_at`, `duration_seconds`, `topic_id`, `abandon_reason` | `completion_status`: `completed` \| `abandoned_after_start` |
| `reflection.submitted` | C | **Registered + emitted** | `reflection_id`, `session_id`, `student_id`, `reflection_type` | — | After successful `ReflectionManager.capture`; `student_id` = opaque int |
| `reflection.completed` | C | **Registered + emitted** | `reflection_id`, `processing_status` | — | Same capture transaction; `processing_status`: `completed` |
| `educational_state.snapshot` | D | **Registered + emitted** | `snapshot_id`, `content_hash` | — | After material ESS assembly; SHA-256 hex; envelope carries `user_id` / `schema_version` / `occurred_at` / `correlation_id` |
| `journey.progressed` | E | **Registered** (production emit deferred) | `journey_id`, `curriculum_node_id`, `transition_id` | — | Post-save observe helper shipped; durable Journey repository pending (ADR-026). Supersedes PRD name `journey.milestone_reached` |
| `twin.evolved` | E | **Registered + emitted** | `twin_snapshot_id`, `twin_version`, `evolution_reason`, `snapshot_hash` | — | After TwinRepository birth/successor commit; hash + metadata only — Twin payload FORBIDDEN |

## Session identity

LXP Study Session is 1:1 with a daily Mission. Canonical `session_id` = `mission:{mission_id}`.

## Reflection identity

Learning Journey / Learning Session structured reflection uses the domain `reflection_id` (e.g. `ref-…`). Canonical `reflection_type` for Phase C = `journey_session`. Envelope `user_id` and payload `student_id` are the same privacy-compliant opaque integer.

## Educational State snapshot identity

`snapshot_id` is a new opaque id per material content-hash change. `content_hash` is SHA-256 hex of the canonical assembled Educational State representation (computed by EducationalStateService — never stored as payload). Envelope `user_id` is the privacy-compliant opaque integer student identifier. Emit is gated on material hash change (not every page view).

## Twin evolution identity

`twin_snapshot_id` is the durable TwinRepository snapshot id. `twin_version` is the monotonic persist `sequence` as a string. `evolution_reason` is the canonical enum `birth` \| `successor`. `snapshot_hash` is SHA-256 hex of the Twin codec JSON (computed at Twin persist authority — Twin payload never enters analytics).

## Journey progression identity

`journey_id` is the Learning Journey aggregate id. `curriculum_node_id` is the journey topic id. `transition_id` is a canonical `JourneyTransitionEvent` value. Production emit requires a durable repository adapter calling `observe_journey_progressed` after `save` (ADR-026).

## Abandon / cancel

There is **no** `session.cancelled` event type. Canonical lifecycle uses:

```text
session.completed  +  completion_status=abandoned_after_start
```

Mapped from LXP `finish_session(..., completion_status="no")` with optional `abandon_reason=completion_no`.

## Envelope (all events)

`event_id`, `event_type`, `user_id`, `occurred_at`, `idempotency_key`, `schema_version`, `correlation_id`, `payload`, `audit`.

Idempotency: unique per `(user_id, event_type, entity_key)` where entity_key is `session_id` for Session events, `reflection_id` for Reflection events, `snapshot_id` for Educational State snapshot events, `twin_snapshot_id` for Twin evolution, and `journey_id:transition_id:…` for Journey progression.
