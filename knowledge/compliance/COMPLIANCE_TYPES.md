# Compliance Types

**Programme:** IX — Workstream 3 — Constitutional Conformance Architecture  
**Milestone:** MS001 — Constitutional Compliance Model  
**Classification:** Closed catalogue of recognised constitutional compliance categories  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional compliance categories** (CCM-01…CCM-07).

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_COMPLIANCE_MODEL.md`](CONSTITUTIONAL_COMPLIANCE_MODEL.md)
3. [`COMPLIANCE_OBJECTIVES.md`](COMPLIANCE_OBJECTIVES.md)
4. [`../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md)
5. [`../conformance/CONFORMANCE_TYPES.md`](../conformance/CONFORMANCE_TYPES.md)
6. [`../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md`](../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md)
7. [`../conformance/traceability/TRACEABILITY_TYPES.md`](../conformance/traceability/TRACEABILITY_TYPES.md)
8. [`../verification/CONSTITUTIONAL_VERIFICATION_MODEL.md`](../verification/CONSTITUTIONAL_VERIFICATION_MODEL.md)
9. [`../verification/VERIFICATION_TYPES.md`](../verification/VERIFICATION_TYPES.md)
10. Programme VI corpora under [`../educational/`](../educational/)
11. Programme VII corpora under [`../orchestration/`](../orchestration/)
12. Programme VIII corpora under [`../runtime/`](../runtime/)
13. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published compliance types may speak to whether published constitutional obligations have been satisfied.  
> Unpublished “implied compliance” is constitutionally defective.**

**Catalogue disambiguation:** CCM-01…CCM-07 here are *constitutional compliance types*. They are not MS001 conformance types (CC-01…CC-07), MS002 traceability types (CT-01…CT-07), WS2 verification types (CV-01…CV-07), Educational Validation Framework coach capability IDs, Programme VIII runtime contracts (RC-xx), evidence categories (EC-xx), or evidence validation categories (EV-xx).

---

## 1. Purpose

Determination without a closed compliance catalogue invents law by proximity: whichever badge, report, or pipeline happens to be green becomes the tutor’s “proof the system is constitutionally compliant.”

This catalogue names the only lawful constitutional compliance types a determination may apply — and binds each type to purpose, scope, inputs, outputs, and permitted / prohibited determinations.

---

## 2. Catalogue Overview

| ID | Compliance type | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|-----------------|--------------------------------|----------------|-----------------|
| **CCM-01** | Structural Compliance | Determine whether structural / layering obligations have been satisfied | Published layering / authority obligations + CV structural findings + CT links | Structure obligations satisfied / not-satisfied (+ deferred / escalated) |
| **CCM-02** | Behavioural Compliance | Determine whether behavioural obligations have been satisfied | Published behavioural obligations + CV behavioural findings + CT links | Behaviour obligations satisfied / not-satisfied (+ deferred / escalated) |
| **CCM-03** | Evidence Compliance | Determine whether evidence-handling obligations have been satisfied | EIP-002 + Programme VIII evidence obligations + CV evidence findings + CT links | Evidence obligations satisfied / not-satisfied |
| **CCM-04** | Runtime Compliance | Determine whether runtime execution obligations have been satisfied | Programme VIII runtime obligations + CV runtime findings + CT links | Runtime obligations satisfied / not-satisfied |
| **CCM-05** | Interface Compliance | Determine whether interface composition obligations have been satisfied | Programme VIII interface obligations + CV interface findings + CT links | Interface obligations satisfied / not-satisfied |
| **CCM-06** | API Compliance | Determine whether API-facing obligations have been satisfied | Published callable-act obligations + CV API findings + CT links | API obligations satisfied / not-satisfied |
| **CCM-07** | Governance Compliance | Determine whether governance / authority-preservation obligations have been satisfied | Governance / authority / continuity obligations + CV governance findings + CT links | Governance obligations satisfied / not-satisfied |

Material determination must map to one or more of these types as published law requires. Cross-cutting situations may bind multiple CCM types; none may invent a type outside this catalogue.

