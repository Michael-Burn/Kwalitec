# Conformance Objectives

**Programme:** IX — Workstream 1 — Constitutional Conformance Architecture  
**Milestone:** MS001 — Constitutional Conformance Model  
**Classification:** Constitutional optimisation targets for constitutional conformance  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional conformance assessment must optimise**.

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`CONSTITUTIONAL_CONFORMANCE_MODEL.md`](CONSTITUTIONAL_CONFORMANCE_MODEL.md)
4. Programme VI constitutional models (educational meaning authorities)
5. Programme VII constitutional models (orchestration, authority, recommendation, state)
6. Programme VIII constitutional models (runtime contracts, evidence, services, interfaces)
7. [`../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
8. [`../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Assessment tools, CI jobs, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here — and never become educational quality scores or constitutional amendments.

> **Conformance objectives specialise verification of implementation fidelity to published constitutional law.  
> They never authorise creating constitutional law, modifying specifications, reinterpreting educational meaning, or freezing a stack as authority.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “pipeline green” or “coverage high.” The tutor optimises **faithful adherence honesty**: only implementations that can be traced to published constitutional specifications — without rewriting those specifications to match the code — may be called constitutionally conformant.

These objectives bind every constitutional conformance assessment and every successor assessment machinery that claims constitutional compliance.

---

## 2. Primary Objective

### CCO-01 — Verify constitutional adherence

**Definition.** Ensure that every material conformance assessment determines — for named implementation artefacts against named published constitutional specifications — whether the implementation adheres under recognised CC-01…CC-07 types, or honestly reports non-conformant / deferred / escalated when adherence cannot be confirmed.

**Includes:**

- Applying the closed CC catalogue required by published law for the assessment scope.
- Binding every material assessment to identifiable published Constitution / EIP / Programme VI / VII / VIII specifications.
- Preferring lawful non-conformant / deferred / escalated findings over rewriting law so code “passes.”
- Keeping adherence distinct from educational quality, mastery, readiness, product success, or constitutional amendment.
- Preserving the Model’s posture: findings evaluate fidelity; they do not become law.

**Excludes:**

- Treating green CI, coverage percentages, linter scores, Twin estimates, Adaptive scores, or UI ticks as constitutional adherence.
- Soft-amending specifications, inventing unpublished customs, or privileging “how main works” to force conformity.
- Optimising for throughput, latency, or demo continuity as a substitute for constitutional fidelity.
- Declaring “close enough” adherence without documenting a corpus amendment.

**Tutor rationale.** Professional exam preparation fails when software pretends non-conformant educational behaviour is fine because the product needs a green path. Adherence honesty is care; conformance theatre is harm.

---

## 3. Supporting Objectives

### CCO-02 — Preserve traceability

**Definition.** Ensure that every material conformance finding can be traced from published constitutional specification → applied CC type → named implementation artefact → criterion → disposition — so origin of the judgement is reconstructable.

**Tutor rationale.** A coach who cannot say *which rule* yesterday’s plan obeyed cannot be trusted. Conformance without traceability is educational amnesia.

**Manifestations:**

- Findings cite corpus paths and specification identities, not only ticket IDs or commit SHAs.
- Artefacts under assessment are named (module, interface, behaviour class, API surface, audit trail) without treating names as law.
- Continuity (EIP-005) forbids erasing prior lawful assessment history to simplify the next report.
- Missing specification identity or missing artefact identity is a defect.

---

### CCO-03 — Preserve implementation neutrality

**Definition.** Ensure that conformance judgements evaluate fidelity to published law independently of programming language, framework, datastore, CI vendor, cloud topology, or preferred Runtime A shape — so no stack becomes constitutional by proximity.

**Tutor rationale.** A coach who declares only one notebook brand “correct” has abandoned educational law for vendor preference.

**Manifestations:**

- CC criteria speak to constitutional obligations, not “must use Flask / SQLAlchemy / OpenAPI.”
- Equivalent lawful implementations under the same published law may both be conformant.
- Replacing a conformant stack with another that still obeys published law does not itself create non-conformance.
- “Our reference implementation does it this way” is never a substitute for a published specification.

---

### CCO-04 — Preserve constitutional integrity

**Definition.** Ensure that assessments never create, modify, soft-amend, or reinterpret constitutional specifications — and never treat conformance findings as constitutional amendments, educational meaning, or runtime behaviour licences.

**Tutor rationale.** A tutor who quietly rewrites the syllabus so last week’s notes look correct has abandoned integrity for convenience.

**Manifestations:**

- Forbidden actions in `CONFORMANCE_BOUNDARIES.md` are hard stops.
- Claim ladder and Programme VI meanings survive assessment untouched.
- Findings may recommend a *corpus amendment proposal*; they may not enact one.
- Implementation convenience never rewrites authority, tip, state, or contract law.

---

### CCO-05 — Preserve repeatability

**Definition.** Ensure that the same published constitutional specifications, the same implementation artefact facts, and the same published CC criteria yield the same conformance disposition (conformant / non-conformant / deferred / escalated) — absent a published non-deterministic exception (none are granted by this Model for constitutional meaning or adherence).

**Tutor rationale.** A coach who treats the same plan as lawful or not depending on which reviewer woke first is not coaching; they are gambling.

**Manifestations:**

- Assessment classification and outcomes are corpus-bound and reproducible.
- Parallel CI runners, sharding, and cache races must not change constitutional disposition.
- Explicit multi-type CC sets use published conjunction / published stop rules, not random reviewer races.
- “Eventually consistent conformance meaning” is a constitutional defect.

---

### CCO-06 — Preserve auditability and explainability

**Definition.** Ensure that every material conformance assessment leaves a reconstructable, speakable trail: which specifications were evaluated, which artefacts were assessed, which criteria applied, which findings were produced, and which boundaries were preserved.

**Tutor rationale.** A tutor who cannot later say *why* a plan was accepted cannot be trusted. Silent green badges destroy student and auditor trust.

**Manifestations:**

- Audit records preserve constitutional references, not only technical CI logs.
- Explainability obligations in `CONFORMANCE_EXPLAINABILITY.md` apply to all material assessments.
- Missing CC identity, missing specification refs, or missing finding disposition is a defect.
- Student / developer / auditor projections share one truth with different vocabulary.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| CCO-01 conflicts with “helping” incomplete code look conformant | Constitutional adherence honesty wins — non-conformant / deferred / escalated |
| CCO-02 conflicts with log volume reduction that erases corpus refs | Traceability wins |
| CCO-03 conflicts with privileging a reference stack as law | Implementation neutrality wins |
| CCO-04 conflicts with soft-amending specs so CI passes | Constitutional integrity wins |
| CCO-05 conflicts with race-dependent reviewer outcomes | Repeatability wins |
| CCO-06 conflicts with opaque “trust us” badges | Auditability and explainability win |

No supporting objective authorises violating CCO-01.

These objectives specialise — and never weaken — Constitution / EIP integrity obligations and Programme VI–VIII authority preservation for the conformance horizon.

---

## 5. Non-Objectives

Constitutional conformance does **not** optimise for:

- educational quality scoring, mastery grading, or exam-readiness judgement;
- CI throughput, flaky-test suppression, or coverage theatre as educational success;
- inventing constitutional certainty when specifications are incomplete;
- collapsing CC types into one mega-check that owns meaning;
- making a particular language, framework, store, or CI vendor irreplaceable;
- using Twin / Adaptive / UI / analytics signals as substitutes for published constitutional specifications;
- treating documentation as optional commentary on whatever code already shipped.

---

## 6. Closing Statement

> **An assessment that becomes “conformant” by rewriting constitutional law is a failed educational system.  
> An assessment that verifies only published adherence — with traceability, neutrality, integrity, repeatability, and explainability intact — is doing its only conformance job.**
