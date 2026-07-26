# Verification Types

**Programme:** IX — Workstream 2 — Constitutional Conformance Architecture  
**Milestone:** MS001 — Constitutional Verification Model  
**Classification:** Closed catalogue of recognised constitutional verification categories  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional verification categories** (CV-01…CV-07).

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_VERIFICATION_MODEL.md`](CONSTITUTIONAL_VERIFICATION_MODEL.md)
3. [`VERIFICATION_OBJECTIVES.md`](VERIFICATION_OBJECTIVES.md)
4. [`../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md)
5. [`../conformance/CONFORMANCE_TYPES.md`](../conformance/CONFORMANCE_TYPES.md)
6. [`../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md`](../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md)
7. [`../conformance/traceability/TRACEABILITY_TYPES.md`](../conformance/traceability/TRACEABILITY_TYPES.md)
8. Programme VI corpora under [`../educational/`](../educational/)
9. Programme VII corpora under [`../orchestration/`](../orchestration/)
10. Programme VIII corpora under [`../runtime/`](../runtime/)
11. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published verification types may speak to whether implementation evidence satisfies published constitutional requirements.  
> Unpublished “implied verification” is constitutionally defective.**

**Catalogue disambiguation:** CV-01…CV-07 here are *constitutional verification types*. They are not MS001 conformance types (CC-01…CC-07), MS002 traceability types (CT-01…CT-07), Educational Validation Framework coach capability IDs, Programme VIII runtime contracts (RC-xx), evidence categories (EC-xx), or evidence validation categories (EV-xx).

---

## 1. Purpose

Assessment without a closed verification catalogue invents law by proximity: whichever check, linter, or pipeline happens to be green becomes the tutor’s “proof the system is constitutionally verified.”

This catalogue names the only lawful constitutional verification types an assessment may apply — and binds each type to purpose, scope, inputs, outputs, and permitted / prohibited verification.

---

## 2. Catalogue Overview

| ID | Verification type | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|-------------------|--------------------------------|----------------|-----------------|
| **CV-01** | Structural Verification | Evaluate evidence that constitutional layering / responsibility structure is preserved | Published layering / authority specs + structural evidence + CT links | Structure satisfied / not-satisfied (+ deferred / escalated) |
| **CV-02** | Behavioural Verification | Evaluate evidence that observable behaviour obeys published constitutional rules | Published behavioural rules + behavioural evidence + CT links | Behaviour satisfied / not-satisfied (+ deferred / escalated) |
| **CV-03** | Evidence Verification | Evaluate evidence that evidence handling obeys published evidence law | EIP-002 + Programme VIII evidence corpora + handling evidence + CT links | Evidence-handling satisfied / not-satisfied |
| **CV-04** | Runtime Verification | Evaluate evidence that runtime execution posture obeys published runtime law | Programme VIII runtime corpora + runtime evidence + CT links | Runtime satisfied / not-satisfied |
| **CV-05** | Interface Verification | Evaluate evidence that interface composition obeys published interface law | Programme VIII interface corpora + interface evidence + CT links | Interface satisfied / not-satisfied |
| **CV-06** | API Verification | Evaluate evidence that API surfaces obey published callable-act obligations | Published API-facing constitutional obligations + API evidence + CT links | API satisfied / not-satisfied |
| **CV-07** | Governance Verification | Evaluate evidence that governance / authority-preservation obligations are satisfied | Governance / authority / conformance / continuity specs + governance evidence + CT links | Governance satisfied / not-satisfied |

Material assessment must map to one or more of these types as published law requires. Cross-cutting situations may bind multiple CV types; none may invent a type outside this catalogue.

**Relation to CC / CT / RC / EC / EV:** Those catalogues remain defined solely by their owners. CV types *evaluate whether implementation evidence satisfies* published requirements under established lineage; they do not replace, reclassify, certify, or invent those catalogues.

