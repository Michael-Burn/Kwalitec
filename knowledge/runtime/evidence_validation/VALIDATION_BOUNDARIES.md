# Validation Boundaries

**Programme:** VIII — Workstream 2 — Constitutional Evidence Consumption  
**Milestone:** MS002 — Constitutional Evidence Validation Model  
**Classification:** Authority limits — what runtime may and must never do when validating constitutional evidence  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **Constitutional Evidence Validation authority limits**: what runtime implementations may lawfully do when verifying published evidence and determining execution eligibility, and what must remain with the Constitution, EIP, Programme VI, Programme VII, Programme VIII WS1 contracts / event / completion corpora, and Programme VIII WS2 / MS001 evidence consumption corpora.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md)
3. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
4. [`CONSTITUTIONAL_EVIDENCE_VALIDATION_MODEL.md`](CONSTITUTIONAL_EVIDENCE_VALIDATION_MODEL.md)
5. [`VALIDATION_OBJECTIVES.md`](VALIDATION_OBJECTIVES.md)
6. [`VALIDATION_TYPES.md`](VALIDATION_TYPES.md)
7. [`../evidence_consumption/EVIDENCE_BOUNDARIES.md`](../evidence_consumption/EVIDENCE_BOUNDARIES.md)
8. [`../contracts/CONTRACT_BOUNDARIES.md`](../contracts/CONTRACT_BOUNDARIES.md)
9. Programme VI boundary corpora (Master Planner and coaches)
10. Programme VII boundary corpora (workflow, authority, recommendation, state)
11. EIP Continuity, Explainability, and Knowledge & Mastery standards

> **Runtime may verify published evidence,  
> verify provenance,  
> verify contractual compliance,  
> and determine execution eligibility.  
> Runtime must never modify evidence,  
> reinterpret evidence meaning,  
> invent provenance,  
> create substitute evidence,  
> or bypass constitutional validation requirements.**

---

## 1. Purpose

Runtime that silently becomes a second evidence authority — rewriting warrants during “validation,” inventing provenance so a tip can ship, manufacturing substitute evidence when checks fail, judging educational quality under the label “eligible,” or bypassing validation for demos — destroys student trust and educational integrity.

This document draws a bright line between **lawful evidence validation** (Programme VIII / WS2 / MS002) and **constitutional evidence authorship / educational judgement** (Constitution / EIP / Programmes VI–VII / permitted writers / MS001 producers).

---

## 2. Boundary Principles

1. **Validate, do not transform.** Validation confirms suitability; it does not alter evidence.
2. **Published evidence only.** Unpublished customs and infrastructure signals without EC mapping are hard stops.
3. **Published validation only.** Unpublished EV customs are unlawful.
4. **Published contracts only.** Validation without RC binding is unlawful.
5. **Exactly as published.** Successful validation never rewrites meaning or classification.
6. **Integrity first.** Altered or enriched warrants are refused, not “fixed” in validation.
7. **Provenance required.** Origin and succession are not optional metadata and must not be invented.
8. **Eligibility ≠ quality.** Validation never grades learning, mastery, readiness, or constitutional truth.
9. **No reinterpretation.** Programme VI questions and EIP-002 claim classes survive validators intact.
10. **No substitute evidence.** Failed checks do not authorise minting replacement warrants.
11. **No bypass.** Product urgency never waives constitutional validation requirements.
12. **Determinism.** Race-dependent eligibility is a defect.
13. **Explain the stop.** Students and developers should hear when validation must refuse.
14. **No emergency exemption.** Load, deadlines, and demos never mint constitutional validation power.
15. **Replaceability.** Validator / schema topology never becomes validation law.

---

## 3. What Runtime May Do (Lawful)

| Lawful action | Constitutional meaning |
|---------------|------------------------|
| **Verify published evidence** | Apply EV-01…EV-07 to EC-01…EC-07 instances with identifiable published producers |
| **Verify provenance** | Confirm producer, corpus path, succession / continuity refs, and non-forgery (EV-02) |
| **Verify contractual compliance** | Confirm RC-01…RC-07 bindings for the contemplated act (EV-03) |
| **Determine execution eligibility** | Emit eligible / ineligible / defer / escalate under EV-06 composition |
| **Refuse unlawfully requested consumption** | Prefer honest stop / defer / escalate over improvisation |
| **Compose required checks** | Apply published EV conjunctions without collapsing failed checks |
| **Remain deterministic** | Same published inputs → same eligibility disposition |
| **Remain replaceable** | Honour validation law in any compliant implementation |
| **Explain validation** | Answer evidence / EV / contracts / eligibility / boundaries without rewriting meaning |

