# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T19:29:54Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `ff4a1114c7708c2cf7ed746b5e88407ffac91160863524c86ec7243a68b489e1`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 1664 |
| Needs migration | 261 |
| Migrated (dollar-delimited) | 1645 |
| Correctly excluded | 278 |
| Needs manual review (flag) | 300 |
| Confident automated (no flag) | 1903 |
| Packages with migration backlog | 36 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (12 packages, 135 needs_migration strings).

- `2.6.2-sampling-distribution-statistic-cs1009.json` (`CS1-EP001-PKG-2.6-SAMPLING-DISTRIBUTION-STATISTIC`): 13 migrate, 0 tier-1, 2 manual-review flags
- `3.3.3-permutation-tests-cs1012.json` (`CS1-EP001-PKG-3.3-PERMUTATION-TESTS`): 13 migrate, 0 tier-1, 7 manual-review flags
- `2.1.5-inverse-transform-cs1004.json` (`CS1-EP001-PKG-2.1-INVERSE-TRANSFORM`): 12 migrate, 0 tier-1, 5 manual-review flags
- `5.1.5-credible-intervals-cs1015.json` (`CS1-EP001-PKG-CO-5.1-CREDIBLE-INTERVALS`): 12 migrate, 0 tier-1, 7 manual-review flags
- `cp-3.2.1-ci-sample-cs1016.json` (`CS1-EP001-PKG-CP-3.2-CI-SAMPLE`): 12 migrate, 0 tier-1, 3 manual-review flags
- `3.2.8-bootstrap-confidence-interval-cs1011.json` (`CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL`): 11 migrate, 0 tier-1, 5 manual-review flags
- `5.1.7-bayesian-credibility-cs1015.json` (`CS1-EP001-PKG-CO-5.1-BAYESIAN-CREDIBILITY`): 11 migrate, 0 tier-1, 6 manual-review flags
- `cr-2.1.1-discrete-cs1017.json` (`CS1-EP001-PKG-CR-2.1-DISCRETE`): 11 migrate, 0 tier-1, 1 manual-review flags
- `5.1.7-bayesian-credibility-cs1003.json` (`CS1-EP001-PKG-5.1-BAYESIAN-CREDIBILITY`): 10 migrate, 0 tier-1, 3 manual-review flags
- `5.1.4-loss-estimators-cs1015.json` (`CS1-EP001-PKG-CO-5.1-LOSS-ESTIMATORS`): 10 migrate, 0 tier-1, 2 manual-review flags
- `cp-3.3.1-hypothesis-testing-cs1016.json` (`CS1-EP001-PKG-CP-3.3-HYPOTHESIS-TESTING`): 10 migrate, 0 tier-1, 4 manual-review flags
- `cr-1.2.2-correlation-cs1017.json` (`CS1-EP001-PKG-CR-1.2-CORRELATION`): 10 migrate, 0 tier-1, 2 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `2.6.2-sampling-distribution-statistic-cs1009.json`: backlog 13 (tier-1 0, manual-review 2, compliant 0, excluded 2)
- `3.3.3-permutation-tests-cs1012.json`: backlog 13 (tier-1 0, manual-review 7, compliant 0, excluded 3)
- `2.1.5-inverse-transform-cs1004.json`: backlog 12 (tier-1 0, manual-review 5, compliant 5, excluded 0)
- `5.1.5-credible-intervals-cs1015.json`: backlog 12 (tier-1 0, manual-review 7, compliant 0, excluded 6)
- `cp-3.2.1-ci-sample-cs1016.json`: backlog 12 (tier-1 0, manual-review 3, compliant 0, excluded 3)
- `3.2.8-bootstrap-confidence-interval-cs1011.json`: backlog 11 (tier-1 0, manual-review 5, compliant 0, excluded 4)
- `5.1.7-bayesian-credibility-cs1015.json`: backlog 11 (tier-1 0, manual-review 6, compliant 0, excluded 2)
- `cr-2.1.1-discrete-cs1017.json`: backlog 11 (tier-1 0, manual-review 1, compliant 0, excluded 0)
- `5.1.7-bayesian-credibility-cs1003.json`: backlog 10 (tier-1 0, manual-review 3, compliant 0, excluded 2)
- `5.1.4-loss-estimators-cs1015.json`: backlog 10 (tier-1 0, manual-review 2, compliant 0, excluded 1)
- `cp-3.3.1-hypothesis-testing-cs1016.json`: backlog 10 (tier-1 0, manual-review 4, compliant 0, excluded 2)
- `cr-1.2.2-correlation-cs1017.json`: backlog 10 (tier-1 0, manual-review 2, compliant 0, excluded 1)
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
