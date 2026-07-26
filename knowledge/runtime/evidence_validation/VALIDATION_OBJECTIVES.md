# Validation Objectives

**Programme:** VIII — Workstream 2 — Constitutional Evidence Consumption  
**Milestone:** MS002 — Constitutional Evidence Validation Model  
**Classification:** Constitutional optimisation targets for constitutional evidence validation  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional evidence validation must optimise**.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md)
3. [`CONSTITUTIONAL_EVIDENCE_VALIDATION_MODEL.md`](CONSTITUTIONAL_EVIDENCE_VALIDATION_MODEL.md)
4. [`../evidence_consumption/CONSTITUTIONAL_EVIDENCE_CONSUMPTION_MODEL.md`](../evidence_consumption/CONSTITUTIONAL_EVIDENCE_CONSUMPTION_MODEL.md)
5. [`../evidence_consumption/EVIDENCE_OBJECTIVES.md`](../evidence_consumption/EVIDENCE_OBJECTIVES.md)
6. [`../contracts/RUNTIME_CONTRACT_MODEL.md`](../contracts/RUNTIME_CONTRACT_MODEL.md)
7. [`../contracts/CONTRACT_OBJECTIVES.md`](../contracts/CONTRACT_OBJECTIVES.md)
8. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
9. Programme VI constitutional models (educational meaning authorities)
10. Programme VII constitutional models (orchestration, authority, recommendation, state)
11. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
12. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)

Algorithms, validators, and operational proxies may introduce numerical or engineering metrics for these objectives. Proxies never redefine the constitutional meaning stated here — and never become educational quality scores.

> **Evidence validation objectives specialise confirmation of constitutional suitability for consumption.  
> They never authorise modifying evidence, reinventing provenance, creating substitute warrants, judging educational quality, or rewriting Programme VI / VII / EIP-002 / MS001.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “validators green” or “schemas happy.” The tutor optimises **faithful eligibility honesty**: only published warrants that remain intact, attributable, contractually authorised, and constitutionally eligible may support execution — without rewriting the warrant to make it pass.

These objectives bind every Runtime A evidence-validation behaviour and every successor runtime that claims constitutional compliance.

---

## 2. Primary Objective

### EVO-01 — Confirm constitutional eligibility for execution

**Definition.** Ensure that runtime determines — for each material published constitutional evidence instance (EC-01…EC-07) — whether that instance is constitutionally eligible for the contemplated consumption / execution under published EV-01…EV-07 checks and RC-01…RC-07 bindings — or honestly refuse / defer / escalate when eligibility cannot be confirmed.

**Includes:**

- Applying the closed EV catalogue required by published law for the contemplated act.
- Binding every material validation to RC-01…RC-07 as applicable (RC-02 when Educational Evidence of understanding is at stake).
- Preferring lawful refusal / deferral / escalation over “fixing” evidence so it becomes eligible.
- Preserving MS001 consumption posture: eligible evidence is still consumed exactly as published.
- Keeping eligibility distinct from educational quality, mastery, readiness, or constitutional truth.

**Excludes:**

- Treating green checksums, cache hits, Twin estimates, Adaptive scores, or UI ticks as educational quality judgements.
- Soft-upgrading claim classes, enriching payloads, or inventing provenance to force eligibility.
- Optimising for throughput, latency, or demo continuity as a substitute for constitutional fidelity.
- Declaring “close enough” eligibility without documenting a corpus amendment.

**Tutor rationale.** Professional exam preparation fails when software pretends a broken warrant is fine because the product needs a green path. Eligibility honesty is care; validation theatre is harm.

---

## 3. Supporting Objectives

### EVO-02 — Verify evidence integrity

**Definition.** Ensure that constitutional evidence meaning, classification, and claim honesty are confirmed intact as published — so validation never silently alters, truncates, enriches, or softens warrants in order to pass.

**Tutor rationale.** A tutor who quietly upgrades “attempted” into “mastered” during a “validation” step has abandoned educational care for product theatre.

**Manifestations:**

- Integrity checks confirm the warrant is unchanged; they do not rewrite it.
- Forbidden actions in `VALIDATION_BOUNDARIES.md` are hard stops.
- Claim ladder (coverage ≠ understanding ≠ mastery) survives validation untouched (EIP-006 / EIP-002).
- MS001 ECO-02 and ECB-04 integrity obligations remain binding during validation.

---

### EVO-03 — Verify provenance

