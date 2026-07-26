# API Types

**Programme:** VIII — Workstream 5 — Constitutional Runtime APIs  
**Milestone:** MS001 — Runtime API Model  
**Classification:** Closed catalogue of recognised constitutional runtime APIs  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional runtime API categories** (RA-01…RA-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RUNTIME_API_MODEL.md`](RUNTIME_API_MODEL.md)
3. [`API_OBJECTIVES.md`](API_OBJECTIVES.md)
4. Programme VI corpora under [`../../educational/`](../../educational/)
5. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
6. Programme VIII WS1 corpora under [`../contracts/`](../contracts/), [`../event_processing/`](../event_processing/), [`../execution_completion/`](../execution_completion/)
7. Programme VIII WS2 corpora under [`../evidence_consumption/`](../evidence_consumption/), [`../evidence_validation/`](../evidence_validation/), [`../evidence_completion/`](../evidence_completion/)
8. Programme VIII WS3 corpora under [`../services/`](../services/), [`../service_collaboration/`](../service_collaboration/), [`../service_completion/`](../service_completion/)
9. Programme VIII WS4 corpora under [`../interfaces/`](../interfaces/), [`../interface_composition/`](../interface_composition/), [`../interface_completion/`](../interface_completion/)
10. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published API types may expose material constitutional runtime interfaces.  
> Unpublished “implied APIs” are constitutionally defective.**

**Namespace note.** RA-* here means **Runtime API**. Other historical RA-* abbreviations elsewhere in the knowledge tree are separate namespaces; path `knowledge/runtime/apis/` always disambiguates. RA APIs expose RI interfaces; they never replace them.

---

## 1. Purpose

Runtime without a closed API catalogue invents authority by proximity: whichever transport happens to hold the call becomes the tutor.

This catalogue names the only lawful exposure contracts between published runtime interfaces and authorised constitutional consumers.

---

## 2. Catalogue Overview

| ID | API | Primary interface exposed | Primary constitutional focus |
|----|-----|---------------------------|------------------------------|
| **RA-01** | Contract API | RI-01 Contract Interface | Expose contract-gated interface interactions |
| **RA-02** | Evidence API | RI-02 Evidence Interface | Expose published evidence-interface interactions |
| **RA-03** | Event API | RI-03 Event Interface | Expose published event-interface interactions |
| **RA-04** | Service API | RI-04 Service Interface | Expose published service-catalogue interface interactions |
| **RA-05** | Execution API | RI-05 Execution Interface | Expose workflow / recommendation / state execution-interface interactions |
| **RA-06** | Audit API | RI-06 Audit Interface | Expose reconstructable constitutional audit-interface interactions |
| **RA-07** | Diagnostic API | RI-07 Diagnostic Interface | Expose non-mutating constitutional diagnostic-interface interactions |

Material API interactions must map to one or more of these types. Cross-cutting interactions (for example an execution call that also requires audit) may bind multiple RAs simultaneously; none may be silently skipped when their responsibility applies.

APIs may **compose** other recognised APIs when the bound RI composition law requires cross-cutting exposure. Composition does not transfer authorship: each composed API remains an exposure contract under its own permitted exposures, and each bound RI remains the interaction contract defined by WS4.

---

## 3. RA-01 — Contract API

### Constitutional purpose

Expose the **published Contract Interface (RI-01)** so authorised consumers may request evaluation and disposition under published RC-01…RC-07 bindings — without inventing contracts, redefining RI-01, or creating educational meaning.

### Constitutional consumers

- Authorised runtime collaborators that must obtain a lawful execute / refuse / defer / escalate disposition via RI-01.
- Authorised adapters that must invoke contract-gated exposure without owning contract law.
- Downstream product surfaces that may observe dispositions — never author contracts or redefine RI-01.

### Constitutional providers

- Runtime Interface Model — RI-01 as the published interaction contract being exposed.
- Runtime Contract Model (RC-01…RC-07) and Contract Execution Service (RS-01) as the fulfilment path beneath RI-01.
- Constitution / EIP / Programme VI / Programme VII corpora cited by the bound contracts.

### Constitutional inputs

- Named RA-01 exposure intent bound to RI-01.
- Named RC-01…RC-07 contract binding(s) applicable to the request.
- Published constitutional rules / conditions cited by those contracts.
- Concrete learner circumstances against which published conditions are evaluated.
- Optional composition context from other authorised RA / RI interactions.

### Constitutional outputs

- Authorised execution dispositions (execute / refuse / defer / escalate) as returned through RI-01.
- Authorised execution records citing contract identity, interface identity, and corpus producers.
- Explicit refusal when no published contract or interface authorises the request.

### Permitted exposure

- Expose RI-01 for evaluation of published constitutional conditions under named RC bindings.
- Accept only authorised constitutional requests already lawful under RI-01.
- Return only dispositions and records already authorised by those contracts / interface.
- Compose with RA-06 when material acts require audit exposure.
- Refuse unpublished contract or interface invents at the exposure boundary.

### Prohibited exposure

- Redefine RI-01 semantics, invent unpublished contracts, or invent educational meanings via request shape.
- Treat protocol success, A/B winners, or product preference as constitutional authorisation.
- Bypass RC catalogue or RI-01 by renaming an endpoint “contract-like.”
- Expose implementation internals (handlers, private schemas, adapter paths) as constitutional law.
- Claim API success as proof of mastery, pass certainty, or educational truth amendment.

---

## 4. RA-02 — Evidence API

### Constitutional purpose

Expose the **published Evidence Interface (RI-02)** so authorised consumers may receive evidence exactly as classified — without reinterpreting, altering, reclassifying warrants, or redefining RI-02.

### Constitutional consumers

- Authorised runtime collaborators that must consume EIP-002 / WS2 artefacts via RI-02.
- Authorised adapters that must obtain lawful evidence exposure without owning evidence law.
- Audit and diagnostic consumers that may observe evidence references — never reclassify them.

### Constitutional providers

- Runtime Interface Model — RI-02 as the published interaction contract being exposed.
- Evidence Model (EIP-002), Knowledge & Mastery (EIP-006), EIP-001 permitted writers, and Programme VIII WS2 models.
- Evidence Consumption Service (RS-02) as the fulfilling capability beneath RI-02.

### Constitutional inputs

- Named RA-02 exposure intent bound to RI-02.
- Published evidence artefact references and claim-class identifiers.
- Contemplated consumption / validation purpose under WS2 law.
- Optional learner-circumstance context required by published validation types.

### Constitutional outputs

- Evidence as published (classifications intact) through RI-02.
- Validation eligibility dispositions under WS2 / EV law when requested.
- Honest understatement / refusal when evidence is incomplete, conflicting, or ineligible.

### Permitted exposure

- Expose RI-02 for lawful receipt and consumption of published evidence artefacts.
- Request validation of execution eligibility without altering evidence.
- Preserve claim-ladder honesty (coverage ≠ understanding ≠ mastery) through the exposure boundary.
- Preserve continuity of evidence history (EIP-005).

### Prohibited exposure

- Redefine RI-02 or reclassify evidence classes at the API (e.g. treating session completion as mastery).
- Alter, erase, or rewrite evidence payloads to simplify UX or protocol shape.
- Mint Estimated Knowledge / Mastery from API convenience alone.
- Present Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Bypass Evidence Model succession rules with “temporary” certainty headers.
- Expose implementation internals as constitutional warrants.

---

## 5. RA-03 — Event API

### Constitutional purpose

Expose the **published Event Interface (RI-03)** so authorised consumers may submit or receive CE-class stimuli under WS1 / MS002 law — without inventing event classes, creating constitutional behaviour, or redefining RI-03.

### Constitutional consumers

- Authorised runtime collaborators that must deliver or observe published constitutional events via RI-03.
- Authorised adapters that must obtain event exposure without owning event-processing law.
- Audit consumers that may observe event trails — never invent event meanings.

### Constitutional providers

- Runtime Interface Model — RI-03 as the published interaction contract being exposed.
- Constitutional Event Processing Model (Programme VIII / WS1 / MS002).
- Event Processing Service (RS-03) as the fulfilling capability beneath RI-03.
- Programme VII / VI corpora that publish the event classes being processed.

### Constitutional inputs

- Named RA-03 exposure intent bound to RI-03.
- Published constitutional event class identity and payload as classified.
- Processing intent already authorised under event-processing law (receive / evaluate / emit).
- Optional workflow / contract context required by published event rules.

### Constitutional outputs

- Event-processing dispositions (accepted / refused / deferred / escalated) through RI-03.
- Authorised published event emissions when law requires emission.
- Processing records citing event class, interface identity, and authorising corpus.

### Permitted exposure

- Expose RI-03 for submission of published CE-class events for lawful processing.
- Observe published event outcomes and required emissions.
- Compose with RA-01 / RA-05 when event processing advances execution.
- Refuse unpublished event invents at the exposure boundary.

### Prohibited exposure

- Redefine RI-03 or invent unpublished event classes, meanings, or side effects via API shape.
- Use events to redefine Programme VI educational meaning or Programme VII ownership.
- Treat transport delivery guarantees as educational truth amendments.
- Bypass event-processing law because a message bus “already fired.”
- Expose implementation internals as constitutional event law.

---

## 6. RA-04 — Service API

### Constitutional purpose

Expose the **published Service Interface (RI-04)** as a constitutional capability-catalogue boundary — so authorised consumers may discover and invoke RS-01…RS-07 capabilities without inventing services, redistributing responsibilities, or redefining RI-04.

### Constitutional consumers

- Authorised runtime collaborators under WS3 / MS002 collaboration law that must invoke RS capabilities via RI-04.
- Authorised adapters that must obtain service-catalogue exposure without owning the service catalogue.
- Product surfaces that may invoke services — never mint new RS or RI types.

### Constitutional providers

- Runtime Interface Model — RI-04 as the published interaction contract being exposed.
- Runtime Service Model (RS-01…RS-07) and Collaboration / Completion Models for lawful composition.
- The specific RS capability that fulfils a given invocation beneath RI-04.

### Constitutional inputs

- Named RA-04 exposure intent bound to RI-04.
- Named RS-01…RS-07 capability identity.
- Published constitutional inputs required by that service type.
- Optional collaboration pattern identity (RSC-*) when composition is requested.

### Constitutional outputs

- Authorised service execution outputs as defined by the invoked RS type, returned through RI-04.
- Collaboration dispositions that preserve (never redistribute) responsibilities.
- Explicit refusal when the requested capability or interface is unpublished or out of catalogue.

### Permitted exposure

- Expose RI-04 for invocation of published RS capabilities under published inputs.
- Request lawful collaboration among published capabilities without merging ownership.
- Observe catalogue membership as constitutional fact — not as a marketing list.
- Compose with RA-06 for material service acts requiring audit.

### Prohibited exposure

- Redefine RI-04 or invent unpublished services, responsibilities, or collaboration patterns at the API.
- Transfer or merge constitutional responsibilities via API naming.
- Treat microservice layout, DI graphs, OpenAPI tags, or module folders as the service catalogue.
- Bypass WS3 collaboration / completion law through “direct” internal calls presented as API success.
- Expose implementation internals as constitutional service law.

---

## 7. RA-05 — Execution API

### Constitutional purpose

Expose the **published Execution Interface (RI-05)** so authorised consumers may request published workflow, recommendation, and educational-state execution acts — without inventing stages, tips, context postures, execution policy, or redefining RI-05.

### Constitutional consumers

- Authorised runtime collaborators that must coordinate learner-facing execution via RI-05.
- Authorised adapters coordinating under Programme VII law without owning orchestration.
- Product surfaces that may observe execution outcomes — never author orchestration or redefine RI-05.

### Constitutional providers

- Runtime Interface Model — RI-05 as the published interaction contract being exposed.
- Workflow Execution / Recommendation Execution / State Execution Services (RS-04…RS-06).
- Programme VII WS1–WS4 corpora for workflow, tips, and EST/CST law.
- Programme VIII WS1 Execution Completion Model for cycle-fulfilment meaning.

### Constitutional inputs

- Named RA-05 exposure intent bound to RI-05.
- Named execution responsibility class (workflow / recommendation / state) and cited corpus refs.
- Published conditions, artefacts, or postures required for the requested act.
- Optional completion-evaluation context when fulfilment status is requested.

### Constitutional outputs

- Authorised execution dispositions and published artefacts (workflow events, recommendation surfaces, EST/CST postures) through RI-05.
- Execution-completion judgements only as published fulfilment of responsibilities — never as educational success.
- Explicit refuse / defer / escalate when warrants fail.

### Permitted exposure

- Expose RI-05 for lawful workflow advancement under published stages and transitions.
- Request lawful recommendation surfacing under WS3 + Programme VI owners.
- Request lawful EST/CST representation under WS4 law.
- Request execution-completion evaluation under published completion criteria.

### Prohibited exposure

- Redefine RI-05, bypass workflow stages, invent tips, invent educational state, or invent runtime policy via API shape.
- Treat execution-completion as mastery, pass certainty, or constitutional change.
- Redefine ownership or mint recommendations under an “execution” label alone.
- Present ranking scores as constitutional educational warrant.
- Use the API to modify constitutional specifications or redefine published interfaces.
- Expose implementation internals as constitutional execution law.

---

## 8. RA-06 — Audit API

### Constitutional purpose

Expose the **published Audit Interface (RI-06)** so authorised consumers may record or retrieve material interaction trails — without inventing constitutional refs after the fact, using audit as a second constitution, or redefining RI-06.

### Constitutional consumers

- All material RA / RI / RS interactions that bind audit obligations.
- Authorised auditors, developers, and continuity-safe history consumers.
- Diagnostic consumers (RA-07) that may read audit trails — never rewrite them into new law.

### Constitutional providers

- Runtime Interface Model — RI-06 as the published interaction contract being exposed.
- Audit Service (RS-07) and Audit Contract (RC-07).
- EIP-003 / EIP-005 and this Programme VIII Runtime API Model.
- Producer corpora of the audited act (RA-01…RA-05 / RA-07 and bound RIs as applicable).

### Constitutional inputs

- Named RA-06 exposure intent bound to RI-06.
- Identity of the audited API interaction and bound RA / RI / RS / RC refs.
- Constitutional evidence / warrant refs actually consumed (if any).
- Constitutional responses / events / dispositions actually produced.
- Boundary-preservation checks performed.

### Constitutional outputs

- Reconstructable audit records answering API / interface / request / response / boundaries.
- Continuity-safe history across retries and replacements.
- Explicit defect signals when required audit components are missing.

### Permitted exposure

- Expose RI-06 to record which RA API(s) were used.
- Record which runtime interface(s) were exposed.
- Record which constitutional requests were received and responses returned.
- Record which constitutional boundaries were preserved.
- Retrieve prior lawful audit trails without erasing history.

### Prohibited exposure

- Redefine RI-06 or emit audit theatre that invents constitutional refs after the fact.
- Strip constitutional provenance while keeping technical access logs only.
- Use audit records to redefine educational meaning, ownership, or interface semantics.
- Treat missing audit as acceptable for “low-risk” educational mutations or primary student-facing tips.
- Present analytics dashboards as substitutes for constitutional audit obligations.
- Expose implementation internals as constitutional audit law.

---

## 9. RA-07 — Diagnostic API

### Constitutional purpose

Expose the **published Diagnostic Interface (RI-07)** so authorised consumers may inspect published law, capability readiness, and boundary posture — without creating constitutional behaviour, altering evidence, becoming an execution authority, or redefining RI-07.

### Constitutional consumers

- Authorised developers, auditors, and operators performing constitutional inspection.
- Authorised runtime collaborators that must confirm readiness before material execution.
- Product surfaces that may display honest diagnostic summaries — never invent educational claims from diagnostics alone.

### Constitutional providers

- Runtime Interface Model — RI-07 as the published interaction contract being exposed.
- Published Constitution / EIP / Programme VI / VII / VIII corpora as inspection sources.
- Read-only projections of RA / RI / RS / RC catalogue membership and boundary posture.
- Audit API (RA-06) / Audit Interface (RI-06) trails when diagnosis requires historical reconstruction.

### Constitutional inputs

- Named RA-07 exposure intent bound to RI-07.
- Diagnostic scope limited to published catalogues, corpus refs, and non-mutating inspection questions.
- Optional audit-trail references for historical diagnosis.
- Explicit non-execution intent (inspect / report — not execute).

### Constitutional outputs

- Diagnostic reports describing published catalogue membership, cited corpora, and boundary posture through RI-07.
- Honesty flags for missing warrants, incomplete audit, or unpublished request shapes.
- Explicit non-claims: diagnosis is not mastery, not pass certainty, not corpus amendment, not interface redefinition.

### Permitted exposure

- Expose RI-07 to inspect which RA / RI / RS / RC types are published and applicable.
- Inspect whether required constitutional inputs appear present for a contemplated act.
- Inspect boundary posture and prior audit trails in read-only form.
- Refuse any diagnostic request that would mutate evidence, state, specifications, or interface meanings.

### Prohibited exposure

- Redefine RI-07 or mutate evidence, state, recommendations, ownership, or specifications under a diagnostic label.
- Execute workflows or mint tips because diagnosis “looked ready.”
- Expose implementation internals (stack traces, private schemas, adapter paths) as constitutional law.
- Present diagnostic confidence scores as educational warrant.
- Use diagnosis to bypass contracts or invent unpublished capabilities / interfaces.

---

## 10. Composition Rules

1. **Primary mapping required.** Every material API interaction names at least one primary RA.
2. **Interface honesty.** RA exposures must map to published RI-01…RI-07 contracts — never invent parallel interface catalogues.
3. **Capability honesty.** Bound RI exposures must map to published RS / WS1 / WS2 capabilities — never invent parallel service catalogues.
4. **Evidence before certainty.** Interactions that claim understanding or mastery bind RA-02 (via RI-02).
5. **Events ≠ meaning.** RA-03 never substitutes for Programme VI meaning or tip law.
6. **Execution ≠ success.** RA-05 completion responses never certify educational success or constitutional change.
7. **Audit always.** RA-06 binds every material interaction in RA-01…RA-05 (and material RA-07 inspections that claim reconstructability).
8. **Diagnosis never executes.** RA-07 is non-mutating; execution requires RA-01 / RA-05 (as applicable) via their bound interfaces.
9. **No interface redefinition.** API composition never merges, absorbs, or rewrites RI identities.
10. **Closed catalogue.** New RA types require a Programme VIII constitutional amendment — not a silent OpenAPI invention.

---

## 11. Closing Statement

> **Runtime may expose constitutional runtime interfaces only through recognised APIs.  
> Outside this catalogue there is no lawful constitutional API exposure — only protocol improvisation.**
