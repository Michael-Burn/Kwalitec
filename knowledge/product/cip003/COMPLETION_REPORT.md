# CIP-003 — Evidence Retrieval Platform

## Summary

CIP-003 establishes Kwalitec’s canonical evidence retrieval layer.
`CurriculumRetrievalService` is the only public interface for curriculum
evidence. Embeddings are one strategy among knowledge graph, provenance,
confidence, metadata, and retrieval policies. No consumer queries the vector
store directly. CS-DOC-001, CIP-001 stages, and CIP-002 trust artefacts are
preserved and extended.

## Files Created

- `app/domain/curriculum_retrieval/__init__.py`
- `app/domain/curriculum_retrieval/intent.py`
- `app/domain/curriculum_retrieval/profile.py`
- `app/domain/curriculum_retrieval/query.py`
- `app/domain/curriculum_retrieval/result.py`
- `app/domain/curriculum_retrieval/ranking.py`
- `app/domain/curriculum_retrieval/embedding.py`
- `app/application/curriculum_retrieval/__init__.py`
- `app/application/curriculum_retrieval/ports/__init__.py`
- `app/application/curriculum_retrieval/ports/vector_store_port.py`
- `app/application/curriculum_retrieval/curriculum_retrieval_service.py`
- `app/application/curriculum_retrieval/embedding_generation_service.py`
- `app/application/curriculum_retrieval/evidence_ranking_service.py`
- `app/application/curriculum_retrieval/knowledge_graph_traversal_service.py`
- `app/application/curriculum_retrieval/retrieval_policy_service.py`
- `app/application/curriculum_retrieval/vector_index_service.py`
- `app/infrastructure/adapters/curriculum_retrieval/__init__.py`
- `app/infrastructure/adapters/curriculum_retrieval/hashing_embedding_model.py`
- `app/infrastructure/adapters/curriculum_retrieval/local_vector_store.py`
- `app/infrastructure/adapters/curriculum_retrieval/embedding_extension.py`
- `migrations/versions/202607270007_cip003_evidence_retrieval.py`
- `tests/application/curriculum_retrieval/__init__.py`
- `tests/application/curriculum_retrieval/test_evidence_retrieval.py`
- `knowledge/product/cip003/ARCHITECTURE.md`
- `knowledge/product/cip003/COMPLETION_REPORT.md`

## Files Modified

- `app/application/curriculum_intelligence/pipeline_coordinator.py` (CIP-003 embedding extension default)
- `app/application/curriculum_intelligence/ports/pdf_extraction_port.py` (extension docs)
- `app/models/curriculum_intelligence.py` (CIP-003 ORM tables)
- `app/models/__init__.py`
- `app/presentation/curriculum_studio/routes.py` (evidence APIs)
- `app/presentation/curriculum_studio/intelligence_serializers.py`
- `app/templates/curriculum_studio/workspace.html` (Evidence Explorer tab)
- `app/static/js/curriculum_intelligence.js`
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Retrieval architecture diagram

See `knowledge/product/cip003/ARCHITECTURE.md`.

## Vector abstraction

- Port: `VectorStorePort` + `EmbeddingModelPort`
- Dev adapter: `LocalVectorStoreAdapter` (`cip_local_vector_entries`)
- Phase-1 model: `HashingEmbeddingModel` (`kwalitec.hash_v1`, dim 64)
- Application never imports a concrete vector technology outside wiring

## Ranking algorithm

Deterministic weighted sum of: semantic similarity, graph proximity,
confidence, founder verification, document version, entity freshness,
relationship strength, evidence count. Profiles supply weights only.

## Retrieval flow

Query → intent → graph expansion → metadata filter → vector search →
ranking (confidence + provenance signals) → `RetrievalResult` + retrieval log.

## Database changes

Alembic `202607270007` adds:

| Table | Purpose |
|---|---|
| `cip_embedding_records` | Embedding metadata (entity, model, version, vector_id, status) |
| `cip_local_vector_entries` | Infrastructure-owned local vector payloads |
| `cip_retrieval_logs` | Append-only retrieval diagnostics |

