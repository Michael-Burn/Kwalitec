# CIP-001 — Curriculum Intelligence Pipeline Foundation

## Summary

CIP-001 extends the stable CS-DOC-001 document upload path into a
deterministic Curriculum Intelligence Pipeline that transforms uploaded PDFs
into structured educational knowledge — stopping at **Ready for Embeddings**.

Founders upload Official Curriculum PDFs as before. After store/enqueue, the
pipeline verifies the blob, extracts pages/blocks (pypdf, no OCR/LLM),
normalises text, structurally parses educational patterns, maps curriculum
entities with provenance and confidence, builds a knowledge graph, and records
per-stage jobs/events for Founder inspection, retry, resume, and cancel.

Embeddings, vector search, LLMs, missions, and Digital Twin reasoning remain
out of scope; `EmbeddingExtensionPort` is the CIP-002 hook.

## Architecture overview

```
Founder UI (CS-DOC-001 cards + CIP status panel)
  → DocumentUploadService (unchanged contract)
       → DocumentStoragePort
       → DocumentProcessingPort
            → CurriculumIntelligenceProcessingAdapter
                 → ProcessingJobService
                 → PipelineCoordinator
                      → DocumentExtractionService → PdfExtractionPort (pypdf)
                      → DocumentNormalizationService
                      → StructuralParserService
                      → CurriculumMappingService
                      → KnowledgeGraphBuilder
                      → CipPersistenceService (normalised tables)
                      → EmbeddingExtensionPort (null stub)
```

Clean Architecture / DDD boundaries:

| Layer | Responsibility |
|---|---|
| Domain `curriculum_intelligence` | Stages, extraction/parse/map/graph contracts |
| Application | Single-responsibility services + ports |
| Infrastructure | pypdf extractor, CIP processing adapter |
| Presentation | Thin Founder routes + UI extensions |
| Models | Normalised CIP tables (no PDF bytes) |

OCR/AI never write directly into business entities. Extraction artefacts are
stored separately from Subject/Topic/Mission runtime tables.

## Pipeline diagram

```
Document Uploaded (CS-DOC-001)
        ↓
     Stored
        ↓
     Queued  ←── retry / resume re-entry
        ↓
    Verified
        ↓
    Extracted
        ↓
   Normalized
        ↓
     Parsed
        ↓
     Mapped
        ↓
  Graph Built
        ↓
Ready for Embeddings ──→ (CIP-002)
        ↓
     Failed / Cancelled
```

## Database schema

Alembic `202607270005` adds:

| Table | Purpose |
|---|---|
| `cip_processing_jobs` | Durable job + status/checkpoint/attempts |
| `cip_processing_events` | Append-only stage timings/diagnostics/errors |
| `cip_extracted_documents` | Extraction root (separate from curriculum entities) |
| `cip_extracted_pages` | Page text + dimensions |
| `cip_extracted_blocks` | Paragraph/heading/table/image blocks |
| `cip_structural_nodes` | Hierarchical educational parse tree |
| `cip_curriculum_entities` | Mapped Subject→…→PracticeQuestion nodes |
| `cip_knowledge_relations` | Directed graph edges |

PDF bytes remain in DocumentStorage (`storage_key` only).

## Service architecture

| Service | SRP |
|---|---|
| `DocumentExtractionService` | PDF → ExtractedDocument via port |
| `DocumentNormalizationService` | Deterministic text cleanup |
| `StructuralParserService` | Educational hierarchy heuristics |
| `CurriculumMappingService` | Structure → curriculum entities + review flags |
| `KnowledgeGraphBuilder` | Entities → relation graph |
| `ProcessingJobService` | Jobs, events, retry/resume/cancel |
| `PipelineCoordinator` | Stage orchestration |
| `CipPersistenceService` | Normalised table writes |

## Sequence diagrams

### Upload → Ready

```
Founder → Upload route → DocumentUploadService
  → storage.put
  → processing.enqueue
       → create QUEUED job
       → (CIP_AUTO_RUN) PipelineCoordinator.run_job
            → verify → extract → normalize → parse → map → graph → ready
            → persist artefacts + events
            → EmbeddingExtensionPort.on_ready_for_embeddings (no-op)
  → return Founder-safe metadata + pipeline_jobs
```

### Retry after failure

```
Founder → POST …/pipeline/retry
  → ProcessingJobService.prepare_retry
  → PipelineCoordinator.run_job (from checkpoint / scratch)
  → status JSON with events + durations
```

## Files created

- `app/domain/curriculum_intelligence/` (stages, extraction, structure, entities, graph)
- `app/application/curriculum_intelligence/` (services, ports, persistence, DTOs)
- `app/infrastructure/adapters/curriculum_intelligence/`
- `app/models/curriculum_intelligence.py`
- `migrations/versions/202607270005_cip001_curriculum_intelligence.py`
- `tests/application/curriculum_intelligence/test_pipeline.py`
- `knowledge/product/cip001/COMPLETION_REPORT.md`
- `knowledge/product/cip001/ARCHITECTURE.md`

## Files modified