**Relation to CC / CT / CV / RC / EC / EV:** Those catalogues remain defined solely by their owners. CCM types *determine whether published obligations have been satisfied* given consumed findings and lineage; they do not replace, reclassify, certify, re-verify, or invent those catalogues.

**Relation to educational quality:** No CCM type judges whether learning was good, whether a tip was wise, or whether the student is ready. Satisfied ≠ quality. Satisfied ≠ certified. Satisfied ≠ permanently conformant. Satisfied ≠ permanently verified.

---

## 3. CCM-01 — Structural Compliance

### Constitutional purpose

Determine whether published **structural and layering obligations** have been **satisfied** — so educational meaning, orchestration, runtime execution, and delivery surfaces do not collapse into a single unlawful authority — using consumed structural verification findings and established lineage.

### Constitutional scope

Obligation status for structural placement of responsibilities, ownership boundaries, and layering duties published by Constitution / EIP / Programmes VI–VIII (and related authority matrices). Does **not** require a particular package layout, language module system, or repository topology beyond what published law states. Does **not** certify structure as permanently lawful.

### Constitutional inputs

- Published structural / layering / authority obligations and specifications (Constitution, EIP-001, Programme VI / VII / VIII boundaries and stack positions).
- Identifiable structural verification findings (typically under CV-01).
- Established CT relationships linking those specs / artefacts / findings (typically CT-01 / CT-02).
- Optional conformance relationships / artefacts under CC-01 when consumed as inputs.
- Published CCMO-01 / CCMO-03 expectations.

### Constitutional outputs

- Structural compliance determination: **satisfied** or **not-satisfied**.
- On not-satisfied: lawful **deferred / escalated** when published law requires waiting or human / corpus escalation.
- Audit-speakable structure note (layering / ownership obligations satisfied: true/false).
- Explicit non-certification: no permanent structural certificate is emitted.

### Permitted determinations

- Determine obligation status that educational meaning authorship remains with Programme VI producers, not with runtime or UI modules claiming meaning.
- Determine obligation status that orchestration ownership / tip / state authorship remains with Programme VII producers.
- Determine obligation status that runtime executes published law rather than inventing parallel authority maps.
- Detect collapsed “god services” that absorb forbidden constitutional responsibilities — as obligation failure when findings so show.
- Consume established CT links and CV findings; emit CCM-07-compatible governance notes when authority preservation is material.

### Prohibited determinations

- Require a particular directory tree, framework, or ORM as constitutional structure.
- Rewrite published layering diagrams to match the code under review.
- Invent CT relationships or rewrite CV findings so structural obligations “pass.”
- Treat architectural preference docs as Constitution / EIP amendments.
- Declare educational meaning “owned by whichever service holds the data.”
- Certify a package layout or service topology as permanently compliant.
- Use CCM-01 to create new constitutional layering law.

---

## 4. CCM-02 — Behavioural Compliance

### Constitutional purpose

Determine whether published **behavioural obligations** have been **satisfied** — so students experience only lawful refusal, deferral, escalation, progression, and explanation postures — using consumed behavioural verification findings and established lineage.

### Constitutional scope

Obligation status for behaviours whose constitutional meaning is published (for example refuse when evidence is missing, defer when continuity requires waiting, escalate when ownership conflicts). Does **not** grade pedagogy quality, invent new behavioural law, or certify behaviour as permanently lawful.

### Constitutional inputs

- Published behavioural obligations from Constitution / EIP / Programmes VI–VIII (objectives, boundaries, transition rules, contract permitted / prohibited execution).
- Identifiable behavioural verification findings (typically under CV-02).
- Established CT relationships for those behaviours / artefacts / findings.
- Optional conformance relationships / artefacts under CC-02 when consumed as inputs.
- Published CCMO-01 / CCMO-02 expectations.

### Constitutional outputs

- Behavioural compliance determination: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named obligation bindings that findings show were satisfied or violated.
- Audit-speakable behaviour note (published disposition honesty obligations satisfied: true/false).
- Explicit non-certification note.

### Permitted determinations

