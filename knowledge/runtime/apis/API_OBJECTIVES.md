# API Objectives

**Programme:** VIII — Workstream 5 — Constitutional Runtime APIs  
**Milestone:** MS001 — Runtime API Model  
**Classification:** Constitutional optimisation targets for runtime APIs  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what runtime APIs must optimise**.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`RUNTIME_API_MODEL.md`](RUNTIME_API_MODEL.md)
4. Programme VI constitutional models (educational meaning authorities)
5. Programme VII constitutional models (orchestration, authority, recommendation, state)
6. Programme VIII WS1 Runtime Contract, Event Processing, and Execution Completion Models
7. Programme VIII WS2 Evidence Consumption, Validation, and Completion Models
8. Programme VIII WS3 Runtime Service, Collaboration, and Completion Models
9. Programme VIII WS4 Runtime Interface, Composition, and Completion Models
10. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
11. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Protocols, OpenAPI documents, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here.

> **Runtime API objectives specialise lawful exposure of published runtime interfaces.  
> They never authorise inventing Programme VI meaning, altering ownership, minting tips, rewriting Programme VII, redefining Programme VIII interfaces or services, bypassing contracts, establishing constitutional authority, or elevating transports into constitutional law.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “endpoints hot” or “OpenAPI methods shipped.” The tutor optimises **faithful constitutional exposure**: authorised consumers receive only the published runtime interfaces that were already lawfully defined — with honest boundaries, reconstructable history, and technology-neutral exposure meaning.

These objectives bind every Runtime A API interaction and every successor runtime that claims constitutional compliance.

---

## 2. Primary Objective

### RAO-01 — Expose constitutional capabilities

**Definition.** Ensure that runtime APIs surface only published constitutional runtime interfaces (RI-01…RI-07) and, through them, only published constitutional execution capabilities — or honestly refuse when no published interface authorises the exposure.

**Includes:**

- Mapping material interactions to recognised RA-01…RA-07 API types.
- Exposing only interfaces already published under the Runtime Interface Model.
- Consuming only authorised constitutional request shapes (interfaces, contracts, evidence, events, service responsibilities).
- Returning only authorised constitutional responses (dispositions, artefacts, audit trails, diagnostic records).
- Preferring lawful refusal / deferral / escalation over invented exposure.

**Excludes:**

- Inventing unpublished interfaces, request shapes, or response classes “to keep the product moving.”
- Redefining RI / RS catalogues via API naming or wire convenience.
- Optimising for engagement, latency, or conversion as a substitute for constitutional fidelity.
- Treating Version 2 Adaptive / Twin / Experience heuristics as replacements for Programmes VI–VIII.
- Exposing “close enough” approximations of constitutional interfaces without documenting a corpus amendment.

**Tutor rationale.** Professional exam preparation fails when the software coach improvises educational law at the wire. Interface exposure is care; improvisation is harm.

---

## 3. Supporting Objectives

### RAO-02 — Preserve interface integrity

**Definition.** Ensure that API interactions never redefine published runtime interfaces, never invent parallel RI catalogues, and never treat transport shapes as substitutes for RI-01…RI-07 interaction contracts.

**Tutor rationale.** A polished endpoint that silently rewrites interface meaning destroys constitutional layering even if the OpenAPI document feels clean.

**Manifestations:**

- APIs expose interfaces; they do not author or amend them.
- Forbidden actions in `API_BOUNDARIES.md` that touch interface redefinition are hard stops.
- RI catalogue semantics survive every protocol migration.
- Product urgency never mints new constitutional interface rights via API shape.

---

### RAO-03 — Preserve implementation independence

**Definition.** Ensure that Runtime API meanings bind behaviour, not a specific language, framework, protocol, OpenAPI document, or deployment topology. Any compliant implementation may honour the same RA catalogue.

**Tutor rationale.** If educational truth can only be exposed through one stack or wire format, that stack has become an unlawful constitution.

**Manifestations:**

- RA-01…RA-07 are technology-neutral exposure contracts.
- Successor runtimes must honour the same API catalogue and boundaries.
- REST, GraphQL, gRPC, HTTP, and OpenAPI are delivery details — never educational law.
- “Only this protocol can decide” is a governance failure unless the Constitution / Programmes say so.

---

### RAO-04 — Preserve auditability

**Definition.** Ensure that every material API interaction leaves a reconstructable constitutional trail: which API ran, which runtime interface was exposed, which request was received, which response was returned, and which boundaries were preserved.

**Tutor rationale.** A tutor who cannot later say *what was asked and what was returned under which interface* cannot be trusted. APIs without audit are educational amnesia at the exposure boundary.

**Manifestations:**

- Audit records preserve constitutional references, not only technical access logs.
- Continuity (EIP-005) is preserved across retries, replacements, and redeploys.
- Missing provenance is a defect, not an acceptable optimisation.
- RA-06 Audit API obligations apply to material interactions across the catalogue.

---

### RAO-05 — Preserve explainability

**Definition.** Ensure that API interactions remain speakable under EIP-003: students and developers can answer the constitutional explainability questions without receiving redefined educational meaning.

**Tutor rationale.** Opaque exposure behaviour recreates black-box tutoring. Clear exposure speech is part of educational honesty.

**Manifestations:**

- Explanations cite API, interface, request, response, and boundaries (`API_EXPLAINABILITY.md`).
- Student speech and developer traces share one truth with different vocabulary.
- Scores and optimiser confidence are never presented as constitutional warrant.
- Explanation never becomes a back door to invent tips, mastery, policy, or interface redefinition.

---

### RAO-06 — Remain technology neutral

**Definition.** Ensure that no networking choice, framework, authentication stack, or OpenAPI schema becomes part of the constitutional architecture. API law describes exposure contracts; transports obey those contracts.

**Tutor rationale.** Treating HTTP routes, gRPC methods, or OpenAPI operations as educational authorities recreates the very technology lock-in Programme VIII exists to prevent.

**Manifestations:**

- Constitutional documents name RA types, not route tables.
- AuthN/AuthZ mechanisms may gate access operationally; they never redefine who owns educational meaning.
- Protocol migrations must preserve RA catalogue semantics and bound RI meanings.
- Framework convenience never rewrites Programme VIII WS1–WS4 law.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| RAO-01 conflicts with engagement metrics | Constitutional interface exposure wins |
| RAO-02 conflicts with convenience rewriting of RI meanings | Interface integrity wins |
| RAO-03 conflicts with lock-in to a single protocol | Implementation independence wins |
| RAO-04 conflicts with log volume reduction that erases constitutional refs | Auditability wins |
| RAO-05 conflicts with cryptic internal jargon as student speech | Explainability honesty wins |
| RAO-06 conflicts with elevating a transport into architecture law | Technology neutrality wins |

No supporting objective authorises violating RAO-01.

---

## 5. Non-Objectives

Runtime APIs do **not** optimise for:

- endpoint count, OpenAPI operation count, or protocol fashion as educational success;
- inventing educational certainty when warrants are incomplete;
- collapsing Programmes VI–VIII into one mega-API;
- making a particular transport irreplaceable;
- using Twin / Adaptive estimates as substitutes for constitutional producers;
- treating documentation as optional commentary on wire behaviour;
- defining educational meaning, constitutional authority, runtime policy, or transport protocols at the API layer;
- redefining published runtime interfaces or runtime services.

---

## 6. Closing Statement

> **An API that is fast, polished, and constitutionally unfaithful is a failed educational exposure boundary.  
> An API that is technology-neutral, auditable, and faithful to published interfaces is doing its only job.**
