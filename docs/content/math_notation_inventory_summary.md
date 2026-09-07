# Mathematical Notation Inventory Summary

**Generated:** 2026-09-07T14:29:57Z
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md`
**Content fingerprint:** `91bb90c2a107c0d45fac34cd4b7800d2874417761e92412b262b709d1424da3a`
**Live packages scanned:** 130

## Totals

| Category | Count |
|---|---:|
| Mathish strings inventoried | 2203 |
| Already compliant | 881 |
| Needs migration | 1055 |
| Migrated (dollar-delimited) | 862 |
| Correctly excluded | 267 |
| Needs manual review (flag) | 402 |
| Confident automated (no flag) | 1801 |
| Packages with migration backlog | 72 |

## Limits of automation

Semantic role (live mathematical object vs prose mention) cannot be decided by pattern matching in every case. Strings with needs_manual_review=true must be human-checked before a wave marks them done or skips them.

## Recommended first migration wave (order only)

Order only: tackle highest-risk compound calculations first for immediate student benefit. This does not narrow ultimate scope; every needs_migration string remains in backlog until migrated or reclassified by manual review.

**Wave 1:** Highest-risk compound calculation boards (1 packages, 6 needs_migration strings).

- `revision-linear-models-cs1003.json` (`CS1-EP001-PKG-REV-LINEAR-MODELS`): 6 migrate, 1 tier-1, 5 manual-review flags

## How to refresh

```bash
python scripts/inventory_math_notation.py
```

Ledger JSON: `docs/content/math_notation_inventory.json`.

## Per-package backlog (top 25 by tier-1 then backlog)

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
