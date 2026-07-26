# Service Types

**Programme:** VIII — Workstream 3 — Constitutional Runtime Services  
**Milestone:** MS001 — Runtime Service Model  
**Classification:** Closed catalogue of recognised constitutional runtime services  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional runtime service categories** (RS-01…RS-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`RUNTIME_SERVICE_MODEL.md`](RUNTIME_SERVICE_MODEL.md)
3. [`SERVICE_OBJECTIVES.md`](SERVICE_OBJECTIVES.md)
4. Programme VI corpora under [`../../educational/`](../../educational/)
5. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
6. Programme VIII WS1 corpora under [`../contracts/`](../contracts/), [`../event_processing/`](../event_processing/), [`../execution_completion/`](../execution_completion/)
7. Programme VIII WS2 corpora under [`../evidence_consumption/`](../evidence_consumption/), [`../evidence_validation/`](../evidence_validation/), [`../evidence_completion/`](../evidence_completion/)
8. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published service types may expose material constitutional execution capabilities.  
> Unpublished “implied services” are constitutionally defective.**

**Namespace note.** RS-* here means **Runtime Service**. Recovery Strategy identifiers under Programme VI Recovery Coach corpora are a separate namespace.

---

## 1. Purpose

Runtime without a closed service catalogue invents authority by proximity: whichever module happens to hold the data becomes the tutor.

This catalogue names the only lawful execution capabilities between constitutional producers and runtime consumers.

---

## 2. Catalogue Overview

| ID | Service | Primary contracts | Primary constitutional focus |
|----|---------|-------------------|------------------------------|
| **RS-01** | Contract Execution Service | RC-01 (+ others as bound) | Execute under published RC bindings |
| **RS-02** | Evidence Consumption Service | RC-02 | Consume published constitutional evidence |
| **RS-03** | Event Processing Service | RC-01 / RC-03 (+ event law) | Process published constitutional events |
| **RS-04** | Workflow Execution Service | RC-03 (+ RC-04 as required) | Execute published workflow responsibilities |
| **RS-05** | Recommendation Execution Service | RC-05 (+ RC-04 as required) | Execute published recommendation responsibilities |
| **RS-06** | State Execution Service | RC-06 | Execute published educational-state responsibilities |
| **RS-07** | Audit Service | RC-07 | Preserve reconstructable constitutional trails |

Material runtime acts must map to one or more of these services. Cross-cutting acts (for example executing a workflow that surfaces a recommendation) may compose multiple RSs simultaneously; none may be silently skipped when their responsibility applies.

Services may **invoke other authorised runtime services**. Composition does not transfer authorship: each composed service remains an executor under its own permitted responsibilities.

---

## 3. RS-01 — Contract Execution Service

### Constitutional purpose

Bind software so that every material educational action is an **execution of published constitutional contracts** (RC-01…RC-07), not an improvisation of educational law.

### Constitutional inputs

- Recognised RC-01…RC-07 contract bindings applicable to the act.
- Published constitutional rules / conditions from Constitution, EIP, Programme VI, and Programme VII as cited by those contracts.
- Concrete learner circumstances against which published conditions are evaluated.
- Optional composition requests from other authorised RS services.

### Constitutional outputs

- Authorised execution dispositions (execute / refuse / defer / escalate) under the bound contracts.
- Authorised execution records citing contract identity and corpus producers.
- Composition handoffs to other RS services when published law requires specialised execution.

### Constitutional consumers

- Runtime A (and lawful successor runtime implementations).
- Other authorised RS services that require contract-gated execution.
- Downstream product surfaces that may observe dispositions — never author contracts.

### Constitutional producers

- Constitution / EIP / Programme VI / Programme VII corpora that publish the rules being executed.
- Programme VIII WS1 Runtime Contract Model that publishes RC-01…RC-07.

### Permitted responsibilities

- Evaluate published constitutional conditions against concrete learner circumstances under named RC bindings.
- Perform actions explicitly authorised by those contracts.
- Refuse, defer, or escalate when published law requires refusal / deferral / escalation.
- Compose multiple published contracts when the corpora themselves allow composition.
- Invoke other authorised RS services to fulfil specialised responsibilities.

### Prohibited responsibilities

