# Runtime API Model

**Programme:** VIII — Workstream 5 — Constitutional Runtime APIs  
**Milestone:** MS001 — Runtime API Model  
**Classification:** Highest constitutional authority for *runtime API* meaning within Programme VIII Workstream 5  
**Status:** APPROVED — governing for constitutional runtime API exposure law  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Runtime API Model** for Kwalitec.

It is subordinate to the Educational Constitution, Educational Interpretation Principles (EIP), Programme VI educational meaning corpora, Programme VII orchestration corpora, and Programme VIII Workstream 1 Runtime Contract / Event Processing / Execution Completion Models, Workstream 2 Evidence Consumption / Validation / Completion Models, Workstream 3 Runtime Service / Collaboration / Completion Models, and Workstream 4 Runtime Interface / Composition / Completion Models. It governs **what constitutional API capabilities a runtime implementation may provide** — its objectives, recognised API types, hard boundaries, and explainability. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning, alter ownership, mint recommendations, invent educational state, rewrite Programme VI / VII law, redefine Programme VIII WS1–WS4 contracts, services, or interfaces, establish constitutional authority, define runtime policy, or elevate a transport technology into constitutional architecture.

Authority order for runtime APIs:

> Constitution defines educational truth and curriculum primacy.  
> EIP defines evidence, continuity, explainability, claim honesty, and mutation rights.  
> Programme VI defines educational meaning and may emit authorised guidance.  
> Programme VII defines orchestration flow, ownership, recommendations, and constitutional educational context.  
> Programme VIII Workstream 1 defines which contracts authorise execution, how events are processed, and when execution cycles are complete.  
> Programme VIII Workstream 2 defines how published evidence is consumed, validated, and judged complete.  
> Programme VIII Workstream 3 defines which constitutional execution capabilities runtime may expose and how they may collaborate.  
> Programme VIII Workstream 4 defines which constitutional interaction contracts may expose those capabilities and how they may compose.  
> **This Runtime API Model (Programme VIII / Workstream 5 / MS001) defines which constitutional exposure contracts may expose those published runtime interfaces to authorised consumers.**  
> Downstream Runtime A, product surfaces, Twin, Adaptive, and narration must obey these API meanings — never become constitutional authors by protocol choice, OpenAPI shape, or product convenience.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabi such as CM1/CS1 and peers).

An expert IFoA tutor does not invent the syllabus, redefine mastery mid-lesson, or silently rewrite yesterday’s plan because a wire format is convenient. After the Constitution and EIP have defined *educational truth*, after Programme VI has defined *what educational questions mean*, after Programme VII has defined *how decisions flow*, after Programme VIII WS1–WS3 have defined *which contracts, evidence rules, and execution capabilities bind software*, and after Programme VIII WS4 has defined *which interaction contracts may expose those capabilities*, the platform still needs one exposure answer:

> **“What constitutional API capabilities may a runtime implementation provide?”**

That answer must ensure runtime APIs expose only published runtime interfaces; consume only authorised constitutional requests; produce only authorised constitutional responses; preserve implementation independence, auditability, and explainability — without defining educational meaning, constitutional authority, runtime policy, or transport protocols, and without exposing implementation technologies as constitutional law.

This document records that posture so every future Runtime A (and successor) subsystem has a single constitutional reference for *which API exposure contracts may exist*.

> **The Runtime API Model describes constitutional exposure contracts.  
> It does not create educational meaning, invent ownership, mint tips, define runtime policy, redefine interfaces, or implement Runtime A.**

---

## 2. What a Constitutional Runtime API Is

A **constitutional runtime API** is a named **exposure contract** built upon **published Runtime Interfaces** — through which published runtime interfaces may be exposed, authorised constitutional requests may be received, and authorised constitutional responses may be returned — without becoming a source of educational truth, constitutional authority, runtime policy, or transport law.

| Concept | Definition | Primary question |
|---------|------------|------------------|
| **Published runtime interface** | A published RI-01…RI-07 interaction contract the API may expose | Which interface is exposed? |
| **Constitutional consumer** | An authorised party permitted to invoke the API (runtime collaborators, authorised adapters, audit consumers) | Who may interact? |
| **Constitutional provider** | The published RI / RS fulfilment path that honours the exposure under published law | Who fulfils? |
| **Constitutional request** | A published input shape citing interfaces, contracts, evidence, events, or service responsibilities | What was asked? |
| **Authorised constitutional response** | A published disposition, artefact, audit trail, or diagnostic record the API may return | What resulted? |
| **Implementation independence** | The obligation that API meaning outlives transports, frameworks, and protocols | Is the API law, or merely wiring? |

