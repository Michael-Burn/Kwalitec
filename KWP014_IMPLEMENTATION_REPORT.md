# KWP-014 — Curriculum Intelligence & Knowledge Graph

**Programme:** KWP-014 · Knowledge Architecture Phase 1  
**Phase:** Curriculum Intelligence — Knowledge Architecture  
**Date:** 2026-07-31  
**Nature:** Curriculum structure layer — **not an Educational Intelligence rewrite**  
**Authority:** KWP-013 · KWP-012 · KWP-011 · KWP-010 · KWP-009 · KWP-008 · KWP-007 · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-014 models the curriculum itself as a structured **Knowledge Graph**: topics as nodes, educational relationships as edges. Educational Intelligence now answers *“Why does this topic matter?”* from explicit prerequisites, foundations, extensions, revision links, and dependency chains — not isolated topic metadata.

Students see a **Curriculum Map** (where today’s topic sits in the qualification), Adaptive Workspace Current Focus that explains curriculum position, and optional Learning Journey timeline references to curriculum movement. Founders see coverage, bottlenecks, difficult prerequisite chains, recovery/revision pathway usage, and graph completeness on Platform Intelligence.

**Verdict:** The platform understands how topics depend upon, reinforce, and build upon one another. Knowledge Architecture is educational structure; Educational Intelligence uses the graph — it does not replace it.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Topic nodes / curriculum metadata | Available | **EXISTING** · reused | `CurriculumGraph`, CKG, certified learner graph — no metadata duplication |
| 2 | Hard prerequisites (`requires`) | Available | **EXISTING** · reused | `DependencyType.REQUIRES` + `PrerequisiteService` |
| 3 | Soft links (revision / related / optional) | Available | **EXISTING** · extended | Prior soft set retained |
| 4 | Foundation / Extension / High Dependency | Absent | **NEW** | Added to `DependencyType` as soft relationships |
| 5 | Graph traversal / topo / successors | Available | **EXISTING** · reused | `CurriculumGraph` algorithms |
| 6 | Named learning paths | Available | **EXISTING** · reused | `LearningPath` + pathway projection |
| 7 | Revision clusters | Available | **EXISTING** · reused | `RevisionPathService` |
| 8 | Student Knowledge Map hierarchy UI | Available | **MODIFIED** · Curriculum Map | Renamed / enriched with pathway + why |
| 9 | Prerequisite natural-language reasoning | Absent | **NEW** | “Bayes relies heavily on Conditional Probability…” |
| 10 | Deterministic revision path kinds | Partial | **NEW** | Weak / Recovery / Exam / Mastery paths |
| 11 | Difficulty propagation to successors | Absent | **NEW** | Weak Interest Theory → Annuities / Loans / Bonds |
| 12 | Adaptive Workspace curriculum why | Absent | **NEW** · KWP-013 reuse | `curriculum_why` on Current Focus |
| 13 | Learning Journey curriculum movement | Absent | **NEW** · KWP-011 reuse | Optional timeline kinds |
| 14 | Founder KG analytics | Absent | **NEW** | Coverage, bottlenecks, chains, pathways |
| 15 | Learning Runtime / Evidence / Progress / Strategy / Diagnostics / Difficulty / Effectiveness / Memory / Forecast / Adaptive Workspace engines / Mission | Must not redesign | **EXISTING** unchanged | Graph consumed only |

### EXISTING (reused)

- `app/domain/curriculum/graph/CurriculumGraph` + `GraphBuilder`  
- `DependencyType`, `PrerequisiteService`, `RevisionPathService`, `CurriculumNavigationService`  
- `LearningPath` entities  
- Certified learner package → topic `prerequisite_ids` via `EducationalArtefactDeriver`  
- Student Knowledge Graph presentation + `/student/knowledge-graph`  
- Adaptive Study Workspace (KWP-013) Current Focus composition  
- Educational Memory timeline (KWP-011)  
- Founder Platform Intelligence section pattern  
- Product Language Guide  

### NEW

