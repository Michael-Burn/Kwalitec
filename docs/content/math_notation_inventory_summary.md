# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T17:02:07Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `dc56c21a08a79a8f531ab7f0641660fa3d4e3cdde2bf4f6537f7354698aa5993`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 1236 |
| Needs migration | 700 |
| Migrated (dollar-delimited) | 1217 |
| Correctly excluded | 267 |
| Needs manual review (flag) | 402 |
| Confident automated (no flag) | 1801 |
| Packages with migration backlog | 65 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-backlog migration boards (no tier-1 remaining) (12 packages, 251 needs_migration strings).

- `4.2.5-linear-predictor-cs1014.json` (`CS1-EP001-PKG-CX-4.2-LINEAR-PREDICTOR`): 25 migrate, 0 tier-1, 15 manual-review flags
- `2.2.1-marginal-conditional-cs1005.json` (`CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL`): 24 migrate, 0 tier-1, 0 manual-review flags
- `revision-joint-distributions-cs1005.json` (`CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS`): 23 migrate, 0 tier-1, 1 manual-review flags
- `2.4.2-moment-via-gf-cs1007.json` (`CS1-EP001-PKG-2.4-MOMENT-VIA-GF`): 22 migrate, 0 tier-1, 3 manual-review flags
- `3.3.1-hypothesis-concepts-cs1012.json` (`CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS`): 22 migrate, 0 tier-1, 4 manual-review flags
- `4.2.4-factors-interactions-cs1014.json` (`CS1-EP001-PKG-CX-4.2-FACTORS-INTERACTIONS`): 22 migrate, 0 tier-1, 11 manual-review flags
- `cp-2.1.3-prob-quantiles-cs1016.json` (`CS1-EP001-PKG-CP-2.1-PROB-QUANTILES`): 21 migrate, 0 tier-1, 4 manual-review flags
- `5.1.1-bayes-theorem-cs1003.json` (`CS1-EP001-PKG-5.1-BAYES-THEOREM`): 20 migrate, 0 tier-1, 0 manual-review flags
- `4.2.5-linear-predictor-cs1003.json` (`CS1-EP001-PKG-4.2-LINEAR-PREDICTOR`): 19 migrate, 0 tier-1, 16 manual-review flags
- `4.2.1-exponential-family-cs1014.json` (`CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY`): 19 migrate, 0 tier-1, 7 manual-review flags
- `2.1.3-prob-quantiles-cs1004.json` (`CS1-EP001-PKG-2.1-PROB-QUANTILES`): 18 migrate, 0 tier-1, 5 manual-review flags
- `5.1.6-credibility-premium-cs1015.json` (`CS1-EP001-PKG-CO-5.1-CREDIBILITY-PREMIUM`): 16 migrate, 0 tier-1, 12 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

- `4.2.5-linear-predictor-cs1014.json`: backlog 25 (tier-1 0, manual-review 15, compliant 0, excluded 8)
- `2.2.1-marginal-conditional-cs1005.json`: backlog 24 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `revision-joint-distributions-cs1005.json`: backlog 23 (tier-1 0, manual-review 1, compliant 0, excluded 0)
- `2.4.2-moment-via-gf-cs1007.json`: backlog 22 (tier-1 0, manual-review 3, compliant 1, excluded 0)
- `3.3.1-hypothesis-concepts-cs1012.json`: backlog 22 (tier-1 0, manual-review 4, compliant 0, excluded 2)
- `4.2.4-factors-interactions-cs1014.json`: backlog 22 (tier-1 0, manual-review 11, compliant 0, excluded 4)
- `cp-2.1.3-prob-quantiles-cs1016.json`: backlog 21 (tier-1 0, manual-review 4, compliant 1, excluded 0)
- `5.1.1-bayes-theorem-cs1003.json`: backlog 20 (tier-1 0, manual-review 0, compliant 0, excluded 0)
- `4.2.5-linear-predictor-cs1003.json`: backlog 19 (tier-1 0, manual-review 16, compliant 0, excluded 11)
- `4.2.1-exponential-family-cs1014.json`: backlog 19 (tier-1 0, manual-review 7, compliant 0, excluded 1)
- `2.1.3-prob-quantiles-cs1004.json`: backlog 18 (tier-1 0, manual-review 5, compliant 1, excluded 1)
- `5.1.6-credibility-premium-cs1015.json`: backlog 16 (tier-1 0, manual-review 12, compliant 0, excluded 7)
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
