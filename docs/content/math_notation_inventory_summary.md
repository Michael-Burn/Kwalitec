# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T13:35:44Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `fdb7c0d9feba9cf27371322f630e871d194794de1bd464b2c52659807f7f6a37`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 716 |
| Needs migration | 1221 |
| Migrated (dollar-delimited) | 697 |
| Correctly excluded | 266 |
| Needs manual review (flag) | 421 |
| Confident automated (no flag) | 1782 |
| Packages with migration backlog | 84 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-risk compound calculation boards (12 packages, 166 needs_migration strings).

- `3.2.2-prediction-interval-cs1011.json` (`CS1-EP001-PKG-3.2-PREDICTION-INTERVAL`): 18 migrate, 1 tier-1, 2 manual-review flags
- `3.3.2-basic-tests-cs1012.json` (`CS1-EP001-PKG-3.3-BASIC-TESTS`): 18 migrate, 1 tier-1, 2 manual-review flags
- `4.1.4-software-inference-cs1003.json` (`CS1-EP001-PKG-4.1-SOFTWARE-INFERENCE`): 17 migrate, 1 tier-1, 3 manual-review flags
- `4.2.10-fit-interpret-cs1003.json` (`CS1-EP001-PKG-4.2-FIT-INTERPRET`): 15 migrate, 1 tier-1, 3 manual-review flags
- `4.1.4-software-fit-cs1013.json` (`CS1-EP001-PKG-CN-4.1-SOFTWARE-FIT`): 15 migrate, 1 tier-1, 3 manual-review flags
- `4.2.9-goodness-tests-cs1003.json` (`CS1-EP001-PKG-4.2-GOODNESS-TESTS`): 14 migrate, 1 tier-1, 11 manual-review flags
- `4.2.10-fit-interpret-cs1014.json` (`CS1-EP001-PKG-CX-4.2-FIT-INTERPRET`): 14 migrate, 1 tier-1, 3 manual-review flags
- `5.1.3-posterior-simple-cs1015.json` (`CS1-EP001-PKG-CO-5.1-POSTERIOR-SIMPLE`): 13 migrate, 1 tier-1, 2 manual-review flags
- `2.5.2-simulated-sample-normal-cs1008.json` (`CS1-EP001-PKG-2.5-SIMULATED-SAMPLE-NORMAL`): 12 migrate, 1 tier-1, 6 manual-review flags
- `4.2.9-goodness-tests-cs1014.json` (`CS1-EP001-PKG-CX-4.2-GOODNESS-TESTS`): 11 migrate, 1 tier-1, 10 manual-review flags
- `revision-confidence-intervals-cs1011.json` (`CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS`): 11 migrate, 1 tier-1, 4 manual-review flags
- `5.1.9-bayes-vs-eb-cs1003.json` (`CS1-EP001-PKG-5.1-BAYES-VS-EB`): 8 migrate, 1 tier-1, 2 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `3.2.2-prediction-interval-cs1011.json`: backlog 18 (tier-1 1, manual-review 2, compliant 0, excluded 2)
- `3.3.2-basic-tests-cs1012.json`: backlog 18 (tier-1 1, manual-review 2, compliant 0, excluded 1)
- `4.1.4-software-inference-cs1003.json`: backlog 17 (tier-1 1, manual-review 3, compliant 0, excluded 2)
- `4.2.10-fit-interpret-cs1003.json`: backlog 15 (tier-1 1, manual-review 3, compliant 3, excluded 0)
- `4.1.4-software-fit-cs1013.json`: backlog 15 (tier-1 1, manual-review 3, compliant 0, excluded 2)
- `4.2.9-goodness-tests-cs1003.json`: backlog 14 (tier-1 1, manual-review 11, compliant 0, excluded 5)
- `4.2.10-fit-interpret-cs1014.json`: backlog 14 (tier-1 1, manual-review 3, compliant 3, excluded 1)
- `5.1.3-posterior-simple-cs1015.json`: backlog 13 (tier-1 1, manual-review 2, compliant 2, excluded 1)
- `2.5.2-simulated-sample-normal-cs1008.json`: backlog 12 (tier-1 1, manual-review 6, compliant 0, excluded 6)
- `4.2.9-goodness-tests-cs1014.json`: backlog 11 (tier-1 1, manual-review 10, compliant 0, excluded 7)
- `revision-confidence-intervals-cs1011.json`: backlog 11 (tier-1 1, manual-review 4, compliant 0, excluded 3)
- `5.1.9-bayes-vs-eb-cs1003.json`: backlog 8 (tier-1 1, manual-review 2, compliant 0, excluded 2)
- `revision-linear-models-cs1003.json`: backlog 6 (tier-1 1, manual-review 5, compliant 0, excluded 5)
- `2.2.3-cov-corr-expectation-cs1005.json`: backlog 44 (tier-1 0, manual-review 1, compliant 0, excluded 0)
- `2.3.1-conditional-expectation-cs1006.json`: backlog 40 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `2.3.2-mean-variance-conditioning-cs1006.json`: backlog 36 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `cp-5.1.1-bayes-theorem-cs1016.json`: backlog 35 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `2.2.4-linear-combinations-cs1005.json`: backlog 34 (tier-1 0, manual-review 2, compliant 0, excluded 1)
- `5.1.1-bayes-theorem-cs1015.json`: backlog 34 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `2.4.1-mgf-cgf-cs1007.json`: backlog 31 (tier-1 0, manual-review 5, compliant 0, excluded 0)
- `cp-2.2.1-marginal-conditional-cs1016.json`: backlog 29 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `4.2.2-mean-variance-cs1014.json`: backlog 28 (tier-1 0, manual-review 10, compliant 0, excluded 3)
- `revision-conditional-expectations-cs1006.json`: backlog 27 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `revision-generating-functions-cs1007.json`: backlog 26 (tier-1 0, manual-review 1, compliant 0, excluded 0)
- `4.2.5-linear-predictor-cs1014.json`: backlog 25 (tier-1 0, manual-review 15, compliant 0, excluded 8)
