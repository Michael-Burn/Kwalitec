# EE-001 — Student Discovery Verification

**Programme:** EE-001 — Student Catalogue Projection Fix  
**Date:** 2026-07-29  
**Clears:** EV-001 minor condition #1 (Choose Exam HTTP 500)

---

## Verification objective

Confirm published Ready subjects are discoverable on student surfaces with correct metadata and without server errors.

---

## Positive path

| Check | Expected | Result | Evidence |
|---|---|---|---|
| Published subject appears in Subject Catalogue service | Ready entry present | Pass | `test_published_ready_subject_appears_with_metadata` |
| Availability label | `Ready` | Pass | same |
| Version | Published version label (e.g. `2026.1`) | Pass | same |
| Published / release date | Formatted `dd Mon YYYY` from authority `published_at` | Pass | same + `test_authority_string_published_at_does_not_500` |
| Choose Exam (`/study-plan/wizard/1`) | HTTP 200; subject code, Ready, version visible | Pass | `test_choose_exam_renders_published_subject` |
| Authority ISO string path (EV-001 failure mode) | No `AttributeError`; label `29 Jul 2026` | Pass | `test_authority_string_published_at_does_not_500` |

---

## Student discovery surfaces covered

1. **Subject Catalogue read model** — `SubjectCatalogueService.list_entries` / `_from_published`
2. **Choose Exam** — Study Plan wizard step 1 HTML
3. **Discovery offer chain** — `PublishedSubjectDiscoveryService` → catalogue projection

---

## EV-001 condition clearance

EV-001 recorded:

> Student Choose Exam 500 — `SubjectCatalogueService._format_release` raises `AttributeError` when authority `published_at` is a `str`. Active Ready package for CS1V exists.

EE-001 fixes that projection assumption. The Ready package / publication lifecycle remains as verified by EV-001; only formatting coercion changed.

---

## Live instance note

A development probe against `instance/kwalitec.sqlite3` on 2026-07-29 showed **no** active published packages in that particular local file (`list_published() == ()`). Discovery verification for EE-001 therefore relies on the automated suite (which publishes a real Foundation package via `publish_subject` and exercises the authority string contract). Re-confirmation against a DB that still holds EV-001’s CS1V package is optional and expected during FV-001C.

---

## Exit mapping

| Exit criterion | Status |
|---|---|
| Student Subject Catalogue loads | ✓ |
| Ready subjects discoverable | ✓ |
| No HTTP 500 | ✓ |
| Published metadata displayed correctly | ✓ |
| Publication pipeline unchanged | ✓ (see REGRESSION_REPORT) |
