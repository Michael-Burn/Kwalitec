# Composition Patterns

**Programme:** VIII — Workstream 4 — Constitutional Runtime Interfaces  
**Milestone:** MS002 — Runtime Interface Composition Model  
**Classification:** Closed catalogue of recognised constitutional runtime interface composition patterns  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional runtime interface composition patterns** (RIC-01…RIC-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RUNTIME_INTERFACE_COMPOSITION_MODEL.md`](RUNTIME_INTERFACE_COMPOSITION_MODEL.md)
3. [`COMPOSITION_OBJECTIVES.md`](COMPOSITION_OBJECTIVES.md)
4. [`../interfaces/INTERFACE_TYPES.md`](../interfaces/INTERFACE_TYPES.md) — RI-01…RI-07 participants
5. [`../interfaces/INTERFACE_BOUNDARIES.md`](../interfaces/INTERFACE_BOUNDARIES.md) — composition boundaries this corpus specialises
6. Programme VI corpora under [`../../educational/`](../../educational/)
7. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
8. Programme VIII WS1 corpora under [`../contracts/`](../contracts/), [`../event_processing/`](../event_processing/), [`../execution_completion/`](../execution_completion/)
9. Programme VIII WS2 corpora under [`../evidence_consumption/`](../evidence_consumption/), [`../evidence_validation/`](../evidence_validation/), [`../evidence_completion/`](../evidence_completion/)
10. Programme VIII WS3 corpora under [`../services/`](../services/), [`../service_collaboration/`](../service_collaboration/), [`../service_completion/`](../service_completion/)
11. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published composition patterns may coordinate material constitutional interaction among runtime interfaces.  
> Unpublished “implied facades” are constitutionally defective.**

**Namespace note.** RIC-* here means **Runtime Interface Composition**. Runtime Interface categories are RI-*. Runtime Service Collaboration patterns are RSC-*. Runtime Contracts are RC-*.

---

## 1. Purpose

Runtime without a closed interface-composition catalogue invents authority by proximity: whichever facade aggregates whichever endpoints becomes the tutor, and distinct RI identities silently dissolve into whoever holds the wire format.

This catalogue names the only lawful coordination forms between authorised RI participants.

---

## 2. Catalogue Overview

| ID | Pattern | Primary coordination form | Typical RI participants (illustrative) |
|----|---------|---------------------------|----------------------------------------|
| **RIC-01** | Sequential Composition | Ordered handoff of authorised artefacts | RI-01 → RI-02 → RI-05 → RI-06 |
| **RIC-02** | Parallel Composition | Concurrent independent interactions under shared law | RI-02 ∥ RI-07 with shared RI-06 |
| **RIC-03** | Conditional Composition | Branching on published dispositions / conditions | RI-01 gates RI-05 / RI-03 |
| **RIC-04** | Nested Composition | One interface interaction embeds another without absorption | RI-05 nests RI-01 / RI-02 / RI-06 |
| **RIC-05** | Evidence-Oriented Composition | Coordination gated by published evidence honesty | RI-02 / EV outcomes gate RI-05 / RI-04 |
| **RIC-06** | Service-Oriented Composition | Coordination through the published service catalogue boundary | RI-04 with specialised RI-01…RI-07 as required |
| **RIC-07** | Diagnostic Composition | Non-mutating inspection over composed interface posture | RI-07 with read-only RI-06 / catalogue inspection |

Material composed interactions must map to one or more of these patterns. Cross-cutting journeys may instantiate several patterns simultaneously; none may be silently skipped when their coordination form applies.

Patterns **coordinate**. They do **not** merge identities: each participating interface remains an interaction contract under its own MS001 permitted exposures.

---

## 3. Participating Interface Roles (Shared Vocabulary)

Across patterns, the following **roles** name coordination faces — not new RI types and not responsibility transfers:

| Role | Meaning |
|------|---------|
| **Initiator** | The RI interface that opens the composition under applicable RC bindings |
| **Participant** | Any RI interface that performs a material interaction within the composition |
| **Specialist** | A participant invoked for a published specialised exposure (e.g. evidence, event, execution, audit, diagnosis) |
| **Gate** | A participant whose published disposition lawfully enables or refuses continuation |
| **Recorder** | Typically RI-06 when audit obligations apply to the composition |
| **Inspector** | Typically RI-07 when the composition is diagnostic and non-mutating |

Roles describe *how a recognised RI participates in a pattern*. They never invent unpublished interfaces or reassign constitutional responsibilities.

---

## 4. RIC-01 — Sequential Composition

### Constitutional purpose

Coordinate authorised RI interfaces so that published exposures are fulfilled in a **lawful order**, with each step consuming authorised artefacts from the prior step — without collapsing steps into one mega-interface or treating order as identity merger.

### Participating interfaces

- **Initiator** — opens the sequence under RC bindings (often RI-01, RI-03, or RI-05).
- **Participants** — successive RI-01…RI-07 interfaces required by published law.
- **Recorder** — RI-06 when material steps require audit composition.

### Permitted composition

- Hand off authorised constitutional artefacts in published order (dispositions, evidence records, event traces, execution artefacts, audit refs, diagnostic scopes).
- Require each step’s own RC bindings and RI exposures before that step’s material interaction.
- Refuse / defer / escalate the sequence when a step’s published law requires stop.
- Compose with other RIC patterns for nested specialised handoffs (e.g. sequential + nested).

### Prohibited composition

- Skipping required specialised interfaces for product convenience.
- Merging successive RI identities into the initiator’s catalogue.
- Treating “previous interface succeeded” as substitute for the next interface’s RC authorisation.
- Reinterpreting artefacts in transit between interfaces.
- Inventing unpublished intermediate mega-interfaces to “simplify the chain.”
- Exposing implementation technology (protocol hops, SDK batching) as the constitutional sequence.

### Constitutional outputs

- Ordered interaction records citing each participating RI, artefacts exchanged, and pattern identity.
- Authorised final dispositions / surfaced artefacts for the sequence as published law requires.
- Continuity-preserving audit trail across the sequence (via RI-06 when applicable).
- Explicit refuse / defer / escalate outcomes when the sequence must stop.

---

## 5. RIC-02 — Parallel Composition

### Constitutional purpose

Coordinate authorised RI interfaces so that **independent published exposures** may execute concurrently under shared constitutional law — without race-dependent educational meaning, identity merger, or silent winner-takes-all authorship.

### Participating interfaces

- **Initiator** — opens the parallel set under RC bindings that authorise concurrent composition.
- **Participants** — RI interfaces whose published exposures do not require serial dependence for the acts being coordinated.
- **Recorder** — RI-06 for shared reconstructable trails across concurrent interactions.

### Permitted composition

- Execute independent authorised interactions under the same published cycle / concern when law permits concurrency.
- Exchange only authorised artefacts; share read-only published context without mutual absorption.
- Join concurrent results only under published composition / completion rules (WS1 / WS2 completion law as applicable).
- Refuse the parallel set when concurrency would invent educational meaning or merge interface identities.

### Prohibited composition

- Letting infrastructure races decide tips, ownership, mastery, or state.
- Merging concurrent participants into one unpublished composite interface.
- Using parallelism to bypass a required serial gate (contract check, evidence eligibility, diagnostic non-execution).
- Presenting “first finished” as constitutional warrant.
- Erasing loser-branch provenance to simplify audit.
- Treating fan-out protocol features as constitutional authorisation.

### Constitutional outputs

- Concurrent interaction records for each participant with shared composition identity.
- Published join / non-join dispositions under completion or composition law.
- Shared audit trail that preserves each participant’s constitutional refs.
- Honest refuse / defer when concurrency is not constitutionally authorised.

---

## 6. RIC-03 — Conditional Composition

### Constitutional purpose

Coordinate authorised RI interfaces so that continuation, branching, or stop follows **published dispositions and conditions** — not product preference, A/B winners, or undocumented heuristics.

### Participating interfaces

- **Gate** — typically RI-01 (contract disposition), RI-02 (evidence / eligibility), RI-03 (event evaluation), or RI-07 (readiness inspection that never executes).
- **Participants** — RI interfaces enabled only when published gate outcomes permit.
- **Recorder** — RI-06 for gate and branch auditability.

### Permitted composition

- Branch to specialised RI interactions only when published conditions / dispositions authorise continuation.
- Prefer refuse / defer / escalate branches when law requires stop.
- Compose gate outcomes as authorised artefacts for downstream participants.
- Explain why a branch was taken or refused without inventing new conditions.

### Prohibited composition

- Inventing unpublished conditions or “temporary gates” for convenience.
- Treating feature flags, UI mode, queue depth, or HTTP status as constitutional gates unless published law maps them.
- Continuing after a refuse disposition by renaming the composed call.
- Using conditional branching to redefine Programme VI meaning or Programme VII ownership.
- Presenting optimiser confidence as a constitutional condition.
- Collapsing gate and gated interfaces into one identity.

### Constitutional outputs

- Gate evaluation records citing published conditions and RC bindings.
- Branch participation records for taken / refused paths, naming each RI distinctly.
- Authorised outputs only on lawfully enabled branches.
- Explicit stop speech when conditions fail.

---

## 7. RIC-04 — Nested Composition

### Constitutional purpose

Allow an authorised RI interface to **embed another authorised RI interaction** within its own lawful exposure — without absorbing the nested interface’s identity, transferring its responsibilities, or inventing a new combined interface type.

### Participating interfaces

- **Initiator (outer)** — retains its own MS001 identity and exposures; requests nested specialised interaction.
- **Specialist (inner)** — executes only its published permitted exposures under its own RC bindings and RI identity.
- **Recorder** — RI-06 when the nesting is material.

### Permitted composition

- Nest another authorised RI interaction to fulfil a published specialised exposure (e.g. RI-05 nests RI-01 for contract gate; RI-05 nests RI-02 for evidence honesty; any nests RI-06 for audit).
- Return authorised artefacts / dispositions from inner to outer without reclassification.
- Refuse nesting when the inner interface’s RC conditions or exposures fail.
- Narrate nesting without claiming the outer interface “became” the inner interface.

### Prohibited composition

- Absorbing the inner interface’s identity or permitted exposures into the outer.
- Transferring constitutional responsibilities by nesting proximity.
- Skipping the inner interface’s RC bindings because the outer was already authorised for *its* exposure.
- Inventing tip text, evidence classes, or state postures “on behalf of” the inner interface.
- Treating nested composition as a permanent reassignment of MS001 catalogue identities.
- Presenting nested protocol calls as a single constitutional mega-interface.

### Constitutional outputs

- Nesting records naming outer RI, inner RI, contracts for each, and artefacts returned.
- Inner dispositions / surfaced artefacts remaining under inner provenance and identity.
- Audit composition preserving non-absorption and non-merger.
- Refuse / defer / escalate when nested law cannot be fulfilled.

---

## 8. RIC-05 — Evidence-Oriented Composition

### Constitutional purpose

Coordinate authorised RI interfaces so that material educational interaction is **gated by published constitutional evidence honesty** under Programme VIII WS2 and EIP-002 — without reinterpreting, reclassifying, or inventing warrants across composed boundaries.

### Participating interfaces

- **Evidence participant** — RI-02 (and validation eligibility under WS2 / EV law as required).
- **Dependent participants** — RI-05 / RI-04 / RI-03 / others whose published law requires lawful evidence before acting.
- **Gate** — evidence consumption / validation dispositions as published.
- **Recorder** — RI-06 for evidence provenance through the composition.

### Permitted composition

- Require published EC artefacts and required EV eligibility before dependent RI interactions.
- Exchange evidence consumption / validation records exactly as classified.
- Refuse / understate / defer dependent composition when evidence is incomplete, conflicting, or ineligible.
- Preserve claim-ladder honesty into downstream execution / service / event speech.
- Compose with RIC-01 / RIC-03 / RIC-04 when evidence gating precedes specialised exposures.

### Prohibited composition

- Reclassifying evidence between interfaces (e.g. treating session completion as mastery mid-handoff).
- Minting Estimated Knowledge / Mastery to unblock composition.
- Bypassing RI-02 because another interface “already has the data.”
- Presenting Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Inventing new EC / EV categories by composition convenience.
- Merging RI-02 into an execution facade so evidence honesty becomes unspeakable.

### Constitutional outputs

- Evidence consumption / validation records attached to the composition identity.
- Dependent interaction records only when eligibility / consumption law is satisfied — or honest refuse.
- Provenance-intact artefacts for execution / service / event interactions that required evidence.
- Audit trails showing claim-class honesty and RI-02 identity were preserved.

---

## 9. RIC-06 — Service-Oriented Composition

### Constitutional purpose

Coordinate authorised RI interfaces so that composition proceeds through the **published runtime service catalogue boundary** (RI-04) — exposing RS-01…RS-07 capabilities and lawful RSC collaboration without inventing services, redistributing RS responsibilities, or merging RI identities into a “service API.”

### Participating interfaces

- **Catalogue participant** — RI-04 Service Interface as the capability-boundary face.
- **Specialised participants** — RI-01…RI-07 as required by the invoked RS capabilities and contracts.
- **Recorder** — RI-06 for catalogue invocation and collaboration-facing audit.

### Permitted composition

- Request invocation of published RS capabilities through RI-04 under published inputs.
- Observe or expose RSC-* collaboration pattern identity when composition requests lawful service collaboration — without redefining RSC law.
- Compose RI-04 with RI-01 / RI-02 / RI-03 / RI-05 / RI-06 as published law requires for the invoked capabilities.
- Refuse unpublished services, responsibilities, or collaboration patterns at the boundary.
- Keep RI-04 identity distinct from the specialised RI participants it may nest or sequence.

### Prohibited composition

- Inventing unpublished services, responsibilities, or RSC patterns via interface aggregation.
- Transferring or merging RS responsibilities by calling RI-04.
- Treating microservice layout, DI graphs, module folders, or OpenAPI tags as the service catalogue.
- Bypassing WS3 collaboration / completion law through “direct” internal calls presented as composed interface success.
- Collapsing RI-04 and all specialised RIs into one mega-service-interface identity.
- Redefining constitutional capabilities by convenient endpoint grouping under RI-04.

### Constitutional outputs

- Catalogue invocation records naming RI-04, invoked RS capability, and any RSC pattern observed.
- Authorised service execution / collaboration outputs as defined by WS3 law.
- Distinct RI participant records for any nested specialised interfaces.
- Explicit refusal when the requested capability or collaboration is unpublished.

---

## 10. RIC-07 — Diagnostic Composition

### Constitutional purpose

Coordinate authorised RI interfaces for **non-mutating constitutional inspection** of published law, catalogue membership, composition posture, and boundary readiness — without creating constitutional behaviour, altering evidence, executing workflows, or becoming an execution authority.

### Participating interfaces

- **Inspector** — RI-07 Diagnostic Interface as primary face.
- **Read-only participants** — RI-06 (audit trail retrieval), and read-only projections of RI / RS / RC catalogue membership.
- **Non-participants for execution** — RI-01 / RI-05 may be *inspected* for readiness but must not execute under this pattern alone.

### Permitted composition

- Inspect which RI / RS / RC / RIC types are published and applicable.
- Inspect whether required constitutional inputs appear present for a contemplated act.
- Inspect prior audit trails and composition posture in read-only form.
- Compose RI-07 with RI-06 for historical reconstruction without mutation.
- Refuse any diagnostic composition that would mutate evidence, state, recommendations, ownership, or specifications.

### Prohibited composition

- Mutating evidence, state, recommendations, ownership, or specifications under a diagnostic label.
- Executing workflows or minting tips because diagnosis “looked ready.”
- Using RIC-07 to silently become RIC-01 / RIC-05 execution composition.
- Exposing implementation internals (stack traces, private schemas, adapter paths, wire dumps) as constitutional law.
- Presenting diagnostic confidence scores as educational warrant.
- Merging RI-07 with execution interfaces into one “inspect-and-run” mega-interface.

### Constitutional outputs

- Diagnostic reports describing published catalogue membership, cited corpora, composition posture, and boundary checks.
- Honesty flags for missing warrants, incomplete audit, or unpublished request shapes.
- Explicit non-claims: diagnosis is not mastery, not pass certainty, not corpus amendment, not execution.
- Audit / inspection records preserving RI-07 non-mutating identity.

---

## 11. Catalogue Rules

1. **Closed catalogue.** New RIC patterns require a Programme VIII constitutional amendment — not a silent facade invention.
2. **Participant honesty.** Every participant must be a recognised RI-01…RI-07 interface.
3. **Identity preservation.** Patterns coordinate; they never merge interface identities or transfer responsibilities.
4. **Capability honesty.** Composition never redefines constitutional capabilities or invents unpublished RI / RS types.
5. **Artefact honesty.** Only authorised constitutional artefacts may be exchanged.
6. **Contract binding.** Every material interaction inside a pattern remains under applicable RC-01…RC-07 bindings.
7. **Namespace honesty.** RIC-* must not be confused with RI-*, RSC-*, RS-*, or RC-*.
8. **Technology silence.** Catalogue entries never mandate REST, GraphQL, gRPC, HTTP, WebSockets, SDKs, authentication, networking, or frameworks.
9. **Replaceability.** Any compliant implementation may realise a RIC pattern; none may monopolise constitutional composition truth.
10. **MS001 supremacy for identities.** Pattern selection never alters the Runtime Interface Model catalogue.
11. **Diagnosis never executes.** RIC-07 is non-mutating; execution requires RIC patterns that lawfully include RI-01 / RI-05 (as applicable).
12. **Audit always for material acts.** Material RIC-01…RIC-06 compositions bind RI-06 when reconstructability is claimed.

---

## 12. Closing Statement

> **If a coordination among runtime interfaces cannot name its RIC pattern, its RI participants, the artefacts exchanged, the outputs produced, and the identities preserved, it is not yet constitutional composition — and must not be exposed as educational law.**
