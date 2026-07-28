# EI-001 — Curriculum Knowledge Graph Domain Model

**Programme:** EI-001 — Curriculum Knowledge Graph Foundation  
**Companion:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`RELATIONSHIPS.md`](RELATIONSHIPS.md)  
**Code:** `app/domain/curriculum_knowledge_graph/`

---

## 1. Entity catalogue

### Structural hierarchy

| Entity | Owner | Identifiers | Key fields |
|--------|-------|-------------|------------|
| **Subject** | Graph root | `stable_id` (e.g. `CS1`) | `code`, `title`, `provider`, `edition_label`, `sequence_index` |
| **Topic** | Subject | `stable_id` (`CS1.T04`) | `subject_id`, `code`, `title`, `display_order`, `difficulty`, `estimated_study_minutes` |
| **Section** | Topic | `stable_id` (`CS1.T04.S04.02`) | `topic_id`, `code`, `title`, `display_order`, difficulty, study time |
| **Subsection** | Section | `stable_id` (`…SS01`) | `section_id`, `code`, `title`, `display_order`, difficulty, study time |
| **LearningObjective** | Subsection | `stable_id` (`…LO03`) | `subsection_id`, `code`, `statement`, `cognitive_level`, `learning_type`, `display_order`, difficulty, study time |

### Educational objects

| Entity | Typical owner | Identifiers | Key fields |
|--------|---------------|-------------|------------|
| **Definition** | Subsection (or LO) | `…DEF01` | `owner_id`, `title`, `body`, `cmp_locator` |
| **Formula** | Subsection (or LO) | `…FOR01` | `owner_id`, `title`, `notation`, `latex` |
| **WorkedExample** | Subsection (or LO) | `…WE01` | `owner_id`, `title`, `summary` |
| **PracticeExercise** | Subsection (or LO) | `…PE01` | `owner_id`, `title`, `difficulty` |
| **ReadingReference** | Subject / Subsection / LO | `…RR01` or `CS1.RR01` | `owner_id`, `title`, `document_kind`, `locator` (**no PDF bytes**) |
| **SyllabusOutcome** | Subject / LO | `…SO01` or `CS1.SO01` | `owner_id`, `outcome_code`, `statement_ref` |

### Value objects

| Value object | Purpose |
|--------------|---------|
| `StableCurriculumId` | Parse / build / validate permanent ids |
| `DifficultyBand` | `foundational` → `intermediate` → `advanced` → `capstone` |
| `EstimatedStudyTime` | Non-negative minutes |
| `CkgNodeKind` | Node classification enum |
| `CkgRelationshipType` | Edge type enum |
| `CognitiveLevel` / `LearningType` | LO educational metadata (Bloom / learning type) |

### Aggregate

| Component | Role |
|-----------|------|
| `CurriculumKnowledgeGraph` | Subject-scoped mutable graph: nodes, edges, containment DFS, requires topo-sort |
| `CkgEdge` | Directed typed edge value object |

---

## 2. Ownership rules

1. Every non-root node’s `stable_id` must be a structural child of its declared owner id.  
2. Subject `stable_id` depth must be subject-only.  
3. Educational objects attach to subsection, learning objective, or (for `RR`/`SO` only) subject.  
4. Within a graph aggregate, all node ids share the subject code prefix.  
5. Duplicate `stable_id` registration is rejected.

---

## 3. Persistence mapping

| Domain | ORM table |
|--------|-----------|
| Edition metadata | `ckg_graph_editions` |
| Subject | `ckg_subjects` |
| Topic | `ckg_topics` |
| Section | `ckg_sections` |
| Subsection | `ckg_subsections` |
| LearningObjective | `ckg_learning_objectives` |
| Definition / Formula / WorkedExample / PracticeExercise / ReadingReference / SyllabusOutcome | matching `ckg_*` tables |
| LO → object references | `ckg_lo_links` |
| Typed edges | `ckg_edges` |
| Id continuity | `ckg_id_aliases` |

Containment FKs use parent `stable_id` strings for referential integrity and efficient traversal without integer remapping across editions.

---

## 4. Fields of educational significance

| Concern | Representation |
|---------|----------------|
| Estimated study time | `estimated_study_minutes` on structural nodes; `EstimatedStudyTime` VO in domain |
| Difficulty | `DifficultyBand` / string column on nodes and practice exercises |
| Prerequisites | `requires` edges between learning objectives |
| Cross references | `cross_references` edges between structural nodes |
| CMP reading | `ReadingReference.locator` + `document_kind` |
| Syllabus outcomes | `SyllabusOutcome.outcome_code` + optional `statement_ref` |
