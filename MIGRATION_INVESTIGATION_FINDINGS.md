# Migration Investigation Findings

## Date: 2026-07-10

## Investigation Summary

The investigation successfully identified why the database schema appears to "disappear" after migrations run.

## Root Cause

**Disk I/O Error During Migration Execution**

The migrations are failing with a `sqlite3.OperationalError: disk I/O error` when attempting to create the `alembic_version` table. This is the **first table** that Alembic creates, and when this fails, **none of the application tables are created**.

## Evidence

### 1. Instrumentation Logs Show Migration Failure

The instrumented `env.py` revealed:

```
INFO  [alembic.instrumentation] === INITIAL STATE BEFORE MIGRATIONS ===
INFO  [alembic.instrumentation]   Tables via inspector: ['alembic_version']
INFO  [alembic.instrumentation]   sqlite_master tables: ['alembic_version']
...
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) disk I/O error
[SQL: CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)]
```

### 2. Database State Analysis

**Before migrations:**
- Database file exists: `/Users/kwalitec/Desktop/kwalitec/instance/kwalitec.sqlite3`
- Size: 86,016 bytes
- Tables: `['alembic_version']` only

**After attempted migrations:**
- Database file exists
- Size: 86,016 bytes (unchanged!)
- Tables: `['alembic_version']` only (no application tables created)

### 3. Migration Steps Identified

The instrumentation successfully identified **8 migration steps** that should execute:

1. `202609070004` - Add archived column to study_plans
2. `202609070003` - Add curriculum topic code to study_plans
3. `202609070002` - Add curriculum version to study_plans
4. `202609070001` - Add preferred session minutes
5. `0a272936a47b` - Add decision model
6. `202607080005` - Add adaptive learning fields
7. `202607080004` - Create curriculum learning models
8. `202607080003` - Create study plan models
9. `202607080002` - Create mission models
10. `202607080001` - Create user model

**None of these migrations actually executed** due to the disk I/O error.

## Why the Original Hypothesis Was Wrong

The original hypothesis suggested:
- `fileConfig()` was hanging
- `run_migrations_online()` wasn't executing
- `--sql` flag worked but normal mode didn't

**Evidence against this:**
1. ✅ `fileConfig()` completes successfully (logging is configured)
2. ✅ `run_migrations_online()` **does** execute (instrumentation logs show it running)
3. ✅ `--sql` generates SQL (because it doesn't actually execute DDL)
4. ❌ Normal mode fails with disk I/O error when executing DDL

## The Real Issue

The disk I/O error occurs when SQLAlchemy tries to execute:

```sql
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)
```

This is a **low-level SQLite error** indicating:
- File system permissions issue
- Disk space issue
- File lock issue
- Database corruption
- I/O subsystem error

## Instrumentation Added

The following instrumentation was added to `kwalitec/migrations/env.py`:

1. **Entry/Exit logging** for every migration's `upgrade()` method
2. **Database state inspection** before and after each migration:
   - `connection.in_transaction()` - transaction state
   - `inspect(connection).get_table_names()` - tables via SQLAlchemy
   - `PRAGMA database_list` - database file information
   - `SELECT name FROM sqlite_master` - raw SQLite tables
3. **Migration step enumeration** - lists all migrations that will run
4. **Module inspection** - verifies migration modules are loaded correctly

## Files Modified

1. `kwalitec/migrations/env.py` - Added comprehensive instrumentation
2. `kwalitec/migrations/alembic.ini` - Added logging configuration for instrumentation
3. `kwalitec/test_migration_instrumentation.py` - Test script for existing database
4. `kwalitec/test_fresh_migration.py` - Test script for fresh database

## Next Steps

To resolve the disk I/O error, investigate:

1. **File system permissions:**
   ```bash
   ls -la /Users/kwalitec/Desktop/kwalitec/instance/
   ```

2. **Disk space:**
   ```bash
   df -h /Users/kwalitec/Desktop
   ```

3. **Database file locks:**
   ```bash
   lsof | grep kwalitec.sqlite3
   ```

4. **Database corruption:**
   ```bash
   sqlite3 /Users/kwalitec/Desktop/kwalitec/instance/kwalitec.sqlite3 "PRAGMA integrity_check;"
   ```

5. **Try deleting and recreating the database:**
   ```bash
   rm /Users/kwalitec/Desktop/kwalitec/instance/kwalitec.sqlite3
   cd kwalitec && flask db upgrade
   ```

## Conclusion

The schema is not "disappearing" - it was **never created** in the first place due to a disk I/O error during the very first DDL operation (creating the `alembic_version` table). The instrumentation successfully pinpointed the exact failure point.