# ADR-002: Educational Intelligence Architecture

**Status:** Accepted  
**Date:** July 2026  
**Deciders:** Kwalitec Engineering  
**Epic:** Epic 2 — Educational Intelligence  

**Upstream decisions / gates:**

| Artefact | Outcome |
|---|---|
| ADR-001 — Curriculum Hierarchy | Accepted |
| Recommendation Integrity Review | APPROVED WITH CONDITIONS |
| Mission Integrity Review | APPROVED WITH CONDITIONS |
| Epic 2 Completion Review | APPROVED WITH CONDITIONS |

**Governing specification:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)

---

## Context

Epic 1 established curriculum as syllabus truth: official structure, V1/V2 traversal, and planning foundations that answer *what the student needs to learn*.

Epic 2 answers a different question:

> What is the highest-value thing this student should do next?

That question cannot be answered safely by scattering mastery heuristics, readiness percentages, and next-action logic across Flask services. Professional exam preparation is high-stakes. Students must be able to trust that recommendations are evidence-backed, curriculum-weighted, and explainable — not engagement theatre or opaque scores invented inside route handlers.

Kwalitec therefore required a dedicated **Educational Intelligence** architecture: a framework-independent domain layer that owns learner state and educational reasoning, with product services consuming that authority rather than inventing competing educational models.

Embedding educational logic inside services had already produced the classic failure mode of study-planner products: multiple implicit “truths” (plan rows, mission completion, readiness %, recommendation heuristics) that diverge, cannot explain themselves, and treat activity as learning.

Epic 2 delivered the structural stack that realises this architecture:

- Student Digital Twin  
- Twin Update Pipeline  
- Knowledge, Memory, Behaviour, and Performance Update Strategies  
- Readiness Aggregation  
- Decision Engine  
- Recommendation Engine  
- Mission Intelligence  

Integrity reviews for Recommendation and Mission, and the Epic 2 Completion Review, are all **APPROVED WITH CONDITIONS**. The conditions concern product integration and dual authority with legacy services — not redesign of the Educational Intelligence model itself.

---

## Problem Statement

Legacy study-planner architectures optimise for *recording study* rather than *representing learning*. Their typical limitations include:

1. **Activity mistaken for learning.** Session time, mission ticks, and plan adherence are treated as proxies for mastery or exam readiness.
2. **No single learner model.** Mastery, retention, behaviour, and performance live as ad-hoc fields on plans, missions, or analytics caches — often contradictory.
3. **Write and read conflated.** The same service that suggests a next action silently mutates “mastery” or readiness without an evidence audit trail.
4. **Opaque recommendations.** Students (and engineers) cannot answer *why* a suggestion was made; reason codes and evidence lineage are absent.
5. **Planner-first product shape.** Week plans and daily missions become the source of educational truth instead of consequences of educational reasoning.
6. **Curriculum bypass.** Topic order, weights, or invented trees are reimplemented in planners and recommenders, breaking V1/V2 invariants.
7. **Non-deterministic or LLM-owned cores.** Generative or randomised selection undermines reproducibility and professional trust.
8. **Feature-first growth.** Dashboards, gamification, and engagement loops arrive before an honest model of what the student knows, remembers, and can perform under assessment.

These limitations are incompatible with Kwalitec’s mission: maximise probability of passing professional examinations through evidence-based educational guidance.

---

## Decision

### Adopt Educational Intelligence as the authoritative educational reasoning architecture

Kwalitec adopts a layered Educational Intelligence architecture in which **Learning Evidence** evolves a **Student Digital Twin**, from which **Readiness**, **Decision**, **Recommendation**, and **Mission** are derived as distinct, owned concerns:

```
Learning Evidence
        ↓
Student Digital Twin
        ↓
Readiness
        ↓
Decision
        ↓
Recommendation
        ↓
Mission
```

Curriculum Engine / `CurriculumService` remains the single source of truth for syllabus structure and weights. Educational Intelligence never invents a parallel syllabus.

### Layer ownership