**Definition.** Ensure that producer identity, claim class, succession history, continuity references, and authorising corpus paths are confirmed present, attributable, and non-forged — never invented, stripped, or replaced with operational metadata to obtain eligibility.

**Tutor rationale.** A coach who stamps a forged origin so today’s tip can proceed cannot be trusted. Provenance invention during validation is educational fraud.

**Manifestations:**

- Missing or forged provenance yields refuse / defer / escalate — not invented stamps.
- Continuity (EIP-005) forbids erasing prior lawful evidence history to simplify validation UX.
- Storage keys, cache hits, delivery acks, and validator process IDs are never substitutes for constitutional provenance.
- MS001 ECO-03 and ECB-05 provenance obligations remain binding during validation.

---

### EVO-04 — Verify constitutional eligibility contracts and catalogue fit

**Definition.** Ensure that validation confirms contractual compliance (RC bindings), constitutional catalogue fit (EC category published), and any required authority / state / runtime eligibility checks under EV-03…EV-06 — so consumption is never authorised by unpublished customs.

**Tutor rationale.** A coach who acts on an unauthorised scrap of paper because it “looked official” is not coaching under law.

**Manifestations:**

- Material validation without RC identity is unlawful.
- Material validation without EC identity is unlawful.
- Authority and state checks confirm published ownership / EST–CST suitability when those horizons apply — they do not invent ownership or state.
- Runtime eligibility confirms published execution preconditions — not educational readiness.

---

### EVO-05 — Preserve deterministic execution

**Definition.** Ensure that the same published evidence instance facts, the same published learner constitutional inputs, and the same published corpora yield the same eligibility outcome (eligible / ineligible / defer / escalate) — absent a published non-deterministic exception (none are granted by this Model for educational meaning or eligibility).

**Tutor rationale.** A coach who treats the same warrant as eligible or not depending on which replica woke first is not coaching; they are gambling.

**Manifestations:**

- Validation classification and outcomes are corpus-bound and reproducible.
- Infrastructure concurrency, sharding, and cache races must not change constitutional eligibility.
- Explicit multi-check EV sets use published conjunction / published stop rules, not random validator races.
- “Eventually consistent eligibility meaning” is a constitutional defect.

---

### EVO-06 — Preserve auditability

**Definition.** Ensure that every material evidence validation leaves a reconstructable constitutional trail: which evidence was validated, which EV category applied, which RC / corpus authorised validation, what eligibility outcome resulted, and which boundaries were preserved.

**Tutor rationale.** A tutor who cannot later say *which check* refused yesterday’s warrant cannot be trusted. Validation without audit is educational amnesia.

**Manifestations:**

- Audit records preserve constitutional references, not only technical validator logs.
- Continuity (EIP-005) is preserved across retries, replacements, and redeploys.
- Missing EV/EC/RC identity or missing eligibility outcome is a defect.
- RC-07 Audit Contract and EV-07 obligations apply to all material validations.

---

## 4. Objective Interactions

| If … | Then … |
|------|--------|
| EVO-01 conflicts with “helping” incomplete evidence pass | Constitutional eligibility honesty wins — refuse / defer / escalate |
| EVO-02 conflicts with convenience rewriting inside a validator | Integrity wins |
| EVO-03 conflicts with inventing missing producer refs | Provenance honesty wins — stop |
| EVO-04 conflicts with unpublished customs that feel convenient | Published RC/EC/EV catalogues win |
| EVO-05 conflicts with race-dependent validator outcomes | Determinism wins |
| EVO-06 conflicts with log volume reduction that erases constitutional refs | Auditability wins |

No supporting objective authorises violating EVO-01.

These objectives specialise — and never weaken — MS001 ECO-01…ECO-05, MS001 RCO integrity obligations, and RC-02 obligations for the evidence-validation horizon.

---

## 5. Non-Objectives

Constitutional evidence validation does **not** optimise for:

- educational quality scoring, mastery grading, or exam-readiness judgement;
- validator throughput, schema compile time, or checksum concurrency as educational success;
- inventing educational certainty when warrants are incomplete;
- collapsing EV categories into one mega-check that owns meaning;
- making a particular validator, schema, or store irreplaceable;
- using Twin / Adaptive / UI / analytics signals as substitutes for constitutional producers or eligibility;
- treating documentation as optional commentary on validator behaviour.

---

## 6. Closing Statement

> **A runtime that validates quickly by rewriting warrants is a failed educational system.  
> A runtime that confirms only published eligibility — with integrity, provenance, determinism, and audit intact — is doing its only evidence-validation job.**
