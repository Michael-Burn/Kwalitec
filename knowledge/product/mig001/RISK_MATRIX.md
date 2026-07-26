# MIG-001 — Risk Matrix

**Investigation date:** 2026-07-27  
**Problem:** Dual Alembic heads `202607240001` and `202607260001` block unambiguous `upgrade head`.

---

## Options evaluated

| Option | Action |
|---|---|
| **A** | Delete orphan migration — interpreted as deleting `202607240001` (per brief hypothesis) |
| **B** | Create merge migration joining both heads |
| **C** | Rebase / reparent analytics — evaluated both as (C1) rewrite analytics parent and (C2) reparent commitments onto analytics tip |

Because the brief’s “orphan” hypothesis is **falsified**, Option A as stated targets the wrong revision. Option C as stated (“rebase analytics”) is also the wrong subject; the misparented revision is `202607260001`.

---

## Option A — Delete `202607240001`

| Dimension | Assessment | Evidence |
|---|---|---|
| Correctness | **Incorrect** | Analytics is shipped PRD-001 / ADR-025 contract; not dead |
| Risk | **Critical** | Breaks DBs stamped `202607240001`; removes schema creation for live models/SQL stores |
| Future maintenance | Forces either silent `create_all` divergence or deletion of entire analytics package + tests + ops docs |
| History integrity | Destructive if already applied; Alembic stamp would point at missing revision |
| Existing databases | `instance/kwalitec.sqlite3` already at `202607240001` with tables present |
| Production deployment | Flag-ON activation and privacy/export/purge CLI become impossible without replacement migration |
| Long-term architecture | Violates Accepted ADR-025 |

**Deleting `202607260001` instead** (not Option A as written) would also be **incorrect**: EP-008.3A student commitment feature and model/routes depend on `recommendation_commitments`.

**Verdict:** Reject deletion of either head’s migration as a dual-head “fix.”

---

## Option B — Create merge migration

Example shape (illustrative only — **not created in MIG-001**):

```text
202607240001 ─┐
               ├─→ NEW_MERGE_REV (empty upgrade)
202607260001 ─┘
```

| Dimension | Assessment | Evidence |
|---|---|---|
| Correctness | **Technically valid** | Same pattern as historical `202607190002` merge |
| Risk | **Low–medium** | Safe for DBs that already applied one head; other head upgrades on merge | Needs stamp inventory |
| Future maintenance | Leaves a permanent “Y” in history documenting the accidental branch | Acceptable; mirrors prior V2 merge |
| History integrity | Preserves both revision ids and contents unchanged | Best when either head may already be applied somewhere |
| Existing databases | DB at `202607240001`: upgrade applies `202607260001` then merge (or merge path per Alembic). DB that somehow applied only commitments from branchpoint: more complex — verify before merge | Local primary lacks commitments table |
| Production deployment | Restores single head so `StartupService` / CI `get_current_head()` can work after CI pin update | Dual-head currently breaks upgrade |
| Long-term architecture | Does **not** correct the mistaken parent of `202607260001`; encodes the mistake as a merge | Prefer when rewrite is unsafe |

**Verdict:** Correct **safety-first** choice if any environment may already have `202607260001` in `alembic_version`, or if policy forbids editing committed migration metadata.

---

## Option C — Rebase / reparent

### C1 — Rebase analytics migration (brief Option C literally)

Change or rewrite `202607240001` parentage / history.

| Dimension | Assessment |
|---|---|
| Correctness | **Unnecessary / harmful** — analytics already correctly parents `202607230002` |
| Risk | High for any DB already stamped `202607240001` |
| Verdict | **Reject** |

### C2 — Reparent commitments migration onto analytics tip (correct subject)

Change only:

```text
# 202607260001
down_revision: "202611120001"  →  "202607240001"
```

(Optionally accompanied by CI/ops head pin update to the new single head.)

| Dimension | Assessment | Evidence |
|---|---|---|
| Correctness | **Architecturally best** if unapplied | Linear main line; matches additive independent tables; parent becomes true tip |
| Risk | **Low if never applied; High if already applied from wrong parent** | Changing `down_revision` after apply rewrites graph under a live stamp |
| Future maintenance | Clean linear history; no extra merge node | Preferred for young mistakes |
| History integrity | Edits a committed revision file (`65cb380` added it) | Allowed only with explicit release approval + environment audit |
| Existing databases | Local primary at analytics head **without** commitments → reparent + upgrade creates table cleanly | No evidence found of `202607260001` stamp in inspected local DBs |
| Production deployment | Must confirm no Render/production/`alembic_version` contains `202607260001` | Remote not inspected here |
| Long-term architecture | Fixes root cause (wrong parent) rather than merging around it | Aligns with “small scope / deterministic cores” |

**Verdict:** Preferred **if** environment audit shows `202607260001` never applied.

---

## Comparative matrix

| Criterion | A Delete analytics | B Merge | C1 Rebase analytics | C2 Reparent commitments |
|---|---|---|---|---|
| Fixes dual head | No (destroys feature) | Yes | No / harmful | Yes |
| Matches product intent | No | Yes | N/A | Yes |
| Risk to stamped DBs | Critical | Low–med | Critical | Conditional |
| Root-cause fix | No | Partial | No | Yes |
| Recommended | **No** | **Yes (safe default)** | **No** | **Yes (if unapplied)** |

---

## Ancillary risks (any fix)

1. **Stale CI pin** still asserts `202607230002` — must update to the post-resolution single head or CI “Migration scripts load” remains wrong.
2. **StartupService `upgrade head`** cannot proceed while multiple heads exist (observed `CommandError` on Alembic state detection during Flask CLI).
3. RC-001 / PX-002A reports already document dual-head breakage of fresh SQLite StartupService paths — resolving heads unblocks that class of failures.
