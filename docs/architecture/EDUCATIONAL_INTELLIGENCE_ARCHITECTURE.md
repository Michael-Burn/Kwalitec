# Educational Intelligence Architecture

**Status:** Canonical architecture specification — Milestone E2.0  
**Epic:** Epic 2 – Educational Intelligence  
**Version:** v0.5.x Development  
**Audience:** Product, engineering, AI agents, subsystem owners  
**Scope:** Architecture only — no implementation, schema, or service changes  
**Companion docs:** [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`PRODUCT_BLUEPRINT.md`](../../PRODUCT_BLUEPRINT.md), [`ARCHITECTURE.md`](../../ARCHITECTURE.md), [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)

---

## Document purpose

This document is the **definitive Educational Intelligence Architecture** for Epic 2.

It defines how Kwalitec understands a student’s educational state and how that understanding produces the highest-value next learning action — without implementing scoring formulas, persistence, or HTTP surfaces.

It answers:

1. What Educational Intelligence is and why it exists  
2. How the Digital Twin is structured as the authoritative learner model  
3. Which domains own which educational concerns  
4. How Learning Evidence maps to domain updates  
5. Who owns each Update Strategy  
6. How domains interact  
7. How Readiness is derived (not invented)  
8. How the Decision Engine reasons  
9. How recommendations are generated  
10. How every recommendation remains explainable  
11. How the architecture extends safely  
12. What risks must be managed  
13. Which principles bind all Epic 2 work  
14. Domain interaction diagrams  
15. Sequence diagrams for core flows  

**Non-goals of this document**

- Code, pseudocode algorithms, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete mastery / retention / readiness formulas  
- UI redesign, gamification, dashboards, notifications, or social features  
- Replacement of the Curriculum Engine as syllabus truth  
- Replacement of [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) or [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) as deeper domain companions  

**Current foundation (already delivered)**

| Capability | Status |
|---|---|
| 2.1 Student Digital Twin Domain | Complete |
| 2.2 Twin Update Pipeline | Complete |
| 2.3 Knowledge Update Strategy | Complete (structural) |
| 2.4 Memory Update Strategy | Complete (structural) |
| 2.5–2.10 Behaviour → Mission Intelligence | Planned under this architecture |

---

# 1. Educational Intelligence Vision

## 1.1 Product thesis

Epic 1 taught Kwalitec **what the student needs to learn** (official curriculum structure, V1/V2 traversal, planning foundations).

Epic 2 teaches Kwalitec **how to understand the student**.

Educational Intelligence is the capability to:

> Represent learning — not study, not activity, not motivation alone — and continuously answer:  
> **What is the highest-value thing this student should do next?**

## 1.2 What “learning” means here

| Concept | Meaning in Epic 2 |
|---|---|
| **Study** | Time spent with content; may or may not produce learning |
| **Activity** | Engagement events (sessions, missions, clicks); behavioural signal |
| **Motivation** | Willingness and sustainability signals; context for decisions, not mastery |
| **Learning** | Durable change in knowledge and retention relative to the official syllabus |

The Digital Twin models **learning state**. Activity and motivation inform Behaviour and Confidence; they do not substitute for Knowledge or Performance.

## 1.3 Operating model

```
Curriculum (shared syllabus truth)
        +
Learning Evidence (immutable student history)
        ↓
Digital Twin (authoritative educational state)
        ↓
Readiness + Decision Engine
        ↓
Explainable Recommendation → Mission / Plan consequences
```

Services **consume** Twin state. They must not invent competing educational state stores.

## 1.4 Success criteria (architectural)

Educational Intelligence succeeds when:

- every educational state is evidence-driven;  
- readiness is measurable and factorable;  
- recommendations are explainable and traceable to evidence;  
- missions and plans become adaptive *consequences* of Twin state;  
- Knowledge, Memory, Behaviour, Performance, Confidence, Readiness, and Decision State operate as one coherent reasoning system through the Twin.

## 1.5 Explicit non-goals (Epic 2 product surface)

Epic 2 architecture does **not** mandate:

- UI redesign  
- gamification  
- analytics dashboards as a second intelligence layer  
- notifications product work  
- social features  
- black-box LLM ownership of core recommendation paths  

Those belong to later epics or orthogonal product tracks.

---

# 2. Digital Twin Architecture

## 2.1 Definition

The **Student Digital Twin** is Kwalitec’s single authoritative representation of a learner’s exam-preparation state relative to a syllabus and sitting.

It is:

- **evidence-backed** — beliefs evolve from Learning Evidence;  
- **immutable per snapshot** — updates produce new Twin snapshots, never in-place mutation of aggregates;  
- **curriculum-referenced** — topics and sections are syllabus identities, never invented trees;  
- **deterministic for core consumers** — same Twin inputs → same readiness/decision outputs in core paths;  
- **probabilistic where knowledge is uncertain** — mastery/retention are beliefs, not binary badges.