| Layer | Owns | Does not own |
|---|---|---|
| **Learning Evidence** | Immutable, append-only history of learning events; the only legitimate input that may change Twin beliefs | Twin belief math; next-action selection; syllabus structure |
| **Student Digital Twin** | Authoritative educational state (Knowledge, Memory, Behaviour, Performance, Confidence, Decision State, optional Prediction snapshots); evolved only via Update Strategies on the Twin Update Pipeline | Plans, missions, HTTP, persistence, readiness composites, next-action selection |
| **Readiness** | Derived, factorable preparedness relative to Goals, Curriculum weights, and Twin domains | Raw evidence mutation; next-action selection; inventing topic order |
| **Decision** | Highest-value next-action selection; candidate set; reason codes; Decision State materialisation | Twin belief writes; mission packing; syllabus invention; LLM ownership of selection |
| **Recommendation** | Product packaging of a Decision (title, explanation chain, affordances, warrant posture) | Re-ranking; second Decision Engine; Twin mutation |
| **Mission** | Operationalisation of Decision(s) into attributable session tasks | WeekPlan policy; filler under leftover capacity; selecting or ranking actions; storing private mastery |

### Write path vs read path

**Write path (belief evolution):**

```
Learning Evidence → Twin Update Pipeline → Update Strategies → new Twin snapshot
```

Strategies (Knowledge, Memory, Behaviour, Performance; Confidence when separable) own domain evolution. The pipeline coordinates registration order; it does not embed educational algorithms.

**Read path (reasoning and product projection):**

```
Twin + Curriculum + Goals → Readiness Aggregation → Decision Engine
        → Recommendation packaging (optional)
        → Mission Intelligence (execution / projection)
```

Read-side components must never quietly rewrite Knowledge, Memory, Behaviour, or Performance. Accept/dismiss and mission completion become Learning Evidence (preference / Behaviour), not mastery grants.

### Position in application layering

```
Templates / JS
      ↓
Blueprints
      ↓
Services (orchestration, persistence bridges, product projections)
      ↓
Domain: Evidence + Twin + Strategies + Readiness + Decision + Recommendation + Mission
      ↓
Models + Curriculum Engine
      ↓
DB / JSON
```

Domain packages remain free of Flask, SQLAlchemy, and request globals. Legacy `ReadinessService`, `RecommendationService`, and planning/mission services may coexist during Stage A, but must not become permanent parallel Twin stores or hybrid “legacy % + Twin factor” averages.

---

## Architectural Principles

These principles bind Educational Intelligence work and subsequent product integration.

### 1. Single educational authority

The Student Digital Twin is the sole authoritative representation of learner educational state. Services consume Twin state; they do not invent competing mastery, retention, or readiness stores.

### 2. Explainability by construction

Every educational recommendation must answer *why* through a mandatory chain:

```
Curriculum → Learning Evidence → Twin factors → Readiness factors (when relevant)
        → Decision reason codes → Recommendation / Mission attribution
```

Opaque composites and post-hoc LLM stories that invent evidence are forbidden.

### 3. Structural before scoring

Domain ownership, immutability, evidence lineage, and write/read separation ship before rich belief engines (BKT, forgetting curves, numeric readiness weights). Structure first; calibrated scoring later, in the correct owners.

### 4. Read-side vs write-side separation

Update Strategies write. Readiness, Decision, Recommendation, and Mission read and project. Crossing that firewall breaks auditability and trust.

### 5. Deterministic reasoning core

Same Twin, Curriculum, and Goals inputs produce the same readiness factors and selected action on core paths. Random theatre and required network LLM calls are excluded from educational cores. Generative assistance may narrate; it must not own selection.

### 6. Framework-independent domain

Educational Intelligence lives in domain packages that do not import Flask, ORM, blueprints, or templates. Persistence and HTTP stay in services and blueprints.

### 7. Curriculum-first reasoning

Syllabus identities, order, and exam weights come from Curriculum Engine / `CurriculumService`. Twin domains reference curriculum identities. Decision and Readiness consume weights and order. V1 and V2 both remain first-class.

### 8. Progressive product integration

Domain Educational Intelligence may complete before product surfaces cut over. Coexistence is honest (named dual truth). Integration is additive: adapters and orchestration first; retire divergent authority later. Do not deepen legacy heuristics as Twin-first truth.

### 9. Educational Evidence Principle

Student state is derived from evidence. The platform avoids guessing. Cold-start and thin-warrant postures remain honest — never Mid/High theatre under sparse evidence. Recommendations are explainable from observable history.

