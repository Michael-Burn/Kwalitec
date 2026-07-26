# Composition Patterns

**Programme:** VIII — Workstream 5 — Constitutional Runtime APIs  
**Milestone:** MS002 — Runtime API Composition Model  
**Classification:** Closed catalogue of recognised constitutional runtime API composition patterns  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional runtime API composition patterns** (RAC-01…RAC-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RUNTIME_API_COMPOSITION_MODEL.md`](RUNTIME_API_COMPOSITION_MODEL.md)
3. [`COMPOSITION_OBJECTIVES.md`](COMPOSITION_OBJECTIVES.md)
4. [`../apis/API_TYPES.md`](../apis/API_TYPES.md) — RA-01…RA-07 participants
5. [`../apis/API_BOUNDARIES.md`](../apis/API_BOUNDARIES.md) — composition boundaries this corpus specialises
6. [`../interfaces/INTERFACE_TYPES.md`](../interfaces/INTERFACE_TYPES.md) — RI contracts APIs expose
7. [`../interface_composition/COMPOSITION_PATTERNS.md`](../interface_composition/COMPOSITION_PATTERNS.md) — RIC patterns composition may observe, never redefine
8. Programme VI corpora under [`../../educational/`](../../educational/)
9. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
10. Programme VIII WS1 corpora under [`../contracts/`](../contracts/), [`../event_processing/`](../event_processing/), [`../execution_completion/`](../execution_completion/)
11. Programme VIII WS2 corpora under [`../evidence_consumption/`](../evidence_consumption/), [`../evidence_validation/`](../evidence_validation/), [`../evidence_completion/`](../evidence_completion/)
12. Programme VIII WS3 corpora under [`../services/`](../services/), [`../service_collaboration/`](../service_collaboration/), [`../service_completion/`](../service_completion/)
13. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published composition patterns may coordinate material constitutional exposure among runtime APIs.  
> Unpublished “implied gateways” are constitutionally defective.**

**Namespace note.** RAC-* here means **Runtime API Composition**. Runtime API categories are RA-*. Runtime Interface Composition patterns are RIC-*. Runtime Service Collaboration patterns are RSC-*. Runtime Contracts are RC-*.

---

## 1. Purpose

Runtime without a closed API-composition catalogue invents authority by proximity: whichever gateway aggregates whichever endpoints becomes the tutor, and distinct RA identities silently dissolve into whoever holds the wire format.

This catalogue names the only lawful coordination forms between authorised RA participants.

---

## 2. Catalogue Overview

| ID | Pattern | Primary coordination form | Typical RA participants (illustrative) |
|----|---------|---------------------------|----------------------------------------|
| **RAC-01** | Sequential Composition | Ordered handoff of authorised artefacts across exposures | RA-01 → RA-02 → RA-05 → RA-06 |
| **RAC-02** | Parallel Composition | Concurrent independent exposures under shared law | RA-02 ∥ RA-07 with shared RA-06 |
| **RAC-03** | Conditional Composition | Branching on published dispositions / conditions | RA-01 gates RA-05 / RA-03 |
| **RAC-04** | Nested Composition | One API exposure embeds another without absorption | RA-05 nests RA-01 / RA-02 / RA-06 |
| **RAC-05** | Interface-Oriented Composition | Coordination gated by published RI exposure honesty | RA APIs expose bound RI contracts under RIC observation |
| **RAC-06** | Evidence-Oriented Composition | Coordination gated by published evidence honesty | RA-02 / EV outcomes gate RA-05 / RA-04 |
| **RAC-07** | Diagnostic Composition | Non-mutating inspection over composed API posture | RA-07 with read-only RA-06 / catalogue inspection |

Material composed exposures must map to one or more of these patterns. Cross-cutting journeys may instantiate several patterns simultaneously; none may be silently skipped when their coordination form applies.

Patterns **coordinate**. They do **not** merge identities: each participating API remains an exposure contract under its own MS001 permitted exposures, and each bound RI remains the interaction contract defined by WS4.

---

## 3. Participating API Roles (Shared Vocabulary)

Across patterns, the following **roles** name coordination faces — not new RA types and not responsibility transfers:

| Role | Meaning |
|------|---------|
| **Initiator** | The RA API that opens the composition under applicable RC bindings |
| **Participant** | Any RA API that performs a material exposure within the composition |
| **Specialist** | A participant invoked for a published specialised exposure (e.g. evidence, event, execution, audit, diagnosis) |
| **Gate** | A participant whose published disposition lawfully enables or refuses continuation |
| **Recorder** | Typically RA-06 when audit obligations apply to the composition |
| **Inspector** | Typically RA-07 when the composition is diagnostic and non-mutating |

Roles describe *how a recognised RA participates in a pattern*. They never invent unpublished APIs, redefine bound interfaces, or reassign constitutional responsibilities.

---

## 4. RAC-01 — Sequential Composition

### Constitutional purpose

Coordinate authorised RA APIs so that published interfaces are exposed in a **lawful order**, with each step consuming authorised artefacts from the prior step — without collapsing steps into one mega-API or treating order as identity merger or interface redefinition.

### Participating APIs

- **Initiator** — opens the sequence under RC bindings (often RA-01, RA-03, or RA-05).
- **Participants** — successive RA-01…RA-07 APIs required by published law.
- **Recorder** — RA-06 when material steps require audit composition.

### Permitted composition

- Hand off authorised constitutional artefacts in published order (dispositions, evidence records, event traces, execution artefacts, audit refs, diagnostic scopes).
- Require each step’s own RC bindings, RA exposures, and bound RI integrity before that step’s material exposure.
- Refuse / defer / escalate the sequence when a step’s published law requires stop.
- Compose with other RAC patterns for nested specialised handoffs (e.g. sequential + nested).

### Prohibited composition

- Skipping required specialised APIs for product convenience.
- Merging successive RA identities into the initiator’s catalogue.
- Redefining bound RI contracts across sequential hops.
- Treating “previous API succeeded” as substitute for the next API’s RC authorisation.
- Reinterpreting artefacts in transit between APIs.
- Inventing unpublished intermediate mega-APIs to “simplify the chain.”
- Exposing implementation technology (protocol hops, gateway routing, OpenAPI path batches) as the constitutional sequence.

### Constitutional outputs

- Ordered exposure records citing each participating RA, each exposed RI, artefacts exchanged, and pattern identity.
- Authorised final dispositions / surfaced artefacts for the sequence as published law requires.
- Continuity-preserving audit trail across the sequence (via RA-06 when applicable).
- Explicit refuse / defer / escalate outcomes when the sequence must stop.

---

## 5. RAC-02 — Parallel Composition

### Constitutional purpose

Coordinate authorised RA APIs so that **independent published exposures** may execute concurrently under shared constitutional law — without race-dependent educational meaning, identity merger, interface redefinition, or silent winner-takes-all authorship.

### Participating APIs

- **Initiator** — opens the parallel set under RC bindings that authorise concurrent composition.
- **Participants** — RA APIs whose published exposures do not require serial dependence for the acts being coordinated.
- **Recorder** — RA-06 for shared reconstructable trails across concurrent exposures.

### Permitted composition

- Execute independent authorised exposures under the same published cycle / concern when law permits concurrency.
- Exchange only authorised artefacts; share read-only published context without mutual absorption.
- Join concurrent results only under published composition / completion rules (WS1 / WS2 / WS4 completion law as applicable).
- Refuse the parallel set when concurrency would invent educational meaning, merge API identities, or redefine interfaces.

### Prohibited composition

- Letting infrastructure races decide tips, ownership, mastery, or state.
- Merging concurrent participants into one unpublished composite API.
- Redefining bound RI contracts by concurrent fan-out convenience.
- Using parallelism to bypass a required serial gate (contract check, evidence eligibility, diagnostic non-execution).
- Presenting “first finished” as constitutional warrant.
- Erasing loser-branch provenance to simplify audit.
- Treating fan-out protocol features or gateway concurrency as constitutional authorisation.

### Constitutional outputs

- Concurrent exposure records for each participant with shared composition identity and named exposed interfaces.
- Published join / non-join dispositions under completion or composition law.
- Shared audit trail that preserves each participant’s constitutional refs.
- Honest refuse / defer when concurrency is not constitutionally authorised.

---

## 6. RAC-03 — Conditional Composition

### Constitutional purpose

Coordinate authorised RA APIs so that continuation, branching, or stop follows **published dispositions and conditions** — not product preference, A/B winners, or undocumented heuristics.

### Participating APIs

- **Gate** — typically RA-01 (contract disposition), RA-02 (evidence / eligibility), RA-03 (event evaluation), or RA-07 (readiness inspection that never executes).
- **Participants** — RA APIs enabled only when published gate outcomes permit.
- **Recorder** — RA-06 for gate and branch auditability.

### Permitted composition

- Branch to specialised RA exposures only when published conditions / dispositions authorise continuation.
- Prefer refuse / defer / escalate branches when law requires stop.
- Compose gate outcomes as authorised artefacts for downstream participants.
- Explain why a branch was taken or refused without inventing new conditions or redefining interfaces.

### Prohibited composition

- Inventing unpublished conditions or “temporary gates” for convenience.
- Treating feature flags, UI mode, queue depth, HTTP status, or gateway routing rules as constitutional gates unless published law maps them.
- Continuing after a refuse disposition by renaming the composed call.
- Using conditional branching to redefine Programme VI meaning, Programme VII ownership, or RI contracts.
- Presenting optimiser confidence as a constitutional condition.
- Collapsing gate and gated APIs into one identity.

### Constitutional outputs

- Gate evaluation records citing published conditions, RC bindings, and exposed RI identities.
- Branch participation records for taken / refused paths, naming each RA distinctly.
- Authorised outputs only on lawfully enabled branches.
- Explicit stop speech when conditions fail.

---

## 7. RAC-04 — Nested Composition

### Constitutional purpose

Allow an authorised RA API to **embed another authorised RA exposure** within its own lawful exposure — without absorbing the nested API’s identity, transferring its responsibilities, redefining its bound interface, or inventing a new combined API type.

### Participating APIs

- **Initiator (outer)** — retains its own MS001 identity and exposures; requests nested specialised exposure.
- **Specialist (inner)** — exposes only its published permitted interfaces under its own RC bindings and RA identity.
- **Recorder** — RA-06 when the nesting is material.

### Permitted composition

- Nest another authorised RA exposure to fulfil a published specialised exposure (e.g. RA-05 nests RA-01 for contract gate; RA-05 nests RA-02 for evidence honesty; any nests RA-06 for audit).
- Return authorised artefacts / dispositions from inner to outer without reclassification or interface redefinition.
- Refuse nesting when the inner API’s RC conditions, RA exposures, or bound RI integrity fail.
- Narrate nesting without claiming the outer API “became” the inner API or absorbed its interface.

### Prohibited composition

- Absorbing the inner API’s identity, permitted exposures, or bound RI contract into the outer.
- Transferring constitutional responsibilities by nesting proximity.
- Skipping the inner API’s RC bindings because the outer was already authorised for *its* exposure.
- Inventing tip text, evidence classes, state postures, or interface semantics “on behalf of” the inner API.
- Treating nested composition as a permanent reassignment of MS001 catalogue identities.
- Presenting nested protocol calls as a single constitutional mega-API.

### Constitutional outputs

- Nesting records naming outer RA, inner RA, exposed RIs, contracts for each, and artefacts returned.
- Inner dispositions / surfaced artefacts remaining under inner provenance and identity.
- Audit composition preserving non-absorption, non-merger, and interface integrity.
- Refuse / defer / escalate when nested law cannot be fulfilled.

---

## 8. RAC-05 — Interface-Oriented Composition

### Constitutional purpose

Coordinate authorised RA APIs so that composition proceeds through **published runtime interface exposure honesty** — each participating API exposes only its bound RI-01…RI-07 contract(s), observes applicable RIC composition when required, and never invents, merges, or redefines interfaces by API aggregation.

### Participating APIs

- **Interface-exposing participants** — any RA-01…RA-07 whose material act surfaces a published RI contract.
- **Specialised participants** — additional RAs required when bound RI composition (RIC-*) demands cross-cutting interface coordination.
- **Recorder** — RA-06 for interface-identity and exposure-integrity audit.

### Permitted composition

- Require that every material composed exposure name its bound RI-01…RI-07 interface.
- Observe or require applicable RIC-01…RIC-07 patterns when WS4 law demands interface-level composition — without redefining RIC law.
- Compose multiple RAs only when each continues to expose its published RI without identity merger.
- Refuse unpublished interfaces, interface invents, or mega-interface facades at the exposure boundary.
- Keep each RA identity distinct from the RI contract it exposes.

### Prohibited composition

- Redefining RI-01…RI-07 semantics by composing convenient API endpoints.
- Inventing unpublished RI types or absorbing multiple RIs into one unnamed exposure.
- Treating OpenAPI tags, gateway routes, GraphQL types, or SDK clients as the interface catalogue.
- Bypassing WS4 interface composition / completion law through “direct” internal calls presented as composed API success.
- Collapsing RA and RI identities into one “API-is-the-interface” constitutional type.
- Presenting interface-oriented composition as a licence to rewrite MS001 RA or WS4 RI catalogues.

### Constitutional outputs

- Exposure records naming each participating RA, each exposed RI, and any RIC pattern observed.
- Authorised interface dispositions / artefacts as defined by WS4 and the bound RI.
- Distinct API and interface identity records for audit and explanation.
- Explicit refusal when the requested interface or interface composition is unpublished or would require redefinition.

---

## 9. RAC-06 — Evidence-Oriented Composition

### Constitutional purpose

Coordinate authorised RA APIs so that material educational exposure is **gated by published constitutional evidence honesty** under Programme VIII WS2 and EIP-002 — without reinterpreting, reclassifying, or inventing warrants across composed boundaries.

### Participating APIs

- **Evidence participant** — RA-02 (and validation eligibility under WS2 / EV law as required), exposing RI-02.
- **Dependent participants** — RA-05 / RA-04 / RA-03 / others whose published law requires lawful evidence before acting.
- **Gate** — evidence consumption / validation dispositions as published.
- **Recorder** — RA-06 for evidence provenance through the composition.

### Permitted composition

- Require published EC artefacts and required EV eligibility before dependent RA exposures.
- Exchange evidence consumption / validation records exactly as classified.
- Refuse / understate / defer dependent composition when evidence is incomplete, conflicting, or ineligible.
- Preserve claim-ladder honesty into downstream execution / service / event speech.
- Compose with RAC-01 / RAC-03 / RAC-04 / RAC-05 when evidence gating precedes specialised exposures.

### Prohibited composition

- Reclassifying evidence between APIs (e.g. treating session completion as mastery mid-handoff).
- Minting Estimated Knowledge / Mastery to unblock composition.
- Bypassing RA-02 / RI-02 because another API “already has the data.”
- Presenting Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Inventing new EC / EV categories by composition convenience.
- Merging RA-02 into an execution gateway so evidence honesty becomes unspeakable.
- Redefining RI-02 by evidence-oriented API aggregation.

### Constitutional outputs

- Evidence consumption / validation records attached to the composition identity.
- Dependent exposure records only when eligibility / consumption law is satisfied — or honest refuse.
- Provenance-intact artefacts for execution / service / event exposures that required evidence.
- Audit trails showing claim-class honesty and RA-02 / RI-02 identities were preserved.

---

## 10. RAC-07 — Diagnostic Composition

### Constitutional purpose

Coordinate authorised RA APIs for **non-mutating constitutional inspection** of published law, catalogue membership, composition posture, interface exposure readiness, and boundary readiness — without creating constitutional behaviour, altering evidence, executing workflows, redefining interfaces, or becoming an execution authority.

### Participating APIs

- **Inspector** — RA-07 Diagnostic API as primary face, exposing RI-07.
- **Read-only participants** — RA-06 (audit trail retrieval), and read-only projections of RA / RI / RC / RAC catalogue membership.
- **Non-participants for execution** — RA-01 / RA-05 may be *inspected* for readiness but must not execute under this pattern alone.

### Permitted composition

- Inspect which RA / RI / RC / RAC / RIC types are published and applicable.
- Inspect whether required constitutional inputs appear present for a contemplated act.
- Inspect prior audit trails and composition posture in read-only form.
- Compose RA-07 with RA-06 for historical reconstruction without mutation.
- Refuse any diagnostic composition that would mutate evidence, state, recommendations, ownership, specifications, or interface definitions.

### Prohibited composition

- Mutating evidence, state, recommendations, ownership, specifications, or interfaces under a diagnostic label.
- Executing workflows or minting tips because diagnosis “looked ready.”
- Using RAC-07 to silently become RAC-01 / RAC-05 execution composition.
- Exposing implementation internals (stack traces, private schemas, adapter paths, wire dumps, gateway configs) as constitutional law.
- Presenting diagnostic confidence scores as educational warrant.
- Merging RA-07 with execution APIs into one “inspect-and-run” mega-API.

### Constitutional outputs

- Diagnostic reports describing published catalogue membership, cited corpora, composition posture, exposed-interface readiness, and boundary checks.
- Honesty flags for missing warrants, incomplete audit, or unpublished request shapes.
- Explicit non-claims: diagnosis is not mastery, not pass certainty, not corpus amendment, not execution, not interface redefinition.
- Audit / inspection records preserving RA-07 non-mutating identity.

---

## 11. Catalogue Rules

1. **Closed catalogue.** New RAC patterns require a Programme VIII constitutional amendment — not a silent gateway invention.
2. **Participant honesty.** Every participant must be a recognised RA-01…RA-07 API.
3. **Identity preservation.** Patterns coordinate; they never merge API identities or transfer responsibilities.
4. **Interface integrity.** Composition never redefines constitutional interfaces or invents unpublished RI / RA types.
5. **Artefact honesty.** Only authorised constitutional artefacts may be exchanged.
6. **Contract binding.** Every material exposure inside a pattern remains under applicable RC-01…RC-07 bindings.
7. **Namespace honesty.** RAC-* must not be confused with RA-*, RIC-*, RI-*, RSC-*, RS-*, or RC-*.
8. **Technology silence.** Catalogue entries never mandate REST, GraphQL, gRPC, HTTP, OpenAPI, authentication, networking, API gateways, or frameworks.
9. **Replaceability.** Any compliant implementation may realise a RAC pattern; none may monopolise constitutional composition truth.
10. **MS001 supremacy for identities.** Pattern selection never alters the Runtime API Model catalogue.
11. **WS4 supremacy for interfaces.** Pattern selection never alters or redefines the Runtime Interface Model catalogue.
12. **Diagnosis never executes.** RAC-07 is non-mutating; execution requires RAC patterns that lawfully include RA-01 / RA-05 (as applicable).
13. **Audit always for material acts.** Material RAC-01…RAC-06 compositions bind RA-06 when reconstructability is claimed.

---

## 12. Closing Statement

> **If a coordination among runtime APIs cannot name its RAC pattern, its RA participants, the RI interfaces exposed, the artefacts exchanged, the outputs produced, and the identities preserved, it is not yet constitutional composition — and must not be exposed as educational law.**