It is **not**:

- a study plan;  
- a mission list;  
- a dashboard cache;  
- a second curriculum.

## 2.2 Aggregate structure (Epic 2 educational domains)

Epic 2 focuses the Twin on the educational domains required for intelligence:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Student Digital Twin                            │
│                                                                         │
│  Identity · Goals                                                       │
│                                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │Knowledge │ │  Memory  │ │Behaviour │ │Performan.│                    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                                 │
│  │Confidence│ │Readiness │ │Decision  │  (+ Prediction snapshots)       │
│  │          │ │(derived) │ │  State   │                                 │
│  └──────────┘ └──────────┘ └──────────┘                                 │
│                                                                         │
│  Evidence lineage (ids) · Decision Journal (outcomes)                   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Notes on domain placement**

| Domain | Twin role |
|---|---|
| **Identity / Goals** | Scope the Twin (who, which paper/sitting, capacity) |
| **Knowledge** | What they know *now* (mastery structure + beliefs) |
| **Memory** | Whether they will still know it (retention structure + beliefs) |
| **Behaviour** | How they actually study (consistency, patterns) |
| **Performance** | How they perform under assessment conditions |
| **Confidence** | Self-reported and calibrated certainty (distinct from mastery) |
| **Readiness** | Derived aggregate for exam preparedness (may be stored as Prediction snapshot) |
| **Decision State** | Last decision context, candidates considered, accept/dismiss lineage |
| **Predictions** | Stored readiness / pass-probability snapshots produced elsewhere |

Companion [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) also describes Planning and Motivation as broader Twin domains. Epic 2 treats **Planning artefacts** (WeekPlan, Mission) as *consequences* of Decision Engine output, and **Motivation/burnout** as inputs that Behaviour and Confidence may surface — without making plans or dashboards the source of truth.

## 2.3 Twin Update Pipeline (write path)

```
Learning Evidence (append-only)
      → UpdateContext (Twin + evidence + metadata)
            → TwinUpdatePipeline
                  → registered Update Strategies (registration order)
                        → new DigitalTwin snapshot (UpdateResult)
```

Rules:

1. Evidence is the only legitimate input that may change Twin beliefs.  
2. The pipeline coordinates; strategies own domain-specific evolution.  
3. Strategies are open for extension via registration — the pipeline class must not hard-code educational algorithms.  
4. Multiple strategies may apply to one evidence batch; each receives a context whose Twin reflects prior strategies.  
5. Strategies must remain framework-free (no Flask/ORM/HTTP).

## 2.4 Separation of write and read intelligence

| Path | Responsibility |
|---|---|
| **Update Strategies** | Write: evolve Twin domains from evidence |
| **Readiness Aggregation** | Read: derive preparedness factors from Twin + Curriculum + Goals |
| **Decision Engine** | Read: select highest-value next action from Twin + constraints |
| **Recommendation / Mission generators** | Read: project decisions into product artefacts |
| **Insight / Coach (future)** | Read: narrate Twin factors; must not silently mutate Twin |

Write and read must not be conflated. Services that recommend must not quietly rewrite Knowledge or Memory outside the pipeline.

## 2.5 Layering relative to application architecture

Educational Intelligence sits **inside** the existing layered application:

```
Templates / JS
      ↓
Blueprints
      ↓
Services (orchestration, persistence bridges, product projections)
      ↓
Domain: Twin + Evidence + Update Strategies + Decision/Readiness logic
      ↓
Models + Curriculum Engine
      ↓
DB / JSON
```

Domain packages under `app/domain/` remain free of Flask and SQLAlchemy. Persistence and HTTP stay in services and blueprints. Curriculum Engine remains syllabus truth for structure and weights.

---

# 3. Domain Responsibilities

## 3.1 Knowledge

| | |
|---|---|
| **Question** | What does the student know *now*? |
| **Owns** | Per-topic mastery slots, evidence references supporting those slots, stored mastery beliefs when supplied |
| **Does not own** | Forgetting curves, revision schedules, exam readiness composites, recommendations |
| **Update owner** | `KnowledgeUpdateStrategy` (Capability 2.3 — structural; richer belief math later) |
| **Typical evidence** | Question attempts, quizzes, diagnostics, mocks (assessment-shaped) |

Knowledge must not encode Memory decay. Coverage gaps are interpreted against Curriculum, not invented inside Knowledge.

## 3.2 Memory

| | |
|---|---|
| **Question** | Will the student still know it when it matters? |
| **Owns** | Per-topic retention slots, last-reinforced clocks, revision evidence references, stored retention beliefs when supplied |
| **Does not own** | Mastery scoring, mission generation, curriculum weights |
| **Update owner** | `MemoryUpdateStrategy` (Capability 2.4 — structural; retention/decay engines later) |
| **Typical evidence** | Revision sessions, flashcard reviews |