- Invent unpublished contracts, conditions, or educational meanings.
- Treat engineering heuristics, A/B winners, or product preference as constitutional authorisation.
- Redefine Constitution / EIP / Programme VI / VII / VIII text in code comments or constants.
- Claim execution success as proof of mastery, pass certainty, or educational truth amendment.
- Bypass RC catalogue by renaming modules “executors.”

---

## 4. RS-02 — Evidence Consumption Service

### Constitutional purpose

Ensure runtime **consumes published constitutional evidence exactly as classified** under Programme VIII WS2 and EIP-002 — never inventing, modifying, reinterpreting, or reclassifying warrants.

### Constitutional inputs

- Published evidence artefacts and claim types (EC categories as applicable).
- Evidence validation outcomes (EV eligibility) when required before consumption.
- RC-02 Evidence Consumption Contract bindings.
- EIP-001 writer / mutation rights when routing write requests (never granting new rights).

### Constitutional outputs

- Lawful consumption records (what was received, validated, and applied).
- Honest understatement / refusal when evidence is incomplete, conflicting, or ineligible.
- Continuity-preserving references to evidence history (EIP-005).
- Handoffs to RS-01 / RS-07 (and others) for contract-gated acts and audit.

### Constitutional consumers

- Runtime A and lawful successors when reading or applying observational educational warrants.
- RS-04 / RS-05 / RS-06 when their responsibilities require published evidence.
- Product surfaces that may display honest claim-ladder speech — never reclassify evidence.

### Constitutional producers

- EIP-002 Educational Evidence Model; EIP-006 Knowledge & Mastery; EIP-001 State Authority Matrix.
- Programme VI / VII corpora that publish warrants or orchestration artefacts classified as constitutional evidence.
- Programme VIII WS2 Evidence Consumption, Validation, and Completion Models.

### Permitted responsibilities

- Receive published evidence artefacts as classified.
- Apply published validation eligibility before lawful consumption when WS2 requires it.
- Apply published claim-ladder honesty in downstream speech and decisions.
- Route mutation requests only to EIP-001-permitted writers.
- Confirm evidence-handling fulfilment under WS2 completion law without inventing educational success.

### Prohibited responsibilities

- Reclassify evidence classes in runtime (e.g. treating session completion as mastery).
- Mint Estimated Knowledge / Mastery from coaching convenience alone.
- Erase or rewrite evidence history to simplify UX.
- Present Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Bypass Evidence Model succession rules with “temporary” certainty.
- Invent new EC / EV categories without a Programme VIII amendment.

---

## 5. RS-03 — Event Processing Service

### Constitutional purpose

Ensure runtime **receives, evaluates, and executes published constitutional events** under Programme VIII WS1 / MS002 — without creating constitutional behaviour or inventing event types.

### Constitutional inputs

- Published CE-class events and stimuli.
- Applicable RC bindings that authorise processing the event.
- Published evaluation conditions from Programme VII / VI / EIP as cited by event law.
- Optional composition from RS-01 / RS-04 when workflows are event-gated.

### Constitutional outputs

- Evaluation dispositions (accept / refuse / defer / escalate) under published event law.
- Authorised execution acts triggered only by published event → responsibility mappings.
- Published event traces and processing records required for explainability and audit.
- Handoffs to specialised RS services when the event’s published responsibility demands them.

### Constitutional consumers

- Runtime A and lawful successors when processing educational stimuli.
- RS-04 Workflow Execution Service when events initiate or continue workflows.
- Downstream observers that may watch processing outcomes — never mint CE types.

### Constitutional producers

- Programme VII (and related) corpora that publish event stimuli and orchestration triggers.
- Programme VIII WS1 Constitutional Event Processing Model (CE catalogue).
- Programme VIII WS1 Runtime Contract Model for authorising contracts.

### Permitted responsibilities

- Receive only published constitutional event classes.
- Evaluate published conditions attached to those events.
- Execute only published event → responsibility mappings under RC bindings.
- Emit only published constitutional event classes when law requires emission.
- Preserve processing traces for RS-07 audit composition.

### Prohibited responsibilities

- Invent event types, payloads meanings, or “implicit events” from product convenience.
- Treat UI clicks, cron ticks, or queue deliveries as constitutional events unless a published CE mapping says so.
- Use event processing to redefine Programme VI meaning or Programme VII ownership.
- Bypass contracts by claiming “the event arrived, so we must act.”
- Present successful processing as mastery, plan completion, or constitutional amendment.

---

## 6. RS-04 — Workflow Execution Service

