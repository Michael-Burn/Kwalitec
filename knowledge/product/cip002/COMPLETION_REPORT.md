# CIP-002 — Curriculum Intelligence Validation & Provenance

## Summary

CIP-002 makes CIP-001 knowledge trustworthy, explainable, and auditable.
It adds immutable provenance, explainable confidence, graph validation,
Founder review, audit events, and pipeline quality metrics — without
embeddings, LLMs, or semantic search.

CS-DOC-001 upload and CIP-001 pipeline stages are unchanged. A
`ValidationProvenanceBridge` attaches evidence after parse / map / graph /
ready. Embeddings remain deferred to **CIP-003**.

## Files Created

- `app/domain/curriculum_intelligence/provenance.py`
- `app/domain/curriculum_intelligence/confidence.py`
- `app/domain/curriculum_intelligence/review.py`
- `app/domain/curriculum_intelligence/audit.py`
- `app/domain/curriculum_intelligence/validation_report.py`
- `app/domain/curriculum_intelligence/quality_metrics.py`
- `app/application/curriculum_intelligence/provenance_service.py`
- `app/application/curriculum_intelligence/confidence_scoring_service.py`
- `app/application/curriculum_intelligence/founder_review_service.py`
- `app/application/curriculum_intelligence/graph_validation_service.py`
- `app/application/curriculum_intelligence/audit_service.py`
- `app/application/curriculum_intelligence/pipeline_metrics_service.py`
- `app/application/curriculum_intelligence/validation_provenance_bridge.py`
- `app/presentation/curriculum_studio/intelligence_serializers.py`
- `app/static/js/curriculum_intelligence.js`
- `migrations/versions/202607270006_cip002_validation_provenance.py`
- `tests/application/curriculum_intelligence/test_validation_provenance.py`
- `knowledge/product/cip002/ARCHITECTURE.md`
- `knowledge/product/cip002/COMPLETION_REPORT.md`

## Files Modified

- `app/domain/curriculum_intelligence/__init__.py`
- `app/domain/curriculum_intelligence/knowledge_graph.py` (CIP-003 note)
- `app/application/curriculum_intelligence/__init__.py`
- `app/application/curriculum_intelligence/pipeline_coordinator.py` (bridge hooks)
- `app/application/curriculum_intelligence/ports/pdf_extraction_port.py` (CIP-003 note)
- `app/models/curriculum_intelligence.py` (CIP-002 ORM tables)
- `app/models/__init__.py`
- `app/presentation/curriculum_studio/routes.py` (intelligence REST)
- `app/templates/curriculum_studio/workspace.html` (intelligence tabs)
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Domain model

| Concept | Contract |
|---|---|
| Provenance | `ProvenanceRecord` + `SupportingEvidence` + chain stages |
| Confidence | `ConfidenceRecord` + `ConfidenceFactor` + band |
| Review | `ReviewRecord` / `ReviewStatus` / `VerificationStatus` |
| Validation | `ValidationReport` + `ValidationIssue` |
| Audit | `AuditEvent` + `AuditAction` |
| Metrics | `PipelineQualityMetrics` |

## Database schema

Alembic `202607270006` adds:

| Table | Purpose |
|---|---|
| `cip_provenance_records` | Immutable provenance |
| `cip_provenance_evidence` | Page/paragraph/block excerpts |
| `cip_confidence_records` | Explainable scores |
| `cip_confidence_factors` | Named score contributions |
| `cip_review_records` | Append-only Founder decisions |
| `cip_validation_reports` | Validation snapshots |
| `cip_validation_issues` | Individual findings |
| `cip_audit_events` | Append-only audit trail |
| `cip_quality_metrics` | Pipeline quality snapshots |

Relational columns preferred over JSON blobs (CSV only for compact id lists;
attributes JSON reserved for diagnostics).

## Provenance model

Each entity/relation records document, version, pages, paragraphs, block ids,
parser/mapper/graph builder versions, pipeline job, extraction/parse/map/graph
ids, chain stage, and supporting evidence. Navigable via
`ProvenanceService.chain_for_entity`.

## Confidence model

Deterministic factors (parser confidence, numbered heading, page anchor,
mapper review flag, …) plus Founder-readable reason. Threshold 0.6 flags
`needs_review` for the Review Queue.

## Validation architecture

`GraphValidationService` runs after graph build. Failures do not delete
entities; they produce reports and feed the Review Queue.

