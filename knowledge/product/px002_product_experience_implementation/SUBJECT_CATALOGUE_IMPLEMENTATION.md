# PX-002 — Subject Catalogue Implementation

**Programme:** PX-002  
**Date:** 2026-07-28  
**Authority:** `SUBJECT_CATALOGUE_DESIGN.md` (PX-001)

---

## Purpose

First-class Subject Catalogue so students browse **Subjects**, not curriculum editions or Studio workspaces.

---

## Read model

`app/application/platform_integration/subject_catalogue.py`

| Field | Source |
|-------|--------|
| Name | Catalogue / published title |
| Status | Published / Under preparation (muted) |
| Current Published Edition | Human edition label |
| Availability | Ready / Coming Soon |
| Version | Curriculum version or package version_label |
| Release / Updated date | Package `published_at` when available |

Projection uses existing:

- `PublishedSubjectDiscoveryService`
- `PublishedCurriculumAuthority` / `PublishedCurriculumPackage`
- `SubjectSupportService` (internal SUPPORTED / COMING_SOON / NOT_SUPPORTED)

---

## Availability behaviour

| Availability | Selectable | Behaviour |
|--------------|------------|-----------|
| Ready | Yes | Advances onboarding |
| Coming Soon | No | Shows preparation message; no radio input |
| Unavailable | Omitted | Not listed in primary catalogue |

Coming Soon message:

> This subject’s verified curriculum is still under preparation. It will become available when publishing is complete. You cannot start studying this exam yet.

---

## Surface

Primary: Study Plan wizard **Choose Exam** (`wizard_step_1.html`).

Enrolment of a Ready subject still binds via existing wizard → review → `FounderStudentEnrolmentBridge` / Runtime A Study Plan create → LP-001 onboard. No parallel intelligence bootstrap.

---

## Acceptance

- [x] Catalogue fields present for Ready subjects  
- [x] Coming Soon not selectable  
- [x] No draft editions listed as Ready  
- [x] No CMP / syllabus / publish / Knowledge Graph affordances on catalogue UI  
- [x] Enrolment still invokes LP-001 / bridge  

---

**End of Subject Catalogue Implementation**
