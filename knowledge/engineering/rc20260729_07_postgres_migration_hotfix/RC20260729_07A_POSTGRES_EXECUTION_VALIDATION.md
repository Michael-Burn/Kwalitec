# RC-2026.07.29-07A — PostgreSQL Migration Execution Validation

**Programme:** Production Deployment  
**Phase:** Final deployment gate (real PostgreSQL execution proof)  
**Date:** 2026-07-29  
**Status:** Validation only — **no production deploy, no production modification, no application code change**  
**Release candidate tip:** `18ffad54b04f500619b82aa7d5e17fb118f63d54`  
(`fix(migrations): restore PostgreSQL compatibility` — RC-2026.07.29-07)  
**Predecessor:** RC-2026.07.29-07 Boolean default hotfix after DP-004 pre-deploy failure  

---

## Executive Summary

The complete Alembic chain was executed against a **disposable, empty PostgreSQL 18.4** instance (local zonky-embedded binaries; never production).

`flask --app wsgi.py db upgrade` applied **51** upgrade steps with **zero** SQL / datatype / transaction failures, including the previously blocking revision **`202607270004`**. Alembic reached head **`202607280080`**.

A production-config application boot on the migrated database completed `StartupService` (schema up to date → Founder/Admin bootstrap → bundled curriculum import). Health endpoints returned healthy. A second empty database proved the **StartupService-only** migrate + admin + curriculum path independently.

**Verdict: POSTGRESQL CERTIFIED — safe to retry DP-004** using tip `18ffad5` (not freeze `43cdd46` alone).

---

## PostgreSQL Environment

| Field | Value |
|-------|--------|
| Purpose | Disposable validation only |
| Distribution | Zonky `embedded-postgres-binaries-darwin-arm64v8` **18.4.0** |
| Host | `127.0.0.1` |
| Port | `55432` |
| Superuser / owner | `kwalitec` (trust auth, local only) |
| Validation DB (explicit upgrade) | `kwalitec_rc07a` |
| Validation DB (StartupService boot) | `kwalitec_rc07a_boot` |
| Production | **Not used** |
| Working artefact path | `.tmp/rc07a_pg/` (local disposable; not committed) |

### Step 1 — Empty database confirmation (`kwalitec_rc07a`)

| Check | Result |
|-------|--------|
| `public` base tables | **0** |
| `alembic_version` exists | **False** |
| Schema history | **None** |

---

## Migration Log Summary

Command:

```bash
DATABASE_URL=postgresql+psycopg://kwalitec@127.0.0.1:55432/kwalitec_rc07a \
  flask --app wsgi.py db upgrade
```

| Metric | Result |
|--------|--------|
| Exit code | **0** |
| Alembic impl | `PostgresqlImpl` (transactional DDL) |
| Upgrade steps logged | **51** (`Running upgrade …`) |
| Errors / Tracebacks / DatatypeMismatch | **None** |
| Prior blocker `202607270003 → 202607270004` | **Succeeded** |
| Final revision | **`202607280080` (head)** |

Notable successful step (DP-004 failure point):

```text
Running upgrade 202607270003 -> 202607270004, Add curriculum document file metadata columns (Phase 1 upload).
```

Full log: `.tmp/rc07a_pg/upgrade.log`

---

## Alembic Validation

| Check | Result |
|-------|--------|
| `flask db current` | `202607280080 (head)` |
| `flask db heads` | `202607280080 (head)` |
| `alembic_version.version_num` | `202607280080` |
| current == head | **Yes** |

---

## Schema Validation

Observed on `kwalitec_rc07a` after upgrade:

| Check | Result |
|-------|--------|
| Public base tables | **133** |
| Foreign keys | **129** |
| Indexes | **622** |
| Core tables present | `users`, `subjects`, `missions`, `study_plans`, `curricula`, `sections`, `topics`, `learning_objectives`, `studio_foundation_documents`, `published_curriculum_packages`, … |
| LP-001 table | `llp_lifecycle_operations` (not a literal `learner_lifecycle_checkpoints` name) |

### `studio_foundation_documents` Phase-1 columns (`202607270004`)

