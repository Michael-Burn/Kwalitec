# Mathematical Notation Inventory Summary

**Generated:** 2026-09-06T18:18:04Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `b260a506b3205d16543790e33b7588568941e825d0cefd72a070f3fb7bf431dd`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 19 |
| Needs migration | 1928 |
| Correctly excluded | 256 |
| Needs manual review (flag) | 486 |
| Confident automated (no flag) | 1717 |
| Packages with migration backlog | 120 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-risk compound calculation boards (12 packages, 315 needs_migration strings).

- `4.1.3-least-squares-cs1003.json` (`CS1-EP001-PKG-4.1-LEAST-SQUARES`): 24 migrate, 10 tier-1, 0 manual-review flags
- `4.1.3-least-squares-cs1013.json` (`CS1-EP001-PKG-CN-4.1-LEAST-SQUARES`): 23 migrate, 9 tier-1, 0 manual-review flags
- `4.2.8-residuals-cs1014.json` (`CS1-EP001-PKG-CX-4.2-RESIDUALS`): 28 migrate, 8 tier-1, 5 manual-review flags
- `4.2.8-residuals-cs1003.json` (`CS1-EP001-PKG-4.2-RESIDUALS`): 22 migrate, 8 tier-1, 1 manual-review flags
- `2.6.3-mean-var-sample-cs1009.json` (`CS1-EP001-PKG-2.6-MEAN-VAR-SAMPLE`): 38 migrate, 7 tier-1, 4 manual-review flags
- `2.6.5-t-statistic-cs1009.json` (`CS1-EP001-PKG-2.6-T-STATISTIC`): 27 migrate, 7 tier-1, 11 manual-review flags
- `3.1.2-maximum-likelihood-cs1010.json` (`CS1-EP001-PKG-3.1-MAXIMUM-LIKELIHOOD`): 25 migrate, 7 tier-1, 0 manual-review flags
- `3.2.5-ci-binomial-poisson-cs1011.json` (`CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON`): 20 migrate, 7 tier-1, 2 manual-review flags
- `2.5.1-clt-cs1008.json` (`CS1-EP001-PKG-2.5-CLT`): 32 migrate, 6 tier-1, 2 manual-review flags
- `2.6.4-normal-sample-mean-var-cs1009.json` (`CS1-EP001-PKG-2.6-NORMAL-SAMPLE-MEAN-VAR`): 31 migrate, 5 tier-1, 13 manual-review flags
- `3.1.4-comparison-mse-cs1010.json` (`CS1-EP001-PKG-3.1-COMPARISON-MSE`): 25 migrate, 5 tier-1, 9 manual-review flags
- `3.1.1-method-of-moments-cs1010.json` (`CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS`): 20 migrate, 5 tier-1, 3 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `4.1.3-least-squares-cs1003.json`: backlog 24 (tier-1 10, manual-review 0, compliant 0, excluded 0)
- `4.1.3-least-squares-cs1013.json`: backlog 23 (tier-1 9, manual-review 0, compliant 0, excluded 0)
- `4.2.8-residuals-cs1014.json`: backlog 28 (tier-1 8, manual-review 5, compliant 0, excluded 0)
- `4.2.8-residuals-cs1003.json`: backlog 22 (tier-1 8, manual-review 1, compliant 0, excluded 0)
- `2.6.3-mean-var-sample-cs1009.json`: backlog 38 (tier-1 7, manual-review 4, compliant 0, excluded 3)
- `2.6.5-t-statistic-cs1009.json`: backlog 27 (tier-1 7, manual-review 11, compliant 0, excluded 8)
- `3.1.2-maximum-likelihood-cs1010.json`: backlog 25 (tier-1 7, manual-review 0, compliant 0, excluded 0)
- `3.2.5-ci-binomial-poisson-cs1011.json`: backlog 20 (tier-1 7, manual-review 2, compliant 0, excluded 1)
- `2.5.1-clt-cs1008.json`: backlog 32 (tier-1 6, manual-review 2, compliant 0, excluded 0)
- `2.6.4-normal-sample-mean-var-cs1009.json`: backlog 31 (tier-1 5, manual-review 13, compliant 0, excluded 6)
- `3.1.4-comparison-mse-cs1010.json`: backlog 25 (tier-1 5, manual-review 9, compliant 0, excluded 7)
- `3.1.1-method-of-moments-cs1010.json`: backlog 20 (tier-1 5, manual-review 3, compliant 0, excluded 2)
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
