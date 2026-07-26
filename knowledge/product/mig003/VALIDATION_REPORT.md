# MIG-003 — Validation Report

**Programme:** MIG-003 — Migration Contract Alignment  
**Date:** 2026-07-27  
**Environment:** local development (SQLite; project `.venv`)

---

## 1. `flask db heads`

**Expected:** exactly one head `202607260001`  
**Observed:**

```text
202607260001 (head)
```

**Pass.**

Also: `flask db current` → `202607260001 (head)` (local DB already at tip).

```text
ScriptDirectory.get_current_head() → 202607260001
ScriptDirectory.get_heads() → ['202607260001']
```

---

## 2. Targeted operational tests

**Command:**

```bash
.venv/bin/pytest \
  tests/operational/test_alpha_configuration.py::test_alembic_head_and_migration_files \
  tests/operational/test_alpha_configuration.py::test_checklist_doc_complete \
  -v --tb=short
```

**Outcome:** `2 passed`

| Test | Result |
|---|---|
| `test_alembic_head_and_migration_files` | PASSED (was the MIG-002 residual stale-pin failure) |
| `test_checklist_doc_complete` | PASSED |

---

## 3. Full pytest

**Command:** `.venv/bin/pytest -q --tb=line`

| Metric | Count |
|---|---|
| **Passed** | **43325** |
| **Failed** | **31** |
| **Skipped** | **7** |
| Duration | ~209s |

### Comparison to MIG-002 baseline

| Suite | MIG-002 | MIG-003 |
|---|---|---|
| Passed | 43324 | 43325 |
| Failed | 32 | 31 |
| Skipped | 7 | 7 |

Net: **−1 failure / +1 pass** — the stale `ALEMBIC_HEAD` assertion is resolved.

---

## 4. Alembic-related residual failures

**None.**

No remaining failure asserts `202607230002` as the current head, raises `MultipleHeads`, or fails `get_current_head()` against the operational pin.

The sole Alembic-adjacent failure previously listed in MIG-002 (`test_alembic_head_and_migration_files`) now **passes**.

### Note on `test_startup_service.py::test_empty_database_applies_migrations_and_creates_admin`

Still **FAILED**, but for an **unrelated message assertion**: expects log `'Admin created.'`; runtime emits `'Admin created with Founder RBAC.'`. Migration apply itself succeeds (`Applying migrations...` / `Migrations complete.`). Out of MIG-003 scope — not a stale head pin.

---

## 5. Remaining failures (non-Alembic; not fixed)

All 31 failures are pre-existing / out-of-scope product, architecture purity, snapshot, brand, or message-wording issues. Examples:

- Education OS snapshots / architecture purity / independence
- Recommendation dual-run / recovery injection output diffs
- Brand identity / CSS budget / founder IA wording
- CLI / startup admin log string expectations
- EIP / IA / PTP student-facing copy assertions

Per programme instructions: **no unrelated test fixes**.

---

## 6. Migration files

**MIG-003 modified zero files under `migrations/`.**  
(`git diff` on this programme’s contract files touches only CI, helpers, and the alpha checklist. Pre-existing MIG-002 reparent dirty state in the working tree, if present, is not part of MIG-003.)

---

## Success criteria checklist

| Criterion | Status |
|---|---|
| Exactly one authoritative head in ops contracts | Met (`202607260001`) |
| CI pin updated | Met |
| `ALEMBIC_HEAD` updated | Met |
| Alpha checklist updated | Met |
| No stale Category A asserts of `202607230002` | Met |
| No Alembic-related pytest failures remaining | Met |
| No migration files changed by this programme | Met |
| No application behaviour changed | Met |
| No unrelated tests modified | Met |
