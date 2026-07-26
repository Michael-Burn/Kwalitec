# Event Types

**Programme:** VIII — Workstream 1 — Constitutional Runtime Contracts  
**Milestone:** MS002 — Constitutional Event Processing Model  
**Classification:** Closed catalogue of recognised constitutional event categories  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional event categories** (CE-01…CE-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_EVENT_PROCESSING_MODEL.md`](CONSTITUTIONAL_EVENT_PROCESSING_MODEL.md)
3. [`EVENT_OBJECTIVES.md`](EVENT_OBJECTIVES.md)
4. [`../contracts/CONTRACT_TYPES.md`](../contracts/CONTRACT_TYPES.md)
5. Programme VI corpora under [`../../educational/`](../../educational/)
6. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
7. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published event categories may be processed as constitutional events.  
> Unpublished “implied events” are constitutionally defective.**

---

## 1. Purpose

Runtime without a closed event catalogue invents law by proximity: whichever payload arrives becomes the tutor’s “reason.”

This catalogue names the only lawful constitutional event categories a runtime may receive, evaluate, and execute — and binds each category to producers, consumers, purpose, and permitted / prohibited processing.

---

## 2. Catalogue Overview

| ID | Event category | Primary producer class | Primary consumer | Primary RC binding |
|----|----------------|------------------------|------------------|--------------------|
| **CE-01** | Evidence Event | Evidence Model (EIP-002) + permitted writers (EIP-001) | Runtime A | RC-02 (+ RC-01, RC-07) |
| **CE-02** | Workflow Event | Programme VII Workstream 1 | Runtime A | RC-03 (+ RC-04 when ownership at stake) |
| **CE-03** | Authority Event | Programme VII Workstream 2 | Runtime A | RC-04 |
| **CE-04** | Recommendation Event | Programme VII Workstream 3 (+ Programme VI owners) | Runtime A | RC-05 |
| **CE-05** | State Event | Programme VII Workstream 4 | Runtime A | RC-06 |
| **CE-06** | Audit Event | Constitution / EIP / Programme VIII corpus + producer of audited act | Runtime A | RC-07 |
| **CE-07** | Runtime Lifecycle Event | Programme VIII Runtime Contract / Event Processing Models (operational under constitutional replaceability) | Runtime A | RC-01 + RC-07 (never mint VI/VII meaning) |

Material processed events must map to one of these categories. Cross-cutting situations may emit or bind multiple CE categories; none may invent a category outside this catalogue.

**Relation to Programme VII WE-xx stimuli:** Educational workflow stimuli published in [`../../orchestration/workflows/WORKFLOW_EVENTS.md`](../../orchestration/workflows/WORKFLOW_EVENTS.md) are consumed under **CE-02**. This catalogue does not replace WE-xx meanings; it classifies how runtime processes them (and sibling constitutional signals) under Programme VIII.

---

## 3. CE-01 — Evidence Event

### Constitutional producer

[`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002), Knowledge & Mastery (EIP-006), and permitted writers under the State Authority Matrix (EIP-001).

### Constitutional consumer

Runtime A (and lawful successors) when receiving signals that lawful Educational Evidence has been recorded, updated, or must be consumed with claim-ladder honesty.

### Execution purpose

Ensure runtime **processes evidence-facing signals as classified observational warrants**, triggering only published consumption / routing / continuity behaviour — never reinterpreting coverage, time-on-task, confidence, or engagement as understanding or mastery.

### Permitted processing

- Receive published evidence-recorded / evidence-updated signals whose classification already exists under EIP-002.
- Evaluate RC-02 obligations before any downstream certainty speech or decision.
- Route mutation requests only to EIP-001-permitted writers.
- Surface honest understatement when evidence is incomplete or conflicting.
- Preserve continuity of evidence history (EIP-005).
- Emit CE-06 / RC-07 audit records for material evidence processing.

### Prohibited processing

- Invent evidence classes or reclassify evidence in the handler (e.g. session completion → mastery).
- Mint Estimated Knowledge / Mastery from event convenience alone.
- Treat Twin / Adaptive estimates as primary Evidence Model observations when they are not.
- Bypass Evidence Model succession rules with “temporary” certainty from an event payload.
- Use CE-01 to invent tips, transfer ownership, or advance workflows without WS1 / RC-03 law.

---

## 4. CE-02 — Workflow Event

### Constitutional producer

Programme VII Workstream 1 corpora under [`../../orchestration/workflows/`](../../orchestration/workflows/), including [`WORKFLOW_EVENTS.md`](../../orchestration/workflows/WORKFLOW_EVENTS.md) (WE-xx), plus workflow transition and completion law.

### Constitutional consumer

Runtime A (and lawful successors) when receiving stimuli that initiate, continue, advance, hand off, or conclude educational orchestration.

### Execution purpose