- `DependencyType.FOUNDATION` / `EXTENSION` / `HIGH_DEPENDENCY`  
- `app/application/knowledge_architecture/` — DTOs, relationships, graph adapter, prerequisite reasoning, pathways, revision paths, difficulty propagation, curriculum map, engine  
- `app/services/knowledge_architecture_metrics.py`  
- `tests/test_kwp014_knowledge_architecture.py`  
- `KWP014_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- Adaptive Workspace Current Focus — `curriculum_why` + Curriculum Map quick action  
- Student Knowledge Map → Curriculum Map enrichments  
- Educational Memory timeline — optional curriculum movement events  
- Founder alpha observability — Knowledge Architecture section  
- Product language — `Curriculum Map`, `Knowledge Architecture`  
- Domain curriculum enum exhaustive test  

---

## 3. Knowledge Graph Architecture

```
Certified package / Curriculum aggregate / topic specs
        │
        ▼
 GraphBuilder / graph_from_topic_specs / graph_from_learner_package
        │
        ▼
 CurriculumGraph  (nodes = topics, edges = DependencyType)
        │
        ▼
 KnowledgeArchitectureEngine
        ├─ explain / why_matters          (prerequisite reasoning)
        ├─ pathways                       (LearningPath + topology)
        ├─ revision_paths                 (weak / recovery / exam / mastery)
        ├─ difficulty_attention           (successor propagation)
        ├─ curriculum_map                 (student visual map)
        └─ snapshot / bottlenecks         (founder analytics)
        │
        ├── Adaptive Workspace Current Focus (curriculum_why)
        ├── Curriculum Map page
        ├── Educational Memory timeline (optional movement)
        └── Founder KnowledgeArchitectureMetrics
```

**Hard boundary:** Knowledge Architecture is **educational structure**. It never writes Evidence, Progress, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory state, Forecast, Twin, Adaptive Workspace engines, or Mission Runtime.

| Authority | Relationship |
|---|---|
| CurriculumGraph / CKG / Learner KG | Structure authority — reused, not duplicated |
| Learning Strategy / Diagnostics / Difficulty | Consumed as overlay signals for revision paths only |
| Educational Memory | Timeline optionally references curriculum movement |
| Adaptive Workspace | Presentation consumes `why_matters` |
| Readiness Forecast / Progress / Evidence / Mission | Unchanged |

---

## 4. Curriculum Model

Topics remain the atomic educational nodes. Metadata (title, difficulty band, effort minutes, prerequisite ids) continues to live on existing curriculum / certified package structures.

| Concern | Representation |
|---|---|
| Node | Topic (`topic_id`, title, difficulty, effort) |
| Hard prerequisite | `REQUIRES` — blocks eligibility |
| Foundation | `FOUNDATION` — soft educational foundation |
| Extension | `EXTENSION` — soft extension relationship |
| Frequently revised together | `REVISION` |
| High dependency | `HIGH_DEPENDENCY` — soft “relies heavily” |
| Optional reinforcement | `OPTIONAL` |

No AI generation. Pathways stay curriculum-specific (named `LearningPath` or topological syllabus order).

---

## 5. Dependency Rules

1. `A REQUIRES B` ⇒ B precedes A; hard eligibility; DAG enforced by existing graph algorithms.  
2. Soft edges never block eligibility alone.  
3. Educational relationship labels map onto `DependencyType` via `relationships.py` — no second edge store.  
4. Successors of a weak topic receive educational attention before deterioration is assumed on those dependents.  
5. Explanations only cite relationships present on the graph.

---

## 6. Revision Path Engine

Deterministic paths from curriculum relationships + learner overlay (completed / weak / current / days-to-exam):

| Kind | Derivation |
|---|---|
| Weak prerequisite path | Incomplete / weak ancestors of the focus topic, then focus |
| Recovery path | `RevisionPathService` review sequence seeded on a weak topic |
| Exam revision path | Near-exam (≤21 days): remaining / weak topics in topo order |
| Mastery reinforcement path | Completed foundations + revision/optional neighbours + focus |

Each path carries rationale and evidence codes. No LLM authorship.

---

## 7. Student Experience

### Curriculum Map (`/student/knowledge-graph`)

- Page title **Curriculum Map**  
- Highlights: Completed / Current / Future / Weak prerequisite  
- Pathway strip through the qualification  
- “Why current matters” from prerequisite reasoning  

### Adaptive Workspace (KWP-013 reuse)

- Current Focus shows `curriculum_why` when graph relationships resolve  
- Example: *“Today's topic builds directly on Discount Factors, which you strengthened recently.”*  
- Quick action: **Curriculum Map**  

### Learning Journey (KWP-011 reuse)

Optional timeline events:

- Foundation complete  
- Intermediate modelling  
- Exam integration  

Each may carry `curriculum_movement` (e.g. `foundation → intermediate modelling`).

---

## 8. Founder Analytics

Platform Intelligence section **Knowledge Architecture** reports:

- Curriculum coverage  
- Dependency bottlenecks  
- Most difficult prerequisite chain lengths  
- Recovery path count  
- Revision pathway usage  
- Curriculum Map opens  
- Knowledge graph completeness  

Implementation: `KnowledgeArchitectureMetrics` + alpha observability template.

---

## 9. Architecture Compliance

- Layering preserved: presentation → application knowledge architecture → domain curriculum graph.  
- No educational logic migrated out of Strategy / Diagnostics / Difficulty / Memory / Forecast.  
- Curriculum V1/V2 traversal unchanged; KA consumes certified packages / `CurriculumGraph` only.  
- No Flask globals inside knowledge-architecture services (explicit graph + context).  
- Deterministic cores — same graph + learner context ⇒ same explanations and paths.  

---

## 10. Files Created

- `app/application/knowledge_architecture/__init__.py`  
- `app/application/knowledge_architecture/dto.py`  
- `app/application/knowledge_architecture/relationships.py`  
- `app/application/knowledge_architecture/graph_adapter.py`  
- `app/application/knowledge_architecture/guidance.py`  
- `app/application/knowledge_architecture/prerequisite_reasoning.py`  
- `app/application/knowledge_architecture/pathways.py`  
- `app/application/knowledge_architecture/revision_paths.py`  
- `app/application/knowledge_architecture/difficulty_propagation.py`  
- `app/application/knowledge_architecture/curriculum_map.py`  
- `app/application/knowledge_architecture/engine.py`  
- `app/services/knowledge_architecture_metrics.py`  
- `tests/test_kwp014_knowledge_architecture.py`  
- `KWP014_IMPLEMENTATION_REPORT.md`  

## 11. Files Modified

- `app/domain/curriculum/value_objects/dependency_type.py`  
- `app/presentation/student/dto/adaptive_workspace.py`  
- `app/presentation/student/adaptive_workspace.py`  
- `app/presentation/student/services/student_knowledge_graph_presentation_service.py`  
- `app/templates/student/knowledge_graph.html`  
- `app/templates/student/home.html`  
- `app/static/css/design_system.css`  
- `app/application/educational_memory/dto.py`  
- `app/application/educational_memory/timeline.py`  
- `app/presentation/product_language.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  
- `tests/domain/curriculum/test_repository_and_independence.py`  