- Determine obligation status that published refuse / defer / escalate paths are available when law requires them.
- Determine obligation status that published success paths do not invent meaning, ownership, tips, or state.
- Detect silent improvisation where published law requires a stop — as obligation failure when findings so show.
- Compose with CCM-03…CCM-06 when behaviour spans evidence, runtime, interface, or API surfaces.

### Prohibited determinations

- Invent “helpful” behaviours not authorised by published law and call them satisfied.
- Soft-rewrite Programme VI coach rules so observed UX passes.
- Treat A/B winners, engagement optimisers, or demo scripts as behavioural constitutional law.
- Equate “students finished the flow” with behavioural obligation satisfaction.
- Certify a UX flow or demo script as permanently compliant.
- Use CCM-02 to author new runtime or educational behaviour.

---

## 5. CCM-03 — Evidence Compliance

### Constitutional purpose

Determine whether published **evidence-handling obligations** have been **satisfied** — so warrants are consumed, validated, and completed exactly as published — using consumed evidence verification findings and established lineage.

### Constitutional scope

Obligation status for fidelity to EIP-002, Programme VIII evidence corpora (EC / EV / ECC and related boundaries), and Programme VII orchestration evidence artefacts as published. Does **not** mint educational evidence, reclassify claims, judge educational quality, or certify handlers as permanently lawful.

### Constitutional inputs

- Published evidence obligations (EIP-002; Programme VIII evidence consumption, validation, completion; Programme VII completion evidence as applicable).
- Identifiable evidence-handling verification findings (typically under CV-03).
- Established CT relationships (typically CT-03 and related).
- Optional conformance relationships / artefacts under CC-03 when consumed as inputs.
- Published CCMO-01 / CCMO-04 expectations and EC / EV catalogues as *subjects of obligation*, not as this CCM catalogue.

### Constitutional outputs

- Evidence-handling compliance determination: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named evidence-obligation bindings (corpus paths; EC / EV identities as subjects where applicable).
- Audit-speakable evidence-handling note (no invention / alteration / reclassification / provenance fabrication obligations satisfied: true/false).
- Explicit non-certification note.

### Permitted determinations

- Determine obligation status that only published EC categories are treated as constitutional evidence.
- Determine obligation status that validation specialises eligibility (EV) without rewriting warrants.
- Determine obligation status for provenance preservation and claim-ladder honesty through handling paths.
- Detect bypass of constitutional evidence requirements for product convenience — as obligation failure when findings so show.

### Prohibited determinations

- Invent, alter, enrich, or reclassify educational evidence during “compliance fixing.”
- Treat storage acknowledgements, Twin estimates, or analytics events as Educational Evidence.
- Substitute EV eligibility for educational quality or mastery judgement.
- Amend EIP-002 or Programme VIII evidence corpora via determinations.
- Certify an evidence pipeline as permanently compliant.
- Use CCM-03 to become an evidence producer.

---

## 6. CCM-04 — Runtime Compliance

### Constitutional purpose

Determine whether published **runtime execution obligations** have been **satisfied** — so software executes constitutional law without becoming it — using consumed runtime verification findings and established lineage.

### Constitutional scope

Obligation status for fidelity to RC-01…RC-07 and sibling Programme VIII WS1 / WS3 (and related) runtime corpora. Does **not** require a particular process model, message bus, or “Runtime A” brand. Does **not** certify a runtime topology as permanently lawful.

### Constitutional inputs

- Published runtime obligations (contracts, event processing, execution completion, services, collaboration, related boundaries).
- Identifiable runtime verification findings (typically under CV-04).
- Established CT relationships (typically CT-04 and related).
- Optional conformance relationships / artefacts under CC-04 when consumed as inputs.
- Published CCMO-01 / CCMO-03 expectations.

### Constitutional outputs

- Runtime compliance determination: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named RC / runtime-corpus obligations satisfied or violated per consumed findings.
- Audit-speakable runtime note (execution of published law without law invention obligations satisfied: true/false).
- Explicit non-certification note.

### Permitted determinations

- Determine obligation status that material acts map to published RC bindings as required.
- Determine obligation status that event processing and completion follow published classes and fulfilment rules.
- Determine obligation status that services collaborate without transferring forbidden authority or merging responsibilities.
- Detect runtime improvisation that invents unpublished contracts or completion meanings — as obligation failure when findings so show.

