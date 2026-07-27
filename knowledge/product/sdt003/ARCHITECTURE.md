# SDT-003 Architecture — Learning Graph

Companion to `COMPLETION_REPORT.md`. Introduces the learner-specific Learning
Graph without redesigning CS-DOC-001, CIP-001 → CIP-003, SDT-001, or SDT-002.

## Long-term principle

Kwalitec now has three canonical educational models:

1. **Curriculum Intelligence** — WHAT should be learned
2. **Student Digital Twin** — WHO is learning (educational state)
3. **Learning Graph** — HOW that learner's knowledge is interconnected

Every future adaptive capability (Adaptive Mission Engine, Revision Planner,
Intelligent Tutor, Educational Analytics) must use the Learning Graph for
prerequisite reasoning, dependency analysis, and educational path generation
rather than treating curriculum concepts as isolated entities.

```
Curriculum evidence (CIP-003)
        │
        ▼
Learning Graph sync (nodes + prerequisite edges)
        │
        ▼
Educational Reasoning Engine (SDT-002)
        │   Rules traverse Learning Graph for prerequisites / recovery
        ▼
Student Digital Twin update (SDT-001)
        │
        ▼
Learning Graph mastery projection refresh
```

No LLM. No direct VectorStore access. Curriculum evidence enters exclusively
via `CurriculumRetrievalService`.

## Bounded context

| Layer | Location |
|---|---|
| Domain | `app/domain/learning_graph/` |
| Application | `app/application/learning_graph/` |
| Persistence | `app/models/learning_graph.py` |
| Founder diagnostics | `app/presentation/learning_graph/` (`/founder/learning-graph/*`) |

Aggregate root: `LearningGraph`. One graph per Student Digital Twin.

Owns: Nodes, Edges, Prerequisite Relationships, Mastery Links, Dependency
Chains (derived), Traversal Metadata (derived), Snapshots, Update History.

## Graph architecture

### Nodes

Each node represents one curriculum concept. Projected fields (mastery,
confidence, evidence count, trend, last interaction, prerequisite status) are
resolved from the Twin at sync time. Persistence stores structure +
`mastery_link_id` — Twin mastery rows remain the source of truth.

### Edges

Directed relationships:

| Type | Meaning |
|---|---|
| `prerequisite` | from requires to (to is foundation) |
| `depends_on` | educational dependency |
| `strengthens` | supporting reinforcement |
| `related_concept` | associative link from retrieval |
| `revision_dependency` | revision-order dependency |

Edges carry strength, confidence, provenance, and supporting curriculum
evidence ids.

### Node lifecycle

1. Twin observations / mastery introduce concept ids
2. Sync upserts nodes with MasteryLink → Twin mastery_id
3. Prerequisite status recomputed from dependency edges + projections
4. Stub nodes created for edge endpoints not yet observed

### Edge lifecycle

1. Curriculum evidence (retrieval) supplies prerequisites / related concepts
2. Sync upserts typed edges with evidence provenance
3. Prior edges retained when endpoints remain relevant
4. Traversal consumes edges deterministically (BFS, sorted adjacency)

## Traversal model

`LearningGraphTraversalService` (deterministic):

- Prerequisite traversal (upstream)
- Dependency discovery (downstream)
- Learning path generation (foundations → seed)
- Recovery path generation (weak foundations → seed)
- Impact analysis (downstream dependents)
- Connected concept discovery (undirected neighbourhood)

## Integration with Student Digital Twin

| Concern | Owner |
|---|---|
| Learner state (mastery, gaps, confidence) | SDT-001 Twin |
| Knowledge relationships | SDT-003 Learning Graph |
| Mastery link | Graph node → Twin mastery_id |
| Twin create | Also creates empty Learning Graph |

The Twin remains the sole learner-state source of truth. The Learning Graph
does **not** duplicate mastery inference tables.

## Integration with Educational Reasoning Engine

| Stage | Behaviour |
|---|---|
| Evidence retrieval | Unchanged (CIP-003) |
| Graph sync | Before rules: nodes from Twin, edges from evidence |
| `ReasoningContext.learning_graph` | Attached for rule consumption |
| Prerequisite Analysis | Prefers graph traversal; falls back to evidence |
| Recommendation | Prefers graph recovery path (graph-driven) |
| After Twin update | Refresh mastery projections on graph nodes |

Rules query the graph rather than hardcoding prerequisite adjacency.

## Founder diagnostics

| Endpoint | Purpose |
|---|---|
| `GET /founder/learning-graph/` | Index / list by student_id |
| `GET /founder/learning-graph/<student>` | Graphs for a student |
| `GET/POST /founder/learning-graph/traverse` | Traversal / recovery / impact |
| `GET/POST /founder/learning-graph/prerequisites` | Prerequisite + recovery |
| `GET/POST /founder/learning-graph/dependencies` | Downstream + impact |

Not student-facing.

## Persistence

Alembic `202607270010` adds:

| Table | Purpose |
|---|---|
| `learning_graphs` | Graph root (1:1 with Twin) |
| `learning_graph_nodes` | Concept nodes + mastery links + projections |
| `learning_graph_edges` | Directed relationships |
| `learning_graph_snapshots` | Append-only structural snapshots |
| `graph_update_history` | Append-only update audit |

## What SDT-003 does not do

- Tutoring or Adaptive Mission generation
- Student-facing UX
- Replacement of CIP, Curriculum Studio, Twin, or Reasoning Engine
- LLM / probabilistic inference
- Direct VectorStore or CIP Knowledge Graph access from this context
