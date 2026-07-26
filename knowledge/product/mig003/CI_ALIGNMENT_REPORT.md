# MIG-003 — CI Alignment Report

**Programme:** MIG-003 — Migration Contract Alignment  
**Date:** 2026-07-27  
**Scope:** Continuous integration expectations only (no migration graph edits)

---

## Change

### File: `.github/workflows/ci.yml`

**Job step:** `Migration scripts load`

| Field | Value |
|---|---|
| Previous expectation | `assert head == "202607230002"` |
| New expectation | `assert head == "202607260001"` |
| Reason | After MIG-002, `ScriptDirectory.get_current_head()` returns the unique tip `202607260001`. The CI pin was already stale after analytics (`202607240001`) and remained wrong after commitments. |

**Snippet (post-update):**

```python
head = scripts.get_current_head()
assert head, "No Alembic head"
print("Alembic head:", head)
assert head == "202607260001", head
```

---

## Validation performed

| Check | Result |
|---|---|
| `flask db heads` | `202607260001 (head)` |
| `ScriptDirectory.get_current_head()` | `202607260001` |
| `ScriptDirectory.get_heads()` | `['202607260001']` |
| Logical equivalence to CI assert | Pass — CI would accept the live unique head |

No other workflow files asserted `202607230002`.

---

## Out of scope

- Creating/deleting/rewriting Alembic revisions
- Changing other CI jobs (pytest matrix, ruff, pip-audit soft gate)
- Updating snapshot or Educational OS tests
