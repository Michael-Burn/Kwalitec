# MIG-003 — Operational Contract Update

**Programme:** MIG-003 — Migration Contract Alignment  
**Date:** 2026-07-27  
**Authoritative head:** `202607260001`

---

## Purpose

Align live operational contracts (test helpers, alpha checklist) with the single Alembic tip restored by MIG-002. Migration files were not modified.

---

## Updates

### 1. `tests/operational/helpers.py`

| Field | Value |
|---|---|
| Symbol | `ALEMBIC_HEAD` |
| Previous | `"202607230002"` |
| New | `"202607260001"` |
| Reason | Consumed by `test_alembic_head_and_migration_files` (`get_current_head() == ALEMBIC_HEAD`) and `test_checklist_doc_complete` (checklist must contain the pin string) |
| Validation | Both tests **PASSED** |

### 2. `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md`

| Location | Previous | New |
|---|---|---|
| D8 — Head must be … | `202607230002` | `202607260001` |
| `flask db current` comment | expect `202607230002` | expect `202607260001` |
| Operational caveats — durable flags | upgrade to `202607230002` | upgrade to `202607260001` |

| Field | Value |
|---|---|
| Reason | Live Internal Alpha / RC deploy checklist must name the production tip |
| Validation | `test_checklist_doc_complete` **PASSED** (needle `ALEMBIC_HEAD` present) |

### 3. CI (cross-reference)

See `CI_ALIGNMENT_REPORT.md` for `.github/workflows/ci.yml`.

---

## Startup validation

`StartupService` / `flask` app factory resolve Alembic current vs head dynamically. No hard-coded obsolete revision was present in `app/services/startup_service.py`. Local observation after alignment:

```text
Alembic: current database revision = 202607260001
Alembic: head script revision = 202607260001
Alembic: database is up to date.
```

---

## Intentionally unchanged operational surfaces

| Surface | Why |
|---|---|
| `docs/production/RUNBOOK.md` | Generic “expect head” — no obsolete id |
| `.cursor/RELEASE_CHECKLIST.md` | Generic “expect head” — no obsolete id |
| `tests/ga/test_failure_modes.py` | Mock meta only; not a head contract |
| Historical MIG-001 / MIG-002 docs | Category B/D |
| Migration `down_revision` / revision files | Category C; graph owned by MIG-002 |

---

## Contract statement

Every current operational pin in this repository now agrees:

> The unique production Alembic head is **`202607260001`**.
