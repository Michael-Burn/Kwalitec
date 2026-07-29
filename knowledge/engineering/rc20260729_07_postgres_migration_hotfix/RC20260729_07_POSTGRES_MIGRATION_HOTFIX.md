# RC-2026.07.29-07 — PostgreSQL Migration Compatibility Hotfix

**Programme:** Production Deployment  
**Phase:** Deployment blocker remediation (DP-004 pre-deploy failure)  
**Date:** 2026-07-29  
**Status:** Hotfix committed — suitable for DP-004 retry after operator stamp/schema check  
**Predecessor failure:** Render pre-deploy `flask db upgrade` on freeze tip `43cdd46`  
**Parent freeze tip:** `43cdd46f21d459373eb0489c843fd204f094ebdd`  
**Authority:** DP-004 failure evidence; Alembic chain under `migrations/versions/`

---

## Executive Summary

DP-004 failed in Render’s pre-deploy script while applying revision **`202607270004`**. PostgreSQL rejected:

`ALTER TABLE studio_foundation_documents ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL`

because `server_default=sa.text("1")` emits an **integer** default. SQLite accepted the same construct; PostgreSQL does not.

This hotfix replaces Boolean `0`/`1` server defaults with `sa.true()` / `sa.false()` in the failing revision and in earlier create-table revisions that used the same SQLite-oriented literals. Application behaviour is unchanged. Migration IDs and ordering are unchanged.

Post-failure production health still reports Alembic **`current=202607270003`** on live commit `ee38ac2` (failed deploy never started). That is evidence the failed revision was **not stamped**. Direct SQL inspection of production was not available from this agent environment; operator confirmation SQL is documented below.

**Verdict: READY FOR DP-004 RETRY** (after the operator confirmation query, and after deploying this hotfix commit — not the original freeze tip alone).

---

## Root Cause Analysis

| Item | Detail |
|------|--------|
| Failure point | Render pre-deploy / `releaseCommand`: `flask db upgrade` |
| Failing revision | `202607270004` (`curriculum_document_file_metadata`) |
| Failing DDL | `ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL` |
| Driver error | `psycopg2.errors.DatatypeMismatch` / SQLAlchemy `ProgrammingError` |
| Root cause | `server_default=sa.text("1")` on `sa.Boolean()` → unquoted `DEFAULT 1` |
| Why local/RC missed it | SQLite accepts integer Boolean defaults; greenfield Postgres path was not exercised for this revision on production until DP-004 |
| App impact | None — process exited before Waitress start; live host remained on `ee38ac2` |

SQLAlchemy dialect proof (pre-fix):

| Expression | PostgreSQL render | Postgres Boolean OK? |
|------------|-------------------|----------------------|
| `sa.text("1")` | `DEFAULT 1` | **No** |
| `server_default="1"` | `DEFAULT '1'` | Yes (string cast; already on prod for older tables) |
| `sa.true()` / `sa.false()` | `DEFAULT true` / `false` | **Yes** (preferred) |

---

## PostgreSQL State Review (Step 1)

### Evidence available (no direct DB credentials / Render CLI auth)

| Signal | Observed after failed deploy (2026-07-29) |
|--------|---------------------------------------------|
| Live `/health/live` commit | `ee38ac2…` (prior production; not freeze) |
| Live `/health/ready` migrations | `current=202607270003`, `head=202607270013` (head as seen by **old** deploy artefact) |
| Pre-deploy exit | Status 1; upgrade aborted on `is_active` |
| New process start | Did not occur |

### Interpretation

| Question | Answer |
|----------|--------|
| Was `202607270004` stamped? | **No** — `alembic_version` still reports `202607270003` via health |
| Fully applied? | **No** |
| Partial apply? | **Not evidenced.** PostgreSQL `ADD COLUMN` runs inside Alembic’s migration transaction; failure should roll back prior statements in that revision. **Not directly verified via `information_schema`.** |
| Cleanup required? | **Expected: none.** Confirm with operator SQL before retry. |

### Operator confirmation (required before DP-004 retry)

Run against production Postgres (Render Shell / `psql`):

```sql
SELECT version_num FROM alembic_version;

SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'studio_foundation_documents'
ORDER BY ordinal_position;
```

**Pass criteria for “no cleanup”:**

- `version_num = 202607270003`
- `studio_foundation_documents` does **not** yet have Phase-1 columns from `202607270004`  
  (`workspace_id`, `original_filename`, `content_type`, `byte_size`, `checksum_sha256`, `storage_key`, `version_number`, `is_active`, `processing_stage`)

**If Phase-1 columns exist while stamp remains `202607270003`:** document as partial apply; drop those columns (or restore DB backup) before retry. Do not stamp forward manually.

---

## PostgreSQL Compatibility Audit

### Scope

All scripts under `migrations/versions/` reviewed for:

- Boolean defaults (`sa.text("0"|"1")`, string `"0"`/`"1"`)
- SQLite-only SQL / backend-specific `op.execute`
- Risky ALTER patterns (batch_alter retained; portable)
- Timestamp / JSON defaults (no Boolean-class failures found)

### Confirmed incompatibility

| Revision | Issue | Severity |
|----------|-------|----------|
| `202607270004` | `Boolean` + `server_default=sa.text("1")` → `DEFAULT 1` | **Blocker** (hit in DP-004) |

### Hardened prophylactically (same class of SQLite Boolean literals)

