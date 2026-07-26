# Interface Types

**Programme:** VIII — Workstream 4 — Constitutional Runtime Interfaces  
**Milestone:** MS001 — Runtime Interface Model  
**Classification:** Closed catalogue of recognised constitutional runtime interfaces  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional runtime interface categories** (RI-01…RI-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RUNTIME_INTERFACE_MODEL.md`](RUNTIME_INTERFACE_MODEL.md)
3. [`INTERFACE_OBJECTIVES.md`](INTERFACE_OBJECTIVES.md)
4. Programme VI corpora under [`../../educational/`](../../educational/)
5. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
6. Programme VIII WS1 corpora under [`../contracts/`](../contracts/), [`../event_processing/`](../event_processing/), [`../execution_completion/`](../execution_completion/)
7. Programme VIII WS2 corpora under [`../evidence_consumption/`](../evidence_consumption/), [`../evidence_validation/`](../evidence_validation/), [`../evidence_completion/`](../evidence_completion/)
8. Programme VIII WS3 corpora under [`../services/`](../services/), [`../service_collaboration/`](../service_collaboration/), [`../service_completion/`](../service_completion/)
9. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published interface types may expose material constitutional capabilities.  
> Unpublished “implied interfaces” are constitutionally defective.**

**Namespace note.** RI-* here means **Runtime Interface**. Other historical RI-* abbreviations elsewhere in the knowledge tree are separate namespaces; path `knowledge/runtime/interfaces/` always disambiguates.

---

## 1. Purpose

Runtime without a closed interface catalogue invents authority by proximity: whichever transport happens to hold the call becomes the tutor.

This catalogue names the only lawful interaction contracts between published runtime capabilities and authorised constitutional consumers.

---

## 2. Catalogue Overview

| ID | Interface | Primary capabilities exposed | Primary constitutional focus |
|----|-----------|------------------------------|------------------------------|
| **RI-01** | Contract Interface | RS-01 (+ RC catalogue) | Expose contract-gated execution capabilities |
| **RI-02** | Evidence Interface | RS-02 (+ WS2 consumption / validation) | Expose published evidence consumption capabilities |
| **RI-03** | Event Interface | RS-03 (+ WS1 event processing) | Expose published event-processing capabilities |
| **RI-04** | Service Interface | RS-01…RS-07 catalogue access | Expose published service capabilities as a catalogue boundary |
| **RI-05** | Execution Interface | RS-04 / RS-05 / RS-06 (+ completion) | Expose workflow / recommendation / state execution capabilities |
| **RI-06** | Audit Interface | RS-07 (+ RC-07) | Expose reconstructable constitutional audit capabilities |
| **RI-07** | Diagnostic Interface | Read-only inspection over published law | Expose non-mutating constitutional diagnostic capabilities |

Material interface interactions must map to one or more of these types. Cross-cutting interactions (for example an execution call that also requires audit) may bind multiple RIs simultaneously; none may be silently skipped when their responsibility applies.

Interfaces may **compose** other recognised interfaces. Composition does not transfer authorship: each composed interface remains an interaction contract under its own permitted exposures. Lawful composition patterns are governed by [`../interface_composition/`](../interface_composition/) (Programme VIII / WS4 / MS002 — RIC-01…RIC-07).

---

## 3. RI-01 — Contract Interface

### Constitutional purpose

Expose **contract-gated execution capabilities** so authorised consumers may request evaluation and disposition under published RC-01…RC-07 bindings — without inventing contracts or educational meaning.

### Constitutional consumers

- Authorised runtime services (especially RS-01 and composing RS services).
- Authorised adapters that must obtain a lawful execute / refuse / defer / escalate disposition.
- Downstream product surfaces that may observe dispositions — never author contracts.

### Constitutional providers

- Runtime Contract Model (RC-01…RC-07) as published law.
- Contract Execution Service (RS-01) as the capability fulfils the interaction.
- Constitution / EIP / Programme VI / Programme VII corpora cited by the bound contracts.

### Constitutional inputs

- Named RC-01…RC-07 contract binding(s) applicable to the request.
- Published constitutional rules / conditions cited by those contracts.
- Concrete learner circumstances against which published conditions are evaluated.
- Optional composition context from other authorised RI / RS interactions.

### Constitutional outputs

- Authorised execution dispositions (execute / refuse / defer / escalate).
- Authorised execution records citing contract identity and corpus producers.
- Explicit refusal when no published contract authorises the request.

### Permitted interaction

- Request evaluation of published constitutional conditions under named RC bindings.
- Receive only dispositions and records already authorised by those contracts.
- Compose with RI-06 when material acts require audit exposure.
- Refuse unpublished contract invents at the boundary.

### Prohibited interaction

- Invent unpublished contracts, conditions, or educational meanings via request shape.
- Treat protocol success, A/B winners, or product preference as constitutional authorisation.
- Bypass RC catalogue by renaming an endpoint “contract-like.”
- Claim interface success as proof of mastery, pass certainty, or educational truth amendment.

---

## 4. RI-02 — Evidence Interface

### Constitutional purpose

Expose **published constitutional evidence consumption and validation capabilities** so authorised consumers may receive evidence exactly as classified — without reinterpreting, altering, or reclassifying warrants.

### Constitutional consumers

- Authorised runtime services (especially RS-02).
- Authorised adapters that must consume EIP-002 / WS2 artefacts for lawful execution.
- Audit and diagnostic consumers that may observe evidence references — never reclassify them.

### Constitutional providers

- Evidence Model (EIP-002), Knowledge & Mastery (EIP-006), and EIP-001 permitted writers.
- Programme VIII WS2 Evidence Consumption / Validation / Completion Models.
- Evidence Consumption Service (RS-02) as the fulfilling capability.

### Constitutional inputs

- Published evidence artefact references and claim-class identifiers.
- Contemplated consumption / validation purpose under WS2 law.
- Optional learner-circumstance context required by published validation types.

### Constitutional outputs

- Evidence as published (classifications intact).
- Validation eligibility dispositions under WS2 / EV law when requested.
- Honest understatement / refusal when evidence is incomplete, conflicting, or ineligible.

### Permitted interaction

- Request lawful receipt and consumption of published evidence artefacts.
- Request validation of execution eligibility without altering evidence.
- Preserve claim-ladder honesty (coverage ≠ understanding ≠ mastery) through the boundary.
- Preserve continuity of evidence history (EIP-005).

### Prohibited interaction

- Reclassify evidence classes at the interface (e.g. treating session completion as mastery).
- Alter, erase, or rewrite evidence payloads to simplify UX or protocol shape.
- Mint Estimated Knowledge / Mastery from interface convenience alone.
- Present Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Bypass Evidence Model succession rules with “temporary” certainty headers.

---

## 5. RI-03 — Event Interface

### Constitutional purpose

Expose **published constitutional event-processing capabilities** so authorised consumers may submit or receive CE-class stimuli under WS1 / MS002 law — without inventing event classes or creating constitutional behaviour.

### Constitutional consumers

- Authorised runtime services (especially RS-03).
- Authorised adapters that must deliver or observe published constitutional events.
- Audit consumers that may observe event trails — never invent event meanings.

### Constitutional providers

- Constitutional Event Processing Model (Programme VIII / WS1 / MS002).
- Event Processing Service (RS-03) as the fulfilling capability.
- Programme VII / VI corpora that publish the event classes being processed.

### Constitutional inputs

- Published constitutional event class identity and payload as classified.
- Processing intent already authorised under event-processing law (receive / evaluate / emit).
- Optional workflow / contract context required by published event rules.

### Constitutional outputs

- Event-processing dispositions (accepted / refused / deferred / escalated).
- Authorised published event emissions when law requires emission.
- Processing records citing event class and authorising corpus.

### Permitted interaction

- Submit published CE-class events for lawful processing.
- Observe published event outcomes and required emissions.
- Compose with RI-01 / RI-05 when event processing advances execution.
- Refuse unpublished event invents at the boundary.

### Prohibited interaction

- Invent unpublished event classes, meanings, or side effects via interface shape.
- Use events to redefine Programme VI educational meaning or Programme VII ownership.
- Treat transport delivery guarantees as educational truth amendments.
- Bypass event-processing law because a message bus “already fired.”

---

## 6. RI-04 — Service Interface

### Constitutional purpose

Expose the **published runtime service catalogue** as a constitutional capability boundary — so authorised consumers may discover and invoke RS-01…RS-07 capabilities without inventing services or redistributing responsibilities.

### Constitutional consumers

- Authorised runtime collaborators under WS3 / MS002 collaboration law.
- Authorised adapters that must invoke published RS capabilities.
- Product surfaces that may invoke services — never mint new RS types.

### Constitutional providers

- Runtime Service Model (RS-01…RS-07).
- Runtime Service Collaboration / Completion Models for lawful composition.
- The specific RS capability that fulfils a given invocation.

### Constitutional inputs

- Named RS-01…RS-07 capability identity.
- Published constitutional inputs required by that service type.
- Optional collaboration pattern identity (RSC-*) when composition is requested.

### Constitutional outputs

- Authorised service execution outputs as defined by the invoked RS type.
- Collaboration dispositions that preserve (never redistribute) responsibilities.
- Explicit refusal when the requested capability is unpublished or out of catalogue.

### Permitted interaction

- Request invocation of published RS capabilities under published inputs.
- Request lawful collaboration among published capabilities without merging ownership.
- Observe catalogue membership as constitutional fact — not as a marketing list.
- Compose with RI-06 for material service acts requiring audit.

### Prohibited interaction

- Invent unpublished services, responsibilities, or collaboration patterns at the boundary.
- Transfer or merge constitutional responsibilities via interface naming.
- Treat microservice layout, DI graphs, or module folders as the service catalogue.
- Bypass WS3 collaboration / completion law through “direct” internal calls presented as interface success.

---

## 7. RI-05 — Execution Interface

### Constitutional purpose

Expose **workflow, recommendation, and educational-state execution capabilities** so authorised consumers may request published execution acts — without inventing stages, tips, context postures, or execution policy.

### Constitutional consumers

- Authorised runtime services (especially RS-04, RS-05, RS-06).
- Authorised adapters coordinating learner-facing execution under Programme VII law.
- Product surfaces that may observe execution outcomes — never author orchestration.

### Constitutional providers

- Workflow Execution / Recommendation Execution / State Execution Services (RS-04…RS-06).
- Programme VII WS1–WS4 corpora for workflow, tips, and EST/CST law.
- Programme VIII WS1 Execution Completion Model for cycle-fulfilment meaning.

### Constitutional inputs

- Named execution responsibility class (workflow / recommendation / state) and cited corpus refs.
- Published conditions, artefacts, or postures required for the requested act.
- Optional completion-evaluation context when fulfilment status is requested.

### Constitutional outputs

- Authorised execution dispositions and published artefacts (workflow events, recommendation surfaces, EST/CST postures).
- Execution-completion judgements only as published fulfilment of responsibilities — never as educational success.
- Explicit refuse / defer / escalate when warrants fail.

### Permitted interaction

- Request lawful workflow advancement under published stages and transitions.
- Request lawful recommendation surfacing under WS3 + Programme VI owners.
- Request lawful EST/CST representation under WS4 law.
- Request execution-completion evaluation under published completion criteria.

### Prohibited interaction

- Bypass workflow stages, invent tips, or invent educational state via interface shape.
- Treat execution-completion as mastery, pass certainty, or constitutional change.
- Redefine ownership or mint recommendations under an “execution” label alone.
- Present ranking scores as constitutional educational warrant.
- Use the interface to modify constitutional specifications or execution policy.

---

## 8. RI-06 — Audit Interface

### Constitutional purpose

Expose **reconstructable constitutional audit capabilities** so authorised consumers may record or retrieve material interaction trails — without inventing constitutional refs after the fact or using audit as a second constitution.

### Constitutional consumers

- All material RI / RS interactions that bind audit obligations.
- Authorised auditors, developers, and continuity-safe history consumers.
- Diagnostic consumers (RI-07) that may read audit trails — never rewrite them into new law.

### Constitutional providers

- Audit Service (RS-07) and Audit Contract (RC-07).
- EIP-003 / EIP-005 and this Programme VIII Runtime Interface Model.
- Producer corpora of the audited act (RI-01…RI-05 / RI-07 as applicable).

### Constitutional inputs

- Identity of the audited interface interaction and bound RI / RS / RC refs.
- Constitutional evidence / warrant refs actually consumed (if any).
- Constitutional outputs / events / dispositions actually produced.
- Boundary-preservation checks performed.

### Constitutional outputs

- Reconstructable audit records answering interface / capability / inputs / outputs / boundaries.
- Continuity-safe history across retries and replacements.
- Explicit defect signals when required audit components are missing.

### Permitted interaction

- Record which RI interface(s) were used.
- Record which constitutional capability was exposed.
- Record which constitutional inputs were received and outputs returned.
- Record which constitutional boundaries were preserved.
- Retrieve prior lawful audit trails without erasing history.

### Prohibited interaction

- Emit audit theatre that invents constitutional refs after the fact.
- Strip constitutional provenance while keeping technical access logs only.
- Use audit records to redefine educational meaning or ownership.
- Treat missing audit as acceptable for “low-risk” educational mutations or primary student-facing tips.
- Present analytics dashboards as substitutes for constitutional audit obligations.

---

## 9. RI-07 — Diagnostic Interface

### Constitutional purpose

Expose **non-mutating constitutional diagnostic capabilities** so authorised consumers may inspect published law, capability readiness, and boundary posture — without creating constitutional behaviour, altering evidence, or becoming an execution authority.

### Constitutional consumers

- Authorised developers, auditors, and operators performing constitutional inspection.
- Authorised runtime collaborators that must confirm readiness before material execution.
- Product surfaces that may display honest diagnostic summaries — never invent educational claims from diagnostics alone.

### Constitutional providers

- Published Constitution / EIP / Programme VI / VII / VIII corpora as inspection sources.
- Read-only projections of RI / RS / RC catalogue membership and boundary posture.
- Audit Interface (RI-06) trails when diagnosis requires historical reconstruction.

### Constitutional inputs

- Diagnostic scope limited to published catalogues, corpus refs, and non-mutating inspection questions.
- Optional audit-trail references for historical diagnosis.
- Explicit non-execution intent (inspect / report — not execute).

### Constitutional outputs

- Diagnostic reports describing published catalogue membership, cited corpora, and boundary posture.
- Honesty flags for missing warrants, incomplete audit, or unpublished request shapes.
- Explicit non-claims: diagnosis is not mastery, not pass certainty, not corpus amendment.

### Permitted interaction

- Inspect which RI / RS / RC types are published and applicable.
- Inspect whether required constitutional inputs appear present for a contemplated act.
- Inspect boundary posture and prior audit trails in read-only form.
- Refuse any diagnostic request that would mutate evidence, state, or specifications.

### Prohibited interaction

- Mutate evidence, state, recommendations, ownership, or specifications under a diagnostic label.
- Execute workflows or mint tips because diagnosis “looked ready.”
- Expose implementation internals (stack traces, private schemas, adapter paths) as constitutional law.
- Present diagnostic confidence scores as educational warrant.
- Use diagnosis to bypass contracts or invent unpublished capabilities.

---

## 10. Composition Rules

1. **Primary mapping required.** Every material interface interaction names at least one primary RI.
2. **Capability honesty.** RI exposures must map to published RS / WS1 / WS2 capabilities — never invent parallel catalogues.
3. **Evidence before certainty.** Interactions that claim understanding or mastery bind RI-02.
4. **Events ≠ meaning.** RI-03 never substitutes for Programme VI meaning or tip law.
5. **Execution ≠ success.** RI-05 completion outputs never certify educational success or constitutional change.
6. **Audit always.** RI-06 binds every material interaction in RI-01…RI-05 (and material RI-07 inspections that claim reconstructability).
7. **Diagnosis never executes.** RI-07 is non-mutating; execution requires RI-01 / RI-05 (as applicable).
8. **Closed catalogue.** New RI types require a Programme VIII constitutional amendment — not a silent SDK invention.

---

## 11. Closing Statement

> **Runtime may expose constitutional capabilities only through recognised interfaces.  
> Outside this catalogue there is no lawful constitutional interaction — only protocol improvisation.**
