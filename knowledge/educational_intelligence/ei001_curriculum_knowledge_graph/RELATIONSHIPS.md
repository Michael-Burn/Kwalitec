# EI-001 — Educational Graph Relationships

**Programme:** EI-001 — Curriculum Knowledge Graph Foundation  
**Companion:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`DOMAIN_MODEL.md`](DOMAIN_MODEL.md)  
**Enum:** `CkgRelationshipType` in `app/domain/curriculum_knowledge_graph/value_objects/relationship_type.py`

---

## 1. Relationship catalogue

| From | Type | To | Hard? | Notes |
|------|------|----|-------|-------|
| Subject | `contains` | Topic | No | Structural ownership |
| Topic | `contains` | Section | No | Structural ownership |
| Section | `contains` | Subsection | No | Structural ownership |
| Subsection | `contains` | LearningObjective | No | Structural ownership |
| Subsection | `contains` | Definition / Formula / WorkedExample / PracticeExercise / ReadingReference | No | Object ownership |
| LearningObjective | `references` | Definition | No | LO consumes definition |
| LearningObjective | `references` | Formula | No | LO consumes formula |
| LearningObjective | `references` | WorkedExample | No | LO consumes worked example |
| LearningObjective | `references` | PracticeExercise | No | LO consumes practice |
| LearningObjective | `references` | ReadingReference | No | LO points at CMP locator |
| LearningObjective | `references` | SyllabusOutcome | No | LO aligns to official outcome |
| LearningObjective | `requires` | LearningObjective | **Yes** | Hard prerequisite; must remain acyclic |
| Structural node | `cross_references` | Structural node | No | Soft advisory link |
| Definition | `defines` | LearningObjective / Subsection | No | Optional role refinement |
| WorkedExample | `exemplifies` | LearningObjective / Formula | No | Optional role refinement |
| PracticeExercise | `assesses` | LearningObjective | No | Optional role refinement |
| ReadingReference | `reads` | Subsection / LearningObjective | No | Optional role refinement |

“Hard?” means the edge participates in cycle detection and LO topological ordering.

---

## 2. Semantics

### `contains`

Parent structurally owns child. Direction: parent → child. Materialised both as ownership FKs and as graph edges when a full aggregate is built.

### `references`

Learning objective depends educationally on an object or syllabus outcome for study guidance. Stored in domain edges and/or `ckg_lo_links` for efficient LO-centric queries.

### `requires`

`A requires B` means **A depends on B** — B must precede A in lawful study order. Cycle introduction is rejected at write time.

### `cross_references`

Soft link between structural nodes (e.g. related subsections). Does not block sequencing.

### Role refinements (`defines`, `exemplifies`, `assesses`, `reads`)

Optional typed edges that refine *why* an object relates to a structural node. They do not replace `contains` / `references` as the primary educational links.

---

## 3. Persistence

| Store | Content |
|-------|---------|
| `ckg_edges` | All directed typed edges; unique `(from_stable_id, to_stable_id, relationship_type)` |
| `ckg_lo_links` | Denormalised LO→object reference rows (`target_kind`, `target_stable_id`, `relationship_type`) |

Indexes on `from_stable_id`, `to_stable_id`, and `relationship_type` support traversal without full table scans.

---

## 4. Invariants

1. No self-loops.  
2. Endpoints must exist in the in-memory graph aggregate before an edge is added.  
3. `requires` edges among learning objectives must remain a DAG.  
4. Duplicate `(from, to, type)` edges are rejected.  
5. Soft edges never contribute to hard-prerequisite cycle detection.
