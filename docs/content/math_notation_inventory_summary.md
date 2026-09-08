# Mathematical Notation Inventory Summary

**Generated:** 2026-09-08T02:21:37Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `dc9a7e89b701a56a9e4842f7e0a6874d89cc800795d609d39f2cb897be463726`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 1778 |
| Needs migration | 147 |
| Migrated (dollar-delimited) | 1759 |
| Correctly excluded | 278 |
| Needs manual review (flag) | 300 |
| Confident automated (no flag) | 1903 |
| Packages with migration backlog | 34 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (12 packages, 97 needs_migration strings).

- `2.1.4-poisson-process-cs1004.json` (`CS1-EP001-PKG-2.1-POISSON-PROCESS`): 9 migrate, 0 tier-1, 4 manual-review flags
- `5.1.2-prior-posterior-cs1015.json` (`CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR`): 9 migrate, 0 tier-1, 6 manual-review flags
- `revision-distributions-generation-cs1004.json` (`CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION`): 9 migrate, 0 tier-1, 6 manual-review flags
- `revision-glm-cs1014.json` (`CS1-EP001-PKG-REV-GLM-XI`): 9 migrate, 0 tier-1, 6 manual-review flags
- `2.1.1-discrete-cs1002.json` (`CS1-CS1002-PKG-2.1-DISCRETE`): 8 migrate, 0 tier-1, 1 manual-review flags
- `2.1.6-software-generation-cs1004.json` (`CS1-EP001-PKG-2.1-SOFTWARE-GENERATION`): 8 migrate, 0 tier-1, 2 manual-review flags
- `5.1.2-prior-posterior-cs1003.json` (`CS1-EP001-PKG-5.1-PRIOR-POSTERIOR`): 8 migrate, 0 tier-1, 7 manual-review flags
- `cr-2.1.2-continuous-cs1017.json` (`CS1-EP001-PKG-CR-2.1-CONTINUOUS`): 8 migrate, 0 tier-1, 2 manual-review flags
- `revision-estimators-cs1010.json` (`CS1-EP001-PKG-REV-ESTIMATORS`): 8 migrate, 0 tier-1, 2 manual-review flags
- `revision-regression-glm-cs1003.json` (`CS1-EP001-PKG-REV-REGRESSION-GLM`): 8 migrate, 0 tier-1, 6 manual-review flags
- `1.2.2-eda-association-ep001.json` (`CS1-EP001-PKG-1.2-EDA-ASSOCIATION`): 7 migrate, 0 tier-1, 2 manual-review flags
- `2.1.2-continuous-cs1002.json` (`CS1-CS1002-PKG-2.1-CONTINUOUS`): 6 migrate, 0 tier-1, 2 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `2.1.4-poisson-process-cs1004.json`: backlog 9 (tier-1 0, manual-review 4, compliant 1, excluded 3)
- `5.1.2-prior-posterior-cs1015.json`: backlog 9 (tier-1 0, manual-review 6, compliant 0, excluded 4)
- `revision-distributions-generation-cs1004.json`: backlog 9 (tier-1 0, manual-review 6, compliant 1, excluded 3)
- `revision-glm-cs1014.json`: backlog 9 (tier-1 0, manual-review 6, compliant 0, excluded 1)
- `2.1.1-discrete-cs1002.json`: backlog 8 (tier-1 0, manual-review 1, compliant 0, excluded 0)
- `2.1.6-software-generation-cs1004.json`: backlog 8 (tier-1 0, manual-review 2, compliant 0, excluded 1)
- `5.1.2-prior-posterior-cs1003.json`: backlog 8 (tier-1 0, manual-review 7, compliant 0, excluded 4)
- `cr-2.1.2-continuous-cs1017.json`: backlog 8 (tier-1 0, manual-review 2, compliant 0, excluded 1)
- `revision-estimators-cs1010.json`: backlog 8 (tier-1 0, manual-review 2, compliant 0, excluded 0)
- `revision-regression-glm-cs1003.json`: backlog 8 (tier-1 0, manual-review 6, compliant 0, excluded 3)
- `1.2.2-eda-association-ep001.json`: backlog 7 (tier-1 0, manual-review 2, compliant 0, excluded 1)
- `2.1.2-continuous-cs1002.json`: backlog 6 (tier-1 0, manual-review 2, compliant 0, excluded 1)
- `5.1.4-loss-estimators-cs1003.json`: backlog 6 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `2.1.5-inverse-transform-cs1004.json`: backlog 5 (tier-1 0, manual-review 5, compliant 12, excluded 0)
- `5.1.5-credible-intervals-cs1003.json`: backlog 5 (tier-1 0, manual-review 6, compliant 0, excluded 6)
- `revision-bayesian-cs1015.json`: backlog 5 (tier-1 0, manual-review 6, compliant 0, excluded 6)
- `3.3.3-permutation-tests-cs1012.json`: backlog 4 (tier-1 0, manual-review 7, compliant 9, excluded 3)
- `5.1.7-bayesian-credibility-cs1015.json`: backlog 4 (tier-1 0, manual-review 6, compliant 7, excluded 2)
- `revision-hypothesis-testing-cs1012.json`: backlog 4 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cp-3.3.1-hypothesis-testing-cs1016.json`: backlog 2 (tier-1 0, manual-review 4, compliant 8, excluded 2)
- `revision-midspine-cs1003.json`: backlog 2 (tier-1 0, manual-review 4, compliant 0, excluded 4)
- `1.2.3-pca-cs1002.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `3.2.8-bootstrap-confidence-interval-cs1011.json`: backlog 1 (tier-1 0, manual-review 5, compliant 10, excluded 4)
- `4.1.1-response-explanatory-cs1003.json`: backlog 1 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `5.1.7-bayesian-credibility-cs1003.json`: backlog 1 (tier-1 0, manual-review 3, compliant 9, excluded 2)
