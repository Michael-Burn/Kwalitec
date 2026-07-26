# Traceability Types

**Programme:** IX — Workstream 1 — Constitutional Conformance Architecture  
**Milestone:** MS002 — Constitutional Traceability Model  
**Classification:** Closed catalogue of recognised constitutional traceability categories  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional traceability categories** (CT-01…CT-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_TRACEABILITY_MODEL.md`](CONSTITUTIONAL_TRACEABILITY_MODEL.md)
3. [`TRACEABILITY_OBJECTIVES.md`](TRACEABILITY_OBJECTIVES.md)
4. [`../CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../CONSTITUTIONAL_CONFORMANCE_MODEL.md)
5. [`../CONFORMANCE_TYPES.md`](../CONFORMANCE_TYPES.md)
6. Programme VI corpora under [`../../educational/`](../../educational/)
7. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
8. Programme VIII corpora under [`../../runtime/`](../../runtime/)
9. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published traceability types may certify constitutional lineage among specifications, artefacts, and findings.  
> Unpublished “implied traceability” is constitutionally defective.**

**Catalogue disambiguation:** CT-01…CT-07 here are *constitutional traceability types*. They are not MS001 conformance types (CC-01…CC-07), Educational Validation Framework coach capability IDs, Programme VIII runtime contracts (RC-xx), evidence categories (EC-xx), or evidence validation categories (EV-xx).

---

## 1. Purpose

Linkage without a closed traceability catalogue invents law by proximity: whichever ticket, dependency edge, or pipeline annotation happens to exist becomes the tutor’s “proof the system is constitutionally documented.”

This catalogue names the only lawful constitutional traceability types a relationship may apply — and binds each type to purpose, scope, inputs, outputs, and permitted / prohibited relationships.

---

## 2. Catalogue Overview

| ID | Traceability type | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|-------------------|--------------------------------|----------------|-----------------|
| **CT-01** | Specification Traceability | Preserve lawful relationships among published constitutional specifications | Published corpus identities | Spec-to-spec lineage records |
| **CT-02** | Implementation Traceability | Preserve lawful relationships from published specs to implementation artefacts | Published specs + named artefacts | Spec-to-artefact lineage records |
| **CT-03** | Evidence Traceability | Preserve lineage for evidence-handling artefacts under published evidence law | EIP-002 + Programme VIII evidence corpora + evidence artefacts | Evidence-lineage records |
| **CT-04** | Runtime Traceability | Preserve lineage for runtime execution artefacts under published runtime law | Programme VIII runtime corpora + runtime artefacts | Runtime-lineage records |
| **CT-05** | Interface Traceability | Preserve lineage for interface composition artefacts under published interface law | Programme VIII interface corpora + interface artefacts | Interface-lineage records |
| **CT-06** | API Traceability | Preserve lineage for API exposure artefacts under published callable-act obligations | Published API-facing constitutional obligations + API artefacts | API-lineage records |
| **CT-07** | Assessment Traceability | Preserve lineage for conformance assessments and findings under MS001 | MS001 assessment records + related specs / artefacts | Assessment-lineage records |

Material relationships must map to one or more of these types as published law requires. Cross-cutting situations may bind multiple CT types; none may invent a type outside this catalogue.

**Relation to CC / RC / EC / EV:** Those catalogues remain defined solely by their owners. CT types *preserve lineage* to those (and sibling) published laws and assessed subjects; they do not replace, reclassify, or evaluate fidelity in their place.

**Relation to educational quality:** No CT type judges whether learning was good, whether a tip was wise, or whether the student is ready. Traced ≠ quality. Traced ≠ conformant.

---

## 3. CT-01 — Specification Traceability

### Constitutional purpose

Preserve lawful **relationships among published constitutional specifications** — so subordinate corpora remain reconstructably related to their superior law without inventing amendments or collapsing distinct horizons.

### Constitutional scope

Published Constitution / EIP / Programme VI / VII / VIII / Programme IX MS001 specification identities and their declared subordination / composition relationships. Does **not** create new constitutional documents, merge corpora, or rewrite meaning by “linking harder.”

### Constitutional inputs

