# Mathematical Notation Inventory Summary

**Generated:** 2026-09-08T04:04:50Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `0b08648e0917c25d2d5834964dde8d6bb2b7cb47855982492b6a530cf08e9c1e`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 1890 |
| Needs migration | 29 |
| Migrated (dollar-delimited) | 1871 |
| Correctly excluded | 284 |
| Needs manual review (flag) | 255 |
| Confident automated (no flag) | 1948 |
| Packages with migration backlog | 12 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (12 packages, 29 needs_migration strings).

- `5.1.4-loss-estimators-cs1003.json` (`CS1-EP001-PKG-5.1-LOSS-ESTIMATORS`): 6 migrate, 0 tier-1, 0 manual-review flags
- `5.1.5-credible-intervals-cs1003.json` (`CS1-EP001-PKG-5.1-CREDIBLE-INTERVALS`): 5 migrate, 0 tier-1, 6 manual-review flags
- `revision-bayesian-cs1015.json` (`CS1-EP001-PKG-REV-BAYESIAN-OMICRON`): 5 migrate, 0 tier-1, 6 manual-review flags
- `revision-hypothesis-testing-cs1012.json` (`CS1-EP001-PKG-REV-HYPOTHESIS-TESTING`): 4 migrate, 0 tier-1, 0 manual-review flags
- `revision-midspine-cs1003.json` (`CS1-EP001-PKG-REV-MIDSPINE`): 2 migrate, 0 tier-1, 4 manual-review flags
- `1.2.3-pca-cs1002.json` (`CS1-CS1002-PKG-1.2-PCA`): 1 migrate, 0 tier-1, 0 manual-review flags
- `4.1.1-response-explanatory-cs1003.json` (`CS1-EP001-PKG-4.1-RESPONSE-EXPLANATORY`): 1 migrate, 0 tier-1, 0 manual-review flags
- `4.1.1-response-explanatory-cs1013.json` (`CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY`): 1 migrate, 0 tier-1, 0 manual-review flags
- `cp-4.1.1-linear-regression-cs1016.json` (`CS1-EP001-PKG-CP-4.1-LINEAR-REGRESSION`): 1 migrate, 0 tier-1, 0 manual-review flags
- `cr-1.1.3-data-sources-cs1017.json` (`CS1-EP001-PKG-CR-1.1-DATA-SOURCES`): 1 migrate, 0 tier-1, 0 manual-review flags
- `cr-1.1.2-stages-tools-cs1017.json` (`CS1-EP001-PKG-CR-1.1-STAGES-TOOLS`): 1 migrate, 0 tier-1, 0 manual-review flags
- `cr-1.2.3-pca-cs1017.json` (`CS1-EP001-PKG-CR-1.2-PCA`): 1 migrate, 0 tier-1, 0 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `5.1.4-loss-estimators-cs1003.json`: backlog 6 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `5.1.5-credible-intervals-cs1003.json`: backlog 5 (tier-1 0, manual-review 6, compliant 0, excluded 6)
- `revision-bayesian-cs1015.json`: backlog 5 (tier-1 0, manual-review 6, compliant 0, excluded 6)
- `revision-hypothesis-testing-cs1012.json`: backlog 4 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `revision-midspine-cs1003.json`: backlog 2 (tier-1 0, manual-review 4, compliant 0, excluded 4)
- `1.2.3-pca-cs1002.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `4.1.1-response-explanatory-cs1003.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `4.1.1-response-explanatory-cs1013.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cp-4.1.1-linear-regression-cs1016.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-1.1.3-data-sources-cs1017.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-1.1.2-stages-tools-cs1017.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-1.2.3-pca-cs1017.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
