# PX-001 — Terminology Changes

**Programme:** PX-001 — Operational Model Alignment  
**Date:** 2026-07-28  
**Status:** Design (authoritative for student-facing and Founder-calm product language)

---

## 1. Principle

Replace **implementation terminology** with **domain terminology** on product surfaces.

Prefer:

| Prefer (domain) | Avoid exposing (implementation) |
|-----------------|----------------------------------|
| **Subject** | Curriculum Edition (as the thing students pick) |
| **Study Plan** | Enrolment bridge / Runtime C enrolment (as UI nouns) |
| **Today’s Focus** | Opaque “this topic” without a real subject name; prefer over stacking Mission / Sensei jargon when clarifying daily work |
| **Verified Curriculum** | Draft workspace, extraction output, CIP package |

Educational Intelligence internal names (SCI, Twin, Runtime, Educational Decision, Knowledge Graph) remain **engineering vocabulary** — never student chrome. Founder Studio may use careful operator language; Critical jargon still harms founder calm (FV-001).

---

## 2. Glossary (product)

| Term | Meaning | Audience |
|------|---------|----------|
| **Subject** | An exam / paper the learner prepares for | Both |
| **Subject Catalogue** | List of subjects with Ready / Coming Soon | Student (+ Founder ops view) |
| **Verified Curriculum** | Published, student-consumable official curriculum | Both (Founder publishes; Student consumes) |
| **Current Published Edition** | The live verified package for a subject | Catalogue metadata |
| **Study Plan** | Student’s plan bound to a Ready subject + dates + availability | Student |
| **Today’s Focus** | What to study now (product framing for the daily recommendation / mission surface) | Student |
| **Ready** | Subject available to enrol | Student |
| **Coming Soon** | Subject under preparation — not selectable | Student |
| **Founder Studio** / **Curriculum Studio** | Curriculum Authority workspace | Founder only |
| **Review Queue** | Extraction review & corrections | Founder only |
| **Official CMP** | Official core reading / CMP document | Founder only |
| **Official Syllabus** | Official syllabus document | Founder only |

---

## 3. Student surface replacements

| Current / observed | Replace with | Severity |
|--------------------|--------------|----------|
| Published Curriculum (wizard category) | Subjects / Subject Catalogue / Ready subjects | High |
| “published by founders through Curriculum Studio” | Omit; say Verified Curriculum is Ready | High |
| Supported (badge) | **Ready** | High |
| Coming Soon | **Coming Soon** (keep) | — |
| Not Supported | Omit from catalogue or Coming Soon | Medium |
| Study Sensei (as implied chat coach) | Avoid expectation mismatch; prefer product name + Today’s Focus | Medium (FV-001) |
| Decision Journal | Softer student label in later copy pass (e.g. Study decisions) — out of critical path for catalogue | Medium |
| Educational Timeline | Softer progress language — later copy pass | Medium |
| Education Operating System (hero framing) | Prefer plain study-prep framing for first-run Welcome | Medium |
| Mission (keep if product-standard) | Pair with **Today’s Focus** where students need plain English | Low–Medium |
| Estimated Knowledge | Prefer readiness / progress plain language in later pass | Medium |
| SCI / Runtime / Twin / Educational Decision | **Forbidden** on student UI | Critical |

---

## 4. Founder surface replacements

| Current | Prefer | Notes |
|---------|--------|-------|
| Content (nav) | Subjects / Curriculum Studio / … | Per navigation design |
| Curriculum Intelligence Pipeline | Extraction / Curriculum processing (or hide under Quality → Advanced) | FV-001 Critical |
| Knowledge Graph (primary tab brand) | Structure map / Curriculum structure (or Advanced) | Founder-only; still calm language |
| Evidence Explorer | Supporting evidence (Advanced) | Founder-only |
| Entity Details | Topic / objective details | Founder-only |
| Publish Curriculum Version | Publish Verified Curriculum | Align with domain |
| UPLOADED BY &lt;user id&gt; | Uploaded by &lt;name/email&gt; or omit id | Minor |

Official CMP / Official Syllabus may remain — they are Founder-domain documents, not student chrome.

---

## 5. Terms that stay internal (code / docs only)

Do not put these in student UI. Prefer not as Founder primary nav brands:

- SCI, CKG (as acronyms on chrome)
- Twin / Digital Twin
- Runtime A / B / C
- Educational Decision / Experience Model
- PipelineCoordinator, CipCurriculumEntity
- `FoundationStage` enum tokens (`create_subject`, …) — use STAGE_LABELS / product labels instead

---

## 6. Alignment with existing language law

| Source | Relationship |
|--------|--------------|
| `app/presentation/product_language.py` | Update in follow-on implementation to encode Ready / Subject Catalogue / Verified Curriculum |
| `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` | Extend; do not contradict PX-001 Operational Model |
| FV-001 `TERMINOLOGY_AUDIT.md` | Inputs for Critical / Major fixes |
| PTP-001 support labels | Keep internal statuses; change **student-visible** copy to Ready / Coming Soon |

Where PX-001 conflicts with older “Supported” student copy, **PX-001 wins**.

---

## 7. Acceptance checks

- [ ] Student Choose Exam speaks Subjects / Ready / Coming Soon only  
- [ ] No student string mentions upload, publish, extraction, Knowledge Graph, or Curriculum Studio  
- [ ] Catalogue uses Verified Curriculum / Version / Release Date language  
- [ ] Founder primary nav uses domain workflow labels  
- [ ] Critical EI acronyms absent from student Home / Session / Wizard / Catalogue  

---

**End of Terminology Changes**
