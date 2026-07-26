# Educational Workflow Model

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS001 — Educational Workflow Model  
**Classification:** Constitutional orchestration specification — how educational decisions flow between Programme VI components  
**Status:** APPROVED — governing for educational workflow orchestration meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how educational workflows begin, progress, and conclude across Kwalitec**.

It answers *how educational decisions flow between constitutional educational components*, *what objectives orchestration must pursue*, *which events initiate or continue workflows*, *which stages a lawful workflow passes through*, *what orchestration may and may not do*, and *how workflow orchestration is explained*.

It does **not** implement Runtime A, algorithms, databases, services, UI, analytics, scheduling engines, or execution engines.

> **The Educational Workflow Engine orchestrates educational reasoning produced by Programme VI.  
> It does not redefine educational meaning or coach authority.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001)
8. Programme VI constitutional corpora (Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach) — **educational meaning authorities this Model orchestrates, never redefines**

Related (non-authoritative for educational orchestration meaning):

- [`../../version2/education/EDUCATIONAL_ORCHESTRATION_MODEL.md`](../../version2/education/EDUCATIONAL_ORCHESTRATION_MODEL.md) — Version 2 tutoring collaboration architecture (consumes educational meaning; does not replace this constitutional workflow law)
- [`../../architecture/DESIGN_PRINCIPLES.md`](../../architecture/DESIGN_PRINCIPLES.md) — product design constraints (workflow-first navigation); educational authority remains Programme VI + this Model
- Educational Validation Framework — quality release lens, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_WORKFLOW_MODEL.md`](EDUCATIONAL_WORKFLOW_MODEL.md) | Constitutional overview: what educational workflows are, responsibilities, integrity, stack position |
| [`WORKFLOW_OBJECTIVES.md`](WORKFLOW_OBJECTIVES.md) | What educational orchestration must optimise |
| [`WORKFLOW_EVENTS.md`](WORKFLOW_EVENTS.md) | Events that initiate or continue workflows without making educational decisions |
| [`WORKFLOW_STAGES.md`](WORKFLOW_STAGES.md) | Constitutional stages through which educational reasoning passes |
| [`WORKFLOW_BOUNDARIES.md`](WORKFLOW_BOUNDARIES.md) | What workflows may coordinate and what they must never do |
| [`WORKFLOW_EXPLAINABILITY.md`](WORKFLOW_EXPLAINABILITY.md) | How workflow orchestration is explained to students and developers |

## Relationship to Programme VI

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner** | Diagnose, strategise, decide, blueprint, schedule, and publish the Canonical Study Plan |
| **Programme VI — Daily Coach** | Decide *what is most educationally valuable today* under that contract |
| **Programme VI — Learning Session / Reflection** | Decide *how one sitting is studied* and *what that sitting meant* |
| **Programme VI — Learning Coach** | Decide *whether genuine learning is progressing*, diagnose obstacles, select interventions |
| **Programme VI — Recovery Coach** | Decide *how to restore progress after meaningful disruption* |
| **Programme VI — Revision Coach** | Decide *what should be revised now, and why* |
| **Programme VI — Exam Coach** | Decide *how to prepare for and approach the examination* |
| **Programme VII — this corpus** | Decide *how those constitutional reasonings are sequenced, handed off, and concluded without conflict* |

```
Educational event (login, session complete, evidence, disruption, …)
        │  initiates or continues a workflow — does not decide
        ▼
Educational Workflow Engine (this milestone)
        │  routes / sequences / concludes participation
        ▼
Programme VI constitutional components
        │  Master Planner · Daily Coach · Learning · Recovery · Revision · Exam
        │  each retains its educational meaning authority
        ▼
Authorised educational recommendation / handoff / escalation
        │  explainable chain: event → stages → authorities → outcome
```

Programme VI settles *educational meaning*.  
Programme VII settles *how that meaning is orchestrated across components without inventing new meaning*.

## Architectural requirement

Educational workflows may **coordinate** constitutional components. They must **never**:

| Lawful | Unlawful |
|--------|----------|
| Sequence which coach or planner participates after an event | Redefine what Daily Coach, Learning Coach, or any sibling coach means |
| Hand off when one authority’s question is primary | Modify the Canonical Study Plan “for orchestration convenience” |
| Prevent conflicting simultaneous educational actions | Reinterpret Educational Evidence under a workflow label |
| Preserve determinism of the same event → same stage path | Introduce educational recommendations independently of Programme VI |
| Explain why a workflow started and who participated | Speak opaque optimiser or scheduler jargon as educational law |

If orchestration would require changing educational meaning, the workflow **escalates to the owning Programme VI authority** — it does not absorb that authority.

## Downstream (MS002–MS003)

Stage *movement* — when a workflow may advance, pause, resume, escalate, supersede, hand off, or conclude — is governed by [`../workflow_transitions/`](../workflow_transitions/) (Workflow Transition Framework). MS001 defines events and stages; MS002 defines lawful transitions between them.

Orchestration *fulfilment* — when a workflow has completed its coordination responsibilities, and what may follow — is governed by [`../workflow_completion/`](../workflow_completion/) (Workflow Completion Model). MS002 WT-06 names the conclude move; MS003 defines constitutional completion criteria, evidence, post-completion transitions, and completion explainability — without evaluating educational success.

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Algorithms, scoring, or ranking engines
- Database models, schemas, or ORM entities
- UI components, navigation implementations, or notifications
- Analytics pipelines or telemetry schemas
- Scheduling / calendar packing (owned by Master Planner MS006)
- Workflow execution engines, sagas, job queues, or state machines in code
- Serialisation formats or API contracts
- Transition condition catalogues (owned by MS002)

## How to use this corpus

1. Read `EDUCATIONAL_WORKFLOW_MODEL.md` first.
2. Treat objectives in `WORKFLOW_OBJECTIVES.md` as binding targets for orchestration behaviour.
3. Classify initiating and continuing stimuli under `WORKFLOW_EVENTS.md` — events never decide.
4. Route participation through stages in `WORKFLOW_STAGES.md`.
5. Enforce limits in `WORKFLOW_BOUNDARIES.md` before any proposed orchestration behaviour.
6. Require explainability contracts from `WORKFLOW_EXPLAINABILITY.md` before student- or developer-facing workflow narration.
7. For stage movement law, consult [`../workflow_transitions/`](../workflow_transitions/).
8. For orchestration fulfilment / close law, consult [`../workflow_completion/`](../workflow_completion/).
9. Do not implement algorithms that contradict this corpus without amending it first.