Memory must not become a second mastery store. Knowledge and Memory remain complementary.

## 3.3 Behaviour

| | |
|---|---|
| **Question** | How does the student actually study? |
| **Owns** | Consistency metrics structure, session/pattern references, adherence-related structural facts |
| **Does not own** | Mastery, retention beliefs, exam pass probability |
| **Update owner** | `BehaviourUpdateStrategy` (Capability 2.5 — planned) |
| **Typical evidence** | Mission completed/missed, skipped sessions, abandons, time-on-task, study breaks, recommendation accept/dismiss |

Behaviour informs sustainable pacing and plan realism. It never grants mastery by itself.

## 3.4 Performance

| | |
|---|---|
| **Question** | How does the student perform when assessed? |
| **Owns** | Assessment references, scoped performance summaries, structural performance facts |
| **Does not own** | Daily mission scheduling, syllabus structure |
| **Update owner** | `PerformanceUpdateStrategy` (Capability 2.6 — planned) |
| **Typical evidence** | Quiz/mock/past-paper outcomes, diagnostic assessments, scored attempts |

Performance is the strongest assessed signal into Knowledge and Readiness. It remains a distinct domain so assessment trends are not collapsed into session activity.

## 3.5 Confidence

| | |
|---|---|
| **Question** | How certain does the student *feel*, and how well is that calibrated? |
| **Owns** | Self-report confidence signals, calibration structure against Performance, confidence-tagged evidence lineage |
| **Does not own** | True mastery (Knowledge), retention clocks (Memory), final readiness score alone |
| **Update owner** | Confidence channel within Behaviour/Knowledge strategies or a dedicated Confidence update path — architectural requirement: Confidence remains **separable** from mastery |
| **Typical evidence** | Confidence ratings, readiness self-reviews, reflections |

Confidence is evidence, usually down-weighted relative to assessed Performance. Overconfidence and underconfidence are first-class educational signals for Decision Engine risk framing — not vanity metrics.

## 3.6 Readiness

| | |
|---|---|
| **Question** | How prepared is the student for the target sitting, given syllabus weight and time? |
| **Owns** | Derived readiness factors and optional stored snapshots (PredictionState); factor attributions for explainability |
| **Does not own** | Raw evidence history, syllabus definition, next-action selection |
| **Derivation owner** | Readiness Aggregation (Capability 2.7 — planned); may persist snapshots via Prediction snapshot strategy |
| **Inputs** | Knowledge, Memory, Performance, Behaviour, Confidence, Goals (exam date/capacity), Curriculum weights |

Readiness is **derived**, not a primary write domain fed by arbitrary side channels. See §7.

## 3.7 Decision State

| | |
|---|---|
| **Question** | What decision context is current, and what was recommended/accepted? |
| **Owns** | Candidate actions considered, selected action, reason codes, Twin snapshot references, Decision Journal linkage |
| **Does not own** | Twin domain belief math, curriculum structure |
| **Producer** | Decision Engine (Capability 2.8) and recommendation outcome evidence |
| **Consumers** | Explainable Recommendation Engine, Mission Generation Intelligence, Analytics (read-only) |

Decision State closes the loop: recommendations leave attributable history so future Behaviour and Decision Engine runs can learn from accept/dismiss without inventing state.

## 3.8 Identity and Goals (scoping domains)

| Domain | Responsibility in Educational Intelligence |
|---|---|
| **Identity** | Bind Twin to student; scope all operations |
| **Goals** | Active paper/sitting, ambition, weekly hours, deadline — constraints for Readiness and Decision Engine |

Neither Identity nor Goals invent syllabus topics. Goals reference Curriculum identity.

---

# 4. Evidence Ownership Matrix

Learning Evidence is the immutable history. Domains are the derived state. The matrix below is architectural ownership — not a scoring formula.

| Evidence category / type (illustrative) | Knowledge | Memory | Behaviour | Performance | Confidence | Goals | Decision State |
|---|---|---|---|---|---|---|---|
| Question attempt / correct / incorrect | **Primary** | — | Secondary | Secondary | — | — | — |
| Quiz / mock / past paper / diagnostic | **Primary** | — | Secondary | **Primary** | Secondary | — | — |
| Revision session / flashcard review | Secondary | **Primary** | Secondary | — | — | — | — |
| Mission completed / missed | — | — | **Primary** | — | — | — | Secondary |
| Skipped / abandoned session | — | — | **Primary** | — | — | — | — |
| Time on task / study break | — | — | **Primary** | — | — | — | — |
| Confidence rating / readiness review (self) | Secondary | — | Secondary | — | **Primary** | — | — |
| Plan reschedule / exam date / goal change | — | — | Secondary | — | — | **Primary** | Secondary |
| Recommendation decision (accept/dismiss) | — | — | Secondary | — | — | — | **Primary** |
| Post-exam outcome | Secondary | — | — | **Primary** | — | Secondary | Secondary |