These actions **validate eligibility**. They do **not** publish a new Evidence Model, invent coach warrants, mint tips, author ownership maps, invent EV types, or judge educational quality.

---

## 4. What Runtime Must NEVER Do

| Forbidden action | Why | Lawful alternative |
|------------------|-----|--------------------|
| **Modify evidence** | Producers own warrant content; validation is non-transformative | Leave evidence unchanged; refuse / escalate for corpus amendment |
| **Reinterpret evidence meaning** | Programme VI / EIP-002 own meaning and claim classes | Confirm published meaning; never rewrite it |
| **Invent provenance** | Provenance is constitutional attribution, not UX filler | Require published producer refs or refuse |
| **Create substitute evidence** | EC catalogue is closed; substitutes are law invention | Refuse failed instances; propose corpus amendment upstream |
| **Bypass constitutional validation requirements** | Validation requirements are educational care, not optional polish | Prefer no-action / understatement over invented eligibility |
| **Enrich evidence to force a pass** | Enrichment is alteration by another name | Stop; request published producer repair under permitted writers |
| **Reclassify evidence during validation** | Classification owners own claim classes | Preserve published class; refuse soft-upgrades |
| **Determine educational meaning** | Programme VI owns coach / planner questions | Confirm eligibility only |
| **Determine educational quality** | No EV is a quality rubric | Keep eligibility speech distinct from quality speech |
| **Determine constitutional truth** | Constitution / EIP own truth | Obey published law; do not adjudicate truth in validators |
| **Transfer authority** | Programme VII WS2 owns ownership, permission, and conflict disposition | Apply Authority / Conflict corpora; refuse domain absorption |
| **Invent educational state** | Programme VII WS4 owns EST/CST context law | Apply published postures / transitions only |
| **Generate unpublished recommendations** | Programme VII WS3 + Programme VI owners own tip warrant | Surface lawful artefacts or no-recommendation after eligible consumption |
| **Modify constitutional specifications** | Constitution / EIP / Programmes VI–VIII are amended only under their governance | Change code to obey law, or propose a corpus amendment — never patch law in a validator |
| **Treat Twin / Adaptive / UI / storage noise as EV publishers** | They are consumers / delivery surfaces | Require published EV/EC mapping or refuse |
| **Present scores / acks / latency / cache hits as eligibility or quality** | Operational proxies are not validation law | Cite published corpora, EC, EV, and RC |
| **Become irreplaceable by validator topology** | Replaceability | Keep validation law implementation-independent |

---

## 5. Authority Map

| Concern | Owner | Runtime evidence-validation role |
|---------|-------|----------------------------------|
| Educational truth / integrity | Constitution + EIP | Verify / obey — never adjudicate truth as a quality score |
| Educational Evidence of understanding | EIP-002 (+ EIP-001 writers) | Validate integrity / provenance / eligibility under EC-01 / EC-02 + RC-02 |
| Educational meaning | Programme VI | Never reinterpret via validators |
| Educational quality / mastery / readiness | Programme VI + EIP claim honesty | **Out of EV scope** — eligibility only |
| Workflow orchestration evidence | Programme VII WS1 | Validate when consuming under EC-03 / RC-03 |
| Decision ownership / conflict | Programme VII WS2 | Validate under EV-04 / EC-04 / RC-04 |
| Recommendations | Programme VII WS3 + VI owners | Validate before surfacing under EC-05 / RC-05 |
| Educational context (EST/CST) | Programme VII WS4 | Validate under EV-05 / EC-06 / RC-06 |
| Runtime execution / audit trails | Programme VIII / WS1 | Validate under EV-06 / EV-07 / RC-07 |
| Runtime execution contracts | Programme VIII / WS1 / MS001 | Validate contractual compliance (EV-03) |
| Constitutional evidence consumption rules | Programme VIII / WS2 / MS001 | Specialise Validate phase; preserve EC catalogue |
| Constitutional evidence validation rules | Programme VIII / this corpus | Bind / enforce EV-01…EV-07 |
| Product UX / Adaptive / Twin / stores | Architecture / Version 2 / infra | Downstream delivery only — never EV authors |

