# Completion Objectives

**Programme:** IX — Workstream 2 — Constitutional Conformance Architecture  
**Milestone:** MS003 — Constitutional Verification Completion Model  
**Classification:** Constitutional optimisation targets for constitutional verification completion  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional verification completion must optimise**.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`CONSTITUTIONAL_VERIFICATION_COMPLETION_MODEL.md`](CONSTITUTIONAL_VERIFICATION_COMPLETION_MODEL.md)
4. [`../CONSTITUTIONAL_VERIFICATION_MODEL.md`](../CONSTITUTIONAL_VERIFICATION_MODEL.md)
5. [`../VERIFICATION_OBJECTIVES.md`](../VERIFICATION_OBJECTIVES.md) — WS2 / MS001 CVO-xx; this corpus specialises *completion* of those verification duties
6. [`../lifecycle/CONSTITUTIONAL_VERIFICATION_LIFECYCLE_MODEL.md`](../lifecycle/CONSTITUTIONAL_VERIFICATION_LIFECYCLE_MODEL.md)
7. [`../lifecycle/LIFECYCLE_OBJECTIVES.md`](../lifecycle/LIFECYCLE_OBJECTIVES.md) — WS2 / MS002 CVLO-xx; this corpus specialises *completion* of those lifecycle duties
8. [`../../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md)
9. Programme VI constitutional models (educational meaning authorities)
10. Programme VII constitutional models (orchestration, authority, recommendation, state)
11. Programme VIII constitutional models (runtime contracts, evidence, services, interfaces)
12. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
13. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Linkage tools, CI jobs, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here — and never become compliance certificates, certification scores, educational quality scores, or constitutional amendments.

> **Verification completion objectives specialise lawful confirmation that the required verification lifecycle has been executed and findings lawfully produced.  
> They never authorise implying constitutional compliance, certifying implementations, approving implementations, inventing educational success, reinterpreting constitutional meaning, or rewriting constitutional specifications.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “pipeline greens,” “tickets closed,” or “coverage high enough.” The tutor optimises **honest closing of constitutional verification work**: when the published lifecycle for a concern has been fully executed and findings lawfully produced and recorded, the tutor can say so — without pretending the implementation is compliant, without pretending a release is certified, without pretending the student has mastered the topic, and without rewriting the syllabus because the machinery stopped cleanly.

These objectives bind every constitutional verification completion judgement and every successor verification machinery that claims constitutional verification fulfilment.

---

## 2. Primary Objective

### CVCO-01 — Confirm lifecycle completion

**Definition.** Ensure that runtime / assessment / audit speech affirms verification completion only when a published verification concern under WS2 / MS001–MS002 has executed the required CVL-01…CVL-07 lifecycle obligations — or honestly refuses close when fulfilment criteria are not met.

**Includes:**

- Assessing only concerns that lawfully opened under WS2 / MS001–MS002 identify → prepare → validate → evaluate → produce → record → close law.
- Affirming completion only when `COMPLETION_CRITERIA.md` conditions (CVC-01…CVC-05) hold.
- Preferring lawful “not yet” / refuse-close over inventing a “done enough” status for product convenience.
- Distinguishing lawful stop dispositions (refuse / defer / escalate as published outcomes that exhaust remaining *verification* duties with honest recording) from abandoned lifecycle duties.
- Binding every material completion judgement to reconstructable constitutional references.

**Excludes:**

- Declaring complete because a CI job exited, a ticket closed, a coverage map looked full, or a UI spinner stopped.
- Treating Twin / Adaptive / Experience / Mission heuristics as completion warrants.
- Optimising for throughput, latency, or demo continuity as a substitute for lifecycle honesty.
- Collapsing “verification complete” into “compliant,” “certified,” “approved,” “student succeeded,” or “constitution updated.”

**Tutor rationale.** Professional exam preparation fails when software celebrates unfinished verification work — or celebrates finished pipeline machinery as finished fidelity, certification, or learning. Honest confirmation is care; completion theatre is harm.

---

## 3. Supporting Objectives

### CVCO-02 — Confirm findings are recorded

**Definition.** Ensure that affirming verification completion never occurs without lawful production and recording of verification findings under published CV criteria — including satisfied, not-satisfied, deferred, and escalated dispositions — without upgrading those dispositions into compliance, certification, or approval.

**Tutor rationale.** A coach who declares marking “finished” without recording what was found has not finished care — and a coach who upgrades “not satisfied” into “approved” by closing the folder has abandoned honesty.

**Manifestations:**

- Completion leaves findings identities and dispositions reconstructable.
- Close never substitutes pipeline exit codes or ticket states for published finding dispositions.
- Continuity (EIP-005) forbids erasing prior lawful findings to simplify the next report.
- Missing required findings after an affirmed close is a defect.

---

### CVCO-03 — Preserve audit continuity

**Definition.** Ensure that every material completion judgement leaves a reconstructable trail: which specifications were evaluated, which evidence was assessed, which lifecycle stages were completed, which findings were produced, and which boundaries remained intact.

**Tutor rationale.** A tutor who cannot later say *why* verification was declared finished cannot be trusted. Silent “complete” badges destroy student and auditor trust.

**Manifestations:**

- Audit records preserve constitutional references, not only technical job logs or CI annotations.
- Explainability obligations in `COMPLETION_EXPLAINABILITY.md` apply to all material completion judgements.
- Missing CVC identity against criteria, missing specification refs, missing evidence identity, or missing stage identity is a defect.
- Student / developer / auditor projections share one truth with different vocabulary.

---

### CVCO-04 — Preserve explainability

**Definition.** Ensure that every material completion judgement can answer the mandatory explainability questions — which specifications, which evidence, which stages, which findings, which boundaries — without redefining constitutional meaning or implying compliance / certification / approval / educational success.

**Tutor rationale.** A coach who can only say “it’s fully verified somewhere” is performing, not teaching. Speakable completion is care.

**Manifestations:**

- CVCQ-01…CVCQ-05 answers are producible for every material affirmed or refused close.
- Explanations never soft-amend law or narrate completion as authority, compliance, certification, or approval.
- Audience projections differ in vocabulary, not in constitutional facts.
- Opaque “trust the complete badge” theatre is a defect.

---

### CVCO-05 — Preserve repeatability

**Definition.** Ensure that affirming completion preserves the constitutional repeatability obligation: same published requirements, same evidence facts, same consumed relationships, same stage sequence ⇒ same completion disposition for the same concern scope — so close cannot invent contradictory “done” and “not done” stories from identical published inputs.

**Tutor rationale.** A marking session that finishes differently for the same script under the same rules is not care; it is lottery dressed as law.

**Manifestations:**

- Completion judgements remain reproducible from published constitutional inputs.
- Hidden stack-specific shortcuts that flip completion for one vendor only are defects.
- Continuity forbids deleting prior lawful stage / finding records to force a different close next time.
- Non-deterministic “best effort complete” theatre is a defect.

---

### CVCO-06 — Preserve implementation neutrality

**Definition.** Ensure that completion judgements speak to constitutional lifecycle fulfilment independently of programming language, framework, datastore, CI vendor, cloud topology, or preferred Runtime A shape — so no stack becomes constitutional by proximity to a “complete” flag.

**Tutor rationale.** A coach who declares only one notebook brand “fully verified” has abandoned educational law for vendor preference.

**Manifestations:**

- CVC criteria speak to constitutional identities and obligations, not “must use Flask / SQLAlchemy / OpenAPI.”
- Equivalent lawful implementations under the same published law may both reach lawful completion.
- Replacing a verified stack with another that still obeys published law does not itself create unlawful completion.
- “Our reference implementation completes this way” is never a substitute for published criteria.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| CVCO-01 conflicts with inventing unpublished stages so close can complete | Lifecycle honesty wins — refuse / defer / escalate |
| CVCO-02 conflicts with mute close that skips findings | Findings recording wins |
| CVCO-03 conflicts with opaque complete badges | Audit continuity wins |
| CVCO-04 conflicts with unspeakable “trust us” completion | Explainability wins |
| CVCO-05 conflicts with stack-specific non-reproducible close | Repeatability wins |
| CVCO-06 conflicts with privileging a reference stack as completion law | Implementation neutrality wins |
| Any CVCO conflicts with implying compliance / certification / approval / educational success / law change | Non-implication honesty wins — refuse the overclaim |

No supporting objective authorises violating CVCO-01.

These objectives specialise — and never weaken — Constitution / EIP integrity obligations, Programme VI–VIII authority preservation, WS2 / MS001 CVO duties, and WS2 / MS002 CVLO duties for the *completion* horizon.

---

## 5. Non-Objectives

Constitutional verification completion does **not** optimise for:

- constitutional compliance disposition, fidelity scoring, or “verified therefore compliant” theatre;
- certification of releases, stacks, vendors, or implementations;
- approval of implementations, product milestones, or delivery gates as constitutional law;
- educational quality scoring, mastery grading, or exam-readiness judgement;
- CI throughput, flaky-test suppression, or demo continuity as educational or constitutional success;
- inventing constitutional certainty when required lifecycle stages or findings remain incomplete;
- collapsing CVC criteria into one mega-flag that owns meaning;
- making a particular language, framework, store, or CI vendor irreplaceable;
- using Twin / Adaptive / UI / analytics signals as substitutes for published completion criteria;
- treating documentation of a pipeline as optional commentary on whatever code already shipped;
- declaring compliance, certification, approval, educational success, or constitutional amendment solely because completion was affirmed.

---

## 6. Closing Statement

> **A concern that becomes “verification complete” by rewriting constitutional law — or by implying compliance, certification, approval, or educational success — is a failed educational system.  
> A concern that confirms only that the required published lifecycle ran and findings were lawfully produced — with audit continuity, explainability, repeatability, and neutrality intact — is doing its only completion job.**
