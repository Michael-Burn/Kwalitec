# Lifecycle Stages

**Programme:** IX — Workstream 2 — Constitutional Conformance Architecture  
**Milestone:** MS002 — Constitutional Verification Lifecycle Model  
**Classification:** Closed catalogue of recognised constitutional verification lifecycle stages  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional verification lifecycle stages** (CVL-01…CVL-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_VERIFICATION_LIFECYCLE_MODEL.md`](CONSTITUTIONAL_VERIFICATION_LIFECYCLE_MODEL.md)
3. [`LIFECYCLE_OBJECTIVES.md`](LIFECYCLE_OBJECTIVES.md)
4. [`../CONSTITUTIONAL_VERIFICATION_MODEL.md`](../CONSTITUTIONAL_VERIFICATION_MODEL.md)
5. [`../VERIFICATION_TYPES.md`](../VERIFICATION_TYPES.md) — CV-01…CV-07 applied during CVL-04
6. [`../VERIFICATION_BOUNDARIES.md`](../VERIFICATION_BOUNDARIES.md)
7. [`../../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md`](../../conformance/CONSTITUTIONAL_CONFORMANCE_MODEL.md)
8. [`../../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md`](../../conformance/traceability/CONSTITUTIONAL_TRACEABILITY_MODEL.md)
9. [`../../conformance/traceability/TRACEABILITY_TYPES.md`](../../conformance/traceability/TRACEABILITY_TYPES.md)
10. Programme VI corpora under [`../../educational/`](../../educational/)
11. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
12. Programme VIII corpora under [`../../runtime/`](../../runtime/)
13. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published lifecycle stages may organise constitutional verification from initiation through findings.  
> Unpublished “implied stages” are constitutionally defective.**

**Catalogue disambiguation:** CVL-01…CVL-07 here are *constitutional verification lifecycle stages*. They are not verification types (CV-01…CV-07), conformance types (CC-01…CC-07), traceability types (CT-01…CT-07), Educational Validation Framework coach capability IDs, Programme VIII runtime contracts (RC-xx), evidence categories (EC-xx), or evidence validation categories (EV-xx).

---

## 1. Purpose

Verification without a closed stage catalogue invents law by proximity: whichever pipeline step, ticket status, or reviewer habit happens to finish becomes the tutor’s “proof the system ran a constitutional verification.”

This catalogue names the only lawful constitutional verification lifecycle stages — and binds each stage to purpose, inputs, outputs, and permitted / prohibited activities.

---

## 2. Stage Principles

1. **Ordered and skip-disciplined.** Stages may be brief under thin scope; mandatory initiation, evidence identity, lineage validation, evaluation, findings, recording, and closure obligations may not be silently omitted when a verification finding is claimed.
2. **Consumption before evaluation.** Published specs, named evidence, and established CT relationships are identified before CV assessment.
3. **Explainability accumulates.** Each stage leaves traceable artefacts for `LIFECYCLE_EXPLAINABILITY.md`.
4. **Refusal is a stage outcome.** Not-satisfied, deferred, escalated, and refuse-progress are first-class conclusions.
5. **Deterministic transitions.** Same published inputs ⇒ same next stage outcomes.
6. **Stages coordinate; they do not legislate.** No stage creates, modifies, or redefines constitutional law.
7. **Stages do not certify.** Closure never freezes an implementation as permanently lawful.

---

## 3. Catalogue Overview

| ID | Stage | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|-------|--------------------------------|----------------|-----------------|
| **CVL-01** | Verification Initiation | Open a verification concern against named published specifications and scope | Published corpus identities + concern scope + optional CC artefacts | Initiated concern record (or refuse-open) |
| **CVL-02** | Evidence Preparation | Identify and prepare named implementation evidence for evaluation | Initiated concern + candidate evidence identities | Prepared evidence bundle (or refuse-prepare) |
| **CVL-03** | Traceability Validation | Confirm established CT relationships required for the concern | Prepared evidence + required CT identities | Validated lineage set (or refuse-validate) |
| **CVL-04** | Constitutional Evaluation | Apply CV-01…CV-07 against prepared evidence under published requirements | Validated lineage + published CV criteria + evidence | Evaluation dispositions under CV types |
| **CVL-05** | Findings Production | Emit verification findings under published criteria | Evaluation dispositions | Verification findings (satisfied / not-satisfied / deferred / escalated) |
| **CVL-06** | Findings Recording | Preserve audit-speakable trails of the lifecycle | Findings + stage traces | Audit records bound to specs / evidence / relationships / stages |
| **CVL-07** | Verification Closure | Close the lifecycle honestly when duties are exhausted | Recorded findings + boundary confirmations | Closed lifecycle (or refuse-close) — never a certificate |

Material verification claiming constitutional findings must map to this sequence as published law requires. Stages may be brief; none may invent a stage outside this catalogue.

**Relation to CV / CC / CT / EV:** Those catalogues remain defined solely by their owners. CVL stages *organise when* verification activities occur; they do not replace, reclassify, certify, or invent those catalogues.

---

## 4. Canonical Stage Sequence

```text
CVL-01  Verification Initiation
           ↓
CVL-02  Evidence Preparation
           ↓
CVL-03  Traceability Validation
           ↓
CVL-04  Constitutional Evaluation
           ↓
CVL-05  Findings Production
           ↓
CVL-06  Findings Recording
           ↓
CVL-07  Verification Closure
```

Lawful early stop dispositions (refuse-open / refuse-prepare / refuse-validate / deferred / escalated / not-satisfied) may exhaust remaining *evaluation* duties while still requiring honest recording and closure of what occurred — never silent disappearance of the concern.

---

## 5. Stage Definitions

### CVL-01 — Verification Initiation

**Constitutional purpose**  
Open a material verification concern by naming the published constitutional specifications under evaluation and the scope of the concern — without inventing law, opening against unpublished customs, or treating initiation as a certificate.

**Constitutional inputs**

- Identifiable published Constitution / EIP / Programme VI / VII / VIII specification references for the concern scope
- Concern identity (what implementation subject / fidelity question is under verification)
- Optional identifiable WS1 / MS001 conformance artefacts to be consumed (not rewritten)
- Optional published indication of required CV-01…CV-07 types for the scope

**Constitutional outputs**

- An initiated verification concern record naming specifications, scope, and intended CV type set — **or**
- Lawful refuse-open when standards are unpublished, scope is theatrical, or initiation would invent law

**Permitted activities**

- Name published specifications as evaluation standards
- Bound the concern scope without amending corpora
- Record intended CV types from the published catalogue
- Refuse initiation when constitutional preconditions fail
- Preserve initiation audit identity for later stages

**Prohibited activities**

- Treat “how main works,” tribal knowledge, or stack preference as the standard
- Create or modify constitutional specifications by opening a concern
- Certify an implementation at initiation
- Invent unpublished verification types
- Skip initiation when a material finding will later be claimed

**Authority preserved**  
Published corpora remain the sole standard. Initiation organises; it does not legislate.

---

### CVL-02 — Evidence Preparation

**Constitutional purpose**  
Identify and prepare **named implementation evidence** for evaluation — so assessment evaluates real subjects, not anonymous theatre — without mutating artefacts to manufacture passable evidence.

**Constitutional inputs**

- Initiated concern from CVL-01
- Candidate implementation evidence identities (structure, behaviour, evidence-handling, runtime, interface, API, governance subjects as applicable)
- Published evidence-identity expectations from WS2 / MS001 and relevant Programme VIII / EIP corpora

**Constitutional outputs**

- A prepared evidence bundle with named subjects bound to the concern — **or**
- Lawful refuse-prepare when evidence identity is missing, forged, or would require unlawful mutation

**Permitted activities**

- Collect and name implementation evidence identities
- Bind evidence to the initiated concern and intended CV types
- Refuse preparation when evidence cannot be honestly identified
- Preserve evidence-identity records for audit and explainability

**Prohibited activities**

- Invent missing evidence identities
- Modify implementation artefacts so they become easier to pass
- Treat CI noise, coverage percentages, or UI ticks as constitutional evidence subjects without published mapping
- Redefine educational or constitutional meaning while “preparing”
- Present preparation as satisfaction or certification

**Authority preserved**  
Evidence remains an assessed subject. Preparation organises identity; it does not author educational truth or rewrite code under lifecycle pretext.

---

### CVL-03 — Traceability Validation

**Constitutional purpose**  
Confirm that **established** CT-01…CT-07 relationships required for the concern exist and are consumable — so evaluation does not invent lineage mid-flight.

**Constitutional inputs**

- Prepared evidence bundle from CVL-02
- Required published CT relationship identities for the concern scope
- Established CT provenance / relationship records from WS1 / MS002
- Optional conformance artefact identities already linked under CT law

**Constitutional outputs**

- A validated lineage set naming the established relationships to be consumed — **or**
- Lawful refuse-validate when required relationships are missing, invented, unstable, or forged

**Permitted activities**

- Confirm existence and identity of established CT relationships
- Bind validated lineage to the concern and prepared evidence
- Refuse progress when lineage is incomplete for the required scope
- Preserve lineage-consumption records for audit

**Prohibited activities**

- Invent CT relationships to force progress
- Treat “somehow linked in a ticket” as established constitutional traceability
- Rewrite CT meaning or forge provenance
- Treat validated lineage as itself “verified” or “conformant”
- Skip lineage validation when material findings will be claimed

**Authority preserved**  
WS1 / MS002 owns relationship law. This stage consumes and validates presence; it does not author lineage.

---

### CVL-04 — Constitutional Evaluation

**Constitutional purpose**  
Apply published **CV-01…CV-07** verification types against prepared implementation evidence under published constitutional requirements and validated lineage — yielding evaluation dispositions without rewriting law or certifying implementations.

**Constitutional inputs**

- Validated lineage set from CVL-03
- Prepared evidence bundle from CVL-02
- Published constitutional specifications named at CVL-01
- Published CV-01…CV-07 criteria from WS2 / MS001
- Optional conformance artefacts consumed as inputs (unchanged)

**Constitutional outputs**

- Evaluation dispositions per applied CV type (satisfied / not-satisfied / deferred / escalated under published criteria)
- Composition notes when multiple CV types bind the concern

**Permitted activities**

- Apply only published CV-01…CV-07 types required by the concern
- Evaluate named evidence against published requirements using validated lineage
- Prefer honest not-satisfied / deferred / escalated over improvisation
- Compose published CV conjunctions without collapsing failed checks
- Remain repeatable and implementation-neutral

**Prohibited activities**

- Invent unpublished verification types or customs
- Modify constitutional specifications to force satisfaction
- Redefine Programme VI educational meaning, CC criteria, or CT meaning in evaluation prose
- Privilege a technology stack as constitutional
- Certify implementations, stacks, vendors, or releases
- Invent lineage during evaluation
- Rewrite conformance findings to force a pass
- Determine educational quality, mastery, or readiness as a CV outcome

**Authority preserved**  
WS2 / MS001 owns verification types. This stage applies them; it does not amend the catalogue or become constitutional authority.

---

### CVL-05 — Findings Production

**Constitutional purpose**  
Emit **verification findings** as lawful dispositions under published criteria — speaking to whether evidence satisfied published requirements — without converting findings into amendments, certificates, or educational grades.

**Constitutional inputs**

- Evaluation dispositions from CVL-04
- Published finding vocabulary (satisfied / not-satisfied / deferred / escalated)
- Bound references to specifications, evidence, relationships, and CV types

**Constitutional outputs**

- Verification findings for the concern (including composition outcomes when multiple CV types apply)
- Explicit non-certificate framing (findings are evaluative dispositions only)

**Permitted activities**

- Produce findings under published dispositions only
- Bind each finding to the CV types and specs that produced it
- Record composition / stop-rule application honestly
- Prefer understatement over invented green
- Propose (not enact) upstream corpus amendments when law itself must change

**Prohibited activities**

- Issue certificates for implementations, stacks, vendors, releases, or pipelines
- Present findings as constitutional amendments or new educational meaning
- Narrate satisfaction as mastery, readiness, educational quality, or permanent conformity
- Rewrite findings to match product urgency
- Collapse multi-type failures into a single false “satisfied”

**Authority preserved**  
Findings evaluate evidence against law. They never become law or certificates.

---

### CVL-06 — Findings Recording

**Constitutional purpose**  
Preserve **audit-speakable records** of the lifecycle so reconstruction can answer which specs, evidence, relationships, stages, and findings applied — without erasing history or forging provenance.

**Constitutional inputs**

- Verification findings from CVL-05
- Stage traces from CVL-01…CVL-05
- Boundary confirmations required by `LIFECYCLE_BOUNDARIES.md`
- Continuity obligations from EIP-005

**Constitutional outputs**

- Audit records binding specifications, evidence identities, CT relationships, CV types, CVL stages, findings, and preserved boundaries
- Reconstructable explainability substrate for `LIFECYCLE_EXPLAINABILITY.md`

**Permitted activities**

- Record constitutional references (not only technical CI logs)
- Bind findings to the producing stage (especially CVL-04 / CVL-05)
- Preserve prior lawful history; refuse silent erasure
- Project one truth to student / developer / auditor vocabularies later

**Prohibited activities**

- Erase prior lawful verification or lifecycle history to simplify the next report
- Forge provenance or invent missing corpus references
- Treat audit records as constitutional amendments
- Drop stage-to-finding binding
- Substitute ticket IDs, SHAs, or stack names for published corpus identity as the sole record

**Authority preserved**  
Recording preserves reconstructability. It does not author law or certify subjects.

---

### CVL-07 — Verification Closure

**Constitutional purpose**  
Close the verification lifecycle **honestly** when coordination duties for the concern are exhausted — including lawful early stops — without certifying implementations, freezing stacks, or pretending incomplete work is complete.

**Constitutional inputs**

- Recorded findings and audit records from CVL-06
- Confirmation that remaining coordination duties are exhausted or lawfully stopped
- Boundary confirmations (non-certification, non-legislation, non-redefinition, non-substitution)

**Constitutional outputs**

- Closed lifecycle disposition for the concern — **or**
- Lawful refuse-close when recording is incomplete, boundaries were breached, or closure would imply certification / permanent conformity / new law

**Permitted activities**

- Affirm closure when published duties are exhausted
- Close after lawful refuse / defer / escalate / not-satisfied paths with honest records
- Refuse closure when audit or boundary preconditions fail
- Keep closure distinct from conformance certificates and educational success

**Prohibited activities**

- Certify implementations, stacks, vendors, or releases by closing
- Replace MS001 conformance evaluation with “lifecycle closed”
- Redefine constitutional meaning in closure speech
- Modify constitutional specifications or implementation artefacts as a closure act
- Erase inconvenient stage history so closure looks clean
- Treat closure as licence for the next cycle to use the implementation as constitutional authority

**Authority preserved**  
Closure ends coordination for the concern. Published corpora remain the sole standard afterward.

---

## 6. Stage Transition Rules

| From | To | Transition requires |
|------|----|---------------------|
| — | CVL-01 | Material verification concern needs opening |
| CVL-01 | CVL-02 | Concern initiated (not refuse-open) |
| CVL-01 | CVL-06 / CVL-07 path | Refuse-open recorded honestly |
| CVL-02 | CVL-03 | Evidence prepared (not refuse-prepare) |
| CVL-02 | CVL-06 / CVL-07 path | Refuse-prepare recorded honestly |
| CVL-03 | CVL-04 | Lineage validated (not refuse-validate) |
| CVL-03 | CVL-06 / CVL-07 path | Refuse-validate recorded honestly |
| CVL-04 | CVL-05 | Evaluation dispositions available |
| CVL-05 | CVL-06 | Findings produced under published vocabulary |
| CVL-06 | CVL-07 | Audit records preserved |
| CVL-07 | — | Closed or refuse-close recorded |

Silent jumps that claim findings without CVL-01…CVL-03 honesty are constitutionally defective.

---

## 7. Composition with Verification Types

| During stage | Relationship to CV-01…CV-07 |
|--------------|-----------------------------|
| CVL-01 | May *name* intended CV types; does not apply them |
| CVL-02 | Prepares evidence subjects those types will assess |
| CVL-03 | Validates lineage those types will consume |
| **CVL-04** | **Applies** CV-01…CV-07 |
| CVL-05 | Emits findings produced by those applications |
| CVL-06 | Records CV identities with findings |
| CVL-07 | Closes without inventing new CV types |

Cross-cutting concerns may bind multiple CV types at CVL-04. Lifecycle stages remain CVL-01…CVL-07 only.

---

## 8. Closing Statement

> **Stages sequence verification.  
> Stages do not redefine constitutional meaning, certify implementations, or replace constitutional authority.**
