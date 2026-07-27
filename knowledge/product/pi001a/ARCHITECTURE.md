# PI-001A — Architecture: Founder Curriculum Studio Foundation

**Programme:** PI-001A — Founder Curriculum Studio Foundation  
**Status:** Authoritative for this milestone  
**Date:** 2026-07-27  

---

## 1. Purpose

Enable founders to onboard **entirely new subjects** without developer intervention by making curriculum the single source of truth for the educational engine.

This milestone delivers the **durable foundation** for the Founder Curriculum Studio lifecycle. It does **not** implement mission generation, study plans, recommendation logic, or UI polish.

---

## 2. Required lifecycle

```text
Create Subject
    → Upload CMP
    → Upload Syllabus
    → Extract
    → Parse
    → Validate
    → Founder Review
    → Publish Curriculum Version
```

Every stage is **observable** (processing / publication state) and **auditable** (append-only audit events).

---

## 3. Architecture overview

```text
Founder UI (Curriculum Studio presentation)
        │
        ├─ existing V2 Studio orchestration (in-memory Management / Ingestion ports)
        │
        └─ CurriculumStudioFoundationService  ← PI-001A durable spine
                    │
                    ├─ Curriculum Ingestion Engine (extract / parse / validate)
                    ├─ SQLAlchemy foundation tables
                    └─ PublishedCurriculumAuthority (student-safe read path)
```

### Layering

| Layer | Package | Responsibility |
|---|---|---|
| Domain | `app/domain/curriculum_studio_foundation/` | Lifecycle stages + publication safety invariants |
| Application | `app/application/curriculum_studio_foundation/` | Orchestration, DTOs, published authority |
| Models | `app/models/curriculum_studio_foundation.py` | Durable ORM |
| Presentation | `app/presentation/curriculum_studio/` | Upload form + route (founder-only) |
| Existing V2 | `curriculum_management` / `curriculum_ingestion` / `curriculum_studio` | Unchanged domain engines; Studio UI continues to use ports |

---

## 4. Database model

| Table | Role |
|---|---|
| `studio_foundation_subjects` | Educational products (subject-agnostic codes) |
| `studio_foundation_versions` | Draft → published version carriers + stage / processing state |
| `studio_foundation_documents` | CMP / syllabus **references** (+ optional abstract structure JSON) |
| `studio_foundation_audit_events` | Append-only lifecycle audit |
| `published_curriculum_packages` | Immutable published packages — **only** student-consumable store |

Migration: `migrations/versions/202607270001_pi001a_curriculum_studio_foundation.py`.

**Invariant:** embedded PDF / data-URI payloads are rejected. References only.

---

## 5. Processing pipeline

```text
Documents (CMP + Syllabus refs + optional abstract entries)
        ↓
CurriculumIngestionEngine.ingest()
        ↓
Extract → Normalize (Parse) → Validation report
        ↓
Persisted on StudioFoundationVersion
  (parsed_structure_json, validation_report_json, processing_state)
```

Foundation maps product language:

| Product stage | Implementation |
|---|---|
| Extract | Ingestion extraction |
| Parse | Ingestion normalisation |
| Validate | Ingestion validation report + version gate |

---

## 6. Validation layer

- Structural validation is owned by **Curriculum Ingestion** (deterministic).
- Foundation stores the immutable report JSON on the version.
- `validate_curriculum(..., require_pass=True)` blocks founder review when the report fails.
- Publication requires **founder approval**, not validation alone.

---

## 7. Versioning model

- Versions are labelled `YYYY.N` (aligned with Curriculum Management).
- Unique per subject (`subject_id` + `version_label`).
- Draft versions live only in `studio_foundation_versions`.
- Publishing materialises an immutable `published_curriculum_packages` row.

---

## 8. Publishing model

1. Founder approves (`FOUNDER_REVIEW` → `approved`).
2. `publish_curriculum` writes `PublishedCurriculumPackage`.
3. Prior active package for the subject is deactivated when `activate=True`.
4. Version `publication_state` becomes `published`.

### Student safety

`PublishedCurriculumAuthority` exposes **only** published packages.  
`is_draft_reachable(version_id)` is always `False`.  
Draft / processing / review rows are never returned on this path.

Bundled JSON curricula (`app/curriculum/data/…`) remain the live student import source for existing papers in this milestone; the published package store is the **authoritative foundation** for founder-onboarded subjects going forward.

---

## 9. Founder workflow

| Stage | Service method |
|---|---|
| Create Subject | `create_subject` |
| Upload CMP / Syllabus | `upload_document` |
| Extract + Parse | `process_curriculum` |
| Track state | `get_processing_state` |
| Review parsed | `review_parsed_curriculum` |
| Validate | `validate_curriculum` |
| Founder Review | `founder_review` |
| Publish | `publish_curriculum` |
| Audit | `list_audit_events` |

Studio UI gains a functional **Content Sources** upload form (references) wired to the existing Studio `upload_sources` port path.

---

## 10. Extensibility (future subjects without developers)

- Subject codes are free-form product codes (`LAW1`, `CM9`, …) — not CS1-hardcoded.
- Document kinds are enumerated (`cmp`, `syllabus`, …) without paper-specific parsers in foundation.
- Ingestion consumes **abstract entries** so new subjects supply structure via upload, not code changes.
- Evidence: `test_subject_agnostic_second_subject` publishes `LAW1` end-to-end.

---

## 11. Explicit non-goals (this milestone)

- Mission generation / study plans / recommendations  
- PDF binary parsing / OCR  
- Cutover of existing CS1 student plans onto published packages  
- UI polish beyond functional upload  
