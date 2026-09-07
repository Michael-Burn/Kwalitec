# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T18:04:39Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `df51fb5afdec262b0048c26d7adcbb7e4e5b4d9901dffa2f3a38f188abc3fd2b`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 1458 |
| Needs migration | 478 |
| Migrated (dollar-delimited) | 1439 |
| Correctly excluded | 267 |
| Needs manual review (flag) | 387 |
| Confident automated (no flag) | 1816 |
| Packages with migration backlog | 58 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (12 packages, 173 needs_migration strings).

- `4.2.3-link-canonical-cs1014.json` (`CS1-EP001-PKG-CX-4.2-LINK-CANONICAL`): 16 migrate, 0 tier-1, 7 manual-review flags
- `2.6.6-f-distribution-cs1009.json` (`CS1-EP001-PKG-2.6-F-DISTRIBUTION`): 15 migrate, 0 tier-1, 6 manual-review flags
- `3.2.1-confidence-interval-parameter-cs1011.json` (`CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER`): 15 migrate, 0 tier-1, 3 manual-review flags
- `4.2.1-exponential-family-cs1003.json` (`CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY`): 15 migrate, 0 tier-1, 6 manual-review flags
- `4.2.7-model-choice-cs1014.json` (`CS1-EP001-PKG-CX-4.2-MODEL-CHOICE`): 15 migrate, 0 tier-1, 5 manual-review flags
- `4.1.5-variable-selection-cs1003.json` (`CS1-EP001-PKG-4.1-VARIABLE-SELECTION`): 14 migrate, 0 tier-1, 12 manual-review flags
- `4.2.4-factors-interactions-cs1003.json` (`CS1-EP001-PKG-4.2-FACTORS-INTERACTIONS`): 14 migrate, 0 tier-1, 6 manual-review flags
- `4.2.3-link-canonical-cs1003.json` (`CS1-EP001-PKG-4.2-LINK-CANONICAL`): 14 migrate, 0 tier-1, 9 manual-review flags
- `4.2.7-model-choice-cs1003.json` (`CS1-EP001-PKG-4.2-MODEL-CHOICE`): 14 migrate, 0 tier-1, 5 manual-review flags
- `5.1.6-credibility-premium-cs1003.json` (`CS1-EP001-PKG-5.1-CREDIBILITY-PREMIUM`): 14 migrate, 0 tier-1, 11 manual-review flags
- `4.1.5-variable-selection-cs1013.json` (`CS1-EP001-PKG-CN-4.1-VARIABLE-SELECTION`): 14 migrate, 0 tier-1, 13 manual-review flags
- `2.2.2-independence-cs1005.json` (`CS1-EP001-PKG-2.2-INDEPENDENCE`): 13 migrate, 0 tier-1, 0 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `4.2.3-link-canonical-cs1014.json`: backlog 16 (tier-1 0, manual-review 7, compliant 0, excluded 4)
- `2.6.6-f-distribution-cs1009.json`: backlog 15 (tier-1 0, manual-review 6, compliant 0, excluded 2)
- `3.2.1-confidence-interval-parameter-cs1011.json`: backlog 15 (tier-1 0, manual-review 3, compliant 0, excluded 2)
- `4.2.1-exponential-family-cs1003.json`: backlog 15 (tier-1 0, manual-review 6, compliant 0, excluded 1)
- `4.2.7-model-choice-cs1014.json`: backlog 15 (tier-1 0, manual-review 5, compliant 0, excluded 1)
- `4.1.5-variable-selection-cs1003.json`: backlog 14 (tier-1 0, manual-review 12, compliant 0, excluded 7)
- `4.2.4-factors-interactions-cs1003.json`: backlog 14 (tier-1 0, manual-review 6, compliant 0, excluded 4)
- `4.2.3-link-canonical-cs1003.json`: backlog 14 (tier-1 0, manual-review 9, compliant 1, excluded 3)
- `4.2.7-model-choice-cs1003.json`: backlog 14 (tier-1 0, manual-review 5, compliant 0, excluded 2)
- `5.1.6-credibility-premium-cs1003.json`: backlog 14 (tier-1 0, manual-review 11, compliant 0, excluded 7)
- `4.1.5-variable-selection-cs1013.json`: backlog 14 (tier-1 0, manual-review 13, compliant 0, excluded 8)
- `2.2.2-independence-cs1005.json`: backlog 13 (tier-1 0, manual-review 0, compliant 0, excluded 0)
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
