# Traceability Objectives

**Programme:** IX — Workstream 1 — Constitutional Conformance Architecture  
**Milestone:** MS002 — Constitutional Traceability Model  
**Classification:** Constitutional optimisation targets for constitutional traceability  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional traceability must optimise**.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`CONSTITUTIONAL_TRACEABILITY_MODEL.md`](CONSTITUTIONAL_TRACEABILITY_MODEL.md)
4. [`../CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../CONSTITUTIONAL_CONFORMANCE_MODEL.md) — especially CCO-02 (Preserve traceability)
5. Programme VI constitutional models (educational meaning authorities)
6. Programme VII constitutional models (orchestration, authority, recommendation, state)
7. Programme VIII constitutional models (runtime contracts, evidence, services, interfaces)
8. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
9. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Linkage tools, CI jobs, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here — and never become educational quality scores, conformity certificates, or constitutional amendments.

> **Traceability objectives specialise preservation of lawful relationships among published constitutional specifications, implementation artefacts, and conformance findings.  
> They never authorise creating constitutional law, modifying specifications, reinterpreting constitutional meaning, inferring constitutional authority, or replacing conformance evaluation.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “tickets linked” or “deps mapped.” The tutor optimises **honest provenance**: only relationships that cite published constitutional specifications — without rewriting those specifications to match the code — may be called constitutionally traced.

These objectives bind every constitutional traceability relationship and every successor linkage machinery that claims constitutional lineage.

---

## 2. Primary Objective

### CTO-01 — Preserve constitutional provenance

**Definition.** Ensure that every material traceability relationship anchors to identifiable published Constitution / EIP / Programme VI / VII / VIII specifications (and, where CT-07 applies, identifiable MS001 assessment identities) — so the constitutional origin of the relationship is reconstructable and never invented.

**Includes:**

- Binding every material relationship to published corpus paths and specification identities.
- Preferring lawful refuse / defer / escalate over inventing unpublished anchors so linkage “completes.”
- Keeping provenance distinct from educational quality, mastery, readiness, product success, conformity, or constitutional amendment.
- Preserving the Model’s posture: relationships record lineage; they do not become law.

**Excludes:**

- Treating ticket IDs, commit SHAs, dependency graphs, coverage maps, Twin estimates, Adaptive scores, or UI ticks as constitutional provenance.
- Soft-amending specifications, inventing unpublished customs, or privileging “how main works” to force a link.
- Optimising for throughput, latency, or demo continuity as a substitute for constitutional provenance.
- Declaring “close enough” provenance without documenting a corpus amendment.

**Tutor rationale.** Professional exam preparation fails when software pretends tribal memory is syllabus law because a ticket was closed. Provenance honesty is care; lineage theatre is harm.

---

## 3. Supporting Objectives

### CTO-02 — Preserve lineage

**Definition.** Ensure that every material relationship can be reconstructed as published constitutional specification → applied CT type → named implementation artefact and/or conformance finding — so the chain of relation is walkable without invented hops.

**Tutor rationale.** A coach who cannot say *which rule* yesterday’s notes cited cannot be trusted. Traceability without lineage is educational amnesia.

**Manifestations:**

- Relationships cite corpus paths and specification identities, not only tickets or SHAs.
- Related subjects are named (module, interface, behaviour class, API surface, audit trail, assessment record) without treating names as law.
- Continuity (EIP-005) forbids erasing prior lawful lineage to simplify the next report.
- Missing specification identity or missing subject identity is a defect.

---

### CTO-03 — Support implementation assessment

**Definition.** Ensure that preserved relationships enable Programme IX / WS1 / MS001 conformance assessment to re-locate the same published specifications and named artefacts — so fidelity evaluation remains possible without rewriting law or inventing subjects.

**Tutor rationale.** A tutor who cannot find which syllabus clause a plan claimed to obey cannot assess honesty. Lineage that cannot support assessment is decoration.

**Manifestations:**

- CT relationships expose the same constitutional refs MS001 needs for CC evaluation.
- Artefact identities remain stable enough for repeatable assessment under published inputs.
- Lineage never claims “linked therefore conformant”; it supplies the map assessment walks.
- Incomplete maps for a required assessment scope are defects, not soft-passes.

---

### CTO-04 — Support auditability

**Definition.** Ensure that every material traceability relationship leaves a reconstructable trail: which specifications were referenced, which artefacts or findings were related, which CT category applied, which provenance was preserved, and which boundaries remained intact.

**Tutor rationale.** A tutor who cannot later say *why* a note cited a rule cannot be trusted. Silent link badges destroy student and auditor trust.

**Manifestations:**

- Audit records preserve constitutional references, not only technical link graphs.
- Explainability obligations in `TRACEABILITY_EXPLAINABILITY.md` apply to all material relationships.
- Missing CT identity, missing specification refs, or missing subject identity is a defect.
- Student / developer / auditor projections share one truth with different vocabulary.

---

### CTO-05 — Support explainability

**Definition.** Ensure that every material relationship can answer the mandatory explainability questions — which specification, which artefact, which category, which provenance, which boundaries — without redefining constitutional meaning.

**Tutor rationale.** A coach who can only say “it’s documented somewhere” is performing, not teaching. Speakable lineage is care.

**Manifestations:**

- CTEQ-01…CTEQ-05 answers are producible for every material relationship.
- Explanations never soft-amend law or narrate linkage as authority or conformity.
- Audience projections differ in vocabulary, not in constitutional facts.
- Opaque “trust the graph” badges are defects.

---

### CTO-06 — Preserve implementation neutrality

**Definition.** Ensure that traceability relationships speak to constitutional identities independently of programming language, framework, datastore, CI vendor, cloud topology, or preferred Runtime A shape — so no stack becomes constitutional by proximity to a link.

**Tutor rationale.** A coach who declares only one notebook brand “correctly documented” has abandoned educational law for vendor preference.

**Manifestations:**

- CT criteria speak to constitutional identities and obligations, not “must use Flask / SQLAlchemy / OpenAPI.”
- Equivalent lawful implementations under the same published law may both carry lawful lineage.
- Replacing a linked stack with another that still obeys published law does not itself create unlawful lineage.
- “Our reference implementation links this way” is never a substitute for a published specification.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| CTO-01 conflicts with inventing an unpublished anchor so linkage completes | Constitutional provenance wins — refuse / defer / escalate |
| CTO-02 conflicts with log volume reduction that erases corpus refs | Lineage wins |
| CTO-03 conflicts with “linked therefore skip assessment” | Assessment support honesty wins — CT never replaces CC |
| CTO-04 conflicts with opaque link badges | Auditability wins |
| CTO-05 conflicts with unspeakable “trust us” graphs | Explainability wins |
| CTO-06 conflicts with privileging a reference stack as law | Implementation neutrality wins |

No supporting objective authorises violating CTO-01.

These objectives specialise — and never weaken — Constitution / EIP integrity obligations, Programme VI–VIII authority preservation, and MS001 CCO-02 for the traceability horizon.

---

## 5. Non-Objectives

Constitutional traceability does **not** optimise for:

- educational quality scoring, mastery grading, or exam-readiness judgement;
- CI throughput, flaky-link suppression, or coverage theatre as educational success;
- inventing constitutional certainty when specifications are incomplete;
- collapsing CT types into one mega-link that owns meaning;
- making a particular language, framework, store, or CI vendor irreplaceable;
- using Twin / Adaptive / UI / analytics signals as substitutes for published constitutional specifications;
- treating documentation links as optional commentary on whatever code already shipped;
- declaring conformity solely because a relationship exists.

---

## 6. Closing Statement

> **A relationship that becomes “traced” by rewriting constitutional law is a failed educational system.  
> A relationship that preserves only published provenance — with lineage, assessment support, auditability, explainability, and neutrality intact — is doing its only traceability job.**
