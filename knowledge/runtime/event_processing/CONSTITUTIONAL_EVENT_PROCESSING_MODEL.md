# Constitutional Event Processing Model

**Programme:** VIII — Workstream 1 — Constitutional Runtime Contracts  
**Milestone:** MS002 — Constitutional Event Processing Model  
**Classification:** Highest constitutional authority for *constitutional event processing* meaning within Programme VIII Workstream 1  
**Status:** APPROVED — governing for constitutional event processing educational execution law  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Constitutional Event Processing Model** for Kwalitec.

It is subordinate to the Educational Constitution, Educational Interpretation Principles (EIP), Programme VI educational meaning corpora, Programme VII orchestration corpora, and the Runtime Contract Model (Programme VIII / WS1 / MS001). It governs **how runtime implementations receive, evaluate, and execute published constitutional events** — its objectives, recognised event categories, hard boundaries, and explainability. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning, alter ownership, mint recommendations, invent educational state, invent unpublished event types, or rewrite Programme VI / VII / VIII MS001 law.

Authority order for event processing:

> Constitution defines educational truth and curriculum primacy.  
> EIP defines evidence, continuity, explainability, claim honesty, and mutation rights.  
> Programme VI defines educational meaning and may emit authorised guidance.  
> Programme VII defines orchestration flow, ownership, recommendations, context, and educational stimuli that may initiate or continue workflows.  
> Programme VIII / WS1 / MS001 Runtime Contract Model defines which RC contracts may authorise software execution.  
> **This Constitutional Event Processing Model (Programme VIII / Workstream 1 / MS002) defines how published constitutional events are received, evaluated, and executed under that law.**  
> Downstream Runtime A, product surfaces, Twin, Adaptive, and narration must process events under these rules — never become constitutional authors by queue proximity or product convenience.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabi such as CM1/CS1 and peers).

An expert IFoA tutor does not invent a new educational “reason” mid-lesson because a message arrived, reorder coaching because a queue was busy, or silently mint tips from an unpublished notification. After the Constitution and EIP have defined *educational truth*, after Programme VI has defined *what educational questions mean*, after Programme VII has defined *which stimuli may lawfully start or continue orchestration*, and after Programme VIII MS001 has defined *which contracts authorise execution*, the platform still needs one processing answer:

> **“How are constitutional events received, evaluated and executed while remaining subordinate to published constitutional law?”**

That answer must ensure runtime implementations consume only published events, preserve execution order and constitutional integrity, remain auditable and deterministic, and stay fully explainable — without creating, reinterpreting, or extending constitutional behaviour beyond published specifications.

This document records that posture so every future Runtime A (and successor) subsystem has a single constitutional reference for *how software may process constitutional events*.

> **The Constitutional Event Processing Model describes constitutional reception, evaluation, and execution of published events.  
> It does not create educational meaning, invent ownership, mint tips, invent event types, or implement Runtime A.**

---

## 2. What Constitutional Event Processing Is

**Constitutional event processing** is the binding obligation by which a **runtime implementation** may **receive published constitutional events**, **evaluate them under published contracts and conditions**, and **execute only published constitutional paths** — without becoming a source of educational truth or a mint of new event law.

| Concept | Definition | Primary question |
|---------|------------|------------------|
| **Constitutional event** | A published stimulus or signal class (CE-01…CE-07) whose meaning originates in Constitution / EIP / Programme VI / Programme VII corpora | What was received? |
| **Constitutional producer** | The corpus that publishes the event class and its educational / orchestration meaning | Who authored the event law? |
| **Constitutional consumer** | The runtime implementation bound to process the event under RC contracts | Who processes? |
| **Reception** | Acceptance of a published event instance into constitutional processing | Was it a published class? |
| **Evaluation** | Testing published contracts, conditions, ownership, and boundaries against the event and learner circumstances | May it lawfully proceed? |
| **Execution** | Invoking only published execution paths authorised by RC-01…RC-07 | What may runtime do? |
| **Execution record** | Published audit / continuity artefacts that reconstruct processing | Can it be audited? |
| **Deterministic processing** | Same published inputs and same published law yield the same processing disposition | Is improvisation forbidden? |

Constitutional event processing is:

- **law-subordinate** — events execute published behaviour; they never invent it;
- **contract-bound** — every material processing act maps to RC-01…RC-07 (`../contracts/`);
- **catalogue-closed** — only CE-01…CE-07 may be processed as constitutional events;
- **order-preserving** — lawful succession and published ordering obligations survive delivery;
- **integrity-preserving** — meaning, ownership, evidence, tips, and state are not rewritten by processing;
- **audit-capable** — every material processing leaves reconstructable constitutional traces;
- **explainable** — students and developers can answer which event ran under which contract;
- **implementation-independent** — queues, buses, and frameworks are delivery details, not event law.

Constitutional event processing is **not**:

- a second Educational Constitution, EIP, or Programme VI / VII event catalogue author;
- a licence to invent unpublished CE types, tips, owners, or state postures from infrastructure signals;
- a message queue, event bus, broker topology, or scheduling system;
- a database schema, API contract, DTO, or UI notification surface;
- a claim that successful processing guarantees learning or a pass;
- a replacement for Programme VII `WORKFLOW_EVENTS.md` educational stimuli — those remain upstream publishers; this Model binds *how runtime processes* published stimuli and sibling constitutional signals.

---

## 3. Processing Pipeline (Constitutional, Not Technical)

Every material constitutional event travels through three constitutional phases. These are **normative processing obligations**, not an implementation architecture.

```
Receive published constitutional event
        │
        ▼
Evaluate under published contracts / conditions / boundaries
        │
        ├── refuse / defer / escalate (lawful stop)
        │
        └── Execute published path(s)
                │
                ▼
        Produce published execution record(s)
```

| Phase | Constitutional meaning | Hard stop if … |
|-------|------------------------|----------------|
| **Receive** | Accept only CE-01…CE-07 instances whose class and producer are published | Class is unpublished, forged, or infrastructure-only without constitutional mapping |
| **Evaluate** | Bind RC contracts; test published conditions; check ownership, evidence honesty, and boundaries | No authorising contract / corpus; boundary check fails |
| **Execute** | Invoke only published execution paths; emit only published outputs / records | Path would invent meaning, tips, ownership, state, or bypass workflow law |

> **Processing never “best-effort invents” a fourth phase called improvisation.**

---

## 4. Relationship to Runtime Contracts (MS001)

Event processing is a specialisation of runtime contract execution — not a parallel constitution.

| Event processing concern | Primary RC binding |
|--------------------------|--------------------|
| General lawful execution of an event | RC-01 Execution Contract |
| Evidence-related events | RC-02 Evidence Consumption Contract (+ RC-01, RC-07) |
| Workflow / orchestration events | RC-03 Workflow Execution Contract (+ RC-04 when ownership is at stake) |
| Authority / ownership / conflict events | RC-04 Authority Consumption Contract |
| Recommendation packaging / surfacing events | RC-05 Recommendation Consumption Contract |
| Educational context / EST–CST events | RC-06 State Consumption Contract |
| Every material processing act | RC-07 Audit Contract |

Cross-cutting events may bind multiple RCs simultaneously. None may be silently skipped.

---

## 5. Core Responsibilities

The Constitutional Event Processing Model is constitutionally responsible for:

| Responsibility | Meaning |
|----------------|---------|
| **Define event processing as executor** | Bind Runtime A and successors as processors of published events, not authors (`CONSTITUTIONAL_EVENT_PROCESSING_MODEL.md`) |
| **Bind objectives** | Enforce consumption, order, integrity, auditability, and determinism (`EVENT_OBJECTIVES.md`) |
| **Close the event catalogue** | Permit only recognised CE-01…CE-07 categories (`EVENT_TYPES.md`) |
| **Draw hard boundaries** | Forbid invention, reinterpretation, authority transfer, workflow bypass, and unpublished tips (`EVENT_BOUNDARIES.md`) |
| **Require explainability** | Make event, contract, artefacts, outputs, and boundaries speakable (`EVENT_EXPLAINABILITY.md`) |
| **Preserve layering** | Keep processing subordinate to Constitution, EIP, Programmes VI–VII, and MS001 contracts |

### 5.1 Binding non-responsibility

The Constitutional Event Processing Model must **not**:

- invent new constitutional event types outside CE-01…CE-07 without a Programme VIII amendment;
- redefine Programme VI educational meaning or Programme VII stimuli catalogues;
- transfer authority, mint recommendations, invent EST/CST postures, or reclassify Evidence by processing proximity;
- implement Runtime A, message queues, event buses, algorithms, databases, APIs, UI, analytics, or scheduling;
- treat Version 2 Adaptive / Twin / Mission / Experience surfaces as publishers of constitutional event law;
- present broker acknowledgements, retries, or latency metrics as constitutional warrant.

---

## 6. Educational Purpose

The Constitutional Event Processing Model exists so that:

1. **Events remain stimuli under law** — something happened that published corpora already know how to read; software does not invent a new educational story from the wire.
2. **Order and integrity survive delivery** — coaching succession is not reshuffled by infrastructure convenience.
3. **Audit remains possible** — every material processed event can be reconstructed against producers, contracts, and outputs.
4. **Determinism remains honest** — the same published inputs under the same published law yield the same disposition.
5. **Explainability remains intact** — processing speech describes what was received and executed; it does not redefine what learning means.
6. **Runtimes remain replaceable** — constitutional event law outlives any particular broker or service topology.

---

## 7. Integrity Invariants

| ID | Invariant |
|----|-----------|
| **EPI-01** | All constitutional event meaning originates exclusively from Constitution, EIP, Programme VI, and Programme VII |
| **EPI-02** | Event processing executes published behaviour; it never authors constitutional behaviour |
| **EPI-03** | Every material processed event maps to at least one recognised CE-01…CE-07 category |
| **EPI-04** | Every material processing act maps to at least one recognised RC-01…RC-07 contract |
| **EPI-05** | Unpublished event types, tips, owners, evidence classes, or state postures are hard stops |
| **EPI-06** | Published execution order and succession obligations are preserved through processing |
| **EPI-07** | Workflow law, authority checks, and recommendation provenance are not bypassable by event convenience |
| **EPI-08** | Event explanations describe processing; they never redefine constitutional meaning |
| **EPI-09** | Deterministic evaluation under published inputs is required; silent non-determinism is a constitutional defect |
| **EPI-10** | Any runtime implementation that violates these invariants is constitutionally defective regardless of throughput polish |

---

## 8. Stack Position

```
Constitution / EIP                 → educational truth & integrity
Programme VI                       → educational meaning & authorised guidance
Programme VII                      → orchestration stimuli, ownership, tips, context
Programme VIII / MS001 Contracts   → RC-01…RC-07 execution authorisation
Programme VIII / this Model        → CE-01…CE-07 receive / evaluate / execute law
Runtime A (+ successors)           → processors under CE + RC catalogues
Adapters / Twin / Adaptive         → may observe outcomes; never mint event law
Product surfaces                   → presentation; never constitutional event authority
```

Related Programme VII corpora that publish stimuli runtime may process (never redefine):

- [`../../orchestration/workflows/WORKFLOW_EVENTS.md`](../../orchestration/workflows/WORKFLOW_EVENTS.md) — educational workflow stimuli (WE-xx) consumed under CE-02
- Sibling workflow transition / completion, authority, recommendation, and state corpora — publish conditions and artefacts processing may evaluate under CE-02…CE-05

---

## 9. Out of Scope

This milestone does **not** implement:

- Runtime A
- Message queues
- Event buses
- Algorithms
- Database models
- API endpoints
- Services
- Scheduling
- UI
- Analytics

Those may later *obey* this Model. They do not *define* it.

---

## 10. Success Criteria

At completion of MS002 there exists a permanent constitutional specification describing how constitutional events are processed by runtime implementations while preserving constitutional integrity, auditability, and determinism — fully subordinate to:

- the Educational Constitution
- Educational Interpretation Principles
- Programme VI
- Programme VII
- Programme VIII / WS1 / MS001 Runtime Contract Model

Documentation only. No application code.

---

## 11. Closing Statement

Runtime event processing exists solely to execute published constitutional events under published constitutional contracts.

When an incoming signal and published law disagree, law wins — and the signal must be refused, remapped under a published amendment, or the upstream corpus amended under its own governance. Runtime never settles the dispute by inventing a new event type or silently reinterpreting educational meaning.