**Legend**

- **Primary** — strategy/domain that must evolve when this evidence arrives  
- **Secondary** — may update structural references or weak signals; must not steal primary ownership  
- **—** — not a legitimate owner for that evidence type  

**Hard rules**

1. No domain may claim exclusive ownership of evidence types outside its column without architecture review.  
2. Mixed batches are valid: one quiz may update Knowledge *and* Performance.  
3. Evidence ids are append-only references; domains never rewrite the evidence log.  
4. Curriculum identity on topic-scoped evidence remains mandatory for Knowledge/Memory/Performance topic slots.

---

# 5. Update Strategy Ownership

## 5.1 Ownership table

| Strategy | Capability | Domain mutated | Status |
|---|---|---|---|
| `KnowledgeUpdateStrategy` | 2.3 | KnowledgeState | Complete (structural) |
| `MemoryUpdateStrategy` | 2.4 | MemoryState | Complete (structural) |
| `BehaviourUpdateStrategy` | 2.5 | BehaviourState | Planned |
| `PerformanceUpdateStrategy` | 2.6 | PerformanceState | Planned |
| Confidence update path | (with 2.5/2.3 or dedicated) | Confidence structure | Planned — must remain separable |
| `PredictionSnapshotStrategy` | 2.7 adjacent | PredictionState | Planned (store readiness/pass snapshots) |
| Decision State materialisation | 2.8 / 2.9 | Decision State | Planned (from Decision Engine outcomes) |

## 5.2 Strategy contract (architectural)

Every Update Strategy:

1. Declares a stable `name` for audit in `UpdateResult`.  
2. Implements `supports(context)` based on evidence types and required fields (e.g. `topic_id`).  
3. Implements `apply(context)` returning a **new** Twin snapshot.  
4. Remains pure domain logic: no persistence, HTTP, recommendations, or planning.  
5. Preserves unknown belief fields when structural-only (does not invent mastery math prematurely).

## 5.3 Registration and ordering

- Strategies register with `TwinUpdatePipeline` (constructor list or `register`).  
- Invocation follows **registration order**.  
- Ordering must be intentional when strategies can interact (e.g. Performance before Knowledge belief enrichment once both compute beliefs).  
- Structural phase (current): Knowledge then Memory is sufficient; Behaviour/Performance order will be fixed in Capability 2.5–2.6 architecture notes before coding.

## 5.4 What strategies must not do

- Compute final readiness composites  
- Select next actions or generate missions  
- Persist Twin or evidence  
- Import Flask / SQLAlchemy / request globals  
- Mutate Twin aggregates in place  
- Absorb foreign domain evidence types (e.g. Memory must not own attempt types)

---

# 6. Interaction Between Domains

## 6.1 Complementary pairs

| Pair | Relationship |
|---|---|
| Knowledge ↔ Memory | Know-now vs still-know; complementary, non-competing |
| Performance ↔ Knowledge | Assessed outcomes strongly inform mastery beliefs |
| Performance ↔ Confidence | Calibration: self-report vs measured accuracy |
| Behaviour ↔ Goals | Adherence vs committed capacity |
| Memory ↔ Behaviour | Revision discipline affects retention clocks |
| Knowledge/Memory/Performance/Behaviour/Confidence → Readiness | Inputs to derived preparedness |
| Twin domains → Decision Engine | Inputs to next-action selection |
| Decision State → Behaviour | Accept/dismiss becomes behavioural evidence |

## 6.2 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| Mission service writes mastery directly | Bypasses Evidence → Strategy pipeline |
| Readiness service invents topic order | Breaks V1/V2 curriculum invariants |
| Recommendation embeds hidden Twin mutation | Breaks explainability and audit |
| Memory stores mastery_belief as retention | Collapses domains |
| Analytics forks readiness formula | Second source of truth |
| LLM invents syllabus topics in Twin | Violates curriculum-first principle |

## 6.3 Interaction with Curriculum

Curriculum Engine / `CurriculumService` owns:

- structure (Section → Topic → Learning Objective in V2; V1 flat/tree);  
- canonical ordering;  
- exam weights (topic-level V1 / section-level V2).

Twin domains **reference** curriculum identities. Decision Engine and Readiness **consume** weights and order. Neither Twin nor Decision Engine may invent parallel syllabi.

## 6.4 Interaction with product services (consequences)