### Constitutional purpose

Ensure runtime **executes published workflow responsibilities** — initiation, advancement, handoff, and conclusion under Programme VII WS1 and RC-03 — without becoming a substitute tutor or inventing orchestration shortcuts.

### Constitutional inputs

- Published workflow events, stages, transitions, and completion criteria.
- RC-03 Workflow Execution Contract (and RC-04 when authority checks are required).
- Published participation / outcome classes.
- Event-processing outputs from RS-03 when workflows are event-initiated.
- Authority dispositions when RC-04 applies.

### Constitutional outputs

- Lawful stage transitions and handoff records under published transition law.
- Published participation and outcome records.
- Workflow completion / non-completion dispositions under published completion criteria.
- Published workflow events / traces required by WS1 explainability.
- Composition calls to RS-05 / RS-06 / RS-02 when published law requires tips, state, or evidence at a stage.

### Constitutional consumers

- Runtime A and lawful successors when orchestrating educational journeys.
- RS-01 for contract-gated composition; RS-07 for audit.
- Product surfaces that may present lawful next steps — never invent stages.

### Constitutional producers

- Programme VII Workstream 1 corpora (workflows, transitions, completion).
- Programme VIII WS1 Runtime Contract Model (RC-03) and Event Processing Model as applicable.
- Programme VII WS2 Authority corpora when ownership checks gate advancement.

### Permitted responsibilities

- Accept published workflow events as initiation / continuation triggers.
- Advance only through published stages under published transition conditions.
- Record published participation and outcome classes.
- Conclude workflows only under published completion criteria.
- Invoke RS-02 / RS-05 / RS-06 / RS-07 when published workflow law requires their responsibilities.

### Prohibited responsibilities

- Bypass stages, transitions, or completion criteria for product convenience.
- Invent workflow stages, events, or completion meanings in runtime.
- Use orchestration to redefine Programme VI educational meaning.
- Treat workflow progress as mastery, success, or plan completion unless published law says so.
- Skip authority checks (RC-04) while claiming lawful workflow advancement.

---

## 7. RS-05 — Recommendation Execution Service

### Constitutional purpose

Ensure runtime **executes published recommendation responsibilities** — surfacing and applying only constitutionally structured recommendation artefacts with named owners and sources under RC-05 — without minting tips.

### Constitutional inputs

- Published recommendation artefacts / sets from Programme VII WS3 (+ Programme VI owners).
- RC-05 Recommendation Consumption Contract (and RC-04 when permission is required).
- Published warrants and evidence required by recommendation law (via RS-02 as needed).
- Applicable workflow / state context when corpora require contextual gating (via RS-04 / RS-06).

### Constitutional outputs

- Surfaced constitutional recommendation artefacts / sets with provenance intact.
- No-recommendation / defer / escalate dispositions when warrant is absent or permission fails.
- Execution records linking recommendation identity to owners, sources, and RC-05.
- Audit handoffs to RS-07.

### Constitutional consumers

- Runtime A and lawful successors when presenting educational tips / next-step guidance.
- RS-04 when workflows lawfully surface recommendations at a stage.
- Students / product surfaces as recipients of speakable tips — never authors of tip warrant.

### Constitutional producers

- Programme VII Workstream 3 recommendation corpora.
- Programme VI owner corpora that publish tip warrant / guidance artefacts.
- Programme VIII WS1 Runtime Contract Model (RC-05) and Authority Contract (RC-04) as applicable.

### Permitted responsibilities

- Consume and surface only published recommendation artefacts / sets.
- Preserve owner, source, and warrant provenance through execution.
- Refuse to surface recommendations when RC-04 / RC-05 conditions fail.
- Compose with RS-02 for evidence honesty and RS-06 for lawful context gating.
- Explain recommendation execution without rewriting tip meaning.

### Prohibited responsibilities

- Invent recommendations, tip text, or “helpful nudges” without published warrant.
- Reassign tip ownership by service proximity or product urgency.
- Present Adaptive / Twin / optimiser outputs as constitutional recommendations when they are not.
- Use recommendation execution to redefine Programme VI educational meaning.
- Treat tip display as proof of mastery, readiness, or plan completion.

---

## 8. RS-06 — State Execution Service

### Constitutional purpose

Ensure runtime **executes published educational-state responsibilities** — applying only published EST/CST postures and transitions under RC-06 — without inventing educational context.

