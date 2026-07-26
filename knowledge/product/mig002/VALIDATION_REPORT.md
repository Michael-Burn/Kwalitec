# MIG-002 — Validation Report

**Programme:** MIG-002 — Migration Graph Repair  
**Date:** 2026-07-27  
**Environment:** local development (SQLite; `DATABASE_URL` unset → `instance/kwalitec.sqlite3`)

---

## Command results

### 1. `flask db heads`

**Expected:** exactly one head `202607260001`  
**Observed:**

```text
202607260001 (head)
```

**Pass.**

`ScriptDirectory.get_heads()` → `['202607260001']`.  
`ScriptDirectory.get_current_head()` → `202607260001` (no longer raises multiple-heads).

---

### 2. `flask db history`

**Expected tip adjacency:**

```text
202607240001
↓
202607260001
```

**Observed (verbose tip):**

```text
Rev: 202607260001 (head)
Parent: 202607240001

Rev: 202607240001
Parent: 202607230002
```

**Pass.**

---

### 3. `flask db current` (before upgrade)

**Expected:** remain `202607240001` (reparent must not auto-upgrade)  
**Observed:**

```text
202607240001
```

**Pass.** Startup during Flask CLI reported behind-head but did not apply migrations on CLI inspect commands.

---

### 4. `flask db upgrade`

**Observed:**

```text
Running upgrade 202607240001 -> 202607260001, Create recommendation_commitments table (EP-008.3A).
```

**Pass.** Existing local database upgraded successfully.

---

### 5. `flask db current` (after upgrade)

**Expected:** `202607260001`  
**Observed:**

```text
202607260001 (head)
```

App log: `Alembic: database is up to date.`

**Pass.**

---

### 6. Fresh database upgrade

**Command pattern:** temporary `DATABASE_URL=sqlite:////tmp/kwalitec_mig002_fresh_*.sqlite3` then `flask db upgrade`.

**Observed:** full chain from empty → `202607260001`, including final step:

```text
Running upgrade 202607240001 -> 202607260001, Create recommendation_commitments table (EP-008.3A).
```

Post-upgrade `flask db current` / `flask db heads` both: `202607260001 (head)`.

**Pass.**

---

### 7. `flask db branches` (post-repair)

`202611120001` branchpoint children are only:

```text
→ 202607190001
→ 202607130001
```

`202607260001` is no longer listed under that branchpoint.

**Pass.**

---

## Pytest

**Command:** `pytest -q --tb=line`  
**Outcome:** `32 failed, 43324 passed, 7 skipped` (~208s)

### Failures recorded

| Test | Classification vs MIG-002 |
|---|---|
| `tests/operational/test_alpha_configuration.py::test_alembic_head_and_migration_files` | **Stale pin** — asserts `ALEMBIC_HEAD == "202607230002"`; actual unique head is now `202607260001`. Expected residual from MIG-001 follow-up list (CI / helpers / checklist not updated in this programme). |
| `tests/test_startup_service.py::TestStartupService::test_empty_database_applies_migrations_and_creates_admin` | **Unrelated message assertion** — expects log `'Admin created.'`; runtime emits `'Admin created with Founder RBAC.'`. Migrations themselves applied (`Applying migrations...` / `Migrations complete.`). |
| Education OS architecture / snapshot suite (independence, page snapshots, purity, twin input, authority, consumer_chain, …) | **Pre-existing / out of MIG-002 schema scope** — not caused by `down_revision` reparent. |
| Brand / IA / EIP / PTP / CSS budget / 500-page / CLI admin wording tests | **Pre-existing product/surface assertions** — unrelated to Alembic graph linearity. |

### Alembic-adjacent residual (not fixed here)

Stale single-head contract still documents / asserts `202607230002`:

- `tests/operational/helpers.py` — `ALEMBIC_HEAD = "202607230002"`
- `.github/workflows/ci.yml` — `assert head == "202607230002"`
- `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` — expect `202607230002`

These were already stale after analytics (`202607240001`) and remain stale after commitments (`202607260001`). Updating them was **out of MIG-002 required changes**.

---

## Success criteria checklist

| Criterion | Status |
|---|---|
| Exactly one Alembic head | Met (`202607260001`) |
| Linear history at tip | Met (`… → 202607240001 → 202607260001`) |
| Fresh DB upgrade succeeds | Met |
| Existing local DB upgrades | Met |
| No new migration created | Met |
| No existing schema SQL changed | Met |
| Only `down_revision` modified | Met (1 line in one file) |