| Product artefact | Relationship to Educational Intelligence |
|---|---|
| Study Plan / WeekPlan | Regenerated from Goals + Twin + Curriculum + time constraints |
| Mission / MissionTask | Projected from Decision Engine / Mission Generation Intelligence |
| Decision Journal | Records accept/dismiss; feeds evidence and Decision State |
| Legacy ReadinessService / RecommendationService | Must migrate toward Twin-first inputs without maintaining divergent learner-state stores |

Legacy services remain operational during transition; architecture requires convergence on Twin as learner-state authority (see §11 and Recommendations).

---

# 7. Readiness Derivation

## 7.1 Definition

**Readiness** is a derived, explainable estimate of how prepared the student is for the active Goal’s sitting, relative to official syllabus weighting and remaining time.

Readiness answers: *Are we on track to pass?* — not *What should I do in the next 45 minutes?* (that is Decision Engine).

## 7.2 Derivation principle

```
Readiness = Aggregate(
    Curriculum weights + order,
    Knowledge beliefs / coverage,
    Memory retention risk,
    Performance assessment signals,
    Behaviour consistency / pace,
    Confidence calibration (optional factor),
    Goals: exam date, capacity
)
```

Architectural constraints:

1. **Factorable** — overall readiness must decompose into named factors (coverage, mastery risk, retention risk, pace, assessment strength, time pressure).  
2. **Deterministic** — same Twin + Curriculum + Goals → same factor set and composite in core path.  
3. **V1/V2 safe** — weight handling branches on curriculum format; traversal uses canonical helpers only.  
4. **Snapshotable** — results may be stored in PredictionState for history; storage must not become a write-side hack that skips derivation.  
5. **Explainable** — every presented readiness claim cites factors and underlying Twin/evidence lineage.

## 7.3 Ownership

| Concern | Owner |
|---|---|
| Factor computation & aggregation | Readiness Aggregation (Capability 2.7) |
| Storing readiness/pass snapshots | Prediction snapshot path (optional strategy) |
| Syllabus denominator & weights | Curriculum Engine / CurriculumService |
| Presenting readiness in UI | Analytics/Dashboard services (read-only consumers) |

## 7.4 What Readiness must not do

- Select the next study action (Decision Engine)  
- Mutate Knowledge/Memory  
- Require Sections globally (breaks V1)  
- Emit opaque single scores without factors  
- Treat mission completion as equivalent to exam readiness  

---

# 8. Decision Engine Architecture

## 8.1 Single guiding question

> **What is the highest-value thing this student should do next?**

“Highest-value” means expected educational value toward the Goal (pass the sitting), given Twin state, Curriculum weights, and constraints (time available, sustainable intensity).

## 8.2 Position in the system

```
Digital Twin (current snapshot)
        +
Curriculum (weights, order, LOs)
        +
Constraints (available time, session length, burnout/behaviour flags)
        ↓
Decision Engine
        ↓
Decision State + Explainable Recommendation
        ↓
Mission Generation / Plan rebalance (consumers)
```

The Decision Engine is a **read-side reasoner**. It does not update Knowledge or Memory. Outcomes (accept/dismiss/complete) become Learning Evidence that later update Behaviour and Decision State.

## 8.3 Inputs (architectural)

| Input class | Sources |
|---|---|
| Syllabus value | Exam weights, prerequisites, canonical remaining topics |
| Knowledge gaps | KnowledgeState mastery slots / beliefs |
| Retention risk | MemoryState retention / last_reinforced |
| Assessment weakness | PerformanceState summaries |
| Behavioural feasibility | BehaviourState consistency; capacity from Goals |
| Confidence risk | Over/under-confidence vs Performance |
| Readiness context | Readiness factors (urgency, time pressure) |
| Decision history | Prior Decision State / Decision Journal |

## 8.4 Outputs (architectural)

| Output | Description |
|---|---|
| **Selected action** | Canonical next action (e.g. study topic X, revise topic Y, take diagnostic, rest) |
| **Candidate set** | Alternatives considered (for explainability) |
| **Reason codes** | Stable machine-readable factors |
| **Human explanation chain** | See §10 |
| **Decision State update** | Materialised decision context for audit |
| **Value rationale** | Why this action maximises expected educational value *now* |

## 8.5 Decision principles

1. **Curriculum-weighted value** — high-weight weak areas outrank low-weight polish when time is scarce.  
2. **Evidence over assumption** — cold-start defaults are explicit and low-confidence.  
3. **Learning over activity** — prefer actions that move Knowledge/Memory/Performance, not empty completion.  
4. **Retention awareness** — overdue high-value Memory risk can beat new coverage.  
5. **Feasibility** — Behaviour and capacity constrain ambition; burnout signals demote intensity.  
6. **Determinism** — same inputs → same selected action in core path (no random theatre).  
7. **Explainability mandatory** — no recommendation without reason codes + evidence lineage.  
8. **No LLM ownership** — generative assistance may narrate; it must not own the selection function.