### 10. Trust Before Features

Trustworthy educational reasoning precedes engagement features, dashboards-as-intelligence, gamification, and notification product work. Features that do not improve pass probability, decision quality, student modelling, or explainability should be challenged before implementation.

### 11. Premium is incremental

Premium product value is built by deepening evidence quality, Twin fidelity, readiness factorisation, and decision explainability — not by bolting opaque “AI” or parallel scorer layers onto a planner. Each increment must preserve authority boundaries and the explainability chain.

### Supporting invariants (from Epic 2)

- Knowledge ≠ Memory; Confidence ≠ mastery; Behaviour ≠ learning; Activity ≠ readiness; Completion ≠ mastery.  
- Plans and missions are consequences of intelligence, not the learner model.  
- Prefer additive immutable Twin snapshots over in-place mutation.  
- Architecture before implementation for each capability.

---

## Alternatives Considered

### Monolithic Recommendation Service

**Proposal:** One service owns scoring, readiness, next action, and mission generation.

**Rejected because:** Collapses ownership; conflates write and read; produces unmaintainable god services; destroys explainability and testability of individual educational concerns.

### Planner-first architecture

**Proposal:** Week plans and daily missions remain the educational source of truth; “intelligence” is plan regeneration heuristics.

**Rejected because:** Plans record commitments, not learning state. Planner-first models recreate activity-as-mastery and cannot answer readiness or highest-value next action from evidence-backed Twin domains.

### LLM-first architecture

**Proposal:** A language model selects next actions and invents rationales from chat context.

**Rejected because:** Non-deterministic cores, invented syllabus topics, unverifiable evidence, and loss of professional trust. LLMs may narrate Twin/Decision outputs later; they must not own educational selection.

### Traditional study planner

**Proposal:** Continue as a tracker of study time, checklists, and static schedules without a Digital Twin.

**Rejected because:** Incompatible with the product thesis. Tracking alone does not maximise pass probability or produce explainable, curriculum-weighted educational decisions.

### Embedding Educational Intelligence inside existing Flask services

**Proposal:** Extend `ReadinessService` / `RecommendationService` / `PlanningService` in place as the intelligence layer.

**Rejected because:** Framework coupling, divergent state, and hybrid averages with legacy heuristics. Epic 2 instead places authority in domain packages and treats service cutover as progressive integration (Epic 3), not as the design of educational reasoning.

---

## Consequences

### Positive

- **Clear educational ownership** from evidence through mission execution.  
- **Explainable next actions** grounded in curriculum, evidence, and Twin factors.  
- **Auditability** via append-only evidence, Twin snapshots, Decision State, and Decision Journal.  
- **Safe evolution** of belief math inside Update Strategies without rewriting product surfaces.  
- **Curriculum V1/V2 preservation** through context/lineage rather than Section-global assumptions.  
- **Deterministic, testable cores** free of black-box ownership.  
- **Honest cold-start behaviour** that does not fabricate preparedness theatre.  
- **Foundation for premium product** that deepens intelligence rather than planner cosmetics.

### Negative

- **Dual authority during Stage A.** Legacy readiness / recommendation / mission paths remain live until cutover; program risk if product claims Twin-first prematurely.  
- **Orchestration and persistence debt.** Evidence → pipeline bridges, Twin persistence, `CurriculumContext` builders, and Decision Journal loops remain product-integration work.  
- **Structural before calibrated beliefs.** Mastery/retention engines and Confidence separability are incomplete; educational maturity is high structurally, medium for calibrated belief content.  
- **Contributor cognitive load.** More packages and contracts than a monolithic recommender; mitigated by ADRs, capability architecture docs, and integrity reviews.

### Trade-offs

| Trade-off | Choice | Rationale |
|---|---|---|
| Speed of UI features vs trust | Trust / architecture first | High-stakes exams demand explainability |
| Rich scoring now vs structural domains first | Structure first | Avoid unmaintainable math before ownership is stable |
| Immediate cutover vs coexistence | Named Stage A dual truth | Preserve production behaviour; freeze legacy deepening |
| LLM convenience vs determinism | Deterministic core | Professional trust and reproducibility |
| Mission filler for engagement vs learning value | No filler under leftover capacity | Educational fidelity over theatre |

