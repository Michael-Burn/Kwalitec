# CIP-003 Architecture — Evidence Retrieval Platform

Companion to `COMPLETION_REPORT.md`. Extends CIP-001/CIP-002 without redesigning
pipeline stages. Embeddings are **one** retrieval strategy inside a canonical
evidence layer.

## Long-term principle

Every future AI capability must consume curriculum evidence exclusively through
`CurriculumRetrievalService`. No component may query a vector database directly.

```
Founder / Twin / Tutor / Mission / Revision / Analytics
                    │
                    ▼
        CurriculumRetrievalService  ← only public interface
                    │
     ┌──────────────┼──────────────────────────┐
     ▼              ▼                          ▼
 Knowledge     Provenance +              VectorStorePort
 Graph         Confidence +              (adapter-owned)
               Metadata + Policies
```

## Retrieval pipeline

```
Query
  → Intent Detection (basic keywords, no LLM)
  → Knowledge Graph Expansion
  → Metadata Filtering
  → Vector Search (via VectorStorePort)
  → Evidence Ranking
  → Confidence Weighting
  → Provenance Weighting
  → Structured Educational Evidence (RetrievalResult)
```

Never returns raw vector hits.

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/curriculum_retrieval/` |
| Application | `app/application/curriculum_retrieval/` |
| Ports | `VectorStorePort`, `EmbeddingModelPort` |
| Infrastructure | `app/infrastructure/adapters/curriculum_retrieval/` |
| Persistence | `cip_embedding_records`, `cip_local_vector_entries`, `cip_retrieval_logs` |

CIP-001 stages remain `verify → extract → normalize → parse → map → graph → ready`.
At `ready`, `RetrievalEmbeddingExtension` indexes embeddable entities.

## What is embedded

Educational entities only — not PDFs, pages, or arbitrary chunks:

- Learning Objectives
- Concepts (definitional body)
- Formulae
- Worked Examples
- Practice Questions
- Topics / Subtopics

Each embedding metadata row references `entity_id` + optional `provenance_id`.

## Vector abstraction

```
Application ──VectorStorePort──▶ LocalVectorStoreAdapter (dev)
                              └▶ future: pgvector / external
```

Phase-1 model: deterministic `HashingEmbeddingModel` (`kwalitec.hash_v1`).
Replaceable without domain changes.

## Ranking algorithm (deterministic)

```
rank =
  w_sem  * semantic_similarity
+ w_g    * 1/(1+graph_distance)
+ w_c    * confidence
+ w_v    * founder_verified
+ w_ver  * document_version_score
+ w_f    * entity_freshness
+ w_r    * relationship_strength (+ intent kind boost)
+ w_e    * evidence_count_norm
```

Weights come from `RetrievalProfile` (Tutor, Mission Engine, Revision Planner,
Knowledge Search, Analytics, Founder Explorer). Profiles change weights only.

## Retrieval result

`RetrievalResult` / `RankedEvidence` expose educational structure:

Concept · Learning Objective · Definition · Formulae · Examples ·
Practice Questions · Prerequisites · Related Concepts · Evidence ·
Confidence · Provenance · Rank Score (+ ranking breakdown)

## Founder surface

Curriculum Studio → **Evidence Explorer** tab:

- Concept search
- Embedding status
- Ranking inspection
- Provenance on results
- Graph neighbours

## REST (Founder-auth)

Under `/console/studio/workspaces/<id>/intelligence/`:

| Endpoint | Purpose |
|---|---|
| `GET evidence/search` | Concept / evidence search |
| `GET evidence/retrieve` | Full retrieval with filters |
| `GET entities/<id>/neighbours` | Graph neighbours |
| `GET entities/<id>/related` | Related concepts |
| `GET embeddings/status` | Index status |
| `GET retrieval/diagnostics` | Ranking diagnostics |

## Sequence — ready → index

```
PipelineCoordinator._ready
  → ValidationProvenanceBridge.after_ready (CIP-002)
  → RetrievalEmbeddingExtension.on_ready_for_embeddings
       → VectorIndexService.rebuild_document
            → EmbeddingGenerationService.generate_for_entity
            → VectorStorePort.upsert
```

## Sequence — retrieve

```
Consumer → CurriculumRetrievalService.retrieve
  → detect_intent
  → VectorIndexService.search (entity ids + similarity)
  → KnowledgeGraphTraversalService.expand
  → metadata filter (workspace / kind / verified / confidence)
  → EvidenceRankingService.rank (profile weights)
  → assemble RetrievalResult + CipRetrievalLog
```

## SDT-001 guidance

Student Digital Twin must:

1. Call `CurriculumRetrievalService` only (never VectorStorePort).
2. Prefer `RetrievalProfile.TUTOR` / mission-specific profiles.
3. Gate student-facing claims on `verified` + confidence bands where required.
4. Surface ranking breakdown factors in explainability contracts (K8).
5. Treat retrieval as evidence input — Twin reasoning remains separate.
