# Mathematical Notation Inventory Summary

**Generated:** 2026-09-08T07:05:34Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `66ad0532050967bb82c1b07573d832825118b5247afd4f4086aea32ca111e4c9`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 2011 |
| Needs migration | 0 |
| Migrated (dollar-delimited) | 1992 |
| Correctly excluded | 192 |
| Needs manual review (flag) | 115 |
| Confident automated (no flag) | 2088 |
| Packages with migration backlog | 0 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (0 packages, 0 needs_migration strings).


## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