Ensure runtime **processes published workflow stimuli and orchestration signals** under RC-03 — without becoming a substitute tutor or inventing orchestration shortcuts from delivery noise.

### Permitted processing

- Receive published WE-xx (and sibling published workflow signals) as initiation / continuation triggers.
- Evaluate published stage / transition / completion conditions under RC-03.
- Advance only through published stages; record published participation and outcome classes.
- Conclude workflows only under published completion criteria.
- Invoke RC-04 when ownership or conflict disposition is required for lawful advancement.
- Generate published constitutional workflow traces required by WS1 explainability.
- Emit CE-06 / RC-07 audit records for material workflow processing.

### Prohibited processing

- Invent workflow event classes, stages, or completion meanings in runtime.
- Bypass stages, transitions, or completion criteria because an event “already happened.”
- Use orchestration events to redefine Programme VI educational meaning.
- Treat workflow progress as mastery, success, or plan completion unless published law says so.
- Skip authority checks while claiming lawful workflow advancement from CE-02 alone.

---

## 5. CE-03 — Authority Event

### Constitutional producer

Programme VII Workstream 2 corpora under [`../../orchestration/authority/`](../../orchestration/authority/), [`../../orchestration/conflict_resolution/`](../../orchestration/conflict_resolution/), and [`../../orchestration/authority_explainability/`](../../orchestration/authority_explainability/).

### Constitutional consumer

Runtime A (and lawful successors) when receiving signals that ownership, permission, refusal, delegation, or conflict disposition must be applied.

### Execution purpose

Ensure runtime **processes published ownership and conflict signals** under RC-04, and never absorbs educational domains because an authority-labelled message arrived.

### Permitted processing

- Receive published ownership-check, permission, refusal, delegation, or conflict-disposition signals.
- Resolve the constitutional owner of a decision class from the Authority Model.
- Apply published permission, refusal, delegation, and conflict-resolution outcomes.
- Preserve owner labels through subsequent packaging and delivery.
- Explain permission / refusal using published authority explainability obligations.
- Emit CE-06 / RC-07 audit records for material authority processing.

### Prohibited processing

- Invent or transfer ownership outside published domains via event handling.
- Rank or merge coaches by undocumented heuristics when conflict law applies.
- Treat UI, adapters, Twin, or Adaptive as educational decision owners unless the Authority Model says so.
- Grant mutation rights as a side effect of receiving an authority-shaped payload.
- Silence rightful refusal by inventing a tip to fill a slot after CE-03 processing.

---

## 6. CE-04 — Recommendation Event

### Constitutional producer

Programme VII Workstream 3 corpora under [`../../orchestration/recommendations/`](../../orchestration/recommendations/), [`../../orchestration/recommendation_assembly/`](../../orchestration/recommendation_assembly/), and [`../../orchestration/recommendation_explainability/`](../../orchestration/recommendation_explainability/), plus the Programme VI owner artefacts that warrant each tip.

### Constitutional consumer

Runtime A (and lawful successors) when receiving signals to package, assemble, surface, refuse, defer, or supersede educational recommendations.

### Execution purpose

Ensure runtime **processes constitutional recommendation artefacts as communicative signals**, and never invents tips, rewrites ownership, or executes workflows under a recommendation event label.

### Permitted processing

- Receive signals to surface structured recommendations that already satisfy WS3 structure, sources, and boundaries.
- Assemble lawful recommendations into published recommendation sets under WS3 / MS002 assembly law.
- Communicate refusal / deferral / no-recommendation when warrants fail.
- Preserve provenance, owner, evidence, and constitutional references through delivery.
- Explain recommendation sets under published set-explainability obligations.
- Emit CE-06 / RC-07 audit records for material recommendation processing.

### Prohibited processing

- Invent tips from undocumented heuristics, engagement models, or “AI tutor” improvisation triggered by CE-04.
- Generate unpublished recommendations from Adaptive / Twin / UI proximity alone.
- Reinterpret Educational Evidence while packaging speech.
- Alter constitutional ownership by merging coaches into one silent mega-tip.
- Execute workflows, mutate plans, or advance state under recommendation-event authority alone.
- Present ranking scores as constitutional educational warrant.

---

## 7. CE-05 — State Event

### Constitutional producer

Programme VII Workstream 4 corpora under [`../../orchestration/state/`](../../orchestration/state/), [`../../orchestration/state_transitions/`](../../orchestration/state_transitions/), and [`../../orchestration/state_explainability/`](../../orchestration/state_explainability/), distinct from EIP-001 meaning-bearing educational-state mutation rights.

### Constitutional consumer

Runtime A (and lawful successors) when receiving signals to read, apply, hold, or transition constitutional educational **context** postures (EST/CST).

### Execution purpose

Ensure runtime **processes published educational-context signals** under RC-06, and never invents focus postures, implies mastery/success from context alone, or erases continuity.

### Permitted processing

