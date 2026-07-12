# Capability 3.2.1 — Educational Orchestration Analysis

**Status:** Architecture analysis — analysis only  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.2 Integration (Educational Orchestration analysis preceding architecture and implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Upstream:** Epic 2 Educational Intelligence (v0.5.0) complete; Epic 2 Completion Review and Architecture Guardian Review — APPROVED WITH CONDITIONS  
**Scope:** How the Flask application should orchestrate completed Educational Intelligence without introducing new educational authority — **no implementation, services, code, schemas, migrations, or UI**

---

## Document purpose

Epic 2 delivered a framework-independent Educational Intelligence platform:

```
Learning Evidence → Twin → Readiness → Decision → Recommendation → Mission
```

That stack answers *what the highest-value next action should be*. It does not yet answer *how the product application wires those domains into one student-facing path*.

This milestone answers what **Educational Orchestration** is for Epic 3 Capability 3.2: the thin coordination layer that sequences completed educational domains into product outputs — without becoming a second reasoner.

**Governing principle (binding):**

> **The orchestrator coordinates. It never reasons.**

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- Stage B/C cutover mechanics beyond orchestration boundaries  
- UI templates, copy systems, or premium experience design  
- Hybrid legacy + Twin educational formulas  

---

# 1. Executive Summary

## Why orchestration exists

Educational Intelligence is complete as a **platform**. Version 1.0 needs a **product path**: one ordered call chain from student identity and session context to dashboard-ready outputs that students can trust.

Without orchestration:

- Blueprints would call domain engines directly and invent ordering, error handling, and context assembly.  
- Multiple product surfaces would wire Twin → Readiness → Decision inconsistently.  
- Legacy `ReadinessService` / `RecommendationService` / planning mission paths would remain de facto product authority by convenience.  
- Explainability would break because lineage would not travel as a single composed result.

Orchestration exists to **wire**, not to **think**.

It:

1. Assembles the inputs domains already require (Student, CurriculumContext, Twin, Goals, Constraints, product context).  
2. Invokes Educational Intelligence domains in the only lawful order.  
3. Composes their outputs into the closed product set Version 1.0 needs.  
4. Propagates failures honestly instead of inventing Mid/High theatre when a step cannot warrant a claim.

It does **not**:

- Select next actions (Decision owns that).  
- Aggregate preparedness (Readiness owns that).  
- Package or narrate recommendations (Recommendation owns that).  
- Compose mission tasks (Mission Intelligence owns that).  
- Mutate Twin beliefs (Update Strategies on the Twin Update Pipeline own that).  
- Invent syllabus structure (Curriculum Engine / `CurriculumService` owns that).

Epic 3 replaces **product authority** through cutover and wiring. It does not redesign Educational Intelligence (ADR-002). Orchestration is the first Integration artefact that makes that statement operational.

```
Platform (v0.5.0 domains)
        ↓
Educational Orchestration   ← coordinates only
        ↓
Product surfaces (dashboard, recommendation, mission, explainability)
```

---

# 2. Responsibilities

## 2.1 Own

| Responsibility | Meaning |
|---|---|
| **Coordination** | Invoke the correct Educational Intelligence domains for a product request; do not skip, reorder, or short-circuit educational stages for convenience. |
| **Composition** | Assemble domain outputs into a single product-facing result set (view model + recommendation + mission + readiness projection + explainability payload) without inventing new educational meaning. |
| **Dependency ordering** | Enforce the lawful pipeline order so later stages never run without the inputs earlier stages own. |
| **Error propagation** | Surface domain failures, thin-warrant postures, and cold-start honesty upward; never replace a failed or unknown educational result with a fabricated confident substitute. |
| **Context assembly** | Build and pass the shared context objects domains already contract for (CurriculumContext, Goals, Constraints, Twin snapshot load, product/session facts) using canonical Curriculum helpers — V1 and V2 safe. |

Orchestration is a **conductor**. Domains remain the musicians.

## 2.2 Never own

| Forbidden ownership | Why |
|---|---|
| **Educational reasoning** | Reasoning lives in Twin strategies, Readiness, and Decision. Orchestration that “helps” by scoring or choosing becomes a parallel intelligence. |
| **Readiness** | Preparedness factors and warrant belong to Readiness Aggregation. Orchestration may request and forward readiness; it must not recompute, average, or coerce unknown into Mid/High. |
| **Decision** | Next-action selection, candidate sets, and reason codes belong solely to Decision Engine. Orchestration must not re-rank, filter by engagement heuristics, or substitute legacy recommendation lists. |
| **Recommendation** | Packaging, titles, explanation affordances, and warrant-bound narration belong to Recommendation Engine. Orchestration may request packaging; it must not invent student-facing educational claims. |
| **Mission logic** | Task composition, Decision-binding, and feasibility-shaped execution belong to Mission Intelligence. Orchestration must not invent filler tasks, private priority scores, or a second day plan. |

### Binding vocabulary

| Concept | Owns | Relation to orchestration |
|---|---|---|
| **Educational Orchestration** | Order, wiring, composition, errors, context | Product Integration concern |
| **Curriculum / CurriculumContext** | Syllabus identities, order, weights | Assembled by orchestration via canonical helpers; never invented |
| **Twin** | Authoritative learner educational state | Loaded / passed; never mutated on the read path |
| **Readiness** | Derived preparedness judgement | Called; results forwarded |
| **Decision** | Highest-value next action | Called; sole selection authority |
| **Recommendation** | Decision packaging | Called; projection only |
| **Mission** | Decision operationalisation | Called; execution / projection only |
| **Legacy readiness / recommendation / mission services** | Stage A product peers | Must not be treated as Twin-first authority inside orchestration |

Governing restatement:

> **Orchestration never answers educational questions. It only ensures the owners of those questions are asked in the right order, with the right inputs, and that their answers reach the product intact.**

---

# 3. Inputs

Orchestration assembles inputs. It does not invent educational content for them.

| Input | Role in orchestration | Boundary |
|---|---|---|
| **Student** | Identity and ownership scope for the request (who is studying; whose Twin, goals, and missions apply). | Auth and ownership checks remain blueprint / security concerns; orchestration receives an already-authorised student context, never other users’ state. |
| **Curriculum** | Official syllabus structure and weights for the student’s target sitting. | Built only through Curriculum Engine / `CurriculumService` helpers into a **CurriculumContext**. Orchestration must not invent topics, reorder syllabus privately, or treat plan rows as curriculum truth. V1 (flat) and V2 (hierarchical) both remain first-class. |
| **Goals** | Sitting target, remaining time, capacity and study intent that Readiness and Decision already consume. | Forwarded as Goals contracts domains expect. Orchestration does not invent exam dates, pass targets, or capacity policy. |
| **Twin** | Authoritative educational state snapshot for the read path. | Loaded (or obtained from the lawful write-path snapshot) and passed read-only into Readiness / Decision. Orchestration does not run belief math or write Twin domains on the product read path. |
| **Constraints** | Feasibility and session bounds (time available, sustainability / Behaviour-aware limits, product window). | Shape *how much* can be asked of Mission / session composition; never invent *what* is educationally valuable. |
| **Product context** | Surface intent and session facts needed for composition (e.g. dashboard vs mission path, locale/copy channel, Stage B/C cutover mode if named). | Product metadata only. Must never become a back door for educational selection, hybrid legacy averages, or UI-driven Twin mutation. |

### Input assembly principle

```
Authorised Student
      + Curriculum helpers → CurriculumContext
      + Goals
      + Twin snapshot (read)
      + Constraints
      + Product context
            ↓
     Orchestration entry
```

Missing or thin inputs produce honest downstream postures (cold-start, low warrant, `not_yet_knowable`) — not orchestrator-fabricated Mid/High readiness or motivational next actions.

---

# 4. Outputs

Orchestration returns a **closed product set**. Nothing more enters Version 1.0 educational authority through this path.

| Output | Meaning | Source of truth |
|---|---|---|
| **Dashboard View Model** | Calm product projection: what to show first (next action, today’s work, honest status) without becoming a second intelligence layer. | Composed from Recommendation, Mission, Readiness posture, and Explainability — not from private orchestrator scores. |
| **Recommendation** | Attributable packaging of the Decision (title, affordances, warrant-bound explanation hooks). | Recommendation Engine projecting Decision. |
| **Mission** | Today’s / this session’s attributable task set. | Mission Intelligence operationalising Decision (optionally with Recommendation language hooks). |
| **Readiness** | Factorable preparedness posture and warrant as the product may display. | Readiness Aggregation; forwarded, never recomputed by orchestration. |
| **Explainability** | Chain-supported reason codes and lineage citations so *why* remains answerable. | Carried from Decision lineage (and readiness citations when Decision cites readiness); orchestration preserves and surfaces — it does not invent post-hoc stories. |

### Explicit non-outputs

Orchestration must **not** produce as educational authority:

- Legacy overall readiness percentages presented as Twin-first truth  
- Heuristic recommendation lists that disagree with Decision  
- Filler mission tasks under leftover capacity  
- Hybrid “legacy % + Twin factor” averages  
- Direct mastery / readiness writes from accept, dismiss, or completion  
- Opaque composites or LLM-owned selection results  
- Extra educational artefacts beyond the five outputs above (analytics theatre, streak authority, competing next-action panels)

> **Nothing more.** If a surface needs a sixth educational claim, that is a domain or product-scope question — not an orchestration extension.

---

# 5. Flow

The lawful product read path for Educational Orchestration is:

```
Student
   ↓
CurriculumContext
   ↓
Twin
   ↓
Readiness
   ↓
Decision
   ↓
Recommendation
   ↓
Mission
   ↓
Dashboard
```

### Stage meanings

| Stage | Orchestration action | Domain ownership |
|---|---|---|
| **Student** | Accept authorised student / ownership scope. | Identity; not educational reasoning |
| **CurriculumContext** | Build syllabus context via canonical Curriculum helpers (V1/V2 safe). | Curriculum Engine / `CurriculumService` |
| **Twin** | Load authoritative snapshot for the read path. | Twin aggregate (beliefs owned by Update Strategies on write path) |
| **Readiness** | Invoke Readiness Aggregation with Twin + Curriculum + Goals. | Readiness Aggregation |
| **Decision** | Invoke Decision Engine with Twin, Curriculum, Goals, Readiness, Constraints. | Decision Engine — sole next-action selection |
| **Recommendation** | Invoke Recommendation packaging for the selected Decision. | Recommendation Engine — projection only |
| **Mission** | Invoke Mission Intelligence to operationalise Decision(s) under Constraints. | Mission Intelligence — execution / projection only |
| **Dashboard** | Compose Dashboard View Model + Explainability from the above. | Product projection; no new educational math |

### Flow invariants

1. **No skipping Decision.** Recommendation and Mission never become selection authorities.  
2. **No Twin mutation on this path.** Outcomes that change beliefs become Learning Evidence on the write path (Epic 3.3), not orchestrator side effects during dashboard composition.  
3. **No legacy short-circuit.** Stage A peers may exist during cutover but must not be invoked as Twin-first truth inside this flow.  
4. **Order is educational law.** Parallel calls that invent a second readiness or decision result are forbidden. Caching may reuse identical inputs; it must not invent alternate educational answers.  
5. **Explainability travels with the chain.** Stripping reason codes or warrant to “simplify” the dashboard is an orchestration failure.

### Relation to the student day

Orchestration’s read path feeds the Version 1.0 morning experience (open → recommendation → mission). Study outcomes then enter Evidence → Twin for tomorrow. That write loop is sibling Integration work (Learning Evidence stream); it is not an excuse for the read-path orchestrator to become a belief engine.

---

# 6. Layering

```
Flask
   ↓
Application
   ↓
Orchestrator
   ↓
Educational Intelligence Domains
```

| Layer | Responsibility | Must not |
|---|---|---|
| **Flask** | HTTP, auth decorators, forms, templates, redirects, security headers. | Contain readiness math, Decision selection, mission composition, or Twin belief updates. |
| **Application** | Product use-cases and persistence bridges (load Twin, record journal later, map domain Mission to product persistence when authorised). | Become a second Educational Intelligence stack or hybrid scorer. |
| **Orchestrator** | Dependency ordering, context assembly, composition of the five outputs, error propagation. | Own educational reasoning, readiness, decision, recommendation, or mission logic. |
| **Educational Intelligence Domains** | Evidence, Twin (+ strategies), Readiness, Decision, Recommendation, Mission — framework-independent. | Import Flask, request globals, or ORM as domain authority. |

### Layering consequences

- Blueprints call application / orchestration entry points; they do not call Decision Engine with ad-hoc arguments invented in routes.  
- Domain packages remain free of Flask and SQLAlchemy (ADR-002). Persistence adapters sit in Application, not inside `app/domain/`.  
- Curriculum truth remains in Curriculum Engine / `CurriculumService`; orchestration only builds CurriculumContext.  
- Legacy services sit beside this stack during Stage A/B; they are not layers *inside* the Twin-first orchestrator.

This layering preserves:

```
Templates / JS → Blueprints → Services (orchestration / persistence) → Domain EI → Models + Curriculum → DB / JSON
```

---

# 7. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **God Service** | One orchestrator accumulates scoring, selection, packaging, mission packing, and persistence until it recreates the monolithic Recommendation Service ADR-002 rejected. | Keep orchestrator thin: coordinate and compose only; refuse new educational algorithms in orchestration milestones. |
| **Business logic leakage** | Routes or application helpers quietly re-rank Decisions, coerce readiness, or invent mission filler “for UX.” | Enforce layering reviews; product copy and UX consume domain outputs — they do not override them. |
| **Duplicate reasoning** | Orchestration reimplements readiness factors or decision heuristics “temporarily,” or averages legacy % with Twin factors. | Forbidden hybrid truth; Stage B adapters must name dual authority honestly; Stage C retires legacy as product educational authority. |
| **Slow orchestration** | Sequential over-fetching, repeated Twin loads, or unnecessary full-pipeline work on every partial UI refresh makes the calm daily path feel heavy — a trust issue. | Compose once per product request; reuse snapshots for identical inputs; optimise wiring without collapsing domain boundaries or skipping Decision. |
| **Parallel educational truth** | Dashboard uses Twin-first Decision while missions or progress still use Stage A planning / readiness %; students see conflicting “today” stories. | Orchestration is useless unless cutover binds all Version 1.0 educational surfaces to the same chain; dual truth must be named and time-boxed, never marketed as Twin-first Version 1.0. |

### Risk restatement

The primary danger is not missing a feature. It is **orchestration that starts reasoning** — or product surfaces that bypass orchestration and recreate parallel truth. Either failure reintroduces the study-planner pathology Epic 2 was built to end.

---

# 8. Recommendations

How Educational Orchestration should proceed after this analysis:

1. **Treat this document as analysis law for Capability 3.2.1** — orchestration coordinates; it never reasons. Do not reopen ADR-002’s educational chain.  
2. **Proceed Analysis → Architecture → Implementation → Review** (Engineering Charter). Next artefact is an orchestration *architecture* note: contracts, boundaries, cutover modes — still without domain redesign.  
3. **Define a single product read-path entry** that implements the Student → … → Dashboard flow before any Twin-first UI claims.  
4. **Ship CurriculumContext assembly via canonical Curriculum helpers first** so V1/V2 safety is proven at the orchestration boundary.  
5. **Wire Decision → Recommendation → Mission as one composed path** before live consumers; never expose Recommendation or Mission as selection authorities.  
6. **Preserve write/read firewall** — orchestration on the dashboard path must not mutate Twin; completion / accept / dismiss become Evidence in Capability 3.3 workstreams.  
7. **Freeze legacy heuristic deepening** as Twin-first truth; plan Stage B named dual-truth adapters and Stage C single product authority without hybrid averages.  
8. **Limit outputs to the five product artefacts** (Dashboard View Model, Recommendation, Mission, Readiness, Explainability). Reject “just one more” educational side channel.  
9. **Design for honest error and cold-start propagation** so thin warrant survives into product language.  
10. **Guard against God Service** in architecture review: if a proposed orchestrator method selects, scores, or invents tasks, it is out of scope.  
11. **Measure perceived latency on the daily path** as a trust concern once implementation begins — optimise composition, not by collapsing domains.  
12. **STOP.** This milestone is analysis only. No services. No code. No implementation until an explicit architecture / implementation milestone authorises them.

---

# References

- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md)  
- [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
- [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
- [`CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.2.1 complete as analysis only.
