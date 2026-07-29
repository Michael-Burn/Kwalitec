# EE-001 — Regression Report

**Programme:** EE-001 — Student Catalogue Projection Fix  
**Date:** 2026-07-29

---

## Scope

Confirm that repairing release-date coercion does **not** surface non-Ready curricula to students, and does not alter publication lifecycle behaviour.

---

## Catalogue visibility regressions

| Scenario | Expected | Result | Evidence |
|---|---|---|---|
| Draft subject (created, versioned, never published) | Hidden from Published catalogue | Pass | `test_draft_subject_hidden` |
| Incomplete subject (partial upload, never published) | Hidden | Pass | `test_incomplete_subject_hidden` |
| Validated but unpublished | Hidden | Pass | `test_validated_but_unpublished_hidden` |
| Validation failure / empty structures, never published | Hidden | Pass | `test_validation_failure_hidden` |
| Unsupported legacy paper (e.g. CFA Level I) | Omitted | Pass | `test_catalogue_omits_unavailable` (PX-002) |
| Coming Soon legacy papers | Visible as Coming Soon, not selectable | Pass | `test_coming_soon_not_selectable` (PX-002) |

---

## Publication pipeline unchanged

EE-001 modified only `subject_catalogue.py` projection helpers.

Not touched:

- Validation service / policy wiring
- Preview service
- Approval / founder review
- Publication service / publication bridge
- Foundation Ready package materialisation
- Authority snapshot construction (still projects `published_at` as `str`)

Existing PX-002 surface tests continue to pass (`tests/test_px002_product_experience.py`).

---

## Formatting edge cases

| Input | Expected label | Result |
|---|---|---|
| ISO string `2026-07-29T10:15:30` | `29 Jul 2026` | Pass |
| ISO string with `Z` | `29 Jul 2026` | Pass |
| `datetime(2026, 1, 5, …)` | `05 Jan 2026` | Pass |
| `None` / blank | empty | Pass |
| Unparseable string | empty (no raise) | Pass |

---

## Commands

```bash
python3 -m pytest tests/application/platform_integration/test_subject_catalogue.py tests/test_px002_product_experience.py -v
```

**Outcome:** 20 passed.

---

## Residual risk

Low. Discovery still depends on active `PublishedCurriculumPackage` rows and bridge discovery flags. A subject that is Ready in Studio but discovery-flag-off remains hidden — unchanged pre-EE-001 behaviour.