---

## 6. Boundary Checks (Pre-Eligibility)

Before material constitutional evidence is treated as eligible for consumption, validation requires affirmative answers:

| Check | Question |
|-------|----------|
| **EVB-01 Evidence class** | Is this a published EC-01…EC-07 category (not an unpublished custom)? |
| **EVB-02 Validation class** | Are required EV-01…EV-07 categories being applied (not unpublished customs)? |
| **EVB-03 Producer** | Which published corpus / permitted writer authored the evidence? |
| **EVB-04 Contract** | Which RC-01…RC-07 contract(s) authorise validation and contemplated consumption? |
| **EVB-05 Integrity** | Is the evidence intact and claim-class honest as published (EV-01)? |
| **EVB-06 Provenance** | Are producer, succession, and corpus refs present and non-forged (EV-02)? |
| **EVB-07 Non-modification** | Does validation avoid modifying, enriching, or rewriting the warrant? |
| **EVB-08 Non-reinterpretation** | Does validation avoid reinterpreting Programme VI educational meaning? |
| **EVB-09 Non-reclassification** | Does validation avoid reclassifying the warrant? |
| **EVB-10 No substitutes** | Does failure avoid creating substitute evidence or invented provenance? |
| **EVB-11 Authority honesty** | If ownership-sensitive, does EV-04 pass under published WS2 law? |
| **EVB-12 State honesty** | If context-sensitive, does EV-05 pass under published WS4 law? |
| **EVB-13 Eligibility ≠ quality** | Is the outcome framed as eligibility — not educational quality / truth? |
| **EVB-14 Spec immutability** | Does validation avoid modifying constitutional specifications? |
| **EVB-15 Determinism / audit** | Is disposition reproducible; will EV-07 / RC-07 records preserve evidence, EV, contracts, eligibility, and boundaries? |

Any failed check → refuse / defer / escalate. Do not “best-effort” invent validation law or repair evidence in situ.

---

## 7. Relationship to Sibling Boundaries

| Sibling corpus | Relationship |
|----------------|--------------|
| [`../evidence_consumption/EVIDENCE_BOUNDARIES.md`](../evidence_consumption/EVIDENCE_BOUNDARIES.md) | This Model specialises the Validate horizon of those limits; consumption boundaries remain binding after eligibility |
| [`../contracts/CONTRACT_BOUNDARIES.md`](../contracts/CONTRACT_BOUNDARIES.md) | EV-03 specialises contractual limits for the validation horizon |
| [`../event_processing/EVENT_BOUNDARIES.md`](../event_processing/EVENT_BOUNDARIES.md) | CE processing may deliver evidence-facing stimuli; validation still obeys these limits |
| [`../execution_completion/COMPLETION_BOUNDARIES.md`](../execution_completion/COMPLETION_BOUNDARIES.md) | Completion may reference eligibility; it never mints evidence or rewrites validation outcomes |
| Programme VI `*_BOUNDARIES.md` | Validators must not cross coach / planner boundaries while checking eligibility |
| Programme VII `AUTHORITY_BOUNDARIES.md` | EV-04 specialises validation under those limits |
| Programme VII state / transition boundaries | EV-05 specialises validation under those limits |
| EIP-001 State Authority Matrix | Mutation rights remain orthogonal; validation never grants them by proximity |
| EIP-002 Educational Evidence Model | EV checks confirm intact published classifications; they never invent a rival model or quality rubric |

This document does not replace sibling boundaries. It binds **evidence validation** so those boundaries survive validators, schemas, caches, and replacements.

---

## 8. Closing Statement

> **Runtime evidence validation is powerful only as a faithful eligibility gate for published warrants.  
> The moment it modifies evidence, reinterprets meaning, invents provenance, creates substitute evidence, or bypasses validation requirements — or pretends eligibility is educational quality — it has left constitutional education and entered product fiction.**
