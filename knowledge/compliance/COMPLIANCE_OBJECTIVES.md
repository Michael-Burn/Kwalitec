# Compliance Objectives

**Programme:** IX — Workstream 3 — Constitutional Conformance Architecture  
**Milestone:** MS001 — Constitutional Compliance Model  
**Classification:** Constitutional optimisation targets for constitutional compliance  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional compliance determination must optimise**.

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`CONSTITUTIONAL_COMPLIANCE_MODEL.md`](CONSTITUTIONAL_COMPLIANCE_MODEL.md)
4. [`../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md)
5. [`../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md`](../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md)
6. [`../verification/CONSTITUTIONAL_VERIFICATION_MODEL.md`](../verification/CONSTITUTIONAL_VERIFICATION_MODEL.md)
7. [`../verification/VERIFICATION_OBJECTIVES.md`](../verification/VERIFICATION_OBJECTIVES.md)
8. Programme VI constitutional models (educational meaning authorities)
9. Programme VII constitutional models (orchestration, authority, recommendation, state)
10. Programme VIII constitutional models (runtime contracts, evidence, services, interfaces)
11. [`../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
12. [`../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Assessment tools, CI jobs, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here — and never become educational quality scores, conformity certificates, implementation certificates, or constitutional amendments.

> **Compliance objectives specialise determination of whether published constitutional obligations have been satisfied.  
> They never authorise creating constitutional law, modifying specifications, redefining constitutional meaning, replacing constitutional authority, or certifying implementations.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “seal green” or “dashboard complete.” The tutor optimises **honest obligation status**: only published constitutional obligations that can be judged from identifiable verification findings against published specifications — using established traceability, without rewriting those specifications or inventing findings — may support a compliance determination.

These objectives bind every constitutional compliance determination and every successor compliance machinery that claims constitutional compliance.

---

## 2. Primary Objective

### CCMO-01 — Determine constitutional obligation status

**Definition.** Ensure that every material compliance determination judges — for named published constitutional obligations, consuming identifiable verification findings, published constitutional specifications, and established traceability relationships — whether those obligations have been satisfied under recognised CCM-01…CCM-07 types, or honestly reports not-satisfied / deferred / escalated when satisfaction cannot be confirmed.

**Includes:**

- Applying the closed CCM catalogue required by published law for the determination scope.
- Binding every material determination to identifiable published Constitution / EIP / Programme VI / VII / VIII obligations and specifications.
- Consuming identifiable verification findings and established CT relationships (and identifiable conformance relationships where applicable) as inputs.
- Preferring lawful not-satisfied / deferred / escalated determinations over rewriting law or inventing findings so a report “passes.”
- Keeping obligation satisfaction distinct from educational quality, mastery, readiness, product success, conformity certificates, verification re-runs, or constitutional amendment.
- Preserving the Model’s posture: determinations judge obligation status; they do not become law or certificates.

**Excludes:**

- Treating green CI, coverage percentages, linter scores, Twin estimates, Adaptive scores, UI ticks, or seals as constitutional obligation satisfaction.
- Soft-amending specifications, inventing unpublished customs, inventing or rewriting verification findings, inventing lineage, or privileging “how main works” to force satisfaction.
- Optimising for throughput, latency, or demo continuity as a substitute for constitutional compliance.
- Declaring “close enough” satisfaction without documenting a corpus amendment.
- Issuing certificates that freeze an implementation as permanently compliant.

**Tutor rationale.** Professional exam preparation fails when software pretends unsatisfied educational obligations are fine because the product needs a green seal. Obligation honesty is care; compliance theatre is harm.

---

## 3. Supporting Objectives

### CCMO-02 — Preserve consistency

**Definition.** Ensure that the same published constitutional obligations, the same consumed verification findings, the same established traceability relationships, the same referenced specifications, and the same published CCM criteria yield the same compliance determination (satisfied / not-satisfied / deferred / escalated) — absent a published non-deterministic exception (none are granted by this Model for constitutional meaning or obligation status).

**Tutor rationale.** A coach who treats the same findings as satisfying or not depending on which reviewer woke first is not coaching; they are gambling.

**Manifestations:**

- Determination classification and outcomes are corpus-bound and reproducible.
- Parallel CI runners, sharding, and cache races must not change constitutional disposition.
- Explicit multi-type CCM sets use published conjunction / published stop rules, not random reviewer races.
- “Eventually consistent compliance meaning” is a constitutional defect.
- Invented or unstable findings / lineage inputs are hard stops, not soft variables.
- Contradictory determinations for equivalent published inputs without published justification are defects.

---

### CCMO-03 — Preserve implementation neutrality

**Definition.** Ensure that compliance judgements determine obligation status independently of programming language, framework, datastore, CI vendor, cloud topology, or preferred Runtime A shape — so no stack becomes constitutional by proximity to a compliance determination.

**Tutor rationale.** A coach who declares only one notebook brand “compliant” has abandoned educational law for vendor preference.

**Manifestations:**

- CCM criteria speak to constitutional obligations, not “must use Flask / SQLAlchemy / OpenAPI.”
- Equivalent lawful implementations under the same published law may both reach satisfied obligation status.
- Replacing a stack that previously satisfied obligations with another that still obeys published law does not itself create not-satisfaction — and does not create a certificate for either stack.
- “Our reference implementation does it this way” is never a substitute for a published specification.

---

### CCMO-04 — Preserve auditability

**Definition.** Ensure that every material compliance determination leaves a reconstructable trail: which obligations were evaluated, which verification findings were consumed, which constitutional specifications were referenced, which determination was reached, and which boundaries were preserved.

**Tutor rationale.** A tutor who cannot later say *why* an obligation was marked satisfied cannot be trusted. Silent seals destroy student and auditor trust.

**Manifestations:**

- Audit records preserve constitutional references, not only technical CI logs or badge images.
- Consumed finding identities, CT identities, and conformance relationship identities are recorded when material.
- Missing CCM identity, missing obligation / specification refs, missing finding identity, or missing determination disposition is a defect.
- Continuity (EIP-005) forbids erasing prior lawful compliance history to simplify the next report.

---

### CCMO-05 — Preserve explainability

**Definition.** Ensure that every material compliance determination can honestly answer the mandatory explainability questions in `COMPLIANCE_EXPLAINABILITY.md` — so students, developers, and auditors hear the same constitutional truth in appropriate vocabulary.

**Tutor rationale.** A coach who cannot say *which obligation* was judged from *which findings* under *which specifications* is performing, not determining.

**Manifestations:**

- Explainability obligations apply to all material determinations.
- Student / developer / auditor projections share one truth with different vocabulary.
- Obligation satisfaction is never narrated as mastery, readiness, educational quality, new law, permanent conformity, or a certificate.
- Stack preference and race-dependent outcomes are defects to disclose, not mysteries to hide.

---

### CCMO-06 — Consume verification and conformance without replacing them

**Definition.** Ensure that compliance strengthens obligation-status honesty by consuming WS2 verification findings and WS1 conformance relationships under established lineage — without rewriting CV or CC meaning, inventing satisfaction, re-running verification as a silent second engine, or issuing certificates that substitute for verification or conformance evaluation.

**Tutor rationale.** A tutor who stamps “verified = compliant forever = certified” has abandoned honesty and authority.

**Manifestations:**

- Compliance may consume CV findings and CC relationships as inputs; it may not amend them.
- Satisfied determinations speak to obligation status; they do not redefine when conformity may be claimed or when evidence satisfaction was verified.
- “Compliant” must never be narrated as “certified,” “permanently verified,” or “constitutionally permanent.”
- Missing established CT relationships or missing required findings remain hard stops even when a team wants a fast compliance story.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| CCMO-01 conflicts with “helping” incomplete findings look satisfying | Constitutional obligation honesty wins — not-satisfied / deferred / escalated |
| CCMO-02 conflicts with race-dependent reviewer outcomes | Consistency wins |
| CCMO-03 conflicts with privileging a reference stack as law | Implementation neutrality wins |
| CCMO-04 conflicts with log volume reduction that erases corpus refs | Auditability wins |
| CCMO-05 conflicts with opaque “trust us” seals | Explainability wins |
| CCMO-06 conflicts with treating compliance as a certificate of verification or conformity | Consume-without-replacement wins |

No supporting objective authorises violating CCMO-01.

These objectives specialise — and never weaken — Constitution / EIP integrity obligations, Programme VI–VIII authority preservation, WS1 conformance honesty, WS1 traceability provenance, and WS2 verification finding honesty for the compliance horizon.

---

## 5. Non-Objectives

Constitutional compliance does **not** optimise for:

- educational quality scoring, mastery grading, or exam-readiness judgement;
- CI throughput, flaky-test suppression, coverage theatre, or seal theatre as educational success;
- inventing constitutional certainty when specifications, findings, or lineage are incomplete;
- collapsing CCM types into one mega-check that owns meaning;
- making a particular language, framework, store, or CI vendor irreplaceable;
- using Twin / Adaptive / UI / analytics signals as substitutes for published constitutional obligations;
- certifying implementations, releases, or stacks as permanently lawful;
- treating documentation as optional commentary on whatever code already shipped;
- replacing MS001 conformance evaluation, MS002 lineage preservation, or WS2 verification evaluation.

---

## 6. Closing Statement

> **A determination that becomes “compliant” by rewriting constitutional law, inventing findings, or inventing lineage is a failed educational system.  
> A determination that judges only published obligations — with consistency, neutrality, auditability, and explainability intact, without certifying implementations — is doing its only compliance job.**
