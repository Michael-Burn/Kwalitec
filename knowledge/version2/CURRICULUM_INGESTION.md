# Curriculum Ingestion

**Document ID:** V2-012-CURRICULUM-INGESTION  
**Milestone:** V2-012 — Curriculum Ingestion Engine  
**Status:** Authoritative domain + application specification  
**Nature:** Framework-independent deterministic curriculum document ingestion  

**Packages:**
- `app/domain/curriculum_ingestion/`
- `app/application/curriculum_ingestion/`

**Related:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md) · [`CURRICULUM_MANAGEMENT.md`](CURRICULUM_MANAGEMENT.md) · [`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md) · [`CURRICULUM_GRAPH.md`](CURRICULUM_GRAPH.md)

---

## 1. Purpose

Curriculum Ingestion transforms **abstract curriculum document sources** into **normalised educational structures**.

It performs:

- Classification
- Extraction
- Normalisation
- Validation
- Preview / package mapping

It does **not**:

- Teach
- Generate learning activities
- Generate learning sessions
- Generate missions
- Perform AI / LLM reasoning
- Persist data
- Depend on Flask or upload endpoints
- Modify Education Platform or Curriculum Management

```text
Abstract Document Sources
          │
          ▼
   Curriculum Ingestion Engine
          │
          ▼
Normalised Topics / Objectives / Sections / Prerequisites / Metadata
          │
          ▼
Curriculum Package Preview (handoff shape only)
```

Official traversable syllabus graphs remain owned by the Curriculum Graph. Publication lifecycle remains owned by Curriculum Management. This engine produces **structural candidates and validation reports** for downstream consumers.

---

## 2. Pipeline

```text
Document
   ↓
Classification
   ↓
Extraction
   ↓
Normalization
   ↓
Validation
   ↓
Preview
   ↓
Curriculum Package
```

### Lifecycle states

| State | Meaning |
|-------|---------|
| `received` | Job created with abstract documents |
| `classified` | Document kinds resolved |
| `extracted` | Raw sections / topics / objectives captured |
| `normalized` | Canonical ids, numbers, and hierarchy |
| `validated` | Immutable validation report attached |
| `preview_ready` | Package preview may be projected |
| `completed` | Successful terminal state |
| `failed` | Terminal failure (blocking validation or pipeline error) |

---

## 3. Supported document types

Initially supported **references / abstract sources**:

| Kind | Role |
|------|------|
| `cmp` | Core maths / subject pack structural source |
| `syllabus` | Primary syllabus / specification structure |
| `learning_objectives` | Explicit learning objective lists |
| `formula_sheet` | Formula entries (notes only; no teaching) |
| `supporting_document` | Ancillary notes / appendix structure |
| `unknown` | Unclassified; warned during validation |

Documents are **abstract**: typed `DocumentEntry` rows with optional numbers, parent refs, and attributes. The engine never stores PDF bytes and rejects data-URI / embedded `%PDF` references.

---

## 4. Normalisation strategy

1. **Stable identities** — slugify ids with typed prefixes (`section-…`, `topic-…`, `objective-…`).
2. **Whitespace collapse** — titles and objective text are whitespace-normalised.
3. **Numbering** — prefer explicit dotted numbers; otherwise synthesise from document order.
4. **Default section** — topics without a section land under `section-default` / “General”.
5. **Prerequisite edges** — collected from topic attributes and prerequisite entries; canonicalised to topic ids.
6. **Metadata merge** — first-wins by lowercased key; `subject_code` expected for readiness warnings.
7. **Deduplication** — first occurrence of a canonical id wins; duplicates surface in validation.

Normalisation is pure and deterministic: identical inputs always yield identical outputs.

---

## 5. Validation

The validation policy detects:

| Code | Intent |
|------|--------|
| `missing_objectives` | Topic without learning objectives |
| `duplicate_topic` | Duplicate topic id or title |
| `unknown_section` | Topic references a missing section |
| `malformed_hierarchy` | Self-parent sections / self-prerequisites |
| `inconsistent_numbering` | Non-increasing dotted numbers |
| `missing_metadata` | Required keys (e.g. `subject_code`) absent |
| `empty_document` | No structural entries |
| `unknown_document_kind` | Classification fell back to unknown |
| `duplicate_section` / `duplicate_objective` | Identity collisions |
| `orphan_objective` | Objective topic ref unresolved |
| `dangling_prerequisite` | Prerequisite edge points nowhere |

Reports are **immutable**. Re-validation produces a new report. Blocking findings prevent `completed`.

---

## 6. Error handling

- Domain constructors raise `ValueError` on invariant violations.
- Application exceptions inherit `CurriculumIngestionError`.
- `ValidationFailed` is raised by the engine when `require_pass=True` and the report blocks.
- Illegal lifecycle transitions raise `ValueError` / `IllegalState`.
- Pipeline failures move the job to `failed` with a reason; no partial persistence is attempted (engine is non-persisting).

---

## 7. Extension strategy

To extend without breaking determinism:

1. **New document kind** — add `DocumentKind`, classifier hints, and `ExtractionPolicy` allow-lists.
2. **New entry type** — extend `DocumentEntryType` and teach the extractor a pure mapping rule.
3. **New validation rule** — add an `IngestionIssueCode` and a check in `ValidationPolicy.collect_issues`.
4. **Downstream handoff** — consume `CurriculumPackagePreview` / normalised DTOs from Curriculum Management or Curriculum Graph adapters (out of scope here).

Do **not** introduce probabilistic models, prompt calls, or Flask upload routes into this package.

---

## 8. Architecture packages

### Domain

```text
app/domain/curriculum_ingestion/
    ingestion_job.py
    ingestion_state.py
    curriculum_document.py
    extracted_topic.py
    extracted_objective.py
    extracted_section.py
    extraction_result.py
    normalization_result.py
    ingestion_report.py
```

### Application

```text
app/application/curriculum_ingestion/
    ingestion_engine.py
    document_classifier.py
    extraction_service.py
    normalization_service.py
    validation_service.py
    mapping_service.py
    preview_service.py
    exceptions.py
    dto/
    policies/
```

### Principles

1. **Deterministic cores** — same documents → same structures and reports.
2. **Immutable outputs** — frozen dataclasses / DTOs throughout.
3. **Framework independence** — no Flask, SQLAlchemy, UI, or persistence.
4. **Structural only** — never invents teaching content, sessions, activities, or missions.
5. **Isolation** — does not import or modify Education Platform / Curriculum Management.

---

## 9. Exit criteria

- Deterministic ingestion pipeline
- Normalised curriculum structures (sections, topics, objectives, prerequisites, metadata)
- Validation reports with the required issue classes
- Immutable outputs
- Framework-independent package with dedicated tests