**Relation to educational quality:** No CV type judges whether learning was good, whether a tip was wise, or whether the student is ready. Satisfied ≠ quality. Satisfied ≠ certified. Satisfied ≠ permanently conformant.

---

## 3. CV-01 — Structural Verification

### Constitutional purpose

Evaluate **implementation evidence** that the implementation’s **responsibility structure and layering** preserve published constitutional separations — so educational meaning, orchestration, runtime execution, and delivery surfaces do not collapse into a single unlawful authority.

### Constitutional scope

Structural placement of responsibilities, ownership boundaries, and layering obligations published by Constitution / EIP / Programmes VI–VIII (and related authority matrices). Does **not** require a particular package layout, language module system, or repository topology beyond what published law states. Does **not** certify structure as permanently lawful.

### Constitutional inputs

- Published structural / layering / authority specifications (Constitution, EIP-001, Programme VI / VII / VIII boundaries and stack positions).
- Named structural implementation evidence (module / service / adapter responsibility maps — assessed for placement, not as law).
- Established CT relationships linking those specs to those artefacts (typically CT-01 / CT-02).
- Optional conformance artefacts under CC-01 when consumed as inputs.
- Published CVO-01 / CVO-03 expectations.

### Constitutional outputs

- Structural verification disposition: **satisfied** or **not-satisfied**.
- On not-satisfied: lawful **deferred / escalated** when published law requires waiting or human / corpus escalation.
- Audit-speakable structure note (layering / ownership separations evidenced: true/false).
- Explicit non-certification: no permanent structural certificate is emitted.

### Permitted verification

- Evaluate evidence that educational meaning authorship remains with Programme VI producers, not with runtime or UI modules claiming meaning.
- Evaluate evidence that orchestration ownership / tip / state authorship remains with Programme VII producers.
- Evaluate evidence that runtime executes published law rather than inventing parallel authority maps.
- Detect collapsed “god services” that absorb forbidden constitutional responsibilities.
- Consume established CT links; emit CV-07-compatible governance notes when authority preservation is material.

### Prohibited verification

- Require a particular directory tree, framework, or ORM as constitutional structure.
- Rewrite published layering diagrams to match the code under review.
- Invent CT relationships so structural evidence “passes.”
- Treat architectural preference docs as Constitution / EIP amendments.
- Declare educational meaning “owned by whichever service holds the data.”
- Certify a package layout or service topology as permanently verified.
- Use CV-01 to create new constitutional layering law.

---

## 4. CV-02 — Behavioural Verification

### Constitutional purpose

Evaluate **implementation evidence** that **observable educational and execution behaviours** obey published constitutional rules — so students experience only lawful refusal, deferral, escalation, progression, and explanation postures.

### Constitutional scope

Behaviours whose constitutional meaning is published (for example refuse when evidence is missing, defer when continuity requires waiting, escalate when ownership conflicts). Does **not** grade pedagogy quality, invent new behavioural law, or certify behaviour as permanently lawful.

### Constitutional inputs

- Published behavioural rules from Constitution / EIP / Programmes VI–VIII (objectives, boundaries, transition rules, contract permitted / prohibited execution).
- Named behavioural evidence (specified flows, observed dispositions, published event / recommendation / state outcomes).
- Established CT relationships for those behaviours / artefacts.
- Optional conformance artefacts under CC-02 when consumed as inputs.
- Published CVO-01 / CVO-02 expectations.

### Constitutional outputs

- Behavioural verification disposition: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named rule bindings that the behavioural evidence obeyed or violated.
- Audit-speakable behaviour note (published disposition honesty evidenced: true/false).
- Explicit non-certification note.

### Permitted verification

- Evaluate evidence that published refuse / defer / escalate paths are available when law requires them.
- Evaluate evidence that published success paths do not invent meaning, ownership, tips, or state.
- Detect silent improvisation where published law requires a stop.
- Compose with CV-03…CV-06 when behaviour spans evidence, runtime, interface, or API surfaces.

### Prohibited verification