These already succeeded on production historically via `DEFAULT '1'` string form, but were converted to `sa.true()` / `sa.false()` for portable, explicit Boolean defaults (no behaviour change):

| Revision | Columns |
|----------|---------|
| `202607080002` | `subjects.active`, `mission_tasks.completed` |
| `202607080003` | `study_plans.active` |
| `202607080004` | `curricula.active`, `topics.active`, `topic_progress.completed`, `learning_objectives.active`, `mistakes.resolved` |

### Reviewed and left unchanged (compatible)

| Pattern | Rationale |
|---------|-----------|
| Integer / float `server_default="0"` / `"1"` / `"1.0"` / `"60"` | Valid on both backends |
| String defaults (`"Pending"`, `"uploaded"`, `"Mixed"`, …) | Valid |
| `server_default=sa.false()` / `sa.true()` already present (e.g. welcome flags, archived) | Preferred form |
| `batch_alter_table` usage | Portable; Postgres emits normal `ALTER` |
| `existing_server_default=sa.text("'#007bff'")` | Colour string, not Boolean |

### Residual audit note

No remaining `sa.text("0"|"1")` Boolean defaults in the chain after this hotfix. Offline PostgreSQL compile of `202607270004` now emits `BOOLEAN DEFAULT true`.

---

## Affected Migration(s)

| Revision | File | Change |
|----------|------|--------|
| `202607270004` | `migrations/versions/202607270004_curriculum_document_file_metadata.py` | `sa.text("1")` → `sa.true()` on `is_active` |
| `202607080002` | `migrations/versions/202607080002_create_mission_models.py` | Boolean `"1"`/`"0"` → `sa.true()`/`sa.false()` |
| `202607080003` | `migrations/versions/202607080003_create_study_plan_models.py` | Boolean `"0"` → `sa.false()` |
| `202607080004` | `migrations/versions/202607080004_create_curriculum_learning_models.py` | Boolean `"1"`/`"0"` → `sa.true()`/`sa.false()` |

No revision IDs changed. No squash. No history rewrite.

---

## Files Modified

- `migrations/versions/202607270004_curriculum_document_file_metadata.py`
- `migrations/versions/202607080002_create_mission_models.py`
- `migrations/versions/202607080003_create_study_plan_models.py`
- `migrations/versions/202607080004_create_curriculum_learning_models.py`
- `knowledge/engineering/rc20260729_07_postgres_migration_hotfix/RC20260729_07_POSTGRES_MIGRATION_HOTFIX.md` (this report)

Application code: **unchanged**.

---

## Migration Validation

| Check | Result |
|-------|--------|
| Fresh SQLite `flask db upgrade` → head | **Pass** — `202607280080 (head)` |
| Offline PG SQL for `202607270004` | **Pass** — `is_active BOOLEAN DEFAULT true NOT NULL`; no `BOOLEAN DEFAULT 1` |
| Offline PG SQL for `202607080002`–`004` | **Pass** — Boolean defaults render as `true`/`false` |
| Single Alembic head | **Pass** — `202607280080` |
| Live Postgres upgrade from empty | **Not run here** (no local `initdb` / Render DB access) |
| Production schema SQL confirm | **Operator step** (documented above) |

---

## Regression Results

| Suite | Result |
|-------|--------|
| `tests/test_startup_service.py` | **Pass** |
| `tests/ga/test_recovery.py` | **Pass** |
| `tests/operational/test_alpha_configuration.py` | **1 pre-existing failure** — `test_alembic_head_and_migration_files` expects stale head `202607270013` vs actual `202607280080` (unrelated to Boolean defaults; not modified in this hotfix) |
| App startup smoke on upgraded SQLite | **Pass** — `/health/live` ok; `/health/ready` migrations `current=head=202607280080` |

---

## Remaining Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Undetected partial columns on prod from failed `202607270004` | Low (transactional DDL + stamp evidence) | Operator confirmation SQL before retry |
| Further PG-only DDL quirks beyond Boolean defaults | Low–medium | DP-004 retry is the live proof; watch pre-deploy logs |
| Deploying original freeze `43cdd46` without this hotfix | **High** | Retry must use **this hotfix commit** (or later) |
| Stale operational test expecting old Alembic head | Low | Follow-up; not a deploy blocker |
| No persistent document disk (DP-003 R-C2) | Medium | Unchanged; separate from migration hotfix |

---

## Recommendation

1. Operator: run confirmation SQL; cleanup only if partial columns exist.  
2. Commit and push this hotfix.  
3. **Manual Deploy** of the hotfix tip on Render (auto-deploy remains optional/off).  
4. Confirm pre-deploy `flask db upgrade` reaches head `202607280080`.  
5. Resume DP-004 verification (health, Founder, Student, storage, logs).

Do **not** redeploy freeze tip `43cdd46` alone — it still contains the incompatible `sa.text("1")` default.

---

## Decision

# READY FOR DP-004 RETRY

| Success criterion | Met? |
|-------------------|------|
| Failed migration investigated | **Yes** |
| Postgres partial-state posture documented | **Yes** (stamp evidence + operator SQL) |
| Full chain audited for Boolean PG incompat | **Yes** |
| Confirmed incompatibilities fixed | **Yes** |
| Behaviour / ordering / history preserved | **Yes** |
| SQLite upgrade + PG SQL compile validated | **Yes** |
| Relevant regressions | **Pass** (one unrelated stale-head assert) |

**Commit message (mandated):** `fix(migrations): restore PostgreSQL compatibility`