## 8.6 Relationship to legacy RecommendationService

Today’s recommendation/readiness services are product-facing ancestors. Epic 2 architecture requires that the Decision Engine become the authoritative next-action reasoner, with Twin-first inputs. Migration is additive: preserve behaviour, redirect authority, retire divergent state.

---

# 9. Recommendation Generation

## 9.1 Definition

A **Recommendation** is the product projection of a Decision Engine output: a concrete, attributable suggestion the student can accept, dismiss, or act on.

Capability 2.9 (Explainable Recommendation Engine) owns presentation-quality packaging of Decision Engine results. Capability 2.10 (Mission Generation Intelligence) owns translating decisions into daily mission structure.

## 9.2 Generation pipeline (architectural)

```
Decision Engine selected action
        ↓
Recommendation packaging
  - title / action type
  - curriculum identity (topic/section/LO as applicable)
  - reason codes + explanation chain
  - urgency / estimated duration
  - Twin snapshot reference / evidence citations
        ↓
Optional Mission projection
        ↓
Decision Journal recording (accept / dismiss / defer)
        ↓
Learning Evidence (recommendation_decision)
```

## 9.3 Recommendation properties

| Property | Requirement |
|---|---|
| **Attributable** | Cites Twin factors and evidence ids / aggregates |
| **Curriculum-bound** | Uses canonical topic/section identities |
| **Actionable** | Maps to a clear student action |
| **Comparable** | Reason codes allow analytics without opaque scores |
| **Non-authoritative for state** | Accepting a recommendation does not grant mastery; completion evidence does |

## 9.4 Mission Generation Intelligence (Capability 2.10)

Missions become adaptive when they:

1. Start from Decision Engine outputs (or a batch thereof for a session window);  
2. Respect Behaviour feasibility and Goals capacity;  
3. Prefer learning-value tasks over filler;  
4. Remain regenerable when Twin state changes;  
5. Never store a private mastery model inside mission rows.

---

# 10. Explainability Chain

## 10.1 Mandatory chain

Every educational recommendation must be able to answer **Why?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant)
                → Decision Engine reason code(s)
                    → Recommendation explanation
