# EI-002 — Curriculum Extraction Architecture

**Programme:** EI-002 — Curriculum Extraction Pipeline  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/curriculum_extraction/` · `app/application/curriculum_extraction/` · `app/infrastructure/adapters/curriculum_extraction/`  
**Depends on:** [EI-001 Curriculum Knowledge Graph](../ei001_curriculum_knowledge_graph/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can understand and model an IFoA curriculum as structured educational knowledge.

Given Canonical Structured Documents for an IFoA CMP and Syllabus, the extraction pipeline constructs a **Draft** Curriculum Knowledge Graph with full source traceability, extraction confidence, validation, and `publication_state=draft` persistence. The output is ready for Founder review and is **not** student-visible.

---

## 2. Canonical Structured Document philosophy

Educational Intelligence **never** operates on PDF bytes (Principle 2).

The sole input contract is the **Canonical Structured Document (CSD)**:

| Element | Role |
|---------|------|
| `CanonicalDocument` | Document identity, kind (`cmp` / `syllabus`), title, `source_ref`, metadata, pages |
| `CanonicalPage` | Logical page with ordered blocks |
| `CanonicalBlock` | `heading` / `paragraph` / `table` / `list` / `list_item` / `caption` / `other` |
| `StructuralLocator` | Permanent recoverability: document, page, block, path, heading, paragraph/table ref |

Future formats (Word, HTML, Markdown, APIs) must adapt **into** CSD. Educational Intelligence stages remain unchanged.

---

## 3. PDF Adapter responsibilities

`PdfCanonicalAdapter` (`app/infrastructure/adapters/curriculum_extraction/`) is **infrastructure only**.

- Uses existing `PdfExtractionPort` for deterministic PDF → `ExtractedDocument`
- Maps pages/blocks into `CanonicalDocument`
- Must not be imported by domain or application pipeline stages
- Does not modify CIP stage contracts

```
PDF bytes → PdfExtractionPort → ExtractedDocument → PdfCanonicalAdapter → CanonicalDocument
```

---

## 4. Extraction pipeline

Facade: `CurriculumExtractionEngine.extract(ExtractionRequest) -> ExtractionResult`

```
Document Import
    ↓
Structural Parsing
    ↓
Curriculum Segmentation
    ↓
Educational Object Extraction
    ↓
Relationship Discovery
    ↓
Draft Curriculum Graph Construction
    ↓
Validation
    ↓ (pass only)
Draft Edition Persist (publication_state=draft)
```

| Stage | Service | Responsibility |
|-------|---------|----------------|
| Document Import | `DocumentImportService` | Validate CSD kinds, non-emptiness, subject metadata |
| Structural Parsing | `StructuralParserService` | Numbered headings, object cues, prerequisite / cross-ref cues |
| Curriculum Segmentation | `CurriculumSegmentationService` | Fuse syllabus + CMP into Topic→Section→Subsection→LO tree |
| Educational Object Extraction | `EducationalObjectExtractor` | Assign `StableCurriculumId`s; materialise EI-001 entities |
| Relationship Discovery | `RelationshipDiscoveryService` | `contains`, `references`, `requires`, `cross_references`, role edges |
| Draft Graph Construction | `DraftGraphConstructor` | Assemble `CurriculumKnowledgeGraph` + provenance map |
| Validation | `GraphValidationService` | Blocker/warning report; gate persistence |
| Draft Persist | `DraftEditionPersistenceService` | Write `ckg_*` as draft only |

Error recovery: typed `CurriculumExtractionError` with stage id; **no partial draft write** when validation has blockers. Replace-on-reextract for the same subject+edition draft.

---

## 5. Graph construction

Uses EI-001 domain entities and relationship catalogue unchanged.

- Syllabus drives LO / syllabus outcome numbering (high confidence)
- CMP contributes definitions, formulas, worked examples, practice exercises, reading references
- Estimated study time and difficulty cues attach to host numbered units
- Stable ids via `StableCurriculumId` helpers (edition-stable; edition label on Subject / edition row)

---

## 6. Source traceability

Every node has sidecar provenance in `ckg_node_provenance`:

- source document id + kind
- page number
- structural path
- section heading
- paragraph or table reference
- extraction confidence (0–100)
- extraction method (`heuristic` | `structured_field` | `adapter_import`)

Educational entity shapes from EI-001 are **not** polluted with extraction metadata.

---

## 7. Confidence scoring (Founder only)

| Score | Band |
|-------|------|
| 99–100 | Highly reliable |
| 90–98 | Review recommended |
| &lt;90 | Manual confirmation required |

Students never see confidence. Low confidence emits validation **warnings** (does not block draft persist).

Examples: numbered syllabus LO → 99; labelled CMP definition → ~92; inferred inline formula → ~88.

---

## 8. Validation rules

| Rule | Severity |
|------|----------|
| Duplicate stable ids | blocker |
| Orphan nodes / missing owners | blocker |
| Broken hierarchy | blocker |
| Invalid relationships / references | blocker |
| Requires cycles / non-LO requires | blocker |
| Incomplete educational objects | blocker |
| Explicit prerequisite cue not materialised | blocker |
| Confidence &lt; 90 | warning |

**Gate:** any blocker → do not persist; return report. Zero blockers → persist draft + store `ckg_validation_reports`.

---

## 9. Draft edition lifecycle

- `ckg_graph_editions.publication_state = "draft"` (EI-002 only writes draft)
- Also stores `validation_status`, `source_cmp_ref`, `source_syllabus_ref`
- No Founder approval UI; no publish transition in this programme
- No `ckg_draft_*` tables; no in-memory-only drafts
- Re-extract of same subject+edition **replaces** prior draft graph nodes/provenance

CKG remains the Single Source of Educational Truth. Only future Founder-approved publish makes curriculum student-visible.

---

## 10. Explicit non-goals

- Twin / missions / recommendations / student runtime
- Founder approval UI or publish workflow
- CIP stage contract changes
- LLM / OCR extraction
- Wiring CKG into production `CurriculumService` traversal