### Constitutional inputs

- Published educational-state postures, entry/exit conditions, and transitions (Programme VII WS4).
- RC-06 State Consumption Contract.
- Published evidence / warrants required for lawful state application (via RS-02).
- Authority permissions when state mutation rights are gated (EIP-001 / RC-04 as applicable).

### Constitutional outputs

- Applied published context postures / transition records.
- Refuse / defer / escalate dispositions when entry conditions fail.
- Continuity-preserving state history references (EIP-005).
- Composition handoffs to RS-04 / RS-05 when workflows or tips are state-gated.

### Constitutional consumers

- Runtime A and lawful successors when applying educational context.
- RS-04 / RS-05 when published law requires state gating.
- Downstream Twin / Adaptive consumers of context facts — never authors of EST/CST law.

### Constitutional producers

- Programme VII Workstream 4 state corpora (EST/CST and siblings).
- EIP-001 State Authority Matrix for mutation rights.
- Programme VIII WS1 Runtime Contract Model (RC-06).

### Permitted responsibilities

- Evaluate published entry/exit and transition conditions.
- Apply only published postures under RC-06.
- Route state writes only to EIP-001-permitted writers.
- Preserve continuity of lawful state history.
- Refuse invented or “temporary” postures that lack published warrant.

### Prohibited responsibilities

- Invent educational states, postures, or transitions in runtime.
- Absorb EIP-001 mutation rights by renaming writers or services.
- Treat UI mode, feature flags, or session cookies as constitutional educational state unless published law maps them.
- Use state execution to redefine ownership, tips, or Programme VI meaning.
- Present applied context as mastery or pass certainty.

---

## 9. RS-07 — Audit Service

### Constitutional purpose

Ensure runtime **preserves reconstructable constitutional trails** for every material service execution under RC-07 — without turning audit into a second educational authority or a mere technical log sink.

### Constitutional inputs

- Material execution acts from RS-01…RS-06 (service identity, RC bindings, evidence/event refs, outputs, boundary checks).
- RC-07 Audit Contract obligations.
- Continuity requirements (EIP-005) and explainability components (EIP-003 / service explainability).

### Constitutional outputs

- Constitutional audit records citing service, contracts, corpora, evidence, events, outputs, and boundaries.
- Continuity-preserving history across retries, replacements, and redeploys.
- Refusal / incompleteness markers when required components are missing (defect signal, not silent success).

### Constitutional consumers

- Runtime A and lawful successors for all material acts.
- Developers / auditors reconstructing “why did this run?”
- Explainability projections (student-plain vs developer vocabulary over one truth).

### Constitutional producers

- Constitution / EIP explainability and continuity standards.
- Programme VIII WS1 Runtime Contract Model (RC-07) and sibling WS1 / WS2 explainability corpora.
- This Runtime Service Model’s explainability obligations.

### Permitted responsibilities

- Capture constitutional references for material RS executions.
- Preserve provenance integrity through packaging into speech / audit.
- Mark incomplete trails as constitutionally defective.
- Support RSO-03 auditability and service explainability questions.
- Compose with every other RS without absorbing their educational responsibilities.

### Prohibited responsibilities

- Invent educational meaning, tips, ownership, or state “for the audit narrative.”
- Reclassify evidence by storytelling in audit text.
- Erase history to simplify storage or UX.
- Substitute scores, latency, or engagement metrics for constitutional references.
- Treat log shippers, analytics products, or dashboards as the Audit Service definition.

---

## 10. Catalogue Rules

1. **Closed catalogue.** New RS types require a Programme VIII constitutional amendment — not a silent schema invention.
2. **Contract binding.** Every material RS act consumes one or more RC-01…RC-07 contracts.
3. **Composition, not absorption.** Invoking another RS does not transfer authorship or expand permitted responsibilities.
4. **Namespace honesty.** Runtime Service RS-* must not be confused with Recovery Strategy RS-* elsewhere in the knowledge tree.
5. **Technology silence.** Catalogue entries never mandate Python, Flask, DI, microservices, REST, queues, schedulers, workers, or databases.
6. **Replaceability.** Any compliant implementation may realise an RS type; none may monopolise constitutional truth.

---

## 11. Closing Statement

> **If a capability cannot name its RS type, its RC bindings, its constitutional producers, and its permitted responsibilities, it is not yet a constitutional runtime service — and must not be exposed as educational law.**