---

## 12. Tests

```bash
python3 -m pytest tests/test_kwp014_knowledge_architecture.py -v
python3 -m pytest tests/domain/curriculum/ tests/test_kwp013_adaptive_workspace.py tests/test_kwp011_educational_memory.py -v
python3 -m ruff check app/application/knowledge_architecture/ app/services/knowledge_architecture_metrics.py …
```

**Outcome:** KWP-014 suite **18 passed**; related curriculum / KWP-013 / KWP-011 suites green after enum exhaustive update; ruff clean on touched paths.

---

## 13. Migration Impact

**None.** No Alembic migrations. Graph relationships reuse existing curriculum domain types and certified package projections.

---

## 14. Known Limitations

1. Curriculum Map richness depends on published certified package prerequisite coverage — sparse packages yield sparse explanations.  
2. Adaptive Workspace `curriculum_why` soft-fails when no subject package / title match is available.  
3. Difficulty propagation is structural attention guidance — it does not mutate Learning Difficulty engine scores.  
4. Exam revision path uses a fixed ≤21-day proximity heuristic.  
5. CKG (LO-level) and topic-level `CurriculumGraph` remain parallel structure authorities; KA Phase 1 standardises on topic-level commercial path.  
6. No interactive graph editor — relationships remain curriculum-authored / certified.  

---

## 15. Technical Debt

- Unify topic-level KA with LO-level CKG under one read model in a later phase.  
- Persist revision-pathway usage events explicitly (currently inferred from presentation telemetry).  
- Wire founder metrics to a live loaded subject graph when Platform Intelligence has an active curriculum edition in context.  

---

## 16. Recommendation for KWP-015

**Working title:** KWP-015 — Knowledge Architecture Continuity & Pathway Authority

**Suggested scope:**

1. Persist and dogfood Curriculum Map / revision-path usage with real certified editions.  
2. Consolidate topic-level and LO-level graph reads behind one student-safe projection.  
3. Feed difficulty-propagation attention into Mission selection as *advisory structure* (still no EI rewrite).  
4. Founder drill-down: bottleneck topics → affected learners → recommended recovery paths.  
5. Validate explanation quality against actuarial syllabus chains (Probability → … → Risk Modelling; Interest Theory → Annuities / Loans / Bonds).  

**Next programme:** KWP-015 Knowledge Architecture Continuity & Pathway Authority (recommended)
