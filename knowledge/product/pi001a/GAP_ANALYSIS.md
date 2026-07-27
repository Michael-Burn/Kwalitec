# PI-001A — Gap Analysis

**Programme:** PI-001A — Founder Curriculum Studio Foundation  
**Date:** 2026-07-27  

Compares the pre-PI-001A codebase with the required Founder Curriculum Studio lifecycle.

---

## 1. Inventory (pre-PI-001A)

### Curriculum runtime (student)

| Area | Location | Notes |
|---|---|---|
| Engine JSON | `app/curriculum/` | Bundled V1/V2 syllabus JSON (CS1, CM1, CB2) |
| ORM | `app/models/curriculum.py` | `Curriculum` / `Section` / `Topic` |
| Services | `CurriculumService`, `CurriculumEngineService` | Import + traversal |
| Subject (missions) | `app/models/subject.py` | User-scoped mission grouping — **not** exam product |

### Founder Curriculum Studio (V2)

| BC | Packages | Persistence |
|---|---|---|
| Curriculum Management | `app/domain|application/curriculum_management/` | **In-memory catalogue only** |
| Curriculum Ingestion | `app/domain|application/curriculum_ingestion/` | **Non-persisting engine** |
| Curriculum Studio | `app/domain|application/curriculum_studio/` | **In-memory StudioRegistry** |
| Presentation | `app/presentation/curriculum_studio/` | Founder UI; missing upload form/route |

---

## 2. Lifecycle gap matrix

| Required stage | Pre-PI-001A | Gap class | PI-001A disposition |
|---|---|---|---|
| Create Subject | Studio + Management (in-memory) | Durable gap | Foundation `create_subject` + table |
| Upload CMP | `upload_sources` service; **no UI route** | Incomplete | Document upload + UI form/route |
| Upload Syllabus | Same | Incomplete | Same |
| Extract | Ingestion engine | Persistence / observability | `process_curriculum` persists state |
| Parse | Ingestion normalisation | Persistence / observability | Stored `parsed_structure_json` |
| Validate | Ingestion + Management gates (memory) | Persistence | Stored report + foundation gate |
| Founder Review | Preview + Approval (memory) | Durable gap | `founder_review` + audit |
| Publish Curriculum Version | Management publish (memory) | SSOT gap | `PublishedCurriculumPackage` |
| Students never see drafts | Soft invariant in docs | Enforcement gap | `PublishedCurriculumAuthority` |
| Stage observability | In-memory activity | Audit gap | Append-only `studio_foundation_audit_events` |
| Onboard subject without developers | JSON files require engineer commit | Product gap | Subject-agnostic durable path |

Gap classes: **Durable** (lost on restart), **Incomplete** (logic without surface), **SSOT** (publish not student-authoritative), **Enforcement** (invariant not coded), **Audit**, **Product**.

---

## 3. Mapping: Studio workflow ↔ required lifecycle

| Studio stage (V2-016) | Required lifecycle |
|---|---|
| Subject | Create Subject |
| Content Sources | Upload CMP + Upload Syllabus |
| Validation | Extract + Parse + Validate |
| Preview + Approval | Founder Review |
| Publication | Publish Curriculum Version |

V2 Studio remains the Founder UX orchestration layer. PI-001A adds the **durable foundation spine** and closes the upload UI gap.

---

## 4. Residual gaps (explicitly deferred)

| Residual | Why deferred |
|---|---|
| Student `CurriculumService` import from published packages | Avoid regressing CS1 plans; cutover is a later programme |
| Real PDF/CMP binary extraction | Engine is abstract-entry based by design |
| Full durable backing of in-memory Management catalogue | Foundation tables cover the onboarding SSOT path first |
| Mission / plan / recommendation changes | Out of scope |

---

## 5. Acceptance coverage

| Criterion | Evidence |
|---|---|
| Create a subject | `CurriculumStudioFoundationService.create_subject` + tests |
| Upload curriculum documents | `upload_document` + Studio upload route/form |
| Track processing state | `get_processing_state` / version `processing_state` |
| Review parsed curriculum | `review_parsed_curriculum` |
| Validate curriculum | `validate_curriculum` |
| Publish a curriculum version | `publish_curriculum` → `published_curriculum_packages` |
| Future subjects without developers | `LAW1` subject-agnostic integration test |