| Column | data_type | column_default | nullable |
|--------|-----------|----------------|----------|
| `is_active` | boolean | `true` | NO |
| `version_number` | integer | `1` | NO |
| `workspace_id` | varchar | null | YES |
| `processing_stage` | varchar | `'uploaded'` | YES |

Indexes include `ix_studio_foundation_documents_is_active` and `ix_studio_foundation_documents_workspace_kind_active`.

Boolean defaults sample after hotfix: `true` / `false` literals (not integer `1`/`0`).

---

## Startup Validation

### A — Migrated DB + `ProductionConfig` (`kwalitec_rc07a`)

Environment (disposable values only): `APP_ENV=production`, strong `SECRET_KEY`, `ADMIN_EMAIL` / `ADMIN_PASSWORD`, V1 sole-runtime flag matrix.

| Step | Result |
|------|--------|
| `create_app()` | Success |
| StartupService | Complete |
| Migrations | Already at head (no-op) |
| Founder/Admin bootstrap | **Created** `rc07a-founder@example.com` with Founder + Administrator + Student |
| Curriculum import | **3** imported (CB2, CM1, CS1); 0 errors |
| Idempotent second boot | Admin exists; curricula skipped (3) |
| Password verify | `check_password` **True** |
| Roles | founder, administrator, student |
| Login POST (with CSRF + Referer) | **302 → `/console/`** |

### B — Empty DB + StartupService-only path (`kwalitec_rc07a_boot`)

No prior `flask db upgrade`. Production `create_app()` alone:

| Step | Result |
|------|--------|
| Alembic upgrades inside StartupService | Full chain through `202607280080` (includes `202607270004`) |
| Admin created | **Yes** |
| Curricula imported | **3** |
| `/health/ready` | `ready=true`, migrations ok |

---

## Health Validation

Against migrated production-config app (`kwalitec_rc07a`):

| Endpoint | HTTP | Outcome |
|----------|------|---------|
| `/health/live` | 200 | `status=ok` |
| `/health/ready` | 200 | `ready=true`, `environment=production`, `database=connected`, migrations `current=head=202607280080` |
| `/health` | 200 | `status=ok`, `database=connected` |

---

## Regression Results

| Suite | Result |
|-------|--------|
| `tests/test_startup_service.py` | **Pass** |
| `tests/ga/test_recovery.py` | **Pass** |
| Combined | **25 passed** |

No new PostgreSQL incompatibility discovered → **no further code changes** in this programme.

---

## Remaining Risks

| Risk | Severity | Note |
|------|----------|------|
| Production still on old tip `ee38ac2` / stamp `202607270003` until DP-004 retry | Operational | Expected; do not deploy freeze `43cdd46` alone |
| Production may need operator column check from failed DP-004 attempt | Low | RC-07 SQL confirmation still recommended once |
| Disposable PG 18.4 vs Render Postgres major version may differ | Low | Boolean/`DEFAULT true` fix is version-agnostic for supported PG |
| Document storage durability (DP-003 R-C2) | Medium | Unrelated to migration certification |
| Local `.tmp/rc07a_pg` artefacts | N/A | Disposable; stop cluster after validation (stopped) |

---

## Recommendation

1. Treat tip **`18ffad5`** as the deployable release candidate for DP-004 retry.  
2. Push to the Render deploy branch (`main`) and **manual deploy** that commit.  
3. Before retry, optionally re-confirm production has no partial `202607270004` columns (RC-07 SQL).  
4. Do **not** redeploy `43cdd46` without the migration hotfix.

---

## Decision

# POSTGRESQL CERTIFIED

| Success criterion | Met? |
|-------------------|------|
| Empty PostgreSQL created | **Yes** |
| Entire migration chain executed | **Yes** (51 steps) |
| Alembic reached head `202607280080` | **Yes** |
| Application started | **Yes** |
| Founder bootstrap succeeded | **Yes** |
| Health endpoints passed | **Yes** |
| No PostgreSQL migration failures | **Yes** |
| Safe to retry DP-004 | **Yes** |

**Not performed:** production connection, production deploy, application behaviour changes.