- Published constitutional specification identities (paths, catalogue IDs, authority statements).
- Published stack / subordination declarations among those specifications.
- Published CTO-01 / CTO-02 expectations.

### Constitutional outputs

- Spec-to-spec lineage record under CT-01.
- Named superior / subordinate / sibling relationship notes as published (never invented).
- Audit-speakable specification-provenance note (published identities preserved: true/false).

### Permitted relationships

- Relate a Programme IX conformance objective to the published MS001 Model that defines it.
- Relate a Programme VIII contract corpus to EIP / Constitution authorities it cites as superior.
- Record composition among published sibling corpora without merging their meanings.
- Emit CT-07-compatible records when assessment cites multi-spec sets.

### Prohibited relationships

- Invent a new constitutional specification identity via a “traceability doc.”
- Soft-merge Programme VI and Programme VIII meanings because they are “linked.”
- Treat architecture / Version 2 preference docs as Constitution / EIP amendments through lineage.
- Declare unpublished customs as peer specifications.
- Use CT-01 to create or modify constitutional law.

---

## 4. CT-02 — Implementation Traceability

### Constitutional purpose

Preserve lawful **relationships from published constitutional specifications to named implementation artefacts** — so code, behaviour, and delivery surfaces remain reconstructably related to the law they claim to obey, without becoming that law.

### Constitutional scope

Named implementation subjects (modules, services, adapters, behavioural classes, stores as organisational units) related to published obligations. Does **not** require a particular package layout, language, or repository topology beyond what published law states — and never treats the artefact as the standard.

### Constitutional inputs

- Published constitutional specifications under which the artefact claims relevance.
- Named implementation artefacts (without treating names as law).
- Published CTO-01 / CTO-03 / CTO-06 expectations.

### Constitutional outputs

- Spec-to-artefact lineage record under CT-02.
- Named obligation bindings the artefact is claimed to relate to (not “passed”).
- Audit-speakable implementation-provenance note (artefact related without authority substitution: true/false).

### Permitted relationships

- Relate a published Programme VI boundary to the module that claims to respect it.
- Relate a published Programme VIII contract to the execution path that claims to bind it.
- Support MS001 assessment by exposing the same named subjects and corpus refs.
- Compose with CT-03…CT-06 when the artefact spans evidence, runtime, interface, or API surfaces.

### Prohibited relationships

- Treat “file mentions the doc” as constitutional law or as conformity.
- Soft-rewrite published obligations so the artefact looks related.
- Privilege a reference implementation as the constitutional standard via lineage.
- Infer authority because an artefact is linked.
- Use CT-02 to replace MS001 evaluation (“linked therefore conformant”).

---

## 5. CT-03 — Evidence Traceability

### Constitutional purpose

Preserve lineage for **evidence-handling artefacts** under published Educational Evidence and Programme VIII evidence consumption / validation / completion law — so warrants, consumers, validators, and provenance paths remain reconstructably related without inventing evidence.

### Constitutional scope

Lineage to EIP-002, Programme VIII evidence corpora (EC / EV / ECC and related boundaries), and Programme VII orchestration evidence artefacts as published. Does **not** mint evidence, reclassify claims, or judge educational quality.

### Constitutional inputs

- Published evidence law (EIP-002; Programme VIII evidence consumption, validation, completion; Programme VII completion evidence as applicable).
- Named evidence-handling artefacts (consumers, validators, provenance preservation paths, refusal paths).
- Published CTO-01 / CTO-02 expectations and EC / EV catalogues as *subjects of lineage*, not as this CT catalogue.

### Constitutional outputs

- Evidence-lineage record under CT-03.
- Named evidence-law bindings (corpus paths; EC / EV identities as subjects where applicable).
- Audit-speakable evidence-provenance note (no invention / alteration / reclassification / provenance fabrication via linkage: true/false).

### Permitted relationships

- Relate published EC categories to the handling paths that claim to consume them.
- Relate EV eligibility checks to the validation artefacts that claim to apply them.
- Preserve claim-ladder and warrant identity through lineage records.
- Compose with CT-02 / CT-07 when implementation or assessment lineage is material.

### Prohibited relationships