### Prohibited determinations

- Require a specific language, framework, queue, or host as constitutional runtime.
- Treat “service is up” as RC obligation satisfaction.
- Rewrite Programme VIII contract text to match observed code.
- Elevate Runtime A topology into constitutional law.
- Certify Runtime A (or any successor) as permanently compliant.
- Use CCM-04 to author new runtime behaviour under a compliance badge.

---

## 7. CCM-05 — Interface Compliance

### Constitutional purpose

Determine whether published **interface composition obligations** have been **satisfied** — so composed surfaces remain subordinate to constitutional producers and do not invent educational meaning — using consumed interface verification findings and established lineage.

### Constitutional scope

Obligation status for fidelity to published interface composition models, boundaries, and completion corpora. Does **not** mandate a particular UI kit, widget set, or frontend framework. Does **not** certify an interface surface as permanently lawful.

### Constitutional inputs

- Published interface / composition / interface-completion obligations and related boundaries.
- Identifiable interface verification findings (typically under CV-05).
- Established CT relationships (typically CT-05 and related).
- Optional conformance relationships / artefacts under CC-05 when consumed as inputs.
- Published CCMO-03 / CCMO-05 expectations.

### Constitutional outputs

- Interface compliance determination: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named interface-corpus obligations satisfied or violated per consumed findings.
- Audit-speakable interface note (composition without meaning invention / authority transfer obligations satisfied: true/false).
- Explicit non-certification note.

### Permitted determinations

- Determine obligation status that composed interfaces consume published contracts / evidence / recommendations / state without rewriting them.
- Determine obligation status that completion of interface responsibilities follows published fulfilment rules.
- Detect UI or adapter layers that silently become educational or ownership authorities — as obligation failure when findings so show.
- Compose with CCM-02 / CCM-06 when interface behaviour or API exposure is material.

### Prohibited determinations

- Require a particular design system or component library as constitutional.
- Treat visual polish or accessibility tooling scores as constitutional interface law (unless a published constitutional specification so states — none do by default).
- Invent interface completion meanings to force satisfaction.
- Amend Programme VIII interface corpora via determinations.
- Certify a UI kit or composition map as permanently compliant.
- Use CCM-05 to author educational tips or state transitions.

---

## 8. CCM-06 — API Compliance

### Constitutional purpose

Determine whether published **API-facing constitutional obligations** have been **satisfied** — so APIs execute and expose law without inventing it — using consumed API verification findings and established lineage.

### Constitutional scope

Obligation status for fidelity of callable surfaces to published constitutional obligations (authorisation of acts, evidence / contract honesty, refusal postures, explainability hooks as published). Does **not** require REST, OpenAPI, GraphQL, or any particular protocol as constitutional. Does **not** certify an API inventory as permanently lawful.

### Constitutional inputs

- Published constitutional obligations for callable acts (Programme VIII contracts / boundaries / explainability; Programme VI / VII boundaries as they constrain exposed acts).
- Identifiable API verification findings (typically under CV-06).
- Established CT relationships (typically CT-06 and related).
- Optional conformance relationships / artefacts under CC-06 when consumed as inputs.
- Published CCMO-01 / CCMO-03 / CCMO-05 expectations.

### Constitutional outputs

- API compliance determination: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Named constitutional obligations satisfied or violated by the callable-surface findings.
- Audit-speakable API note (callable acts remain law-executing, not law-making: true/false).
- Explicit non-certification note.

### Permitted determinations

- Determine obligation status that exposed acts map to published authorising contracts / ownership / evidence rules.
- Determine obligation status that refuse / defer / escalate dispositions are expressible when law requires them.
- Determine obligation status that APIs do not invent educational meaning fields or soft-upgrade claim classes.
- Detect protocol theatre (schema green) presented as constitutional satisfaction without corpus binding — as obligation failure when findings so show.

### Prohibited determinations