- Invent “helpful” behaviours not authorised by published law and call them satisfied.
- Soft-rewrite Programme VI coach rules so observed UX passes.
- Treat A/B winners, engagement optimisers, or demo scripts as behavioural constitutional law.
- Equate “students finished the flow” with behavioural requirement satisfaction.
- Certify a UX flow or demo script as permanently verified.
- Use CV-02 to author new runtime or educational behaviour.

---

## 5. CV-03 — Evidence Verification

### Constitutional purpose

Evaluate **implementation evidence** that the implementation’s **evidence handling** obeys published Educational Evidence and Programme VIII evidence consumption / validation / completion law — so warrants are consumed, validated, and completed exactly as published.

### Constitutional scope

Fidelity to EIP-002, Programme VIII evidence corpora (EC / EV / ECC and related boundaries), and Programme VII orchestration evidence artefacts as published. Does **not** mint educational evidence, reclassify claims, judge educational quality, or certify handlers as permanently lawful.

### Constitutional inputs

- Published evidence law (EIP-002; Programme VIII evidence consumption, validation, completion; Programme VII completion evidence as applicable).
- Named evidence-handling implementation evidence (consumers, validators, provenance preservation paths, refusal paths).
- Established CT relationships (typically CT-03 and related).
- Optional conformance artefacts under CC-03 when consumed as inputs.
- Published CVO-01 / CVO-04 expectations and EC / EV catalogues as *subjects of fidelity*, not as this CV catalogue.

### Constitutional outputs

- Evidence-handling verification disposition: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named evidence-law bindings (corpus paths; EC / EV identities as subjects where applicable).
- Audit-speakable evidence-handling note (no invention / alteration / reclassification / provenance fabrication evidenced: true/false).
- Explicit non-certification note.

### Permitted verification

- Evaluate evidence that only published EC categories are treated as constitutional evidence.
- Evaluate evidence that validation specialises eligibility (EV) without rewriting warrants.
- Evaluate provenance preservation and claim-ladder honesty through handling paths.
- Detect bypass of constitutional evidence requirements for product convenience.

### Prohibited verification

- Invent, alter, enrich, or reclassify educational evidence during “verification fixing.”
- Treat storage acknowledgements, Twin estimates, or analytics events as Educational Evidence.
- Substitute EV eligibility for educational quality or mastery judgement.
- Amend EIP-002 or Programme VIII evidence corpora via findings.
- Certify an evidence pipeline as permanently verified.
- Use CV-03 to become an evidence producer.

---

## 6. CV-04 — Runtime Verification

### Constitutional purpose

Evaluate **implementation evidence** that the implementation’s **runtime execution posture** obeys published Programme VIII runtime contracts, event processing, execution completion, and service / collaboration law — so software executes constitutional law without becoming it.

### Constitutional scope

Fidelity to RC-01…RC-07 and sibling Programme VIII WS1 / WS3 (and related) runtime corpora. Does **not** require a particular process model, message bus, or “Runtime A” brand. Does **not** certify a runtime topology as permanently lawful.

### Constitutional inputs

- Published runtime corpora (contracts, event processing, execution completion, services, collaboration, related boundaries).
- Named runtime implementation evidence (execution paths, contract bindings, completion records, service responsibility maps).
- Established CT relationships (typically CT-04 and related).
- Optional conformance artefacts under CC-04 when consumed as inputs.
- Published CVO-01 / CVO-03 expectations.

### Constitutional outputs

- Runtime verification disposition: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named RC / runtime-corpus bindings obeyed or violated by evidence.
- Audit-speakable runtime note (execution of published law without law invention evidenced: true/false).
- Explicit non-certification note.

### Permitted verification

- Evaluate evidence that material acts map to published RC bindings as required.
- Evaluate evidence that event processing and completion follow published classes and fulfilment rules.
- Evaluate evidence that services collaborate without transferring forbidden authority or merging responsibilities.
- Detect runtime improvisation that invents unpublished contracts or completion meanings.

