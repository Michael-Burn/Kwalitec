# SDT-003 — Learning Graph

## Summary

SDT-003 delivers Kwalitec’s Learning Graph: a learner-specific graph that models
relationships between curriculum concepts, prerequisite chains, and evolving
mastery projections. Every Twin now owns a Learning Graph. Educational Reasoning
(SDT-002) syncs the graph from Twin state + CIP-003 curriculum evidence, then
traverses it for prerequisite analysis and graph-driven recovery recommendations.
Student Digital Twin remains the canonical learner-state model; the graph stores
relationships and mastery links rather than duplicated mastery rows. No LLM
dependency was introduced. CS-DOC-001, CIP-001 → CIP-003, SDT-001, and SDT-002
remain intact.

## Files Created

- `app/domain/learning_graph/__init__.py`
- `app/domain/learning_graph/learning_graph.py`
- `app/domain/learning_graph/graph_node.py`
- `app/domain/learning_graph/graph_edge.py`
- `app/domain/learning_graph/prerequisite.py`
- `app/domain/learning_graph/dependency.py`
- `app/domain/learning_graph/mastery_link.py`
- `app/domain/learning_graph/relationship.py`
- `app/domain/learning_graph/graph_snapshot.py`
- `app/domain/learning_graph/graph_update.py`
- `app/domain/learning_graph/graph_traversal.py`
- `app/application/learning_graph/__init__.py`
- `app/application/learning_graph/learning_graph_service.py`
- `app/application/learning_graph/learning_graph_traversal_service.py`
- `app/application/learning_graph/graph_builder_service.py`
- `app/application/learning_graph/persistence.py`
- `app/models/learning_graph.py`
- `app/presentation/learning_graph/__init__.py`
- `app/presentation/learning_graph/routes.py`
- `migrations/versions/202607270010_sdt003_learning_graph.py`
- `tests/application/learning_graph/__init__.py`
- `tests/application/learning_graph/test_learning_graph.py`
- `knowledge/product/sdt003/ARCHITECTURE.md`
- `knowledge/product/sdt003/COMPLETION_REPORT.md`

## Files Modified

- `app/domain/educational_reasoning/reasoning_context.py` (optional `learning_graph`)
- `app/domain/educational_reasoning/gap_analysis.py` (graph-preferred prerequisites)
- `app/domain/educational_reasoning/recommendation_rule.py` (graph-driven recovery)
- `app/application/educational_reasoning/educational_reasoning_service.py` (sync graph before rules)
- `app/application/student_digital_twin/student_digital_twin_service.py` (create graph with Twin)
- `app/application/student_digital_twin/student_reasoning_service.py` (refresh projections)
- `app/models/__init__.py` (register Learning Graph ORM models)
- `app/__init__.py` (model import + `/founder/learning-graph` blueprint)
- `ARCHITECTURE.md`
- `PROJECT_CONTEXT.md`

## Tests Executed

```
python3 -m pytest tests/application/learning_graph/ \
  tests/application/educational_reasoning/ \
  tests/application/student_digital_twin/ -q
# 34 passed

python3 -m ruff check app/domain/learning_graph \
  app/application/learning_graph \
  app/presentation/learning_graph \
  app/models/learning_graph.py \
  app/domain/educational_reasoning \
  app/application/educational_reasoning \
  app/application/student_digital_twin \
  tests/application/learning_graph
```

## Migration Impact

Alembic revision `202607270010` (revises `202607270009`) adds:

| Table | Purpose |
|---|---|
| `learning_graphs` | Graph root (1:1 with Twin) |
| `learning_graph_nodes` | Concept nodes + mastery links + projections |
| `learning_graph_edges` | Directed relationships |
| `learning_graph_snapshots` | Append-only structural snapshots |
| `graph_update_history` | Append-only update audit |

Does not alter SDT-001 Twin inference tables or SDT-002 reasoning metadata tables.
Projected mastery columns on nodes are caches for traversal/diagnostics only.

## Architecture Compliance

- Layering preserved: domain → application → presentation; no HTTP in services.
- Curriculum evidence exclusively via `CurriculumRetrievalService` (no VectorStore /
  CIP Knowledge Graph / embeddings direct access from this context).
- Curriculum V1/V2 traversal/import paths untouched (N/A for this milestone).
- Twin remains sole learner-state SoT; Learning Graph owns relationships.
- Educational Reasoning remains deterministic and explainable; rules prefer graph
  traversal with evidence fallback for SDT-002 compatibility.
- No LLM introduced.

## Technical Debt

- Edge sync currently derives relationships from retrieval evidence bundles for
  candidate concepts; richer multi-hop CIP relation import (still via retrieval
  ports, never direct graph DB access from rules) may be needed for denser graphs.
- Node projected mastery is a denormalised cache — keep refresh paths in sync when
  Twin reasoning evolves.
- Founder `/founder/*` diagnostics coexist with Console redirect shim; static
  Learning Graph routes are registered before the `<student>` parameter route.

## Known Limitations

- No student-facing Learning Graph UX.
- No Adaptive Mission / tutoring generation.
- Recovery paths are structural (mastery-threshold BFS), not full study-plan
  scheduling.
- Related-concept and strengthens edges are seeded from retrieval when present;
  revision_dependency edges are modelled but not auto-populated in this milestone.