- Mandate REST, OpenAPI, gRPC, or a particular schema language as constitutional.
- Treat OpenAPI lint success, HTTP status fashion, or SDK generation as constitutional law.
- Rewrite published boundaries so a convenient endpoint “passes.”
- Expose Twin / Adaptive estimates as Educational Evidence via API without published warrant.
- Certify an OpenAPI document or SDK as permanently compliant.
- Use CCM-06 to create new constitutional API law or educational meaning.

---

## 9. CCM-07 — Governance Compliance

### Constitutional purpose

Determine whether published **governance and authority-preservation obligations** have been **satisfied** — so constitutional authority, conformance honesty, traceability provenance, verification integrity, continuity, and explainability survive operational pressure without compliance becoming a second constitution or a certification bureau.

### Constitutional scope

Obligation status for fidelity to published governance / authority / continuity / explainability / conformance / traceability / verification obligations as they bind how implementations and assessment machinery preserve constitutional authority. Includes reconstructability of compliance determinations under this Model. Does **not** mandate a particular log shipper, SIEM, governance tool, or compliance vendor. Does **not** certify an organisation, release, or stack as permanently governed.

### Constitutional inputs

- Published governance-relevant obligations (Constitution / EIP authority and continuity / explainability standards; Programme VII authority corpora; WS1 conformance and traceability boundaries; WS2 verification boundaries; this Model’s boundaries and explainability corpus).
- Identifiable governance verification findings (typically under CV-07) and related assessment trails.
- Established CT relationships (including CT-07 assessment lineage where applicable).
- Optional conformance relationships / artefacts under CC-07 and related when consumed as inputs.
- Published CCMO-04 / CCMO-05 / CCMO-06 expectations.

### Constitutional outputs

- Governance compliance determination: **satisfied** or **not-satisfied** (+ deferred / escalated).
- Confirmation that authority preservation, non-legislation, non-certification, and reconstructability obligations are satisfied per consumed findings.
- Audit-speakable meta-record (obligations / findings / specs / determination / boundaries preserved: true/false).
- Explicit non-certification note (governance satisfaction is not a certificate of the product).

### Permitted determinations

- Determine obligation status that material educational / runtime acts leave constitutional refs, not only technical logs.
- Determine obligation status that material CCM determinations answer the mandatory explainability questions.
- Determine obligation status that verification / conformance / lineage / compliance machinery does not invent law, rewrite specs, or certify implementations.
- Detect erasure of prior lawful history for UX or log-cost convenience — as obligation failure when findings so show.
- Confirm student / developer / auditor projections can share one truth.

### Prohibited determinations

- Require a particular logging vendor, GRC product, or metrics backend as constitutional.
- Treat log volume, retention dashboards, SOC2 theatre, or “observability scores” as constitutional governance law.
- Fabricate governance trails after the fact to force satisfaction.
- Erase not-satisfied determinations to present a green history.
- Issue organisational or product certificates under the label CCM-07.
- Use CCM-07 to invent educational meaning or amend constitutional specifications.

---

## 10. Catalogue Discipline

| Rule | Meaning |
|------|---------|
| **Closed set** | Only CCM-01…CCM-07 are constitutional compliance types |
| **Multi-bind allowed** | A single determination may bind multiple CCM types when published law requires |
| **No silent skip** | Required types for a scope may not be omitted for convenience |
| **Subjects ≠ types** | CC / CT / CV / RC / EC / EV / Programme VI–VII IDs may appear as *inputs*; they are not CCM types |
| **Determinations ≠ amendments** | Not-satisfied results may motivate corpus proposals; they do not enact law |
| **Determinations ≠ certificates** | Satisfied results never certify implementations, stacks, vendors, or releases |
| **Consume, do not invent** | CV findings, CT relationships, and CC artefacts are inputs; inventing or rewriting them to force satisfaction is unlawful |
| **Technology-neutral** | No CCM type privileges a language, framework, protocol, or CI vendor |

---

## 11. Closing Statement

> **Only published compliance types may speak to whether published constitutional obligations have been satisfied.  
> Unpublished “implied compliance,” green seals, preferred stacks, and certificates are not constitutional law — and never become it through compliance theatre.**