### Prohibited verification

- Require a specific language, framework, queue, or host as constitutional runtime.
- Treat “service is up” as RC satisfaction.
- Rewrite Programme VIII contract text to match observed code.
- Elevate Runtime A topology into constitutional law.
- Certify Runtime A (or any successor) as permanently verified.
- Use CV-04 to author new runtime behaviour under a verification badge.

---

## 7. CV-05 — Interface Verification

### Constitutional purpose

Evaluate **implementation evidence** that **interface composition** obeys published Programme VIII interface / composition / completion law — so composed surfaces remain subordinate to constitutional producers and do not invent educational meaning.

### Constitutional scope

Fidelity to published interface composition models, boundaries, and completion corpora. Does **not** mandate a particular UI kit, widget set, or frontend framework. Does **not** certify an interface surface as permanently lawful.

### Constitutional inputs

- Published interface / composition / interface-completion corpora and related boundaries.
- Named interface implementation evidence (composition maps, handoff points, surface responsibilities).
- Established CT relationships (typically CT-05 and related).
- Optional conformance artefacts under CC-05 when consumed as inputs.
- Published CVO-03 / CVO-05 expectations.

### Constitutional outputs

- Interface verification disposition: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named interface-corpus bindings obeyed or violated by evidence.
- Audit-speakable interface note (composition without meaning invention / authority transfer evidenced: true/false).
- Explicit non-certification note.

### Permitted verification

- Evaluate evidence that composed interfaces consume published contracts / evidence / recommendations / state without rewriting them.
- Evaluate evidence that completion of interface responsibilities follows published fulfilment rules.
- Detect UI or adapter layers that silently become educational or ownership authorities.
- Compose with CV-02 / CV-06 when interface behaviour or API exposure is material.

### Prohibited verification

- Require a particular design system or component library as constitutional.
- Treat visual polish or accessibility tooling scores as constitutional interface law (unless a published constitutional specification so states — none do by default).
- Invent interface completion meanings to force satisfaction.
- Amend Programme VIII interface corpora via findings.
- Certify a UI kit or composition map as permanently verified.
- Use CV-05 to author educational tips or state transitions.

---

## 8. CV-06 — API Verification

### Constitutional purpose

Evaluate **implementation evidence** that **API surfaces** obey published constitutional contract, boundary, and explainability obligations that apply to externally or internally callable educational / runtime acts — so APIs execute and expose law without inventing it.

### Constitutional scope

Fidelity of callable surfaces to published constitutional obligations (authorisation of acts, evidence / contract honesty, refusal postures, explainability hooks as published). Does **not** require REST, OpenAPI, GraphQL, or any particular protocol as constitutional. Does **not** certify an API inventory as permanently lawful.

### Constitutional inputs

- Published constitutional obligations for callable acts (Programme VIII contracts / boundaries / explainability; Programme VI / VII boundaries as they constrain exposed acts).
- Named API implementation evidence (endpoint / operation inventories, request–response dispositions, error / refuse / escalate postures — protocol-neutral).
- Established CT relationships (typically CT-06 and related).
- Optional conformance artefacts under CC-06 when consumed as inputs.
- Published CVO-01 / CVO-03 / CVO-05 expectations.

### Constitutional outputs

- API verification disposition: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named constitutional obligations obeyed or violated by the callable-surface evidence.
- Audit-speakable API note (callable acts remain law-executing, not law-making: true/false).
- Explicit non-certification note.

### Permitted verification

- Evaluate evidence that exposed acts map to published authorising contracts / ownership / evidence rules.
- Evaluate evidence that refuse / defer / escalate dispositions are expressible when law requires them.
- Evaluate evidence that APIs do not invent educational meaning fields or soft-upgrade claim classes.
- Detect protocol theatre (schema green) presented as constitutional satisfaction without corpus binding.

### Prohibited verification

