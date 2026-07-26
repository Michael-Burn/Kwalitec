# MIG-001 — Dependency Analysis

**Investigation date:** 2026-07-27  
**Tables:** `analytics_events`, `analytics_outbox`, `analytics_audit_log`  
**Migration:** `202607240001`

---

## Summary

| Consumer class | Depends on tables? | When |
|---|---|---|
| ORM models | Yes (define tables) | Always imported / registered |
| SQL analytics store / outbox / audit | Yes | Flag ON, worker, privacy/purge/replay CLI |
| Educational request path | Soft — emit helpers called | Flag OFF → no writes; Flag ON → outbox/store writes |
| Student UX / Runtime A ranking | No | Analytics must not drive educational truth (ADR-025) |
| EP-008.3A commitments | No (separate table) | Uses `recommendation_commitments` |

**Unreachable migration?** No. Code paths, models, CLI, tests, and local DB stamp all reach this schema. Writes are **feature-flag gated**, not code-deleted.

---

## 1. Models and registration

| Artifact | Evidence |
|---|---|
| `app/models/analytics_events.py` | `__tablename__` = `analytics_events`, `analytics_outbox`, `analytics_audit_log` |
| `app/models/__init__.py` | Imports / exports `AnalyticsEventRecord` (and related) |
| App factory model import | Models loaded so SQLAlchemy metadata includes analytics tables |

---

## 2. Infrastructure package (read/write)

Package: `app/infrastructure/analytics/` (47 Python modules under package + tests).

| Component | Table use | Evidence |
|---|---|---|
| `SqlAnalyticsEventStore` | `analytics_events` | `sqlalchemy_store.py` queries `AnalyticsEventRecord` |
| `SqlOutboxSink` / durable outbox | `analytics_outbox` | `outbox.py`; EP-002 runbook |
| `SqlAnalyticsAuditLog` | `analytics_audit_log` | `audit_log.py`; EP-002 runbook |
| `AnalyticsEventDispatcher` | Via outbox when enabled | `dispatcher.py`; flag gate |
| Worker / replay / purge / privacy | Yes | `worker.py`, `replay.py`, `purge.py`, `privacy.py`, `cli.py` |

Feature flag (`ANALYTICS_EVENTS_V1`): when OFF, `dispatch` returns disabled and **writes nothing** (`feature_flag.py`, ADR-025). That does **not** remove the dependency of the SQL adapters on the tables existing if/when flag or CLI paths run.

---

## 3. Runtime emit call sites (educational observe-only)

| Domain | Call site | Evidence |
|---|---|---|
| Session | `app/services/study_session_service.py` | `emit_session_started` / `emit_session_completed` |
| Reflection | `app/application/learning_session/reflection_manager.py` | `emit_reflection_lifecycle` |
| Educational State | `app/application/educational_state/__init__.py` | `emit_educational_state_snapshot` |
| Twin | `app/application/twin_repository/observation.py` | `emit_twin_evolved` |
| Journey | `app/application/learning_journey/journey_observation.py` | `emit_journey_progressed` (production durable emit deferred per ADR-026) |
| CLI registration | `app/__init__.py` | analytics CLI import |

Note: some `*_telemetry.py` modules under adaptive/twin/bridge adapters are **separate** bridge telemetry (not the PRD-001 SQL tables). They do not replace `analytics_*` dependency analysis for PRD-001.

---

## 4. HTTP / presentation

| Surface | Dependency |
|---|---|
| `app/analytics/` blueprint | Product analytics UI routes exist; Phase A+ docs treat event store as infrastructure behind flag — not a second educational engine |
| Founder / student templates | No direct SQL references to `analytics_events` found as table name in templates |

---

## 5. Tests

| Area | Evidence |
|---|---|
| `tests/infrastructure/analytics/` | Contract, dispatcher, SQL outbox integration, reliability, session/reflection/ESS/twin/journey event tests |
| SQL integration | Imports `SqlAnalyticsEventStore`, creates events against DB |

Removing the migration without removing this suite would leave tests expecting schema that upgrade no longer creates.

---

## 6. Knowledge / ops / release docs that assume tables

- ADR-025 persistence section
- EP-002 production runbook / go-live / recovery / replay / privacy guides
- EP-008.2B pilot readiness / go-live / privacy signoff (migrations present checklist)
- EP-004 analytics activation
- `VERSION_1_READINESS.md` Analytics COMPLETE

---

## 7. Local database evidence

| DB | `alembic_version` | Analytics tables | `recommendation_commitments` |
|---|---|---|---|
| `instance/kwalitec.sqlite3` | `202607240001` | Present | **Absent** |
| Several `instance/ipv*_eval.sqlite3` | Older revisions (`202607160003` / `202607170003`) | Absent | Absent |

Interpretation:

- At least one active local app DB **has applied** the analytics migration.
- The commitments migration has **not** been applied on that same DB (consistent with dual-head blocking clean upgrade to both tips).

**Production hosted DB stamp:** not inspected in this investigation (no production credentials / remote DB in workspace). Absence of remote evidence is stated explicitly — release engineering must verify `alembic_version` on every deployed environment before choosing reparent vs merge (see [`RECOMMENDED_RESOLUTION.md`](RECOMMENDED_RESOLUTION.md)).

---

## 8. Comparator: `recommendation_commitments` dependencies

Not analytics, but relevant to dual-head resolution:

| Consumer | Evidence |
|---|---|
| Model | `app/models/recommendation_commitment.py` |
| Service | `RecommendationCommitmentService` |
| Routes | `app/presentation/student/routes.py`, `app/mission/routes.py` |
| Home / history | `home_service.py`, `history_service.py` |
| EP-008.2B note | Soft log when table missing on SQLite with other head (`GO_LIVE_CHECKLIST.md`) |

Both heads correspond to **live application features**, not disposable stubs.