## Review workflow

Approve / Reject / Remap append `cip_review_records` and audit events.
Provenance and original confidence history remain intact.

## Audit model

Actions include entity created/reviewed/approved/rejected/remapped, graph
rebuilt/validated, pipeline completed, metrics recorded. Fields: timestamp,
actor, action, entity, pipeline job, document version, workspace.

## Sequence diagrams

See `knowledge/product/cip002/ARCHITECTURE.md`.

## Tests Executed

```
python3 -m pytest tests/application/curriculum_intelligence/test_validation_provenance.py \
  tests/application/curriculum_intelligence/test_pipeline.py -q
# 28 passed

python3 -m ruff check app/domain/curriculum_intelligence \
  app/application/curriculum_intelligence \
  app/models/curriculum_intelligence.py \
  app/presentation/curriculum_studio/routes.py \
  app/presentation/curriculum_studio/intelligence_serializers.py \
  tests/application/curriculum_intelligence
# All checks passed
```

### Test coverage

- Confidence calculation + factors
- Provenance generation + chain + immutability
- Review workflow (approve / reject / remap) without overwriting provenance
- Audit logging
- Validation rules (orphan, circular, duplicate, missing LO, broken refs,
  invalid edges, version inconsistency)
- Metrics snapshots
- Retry regenerates validation while retaining prior audit/report history
- Intelligence REST endpoints
- CIP-001 ready-stage regression

## Migration Impact

Requires `flask db upgrade` to revision `202607270006`.
No changes to student-facing curriculum V1/V2 JSON engine tables.
CIP-001 tables untouched.

## Architecture Compliance

- Layering preserved: thin blueprints, application services, domain contracts.
- CS-DOC-001 and CIP-001 stages unmodified; CIP-002 is additive.
- Curriculum V1/V2 engine untouched.
- Deterministic cores only — no LLM / embeddings / OCR.

## Technical Debt

- Relation provenance does not yet deep-link source pages for inferred
  `depends_on` edges (excerpt is relation metadata only).
- Confidence replace-on-rerun deletes prior confidence rows for a subject
  (audit trail retains history; confidence table is latest-snapshot oriented).
- Review Queue validation-error join is best-effort across latest issues and
  may include findings from superseded reports until a dedicated “open issue”
  index exists.
- Synchronous pipeline still runs CIP-002 work in-request (`CIP_AUTO_RUN`).

## Known Limitations

- No embeddings / vector DB / semantic search (CIP-003)
- No LLM-assisted remapping suggestions
- No Student Digital Twin consumption of verified entities yet
- Paragraph indices are approximate (block-order heuristics)

## Recommendations for CIP-003 (Curriculum Embedding Engine)

1. Implement `EmbeddingExtensionPort` to chunk **verified** (or
   high-confidence) entities + provenance-linked source blocks.
2. Persist embedding jobs as a new stage after `ready_for_embeddings`.
3. Choose a vector store adapter behind a port (pgvector / external).
4. Index provenance (`document_id`, pages, `entity_id`, `provenance_id`) on
   every vector so retrieval remains evidence-first.
5. Never let embedding models mutate curriculum entities — write vectors only.
6. Gate Twin/Mission retrieval on Founder verification status where required.
7. Keep retrieval out of recommendation math until explainability contracts
   exist for retrieved evidence.

## Student Impact Assessment

N/A for CIP-002 (Founder authoring / knowledge-trust infrastructure).
Enables future Twin consumption of evidence-backed curriculum facts without
changing student-facing recommendations in this milestone.

## Estimated KSI contribution

ΔKSI ≈ 0 (infra/authoring). Future CIP-003+ Twin paths target K1/K2/K8 once
student-facing intelligence reads verified graph entities.

## Evidence collected

- `tests/application/curriculum_intelligence/test_validation_provenance.py`
- CIP-001 regression suite remains green
- Migration `202607270006`

## Lessons learned for student value

Structured knowledge is not enough for Twin reasoning — confidence,
provenance, and Founder verification are the trust layer that keeps
student-facing explanations defensible.

## Explainability Review

N/A — no student-facing intelligence changed.

## Recommendation Quality Review

N/A — no recommendation ranking/selection changed.

## Version 1 readiness residual

N/A — does not claim Version 1 production-ready progress beyond Founder
knowledge-trust infrastructure.
