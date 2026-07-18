# Curriculum Graph

**Document ID:** V2-004-CURRICULUM-GRAPH  
**Milestone:** V2-004 — Curriculum Graph Foundation  
**Status:** Implemented (domain layer only)  
**Nature:** Educational knowledge model — structure without proprietary content  

**Parent:** [`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md), [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)  
**Code:** `app/domain/curriculum/`

This document describes the Version 2 Curriculum Graph: the educational knowledge model that represents curriculum structure, topic relationships, prerequisites, revision associations, and pathways. It does **not** store copyrighted syllabus text, questions, or proprietary notes.

---

## 1. Educational philosophy

Kwalitec’s Curriculum Graph models **structure**, not content.

| Models | Does not model |
|--------|----------------|
| Programme identity (e.g. paper codes) | Official syllabus prose |
| Subject → Module → Topic hierarchy | Copyrighted study notes |
| Prerequisite and advisory edges | Exam questions / solutions |
| Revision clusters | Mastery / competence scores |
| Named learning pathways | Pass probability |

Deterministic graph algorithms answer sequencing questions. No AI and no opaque heuristics enter the graph core.

Educational law remains subordinate to the [Educational Constitution](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md). Topic Complete and mastery beliefs stay with Learning Journey / Twin domains — the graph only supplies **what can come next structurally**.

---

## 2. Graph model

```
Curriculum
    ↓
Subject
    ↓
Module
    ↓
Topic  ←── nodes of CurriculumGraph
    ↑
Dependencies / Prerequisites / RevisionLinks / LearningPaths
```

### Entities

| Entity | Role |
|--------|------|
| **Curriculum** | Educational programme aggregate (structure + relationships) |
| **Subject** | Ordered modules within a programme |
| **Module** | Ordered topics within a subject |
| **Topic** | Atomic educational concept (id, name, difficulty, effort, objective refs) |
| **LearningPath** | One valid ordered route through topic ids |
| **Prerequisite** | Hard required-knowledge link |
| **Dependency** | Directed relationship (`REQUIRES` / `RECOMMENDS` / `RELATED` / `OPTIONAL` / `REVISION`) |
| **RevisionLink** | Undirected joint-revision association (canonical pair) |
| **CurriculumVersion** | Edition / schema metadata |

### Value objects

| Value object | Values |
|--------------|--------|
| `TopicId` / `CurriculumId` | Canonical identities |
| `TopicDifficulty` | FOUNDATIONAL → INTERMEDIATE → ADVANCED → CAPSTONE |
| `DependencyType` | REQUIRES, RECOMMENDS, RELATED, OPTIONAL, REVISION |
| `TopicStatus` | LOCKED, AVAILABLE, ACTIVE, COMPLETED, ARCHIVED |

### Graph components

| Component | Role |
|-----------|------|
| `CurriculumGraph` | Mutable graph: add/remove/connect, queries, algorithms |
| `GraphNode` | Topic node |
| `GraphEdge` | Directed dependency edge |
| `GraphBuilder` | Build graph from `Curriculum` / topic collections |
| `GraphValidator` | Cycles, duplicates, disconnected nodes, invalid endpoints |

**REQUIRES semantics:** edge `source → target` means *source requires target* (target precedes source in study order).

---

## 3. Algorithms

All algorithms are deterministic (stable sorted neighbour order).

| Algorithm | Use |
|-----------|-----|
| Depth-first traversal (DFS) | Explore dependency chains |
| Breadth-first traversal (BFS) | Layered neighbourhood walks |
| Kahn topological sort | Lawful study order under REQUIRES |
| DFS colouring cycle detection | Reject cyclic hard-prerequisite graphs |
| Shortest prerequisite path (BFS) | Minimal REQUIRES path between topics |
| Connected components | Revision clusters over REVISION edges |

No scoring heuristics. Soft edges (`RECOMMENDS`, `RELATED`, `OPTIONAL`, `REVISION`) do not participate in topological ordering or cycle detection for hard prerequisites.

---

## 4. Traversal examples

Illustrative structural labels only (not syllabus content):

```
Probability ──REQUIRES──► Random Variables ──REQUIRES──► Expectation
```

- `find_prerequisites(Expectation)` → `{Random Variables}`
- `all_prerequisites(Expectation)` → `{Probability, Random Variables}`
- `topological_ordering()` → `Probability, Random Variables, Expectation, …`
- `dfs(Expectation)` along REQUIRES out → `Expectation → Random Variables → Probability`

Diamond:

```
        A
       / \
      B   C
       \ /
        D
```

Topological order always places `A` before `B`/`C` and both before `D`. Shortest path `D → A` has length 3 (`D-B-A` or `D-C-A`).

---

## 5. Dependency examples

| Type | Meaning | Blocks eligibility? |
|------|---------|---------------------|
| REQUIRES | Hard prerequisite | Yes |
| RECOMMENDS | Advisory prior study | No (boosts recommendations) |
| RELATED | Associative link | No |
| OPTIONAL | Nice-to-have prior | No |
| REVISION | Joint revision association | No |

`Prerequisite` entities are authoring-friendly aliases for REQUIRES; `GraphBuilder` merges them with `Dependency` edges without duplication.

---

## 6. Revision graph

```
Expectation ⇄ Variance     (RevisionLink → bidirectional REVISION edges)
Expectation ──RELATED──► MGF
```

`RevisionPathService`:

- `related_concepts` — direct REVISION (+ optional RELATED) neighbours
- `revision_clusters` — connected components over REVISION
- `recommended_review_sequence` — cluster members in topological / stable order, incomplete first when completion sets are supplied

---

## 7. Services

| Service | Examples |
|---------|----------|
| `CurriculumNavigationService` | next/previous topic, available topics, recommended topics, learning path, derived `TopicStatus` |
| `PrerequisiteService` | eligible / missing / blocked / transitive missing |
| `RevisionPathService` | related concepts, clusters, review sequence |

---

## 8. Integration diagrams

### Current (V2-004)

```
Curriculum entities
        ↓
   GraphBuilder
        ↓
  CurriculumGraph
        ↓
Navigation / Prerequisite / Revision services
```

Pure domain only. No Flask routes, ORM, persistence writes, or UI.

### Future — Learning Journey Engine

```
Learning Journey Engine
        ↓
Curriculum Navigation
        ↓
Curriculum Graph
        ↓
Topic
```

The Journey Engine must **not** embed graph algorithms. It asks navigation / prerequisite services for structural eligibility and sequencing, then applies journey state / completion policy in its own bounded context.

**V2-004 does not modify** `app/domain/learning_journey/` or `app/application/learning_journey/`.

### Future — Mission Engine

```
Mission Engine
    ↓ (needs “what is structurally next?”)
Curriculum Navigation + PrerequisiteService
    ↓
Curriculum Graph
```

Missions operationalise decisions; the graph remains the structural source of lawful topic order.

### Future — Student Digital Twin

```
Twin (beliefs / readiness)
    ↓ (learner state)
PrerequisiteService + TopicStatus derivation
    ↓
Curriculum Graph (structure only)
```

The Twin owns mastery / readiness beliefs. The graph never invents competence scores from edges alone.

---

## 9. Repository contract

`CurriculumRepository` is an abstract persistence port (get / list / save / delete). No implementation ships in V2-004.

---

## 10. Constraints (honoured)

- Do not modify Version 1 Curriculum Engine behaviour
- Do not modify Learning Journey domain or engine
- No persistence, Flask routes, ORM models, or UI
- No copyrighted educational text; no hardcoded IFoA syllabus content
- Deterministic algorithms only

---

## 11. Package map

```
app/domain/curriculum/
├── entities/
├── value_objects/
├── graph/
├── services/
└── interfaces/
```

Tests: `tests/domain/curriculum/` (~150 pure unit tests).
