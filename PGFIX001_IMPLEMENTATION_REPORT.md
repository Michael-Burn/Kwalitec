# PGFIX001_IMPLEMENTATION_REPORT.md

**Programme:** PGFIX-001 — PostgreSQL Persistence Fix  
**Date:** 2026-07-30  
**Trigger:** RCV-001 STEP 2 blocked on production Postgres  
**Scope:** Educational Intelligence generation-store persistence only  
**Out of scope:** Production recovery, Runtime, Deriver, Publication, architecture redesign

---

## Executive Summary

`SqlAlchemyGenerationStore.append_snapshot()` inserted educational nodes and then issued a lineage existence **SELECT**. That SELECT triggered SQLAlchemy **autoflush**, which flushed pending node rows **before** the parent snapshot row existed. PostgreSQL correctly rejected the insert on `ei_educational_nodes.snapshot_id_fkey`. Local SQLite had masked the bug because foreign keys were off (`PRAGMA foreign_keys=0`).

**Minimal fix:** flush chain/generation/snapshot rows before inserting dependent nodes, and wrap the lineage existence query in `session.no_autoflush`.

Verified:

- SQLite with foreign keys **ON** (suite default)
- Disposable PostgreSQL database (`kwalitec_pgfix001`) — Generations 1–7 persist
- Full EI / curriculum-intelligence adapter suite green under FK-enforced SQLite

**Do not re-run RCV-001 until this fix is present in the checkout used against production.**

---

## Failure Sequence (exact)

Inside `append_snapshot`:

1. `EiGenerationChain` / `EiGeneration` added if missing  
2. `EiGenerationSnapshot` **added** (pending)  
3. For each node: `EiEducationalNode` **added** (pending)  
4. `_ensure_lineage_op` runs `EiLineageOperation.query.filter_by(...).first()`  
5. Query invokes **autoflush** of pending objects  
6. SQLAlchemy emits `INSERT INTO ei_educational_nodes …` referencing `snapshot_id`  
7. PostgreSQL FK check: snapshot row not yet inserted → **`ForeignKeyViolation`**  
8. Session enters rollback-needed state; further pipeline work fails

RCV-001 evidence: `knowledge/evidence/releases/RCV001/issues.json`  
(`snap-081e04ecdb0472e1` missing from `ei_generation_snapshots`).

Why local RR-001 succeeded: SQLite default `PRAGMA foreign_keys=OFF`.

---

## Change Made

### File: `app/infrastructure/adapters/curriculum_intelligence/generation_store.py`

1. **`db.session.flush()`** immediately after adding `EiGenerationSnapshot`, before the node loop — persists parent rows so FK checks succeed.  
2. **`with db.session.no_autoflush:`** around the lineage existence SELECT — prevents incidental autoflush during the idempotent lookup.

No schema/migration changes. No Runtime / Deriver / Publication changes. Transactional + FK integrity preserved (parents first, then children, still one session/transaction).

---

## Tests

### SQLite FK enforcement (suite-wide)

`tests/conftest.py` now registers a SQLAlchemy `connect` listener:

```text
PRAGMA foreign_keys=ON
```

Guard test: `test_sqlite_foreign_keys_are_enforced`.

### PGFIX-001 regression module

`tests/infrastructure/adapters/curriculum_intelligence/test_pgfix001_generation_store.py`

| Test | Backend | Result |
|---|---|---|
| `test_sqlite_foreign_keys_are_enforced` | SQLite | PASS |
| `test_append_snapshot_with_lineage_persists_under_fk` | SQLite + FK | PASS |
| `test_generations_1_through_7_persist` | SQLite + FK | PASS |
| `test_postgres_append_snapshot_with_lineage` | PostgreSQL | PASS |
| `test_postgres_generations_1_through_7` | PostgreSQL | PASS |

PostgreSQL runs require `TEST_POSTGRES_URL`. Marker: `@pytest.mark.postgres` (registered in `pyproject.toml`).

Verification used a **disposable** database `kwalitec_pgfix001` on the Render Postgres instance (created + dropped; product DB `kwalitec` untouched — `ei_generation_snapshots` still 0).

### Broader regression

```text
tests/application/curriculum_intelligence/
tests/infrastructure/adapters/curriculum_intelligence/
→ 102 passed (postgres tests skipped without URL in that run)
```

Re-run with Postgres:

```text
2 passed (append_snapshot + G1–G7)
```

Unrelated pre-existing curriculum_studio failures (checklist counts / flask import independence) are **not** caused by this fix and were not modified.

---

## Commands

```bash
# SQLite FK-enforced (default suite)
python -m pytest \
  tests/infrastructure/adapters/curriculum_intelligence/test_pgfix001_generation_store.py \
  tests/application/curriculum_intelligence/ \
  -m "not postgres" -q

# PostgreSQL regression
TEST_POSTGRES_URL='postgresql+psycopg://…/kwalitec_pgfix001' \
python -m pytest \
  tests/infrastructure/adapters/curriculum_intelligence/test_pgfix001_generation_store.py \
  -m postgres -v
```

---

## Architecture Compliance

| Constraint | Status |
|---|---|
| No architectural redesign | Met |
| No Runtime / Deriver / Publication changes | Met |
| Preserve transactional integrity | Met |
| Preserve FK integrity | Met (and now enforced in SQLite tests) |
| Works on PostgreSQL | Met |
| Continues on SQLite | Met |

---

## Migration Impact

**None.**

---

## Technical Debt

- Full-app `create_all()` on empty Postgres still fails on an unrelated `lee_evidence_events` self-FK uniqueness issue; PGFIX Postgres tests therefore create **EI tables only**. Separate from this programme.
- Production recovery (RCV-001) remains blocked until this fix is deployed/used in the ops checkout.

---

## Final Verdict

**PGFIX-001 PASS.**

Educational Intelligence persistence is correct on PostgreSQL and on SQLite with foreign keys enabled. Generations 1–7 complete and persist. RCV-001 may be resumed only after this fix is in the environment used against production.
