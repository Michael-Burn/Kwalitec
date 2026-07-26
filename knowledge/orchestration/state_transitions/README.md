# Educational State Transition Framework

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS002 — Educational State Transition Framework  
**Classification:** Constitutional specification — when constitutional educational context may lawfully transition  
**Status:** APPROVED — governing for educational state (contextual) transitions  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **when one constitutional educational context may lawfully transition into another**.

It answers *when contextual succession is lawful*, *which transition kinds exist*, *what conditions permit each transition*, *what transitions may and may not do*, and *how contextual transitions are explained*.

It does **not** implement Runtime A, state machines, algorithms, scheduling, databases, services, UI, or analytics.

> **State transitions concern contextual representation only.  
> They do not redefine educational meaning, execute workflows, transfer authority, or generate recommendations.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001) — especially Article IV (meaning-bearing educational states; orthogonal) and Article III (truth / claim honesty)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
7. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — **mutation rights for Article IV educational states**; this Framework owns **contextual succession law**, not write paths
8. [`../state/`](../state/) — Educational State Model (WS4 / MS001) — **what EST types exist; this Framework defines when they may succeed**
9. Programme VI constitutional corpora (Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach) — **educational meaning authorities; transitions never redefine them**
10. [`../workflows/`](../workflows/), [`../workflow_transitions/`](../workflow_transitions/), [`../workflow_completion/`](../workflow_completion/) — Educational Workflow Engine (WS1) — **orchestration may lawfully progress and be referenced as condition evidence; this Framework never executes flows or invents stages**
11. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map; transitions never transfer domains**
12. [`../conflict_resolution/`](../conflict_resolution/) — Conflict Resolution Framework (WS2 / MS002) — **disposition among valid recommendations; transitions may enter/exit conflict-await context, never resolve conflicts**
13. [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003)
14. [`../recommendations/`](../recommendations/) and siblings — Educational Recommendation Engine (WS3) — **recommendations may reference post-transition context; transitions never create tips or assemble sets**

Related (non-authoritative for Programme VII educational-state *transition* law):

- Constitution Article IV Educational State Model — **meaning-bearing** educational concepts; orthogonal to EST context succession
- [`../../educational/EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`](../../educational/EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md) — lifecycle / ownership architecture for Article IV–class states
- [`../../version2/education/EDUCATIONAL_STATE_TRANSITIONS.md`](../../version2/education/EDUCATIONAL_STATE_TRANSITIONS.md) — Version 2 educational transition notes; does not replace this constitutional context-transition law
- [`../../version2/STATE_MACHINE.md`](../../version2/STATE_MACHINE.md) — Version 2 operational state machines; does not replace this Framework
- Product analytics “Educational State evolution” metrics — observational projections; never redefine this Framework

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_STATE_TRANSITION_FRAMEWORK.md`](EDUCATIONAL_STATE_TRANSITION_FRAMEWORK.md) | Constitutional overview: what contextual transitions are, responsibilities, integrity, stack position |
| [`TRANSITION_TYPES.md`](TRANSITION_TYPES.md) | Recognised constitutional state transition types — origin, destination, purpose, prohibited interpretations |
| [`TRANSITION_CONDITIONS.md`](TRANSITION_CONDITIONS.md) | Constitutional conditions that permit each contextual transition |
| [`TRANSITION_BOUNDARIES.md`](TRANSITION_BOUNDARIES.md) | What contextual transitions may update and must never invent or execute |
| [`TRANSITION_EXPLAINABILITY.md`](TRANSITION_EXPLAINABILITY.md) | How contextual state transitions are explained to students and developers |

## Relationship to MS001

| Horizon | Job |
|---------|-----|
| **MS001 — Educational State Model** | Define *what constitutional educational context may exist* and *what each EST type represents* |
| **MS002 — this corpus** | Define *when* one constitutional context may lawfully transition into another |

```
MS001 EST types (EST-01…EST-12)
        │  succession governed by
        ▼
MS002 transitions (CST-xx)
        │  conditions / boundaries / explainability
        ▼
Programme VI meaning · WS1 flow · WS2 ownership · WS3 tips remain intact
```

MS001 without MS002 risks treating context catalogues as ornamental.  
MS002 without MS001 risks inventing movement without published context types, entry/exit law, or non-claim prohibitions.

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised educational guidance |
| **Constitution Article IV / EIP-001** | Define *meaning-bearing educational states* and *who may mutate them* |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners — *may supply lawful progression facts* consumed as transition conditions |
| **Programme VII / WS2 — Authority · Conflict · Permission** | Ownership, disposition, and permission speech — *may supply authority / disposition facts*; ownership never moved by CST labels |
| **Programme VII / WS3 — Recommendations · Assembly · Set Explainability** | Communicate and organise lawful guidance — *may reference* post-transition context without inventing it |
| **Programme VII / WS4 / MS001 — Educational State Model** | Define *what constitutional educational context may exist* |
| **Programme VII / WS4 / MS002 — this corpus** | Define *when constitutional educational context may lawfully transition* |

```
Educational Constitution / EIP
        │  educational truth, Article IV meaning-bearing states, mutation rights
        ▼
Programme VI meaning authorities
        │  Master Planner · Daily · Learning · Recovery · Revision · Exam
        ▼
Educational State Model (WS4 / MS001)
        │  publishes EST-01…EST-12 context postures
        ▼
