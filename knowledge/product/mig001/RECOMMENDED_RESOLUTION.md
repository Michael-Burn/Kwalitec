# MIG-001 — Recommended Resolution

**Investigation date:** 2026-07-27  
**Status:** Recommendation only — **no code or migration changes performed**

---

## Unambiguous recommendation

1. **`202607240001` (analytics) must remain** in the production migration chain.  
2. **Do not delete** the analytics migration.  
3. **Do not rebase/rewrite** the analytics migration.  
4. **Treat `202607260001` as the misparented head** (parent `202611120001` instead of the current tip).  
5. **Resolve dual heads by either:**
   - **Preferred (if `202607260001` never applied anywhere):** reparent `202607260001.down_revision` from `202611120001` → `202607240001` (linearize).  
   - **Safe default (if any environment may already have applied `202607260001`, or policy forbids editing committed revisions):** add an empty **merge** revision with `down_revision = ("202607240001", "202607260001")`.  
6. After either path, update CI / ops single-head pins from `202607230002` to the new unique head.

---

## Answers to the brief’s resolution verbs

| Verb | Analytics migration `202607240001` | Commitments migration `202607260001` |
|---|---|---|
| Remain | **Yes** | **Yes** (content); parent may change |
| Merged | Only as one parent of a merge node if Option B chosen | Same |
| Rebased | **No** | **Reparent preferred** (Option C2) if unapplied |
| Removed | **No** | **No** |

---

## Decision gate (release engineering)

Before choosing Preferred vs Safe default, run on **every** deployed / shared database:

```sql
SELECT version_num FROM alembic_version;
-- and / or
SELECT name FROM sqlite_master WHERE name = 'recommendation_commitments';
-- postgres: information_schema.tables
```

| Finding | Choose |
|---|---|
| No DB has stamp `202607260001` and no DB has `recommendation_commitments` from that revision | **C2 reparent** |
| Any DB has stamp `202607260001` or uncertain (including production not yet audited) | **B merge** |
| Any proposal to delete `202607240001` | **Reject** |

**This investigation audited local `instance/*.sqlite3` only.** Primary app DB is at `202607240001` without `recommendation_commitments`. Remote/production stamps were **not** available — gate above is mandatory before implementing the fix in a follow-up milestone.

---

## Why not merge-only always?

Merge is always *valid*. Reparent is *cleaner* when the mistake is young and unapplied (commitments revision was added in `65cb380` RC1 and RC-001 docs previously described it as untracked WIP). Prefer not to permanently encode a wrong branchpoint parent when a one-line parent fix restores a linear graph matching product chronology (analytics 2026-07-24, commitments 2026-07-26).

---

## Why analytics empty tables are acceptable

Under `ANALYTICS_EVENTS_V1=OFF`, tables may be empty. That is **by design** (ADR-025 kill switch), not “unused production schema” justifying deletion. Activation checklists and privacy workflows require the schema to exist before flag-on.

---

## Follow-up work (out of MIG-001 scope)

Implementation milestone should:

1. Execute the decision gate.  
2. Apply C2 or B (not both).  
3. Update `.github/workflows/ci.yml` and `tests/operational/helpers.py` head pin.  
4. Update `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` expected head.  
5. Re-run `flask db heads` → exactly one head; `StartupService` upgrade on fresh DB.  
6. Confirm curriculum V1/V2 unaffected (neither migration touches curriculum traversal).

---

## Explicit non-actions for this investigation

- No migration files created, deleted, or edited.  
- No history rewrite performed.  
- No feature flag changes.  
- No production deploy.
