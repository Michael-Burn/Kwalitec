# Educational State Model

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS001 — Educational State Model  
**Classification:** Constitutional specification — what constitutional educational state may exist and what each state represents  
**Status:** APPROVED — governing for educational state (constitutional context)  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **what constitutional educational state may exist**, and **what each recognised state represents**.

It answers *what educational state must optimise*, *which constitutional context states are recognised*, *what educational state may and must not do*, and *how educational state is explained* — without creating educational meaning, altering constitutional authority, executing workflows, or minting recommendations.

It does **not** implement Runtime A, state machines, algorithms, scheduling, databases, services, UI, or analytics.

> **Educational state represents constitutional educational context.  
> It does not create educational meaning, alter authority, or execute workflows.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001) — especially Article IV (meaning-bearing educational states) and Article III (truth / claim honesty)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
7. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — **mutation rights for Article IV educational states**; this Model owns **constitutional context representation**, not write paths
8. Programme VI constitutional corpora (Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach) — **educational meaning authorities; this Model never redefines them**
9. [`../workflows/`](../workflows/) and siblings — Educational Workflow Engine (WS1) — **orchestration may observe and reference this Model’s context; this Model never invents stages or executes flows**
10. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map; this Model never transfers domains**
11. [`../conflict_resolution/`](../conflict_resolution/) — Conflict Resolution Framework (WS2 / MS002) — **disposition among valid recommendations; this Model may represent conflict-await context, never resolve conflicts**
12. [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003)
13. [`../recommendations/`](../recommendations/) and siblings — Educational Recommendation Engine (WS3) — **recommendations and sets may reference this Model’s context; this Model never creates tips or assembles sets**

Related (non-authoritative for Programme VII educational-state *context* law):

- Constitution Article IV Educational State Model — defines **meaning-bearing** educational concepts (Study Progress, Evidence, Mission, …); **orthogonal** to this corpus’s constitutional *context* states
- [`../../educational/EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`](../../educational/EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md) — lifecycle / ownership architecture for Article IV–class states
- [`../../version2/STATE_MACHINE.md`](../../version2/STATE_MACHINE.md) — Version 2 operational state machines; does not replace this constitutional context law
- Product analytics “Educational State evolution” metrics — observational projections; never redefine this Model

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_STATE_MODEL.md`](EDUCATIONAL_STATE_MODEL.md) | Constitutional overview: what educational state is, responsibilities, integrity, stack position |
| [`STATE_OBJECTIVES.md`](STATE_OBJECTIVES.md) | Constitutional objectives educational state must serve |
| [`STATE_TYPES.md`](STATE_TYPES.md) | Recognised constitutional educational states — meaning, entry/exit, observers, prohibited interpretations |
| [`STATE_BOUNDARIES.md`](STATE_BOUNDARIES.md) | What educational state may represent and must never invent or execute |
| [`STATE_EXPLAINABILITY.md`](STATE_EXPLAINABILITY.md) | How educational state is explained to students and developers |

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised educational guidance |
| **Constitution Article IV / EIP-001** | Define *meaning-bearing educational states* and *who may mutate them* |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners — *observes* constitutional context |
| **Programme VII / WS2 — Authority · Conflict · Permission** | Ownership, disposition, and permission speech — *may consume* context without owning it |
| **Programme VII / WS3 — Recommendations · Assembly · Set Explainability** | Communicate and organise lawful guidance — *may reference* context without inventing it |
| **Programme VII / WS4 / MS001 — this corpus** | Define *what constitutional educational state (context) may exist* and what each state represents |

```
Educational Constitution / EIP
        │  educational truth, Article IV meaning-bearing states, mutation rights
        ▼
Programme VI meaning authorities
        │  Master Planner · Daily · Learning · Recovery · Revision · Exam
        ▼
Educational State Model (this milestone)
        │  represents constitutional educational *context*
        │  does not invent meaning, tips, ownership, or workflow execution
        ▼
Educational Workflow Engine (WS1)
        │  observes context when sequencing / handing off / concluding
        ▼
Authority · Conflict · Permission (WS2)
        │  may consume context; never transferred by state labels
        ▼
Recommendations · Assembly · Set Explainability (WS3)
        │  may reference context when packaging lawful guidance
        ▼
Authorised educational outcome
        │  explainable: current context · why it exists · supporting warrants · consumers
