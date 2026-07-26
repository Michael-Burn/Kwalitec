# Collaboration Patterns

**Programme:** VIII — Workstream 3 — Constitutional Runtime Services  
**Milestone:** MS002 — Runtime Service Collaboration Model  
**Classification:** Closed catalogue of recognised constitutional runtime service collaboration patterns  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional runtime service collaboration patterns** (RSC-01…RSC-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RUNTIME_SERVICE_COLLABORATION_MODEL.md`](RUNTIME_SERVICE_COLLABORATION_MODEL.md)
3. [`COLLABORATION_OBJECTIVES.md`](COLLABORATION_OBJECTIVES.md)
4. [`../services/SERVICE_TYPES.md`](../services/SERVICE_TYPES.md) — RS-01…RS-07 participants
5. [`../services/SERVICE_BOUNDARIES.md`](../services/SERVICE_BOUNDARIES.md) — composition boundaries collaboration specialises
6. Programme VI corpora under [`../../educational/`](../../educational/)
7. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
8. Programme VIII WS1 corpora under [`../contracts/`](../contracts/), [`../event_processing/`](../event_processing/), [`../execution_completion/`](../execution_completion/)
9. Programme VIII WS2 corpora under [`../evidence_consumption/`](../evidence_consumption/), [`../evidence_validation/`](../evidence_validation/), [`../evidence_completion/`](../evidence_completion/)
10. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published collaboration patterns may coordinate material constitutional execution among runtime services.  
> Unpublished “implied orchestration” is constitutionally defective.**

**Namespace note.** RSC-* here means **Runtime Service Collaboration**. Runtime Service categories are RS-*; Runtime Contracts are RC-*. Recovery Strategy identifiers under Programme VI are a separate namespace.

---

## 1. Purpose

Runtime without a closed collaboration catalogue invents authority by proximity: whichever module calls whichever other module becomes the tutor, and duties silently merge into whoever holds the thread.

This catalogue names the only lawful coordination forms between authorised RS participants.

---

## 2. Catalogue Overview

| ID | Pattern | Primary coordination form | Typical RS participants (illustrative) |
|----|---------|---------------------------|----------------------------------------|
| **RSC-01** | Sequential Collaboration | Ordered handoff of published artefacts | RS-01 → RS-04 → RS-05 → RS-07 |
| **RSC-02** | Parallel Collaboration | Concurrent independent acts under shared law | RS-02 ∥ RS-06 with shared RS-07 |
| **RSC-03** | Delegated Collaboration | Caller requests specialised execution without absorbing duty | RS-04 delegates to RS-05 / RS-02 |
| **RSC-04** | Conditional Collaboration | Branching on published dispositions / conditions | RS-01 gates RS-04 / RS-05 |
| **RSC-05** | Evidence-Driven Collaboration | Coordination gated by published evidence honesty | RS-02 / EV outcomes gate RS-04 / RS-05 / RS-06 |
| **RSC-06** | Event-Driven Collaboration | Coordination initiated or continued by published CE events | RS-03 initiates RS-04 / specialised RS |
| **RSC-07** | Audit Collaboration | Composition that preserves reconstructable trails | RS-07 with any RS-01…RS-06 |

Material collaborative acts must map to one or more of these patterns. Cross-cutting journeys may instantiate several patterns simultaneously; none may be silently skipped when their coordination form applies.

Patterns **coordinate**. They do **not** transfer authorship: each participating service remains an executor under its own MS001 permitted responsibilities.

---

## 3. Participating Service Roles (Shared Vocabulary)

Across patterns, the following **roles** name coordination faces — not new RS types and not ownership transfers:

| Role | Meaning |
|------|---------|
| **Initiator** | The RS service that opens the collaboration under applicable RC bindings |
| **Participant** | Any RS service that executes a material act within the collaboration |
| **Specialist** | A participant invoked for a published specialised responsibility (e.g. evidence, tips, state, audit) |
| **Gate** | A participant whose published disposition lawfully enables or refuses continuation |
| **Recorder** | Typically RS-07 when audit obligations apply to the collaboration |

Roles describe *how a recognised RS participates in a pattern*. They never invent unpublished services or reassign constitutional ownership.

---

## 4. RSC-01 — Sequential Collaboration

### Constitutional purpose

Coordinate authorised RS services so that published responsibilities are fulfilled in a **lawful order**, with each step consuming published artefacts from the prior step — without collapsing steps into one mega-service or treating order as ownership.

### Participating service roles

- **Initiator** — opens the sequence under RC bindings (often RS-01 or RS-03 / RS-04).
- **Participants** — successive RS-01…RS-07 services required by published law.
- **Recorder** — RS-07 when material steps require audit composition.

### Permitted collaboration

- Hand off published constitutional artefacts in published order (dispositions, evidence records, workflow events, recommendation artefacts, state postures, audit refs).
- Require each step’s own RC bindings before that step’s material act.
- Refuse / defer / escalate the sequence when a step’s published law requires stop.
- Compose with other RSC patterns for nested specialised handoffs (e.g. sequential + delegated).

### Prohibited collaboration

- Skipping required specialised steps for product convenience.
- Merging successive RS responsibilities into the initiator’s catalogue.
- Treating “previous step succeeded” as substitute for the next step’s RC authorisation.
- Reinterpreting artefacts in transit between steps.
- Inventing unpublished intermediate mega-capabilities to “simplify the chain.”

### Expected constitutional outputs

- Ordered execution records citing each participant, contracts, and artefacts exchanged.
- Authorised final dispositions / surfaced artefacts for the sequence as published law requires.
- Continuity-preserving audit trail across the sequence (via RS-07 when applicable).
- Explicit refuse / defer / escalate outcomes when the sequence must stop.

---

## 5. RSC-02 — Parallel Collaboration

### Constitutional purpose

Coordinate authorised RS services so that **independent published responsibilities** may execute concurrently under shared constitutional law — without race-dependent educational meaning, ownership disposition, or silent winner-takes-all authorship.

### Participating service roles

- **Initiator** — opens the parallel set under RC bindings that authorise concurrent composition.
- **Participants** — RS services whose published responsibilities do not require serial dependence for the acts being coordinated.
- **Recorder** — RS-07 for shared reconstructable trails across concurrent acts.

### Permitted collaboration

- Execute independent authorised acts under the same published cycle / concern when law permits concurrency.
- Exchange only published artefacts; share read-only published context without mutual absorption.
- Join concurrent results only under published composition / completion rules (WS1 / WS2 completion law as applicable).
- Refuse the parallel set when concurrency would invent educational meaning or ownership disposition.

### Prohibited collaboration

- Letting infrastructure races decide tips, ownership, mastery, or state.
- Merging concurrent participants into one unpublished composite service.
- Using parallelism to bypass a required serial gate (authority, evidence eligibility, contract check).
- Presenting “first finished” as constitutional warrant.
- Erasing loser-branch provenance to simplify audit.

### Expected constitutional outputs

- Concurrent execution records for each participant with shared collaboration identity.
- Published join / non-join dispositions under completion or composition law.
- Shared audit trail that preserves each participant’s constitutional refs.
- Honest refuse / defer when concurrency is not constitutionally authorised.

---

## 6. RSC-03 — Delegated Collaboration

### Constitutional purpose

Allow an authorised RS service to **request specialised execution** from another authorised RS service without absorbing the specialist’s responsibilities or transferring constitutional ownership to the caller.

### Participating service roles

- **Initiator (delegator)** — retains its own MS001 responsibilities; requests specialised help.
- **Specialist (delegate)** — executes only its published permitted responsibilities under its own RC bindings.
- **Recorder** — RS-07 when the delegation is material.

### Permitted collaboration

- Invoke another authorised RS service to fulfil a published specialised responsibility (e.g. RS-04 → RS-05 for tips; RS-04 → RS-02 for evidence honesty; any → RS-07 for audit).
- Return published artefacts / dispositions from specialist to initiator without reclassification.
- Refuse delegation when the specialist’s RC conditions fail.
- Narrate delegation without claiming the initiator “became” the specialist.

### Prohibited collaboration

- Absorbing the specialist’s permitted responsibilities into the initiator.
- Transferring ownership of tip warrant, evidence classification, state law, or authority domains by call proximity.
- Skipping the specialist’s RC bindings because the initiator was already authorised for *its* act.
- Inventing tip text, evidence classes, or state postures “on behalf of” the specialist.
- Treating delegation as a permanent reassignment of MS001 catalogue duties.

### Expected constitutional outputs

- Delegation records naming delegator, specialist, contracts for each, and artefacts returned.
- Specialist dispositions / surfaced artefacts remaining under specialist provenance.
- Audit composition preserving non-absorption.
- Refuse / defer / escalate when specialised law cannot be fulfilled.

---

## 7. RSC-04 — Conditional Collaboration

### Constitutional purpose

Coordinate authorised RS services so that continuation, branching, or stop follows **published dispositions and conditions** — not product preference, A/B winners, or undocumented heuristics.

### Participating service roles

- **Gate** — typically RS-01 (contract disposition), RS-03 (event evaluation), RS-02 (evidence / eligibility), or RC-04-gated authority checks via applicable RS composition.
- **Participants** — RS services enabled only when published gate outcomes permit.
- **Recorder** — RS-07 for gate and branch auditability.

### Permitted collaboration

- Branch to specialised RS acts only when published conditions / dispositions authorise continuation.
- Prefer refuse / defer / escalate branches when law requires stop.
- Compose gate outcomes as published artefacts for downstream participants.
- Explain why a branch was taken or refused without inventing new conditions.

### Prohibited collaboration

- Inventing unpublished conditions or “temporary gates” for convenience.
- Treating feature flags, UI mode, or queue depth as constitutional gates unless published law maps them.
- Continuing after a refuse disposition by renaming the call.
- Using conditional branching to redefine Programme VI meaning or Programme VII ownership.
- Presenting optimiser confidence as a constitutional condition.

### Expected constitutional outputs

- Gate evaluation records citing published conditions and RC bindings.
- Branch participation records for taken / refused paths.
- Authorised outputs only on lawfully enabled branches.
- Explicit stop speech when conditions fail.

---

## 8. RSC-05 — Evidence-Driven Collaboration

### Constitutional purpose

Coordinate authorised RS services so that material educational execution is **gated by published constitutional evidence honesty** under Programme VIII WS2 and EIP-002 — without reinterpreting, reclassifying, or inventing warrants in the collaboration path.

### Participating service roles

- **Evidence participant** — RS-02 (and validation outcomes under WS2 / MS002 EV law as required).
- **Dependent participants** — RS-04 / RS-05 / RS-06 / others whose published law requires lawful evidence before acting.
- **Gate** — evidence consumption / validation dispositions as published.
- **Recorder** — RS-07 for evidence provenance through the collaboration.

### Permitted collaboration

- Require published EC artefacts and required EV eligibility before dependent RS acts.
- Exchange evidence consumption / validation records exactly as classified.
- Refuse / understate / defer dependent collaboration when evidence is incomplete, conflicting, or ineligible.
- Preserve claim-ladder honesty into downstream tip / workflow / state speech.

### Prohibited collaboration

- Reclassifying evidence between services (e.g. treating session completion as mastery mid-handoff).
- Minting Estimated Knowledge / Mastery to unblock collaboration.
- Bypassing RS-02 because another service “already has the data.”
- Presenting Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Inventing new EC / EV categories by collaboration convenience.

### Expected constitutional outputs

- Evidence consumption / validation records attached to the collaboration identity.
- Dependent execution records only when eligibility / consumption law is satisfied — or honest refuse.
- Provenance-intact artefacts for tips / workflows / state that required evidence.
- Audit trails showing claim-class honesty was preserved.

---

## 9. RSC-06 — Event-Driven Collaboration

### Constitutional purpose

Coordinate authorised RS services so that collaboration is **initiated or continued by published constitutional events** under Programme VIII WS1 / MS002 — without inventing event types or treating delivery technology as constitutional stimulus.

### Participating service roles

- **Initiator / event participant** — RS-03 receives, evaluates, and maps published CE events.
- **Downstream participants** — RS-04 and specialised RS services required by published event → responsibility mappings.
- **Recorder** — RS-07 for event and handoff traces.

### Permitted collaboration

- Open or continue collaboration only from published CE classes under event-processing law.
- Hand off published event evaluation dispositions to specialised RS participants.
- Execute only published event → responsibility mappings under RC bindings.
- Emit only published CE classes when law requires emission as part of collaboration.

### Prohibited collaboration

- Inventing event types, payload meanings, or “implicit events” from product convenience.
- Treating UI clicks, cron ticks, bus deliveries, or queue receipts as constitutional events unless a published CE mapping says so.
- Using event-driven collaboration to redefine Programme VI meaning or Programme VII ownership.
- Bypassing contracts by claiming “the event arrived, so collaboration must proceed.”
- Presenting successful event-driven collaboration as mastery, plan completion, or constitutional amendment.

### Expected constitutional outputs

- Event processing records (receive / evaluate / execute) bound to the collaboration.
- Downstream RS execution records authorised by published mappings and RC bindings.
- Published event traces required for explainability and audit.
- Refuse / defer / escalate when event law does not authorise continuation.

---

## 10. RSC-07 — Audit Collaboration

### Constitutional purpose

Ensure that collaborations among RS-01…RS-06 **preserve reconstructable constitutional trails** under RC-07 — without turning audit into a second educational authority, a responsibility sink, or a mere technical log shipper.

### Participating service roles

- **Recorder** — RS-07 Audit Service.
- **Participants** — any RS-01…RS-06 services whose material acts belong to the collaboration.
- **Initiator** — may be any authorised RS; audit composition does not transfer their duties to RS-07.

### Permitted collaboration

- Capture constitutional references for each material participant: service identity, RSC pattern, RC bindings, artefacts exchanged, outputs, boundary checks.
- Compose audit with every other RSC pattern without absorbing educational responsibilities.
- Mark incomplete collaborative trails as constitutionally defective.
- Support RSCO-04 auditability and collaboration explainability questions.

### Prohibited collaboration

- Inventing educational meaning, tips, ownership, or state “for the audit narrative.”
- Reclassifying evidence by storytelling in collaborative audit text.
- Erasing participant history to simplify storage or UX.
- Substituting scores, latency, hop counts, or engagement metrics for constitutional references.
- Treating log shippers, analytics products, or dashboards as the Audit Collaboration definition.
- Claiming RS-07 ownership of the educational acts it records.

### Expected constitutional outputs

- Constitutional audit records covering the collaboration graph.
- Continuity-preserving history across retries, replacements, and redeploys.
- Refusal / incompleteness markers when required components are missing.
- Explainability-aligned components for student-plain vs developer vocabulary over one truth.

---

## 11. Catalogue Rules

1. **Closed catalogue.** New RSC patterns require a Programme VIII constitutional amendment — not a silent orchestration invention.
2. **Participant honesty.** Every participant must be a recognised RS-01…RS-07 service.
3. **Contract binding.** Every material act inside a pattern consumes one or more RC-01…RC-07 contracts.
4. **Composition, not absorption.** Patterns coordinate; they never transfer ownership or merge responsibilities.
5. **Artefact honesty.** Only published constitutional artefacts may be exchanged.
6. **Namespace honesty.** RSC-* must not be confused with RS-*, RC-*, or Recovery Strategy RS-* elsewhere.
7. **Technology silence.** Catalogue entries never mandate orchestration engines, DI, buses, microservices, REST, queues, schedulers, workers, or databases.
8. **Replaceability.** Any compliant implementation may realise an RSC pattern; none may monopolise constitutional coordination truth.
9. **MS001 supremacy for duties.** Pattern selection never alters the Runtime Service Model catalogue.

---

## 12. Closing Statement

> **If a coordination among runtime services cannot name its RSC pattern, its RS participants, its RC bindings, the artefacts exchanged, and the responsibilities preserved, it is not yet constitutional collaboration — and must not be exposed as educational law.**