Educational State Transition Framework (this milestone)
        │  publishes CST-xx contextual succession law
        │  updates representation only — never meaning, authority, tips, or workflow execution
        ▼
WS1 Workflow · WS2 Authority/Conflict · WS3 Recommendations
        │  may observe / reference post-transition context
        ▼
Authorised educational outcome
        │  explainable: why context moved · warrants · rules · continuity
```

Programme VI settles *educational meaning*.  
Constitution Article IV / EIP settle *meaning-bearing educational states* and *mutation rights*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 settles *decision ownership, conflict disposition, and permission speech*.  
Programme VII Workstream 3 settles *recommendation artefacts and sets*.  
Programme VII Workstream 4 / MS001 settles *constitutional educational context representation*.  
Programme VII Workstream 4 / MS002 settles *lawful contextual succession among those representations*.

## Architectural requirement

Contextual state transitions update **only the constitutional representation of context**. They must **never** be interpreted as:

| Forbidden reading | Why |
|-------------------|-----|
| Educational success | Success is not a contextual succession meaning |
| Learner mastery / Estimated Mastery | EIP-006 / Twin / Evidence authorities own claim types |
| Workflow completion | WS1 Completion Model owns orchestration fulfilment |
| Authority transfer | WS2 owns the ownership map; CST labels never move domains |
| Recommendation creation | WS3 / Programme VI own tips; succession never mints guidance |
| Workflow execution | WS1 owns stage movement and completion; CST never runs flows |
| Study Progress / coverage truth | Article IV + EIP-001 own meaning-bearing coverage states |

| Lawful | Unlawful |
|--------|----------|
| Update which EST-xx posture is primary (or parallel-read) | Redefine Programme VI educational meaning |
| Reference lawful workflow progression / completion as condition evidence | Execute workflows or invent WT/S stage movement |
| Preserve contextual continuity across succession | Imply learner success or mastery from the move |
| Cite published constitutional rules that permitted the move | Modify authority ownership via transition labels |
| Explain why context moved and how history was preserved | Create recommendations or assemble tip sets |

If a proposed behaviour would require inventing context types, silent mastery claims, authority transfer, tip minting, or workflow execution by transition label, **amend this Framework first** — or refuse. Contextual transitions never gain educational authority by product convenience.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **WS4 / MS001 Educational State Model** | What EST types exist; entry/exit for types; non-claim prohibitions | *When* succession between types is a named transition act (this Framework) |
| **WS1 Workflow Transitions / Completion** | When workflows move stages / when orchestration is fulfilled | When *context representation* succeeds (this Framework) |
| **WS2 Authority / Conflict** | Who owns decisions; which tip is acted upon | Context succession catalogue (this Framework) |
| **WS3 Recommendations / Assembly** | What tips and sets are | Context that may change around those artefacts (this Framework) |
| **Constitution Article IV / EIP-001** | Meaning-bearing states and writers | Constitutional *context* succession (this Framework) |
| **This Educational State Transition Framework** | When context may lawfully transition; types; conditions; boundaries; explainability | Runtime A, state machines, algorithms, Article IV mutation, workflow execution, tip invention |

**Binding distinction:** Workflow transitions (WT-xx) move *orchestration stages*. Contextual state transitions (CST-xx) update *educational context representation*. Neither may be collapsed into the other by naming convenience.

## Downstream (MS003)

*How* constitutional educational context and contextual progression are explained — spanning initial posture, single and multiple transitions, and workflow-referenced succession — is governed by [`../state_explainability/`](../state_explainability/) (Educational State Explainability). MS002 remains authoritative for CST types, conditions, and transition-moment speech (`TRANSITION_EXPLAINABILITY.md`); MS003 binds the unified explanation contract without amending CST law.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- State machines, transition algorithms, or schedulers in code
- Database models, schemas, or ORM entities
- UI components, navigation, or notifications
- Analytics pipelines or telemetry schemas
- Workflow execution engines, sagas, or job queues
- Recommendation creation, ranking, or assembly engines
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning (owned by those corpora)
- Amendments to Article IV definitions or EIP-001 mutation rows by transition fiat
- Amendments to MS001 EST catalogue by transition labels alone (amend `STATE_TYPES.md` first)

## How to use this corpus

1. Read `EDUCATIONAL_STATE_TRANSITION_FRAMEWORK.md` first.
2. Confirm origin and destination EST types under [`../state/STATE_TYPES.md`](../state/STATE_TYPES.md).
3. Classify the proposed succession under `TRANSITION_TYPES.md`.
4. Verify permitting conditions in `TRANSITION_CONDITIONS.md`.
5. Enforce limits in `TRANSITION_BOUNDARIES.md` before accepting the transition.
6. Require explainability contracts from `TRANSITION_EXPLAINABILITY.md` for material transitions.
7. When orchestration stage movement is at stake, consult [`../workflow_transitions/`](../workflow_transitions/). When ownership is unclear, consult [`../authority/`](../authority/). When tips are at stake, consult [`../recommendations/`](../recommendations/).
8. When narrating why context is live and how it evolved across one or more transitions, consult [`../state_explainability/`](../state_explainability/) — keep consistency with `TRANSITION_EXPLAINABILITY.md`.
9. Do not implement behaviours that contradict this corpus without amending it first.