## Tests Executed

```
python3 -m pytest tests/application/curriculum_retrieval/test_evidence_retrieval.py \
  tests/application/curriculum_intelligence/test_pipeline.py \
  tests/application/curriculum_intelligence/test_validation_provenance.py -q
# 39 passed

python3 -m ruff check app/domain/curriculum_retrieval \
  app/application/curriculum_retrieval \
  app/infrastructure/adapters/curriculum_retrieval \
  app/models/curriculum_intelligence.py \
  app/presentation/curriculum_studio/routes.py \
  app/presentation/curriculum_studio/intelligence_serializers.py \
  app/application/curriculum_intelligence/pipeline_coordinator.py \
  tests/application/curriculum_retrieval
# All checks passed
```

### Test coverage

- Embedding generation (deterministic hashing, skip non-embeddable)
- Graph traversal neighbours
- Ranking determinism + profile sensitivity
- Retrieval policies (weights / kind boost)
- Evidence ordering (confidence)
- Vector abstraction (LocalVectorStoreAdapter)
- Pipeline → index → retrieve regression
- Founder Evidence Explorer REST endpoints
- CIP-001 / CIP-002 regression suites

## Migration Impact

Requires `flask db upgrade` to revision `202607270007`.
No changes to student-facing curriculum V1/V2 JSON engine tables.
CIP-001 / CIP-002 tables untouched.

## Architecture Compliance

- Clean Architecture / DDD: domain contracts, application services, ports,
  infrastructure adapters.
- CS-DOC-001 upload unchanged.
- CIP-001 pipeline stages unchanged; ready-hook indexes entities.
- CIP-002 provenance/confidence consumed, not rewritten.
- Curriculum V1/V2 engine untouched.
- No LLM in retrieval path.

## Technical Debt

- Phase-1 hashing embeddings are not semantic-quality production embeddings;
  swap via `EmbeddingModelPort` when a model is chosen.
- Local vector store is O(n) brute-force cosine — fine for Founder corpora,
  not for multi-million vectors.
- Entity freshness uses `created_at` only (no document version calendar).
- Lexical fallback when the index is sparse may over-include title matches.
- Relationship embeddings (optional in brief) not generated as separate vectors.

## Known Limitations

- No LLM reasoning / tutor conversations / mission generation
- No Student Digital Twin consumption yet (SDT-001)
- No student-context retrieval signals (future)
- No pgvector / external vector DB adapter yet

## Recommendations for SDT-001

1. Twin reads evidence only through `CurriculumRetrievalService`.
2. Use profile-specific policies (`TUTOR`, `MISSION_ENGINE`, …).
3. Prefer Founder-verified + high-confidence evidence for student-facing claims.
4. Attach ranking breakdown + provenance ids to Twin explainability payloads (K8).
5. Do not introduce parallel vector queries in Twin or Mission services.
6. Keep Twin reasoning separate from retrieval — retrieval supplies evidence,
   Twin decides pedagogy.

## Student Impact Assessment

N/A for CIP-003 (Founder / platform infrastructure). Enables future Twin and
Tutor capabilities to ground answers in explainable curriculum evidence.

## Estimated KSI contribution

ΔKSI ≈ 0 (infra/authoring). Future SDT/Tutor paths target K1/K2/K8 once
student-facing intelligence consumes this layer.

## Evidence collected

- `tests/application/curriculum_retrieval/test_evidence_retrieval.py`
- CIP-001 / CIP-002 regression suites
- Migration `202607270007`
- Architecture: `knowledge/product/cip003/ARCHITECTURE.md`

## Lessons learned for student value

Semantic search alone is insufficient for educational trust. Combining graph
distance, confidence, Founder verification, and provenance into one retrieval
contract keeps future Twin explanations defensible.

## Explainability Review

N/A — no student-facing intelligence changed. Ranking breakdown is designed
to feed future K8 explainability contracts.

## Recommendation Quality Review

N/A — no student recommendation ranking/selection changed.

## Version 1 readiness residual

N/A — does not claim Version 1 production-ready progress beyond Founder
evidence-retrieval infrastructure.
