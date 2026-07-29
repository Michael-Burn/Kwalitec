# PX-001 — Subject Catalogue Design

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Design (authoritative for student-facing subject discovery)

---

## 1. Purpose

Create a **first-class Subject Catalogue**. Students interact with **Subjects**, not Curriculum Editions or Studio workspaces.

The catalogue is the student-facing projection of Founder-published curriculum authority. It does not redesign CKG / Twin / Decisions.

---

## 2. Catalogue record (required fields)

Each catalogue entry exposes:

| Field | Student meaning | Source (implementation projection) |
|-------|-----------------|--------------------------------------|
| **Name** | Exam / subject display name | `StudioFoundationSubject` title / published package title |
| **Status** | Lifecycle posture of the *subject offer* | Derived from publication + support policy |
| **Current Published Edition** | Human-safe edition label (e.g. “2025 Syllabus”) | Active `PublishedCurriculumPackage` / version label — **not** workspace IDs |
| **Availability** | **Ready** or **Coming Soon** | See §4 |
| **Version** | Version string students may cite | `StudioFoundationVersion` / package version |
| **Release Date** | When the current published edition became available | Package publish timestamp |

Students must not see: draft workspace IDs, extraction job IDs, CIP entity counts, Knowledge Graph node totals, or “Failed” pipeline states.

---

## 3. Surfaces

### 3.1 Student — primary

| Surface | Role |
|---------|------|
| **Subject Catalogue** (new or elevated) | Browse available exams before / during onboarding |
| **Choose Exam** onboarding step | Catalogue-driven selection (replaces examining-body + “Published Curriculum” dual path as the primary mental model) |
| Study Plan entry points | Deep-link into catalogue or filtered Ready subjects |

### 3.2 Founder — operational

| Surface | Role |
|---------|------|
| **Subjects** (Founder Studio nav) | Create / manage subject records |
| Curriculum Studio workspace | Author editions that *feed* the catalogue on publish |
| Publishing / Versions | Control which edition is Current Published Edition |

Founders manage subjects and editions; the **catalogue** is the read model students see after publish.

---

## 4. Availability model

### Student-facing values (authoritative)

| Availability | Selectable? | Behaviour |
|--------------|-------------|-----------|
| **Ready** | Yes | Student may choose the subject and continue onboarding |
| **Coming Soon** | No | Card visible (optional) or listed as unavailable; selection blocked |

**Unavailable** subjects (not Ready and not shown as Coming Soon) must not be selectable. Prefer omitting them from the primary student list; if shown for roadmap honesty, treat as Coming Soon.

### Mapping from current PTP-001 statuses

| PTP-001 today | PX-001 student label | Enrolment |
|---------------|----------------------|-----------|
| Supported | **Ready** | Allowed |
| Coming Soon | **Coming Soon** | Blocked |
| Not Supported | Omit or Coming Soon (product choice: prefer omit from primary catalogue) | Blocked |

Internal code may keep `SUPPORTED` tokens; **student UI copy** must say Ready / Coming Soon.

### Coming Soon message (required tone)

Professional, non-technical, no Studio jargon. Example:

> This subject’s verified curriculum is still under preparation. It will appear as Ready when publishing is complete. You cannot enrol yet.

Do **not** say: “Curriculum Studio”, “extraction failed”, “Knowledge Graph incomplete”, “Runtime C disabled”.

---

## 5. Status vs Availability

Keep **Status** and **Availability** distinct:

| Concept | Audience | Examples |
|---------|----------|----------|
| **Status** | Mostly Founder; optional muted student badge | Drafting, In review, Published, Archived |
| **Availability** | Student decision surface | Ready, Coming Soon |

A subject with Status = Published and a current package is **Ready**.  
A subject created but not published is **Coming Soon** (or omitted).  
Archived subjects leave the student catalogue.

---

## 6. Student interaction rules

1. Students select a **Subject** card — never a workspace or edition editor.  
2. Only **Ready** subjects advance onboarding.  
3. Choosing Ready binds later enrolment to the **Current Published Edition** via existing PI-002A / LP-001 paths — no new educational math.  
4. Catalogue does not start Twin / Decisions; enrolment hooks do.  
5. Built-in V1 papers (e.g. on-disk CS1) may appear as Ready when support policy says so — still labelled as Subjects, not “JSON curricula”.

---

## 7. Founder → Catalogue publish path

```
New Subject
  → Upload CMP
  → Upload Syllabus
  → Extraction / Review / Corrections
  → Publish Verified Curriculum
  → Catalogue Availability = Ready
       (Name, Current Published Edition, Version, Release Date populated)
```

Until Publish succeeds with a student-consumable package, Availability must not be Ready.

---

## 8. Data / architecture notes (non-redesign)

| Concern | Guidance |
|---------|----------|
| SSOT for student-consumable curriculum | Keep `PublishedCurriculumPackage` / `PublishedCurriculumAuthority` |
| Subject identity | Keep `StudioFoundationSubject` |
| Discovery service | Evolve `PublishedSubjectDiscoveryService` + `SubjectSupportService` projections toward catalogue DTO |
| Wizard | Shrink to catalogue-first Choose Exam; do not invent a second enrolment authority |
| EI | Unchanged; catalogue is presentation + policy labels |

---

## 9. Acceptance checks

- [ ] Catalogue fields present for every Ready subject  
- [ ] Coming Soon not selectable  
- [ ] No draft editions listed as Ready  
- [ ] No CMP / syllabus / publish / Knowledge Graph affordances on catalogue UI  
- [ ] Enrolment of Ready subject still invokes LP-001 / bridge — not a parallel path  

---

**End of Subject Catalogue Design**