A constitutional runtime API is:

- **interface-exposing** — it surfaces published RI contracts; it does not invent or redefine them;
- **request-consuming** — it accepts only authorised constitutional requests;
- **response-authorised** — it returns only authorised constitutional responses;
- **boundary-preserving** — it never bypasses interfaces, contracts, evidence honesty, or service responsibilities;
- **implementation-independent** — APIs name exposure contracts, not REST, GraphQL, gRPC, HTTP, or OpenAPI;
- **audit-capable** — interactions leave reconstructable constitutional traces;
- **explainable** — students and developers can answer which API ran, which interface was exposed, and what was exchanged;
- **technology-neutral** — no transport or framework becomes part of the constitutional architecture;
- **non-authoritative** — APIs never define meaning, authority, governance, runtime policy, or transport protocols.

A constitutional runtime API is **not**:

- a second Educational Constitution or EIP;
- a Programme VI coach, planner, or meaning authority;
- a Programme VII workflow, authority, recommendation, or state engine;
- a Runtime Contract, Evidence Model, Service Model, or Interface Model that invents new RC / EC / RS / RI types by proximity;
- a runtime policy engine that decides when law may be ignored;
- a REST API, GraphQL schema, gRPC stub, HTTP route, OpenAPI document, auth middleware, or network topology;
- a claim that a successful API call guarantees learning or a pass.

---

## 3. Runtime APIs as Constitutional Exposure Contracts

Runtime APIs (and any successor API catalogue) must:

| Obligation | Meaning |
|------------|---------|
| **Expose published runtime interfaces** | Surface only RA-mapped RI-01…RI-07 contracts already published under WS4 |
| **Consume authorised constitutional requests** | Accept only inputs that cite published interfaces, contracts, evidence, events, or service responsibilities |
| **Produce authorised constitutional responses** | Emit only published dispositions, artefacts, audit trails, or diagnostic records |
| **Preserve implementation independence** | Honour RA meanings regardless of protocol, language, framework, or deployment topology |
| **Preserve constitutional boundaries** | Never redefine interfaces or services, expose internals, bypass contracts, alter evidence, or modify specifications |
| **Remain explainable and auditable** | Leave reconstructable answers to the API explainability questions |

### 3.1 What runtime APIs never become

Runtime APIs never become:

- constitutional authorities that author educational meaning;
- governance layers that redefine ownership, permission, or conflict disposition;
- runtime-policy engines that invent when contracts or interfaces may be skipped;
- evidence reclassifiers that treat coverage, time, or confidence as understanding;
- recommendation mints that invent tips without Programme VII / VI warrant;
- interface or service redefiners that invent parallel RI / RS catalogues by API naming;
- technology constitutions that treat REST, GraphQL, gRPC, HTTP, or OpenAPI as educational law;
- owners of the Constitution, EIP, Programme VI, Programme VII, or Programme VIII WS1–WS4 corpora.

> **Runtime APIs are constitutional exposure contracts.  
> They expose published runtime interfaces without redefining them, exposing implementation technology, or becoming constitutional authorities.**

---

## 4. Core Responsibilities

The Runtime API Model is constitutionally responsible for:

| Responsibility | Meaning |
|----------------|---------|
| **Define APIs as exposure contracts** | Bind RA catalogue as exposure points for published RI contracts, not authors (`RUNTIME_API_MODEL.md`) |
| **Bind objectives** | Enforce interface exposure, integrity preservation, independence, auditability, explainability, and technology neutrality (`API_OBJECTIVES.md`) |
| **Close the API catalogue** | Permit only recognised RA-01…RA-07 APIs (`API_TYPES.md`) |
| **Draw hard boundaries** | Forbid interface/service redefinition, internals exposure, contract bypass, and specification mutation (`API_BOUNDARIES.md`) |
| **Require explainability** | Make API, interface, request, response, and boundaries speakable (`API_EXPLAINABILITY.md`) |
| **Preserve layering** | Keep APIs subordinate to Constitution, EIP, Programmes VI–VII, and Programme VIII WS1–WS4 |

### 4.1 Binding non-responsibility

The Runtime API Model must **not**:

