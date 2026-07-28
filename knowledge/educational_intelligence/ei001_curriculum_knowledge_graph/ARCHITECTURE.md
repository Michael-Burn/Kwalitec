# EI-001 — Curriculum Knowledge Graph Architecture

**Programme:** EI-001 — Curriculum Knowledge Graph Foundation  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/curriculum_knowledge_graph/` · `app/models/curriculum_knowledge_graph.py`  
**Companions:** [`DOMAIN_MODEL.md`](DOMAIN_MODEL.md) · [`RELATIONSHIPS.md`](RELATIONSHIPS.md)

> **ID disambiguation:** Historical Engineering Improvements also used the code **EI-001** under `knowledge/release/EI-001/`. This Educational Intelligence programme is distinct and lives here.

---

## 1. Graph philosophy

Kwalitec’s Curriculum Knowledge Graph (CKG) is the **target Single Source of Educational Truth** for future Educational Intelligence programmes.

It models how an IFoA (or similar) subject is organised at subsection-level precision:

```
Subject → Topic → Section → Subsection → Learning Objective
```

plus educational objects (definitions, formulas, worked examples, practice exercises, CMP reading references, syllabus outcomes) and typed educational relationships (containment, references, hard prerequisites, cross-references).

| Models | Does not model |
|--------|----------------|
| Structural hierarchy and stable identities | Copyrighted CMP prose dumps |
| Difficulty bands and study-time estimates | Mastery / Twin beliefs |
| Prerequisite and cross-reference edges | Student progress or missions |
| Edition metadata and id aliases | PDF bytes or extraction jobs |

The graph is **deterministic**. Given the same nodes and edges, traversals and topological orders are reproducible. No AI or opaque scoring enters the CKG core.

Educational law remains subordinate to the [Educational Constitution](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md).

---

## 2. Modelling decisions

### Additive parallel SoT

CKG is **additive**. It does not replace:

| Existing system | Role retained |
|-----------------|---------------|
| Curriculum Engine V1/V2 (`app/curriculum/`, `curricula` / `sections` / `topics`) | Student runtime syllabus import & traversal |
| CIP tables (`cip_*`) | Document extraction / mapping pipeline |
| `app/domain/curriculum` (V2-004 Subject→Module→Topic) | Structural pathway graph (different hierarchy) |
| `domain.education.knowledge_graph` | Abstract concept dependency graph |
| SDT Learning Graph (`learning_graph_*`) | Per-student Twin-linked concept graph |

Student runtime continues on V1/V2 until a future cutover programme. CIP may later **publish into** CKG; that wiring is out of scope for EI-001.

### Hierarchy naming vs V2

| CKG term | Meaning | Closest V2 analogue |
|----------|---------|---------------------|
| Subject | Examinable paper (e.g. CS1) | Curriculum / exam_code |
| Topic | CMP topic | *(not V2 Section)* |
| Section | Section within a CMP topic | *(not V2 Section)* |
| Subsection | Finer CMP unit | — |
| Learning Objective | Measurable objective | Learning Objective |

Names collide across contexts **intentionally**. Do not rename V2 entities to match CKG.

### Containment dual representation

Structural ownership is stored as:

1. FK / ownership fields on entities (efficient tree walks)
2. Explicit `contains` edges in the graph aggregate / `ckg_edges` (uniform edge queries)

Both must agree when a full graph is materialised.

### Educational objects

Objects are first-class nodes with typed stable ids (`.DEF`, `.FOR`, `.WE`, `.PE`, `.RR`, `.SO`). Learning objectives **reference** them; subsections typically **contain** them. No item-bank payloads or PDF bytes.

---

## 3. Stable curriculum IDs

Pattern:

```
{SUBJECT}.T{tt}.S{ss}.{oo}.SS{uu}.LO{ll}
```

Example: `CS1.T04.S04.02.SS01.LO03`

Rules:

- **Edition-stable** — year/edition is on `Subject.edition_label` / `ckg_graph_editions`, never in the id
- Numeric segments are zero-padded; once assigned, ids are opaque
- Educational objects append typed suffixes
- Subject-level `RR` / `SO` may attach directly (`CS1.RR01`)
- Renumbers use `ckg_id_aliases` (`old_stable_id` → `new_stable_id`); never silent reuse

Implementation: `StableCurriculumId` in `app/domain/curriculum_knowledge_graph/value_objects/stable_curriculum_id.py`.

---

## 4. Traversal strategy

| Algorithm | Use |
|-----------|-----|
| Depth-first containment walk | Enumerate structure under a root (stable-sorted children) |
| Direct `requires` neighbours | Immediate prerequisites of an LO |
| Kahn topological sort over LOs | Lawful study order under hard prerequisites |
| Cycle detection on `requires` | Reject illegal prerequisite edges at write time |

Soft edges (`cross_references`, advisory object roles) do **not** participate in hard-prerequisite cycle detection or LO topological order.

ORM indexes support parent FK walks and edge endpoint lookups (`from_stable_id`, `to_stable_id`, `relationship_type`).

---

## 5. Versioning considerations

| Concern | Approach |
|---------|----------|
| Annual syllabus edition | New `ckg_graph_editions` row; reuse stable ids when structure unchanged |
| Structural renumber | Insert `ckg_id_aliases`; keep old id queryable |
| Parallel drafts | Future Founder Studio publish programmes own draft→published; CKG tables are the published educational store |
| Runtime dual-run | V1/V2 remain authoritative for student plans until explicit migration |

---

## 6. Persistence

Normalised `ckg_*` tables with FK containment, `ckg_lo_links` for LO→object references, `ckg_edges` for typed directed edges, and `ckg_id_aliases` for identity continuity.

Migration: `migrations/versions/202607280010_ei001_curriculum_knowledge_graph.py` (merges Alembic heads `202607190002` + `202607280002`).

---

## 7. Explicit non-goals (EI-001)

- Founder upload workflow / PDF parse / AI extraction  
- Mission generation / Twin redesign / UI redesign  
- Migrating student runtime off V1/V2  
- CIP → CKG publish pipeline  
