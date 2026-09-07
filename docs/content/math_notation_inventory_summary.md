# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T11:22:39Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `051fd8c98f68ee61eefd288a5bb880afce92154d66ba879018e0cb9eebd5308e`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 326 |
| Needs migration | 1613 |
| Migrated (dollar-delimited) | 307 |
| Correctly excluded | 264 |
| Needs manual review (flag) | 463 |
| Confident automated (no flag) | 1740 |
| Packages with migration backlog | 108 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-risk compound calculation boards (12 packages, 222 needs_migration strings).

- `3.2.4-ci-normal-mean-variance-cs1011.json` (`CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE`): 19 migrate, 5 tier-1, 8 manual-review flags
- `3.3.4-chi-square-gof-cs1012.json` (`CS1-EP001-PKG-3.3-CHI-SQUARE-GOF`): 19 migrate, 4 tier-1, 7 manual-review flags
- `cp-3.1.1-estimators-cs1016.json` (`CS1-EP001-PKG-CP-3.1-ESTIMATORS`): 17 migrate, 4 tier-1, 3 manual-review flags
- `3.1.6-bootstrap-estimator-cs1010.json` (`CS1-EP001-PKG-3.1-BOOTSTRAP-ESTIMATOR`): 16 migrate, 4 tier-1, 4 manual-review flags
- `5.1.8-empirical-bayes-cs1015.json` (`CS1-EP001-PKG-CO-5.1-EMPIRICAL-BAYES`): 14 migrate, 4 tier-1, 4 manual-review flags
- `5.1.8-empirical-bayes-cs1003.json` (`CS1-EP001-PKG-5.1-EMPIRICAL-BAYES`): 13 migrate, 4 tier-1, 2 manual-review flags
- `cp-2.5.1-clt-cs1016.json` (`CS1-EP001-PKG-CP-2.5-CLT`): 31 migrate, 3 tier-1, 2 manual-review flags
- `3.1.3-efficiency-bias-consistency-mse-cs1010.json` (`CS1-EP001-PKG-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE`): 23 migrate, 3 tier-1, 0 manual-review flags
- `3.1.5-asymptotic-mle-cs1010.json` (`CS1-EP001-PKG-3.1-ASYMPTOTIC-MLE`): 20 migrate, 3 tier-1, 1 manual-review flags
- `4.1.2-simple-multiple-cs1003.json` (`CS1-EP001-PKG-4.1-SIMPLE-MULTIPLE`): 20 migrate, 3 tier-1, 5 manual-review flags
- `3.3.5-contingency-independence-cs1012.json` (`CS1-EP001-PKG-3.3-CONTINGENCY-INDEPENDENCE`): 19 migrate, 3 tier-1, 5 manual-review flags
- `cp-revision-spine-memory-cs1016.json` (`CS1-EP001-PKG-REV-SPINE-MEMORY-PI`): 11 migrate, 3 tier-1, 1 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `3.2.4-ci-normal-mean-variance-cs1011.json`: backlog 19 (tier-1 5, manual-review 8, compliant 0, excluded 6)
- `3.3.4-chi-square-gof-cs1012.json`: backlog 19 (tier-1 4, manual-review 7, compliant 0, excluded 3)
- `cp-3.1.1-estimators-cs1016.json`: backlog 17 (tier-1 4, manual-review 3, compliant 0, excluded 3)
- `3.1.6-bootstrap-estimator-cs1010.json`: backlog 16 (tier-1 4, manual-review 4, compliant 0, excluded 4)
- `5.1.8-empirical-bayes-cs1015.json`: backlog 14 (tier-1 4, manual-review 4, compliant 0, excluded 2)
- `5.1.8-empirical-bayes-cs1003.json`: backlog 13 (tier-1 4, manual-review 2, compliant 0, excluded 1)
- `cp-2.5.1-clt-cs1016.json`: backlog 31 (tier-1 3, manual-review 2, compliant 0, excluded 0)
- `3.1.3-efficiency-bias-consistency-mse-cs1010.json`: backlog 23 (tier-1 3, manual-review 0, compliant 0, excluded 0)
- `3.1.5-asymptotic-mle-cs1010.json`: backlog 20 (tier-1 3, manual-review 1, compliant 0, excluded 1)
- `4.1.2-simple-multiple-cs1003.json`: backlog 20 (tier-1 3, manual-review 5, compliant 0, excluded 2)
- `3.3.5-contingency-independence-cs1012.json`: backlog 19 (tier-1 3, manual-review 5, compliant 0, excluded 2)
- `cp-revision-spine-memory-cs1016.json`: backlog 11 (tier-1 3, manual-review 1, compliant 0, excluded 0)
- `4.2.6-deviance-estimation-cs1014.json`: backlog 17 (tier-1 2, manual-review 3, compliant 0, excluded 1)
- `3.2.7-ci-paired-means-cs1011.json`: backlog 16 (tier-1 2, manual-review 1, compliant 0, excluded 0)
- `4.2.6-deviance-estimation-cs1003.json`: backlog 16 (tier-1 2, manual-review 4, compliant 0, excluded 0)
- `3.2.3-ci-given-sampling-distribution-cs1011.json`: backlog 15 (tier-1 2, manual-review 6, compliant 0, excluded 5)
- `4.1.2-simple-multiple-cs1013.json`: backlog 15 (tier-1 2, manual-review 4, compliant 0, excluded 1)
- `5.1.3-posterior-simple-cs1003.json`: backlog 11 (tier-1 2, manual-review 1, compliant 0, excluded 0)
- `5.1.9-bayes-vs-eb-cs1015.json`: backlog 10 (tier-1 2, manual-review 5, compliant 0, excluded 3)
- `revision-sampling-distributions-cs1009.json`: backlog 9 (tier-1 2, manual-review 3, compliant 0, excluded 3)
- `revision-linear-regression-cs1013.json`: backlog 7 (tier-1 2, manual-review 7, compliant 0, excluded 6)
- `revision-central-limit-theorem-cs1008.json`: backlog 6 (tier-1 2, manual-review 0, compliant 0, excluded 0)
- `4.2.2-mean-variance-cs1003.json`: backlog 29 (tier-1 1, manual-review 11, compliant 0, excluded 5)
- `3.2.6-ci-two-sample-cs1011.json`: backlog 19 (tier-1 1, manual-review 4, compliant 0, excluded 1)
- `3.2.2-prediction-interval-cs1011.json`: backlog 18 (tier-1 1, manual-review 2, compliant 0, excluded 2)
