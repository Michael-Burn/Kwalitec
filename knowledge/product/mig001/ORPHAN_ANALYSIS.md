# MIG-001 — Orphan Analysis

**Investigation date:** 2026-07-27  
**Subject revision:** `202607240001` (`202607240001_prd001_analytics_event_infrastructure.py`)  
**Comparator head:** `202607260001` (`202607260001_create_recommendation_commitments.py`)

---

## Investigation questions (answered)

### 1. Why does `202607240001` exist?

It is the **PRD-001 Phase A** Alembic revision that creates analytics persistence tables.

Evidence:

- File docstring: “PRD-001 Phase A — Analytics event store tables.”
- Creates `analytics_events`, `analytics_outbox`, `analytics_audit_log`.
- `down_revision = "202607230002"` (then-current production tip after PR-001 RBAC).
- Introduced in commit `0cf8541` — `feat(analytics): implement passive event infrastructure (Phase A)` (2026-07-24).
- Documented in `knowledge/product/analytics/PHASE_A_IMPLEMENTATION_REPORT.md` and ADR-025.

### 2. Was it intended to become part of the production migration chain?

**Yes.**

Evidence:

- Parents the then-documented production head (`202607230002`).
- ADR-025 (Accepted) mandates these tables as the analytics persistence contract.
- `knowledge/VERSION_1_READINESS.md` marks Analytics **COMPLETE (ops ready; flag OFF)** citing PRD-001 Phases A–E + EP-002.
- Pilot / EP-008.2B go-live materials require migrations applied for the three analytics tables and record local upgrade to `202607240001` (`knowledge/product/ep008_2b_stage1_pilot_readiness_closure/GO_LIVE_CHECKLIST.md`).
- Primary local DB `instance/kwalitec.sqlite3` is stamped at `202607240001`.

### 3. Was it replaced by another implementation?

**No.**

Evidence searched: repository-wide for alternate analytics store migrations, superseding ADRs, and “analytics tables replaced” language.

- No later Alembic revision recreates or replaces `analytics_*` tables.
- EP-002 explicitly reuses Phase A tables (`knowledge/product/analytics/ep002/OPERATIONAL_READINESS_REPORT.md`: “No Alembic revision added”).
- ADR-025 remains **Accepted**; ADR-026 only defers Journey *production emit*, not the schema.
- Runtime package `app/infrastructure/analytics/` and models `app/models/analytics_events.py` still implement this schema.

### 4. Is it dead code?

**No.**

Evidence:

- Full infrastructure package + ORM models + CLI registration in `app/__init__.py`.
- Emit hooks exist in educational paths (Session, Reflection, Educational State, Twin, Journey observe helpers) — gated by `ANALYTICS_EVENTS_V1` (default OFF).
- Test suite under `tests/infrastructure/analytics/` exercises SQL store / outbox paths.
- Product status: “shipped” with flag OFF (`knowledge/product/analytics/README.md`).

“No later migration depends on `202607240001`” is **expected for a head**, not evidence of dead code.

### 5. Does runtime still depend on the three analytics tables?

See [`DEPENDENCY_ANALYSIS.md`](DEPENDENCY_ANALYSIS.md). Short answer: **yes for the analytics subsystem when the flag is ON or ops CLI runs; educational paths no-op when the flag is OFF but still import emit helpers.** Models are registered at app startup regardless of flag.

### 6. Would deleting the migration break anything?

**Yes — high severity.** See [`RISK_MATRIX.md`](RISK_MATRIX.md) Option A.

Immediate breaks:

- DBs already stamped `202607240001` (at least `instance/kwalitec.sqlite3`) become history-inconsistent.
- Fresh `flask db upgrade` would never create analytics tables while models/SQL stores remain.
- Pilot / EP-002 runbooks and privacy workflows that assume tables exist would be false.
- SQL integration tests that hit real tables would fail.

### 7–9. Merge vs rebase vs preserve

See [`RECOMMENDED_RESOLUTION.md`](RECOMMENDED_RESOLUTION.md). Summary:

- Deleting analytics is incorrect.
- Merging heads can restore a single tip but does not fix the misparent of `202607260001`.
- Reparenting / rebasing **the commitments migration** onto `202607240001` is the architecturally correct linearization **if** no environment has already applied `202607260001` from the wrong parent.
- Preserving analytics leaves intentional empty tables while the flag is OFF — by design (ADR-025), not accidental unused schema.

### 10. Safest release decision?

**Keep `202607240001`. Do not treat it as an orphan. Resolve dual heads by correcting or merging the EP-008.3A branch (`202607260001`).**

---

## Hypothesis under test (from MIG-001 brief)

> “Nothing references `202607240001` … strongly suggests an orphaned migration branch.”

### Verdict: **Hypothesis falsified.**

| Claim | Finding |
|---|---|
| Nothing references the revision id | True as a grep fact for *child* migrations; false as an orphan signal — heads have no children by definition |
| Orphaned branch | False — connected main-line tip after `202607230002` |
| Dead / cancelled feature | False — PRD-001 Approved; Phases A–E + EP-002 shipped; flag-gated |

The revision that creates the dual-head *problem* is `202607260001` parenting `202611120001`.