- Receive published EST / CST succession or representation signals.
- Represent live educational context only via published EST postures.
- Apply published CST succession under published conditions.
- Hold / wait / refuse-remain when law requires continuity over motion.
- Explain live context and lawful succession under WS4 explainability obligations.
- Keep context speech distinct from Programme VI tip warrant and EIP-002 understanding evidence.
- Emit CE-06 / RC-07 audit records for material state processing.

### Prohibited processing

- Invent unpublished EST/CST types from event payloads.
- Treat context posture as mastery, pass certainty, workflow completion, or tip authorisation.
- Transfer ownership or mint recommendations via state-event labels.
- Erase prior lawful context to simplify narration (EIP-005).
- Confuse EIP-001 meaning-bearing mutation rights with WS4 contextual representation.

---

## 8. CE-06 — Audit Event

### Constitutional producer

Educational Constitution; EIP-003 / EIP-005; Programme VIII Runtime Contract and Event Processing Models; and the producer corpora of the audited act (CE-01…CE-05 / CE-07 as applicable).

### Constitutional consumer

Runtime A (and lawful successors) when emitting or receiving signals that material educational execution must be recorded, retained, or reconstructed.

### Execution purpose

Ensure runtime **processes audit-facing signals so reconstructable constitutional records exist** — without using audit machinery as a second constitution or a back door to invent meaning.

### Permitted processing

- Emit / receive signals to record which CE and RC executed.
- Record which constitutional corpus / artefact authorised the act.
- Record which constitutional artefacts / evidence were consumed.
- Record which constitutional outputs were produced.
- Record which boundaries were checked and preserved.
- Retain continuity-safe history across retries and replacements.
- Support developer / auditor reconstruction under EIP-003 / EIP-005.

### Prohibited processing

- Emit audit theatre that invents constitutional refs after the fact.
- Strip constitutional provenance while keeping technical delivery logs only.
- Use audit events to redefine educational meaning or ownership.
- Treat missing audit as acceptable for “low-risk” educational mutations or primary student-facing tips.
- Present analytics dashboards as substitutes for constitutional audit obligations.
- Invent new educational behaviour solely because an audit event fired.

---

## 9. CE-07 — Runtime Lifecycle Event

### Constitutional producer

Programme VIII Runtime Contract Model and this Event Processing Model — limited to **operational lifecycle signals** required for replaceable, continuous, auditable execution (start, stop, replace, resume, refuse-ready, continuity handoff). Constitutional educational meaning remains upstream.

### Constitutional consumer

Runtime A (and lawful successors) when receiving signals about runtime readiness, replacement, resume, or continuity of processing capacity — not educational coaching content.

### Execution purpose

Ensure runtime **processes lifecycle signals so executors remain replaceable and continuous** (RCO-06 / EPO continuity) without allowing operational events to mint Programme VI / VII educational behaviour.

### Permitted processing

- Receive published lifecycle signals: runtime ready / not-ready, lawful replacement begin / complete, resume after interruption, continuity handoff between compliant executors.
- Refuse educational CE-01…CE-05 processing when lifecycle state requires refuse / defer (honest stop).
- Preserve RC-07 audit of lifecycle transitions that affect educational continuity.
- Re-enter processing only at published points after resume / replacement.
- Keep lifecycle speech operational — never as tip warrant, mastery claim, or ownership transfer.

### Prohibited processing

- Invent educational meaning, tips, ownership, evidence classes, or EST/CST postures from lifecycle events.
- Treat deploy, scale, restart, or health-check infrastructure noise as CE-07 without a published constitutional lifecycle mapping.
- Bypass workflow / authority / recommendation / state law because “runtime just came up.”
- Make a particular process, pod, or codebase constitutionally irreplaceable via lifecycle theatre.
- Use CE-07 to amend Constitution / EIP / Programme VI / VII specifications.

---

## 10. Composition Rules

1. **Primary mapping required.** Every material constitutional event names at least one primary CE.
2. **Upstream stimulus honesty.** WE-xx and sibling Programme VII stimuli map into CE-02 (or the matching CE) without rewriting their educational meaning.
3. **Contract binding required.** Every material CE processing act binds the RC catalogue per §2 and MS001 composition rules.
4. **Evidence before certainty.** Acts that claim understanding or mastery require CE-01 / RC-02 honesty.
5. **Context ≠ meaning.** CE-05 never substitutes for Programme VI meaning or tip law (CE-04).
6. **Audit always.** Material CE-01…CE-05 / CE-07 processing binds RC-07; CE-06 specialises audit signalling without replacing that obligation.
7. **Lifecycle never coaches.** CE-07 may gate processing; it never authors educational guidance.
8. **Closed catalogue.** New CE types require a Programme VIII constitutional amendment — not a silent handler invention.

---

## 11. Closing Statement

> **Runtime may process only recognised constitutional event categories.  
> Outside this catalogue there is no lawful educational event processing — only product improvisation.**