- Invent, alter, enrich, or reclassify evidence during “traceability fixing.”
- Treat storage acknowledgements, Twin estimates, or analytics events as Educational Evidence via a link.
- Substitute EV eligibility or CT lineage for educational quality or mastery judgement.
- Amend EIP-002 or Programme VIII evidence corpora via lineage records.
- Use CT-03 to become an evidence producer or to claim conformity without MS001.

---

## 6. CT-04 — Runtime Traceability

### Constitutional purpose

Preserve lineage for **runtime execution artefacts** under published Programme VIII runtime contracts, event processing, execution completion, and service / collaboration law — so software execution remains reconstructably related to published law without becoming it.

### Constitutional scope

Lineage to RC-01…RC-07 and sibling Programme VIII WS1 / WS3 (and related) runtime corpora. Does **not** require a particular process model, message bus, or “Runtime A” brand.

### Constitutional inputs

- Published runtime corpora (contracts, event processing, execution completion, services, collaboration, related boundaries).
- Named runtime artefacts (execution paths, contract bindings, completion records, service responsibility maps).
- Published CTO-01 / CTO-06 expectations.

### Constitutional outputs

- Runtime-lineage record under CT-04.
- Named RC / runtime-corpus bindings related (not “satisfied”).
- Audit-speakable runtime-provenance note (execution related to published law without law invention: true/false).

### Permitted relationships

- Relate material acts to published RC identities as claimed bindings.
- Relate event processing and completion artefacts to published classes and fulfilment rules.
- Relate service collaboration maps without transferring forbidden authority via the link.
- Detect missing published anchors for claimed runtime lineage (refuse invented RC identities).

### Prohibited relationships

- Require a specific language, framework, queue, or host as constitutional runtime via lineage.
- Treat “service is up” or “deps linked” as RC satisfaction.
- Rewrite Programme VIII contract text to match observed code through a trace record.
- Elevate Runtime A topology into constitutional law via CT-04.
- Use CT-04 to author new runtime behaviour or to replace CC-04 evaluation.

---

## 7. CT-05 — Interface Traceability

### Constitutional purpose

Preserve lineage for **interface composition artefacts** under published Programme VIII interface / composition / completion law — so composed surfaces remain reconstructably subordinate to constitutional producers and do not invent educational meaning through linkage.

### Constitutional scope

Lineage to published interface composition models, boundaries, and completion corpora. Does **not** mandate a particular UI kit, widget set, or frontend framework.

### Constitutional inputs

- Published interface / composition / interface-completion corpora and related boundaries.
- Named interface artefacts (composition maps, handoff points, surface responsibilities).
- Published CTO-02 / CTO-05 expectations.

### Constitutional outputs

- Interface-lineage record under CT-05.
- Named interface-corpus bindings related.
- Audit-speakable interface-provenance note (composition related without meaning invention / authority transfer: true/false).

### Permitted relationships

- Relate composed interfaces to published contracts / evidence / recommendations / state they claim to consume.
- Relate interface-completion artefacts to published fulfilment rules.
- Detect UI or adapter layers that claim lineage while silently becoming educational or ownership authorities (refuse authority inference).
- Compose with CT-02 / CT-06 when implementation or API lineage is material.

### Prohibited relationships

- Require a particular design system or component library as constitutional via lineage.
- Treat visual polish or accessibility tooling scores as constitutional interface law (unless a published constitutional specification so states — none do by default).
- Invent interface completion meanings to force a link.
- Amend Programme VIII interface corpora via lineage records.
- Use CT-05 to author educational tips, state transitions, or conformity certificates.

---

## 8. CT-06 — API Traceability

### Constitutional purpose

Preserve lineage for **API exposure artefacts** under published constitutional contract, boundary, and explainability obligations that apply to callable educational / runtime acts — so APIs remain reconstructably related to law without inventing it.

### Constitutional scope

Lineage of callable surfaces to published constitutional obligations (authorisation of acts, evidence / contract honesty, refusal postures, explainability hooks as published). Does **not** require REST, OpenAPI, GraphQL, or any particular protocol as constitutional.

### Constitutional inputs