- `app/domain/curriculum_documents/processing_stage.py` (CIP stages + labels)
- `app/presentation/curriculum_studio/factory.py` (CIP processing adapter)
- `app/presentation/curriculum_studio/routes.py` (pipeline inspect/retry/cancel)
- `app/application/curriculum_studio/document_upload_service.py` (status jobs)
- `app/application/curriculum_studio/dto/document_metadata.py`
- `app/templates/curriculum_studio/workspace.html`
- `app/static/js/document_upload.js`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/models/__init__.py`, `app/__init__.py`
- `app/config.py`, `.env.example`, `requirements.txt` (`pypdf`)
- `ARCHITECTURE.md`, `PROJECT_CONTEXT.md`

## Tests added

`tests/application/curriculum_intelligence/test_pipeline.py` covers:

- lawful pipeline transitions / failure / retry aliases
- pypdf extraction + non-PDF rejection
- normalisation idempotency
- structural hierarchy recognition
- curriculum mapping + uncertain flags
- knowledge graph relation kinds
- full upload → ready_for_embeddings persistence
- idempotent job creation after terminal
- failure recovery retry
- cancel
- multi-version replace
- status `pipeline_jobs` projection
- large (40-page) documents

## Tests executed

```
python3 -m pytest tests/application/curriculum_intelligence/test_pipeline.py \
  tests/application/curriculum_studio/test_document_upload.py -q
# 27 passed

python3 -m ruff check app/domain/curriculum_intelligence \
  app/application/curriculum_intelligence \
  app/infrastructure/adapters/curriculum_intelligence \
  app/models/curriculum_intelligence.py \
  app/domain/curriculum_documents/processing_stage.py \
  app/presentation/curriculum_studio/factory.py \
  app/presentation/curriculum_studio/routes.py \
  app/application/curriculum_studio/document_upload_service.py \
  app/application/curriculum_studio/dto/document_metadata.py \
  tests/application/curriculum_intelligence
# All checks passed
```

## Migration impact

Requires `flask db upgrade` to revision `202607270005`.
Fresh test DBs create CIP tables via `create_all`.
No changes to student-facing curriculum V1/V2 JSON engine tables.

## Architecture compliance

- Layering preserved: thin blueprints, application orchestration, ports for I/O.
- CS-DOC-001 upload not redesigned — processing port swapped to CIP adapter.
- Curriculum V1/V2 engine untouched; CIP knowledge is additive Founder authoring
  infrastructure ahead of Student Digital Twin consumption.
- Deterministic cores only — no LLM/OCR in the pipeline.

## Processing flow (Founder-visible)

1. Upload PDF → Stored → Queued (Processing)
2. Verified → Extracted → Parsed → Mapped → Knowledge Graph Built → Ready
3. Each stage records started/finished/duration/diagnostics/errors
4. Failed jobs expose Retry; in-flight jobs expose Cancel
5. Status API includes `pipeline_jobs` for inspection

## Technical debt

- Default `CIP_AUTO_RUN=true` runs the pipeline synchronously in-request;
  long PDFs may need async workers (`CIP_AUTO_RUN=false` + worker consumer).
- Structural parser/mapper heuristics are deterministic but incomplete for
  complex scanned/layout-heavy CMPs — uncertain nodes flagged `needs_review`.
- Sequential `depends_on`/`requires` edges are inferred from sibling order and
  always marked for review.
- Fixture-aware text seeding is test-only; production relies on pypdf text layer.
- CIP entity ids are not yet published into `PublishedCurriculumPackage` /
  student runtime — intentional until a later publish bridge.

## Known limitations

- No OCR for image-only PDFs
- No embeddings / vector DB / semantic search
- No LLM-assisted mapping
- No mission / Digital Twin consumption of the graph yet
- Contradicts / supports / extends coverage is partial (deterministic subset)

## Recommendations for CIP-002 (Embeddings & Retrieval)

1. Implement `EmbeddingExtensionPort` to chunk graph entities + source blocks
2. Persist embedding jobs as a new stage after `ready_for_embeddings`
3. Choose a vector store adapter behind a port (pgvector / external)
4. Keep retrieval out of recommendation math until explainability contracts exist
5. Index provenance (document_id, pages, entity_id) on every vector
6. Add Founder “Embedding status” strip without changing upload cards
7. Never let embedding models mutate curriculum entities — write vectors only

## Student Impact Assessment

N/A for CIP-001 (Founder authoring / knowledge-foundation infrastructure).
Enables future authoritative curriculum knowledge for the Student Digital Twin
without changing student-facing recommendations in this milestone.

## Estimated KSI contribution

ΔKSI ≈ 0 (infra/authoring). Future CIP-002+ consumption paths target K1/K2/K8
once student-facing intelligence reads the graph.

## Evidence collected

- `tests/application/curriculum_intelligence/test_pipeline.py`
- Existing CS-DOC-001 upload tests remain green with queue-only adapter
- Migration `202607270005`

## Lessons learned for student value

Authoritative PDFs must become structured knowledge before Twin/Mission systems
can explain *why* a topic exists. Separating extraction from curriculum entities
keeps Founder iteration safe and avoids coupling student runtime to PDF noise.

## Explainability Review

N/A — no student-facing intelligence changed.

## Recommendation Quality Review

N/A — no recommendation ranking/selection changed.

## Version 1 readiness residual

N/A — does not claim Version 1 production-ready progress beyond Founder
authoring infrastructure.
