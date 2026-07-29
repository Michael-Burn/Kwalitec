# PX-002 — Terminology Implementation Report

**Programme:** PX-002  
**Date:** 2026-07-28  
**Authority:** `TERMINOLOGY_CHANGES.md` (PX-001)

---

## Principle applied

Replace implementation terminology with domain terminology on product surfaces. Internal EI names remain engineering vocabulary.

---

## Student replacements implemented

| Before | After | Where |
|--------|-------|-------|
| Supported | **Ready** | `SubjectSupportService` labels, badges, gate |
| Not Supported | **Unavailable** (omit from catalogue) | Support service + catalogue omit |
| Published Curriculum category | **Subjects** / catalogue cards | Discovery category name + Choose Exam |
| “published by founders through Curriculum Studio” | Omitted; Ready / verified language | Discovery + support explanations |
| Education Operating System (welcome) | Plain study-prep framing | Alpha onboarding |
| Today's Mission (default hero fallback) | **Today's Focus** | `student/home.html` |
| What you did / What happens next | What you completed / What happens tomorrow | Home commitment reflection |
| Supported alternatives | Ready alternatives | Support gate partial |

## Founder replacements implemented

| Before | After | Where |
|--------|-------|-------|
| Content (nav) | Subjects / Curriculum Studio / Review Queue / Publishing / Versions / Quality | `nav.py` |
| Publish Curriculum | **Publish Verified Curriculum** | Studio form + flash + product_language |
| Operational decisions (sidebar) | Curriculum Authority | Console sidebar |

## Constants updated

- `FOUNDER_PRIMARY_NAV_LABELS` in `app/presentation/product_language.py`
- `FOUNDER_STUDIO_CTAS` publish label
- Coming Soon canonical message in `subject_catalogue.py` / support service

## Still internal (not student chrome)

SCI, Twin, Runtime A/B/C, Educational Decision, Knowledge Graph, CIP acronyms, FoundationStage enum tokens.

---

## Acceptance

- [x] Choose Exam speaks Subjects / Ready / Coming Soon  
- [x] No student Choose Exam string mentions upload / publish / extraction / Knowledge Graph / Curriculum Studio  
- [x] Catalogue uses Version / Updated (release) metadata  
- [x] Founder primary nav uses domain workflow labels  
- [x] Critical EI acronyms absent from Choose Exam / Begin Learning / catalogue  

---

**End of Terminology Implementation Report**