---

## Educational Impact

This architecture better supports professional exam success because it:

1. **Models learning, not study theatre** — Knowledge and Memory remain complementary; Behaviour never grants mastery; Performance remains a distinct assessed signal.  
2. **Weights effort by syllabus truth** — Decision and Readiness consume official exam weights and canonical order from Epic 1’s curriculum foundation.  
3. **Prioritises highest educational value under time scarcity** — Decision selects next action from Twin state and constraints, not from empty completion pressure.  
4. **Makes readiness factorable** — Students and coaches can see coverage, retention risk, assessment strength, pace, and time pressure instead of a single opaque percentage.  
5. **Closes the evidence loop** — Accept/dismiss and mission outcomes return as Learning Evidence, so future decisions improve from real behaviour without silent state hacks.  
6. **Earns trust** — Explainability by construction aligns with the Engineering Charter: students should never be asked to trust a black box for core next-action advice.

The result is a platform positioned to improve probability of passing in the shortest sustainable time — not merely to increase time spent in the application.

---

## Epic 3 Implications

**Epic 3 is Product Integration, not Educational Intelligence redesign.**

Epic 2 closes the domain Educational Intelligence stack (capabilities 2.1–2.10) under binding conditions. Epic 3 (and related Stage B/C integration milestones) must:

- Wire thin orchestration: Evidence capture → Pipeline → Twin; Curriculum context builders; Decision → Recommendation → Mission → persistence.  
- Cut over product surfaces from legacy readiness / recommendation / mission authorities without hybrid averages.  
- Preserve write/read firewall, Decision as sole selection authority, warrant honesty, and Curriculum V1/V2 helpers.  
- Record Decision Journal and completion/failure evidence only through Learning Evidence → Strategies.  
- Deepen belief/Confidence enrichment *inside* existing ownership boundaries — not by inventing a second intelligence architecture.

Epic 3 must **not**:

- Redesign the Evidence → Twin → Readiness → Decision → Recommendation → Mission chain.  
- Move educational selection into Recommendation, Mission, or LLM-owned services.  
- Treat structural Twin postures as finished calibrated preparedness scores without warrant discipline.

Residual conditions from Epic 2 Completion Review remain program obligations for integration, not grounds to reopen this ADR’s architectural decision.

---

## References

| Document | Role |
|---|---|
| [`ADR-001-Curriculum-Hierarchy.md`](ADR-001-Curriculum-Hierarchy.md) | Curriculum as syllabus truth; V1/V2 foundation for Educational Intelligence |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Canonical Educational Intelligence Architecture specification |
| [`docs/reviews/EPIC_2_COMPLETION_REVIEW.md`](../reviews/EPIC_2_COMPLETION_REVIEW.md) | Epic 2 Completion Review — APPROVED WITH CONDITIONS |
| [`docs/reviews/RECOMMENDATION_INTEGRITY_REVIEW.md`](../reviews/RECOMMENDATION_INTEGRITY_REVIEW.md) | Recommendation Integrity Review — APPROVED WITH CONDITIONS |
| [`docs/reviews/MISSION_INTEGRITY_REVIEW.md`](../reviews/MISSION_INTEGRITY_REVIEW.md) | Mission Integrity Review — APPROVED WITH CONDITIONS |
| [`docs/reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`](../reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md) | Midpoint architecture gate |
| [`docs/reviews/EDUCATIONAL_REASONING_REVIEW.md`](../reviews/EDUCATIONAL_REASONING_REVIEW.md) | Educational Reasoning Review |
| [`docs/reviews/READINESS_ARCHITECTURE_REVIEW.md`](../reviews/READINESS_ARCHITECTURE_REVIEW.md) | Readiness Architecture Review |
| [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md) | Epic 2 kickoff and guiding question |
| [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md) | Engineering principles and trust mandate |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Twin companion specification |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Learning Evidence companion specification |
| [`ARCHITECTURE.md`](../../ARCHITECTURE.md) | Application layering and curriculum invariants |

---

## Document control

| Field | Value |
|---|---|
| Nature | Architecture Decision Record only |
| Code impact | None |
| Migration impact | None |
| Implementation | None |
| Supersedes | None (records the decision to adopt the Educational Intelligence Architecture) |

---

*End of ADR-002.*