- Mandate REST, OpenAPI, gRPC, or a particular schema language as constitutional.
- Treat OpenAPI lint success, HTTP status fashion, or SDK generation as constitutional law.
- Rewrite published boundaries so a convenient endpoint “passes.”
- Expose Twin / Adaptive estimates as Educational Evidence via API without published warrant.
- Certify an OpenAPI document or SDK as permanently verified.
- Use CV-06 to create new constitutional API law or educational meaning.

---

## 9. CV-07 — Governance Verification

### Constitutional purpose

Evaluate **implementation evidence** that **governance and authority-preservation obligations** are satisfied — so constitutional authority, conformance honesty, traceability provenance, continuity, and explainability survive operational pressure without verification becoming a second constitution or a certification bureau.

### Constitutional scope

Fidelity to published governance / authority / continuity / explainability / conformance / traceability obligations as they bind how implementations and assessment machinery preserve constitutional authority. Includes reconstructability of verification assessments under this Model. Does **not** mandate a particular log shipper, SIEM, governance tool, or compliance vendor. Does **not** certify an organisation, release, or stack as permanently governed.

### Constitutional inputs

- Published governance-relevant specifications (Constitution / EIP authority and continuity / explainability standards; Programme VII authority corpora; WS1 conformance and traceability boundaries; this Model’s boundaries and explainability corpus).
- Named governance implementation evidence (authority-preservation trails; assessment records; refusal / escalation paths; non-certification posture records).
- Established CT relationships (including CT-07 assessment lineage where applicable).
- Optional conformance artefacts under CC-07 and related when consumed as inputs.
- Published CVO-04 / CVO-05 / CVO-06 expectations.

### Constitutional outputs

- Governance verification disposition: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Confirmation that authority preservation, non-legislation, non-certification, and reconstructability obligations are evidenced.
- Audit-speakable meta-record (specs / evidence / relationships / findings / boundaries preserved: true/false).
- Explicit non-certification note (governance satisfaction is not a certificate of the product).

### Permitted verification

- Evaluate evidence that material educational / runtime acts leave constitutional refs, not only technical logs.
- Evaluate evidence that material CV assessments answer the mandatory explainability questions.
- Evaluate evidence that verification / conformance / lineage machinery does not invent law, rewrite specs, or certify implementations.
- Detect erasure of prior lawful history for UX or log-cost convenience.
- Confirm student / developer / auditor projections can share one truth.

### Prohibited verification

- Require a particular logging vendor, GRC product, or metrics backend as constitutional.
- Treat log volume, retention dashboards, SOC2 theatre, or “observability scores” as constitutional governance law.
- Fabricate governance trails after the fact to force satisfaction.
- Erase not-satisfied findings to present a green history.
- Issue organisational or product certificates under the label CV-07.
- Use CV-07 to invent educational meaning or amend constitutional specifications.

---

## 10. Catalogue Discipline

| Rule | Meaning |
|------|---------|
| **Closed set** | Only CV-01…CV-07 are constitutional verification types |
| **Multi-bind allowed** | A single assessment may bind multiple CV types when published law requires |
| **No silent skip** | Required types for a scope may not be omitted for convenience |
| **Subjects ≠ types** | CC / CT / RC / EC / EV / Programme VI–VII IDs may appear as *inputs*; they are not CV types |
| **Findings ≠ amendments** | Not-satisfied results may motivate corpus proposals; they do not enact law |
| **Findings ≠ certificates** | Satisfied results never certify implementations, stacks, vendors, or releases |
| **Consume, do not invent** | CT relationships and CC artefacts are inputs; inventing them to force satisfaction is unlawful |
| **Technology-neutral** | No CV type privileges a language, framework, protocol, or CI vendor |

---

## 11. Closing Statement

> **Only published verification types may speak to whether implementation evidence satisfies published constitutional requirements.  
> Unpublished “implied verification,” green pipelines, preferred stacks, and certificates are not constitutional law — and never become it through verification theatre.**
