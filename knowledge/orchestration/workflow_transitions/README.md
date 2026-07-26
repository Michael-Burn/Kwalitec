# Workflow Transition Framework

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS002 — Workflow Transition Framework  
**Classification:** Constitutional orchestration specification — when educational workflows move between stages  
**Status:** APPROVED — governing for educational workflow transition meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **when an educational workflow may move from one constitutional stage to another**.

It answers *when stage movement is lawful*, *which transition kinds exist*, *what conditions permit each transition*, *what transitions may and may not do*, and *how stage movement is explained*.

It does **not** implement Runtime A, algorithms, databases, services, UI, analytics, scheduling engines, or execution engines.

> **Transitions coordinate educational flow.  
> They do not create educational meaning or alter coach authority.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001)
7. [`../workflows/`](../workflows/) — Educational Workflow Model (MS001): events, stages, objectives, boundaries, explainability
8. Programme VI constitutional corpora — **educational meaning authorities whose outputs transitions may await or hand off; transitions never redefine them**

## Contents

| Document | Role |
|---|---|
| [`WORKFLOW_TRANSITION_FRAMEWORK.md`](WORKFLOW_TRANSITION_FRAMEWORK.md) | Constitutional overview: what transitions are, responsibilities, integrity, stack position |
| [`TRANSITION_CATALOGUE.md`](TRANSITION_CATALOGUE.md) | Named lawful transition kinds (orchestration only) |
| [`TRANSITION_CONDITIONS.md`](TRANSITION_CONDITIONS.md) | Constitutional conditions that permit each transition |
| [`TRANSITION_BOUNDARIES.md`](TRANSITION_BOUNDARIES.md) | What transitions may coordinate and what they must never do |
| [`TRANSITION_EXPLAINABILITY.md`](TRANSITION_EXPLAINABILITY.md) | How workflow transitions are explained to students and developers |

## Relationship to MS001

| Horizon | Job |
|---------|-----|
| **MS001 — Educational Workflow Model** | Define *what workflows are*, *which events initiate them*, *which stages exist*, *what orchestration may do* |
| **MS002 — this corpus** | Define *when* a workflow may move between those stages (and pause, resume, escalate, or conclude) |

```
MS001 event (WE-xx) recognised
        │
        ▼
MS001 stages (S0…S7)
        │  movement governed by
        ▼
MS002 transitions (WT-xx)
        │  conditions / boundaries / explainability
        ▼
Programme VI authorities remain owners of educational meaning
```

MS001 without MS002 risks treating stage lists as ornamental.  
MS002 without MS001 risks inventing movement without stages, events, or orchestration law.

## Architectural requirement

Workflow transitions may **move** workflows between constitutional stages. They must **never**:

| Lawful | Unlawful |
|--------|----------|
| Advance S0→S7 when conditions hold | Reinterpret Educational Evidence to “justify” a jump |
| Pause awaiting lawful Programme VI / evidence outputs | Modify coach recommendations mid-transition |
| Resume when awaited outputs are available | Rewrite Canonical Study Plan as a transition side-effect |
| Escalate structural questions to Master Planner pathways | Introduce independent educational decisions |
| Conclude when an authorised outcome exists | Claim mastery because a transition completed |
| Explain why movement occurred and that authority was preserved | Speak opaque scheduler or job-queue jargon as educational law |

If lawful movement would require changing educational meaning, the transition **escalates or refuses** — it does not absorb Programme VI authority.

## Downstream (MS003)

Orchestration *fulfilment* — when conclude (WT-06) is constitutionally honest as completion of coordination duties, and what may follow (archive, successor, await, audit) — is governed by [`../workflow_completion/`](../workflow_completion/) (Workflow Completion Model). MS002 names conclude as a transition kind; MS003 specialises completion criteria, evidence, post-completion transitions, and completion explainability — without evaluating educational success, mastery, or coach outcomes.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Algorithms, scoring, ranking, or scheduling logic
- Database models, schemas, or ORM entities
- UI components, navigation implementations, or notifications
- Analytics pipelines or telemetry schemas
- Workflow execution engines, sagas, job queues, or state machines in code
- Serialisation formats or API contracts
- Workflow completion criteria catalogues (owned by MS003)

## How to use this corpus

1. Read `WORKFLOW_TRANSITION_FRAMEWORK.md` first.
2. Classify proposed stage movement under `TRANSITION_CATALOGUE.md`.
3. Verify permitting conditions in `TRANSITION_CONDITIONS.md`.
4. Enforce limits in `TRANSITION_BOUNDARIES.md` before accepting the transition.
5. Require explainability contracts from `TRANSITION_EXPLAINABILITY.md` for material transitions.
6. For orchestration fulfilment judgements and post-completion moves, consult [`../workflow_completion/`](../workflow_completion/).
7. Do not implement algorithms that contradict this corpus without amending it first.