```

Students must never be asked to trust a black box for core next-action advice.

## 10.2 Explanation layers

| Layer | Example content |
|---|---|
| **Curriculum** | “Section C carries 25% exam weight.” |
| **Evidence** | “Last three attempts on Topic T were incorrect (evidence ids …).” |
| **Twin** | “Knowledge mastery belief low; Memory last reinforced 28 days ago.” |
| **Readiness** | “Retention risk elevates pass risk on weighted Section C.” |
| **Decision** | “Revise Topic T now: high weight × high retention risk × feasible session length.” |

## 10.3 Audit artefacts

| Artefact | Role |
|---|---|
| Learning Evidence log | Immutable history |
| Twin snapshot / domain evidence ids | State lineage |
| Decision State | Candidates + selected action + reason codes |
| Decision Journal | User response to recommendations |
| PredictionState metadata | Model/version factors for readiness snapshots |

## 10.4 Forbidden explanation patterns

- Single opaque composite without factors  
- Explanations that cite UI labels but not Twin/evidence  
- LLM-generated rationales that invent evidence  
- Post-hoc stories that disagree with Decision Engine reason codes  

---

# 11. Future Extensibility

## 11.1 Extension points

| Extension | How to extend safely |
|---|---|
| New Update Strategy | Subclass strategy contract; register with pipeline; do not fork pipeline algorithms |
| Richer Knowledge/Memory beliefs | Extend strategies or successor engines; keep structural slots stable |
| New evidence types | Add to Evidence Model catalogue; assign primary domain in ownership matrix |
| New readiness factors | Add named factors to aggregation; preserve V1/V2 traversal |
| New decision reason codes | Version reason vocabulary; keep deterministic selection |
| Insight / AI Coach | Read Twin + explanations; never silent Twin writes |
| Multi-paper Goals | Scope inside one Twin via Goals — do not duplicate Twins |
| Institutional overlays | Observe Twin; do not fork student-owned state |

## 11.2 Compatibility guarantees

1. **Curriculum V1 and V2** remain loadable and traversable.  
2. **Structural Twin fields** prefer additive optional fields over breaking renames.  
3. **Evidence append-only** semantics remain permanent.  
4. **Deterministic cores** remain free of required network LLM calls.  
5. **Legacy product services** may adapt via adapters; they must not become permanent parallel Twin stores.

## 11.3 Deferred educational algorithms

The following are deliberately **not** locked by E2.0 beyond ownership boundaries:

- Specific mastery models (BKT, IRT, heuristic)  
- Specific forgetting curves / FSRS / SM-2  
- Numeric readiness weights  
- Exact Decision Engine scoring function  

E2.0 locks **where** those algorithms live and **how** their outputs enter Twin, Readiness, and Decision paths.

---

# 12. Risks

| Risk | Impact | Architectural mitigation |
|---|---|---|
| **Parallel learner-state stores** | Divergent mastery/readiness; broken trust | Twin is sole educational state authority; services consume Twin |
| **Domain collapse** (Memory≈Knowledge) | Unexplainable dual scores | Strict ownership matrix; complementary questions |
| **Evidence → Twin bypass** | Silent mutations; no audit | All belief changes via Evidence + Update Strategies |
| **Opaque Decision Engine** | Product thesis failure | Mandatory reason codes + explainability chain |
| **V1 breakage** | Legacy plans/readiness fail | Canonical traversal; nullable sections; dual weight handling |
| **Premature scoring complexity** | Unmaintainable math before domains mature | Structural strategies first; beliefs additive later |
| **Readiness conflated with next action** | Wrong UX and wrong owners | Separate Readiness Aggregation vs Decision Engine |
| **Mission rows as mastery** | Stale private state | Missions are projections only |
| **LLM ownership creep** | Non-determinism; invented syllabus | Coach narrates; Decision Engine selects |
| **Strategy order hazards** | Non-reproducible Twin updates | Explicit registration order; documented in capability reviews |
| **Confidence treated as mastery** | Optimistic false readiness | Confidence separable; down-weighted vs Performance |
| **Transition debt from legacy services** | Dual formulas during Epic 2 | Explicit convergence plan; no new forks |

---

# 13. Architecture Principles

These principles bind all Epic 2 Educational Intelligence work.

1. **Digital Twin is the single source of truth for educational state.**  
2. **Curriculum is the single source of truth for syllabus structure and weights.**  
3. **Learning Evidence is the only legitimate input that changes Twin beliefs.**  
4. **Update Strategies own domain evolution; the pipeline only coordinates.**  
5. **Services consume Twin state; they do not invent educational state.**  
6. **Plans and missions are consequences of intelligence, not the learner model.**  
7. **Knowledge and Memory remain complementary, never competing mastery stores.**  
8. **Readiness is derived and factorable; Decision Engine selects next action.**  
9. **Every recommendation must be explainable via the evidence → Twin → decision chain.**  
10. **Core paths are deterministic and free of black-box LLM ownership.**  
11. **V1 and V2 curricula both remain first-class.**  
12. **Prefer additive, immutable snapshots over in-place mutation and breaking rewrites.**  
13. **Confidence is not mastery; Behaviour is not learning; Activity is not readiness.**  
14. **Educational fidelity over engagement theatre.**  
15. **Architecture before implementation for each capability (Epic 2 engineering standard).**  

---

# 14. Domain Interaction Diagrams

## 14.1 Educational Intelligence system context

```
┌────────────────────┐     ┌────────────────────┐
│ Curriculum Engine  │     │ Learning Evidence  │
│ (syllabus truth)   │     │ (immutable history)│
└─────────┬──────────┘     └─────────┬──────────┘
          │                          │
          │         ┌────────────────▼────────────────┐
          │         │     Twin Update Pipeline         │
          │         │  Knowledge / Memory / Behaviour  │
          │         │  Performance / Confidence / …    │
          │         └────────────────┬────────────────┘
          │                          │
          │         ┌────────────────▼────────────────┐
          └────────►│       Student Digital Twin       │
                    │  Knowledge Memory Behaviour      │
                    │  Performance Confidence          │
                    │  Readiness* Decision State        │
                    └───────┬───────────────┬──────────┘
                            │               │
                ┌───────────▼──┐    ┌───────▼──────────┐
                │  Readiness   │    │ Decision Engine  │
                │ Aggregation  │───►│ (next action)    │
                └──────────────┘    └───────┬──────────┘
                                            │
                            ┌───────────────▼──────────────┐
                            │ Explainable Recommendations  │
                            │ Mission Generation           │
                            └───────────────┬──────────────┘
                                            │
                            ┌───────────────▼──────────────┐
                            │ Decision Journal → Evidence  │
                            └──────────────────────────────┘

* Readiness factors derived; optional PredictionState snapshot
```

## 14.2 Twin domain complementarity

```
                 ┌─────────────┐
                 │ Performance │◄──── assessed outcomes
                 └──────┬──────┘
                        │ informs
           ┌────────────▼────────────┐
           │       Knowledge         │  “know now”
           └────────────┬────────────┘
                        │ complementary
           ┌────────────▼────────────┐
           │        Memory           │  “still know”
           └────────────┬────────────┘
                        │
     ┌──────────────────┼──────────────────┐
     │                  │                  │
