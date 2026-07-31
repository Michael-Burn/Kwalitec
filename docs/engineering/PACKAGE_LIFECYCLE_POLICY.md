# Package Lifecycle Policy

**Programme:** V1S-003  
**Status:** Active  
**Effective:** 2026-07-31  
**Registry:** `app/services/package_lifecycle.py`

---

## Lifecycles

| Status | Meaning | Allowed changes |
|---|---|---|
| **ACTIVE** | Owns a live product or founder responsibility | Normal feature work in scope |
| **MAINTENANCE** | Needed, but not the growth surface | Bugfixes, docs, narrow compatibility |
| **DEPRECATED** | Superseded; still importable for coexistence | No new callers; extract then archive |
| **ARCHIVED** | Unwired from production; retained for tests / history | No new production imports |
| **REMOVE** | Scheduled for deletion | Delete only when gates pass |

Every package has **exactly one** lifecycle at a time.

---

## Transition rules

```
ACTIVE ──► MAINTENANCE ──► DEPRECATED ──► ARCHIVED ──► REMOVE
                ▲                              │
                └──────── (reactivate only with programme authority)
```

1. **Deprecate** before archive when callers still exist.
2. **Archive** when production / presentation / services imports are zero (tests may remain).
3. **Remove** only when:
   - independence / regression tests migrated or intentionally deleted
   - no dynamic imports remain
   - owner records the gate in the readiness debt register
4. Do **not** hard-delete packages mid-dogfood without a programme that names the gate.

---

## Ownership

- Owner is a capability team / programme name, not a person email.
- Changing ownership requires updating `package_lifecycle.py` (and runtime ownership when educational).
- Unowned packages are a defect — add them to the registry in the same change that introduces them.

---

## Recommendations vocabulary

| Recommendation | Meaning |
|---|---|
| `retain` | Keep as-is |
| `split` | Divide oversized package / module |
| `merge` | Fold into a canonical sibling |
| `extract` | Move a subpackage to a new home (e.g. planning/) |
| `archive` | Mark ARCHIVED; stop production use |
| `remove` | Delete after gates |

---

## Relation to runtime ownership

- `app/services/runtime_ownership.py` — **educational runtime / curriculum / mission** authority
- `app/services/package_lifecycle.py` — **repository package** health

Both surface on `/founder/v1-readiness`.

---

## New package checklist

1. Add package under the correct layer (`application` / `domain` / …).
2. Add `PackageEntry` to the lifecycle registry (`ACTIVE`, owner, responsibility).
3. Export a clear entry point; avoid deep wildcard re-exports unless established pattern.
4. Add behaviour tests under `tests/test_<programme>_*.py` or a focused package suite.
5. Do not introduce a parallel package for the same responsibility.
