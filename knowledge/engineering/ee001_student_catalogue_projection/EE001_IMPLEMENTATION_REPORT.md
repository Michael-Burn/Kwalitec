# EE-001 — Implementation Report

**Programme:** EE-001 — Student Catalogue Projection Fix  
**Status:** Complete  
**Date:** 2026-07-29  
**Predecessor:** EV-001 (VERIFIED WITH MINOR CONDITIONS)  
**Scope:** Student Subject Catalogue projection only

---

## Summary

Fixed student catalogue release-date formatting so Ready published subjects are discoverable without HTTP 500. `PublishedCurriculumAuthority` already projects `published_at` as an ISO-8601 **string**; `_format_release` incorrectly assumed a `datetime` and called `.strftime`, raising `AttributeError` on Choose Exam.

The projection layer now coerces `datetime | date | str | None` before formatting. Publication, validation, preview, approval, Ready generation, Foundation package materialisation, and the authority model were **not** modified.

---

## Root cause (confirmed)

| Layer | Contract |
|---|---|
| ORM `PublishedCurriculumPackage.published_at` | `datetime` |
| Authority `PublishedPackageSnapshot.published_at` | `str` (via `.isoformat()`) |
| Catalogue `_format_release` (before EE-001) | Assumed `datetime` only |

Catalogue `_active_package` reads authority snapshots, so runtime values were strings. EV-001 already proved the Ready package exists for CS1V; only projection formatting failed.

---

## Fix

1. Added `_coerce_release(value)` — normalises authority strings, ORM datetimes, and dates; returns `None` for blank/unparseable input (no raise).
2. Updated `_format_release` to format the coerced value (`%d %b %Y`).
3. `_from_published` stores the coerced `datetime | None` on `release_date`.
4. Corrected `_active_package` return annotation to `PublishedPackageSnapshot | None` (matches authority contract).

---

## Files Created

- `tests/application/platform_integration/test_subject_catalogue.py`
- `knowledge/engineering/ee001_student_catalogue_projection/EE001_IMPLEMENTATION_REPORT.md`
- `knowledge/engineering/ee001_student_catalogue_projection/REGRESSION_REPORT.md`
- `knowledge/engineering/ee001_student_catalogue_projection/STUDENT_DISCOVERY_VERIFICATION.md`

---

## Files Modified

- `app/application/platform_integration/subject_catalogue.py` — release coercion / formatting only

---

## Files intentionally not modified

- Publication pipeline / `publication_service.py` / `publication_bridge.py`
- Validation / Preview / Approval services
- Ready / Foundation package generation
- `PublishedCurriculumAuthority` / authority DTO / ORM model

---

## Tests Executed

```bash
python3 -m pytest tests/application/platform_integration/test_subject_catalogue.py tests/test_px002_product_experience.py -v
python3 -m ruff check app/application/platform_integration/subject_catalogue.py tests/application/platform_integration/test_subject_catalogue.py
```

**Outcome:** 20 passed; ruff clean.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved: catalogue remains a student-facing read model over authority + discovery.
- Curriculum V1/V2 invariants: N/A (projection-only; no curriculum engine/traversal changes).
- Authority contract unchanged; projection adapted to the existing string projection.

---

## Technical Debt

None introduced. Unparseable release strings render an empty label rather than 500 — acceptable for display resilience.

---

## Known Limitations

- Enrolment selectability still depends on Runtime C bridge flags (`ENABLE_RUNTIME_C_ENROLMENT`); Ready discoverability with a published package is independent of that gate (existing PX-002 behaviour).
- EE-001 does not re-run Founder Studio blind validation (FV-001B) or student blind validation (FV-001C).

---

## Exit criteria

| Criterion | Status |
|---|---|
| Student Subject Catalogue loads | ✓ |
| Ready subjects discoverable | ✓ |
| No HTTP 500 from `_format_release` | ✓ |
| Published metadata (Ready / Version / Published Date) correct | ✓ |
| Publication pipeline unchanged | ✓ |

---

## Next programme

**FV-001B — Final Founder Studio Blind Validation**, then **FV-001C — Student Blind Validation**.