┌────▼─────┐     ┌──────▼─────┐     ┌──────▼─────┐
│Behaviour │     │ Confidence │     │   Goals    │
│ how they │     │ feel vs    │     │ deadline / │
│  study   │     │  calibrate │     │  capacity  │
└────┬─────┘     └──────┬─────┘     └──────┬─────┘
     │                  │                  │
     └──────────────────┼──────────────────┘
                        ▼
                 ┌─────────────┐
                 │  Readiness  │  (derived)
                 └──────┬──────┘
                        ▼
                 ┌─────────────┐
                 │  Decision   │
                 │   Engine    │
                 └─────────────┘
```

## 14.3 Evidence → domain ownership (simplified)

```
Assessment evidence ──────────► Knowledge + Performance
Revision evidence ────────────► Memory
Mission / skip / time ────────► Behaviour
Confidence ratings ───────────► Confidence
Goal / exam date changes ─────► Goals
Recommendation decisions ─────► Decision State (+ Behaviour)
```

---

# 15. Sequence Diagrams

## 15.1 Twin update from Learning Evidence

```
Student/UI          Evidence Path         TwinUpdatePipeline      Strategies         DigitalTwin
    │                     │                        │                   │                  │
    │  learning event     │                        │                   │                  │
    │────────────────────►│                        │                   │                  │
    │                     │ validate → Evidence    │                   │                  │
    │                     │───────────────────────►│                   │                  │
    │                     │                        │ supports?/apply   │                  │
    │                     │                        │──────────────────►│                  │
    │                     │                        │                   │ new domain state │
    │                     │                        │                   │─────────────────►│
    │                     │                        │◄──────────────────│ new Twin snapshot│
    │                     │     UpdateResult       │                   │                  │
    │                     │◄───────────────────────│                   │                  │
```

## 15.2 Readiness derivation

```
Consumer            Readiness Aggregation         DigitalTwin         Curriculum
   │                         │                         │                    │
   │  request readiness      │                         │                    │
   │────────────────────────►│  read domain states     │                    │
   │                         │────────────────────────►│                    │
   │                         │  weights / order        │                    │
   │                         │─────────────────────────────────────────────►│
   │                         │  factorise + aggregate  │                    │
   │  readiness + factors    │                         │                    │
   │◄────────────────────────│  optional snapshot → PredictionState        │
```

## 15.3 Decision → recommendation → evidence loop

```
Consumer     Decision Engine     Twin+Curriculum     Recommendation      Decision Journal     Evidence
   │               │                   │                   │                    │                │
   │ next action?  │                   │                   │                    │                │
   │──────────────►│ read Twin/factors │                   │                    │                │
   │               │──────────────────►│                   │                    │                │
   │               │ select + reasons  │                   │                    │                │
   │               │──────────────────────────────────────►│                    │                │
   │  recommendation + explanation chain                   │                    │                │
   │◄──────────────────────────────────────────────────────│                    │                │
   │ accept/dismiss│                   │                   │───────────────────►│                │
   │               │                   │                   │                    │ recommendation │
   │               │                   │                   │                    │────decision───►│
   │               │                   │                   │                    │                │
   │               │         (later) TwinUpdatePipeline applies Behaviour/Decision strategies    │
```

## 15.4 Mission generation from Decision Engine

```
Mission Service     Mission Intelligence     Decision Engine     Twin     Behaviour/Goals
      │                      │                     │               │            │
      │ generate daily       │                     │               │            │
      │─────────────────────►│ request actions     │               │            │
      │                      │────────────────────►│ read          │            │
      │                      │                     │──────────────►│            │
      │                      │                     │ feasibility   │───────────►│
      │                      │  ranked actions     │               │            │
      │                      │◄────────────────────│               │            │
      │  mission projection  │                     │               │            │
      │◄─────────────────────│                     │               │            │
```

---

# Appendix A — Capability Map (Epic 2)

| ID | Capability | Architectural deliverable |
|---|---|---|
| 2.1 | Student Digital Twin Domain | Immutable domain aggregate |
| 2.2 | Twin Update Pipeline | Registry orchestration |
| 2.3 | Knowledge Update Strategy | Knowledge structural evolution |
| 2.4 | Memory Update Strategy | Memory structural evolution |
| 2.5 | Behaviour Update Strategy | Behaviour evolution from evidence |
| 2.6 | Performance Update Strategy | Performance evolution from evidence |
| 2.7 | Readiness Aggregation | Factorable readiness derivation |
| 2.8 | Decision Engine | Highest-value next action reasoner |
| 2.9 | Explainable Recommendation Engine | Explanation chain packaging |
| 2.10 | Mission Generation Intelligence | Twin-driven adaptive missions |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | E2.0 — Educational Intelligence Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward |
| Supersedes | None (complements Twin + Evidence specs) |
| Next | Capability 2.5 — Behaviour Update Strategy (architecture → implementation) |

---

*End of Educational Intelligence Architecture.*
