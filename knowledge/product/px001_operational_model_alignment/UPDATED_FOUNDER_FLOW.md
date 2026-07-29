# PX-001 — Updated Founder Flow

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Authoritative Founder product workflow

---

## 1. Persona

The Founder is the **Curriculum Authority** — the only role that creates or modifies curricula.

Educational Intelligence is not operated as a separate “build Twin” step in this flow. Publishing Verified Curriculum makes subjects Ready; EI personalises **students** after enrolment (LP-001 / VP-001).

---

## 2. Canonical workflow

```
New Subject
    ↓
Upload CMP
    ↓
Upload Syllabus
    ↓
Extraction
    ↓
Review
    ↓
Corrections
    ↓
Publish
    ↓
Available to Students
```

Domain stage spine (unchanged engineering order):

`CREATE_SUBJECT → UPLOAD_CMP → UPLOAD_SYLLABUS → EXTRACT → PARSE → VALIDATE → FOUNDER_REVIEW → PUBLISH`

Product UI may group PARSE / VALIDATE under Extraction quality and Quality nav, but must not ask Founders to invent a different order.

---

## 3. Stage-by-stage product behaviour

| Stage | Founder action | Outcome | Student impact |
|-------|----------------|---------|----------------|
| **New Subject** | Create subject (name, identity) | Subject exists; catalogue Coming Soon or omitted | Not Ready |
| **Upload CMP** | Upload Official CMP | Document attached to working edition | None |
| **Upload Syllabus** | Upload Official Syllabus | Syllabus attached | None |
| **Extraction** | Run / monitor extraction | Structure derived for review | None |
| **Review** | Inspect extracted structure | Issues queued | None |
| **Corrections** | Approve / reject / remap / fix | Verified structure ready to publish | None |
| **Publish** | Publish Verified Curriculum; assign version | `PublishedCurriculumPackage` student-consumable | Subject → **Ready** in catalogue |
| **Available to Students** | Optional QA / version check | Catalogue fields populated (Name, Edition, Version, Release Date) | Students may enrol |

Failed extraction or refused publish **must not** mark the subject Ready.

---

## 4. Navigation framing

Primary Founder chrome (see `NAVIGATION_CHANGES.md`):

1. Subjects  
2. Curriculum Studio  
3. Review Queue  
4. Publishing  
5. Versions  
6. Quality  

Secondary ops (Students, Platform, Support) must not interrupt the curriculum path as if they were required steps to publish.

---

## 5. Responsibilities checklist

| Responsibility | In this flow? |
|----------------|---------------|
| Create subjects | ✓ |
| Upload official CMP | ✓ |
| Upload official syllabus | ✓ |
| Review extraction | ✓ |
| Correct extraction | ✓ |
| Publish verified curriculum | ✓ |
| Version management | ✓ |
| Curriculum quality assurance | ✓ |
| Upload on behalf of students | ✗ — students never upload |
| Redesign Twin / Decisions / Runtime | ✗ — out of scope |

---

## 6. What “Available to Students” means

After successful Publish:

1. Subject Catalogue **Availability = Ready**.  
2. Current Published Edition, Version, and Release Date are set.  
3. Student onboarding may select the subject.  
4. Enrolment triggers LP-001 onboard (and existing bridge) — Founder does not manually “start EI” per student.

Draft, processing, ready_for_review, approved-but-unpublished, archived, and failed states are **not** Available.

---

## 7. Relationship to existing Studio

| Existing capability | PX-001 presentation |
|---------------------|---------------------|
| `create_subject` | New Subject |
| Document upload CMP / syllabus | Upload CMP / Upload Syllabus |
| Pipeline / CIP extract | Extraction |
| Review queue / entity approve-reject-remap | Review + Corrections |
| validate / preview / approve | Quality (+ Publishing gate) |
| publish / assign_version | Publish + Versions |
| Knowledge Graph UI | Founder Advanced / Quality — never student |

Do not fork a second Studio. Reshape navigation and language around the existing spine (PI-001).

---

## 8. Acceptance checks

- [ ] Founder can complete New Subject → … → Publish without student shell  
- [ ] Publish is the only transition that makes a subject Ready  
- [ ] Review / Corrections occur before Publish in the happy path  
- [ ] No requirement for Founder to touch Twin diagnostics to release a subject  
- [ ] Student catalogue updates from publish, not from draft upload  

---

**End of Updated Founder Flow**
