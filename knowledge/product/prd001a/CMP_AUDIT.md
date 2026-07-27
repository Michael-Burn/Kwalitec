# PRD-001A — CMP Audit

---

## What “CMP” means in Kwalitec

| Context | Meaning |
|---|---|
| Educational boundary | **IFoA Core Materials Pack** (and notes/papers) — students bring official materials; Kwalitec does not replace them |
| Curriculum Studio | **Document kind** `DocumentKind.CMP = "cmp"` — required source reference before curriculum publication validation |
| Student product myth | “Upload my syllabus / map my CMP into the app” — **not** an implemented student journey |

Evidence: Educational Planning Model adjacency; `app/domain/curriculum_ingestion/curriculum_document.py`; `CURRICULUM_STUDIO.md` Stage 2 gate; private-beta blind reviews (students keep CMP beside the product).

---

## Is CMP upload required / optional / automatic / missing?

| Actor | Status |
|---|---|
| **Student** | **Not implemented** — neither required nor optional in-app. Model is **BYO materials outside the product**. |
| **Founder / Curriculum Studio** | **Required for publish validation** (`cmp_uploaded` + official syllabus). |
| **Automatic** | **No** automatic CMP ingest from student accounts. |
| **Placeholder** | Studio **service** can register CMP/syllabus **reference strings**; HTTP workspace **lacks upload UI/form**. |

---

## If implemented — founder workflow (intended)

```
Founder Console → Curriculum Studio workspace
  → upload_sources(cmp_reference, syllabus_reference)  [application service]
  → Ingestion
  → Validation (fails if MISSING_CMP)
  → Preview → Approve → Publish
```

**Implemented:** application `workspace_service.upload_sources`, validation issue `MISSING_CMP`, stage checklist language.  
**Not wired for operators in UI:** file upload fields / routes in `curriculum_studio` templates/routes (actions: validate/preview/publish/advance only).

Learner syllabuses in alpha are **pre-bundled JSON** (`cs1`/`cm1`/`cb2` 2026), not CMP-derived per student.

---

## Student journey vs Blueprint

| Blueprint expectation | Alignment |
|---|---|
| Understand official curriculum | Met via bundled JSON, not via CMP upload |
| Not a question bank / not replacing textbooks | Aligned — CMP stays external |
| Educational intelligence over student’s materials | **Not** met as CMP integration — no mapping of student’s pack pages into missions |
| Version 1 shipped curricula | Met for supported IFoA papers |

**Verdict:** Absence of a student CMP workflow is **not** a regression against Blueprint Version 1 claims if CMP is understood as **external materials adjacency**. It **is** a gap against founder/student expectations that “syllabus mapping” or “CMP workflow” appears inside the EOS. Classify carefully:

- Student CMP upload: **Category E** (never built as student feature)  
- Founder Studio upload UI: **Category C** (backend/policy exists, UI disconnected)  
- Expectation that CMP drives Daily Mission: **Category F** risk (product language / mental model drift) if marketing implies materials intelligence

---

## Does current student journey align with Blueprint?

**Partially.**

- Aligns with “companion beside materials,” not “upload CMP to unlock product.”  
- Misaligns with student desire to **see** syllabus/CMP structure mirrored in the app (Journey helps; full mapping missing).  
- Calibration “declared coverage” is **not** CMP and **not** Estimated Knowledge — another potential confusion vector.
