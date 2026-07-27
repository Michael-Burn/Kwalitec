# CIP-002 Architecture — Validation & Provenance

Companion to `COMPLETION_REPORT.md`. Extends CIP-001 without modifying
CS-DOC-001 upload or CIP-001 pipeline stage contracts.

Embeddings / retrieval are **CIP-003** (not this milestone).

## Long-term principle

Every educational entity must answer:

- Where did I come from?
- Why was I created?
- Which document / pages / paragraphs support me?
- Which parser and pipeline job created me?
- How confident is the mapping?
- Has a Founder verified me?
- Which curriculum version am I derived from?

Nothing should exist without evidence.

## Evidence chain

```
Document
  → Extraction
  → Parser
  → Curriculum Mapping
  → Knowledge Graph
```

Each hop is persisted as immutable provenance (+ confidence factors).
Founder review decisions append review and audit records; they never
overwrite provenance.

## Bounded extension

| Layer | CIP-002 addition |
|---|---|
| Domain | `provenance`, `confidence`, `review`, `audit`, `validation_report`, `quality_metrics` |
| Application | Provenance / Confidence / Review / Validation / Audit / Metrics services + `ValidationProvenanceBridge` |
| Models | Normalised CIP-002 tables (Alembic `202607270006`) |
| Presentation | Curriculum Studio intelligence tabs + REST endpoints |

CIP-001 stages (`verify → extract → normalize → parse → map → graph → ready`)
are unchanged. The bridge runs **after** parse / map / graph / ready as a
side-effect inside `PipelineCoordinator`.

## Confidence model

`ConfidenceScoringService` produces:

- Score (0.0–1.0)
- Band (high / medium / low / very_low)
- Reason (Founder-readable)
- Factors (named contributions)

Low-confidence entities remain usable and appear in the Review Queue.

## Validation model

`GraphValidationService` checks:

- Orphan concepts
- Circular prerequisite chains
- Duplicate concepts
- Missing learning objectives
- Broken document references
- Invalid graph edges
- Version inconsistencies

Reports are append-only snapshots (history preserved across retries).

## Founder review

Approve / Reject / Remap create durable `cip_review_records` and audit
events. Provenance rows are never mutated.

## Founder surface

Curriculum Studio workspace → **Curriculum Intelligence** panel tabs:

Overview · Documents · Pipeline · Knowledge Graph · Validation ·
Review Queue · Metrics · Entity Details

## REST (Founder-auth)

Under `/console/studio/workspaces/<id>/intelligence/`:

| Endpoint | Purpose |
|---|---|
| `GET overview` | Aggregate counts + metrics |
| `GET validation` | Latest validation reports |
| `GET review-queue` | Low-confidence / failing entities |
| `POST entities/<id>/approve` | Approve |
| `POST entities/<id>/reject` | Reject |
| `POST entities/<id>/remap` | Remap |
| `GET entities/<id>` | Entity details |
| `GET entities/<id>/provenance` | Provenance chain |
| `GET audit` | Audit history |
| `GET metrics` | Pipeline quality metrics |
| `GET knowledge-graph` | Educational nodes/edges |

Responses expose educational concepts only (no storage keys).

## Sequence — map → evidence

```
PipelineCoordinator._map
  → CurriculumMappingService.map (CIP-001)
  → CipPersistenceService.replace_curriculum_map
  → ValidationProvenanceBridge.after_map
       → ProvenanceService.record_entity (each entity)
       → ConfidenceScoringService.score_entity
       → AuditService.ENTITY_CREATED
```

## Sequence — graph → validation

```
PipelineCoordinator._build_graph
  → KnowledgeGraphBuilder.build (CIP-001)
  → CipPersistenceService.replace_knowledge_graph
  → ValidationProvenanceBridge.after_graph
       → relation provenance + confidence
       → GraphValidationService.validate_document
       → PipelineMetricsService.record_for_job
       → Audit GRAPH_VALIDATED / GRAPH_REBUILT / METRICS_RECORDED
```

## Sequence — Founder approve

```
Founder → POST …/approve
  → FounderReviewService.approve
       → append CipReviewRecord
       → Audit ENTITY_APPROVED + ENTITY_REVIEWED
       → provenance unchanged
```