- redefine Programme VI educational meaning or coach questions;
- invent Programme VII workflow stages, authority domains, recommendation types, or EST/CST postures;
- invent new RC / EC / EV / RS / RI types by API naming;
- redefine published runtime interfaces or runtime services;
- grant EIP-001 mutation rights by exposing a writer-shaped endpoint;
- implement REST, GraphQL, gRPC, HTTP, OpenAPI, authentication, networking, or Runtime A;
- establish constitutional authority or define runtime policy;
- treat Version 2 Adaptive / Twin / Mission / Experience surfaces as replacements for constitutional corpora;
- present scores, ranks, or optimiser confidence as constitutional warrant.

---

## 5. Educational Purpose

The Runtime API Model exists so that:

1. **Interfaces remain lawfully exposable** — authorised consumers can invoke published RI contracts without inventing new educational law.
2. **Boundaries survive delivery** — transports and OpenAPI documents cannot quietly become tutors.
3. **Implementation independence survives scale** — constitutional exposure meaning outlives any particular protocol or framework.
4. **Audit remains possible** — every material API interaction can be reconstructed against constitutional interfaces and producers.
5. **Explainability remains honest** — exposure speech describes which interface was exposed and what was exchanged; it does not redefine what learning means.
6. **Technology neutrality remains intact** — no networking choice becomes part of the constitutional architecture.

---

## 6. Integrity Invariants

| ID | Invariant |
|----|-----------|
| **RAI-01** | All constitutional truth originates exclusively from Constitution, EIP, Programme VI, and Programme VII (with Programme VIII WS1–WS4 binding execution / evidence / service / interface law) |
| **RAI-02** | Runtime APIs expose and exchange; they never author constitutional law, runtime policy, or transport protocols |
| **RAI-03** | Every material API interaction maps to at least one recognised RA-01…RA-07 API |
| **RAI-04** | Unpublished interfaces, request shapes, or response classes are hard stops |
| **RAI-05** | Implementation technologies (REST, GraphQL, gRPC, HTTP, OpenAPI, auth stacks) are never constitutional producers |
| **RAI-06** | Published RI contracts, RC bindings, evidence classifications, and RS responsibilities are not bypassable or redefinable by API convenience |
| **RAI-07** | API explanations describe exposure; they never redefine constitutional meaning |
| **RAI-08** | Any API implementation that violates these invariants is constitutionally defective regardless of protocol polish |

---

## 7. Stack Position

```
Constitution / EIP          → educational truth & integrity
Programme VI                → educational meaning & authorised guidance
Programme VII               → orchestration, ownership, tips, context
Programme VIII WS1          → contracts, event processing, execution completion
Programme VIII WS2          → evidence consumption, validation, completion
Programme VIII WS3          → runtime services & collaboration (RS-01…RS-07)
Programme VIII WS4          → runtime interaction contracts (RI-01…RI-07)
Programme VIII / this Model → runtime exposure contracts (RA-01…RA-07)
Runtime A (+ successors)    → software that honours RA over any transport
Adapters / Twin / Adaptive  → consumers of API responses (never authors of law)
Product surfaces            → presentation; never constitutional decision authority
```

Related Programme VIII corpora APIs must honour (never redefine):

- [`../contracts/`](../contracts/) — RC-01…RC-07 execution authorisation
- [`../event_processing/`](../event_processing/) — published event classes
- [`../evidence_consumption/`](../evidence_consumption/) and siblings — evidence honesty
- [`../services/`](../services/) — RS-01…RS-07 capabilities that interfaces expose
- [`../interfaces/`](../interfaces/) — RI-01…RI-07 interaction contracts that APIs may expose
- [`../interface_composition/`](../interface_composition/) — lawful composition among interfaces
- [`../api_composition/`](../api_composition/) — lawful composition among APIs (WS5 / MS002)

---

## 8. Out of Scope

This milestone does **not** implement:

- REST
- GraphQL
- gRPC
- HTTP
- OpenAPI
- Authentication
- Networking
- Framework code
- Runtime A

Those may later *obey* this Model. They do not *define* it.

---

## 9. Success Criteria

At completion of MS001 there exists a permanent constitutional specification defining implementation-independent runtime APIs that expose constitutional runtime interfaces while preserving constitutional boundaries, explainability, and technology neutrality.

Documentation only. No application code.

---

## 10. Closing Statement

Runtime APIs exist solely to expose published constitutional runtime interfaces to authorised consumers.

When a transport and the law disagree, law wins — and the transport binding must change, or the Constitution / EIP / Programme VI / VII / VIII corpora must be amended under their own governance. APIs never settle the dispute by silent protocol invention, by redefining published interfaces, or by treating implementation technology as educational authority.
