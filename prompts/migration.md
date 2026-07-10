# Prompt: Database Migration

Use this prompt for Alembic / schema work on Kwalitec.

---

## Agent instructions

You are changing the **Kwalitec** database schema.

Mandatory:

1. Read `ARCHITECTURE.md` (database layer) and `.cursor/rules/10-security.mdc`.
2. Prefer additive, nullable, or dual-write compatible changes when migrating live concepts (especially curriculum V1→V2).
3. Create Alembic revisions under `migrations/versions/` — do not rely on `db.create_all()` for production schema.
4. Keep `StartupService` non-destructive (no drops of user data).
5. Update SQLAlchemy models to match the migration.
6. Add/adjust tests for the new schema behaviour.
7. Document upgrade/downgrade notes and data backfill needs.

## Migration request

**Purpose:** \<why\>

**Tables/columns affected:**
- \<list\>

**Data migration required?** Yes / No — \<details\>

**Compatibility requirements:**
- V1 curricula: \<preserve / N/A\>
- V2 sections/topics: \<details\>
- Existing study plans / progress rows: \<details\>

**Out of scope:**
- \<e.g. UI redesign, unrelated services\>

## Verification checklist

- [ ] `flask db upgrade` succeeds on a clean DB
- [ ] `flask db upgrade` succeeds on a DB with existing data (if applicable)
- [ ] Downgrade tested or explicitly marked irreversible with rationale
- [ ] pytest modules covering models/services updated
- [ ] Completion report includes **Migration Impact**

## Completion

Use `.cursor/rules/07-reporting.mdc`. Emphasize Migration Impact and Architecture Compliance. Commit only if asked.
