# Mathematical Notation Inventory Summary

**Generated:** 2026-09-08T03:27:43Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `cc3754d6c572a8ac5815d55a1d801bd486f4e327db8497b84d5c677a7f63f3dc`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 1869 |
| Needs migration | 53 |
| Migrated (dollar-delimited) | 1850 |
| Correctly excluded | 281 |
| Needs manual review (flag) | 279 |
| Confident automated (no flag) | 1924 |
| Packages with migration backlog | 24 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (12 packages, 41 needs_migration strings).

- `5.1.4-loss-estimators-cs1003.json` (`CS1-EP001-PKG-5.1-LOSS-ESTIMATORS`): 6 migrate, 0 tier-1, 0 manual-review flags
- `5.1.5-credible-intervals-cs1003.json` (`CS1-EP001-PKG-5.1-CREDIBLE-INTERVALS`): 5 migrate, 0 tier-1, 6 manual-review flags
- `revision-bayesian-cs1015.json` (`CS1-EP001-PKG-REV-BAYESIAN-OMICRON`): 5 migrate, 0 tier-1, 6 manual-review flags
- `revision-glm-cs1014.json` (`CS1-EP001-PKG-REV-GLM-XI`): 5 migrate, 0 tier-1, 6 manual-review flags
- `revision-hypothesis-testing-cs1012.json` (`CS1-EP001-PKG-REV-HYPOTHESIS-TESTING`): 4 migrate, 0 tier-1, 0 manual-review flags
- `5.1.2-prior-posterior-cs1003.json` (`CS1-EP001-PKG-5.1-PRIOR-POSTERIOR`): 3 migrate, 0 tier-1, 7 manual-review flags
- `revision-distributions-generation-cs1004.json` (`CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION`): 3 migrate, 0 tier-1, 6 manual-review flags
- `revision-regression-glm-cs1003.json` (`CS1-EP001-PKG-REV-REGRESSION-GLM`): 3 migrate, 0 tier-1, 6 manual-review flags
- `5.1.2-prior-posterior-cs1015.json` (`CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR`): 2 migrate, 0 tier-1, 6 manual-review flags
- `revision-estimators-cs1010.json` (`CS1-EP001-PKG-REV-ESTIMATORS`): 2 migrate, 0 tier-1, 2 manual-review flags
- `revision-midspine-cs1003.json` (`CS1-EP001-PKG-REV-MIDSPINE`): 2 migrate, 0 tier-1, 4 manual-review flags
- `1.2.3-pca-cs1002.json` (`CS1-CS1002-PKG-1.2-PCA`): 1 migrate, 0 tier-1, 0 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `5.1.4-loss-estimators-cs1003.json`: backlog 6 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `5.1.5-credible-intervals-cs1003.json`: backlog 5 (tier-1 0, manual-review 6, compliant 0, excluded 6)
- `revision-bayesian-cs1015.json`: backlog 5 (tier-1 0, manual-review 6, compliant 0, excluded 6)
- `revision-glm-cs1014.json`: backlog 5 (tier-1 0, manual-review 6, compliant 4, excluded 1)
- `revision-hypothesis-testing-cs1012.json`: backlog 4 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `5.1.2-prior-posterior-cs1003.json`: backlog 3 (tier-1 0, manual-review 7, compliant 5, excluded 4)
- `revision-distributions-generation-cs1004.json`: backlog 3 (tier-1 0, manual-review 6, compliant 7, excluded 3)
- `revision-regression-glm-cs1003.json`: backlog 3 (tier-1 0, manual-review 6, compliant 5, excluded 3)
- `5.1.2-prior-posterior-cs1015.json`: backlog 2 (tier-1 0, manual-review 6, compliant 7, excluded 4)
- `revision-estimators-cs1010.json`: backlog 2 (tier-1 0, manual-review 2, compliant 6, excluded 0)
- `revision-midspine-cs1003.json`: backlog 2 (tier-1 0, manual-review 4, compliant 0, excluded 4)
- `1.2.3-pca-cs1002.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `2.1.2-continuous-cs1002.json`: backlog 1 (tier-1 0, manual-review 2, compliant 5, excluded 1)
- `2.1.1-discrete-cs1002.json`: backlog 1 (tier-1 0, manual-review 1, compliant 7, excluded 0)
- `1.2.2-eda-association-ep001.json`: backlog 1 (tier-1 0, manual-review 2, compliant 6, excluded 1)
- `2.1.4-poisson-process-cs1004.json`: backlog 1 (tier-1 0, manual-review 4, compliant 9, excluded 3)
- `2.1.6-software-generation-cs1004.json`: backlog 1 (tier-1 0, manual-review 2, compliant 7, excluded 1)
- `4.1.1-response-explanatory-cs1003.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `4.1.1-response-explanatory-cs1013.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cp-4.1.1-linear-regression-cs1016.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-1.1.3-data-sources-cs1017.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-1.1.2-stages-tools-cs1017.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-1.2.3-pca-cs1017.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cr-2.1.2-continuous-cs1017.json`: backlog 1 (tier-1 0, manual-review 2, compliant 7, excluded 1)