```

Programme VI settles *educational meaning*.  
Constitution Article IV / EIP settle *meaning-bearing educational states* and *mutation rights*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 settles *decision ownership, conflict disposition, and permission speech*.  
Programme VII Workstream 3 settles *recommendation artefacts and sets*.  
Programme VII Workstream 4 / MS001 settles *constitutional educational context representation*.

## Architectural requirement

Educational state is a **constitutional representation of context**. It must **never** be interpreted as:

| Forbidden reading | Why |
|-------------------|-----|
| Educational success | Success is not a constitutional context label |
| Learner mastery / Estimated Mastery | EIP-006 / Twin / Evidence authorities own claim types |
| Workflow completion | WS1 Completion Model owns orchestration fulfilment |
| Study Progress / coverage truth | Article IV + EIP-001 own meaning-bearing coverage states |
| A licence to create tips or rewrite ownership | WS3 / WS2 remain owners of those concerns |

| Lawful | Unlawful |
|--------|----------|
| Represent which constitutional educational context is live | Create recommendations or educational meaning |
| Support orchestration by naming observable context | Replace workflow stages, transitions, or completion |
| Support recommendation assembly as a reference | Transfer or invent authority domains |
| Support explainability of “where we are educationally” | Redefine Educational Evidence or Twin estimates |
| Preserve continuity of context narration (EIP-005) | Execute educational actions or mutate Article IV states |

If a proposed behaviour would require inventing context types, silent mastery claims, or workflow execution by state label, **amend this Model first** — or refuse. Educational state never gains educational authority by product convenience.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **Constitution Article IV / EIP-001** | What meaning-bearing educational states are and who may write them | Cross-cutting constitutional *context* catalogue (this Model) |
| **Programme VI coach / planner models** | What each educational question *means* | Which constitutional context posture is currently represented (this Model) |
| **WS1 Workflow Model / Transitions / Completion** | How flow is sequenced, moved, and concluded | What context *is* independently of a running workflow (this Model) |
| **WS2 Authority / Conflict / Permission** | Who owns decisions; which valid tip is acted upon; why permitted | Context representation catalogue (this Model) |
| **WS3 Recommendations / Assembly / Set Explainability** | What tips and sets are and how they are packaged / explained | Context that those artefacts may *reference* (this Model) |
| **This Educational State Model** | What constitutional educational context may exist; objectives; types; boundaries; explainability | Runtime A, state machines, algorithms, Article IV mutation, workflow execution, tip invention |

**Binding distinction:** Article IV states are *educational meaning objects*. This Model’s states are *constitutional context postures*. Neither may be collapsed into the other by naming convenience.

## Downstream (MS002)

*When* one constitutional educational context may lawfully transition into another — without redefining meaning, transferring authority, creating tips, or executing workflows — is governed by [`../state_transitions/`](../state_transitions/) (Educational State Transition Framework). MS001 publishes EST types and entry/exit law; MS002 publishes CST transition types, conditions, boundaries, and transition explainability.

## Downstream (MS003)

*How* constitutional educational context and contextual progression are explained — unifying static-context speech (ESQ) and transition-moment speech (STQ) under one explanation contract — is governed by [`../state_explainability/`](../state_explainability/) (Educational State Explainability). MS001 / MS002 remain authoritative for EST/CST law; MS003 binds principles, components, boundaries, and patterns without amending those catalogues.

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- State machines, transition algorithms, or schedulers in code
- Database models, schemas, or ORM entities
- UI components, navigation, or notifications
- Analytics pipelines or telemetry schemas
- Workflow execution engines, sagas, or job queues
- Recommendation creation, ranking, or assembly engines
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning (owned by those corpora)
- Amendments to Article IV definitions or EIP-001 mutation rows by state-context fiat
- Named contextual succession catalogue (owned by MS002)

## How to use this corpus

1. Read `EDUCATIONAL_STATE_MODEL.md` first.
2. Treat objectives in `STATE_OBJECTIVES.md` as binding targets for every educational-state surface.
3. Classify observed context under `STATE_TYPES.md` — entry, exit, observers, and prohibited interpretations.
4. Enforce limits in `STATE_BOUNDARIES.md` before any proposed state behaviour.
5. Require explainability contracts from `STATE_EXPLAINABILITY.md` before student- or developer-facing state narration.
6. When meaning-bearing educational states or writers are at stake, consult Article IV / EIP-001 — do not conflate context with mutation.
7. When orchestration needs stage order, consult [`../workflows/`](../workflows/). When ownership is unclear, consult [`../authority/`](../authority/). When tips are at stake, consult [`../recommendations/`](../recommendations/).
8. When context may succeed from one EST type to another, consult [`../state_transitions/`](../state_transitions/).
9. When narrating why a learner is in a context and how that context evolved, consult [`../state_explainability/`](../state_explainability/) — keep consistency with `STATE_EXPLAINABILITY.md`.
10. Do not implement behaviours that contradict this corpus without amending it first.
