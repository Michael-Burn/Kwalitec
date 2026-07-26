# Validation Types

**Programme:** VIII — Workstream 2 — Constitutional Evidence Consumption  
**Milestone:** MS002 — Constitutional Evidence Validation Model  
**Classification:** Closed catalogue of recognised constitutional evidence validation categories  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional evidence validation categories** (EV-01…EV-07).

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_EVIDENCE_VALIDATION_MODEL.md`](CONSTITUTIONAL_EVIDENCE_VALIDATION_MODEL.md)
3. [`VALIDATION_OBJECTIVES.md`](VALIDATION_OBJECTIVES.md)
4. [`../evidence_consumption/EVIDENCE_TYPES.md`](../evidence_consumption/EVIDENCE_TYPES.md)
5. [`../contracts/CONTRACT_TYPES.md`](../contracts/CONTRACT_TYPES.md)
6. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. Programme VI corpora under [`../../educational/`](../../educational/)
8. Programme VII corpora under [`../../orchestration/`](../../orchestration/)
9. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published validation categories may confirm constitutional eligibility for execution.  
> Unpublished “implied validation” is constitutionally defective.**

**Catalogue disambiguation:** EV-01…EV-07 here are *constitutional evidence validation categories*. They are not Educational Validation Framework coach capability IDs (EC-xx elsewhere), and they are not MS001 constitutional evidence categories (also EC-xx).

---

## 1. Purpose

Runtime without a closed validation catalogue invents law by proximity: whichever checksum, schema pass, or estimate is nearest becomes the tutor’s “proof that evidence is fine.”

This catalogue names the only lawful constitutional evidence validation categories a runtime may apply before consumption — and binds each category to purpose, inputs, outputs, and permitted / prohibited validation.

---

## 2. Catalogue Overview

| ID | Validation category | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|---------------------|--------------------------------|----------------|-----------------|
| **EV-01** | Integrity Validation | Confirm warrant intact as published | Published EC instance + published meaning / claim class | Integrity pass / fail (+ refuse/defer/escalate) |
| **EV-02** | Provenance Validation | Confirm origin attributable and non-forged | Producer / corpus / succession / continuity refs | Provenance pass / fail (+ refuse/defer/escalate) |
| **EV-03** | Contract Validation | Confirm RC authorisation for contemplated consumption | Contemplated act + RC-01…RC-07 catalogue | Contract compliance pass / fail |
| **EV-04** | Authority Validation | Confirm ownership / permission suitability when applicable | EC-04 / WS2 artefacts + contemplated decision act | Authority suitability pass / fail |
| **EV-05** | State Validation | Confirm EST/CST / context suitability when applicable | EC-06 / WS4 artefacts + contemplated context act | State suitability pass / fail |
| **EV-06** | Runtime Eligibility Validation | Confirm published execution preconditions for consumption | Validation outcomes + RC / completion / event bindings as published | Eligibility disposition |
| **EV-07** | Audit Validation | Confirm reconstructability of the validation act | EV/EC/RC identities + eligibility outcome + boundary record | Audit readiness pass / fail |

Material validation must map to one or more of these categories as published law requires. Cross-cutting situations may bind multiple EV categories; none may invent a category outside this catalogue.

**Relation to EC-01…EC-07:** Evidence categories remain defined solely by MS001. EV categories *check* published EC instances; they do not replace or reclassify them.

**Relation to educational quality:** No EV category judges whether learning was good, whether a tip was wise, or whether the student is ready. Eligibility ≠ quality.

---

## 3. EV-01 — Integrity Validation

### Constitutional purpose

Confirm that the published constitutional evidence instance remains **intact, claim-class honest, and unaltered** relative to published law — so consumption proceeds only on honest warrants.

### Constitutional inputs

- Published EC-01…EC-07 evidence instance (as received under MS001).
- Published producer meaning / claim classification (EIP-002 / Programme VI / Programme VII / Programme VIII WS1 as applicable).
- Published integrity expectations from MS001 ECO-02 / ECB-04 and this Model’s EVO-02.

### Constitutional outputs

- Integrity validation disposition: **pass** or **fail**.
- On fail: lawful **refuse / defer / escalate** — evidence left unchanged.
- Audit-speakable integrity note (intact-as-published: true/false).

### Permitted validation

- Verify that meaning, classification, and claim honesty survive as published.
- Detect alteration, truncation, enrichment, or silent soft-upgrade attempts.
- Refuse consumption when integrity cannot be confirmed.
- Emit RC-07 / EV-07-compatible records of the integrity check.

### Prohibited validation

- Modify, enrich, repair, or rewrite the evidence so it “passes.”
- Reclassify claim classes during the check (coverage → understanding → mastery upgrades).
- Treat checksum / schema theatre as educational quality judgement.
- Invent missing meaning fields to complete an incomplete warrant.
- Use EV-01 to determine educational truth or student readiness.

---

## 4. EV-02 — Provenance Validation

### Constitutional purpose

Confirm that **producer identity, corpus path, claim class attribution, succession history, and continuity references** are present, attributable, and non-forged — so origin can be reconstructed.

### Constitutional inputs

- Provenance fields / references attached to the published EC instance.
- Authorising corpus paths and permitted-writer identity when mutation history is material (EIP-001).
- Continuity expectations (EIP-005) and MS001 ECO-03 / ECB-05.

### Constitutional outputs

- Provenance validation disposition: **pass** or **fail**.
- On fail: lawful **refuse / defer / escalate** — no invented provenance.
- Audit-speakable provenance record (producer, corpus refs, succession / continuity refs as confirmed).

### Permitted validation

- Verify producer and corpus references against published catalogues.
- Detect missing, stripped, or forged provenance.
- Prefer stop over fabricating origin for UX continuity.
- Preserve continuity references when confirming history (EIP-005).

### Prohibited validation

- Invent provenance stamps, producers, or succession history.
- Replace constitutional provenance with storage keys, cache hits, broker metadata, or Twin estimates.
- Erase prior lawful history to simplify validation UX.
- Treat “unknown origin but looks fine” as a pass.
- Use EV-02 to mint authority, tips, or educational state.

---

## 5. EV-03 — Contract Validation

### Constitutional purpose

Confirm that the contemplated consumption / execution is **authorised by published RC-01…RC-07 contracts** — especially RC-02 when observational Educational Evidence is at stake — so software never consumes under unpublished customs.

### Constitutional inputs

- Contemplated runtime act (consume / hand off / surface / advance under published law).
- Applicable RC-01…RC-07 catalogue from Programme VIII / WS1 / MS001.
- EC category of the evidence instance (MS001).

### Constitutional outputs

- Contract compliance disposition: **pass** or **fail**.
- Named RC binding(s) that authorised (or refused) the act.
- On fail: lawful **refuse / defer / escalate**.

### Permitted validation

- Map the contemplated act to published RC identities.
- Require RC-02 when EIP-002 observational Educational Evidence is at stake.
- Require sibling RCs when workflow / authority / recommendation / state / audit horizons apply.
- Refuse acts that lack contractual authorisation.

### Prohibited validation

- Invent unpublished contracts or “temporary RC” exceptions.
- Treat table readability, API reachability, or feature flags as constitutional contracts.
- Weaken RC obligations because validation elsewhere looked green.
- Use EV-03 to amend Programme VIII WS1 contract meanings.
- Use EV-03 to determine educational meaning or quality.

---

## 6. EV-04 — Authority Validation

### Constitutional purpose

Confirm — when the contemplated act depends on decision ownership, permission, or conflict disposition — that **published authority evidence** is suitable for that act under Programme VII Workstream 2 law.

### Constitutional inputs

- Published EC-04 Authority Evidence (ownership maps, permission records, conflict-disposition trails) when applicable.
- Contemplated decision / ownership-sensitive act.
- Programme VII Authority / Conflict corpora and RC-04.

### Constitutional outputs

- Authority suitability disposition: **pass** or **fail** (or **not applicable** when no authority horizon is engaged — explicitly recorded).
- On fail: lawful **refuse / defer / escalate** under published conflict / authority law.
- Audit-speakable authority refs (without transferring ownership).

### Permitted validation

- Verify that required ownership / permission / disposition artefacts exist as published.
- Confirm integrity and provenance of EC-04 inputs via composition with EV-01 / EV-02 when required.
- Prefer refuse / defer / escalate when authority evidence is missing or conflicting under published conflict law.
- Bind RC-04 when authority-sensitive execution is contemplated.

### Prohibited validation

- Invent ownership, permission, or conflict winners during validation.
- Transfer authority as a side-effect of a “pass.”
- Reclassify “service that held the row” as constitutional owner.
- Bypass Authority / Conflict corpora because other EV checks passed.
- Use EV-04 to mint tips, educational state, or Educational Evidence of understanding.

---

## 7. EV-05 — State Validation

### Constitutional purpose

Confirm — when the contemplated act depends on educational context — that **published EST/CST / state evidence** is suitable for that act under Programme VII Workstream 4 law.

### Constitutional inputs

- Published EC-06 State Evidence (EST/CST postures, transition warrants, succession trails) when applicable.
- Contemplated context-sensitive act.
- Programme VII state / transition corpora and RC-06.

### Constitutional outputs

- State suitability disposition: **pass** or **fail** (or **not applicable** when no state horizon is engaged — explicitly recorded).
- On fail: lawful **refuse / defer / escalate**.
- Audit-speakable state refs (without inventing postures).

### Permitted validation

- Verify that required published postures / transition warrants exist as classified.
- Confirm integrity and provenance of EC-06 inputs via composition with EV-01 / EV-02 when required.
- Preserve continuity of context history when confirming suitability (EIP-005).
- Bind RC-06 when context-sensitive execution is contemplated.

### Prohibited validation

- Invent EST/CST postures or reclassify UI mode / feature flag as state law.
- Alter state meaning to force entry/exit outside published transition law.
- Treat Twin / Adaptive estimates as primary state evidence when WS4 law does not authorise that classification.
- Bypass state transition / boundary law because other EV checks passed.
- Use EV-05 to mint mastery, unpublished tips, or Educational Evidence meaning.

---

## 8. EV-06 — Runtime Eligibility Validation

### Constitutional purpose

Confirm the **overall constitutional eligibility disposition** for the contemplated runtime consumption / execution — composing required EV outcomes and published execution preconditions — without judging educational quality or truth.

### Constitutional inputs

- Outcomes of required EV-01…EV-05 checks for the act (as published law requires).
- Published RC / event / completion bindings relevant to the act (RC-01, CE stimuli, REC completion preconditions as applicable).
- MS001 consumption preconditions (ECB checks) that validation specialises.

### Constitutional outputs

- Eligibility disposition: **eligible** / **ineligible** / **defer** / **escalate**.
- Explicit catalogue of which EV checks were required and how they composed.
- On ineligible / defer / escalate: no consumption of the warrant for the contemplated act.

### Permitted validation

- Compose published validation requirements into a single eligibility disposition.
- Allow consumption to proceed only when required checks pass.
- Keep eligibility speech distinct from learning / mastery / pass speech.
- Remain deterministic under identical published inputs.

### Prohibited validation

- Declare eligibility by inventing missing EV passes.
- Soften failed integrity / provenance / contract checks into “eligible with warnings” when published law requires a hard stop.
- Equate eligibility with educational quality, readiness, or constitutional truth.
- Bypass constitutional validation requirements for demos, load, or product urgency.
- Use EV-06 to amend evidence, create substitute warrants, or reinterpret meaning.

---

## 9. EV-07 — Audit Validation

### Constitutional purpose

Confirm that the validation act itself is **reconstructable**: evidence identity, EV categories applied, authorising contracts, eligibility outcome, and boundary preservation can be audited later under RC-07.

### Constitutional inputs

- Material validation act record requirements (EVO-06; RC-07 Audit Contract).
- ECE-aligned explainability components for validation (see `VALIDATION_EXPLAINABILITY.md`).
- Continuity expectations (EIP-005) across retries and replacements.

### Constitutional outputs

- Audit readiness disposition: **pass** or **fail**.
- On fail: the validation act is not yet constitutionally complete — even if other checks looked green.
- Audit-speakable trail refs sufficient for later reconstruction.

### Permitted validation

- Verify presence of constitutional references required for reconstruction.
- Refuse to treat the validation act as complete when audit components are missing.
- Preserve continuity of prior lawful validation / consumption history.
- Bind RC-07 for all material validations.

### Prohibited validation

- Accept technical validator logs as substitutes for constitutional audit refs.
- Erase failed checks from the trail to present a cleaner story.
- Fabricate audit completeness.
- Present scores / latency / ack counts as audit of educational warrant.
- Use EV-07 to mint Programme VI meaning or Programme VII ownership / tips / state.

---

## 10. Catalogue Rules

1. **Closed catalogue.** New EV types require a Programme VIII constitutional amendment — not a silent schema invention.
2. **Evidence required.** Every material EV act validates a published EC-01…EC-07 instance (or explicitly records not-applicable horizons for EV-04 / EV-05).
3. **RC binding required.** Material validation without RC identity is unlawful.
4. **Non-transformative.** Validation never alters, enriches, reclassifies, or reinterprets evidence.
5. **Eligibility ≠ quality.** No EV may judge educational quality, mastery, readiness, or constitutional truth.
6. **No silent collapse.** EV categories may compose; they must not be collapsed to hide failed checks.
7. **Failed → stop.** Failures yield refuse / defer / escalate — never substitute evidence.
8. **Exactly as published.** Successful validation authorises consumption of the *unchanged* published warrant under MS001.

---

## 11. Closing Statement

> **If runtime cannot name which EV-01…EV-07 validation was applied to which EC evidence, under which RC binding, yielding which eligibility outcome, the artefact is not yet constitutionally validated for execution — and must not be treated as educational law.**
