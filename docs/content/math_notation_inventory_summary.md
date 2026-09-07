# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T12:10:58Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `c1368d42a7b99c6dadf87e3a666c158315b6b0584b9beea91f5525c3b0ddfef8`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 530 |
| Needs migration | 1409 |
| Migrated (dollar-delimited) | 511 |
| Correctly excluded | 264 |
| Needs manual review (flag) | 463 |
| Confident automated (no flag) | 1740 |
| Packages with migration backlog | 104 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-risk compound calculation boards (12 packages, 170 needs_migration strings).

- `4.2.6-deviance-estimation-cs1014.json` (`CS1-EP001-PKG-CX-4.2-DEVIANCE-ESTIMATION`): 17 migrate, 2 tier-1, 3 manual-review flags
- `3.2.7-ci-paired-means-cs1011.json` (`CS1-EP001-PKG-3.2-CI-PAIRED-MEANS`): 16 migrate, 2 tier-1, 1 manual-review flags
- `4.2.6-deviance-estimation-cs1003.json` (`CS1-EP001-PKG-4.2-DEVIANCE-ESTIMATION`): 16 migrate, 2 tier-1, 4 manual-review flags
- `3.2.3-ci-given-sampling-distribution-cs1011.json` (`CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION`): 15 migrate, 2 tier-1, 6 manual-review flags
- `4.1.2-simple-multiple-cs1013.json` (`CS1-EP001-PKG-CN-4.1-SIMPLE-MULTIPLE`): 15 migrate, 2 tier-1, 4 manual-review flags
- `5.1.3-posterior-simple-cs1003.json` (`CS1-EP001-PKG-5.1-POSTERIOR-SIMPLE`): 11 migrate, 2 tier-1, 1 manual-review flags
- `5.1.9-bayes-vs-eb-cs1015.json` (`CS1-EP001-PKG-CO-5.1-BAYES-VS-EB`): 10 migrate, 2 tier-1, 5 manual-review flags
- `revision-sampling-distributions-cs1009.json` (`CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS`): 9 migrate, 2 tier-1, 3 manual-review flags
- `revision-linear-regression-cs1013.json` (`CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU`): 7 migrate, 2 tier-1, 7 manual-review flags
- `revision-central-limit-theorem-cs1008.json` (`CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM`): 6 migrate, 2 tier-1, 0 manual-review flags
- `4.2.2-mean-variance-cs1003.json` (`CS1-EP001-PKG-4.2-MEAN-VARIANCE`): 29 migrate, 1 tier-1, 11 manual-review flags
- `3.2.6-ci-two-sample-cs1011.json` (`CS1-EP001-PKG-3.2-CI-TWO-SAMPLE`): 19 migrate, 1 tier-1, 4 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

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
