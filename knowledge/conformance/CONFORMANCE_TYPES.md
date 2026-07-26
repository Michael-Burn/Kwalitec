# Conformance Types

**Programme:** IX — Workstream 1 — Constitutional Conformance Architecture  
**Milestone:** MS001 — Constitutional Conformance Model  
**Classification:** Closed catalogue of recognised constitutional conformance categories  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional conformance categories** (CC-01…CC-07).

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_CONFORMANCE_MODEL.md`](CONSTITUTIONAL_CONFORMANCE_MODEL.md)
3. [`CONFORMANCE_OBJECTIVES.md`](CONFORMANCE_OBJECTIVES.md)
4. Programme VI corpora under [`../educational/`](../educational/)
5. Programme VII corpora under [`../orchestration/`](../orchestration/)
6. Programme VIII corpora under [`../runtime/`](../runtime/)
7. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published conformance types may certify constitutional fidelity of an implementation.  
> Unpublished “implied conformance” is constitutionally defective.**

**Catalogue disambiguation:** CC-01…CC-07 here are *constitutional conformance types*. They are not Educational Validation Framework coach capability IDs, Programme VIII runtime contracts (RC-xx), evidence categories (EC-xx), or evidence validation categories (EV-xx).

---

## 1. Purpose

Assessment without a closed conformance catalogue invents law by proximity: whichever check, linter, or pipeline happens to be green becomes the tutor’s “proof the system is constitutional.”

This catalogue names the only lawful constitutional conformance types an assessment may apply — and binds each type to purpose, scope, inputs, outputs, and permitted / prohibited evaluation.

---

## 2. Catalogue Overview

| ID | Conformance type | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|------------------|--------------------------------|----------------|-----------------|
| **CC-01** | Structural Conformance | Confirm constitutional layering / responsibility structure is preserved in the implementation | Published layering / authority specs + structural artefacts | Structure conformant / non-conformant (+ deferred / escalated) |
| **CC-02** | Behavioural Conformance | Confirm observable behaviour obeys published constitutional rules | Published behavioural rules + observed / specified behaviours | Behaviour conformant / non-conformant (+ deferred / escalated) |
| **CC-03** | Evidence Conformance | Confirm evidence handling obeys published evidence / consumption / validation law | EIP-002 + Programme VIII evidence corpora + evidence-handling artefacts | Evidence-handling conformant / non-conformant |
| **CC-04** | Runtime Conformance | Confirm runtime execution posture obeys published runtime contracts and completion law | Programme VIII WS1 / service corpora + runtime artefacts | Runtime conformant / non-conformant |
| **CC-05** | Interface Conformance | Confirm interface composition obeys published interface / composition law | Programme VIII interface corpora + interface artefacts | Interface conformant / non-conformant |
| **CC-06** | API Conformance | Confirm API surfaces obey published contract / boundary / explainability obligations | Published API-facing constitutional obligations + API artefacts | API conformant / non-conformant |
| **CC-07** | Audit Conformance | Confirm reconstructability of constitutional acts and of the conformance assessment itself | Audit / continuity / explainability specs + audit artefacts | Audit conformant / non-conformant |

Material assessment must map to one or more of these types as published law requires. Cross-cutting situations may bind multiple CC types; none may invent a type outside this catalogue.

**Relation to RC / EC / EV:** Those catalogues remain defined solely by Programme VIII (and EIP). CC types *evaluate implementation fidelity* to those (and sibling) published laws; they do not replace or reclassify them.

**Relation to educational quality:** No CC type judges whether learning was good, whether a tip was wise, or whether the student is ready. Conformity ≠ quality.

---

## 3. CC-01 — Structural Conformance

### Constitutional purpose

Confirm that the implementation’s **responsibility structure and layering** preserve published constitutional separations — so educational meaning, orchestration, runtime execution, and delivery surfaces do not collapse into a single unlawful authority.

### Constitutional scope

Structural placement of responsibilities, ownership boundaries, and layering obligations published by Constitution / EIP / Programmes VI–VIII (and related authority matrices). Does **not** require a particular package layout, language module system, or repository topology beyond what published law states.

### Constitutional inputs

- Published structural / layering / authority specifications (Constitution, EIP-001, Programme VI / VII / VIII boundaries and stack positions).
- Named structural implementation artefacts (modules, services, adapters, blueprints as organisational units — assessed for responsibility placement, not as law).
- Published CCO-01 / CCO-03 / CCO-04 expectations.

### Constitutional outputs

- Structural conformance disposition: **conformant** or **non-conformant**.
- On non-conformant: lawful **deferred / escalated** when published law requires waiting or human / corpus escalation.
- Audit-speakable structure note (layering / ownership separations preserved: true/false).

### Permitted evaluation

- Verify that educational meaning authorship remains with Programme VI producers, not with runtime or UI modules claiming meaning.
- Verify that orchestration ownership / tip / state authorship remains with Programme VII producers.
- Verify that runtime executes published law rather than inventing parallel authority maps.
- Detect collapsed “god services” that absorb forbidden constitutional responsibilities.
- Emit CC-07-compatible records of the structural check.

### Prohibited evaluation

- Require a particular directory tree, framework, or ORM as constitutional structure.
- Rewrite published layering diagrams to match the code under review.
- Treat architectural preference docs as Constitution / EIP amendments.
- Declare educational meaning “owned by whichever service holds the data.”
- Use CC-01 to create new constitutional layering law.

---

## 4. CC-02 — Behavioural Conformance

### Constitutional purpose

Confirm that **observable educational and execution behaviours** obey published constitutional rules — so students experience only lawful refusal, deferral, escalation, progression, and explanation postures.

### Constitutional scope

Behaviours whose constitutional meaning is published (for example refuse when evidence is missing, defer when continuity requires waiting, escalate when ownership conflicts). Does **not** grade pedagogy quality or invent new behavioural law.

### Constitutional inputs

- Published behavioural rules from Constitution / EIP / Programmes VI–VIII (objectives, boundaries, transition rules, contract permitted / prohibited execution).
- Named behavioural artefacts (specified flows, observed dispositions, published event / recommendation / state outcomes).
- Published CCO-01 / CCO-05 expectations.

### Constitutional outputs

- Behavioural conformance disposition: **conformant** or **non-conformant** (+ deferred / escalated).
- Named rule bindings that the behaviour obeyed or violated.
- Audit-speakable behaviour note (published disposition honesty preserved: true/false).

### Permitted evaluation

- Verify that published refuse / defer / escalate paths are available when law requires them.
- Verify that published success paths do not invent meaning, ownership, tips, or state.
- Detect silent improvisation where published law requires a stop.
- Compose with CC-03…CC-06 when behaviour spans evidence, runtime, interface, or API surfaces.

### Prohibited evaluation

- Invent “helpful” behaviours not authorised by published law and call them conformant.
- Soft-rewrite Programme VI coach rules so observed UX passes.
- Treat A/B winners, engagement optimisers, or demo scripts as behavioural constitutional law.
- Equate “students finished the flow” with behavioural conformity.
- Use CC-02 to author new runtime or educational behaviour.

---

## 5. CC-03 — Evidence Conformance

### Constitutional purpose

Confirm that the implementation’s **evidence handling** obeys published Educational Evidence and Programme VIII evidence consumption / validation / completion law — so warrants are consumed, validated, and completed exactly as published.

### Constitutional scope

Fidelity to EIP-002, Programme VIII evidence corpora (EC / EV / ECC and related boundaries), and Programme VII orchestration evidence artefacts as published. Does **not** mint evidence, reclassify claims, or judge educational quality.

### Constitutional inputs

- Published evidence law (EIP-002; Programme VIII evidence consumption, validation, completion; Programme VII completion evidence as applicable).
- Named evidence-handling artefacts (consumers, validators, provenance preservation paths, refusal paths).
- Published CCO-02 / CCO-04 expectations and EC / EV catalogues as *subjects of fidelity*, not as this CC catalogue.

### Constitutional outputs

- Evidence-handling conformance disposition: **conformant** or **non-conformant** (+ deferred / escalated).
- Named evidence-law bindings (corpus paths; EC / EV identities as subjects where applicable).
- Audit-speakable evidence-handling note (no invention / alteration / reclassification / provenance fabrication: true/false).

### Permitted evaluation

- Verify that only published EC categories are treated as constitutional evidence.
- Verify that validation specialises eligibility (EV) without rewriting warrants.
- Verify provenance preservation and claim-ladder honesty through handling paths.
- Detect bypass of constitutional evidence requirements for product convenience.

### Prohibited evaluation

- Invent, alter, enrich, or reclassify evidence during “conformance fixing.”
- Treat storage acknowledgements, Twin estimates, or analytics events as Educational Evidence.
- Substitute EV eligibility for educational quality or mastery judgement.
- Amend EIP-002 or Programme VIII evidence corpora via findings.
- Use CC-03 to become an evidence producer.

---

## 6. CC-04 — Runtime Conformance

### Constitutional purpose

Confirm that the implementation’s **runtime execution posture** obeys published Programme VIII runtime contracts, event processing, execution completion, and service / collaboration law — so software executes constitutional law without becoming it.

### Constitutional scope

Fidelity to RC-01…RC-07 and sibling Programme VIII WS1 / WS3 (and related) runtime corpora. Does **not** require a particular process model, message bus, or “Runtime A” brand.

### Constitutional inputs

- Published runtime corpora (contracts, event processing, execution completion, services, collaboration, related boundaries).
- Named runtime artefacts (execution paths, contract bindings, completion records, service responsibility maps).
- Published CCO-01 / CCO-03 expectations.

### Constitutional outputs

- Runtime conformance disposition: **conformant** or **non-conformant** (+ deferred / escalated).
- Named RC / runtime-corpus bindings obeyed or violated.
- Audit-speakable runtime note (execution of published law without law invention: true/false).

### Permitted evaluation

- Verify material acts map to published RC bindings as required.
- Verify event processing and completion follow published classes and fulfilment rules.
- Verify services collaborate without transferring forbidden authority or merging responsibilities.
- Detect runtime improvisation that invents unpublished contracts or completion meanings.

### Prohibited evaluation

- Require a specific language, framework, queue, or host as constitutional runtime.
- Treat “service is up” as RC satisfaction.
- Rewrite Programme VIII contract text to match observed code.
- Elevate Runtime A topology into constitutional law.
- Use CC-04 to author new runtime behaviour under a conformity badge.

---

## 7. CC-05 — Interface Conformance

### Constitutional purpose

Confirm that **interface composition** obeys published Programme VIII interface / composition / completion law — so composed surfaces remain subordinate to constitutional producers and do not invent educational meaning.

### Constitutional scope

Fidelity to published interface composition models, boundaries, and completion corpora. Does **not** mandate a particular UI kit, widget set, or frontend framework.

### Constitutional inputs

- Published interface / composition / interface-completion corpora and related boundaries.
- Named interface artefacts (composition maps, handoff points, surface responsibilities).
- Published CCO-03 / CCO-04 expectations.

### Constitutional outputs

- Interface conformance disposition: **conformant** or **non-conformant** (+ deferred / escalated).
- Named interface-corpus bindings obeyed or violated.
- Audit-speakable interface note (composition without meaning invention / authority transfer: true/false).

### Permitted evaluation

- Verify composed interfaces consume published contracts / evidence / recommendations / state without rewriting them.
- Verify completion of interface responsibilities follows published fulfilment rules.
- Detect UI or adapter layers that silently become educational or ownership authorities.
- Compose with CC-02 / CC-06 when interface behaviour or API exposure is material.

### Prohibited evaluation

- Require a particular design system or component library as constitutional.
- Treat visual polish or accessibility tooling scores as constitutional interface law (unless a published constitutional specification so states — none do by default).
- Invent interface completion meanings to force conformity.
- Amend Programme VIII interface corpora via findings.
- Use CC-05 to author educational tips or state transitions.

---

## 8. CC-06 — API Conformance

### Constitutional purpose

Confirm that **API surfaces** obey published constitutional contract, boundary, and explainability obligations that apply to externally or internally callable educational / runtime acts — so APIs execute and expose law without inventing it.

### Constitutional scope

Fidelity of callable surfaces to published constitutional obligations (authorisation of acts, evidence / contract honesty, refusal postures, explainability hooks as published). Does **not** require REST, OpenAPI, GraphQL, or any particular protocol as constitutional.

### Constitutional inputs

- Published constitutional obligations for callable acts (Programme VIII contracts / boundaries / explainability; Programme VI / VII boundaries as they constrain exposed acts).
- Named API artefacts (endpoint / operation inventories, request–response dispositions, error / refuse / escalate postures — protocol-neutral).
- Published CCO-01 / CCO-03 / CCO-06 expectations.

### Constitutional outputs

- API conformance disposition: **conformant** or **non-conformant** (+ deferred / escalated).
- Named constitutional obligations obeyed or violated by the callable surface.
- Audit-speakable API note (callable acts remain law-executing, not law-making: true/false).

### Permitted evaluation

- Verify exposed acts map to published authorising contracts / ownership / evidence rules.
- Verify refuse / defer / escalate dispositions are expressible when law requires them.
- Verify APIs do not invent educational meaning fields or soft-upgrade claim classes.
- Detect protocol theatre (schema green) presented as constitutional adherence without corpus binding.

### Prohibited evaluation

- Mandate REST, OpenAPI, gRPC, or a particular schema language as constitutional.
- Treat OpenAPI lint success, HTTP status fashion, or SDK generation as constitutional law.
- Rewrite published boundaries so a convenient endpoint “passes.”
- Expose Twin / Adaptive estimates as Educational Evidence via API without published warrant.
- Use CC-06 to create new constitutional API law or educational meaning.

---

## 9. CC-07 — Audit Conformance

### Constitutional purpose

Confirm that the implementation — and the conformance assessment itself — preserve **reconstructable constitutional trails** under published continuity, explainability, and audit obligations — so adherence judgements and educational acts can be audited.

### Constitutional scope

Fidelity to EIP-003 / EIP-005 and Programme VIII audit / explainability / completion trail obligations as published, plus reconstructability of CC assessments under this Model. Does **not** mandate a particular log shipper, SIEM, or analytics product.

### Constitutional inputs

- Published audit / continuity / explainability specifications (EIP-003, EIP-005, RC-07 and sibling audit obligations, this Model’s explainability corpus).
- Named audit artefacts (constitutional trails for material acts; assessment records for material CC evaluations).
- Published CCO-02 / CCO-05 / CCO-06 expectations.

### Constitutional outputs

- Audit conformance disposition: **conformant** or **non-conformant** (+ deferred / escalated).
- Confirmation that material acts and assessments are reconstructable against constitutional refs.
- Audit-speakable meta-record (specs / artefacts / criteria / findings / boundaries preserved: true/false).

### Permitted evaluation

- Verify material educational / runtime acts leave constitutional refs, not only technical logs.
- Verify material CC assessments answer the mandatory explainability questions.
- Detect erasure of prior lawful history for UX or log-cost convenience.
- Confirm student / developer / auditor projections can share one truth.

### Prohibited evaluation

- Require a particular logging vendor or metrics backend as constitutional.
- Treat log volume, retention dashboards, or “observability scores” as constitutional audit law.
- Fabricate audit trails after the fact to force conformity.
- Erase non-conformant findings to present a green history.
- Use CC-07 to invent educational meaning or amend constitutional specifications.

---

## 10. Catalogue Discipline

| Rule | Meaning |
|------|---------|
| **Closed set** | Only CC-01…CC-07 are constitutional conformance types |
| **Multi-bind allowed** | A single assessment may bind multiple CC types when published law requires |
| **No silent skip** | Required types for a scope may not be omitted for convenience |
| **Subjects ≠ types** | RC / EC / EV / Programme VI–VII IDs may appear as *inputs*; they are not CC types |
| **Findings ≠ amendments** | Non-conformant results may motivate corpus proposals; they do not enact law |
| **Technology-neutral** | No CC type privileges a language, framework, protocol, or CI vendor |

---

## 11. Closing Statement

> **Only published conformance types may speak to constitutional fidelity of an implementation.  
> Unpublished “implied conformance,” green pipelines, and preferred stacks are not constitutional law — and never become it through assessment theatre.**
