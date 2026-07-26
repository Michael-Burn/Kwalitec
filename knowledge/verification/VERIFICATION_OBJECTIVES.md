# Verification Objectives

**Programme:** IX — Workstream 2 — Constitutional Conformance Architecture  
**Milestone:** MS001 — Constitutional Verification Model  
**Classification:** Constitutional optimisation targets for constitutional verification  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional verification must optimise**.

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`CONSTITUTIONAL_VERIFICATION_MODEL.md`](CONSTITUTIONAL_VERIFICATION_MODEL.md)
4. [`../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md) — especially CCO-01 (Verify constitutional adherence)
5. [`../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md`](../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md)
6. Programme VI constitutional models (educational meaning authorities)
7. Programme VII constitutional models (orchestration, authority, recommendation, state)
8. Programme VIII constitutional models (runtime contracts, evidence, services, interfaces)
9. [`../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
10. [`../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Assessment tools, CI jobs, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here — and never become educational quality scores, conformity certificates, or constitutional amendments.

> **Verification objectives specialise evaluation of whether implementation evidence satisfies published constitutional requirements.  
> They never authorise creating constitutional law, modifying specifications, redefining constitutional meaning, replacing constitutional authority, or certifying implementations.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “pipeline green” or “coverage high.” The tutor optimises **honest requirement satisfaction**: only implementation evidence that can be evaluated against published constitutional specifications — using established traceability, without rewriting those specifications to match the code — may support a verification finding.

These objectives bind every constitutional verification assessment and every successor verification machinery that claims constitutional verification.

---

## 2. Primary Objective

### CVO-01 — Verify constitutional requirements

**Definition.** Ensure that every material verification assessment determines — for named implementation evidence against named published constitutional specifications, consuming established traceability relationships — whether the evidence satisfies the published requirements under recognised CV-01…CV-07 types, or honestly reports not-satisfied / deferred / escalated when satisfaction cannot be confirmed.

**Includes:**

- Applying the closed CV catalogue required by published law for the assessment scope.
- Binding every material assessment to identifiable published Constitution / EIP / Programme VI / VII / VIII specifications.
- Consuming established CT relationships and identifiable conformance artefacts as inputs.
- Preferring lawful not-satisfied / deferred / escalated findings over rewriting law so evidence “passes.”
- Keeping satisfaction distinct from educational quality, mastery, readiness, product success, conformity certificates, or constitutional amendment.
- Preserving the Model’s posture: findings evaluate evidence against requirements; they do not become law or certificates.

**Excludes:**

- Treating green CI, coverage percentages, linter scores, Twin estimates, Adaptive scores, or UI ticks as constitutional requirement satisfaction.
- Soft-amending specifications, inventing unpublished customs, inventing lineage, or privileging “how main works” to force satisfaction.
- Optimising for throughput, latency, or demo continuity as a substitute for constitutional verification.
- Declaring “close enough” satisfaction without documenting a corpus amendment.
- Issuing certificates that freeze an implementation as permanently verified.

**Tutor rationale.** Professional exam preparation fails when software pretends non-satisfying educational behaviour is fine because the product needs a green path. Requirement honesty is care; verification theatre is harm.

---

## 3. Supporting Objectives

### CVO-02 — Support repeatable assessments

**Definition.** Ensure that the same published constitutional specifications, the same implementation evidence facts, the same established traceability relationships, and the same published CV criteria yield the same verification disposition (satisfied / not-satisfied / deferred / escalated) — absent a published non-deterministic exception (none are granted by this Model for constitutional meaning or requirement satisfaction).

**Tutor rationale.** A coach who treats the same evidence as satisfying or not depending on which reviewer woke first is not coaching; they are gambling.

**Manifestations:**

- Assessment classification and outcomes are corpus-bound and reproducible.
- Parallel CI runners, sharding, and cache races must not change constitutional disposition.
- Explicit multi-type CV sets use published conjunction / published stop rules, not random reviewer races.
- “Eventually consistent verification meaning” is a constitutional defect.
- Invented or unstable lineage inputs are hard stops, not soft variables.

---

### CVO-03 — Preserve implementation neutrality

**Definition.** Ensure that verification judgements evaluate evidence against published law independently of programming language, framework, datastore, CI vendor, cloud topology, or preferred Runtime A shape — so no stack becomes constitutional by proximity to a verification finding.

**Tutor rationale.** A coach who declares only one notebook brand “correct” has abandoned educational law for vendor preference.

**Manifestations:**

- CV criteria speak to constitutional obligations, not “must use Flask / SQLAlchemy / OpenAPI.”
- Equivalent lawful implementations under the same published law may both produce satisfying evidence.
- Replacing a stack that previously yielded satisfying evidence with another that still obeys published law does not itself create not-satisfaction — and does not create a certificate for either stack.
- “Our reference implementation does it this way” is never a substitute for a published specification.

---

### CVO-04 — Preserve auditability

**Definition.** Ensure that every material verification assessment leaves a reconstructable trail: which specifications were evaluated, which implementation evidence was assessed, which traceability relationships were consumed, which findings were produced, and which boundaries were preserved.

**Tutor rationale.** A tutor who cannot later say *why* evidence was accepted cannot be trusted. Silent green badges destroy student and auditor trust.

**Manifestations:**

- Audit records preserve constitutional references, not only technical CI logs.
- Consumed CT identities and conformance artefact identities are recorded when material.
- Missing CV identity, missing specification refs, missing evidence identity, or missing finding disposition is a defect.
- Continuity (EIP-005) forbids erasing prior lawful verification history to simplify the next report.

---

### CVO-05 — Preserve explainability

**Definition.** Ensure that every material verification assessment can honestly answer the mandatory explainability questions in `VERIFICATION_EXPLAINABILITY.md` — so students, developers, and auditors hear the same constitutional truth in appropriate vocabulary.

**Tutor rationale.** A coach who cannot say *which rule* was checked against *which evidence* under *which lineage* is performing, not verifying.

**Manifestations:**

- Explainability obligations apply to all material assessments.
- Student / developer / auditor projections share one truth with different vocabulary.
- Satisfaction is never narrated as mastery, readiness, educational quality, new law, or a certificate.
- Stack preference and race-dependent outcomes are defects to disclose, not mysteries to hide.

---

### CVO-06 — Support constitutional conformance without replacing it

**Definition.** Ensure that verification strengthens fidelity honesty for WS1 / MS001 conformance — by evaluating evidence against published requirements under established lineage — without rewriting CC meaning, inventing conformity, or issuing certificates that substitute for conformance evaluation.

**Tutor rationale.** A tutor who stamps “verified = conformant forever” has abandoned both honesty and authority.

**Manifestations:**

- Verification may consume CC artefacts as inputs; it may not amend them.
- Satisfied findings support fidelity speech; they do not redefine when conformity may be claimed.
- “Verified” must never be narrated as “certified conformant” or “constitutionally permanent.”
- Missing established CT relationships remain hard stops even when a team wants a fast conformance story.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| CVO-01 conflicts with “helping” incomplete evidence look satisfying | Constitutional requirement honesty wins — not-satisfied / deferred / escalated |
| CVO-02 conflicts with race-dependent reviewer outcomes | Repeatability wins |
| CVO-03 conflicts with privileging a reference stack as law | Implementation neutrality wins |
| CVO-04 conflicts with log volume reduction that erases corpus refs | Auditability wins |
| CVO-05 conflicts with opaque “trust us” badges | Explainability wins |
| CVO-06 conflicts with treating verification as a certificate of conformity | Support-without-replacement wins |

No supporting objective authorises violating CVO-01.

These objectives specialise — and never weaken — Constitution / EIP integrity obligations, Programme VI–VIII authority preservation, WS1 conformance honesty, and WS1 traceability provenance for the verification horizon.

---

## 5. Non-Objectives

Constitutional verification does **not** optimise for:

- educational quality scoring, mastery grading, or exam-readiness judgement;
- CI throughput, flaky-test suppression, or coverage theatre as educational success;
- inventing constitutional certainty when specifications or lineage are incomplete;
- collapsing CV types into one mega-check that owns meaning;
- making a particular language, framework, store, or CI vendor irreplaceable;
- using Twin / Adaptive / UI / analytics signals as substitutes for published constitutional specifications;
- certifying implementations, releases, or stacks as permanently lawful;
- treating documentation as optional commentary on whatever code already shipped;
- replacing MS001 conformance evaluation or MS002 lineage preservation.

---

## 6. Closing Statement

> **An assessment that becomes “verified” by rewriting constitutional law or inventing lineage is a failed educational system.  
> An assessment that verifies only published requirements — with repeatability, neutrality, auditability, and explainability intact, without certifying implementations — is doing its only verification job.**