- Published constitutional obligations for callable acts (Programme VIII contracts / boundaries / explainability; Programme VI / VII boundaries as they constrain exposed acts).
- Named API artefacts (endpoint / operation inventories, request–response dispositions, error / refuse / escalate postures — protocol-neutral).
- Published CTO-01 / CTO-03 / CTO-06 expectations.

### Constitutional outputs

- API-lineage record under CT-06.
- Named constitutional obligations related to the callable surface.
- Audit-speakable API-provenance note (callable acts related as law-executing subjects, not law-making authorities: true/false).

### Permitted relationships

- Relate exposed acts to published authorising contracts / ownership / evidence rules.
- Relate refuse / defer / escalate dispositions to published postures when claimed.
- Support MS001 / CC-06 assessment by exposing the same named surfaces and corpus refs.
- Detect protocol theatre (schema “documented”) presented as constitutional lineage without corpus binding.

### Prohibited relationships

- Mandate REST, OpenAPI, gRPC, or a particular schema language as constitutional via lineage.
- Treat OpenAPI lint success, HTTP status fashion, or SDK generation as constitutional law.
- Rewrite published boundaries so a convenient endpoint “looks traced.”
- Expose Twin / Adaptive estimates as Educational Evidence via API lineage without published warrant.
- Use CT-06 to create new constitutional API law, educational meaning, or conformity claims.

---

## 9. CT-07 — Assessment Traceability

### Constitutional purpose

Preserve lineage for **conformance assessments and findings** under Programme IX / WS1 / MS001 — so specs → artefacts → criteria → findings remain reconstructably related, supporting auditability and repeatable re-evaluation without treating findings as law.

### Constitutional scope

Lineage among MS001 assessment records, published specifications under evaluation, named artefacts assessed, CC types applied, and finding dispositions. Does **not** mandate a particular log shipper, SIEM, CI vendor, or analytics product — and never elevates findings into constitutional amendments.

### Constitutional inputs

- Published MS001 corpora (Model, objectives, types, boundaries, explainability) and the constitutional specs / artefacts under assessment.
- Named assessment artefacts (assessment identities, finding dispositions, explainability records).
- Published CTO-03 / CTO-04 / CTO-05 expectations.

### Constitutional outputs

- Assessment-lineage record under CT-07.
- Confirmation that material assessments remain reconstructable against constitutional refs and CC identities.
- Audit-speakable assessment-provenance note (findings related without becoming law; linkage not substituted for evaluation: true/false).

### Permitted relationships

- Relate a finding to the published specifications and artefacts that grounded it.
- Relate CC-01…CC-07 bindings to the assessment record without inventing CC types.
- Preserve prior lawful assessment history under EIP-005 continuity.
- Compose with CT-01…CT-06 when multi-horizon lineage is material to the assessment.

### Prohibited relationships

- Require a particular CI vendor or metrics backend as constitutional via lineage.
- Treat pipeline greens, coverage dashboards, or “observability scores” as constitutional assessment law.
- Fabricate assessment trails after the fact to force a link.
- Erase non-conformant findings to present a green history.
- Use CT-07 to invent educational meaning, amend constitutional specifications, or declare conformity solely from linkage.

---

## 10. Catalogue Discipline

| Rule | Meaning |
|------|---------|
| **Closed set** | Only CT-01…CT-07 are constitutional traceability types |
| **Multi-bind allowed** | A single relationship may bind multiple CT types when published law requires |
| **No silent skip** | Required types for a scope may not be omitted for convenience |
| **Subjects ≠ types** | RC / EC / EV / CC / Programme VI–VII IDs may appear as *inputs*; they are not CT types |
| **Links ≠ amendments** | Lineage may motivate corpus proposals; it does not enact law |
| **Links ≠ conformity** | CT preserves relationships; CC evaluates fidelity |
| **Technology-neutral** | No CT type privileges a language, framework, protocol, or CI vendor |

---

## 11. Closing Statement

> **Only published traceability types may speak to constitutional lineage among specifications, artefacts, and findings.  
> Unpublished “implied traceability,” ticket graphs, and preferred stacks are not constitutional law — and never become it through linkage theatre.**
