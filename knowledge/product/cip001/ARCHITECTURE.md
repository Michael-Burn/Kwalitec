# CIP-001 Architecture — Curriculum Intelligence Pipeline

Companion to `COMPLETION_REPORT.md`. CS-DOC-001 upload remains the ingress;
this document describes the intelligence pipeline that consumes stored PDFs.

## Long-term vision

```
Founder
  → Upload Official Curriculum Documents (CS-DOC-001)
  → Curriculum Intelligence Pipeline (CIP-001)
  → Structured Curriculum Knowledge
  → Knowledge Graph
  → Student Digital Twin (future)
  → Mission Engine / Revision Planner / Adaptive Learning (future)
```

PDFs are inputs. Knowledge is the output. Validation & provenance are CIP-002.
Evidence retrieval (embeddings + graph + trust signals) is CIP-003.

## Bounded contexts

| Context | Role |
|---|---|
| `curriculum_documents` | Document kinds + processing stage vocabulary |
| `curriculum_intelligence` | CIP domain contracts + state machine |
| `curriculum_ingestion` | Existing abstract entry ingestion (unchanged) |
| `curriculum_studio` | Founder workspace + upload orchestration |

CIP does **not** replace the Curriculum Engine JSON (V1/V2). It produces a
parallel Founder knowledge store that can later feed publish / Twin paths.

## Stage contracts

Every stage has an explicit input/output:

| Stage | Input | Output |
|---|---|---|
| Verify | storage_key | Valid PDF bytes in memory |
| Extract | PDF bytes | `ExtractedDocument` (pages/blocks/metadata) |
| Normalize | ExtractedDocument | Cleaned ExtractedDocument |
| Parse | ExtractedDocument | `StructuralDocument` tree |
| Map | StructuralDocument | `CurriculumMap` entities |
| Graph | CurriculumMap | `KnowledgeGraph` relations |
| Ready | Graph id | Embedding extension hook |

## Replaceability

- `PdfExtractionPort` — swap pypdf for pdfminer / commercial extractors
- `DocumentProcessingPort` — sync adapter today; async worker tomorrow
- `EmbeddingExtensionPort` — CIP-003 vector pipeline
- Heuristic parser/mapper — later rule packs without touching persistence

## State machine

Lawful transitions live in
`app/domain/curriculum_intelligence/pipeline_stage.py`.
Failed jobs retry to QUEUED or resume from checkpoint; cancel is terminal
until retry.

## Persistence rules

1. Never store PDF bytes in SQL
2. Never write extraction rows into student Topic/Mission tables
3. Prefer normalised columns over JSON blobs for entities/relations
4. Diagnostics/metadata may use JSON text columns
5. Idempotent replace of artefacts by extraction_id / parse_id / map_id / graph_id

## Founder operating surface

Workspace Content Sources panel shows CIP milestones and per-document job
events (status, duration, errors, retry/cancel). Opaque `ref://` and storage
keys remain hidden.
