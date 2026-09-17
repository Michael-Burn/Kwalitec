# Student Progress Semantics: Phase 2 Semantic Contract

**Status:** Locked Phase 2 semantic contract; Coverage definition amended 2026-09-17 for dual-source reconciliation (shadow interpretive layer; live display cutover deferred)  
**Date:** 2026-09-16 (Coverage §5.1 amended 2026-09-17)  
**Scope:** Authoritative meanings of Coverage, Progression Readiness, Exam Readiness, and Streak as student-progress concepts  
**Authority class:** Product semantic contract under `knowledge/product/` (same convention as locked evaluator and framework designs)  
**Does not authorize:** Live coverage display cutover, formula merges beyond the locked meanings, Decision Engine wiring, or Educational Framework redesign

---

## 1. Purpose

This document locks the Phase 2 semantic contract for four student-facing progress concepts so the meanings live in the repository as a reconciliation instrument, not only in conversation history.

It answers, for each concept:

1. What educational question does it answer?
2. What may lawfully feed it?
3. What must never feed it?
4. What shape may its output take?
5. How must it behave under thin or conflicting evidence?
6. What may it inform?
7. What must it never control or become?

This contract defines the **target meaning**. It does not perform reconciliation of live implementations. Competing live formulas that share a student-facing word remain implementation debt until a later scoped brief aligns them to this contract.

---

## 2. Relationship to existing law

| Document | Relationship to this contract |
|----------|-------------------------------|
| [`../progression_readiness/PROGRESSION_READINESS_DESIGN.md`](../progression_readiness/PROGRESSION_READINESS_DESIGN.md) | **Authoritative** for Progression Readiness evaluator contracts, ternary outcomes, reason codes, philosophy, and learner activation posture. This contract **references** that design. It must not restate per-objective contracts or contradict that document. |
| Educational Constitution (Study Progress; Readiness) | Higher educational law for Coverage-as-Study-Progress and Exam Readiness as preparedness posture. This contract specializes those meanings into a four-concept operational template. |
| LO-07 Exam Readiness (`knowledge/educational/learning_coach/LEARNING_OBJECTIVES.md`) | Authoritative Learning Coach speech law for sitting preparedness. This contract preserves LO-07’s synthesis / refuse-when-thin posture and refuses to freeze today’s candidate evidence dimensions as a complete formula. |
| ADR-007 Student Experience | Streaks are engagement / presentation signals and must not rewrite educational decisions. |
| Phase 0 safety boundary (session practice) | Sound vs unresolved claim posture: soften overconfident speech when provenance is unresolved; do not remove features or merge formulas in this Phase 2 documentation step. |

**Non-duplication rule:** If this document and `PROGRESSION_READINESS_DESIGN.md` appear to conflict on Progression Readiness, the Progression Readiness design wins for evaluator behaviour, contracts, and activation. Amend that design first under its own brief; do not paper over it here.

---

## 3. Honesty principles (cross-cutting)

These principles are binding on every concept below and on any later claim that cites this contract.

1. **Refuse to decide rather than guess when evidence is thin.** Prefer an explicit insufficient / not-yet-claimable / unknown state over a confident-sounding number or label minted from sparse data.
2. **Never let one weak signal alone mint a confident-sounding claim.** Coverage alone, streak alone, calendar proximity alone, or a single soft behavioural signal must not produce high Exam Readiness, Progression READY, or mastery-like speech.
3. **Where a claim’s provenance is unresolved, soften rather than remove or fake certainty.** Do not delete a surface to hide ambiguity, and do not invent a single reconciled formula in speech while engines still diverge.
4. **Name the concept being claimed.** Do not use “ready,” “progress,” or “coverage” as interchangeable synonyms across these four concepts.
5. **Provenance before theatre.** Every student-facing claim should be traceable through the claim-provenance chain in §7. If a link in the chain cannot be named, the claim is unresolved and speech must disclose uncertainty.

---

## 4. Concept contract template

Each concept is defined with the same fields:

| Field | Meaning |
|-------|---------|
| **Question answered** | The single educational question the concept is allowed to answer |
| **Authoritative source** | Where the locked meaning lives (this contract plus any specialized design) |
| **Permitted inputs** | Lawful evidence and state that may feed the concept |
| **Forbidden inputs** | Inputs that must never alone, or at all, determine the concept |
| **Output / state shape** | Allowed result forms (enums, counts, percentages, stages, text) |
| **Uncertainty behaviour** | Required behaviour when evidence is thin, conflicting, or missing |
| **May inform** | Lawful downstream uses |
| **Must never control or become** | Hard exclusions |

---

## 5. Concept contracts

### 5.1 Coverage

**Definition (locked):** Curriculum coverage represents legitimate historical exposure to a canonical curriculum topic through an accepted learning pathway. Coverage does not imply competence, mastery, progression readiness, or exam readiness. Multiple evidence sources may establish coverage where their semantics satisfy the coverage contract; stronger evidence may provide greater provenance or confidence but does not automatically redefine the coverage threshold. Historical activity is preserved independently, and only activity that can be defensibly mapped to the applicable canonical curriculum entity contributes to current coverage.

**Invariant:** Absence of stronger evidence must not be interpreted as evidence that weaker but valid historical exposure did not occur.

| Field | Contract |
|-------|----------|
| **Question answered** | What portion of the authorised syllabus has the student honestly studied (exposed / completed as Study Progress), without claiming competence? |
| **Authoritative source** | This contract §5.1; Educational Constitution Article IV §1 Study Progress; product honesty path for verified Study Progress completion; canonical coverage reconciliation (shadow interpretive layer). |
| **Permitted inputs** | Lawful Study Progress completion for syllabus units that resolve to a canonical curriculum topic; verified Runtime C ``TOPIC_COMPLETED`` (non-baseline) under Study Progress honesty rules; accepted Stage A ``TopicProgress.completed`` (LEGACY_COMPLETION) when the legacy acceptance contract is met; syllabus structure used only to define the denominator (what “the syllabus” is). |
| **Forbidden inputs** | Assessment scores as coverage truth; Estimated Knowledge / Estimated Mastery as coverage; streak length; Progression Readiness READY as coverage; Exam Readiness percentage as coverage; self-reported “I understand this” / prior-knowledge claims alone as coverage of a unit not studied under Study Progress rules; orphaned or unmapped historical topic rows silently promoted to covered. |
| **Output / state shape** | Counts and/or percentages of completed Study Progress units over an explicit syllabus denominator; completed / not-completed per unit; journey-style “how far through” derived only from Study Progress. Labels must narrate coverage or study progress, not mastery. Shadow reconciliation may also emit eligibility categories (CONFIRMED_COVERED, HISTORICALLY_COMPLETED, AMBIGUOUS_HISTORICAL_ACTIVITY, NOT_COVERED) with evidence provenance; those categories are interpretive until a separate cutover brief wires them into live display. |
| **Uncertainty behaviour** | If verification rules cannot confirm completion and legacy acceptance also fails, do not count the unit as covered. Preserve ambiguous historical activity separately rather than deleting it or inventing coverage. If denominator scope is ambiguous (wrong plan / wrong curriculum context), refuse a precise percentage and disclose scope uncertainty rather than inventing a figure. Absence of verified Runtime C evidence alone must not erase accepted legacy historical exposure. |
| **May inform** | Coverage narration; Current Learning Topic advancement; pace-relative signals that consume coverage as one input among others; Exam Readiness only as one candidate evidence dimension among others (never as sole warrant). |
| **Must never control or become** | Must never become Mastery, Estimated Knowledge, Progression Readiness, Exam Readiness, or a pass prophecy. Must never alone mint “you’re ready” speech. Must never gate assessment competence claims. |

**Correct framing:** Coverage = legitimate historical syllabus exposure through an accepted learning pathway. Coverage ≠ understanding, mastery, progression readiness, or exam readiness.

**Evidence sources (non-exclusive):** LEGACY_COMPLETION (accepted Stage A Study Progress completion) and VERIFIED_COMPLETION (Runtime C verified ``TOPIC_COMPLETED``) may each establish coverage when they satisfy the coverage contract. Stronger provenance does not redefine the coverage threshold; it improves auditability.

---

### 5.2 Progression Readiness

| Field | Contract |
|-------|----------|
| **Question answered** | Does available Assessment Evidence justify introducing the next material for **this objective**? |
| **Authoritative source** | [`../progression_readiness/PROGRESSION_READINESS_DESIGN.md`](../progression_readiness/PROGRESSION_READINESS_DESIGN.md) (locked evaluator design). This section states only the cross-concept semantic role; per-objective authored contracts and reason codes live there. |
| **Permitted inputs** | Scored Assessment Evidence (`scored_correct is True` or `False`) for items listed on the authored objective contract; authored prerequisite verification where the contract requires it; authored critical-misconception flags where present. |
| **Forbidden inputs** | Unscored attempts (`scored_correct is None`); Study Progress / coverage alone; streak; Exam Readiness % or stage; Estimated Knowledge alone; participation without scored correctness; universal point averages across objectives; Decision Engine recommendations used as evidence. |
| **Output / state shape** | Ternary result only: `READY`, `NOT_READY`, or `INSUFFICIENT_EVIDENCE` (the last **always** with a reason code). Not a percentage. Not a mastery grade. Student-facing brand remains “What Kwalitec has observed” per the Progression Readiness design; raw enums are founder/internal only. |
| **Uncertainty behaviour** | Thin, incomplete, modality-missing, prerequisite-blocked, or conflicting evidence yields `INSUFFICIENT_EVIDENCE` with an explicit reason code. Never coerce thin evidence into `READY`. Never emit a soft “probably ready” percentage. |
| **May inform** | Informational observation panels; founder/admin diagnostic detail; later, only under a separate decision-wiring brief, bounded educational decisions that explicitly consume Progression Readiness. May contribute **local demonstrated-competence evidence** into a wider Exam Readiness synthesis (see §6), never as a substitute for that synthesis. |
| **Must never control or become** | Must never claim permanent mastery, Estimated Knowledge, or Exam Readiness. Must never silently become today’s mission, recommendation ranking, or sequential curriculum gate until a dedicated decision brief authorizes that wiring. Must never be collapsed into a syllabus-wide percentage. |

**Correct framing:** Demonstrated competence for progression under an authored contract. Local educational gate. Not sitting preparedness.

#### Proven semantic island (do not disturb)

Progression Readiness is a **proven, working semantic island**. Its evaluator, ternary contracts, reason codes, and learner-facing observation posture are owned by [`../progression_readiness/PROGRESSION_READINESS_DESIGN.md`](../progression_readiness/PROGRESSION_READINESS_DESIGN.md).

**Hard protection:** Exam Readiness reconciliation work must **not** touch, reinterpret, rewrite, or merge Progression Readiness into Exam Readiness, regardless of both concepts sharing the word “readiness.” Shared vocabulary is not shared meaning (§6). Do not alter Progression Readiness evaluator behaviour, contracts, or activation posture under an Exam Readiness brief.

---

### 5.3 Exam Readiness

| Field | Contract |
|-------|----------|
| **Question answered** | Given the relevant available evidence for the named sitting (or active exam goal), how prepared is the student becoming across the syllabus as a whole, under honest warrant? |
| **Authoritative source** | This contract §5.3 (stable semantic definition); Educational Constitution Article IV §9 Readiness; LO-07 Exam Readiness. Live calculation ownership remains an unresolved implementation question until a later reconciliation brief; **no live formula is frozen here**. |
| **Permitted inputs** | A synthesis over **relevant available evidence** for the sitting. **Current candidate evidence dimensions** (not a frozen complete formula): (1) **Coverage** posture (Study Progress / exposure across examinable scope); (2) **Pace** relative to remaining calendar and plan context; (3) **Demonstrated evidence** of competence and retention (including, where available, Assessment Evidence, Estimated Knowledge / related estimates, revision maturity, and local Progression Readiness results as contributing local gates). Additional dimensions may be added only by amending this contract; none may be treated as sole warrant. |
| **Forbidden inputs (as sole or decisive warrant)** | Coverage percentage alone; streak alone; calendar proximity alone; a single mission completion; a single weak behavioural signal; Progression Readiness READY on one or a few objectives alone; any one candidate dimension used to mint a high-confidence “ready for the sitting” claim. |
| **Output / state shape** | An explainable preparedness judgement: stage/label and/or provisional estimate, always with warrant disclosure. May include a percentage **only** when the percentage’s provenance chain (§7) is named and its inputs match this semantic definition. Thin warrant must yield not-yet-claimable / uncertain speech, not a theatrical high score. |
| **Uncertainty behaviour** | Thin warrant → “not yet claimable” / refuse confident sitting-preparedness speech (LO-07). Competing engines or unresolved provenance → soften claims (honesty principle 3); do not fake a single reconciled number in speech. Never prophesy pass/fail. |
| **May inform** | Student preparedness narration; advisory / Decision surfaces that consume readiness as posture (not as a silent next-action engine); analytics honesty about sitting preparation. |
| **Must never control or become** | Must never itself schedule Today’s Mission without Decision Hierarchy compliance. Must never become Progression Readiness. Must never become Coverage. Must never become a pass guarantee. Must never be redefined as “coverage %” or “days studied.” |

**Correct framing (stable, abstract):** Exam Readiness is a **whole-syllabus synthesis judgement** of sitting preparedness based on **relevant available evidence**.  

**Not frozen here:** The exact weights, engines, or closed-form combination of today’s candidate dimensions. Those remain reconciliation work. Naming coverage, pace, and demonstrated evidence as **current candidates** records today’s best-grounded dimensions without pretending the formula is complete.

#### Current operational status (Phase 3 decision: live)

| Field | Status |
|-------|--------|
| **Semantic definition** | **Valid**: §5.3 and LO-07 remain authoritative meaning. |
| **Evidence architecture** | **Incomplete**: still being reconciled across competing engines; no live formula is frozen as canonical. |
| **Learner-facing numerical claim** | **Withheld**: student surfaces must show an honest “not yet assessable” state (enough reliable evidence is not yet available for this estimate). Must never be read as “you are unprepared.” Coverage alone must never mint a confident Exam Readiness percentage. |
| **Current decision authority** | **None**: no live engine (`get_overall_readiness`, revoked `calculate_readiness`, Twin estimator display, forecast, or coverage-renamed readiness) may authorise a student-facing Exam Readiness number or sitting-preparedness decision until reconciliation lands. |

This status preserves the concept while stating where implementation honestly stands. It does **not** choose a canonical coverage implementation.

---

### 5.4 Streak

| Field | Contract |
|-------|----------|
| **Question answered** | How many consecutive learner-local calendar days has the student recorded at least one qualifying study day? |
| **Authoritative source** | This contract §5.4; ADR-007 (engagement must not rewrite educational decisions); live Honest Progress / learner-progress qualifying-day definition (Educational+ observation with Twin-admissible validation, dated on the learner profile timezone). |
| **Permitted inputs** | Qualifying study-day events under the canonical learner-progress rules: at least one Educational+ observation with `may_update_twin=True` on a learner-local calendar day; consecutive-day counting ending on `as_of` or the prior local day per the streak helper’s rules. |
| **Forbidden inputs** | Assessment correctness; Coverage totals; Progression Readiness; Exam Readiness; Estimated Knowledge; “consistency” milestone definitions that count only strong finished sittings (those are a **different** concept and must be labelled as such if shown); raw UTC calendar days that ignore the learner timezone. |
| **Output / state shape** | Non-negative integer day count (current streak), optionally with supporting “qualifying days” context. Not a readiness %. Not a coverage %. |
| **Uncertainty behaviour** | If timezone or qualification evidence is missing, do not invent streak days. If a surface uses a rival streak definition, it must not be labelled as the same Streak concept without disclosing the different rule (or it remains an unresolved claim under honesty principle 3). |
| **May inform** | Engagement / continuity narration; habit reflection; motivational presentation that stays honest about what was counted. |
| **Must never control or become** | Must never control Coverage, Progression Readiness, Exam Readiness, recommendations, or mission selection. Must never be presented as proof of understanding, mastery, or sitting preparedness. Must never rewrite educational decisions (ADR-007). |

**Correct framing:** Streak = consecutive qualifying study days on the learner’s own local calendar. Streak ≠ Consistency-as-educational-quality, and Streak ≠ readiness.

---

## 6. Evidence hierarchy: Progression Readiness and Exam Readiness

Progression Readiness and Exam Readiness are **related by evidence hierarchy**, not identical and not unrelated.

```
Local Assessment Evidence
        │
        ▼
Progression Readiness (per-objective gate)
  READY / NOT_READY / INSUFFICIENT_EVIDENCE
        │
        │  may contribute as local demonstrated-competence evidence
        │  never sufficient alone for sitting preparedness
        ▼
Exam Readiness (whole-syllabus synthesis judgement)
  preparedness posture under honest warrant
```

| Rule | Statement |
|------|-----------|
| **Distinct questions** | Progression Readiness asks whether evidence justifies introducing **next material for this objective**. Exam Readiness asks how prepared the student is becoming for the **sitting / exam goal as a whole**. |
| **Grain** | Progression Readiness is local (objective-scoped). Exam Readiness is global (syllabus / sitting-scoped). |
| **Hierarchy** | Local Progression Readiness results may **inform** Exam Readiness as part of demonstrated evidence. Exam Readiness is **never reducible** to one Progression Readiness result, nor to an average of READY flags. |
| **One-way renunciation** | Progression Readiness must not claim Exam Readiness (locked in the Progression Readiness design). Exam Readiness must not silently redefine itself as Progression Readiness. |
| **Shared word, not shared meaning** | Both use “ready.” That lexical overlap is not semantic identity. |

---

## 7. Claim-provenance chain (cross-cutting)

Every student-facing claim about these concepts should be reconstructible as:

1. **Concept**: which of the four (or a clearly named adjacent concept)
2. **Authoritative definition**: which contract / design section defines it
3. **Source evidence**: which observations or state records were read
4. **Calculation / interpretation**: which rule or synthesis turned evidence into a result
5. **Claim**: what was shown to the student (number, label, or sentence)

If any link cannot be named, the claim’s provenance is **unresolved**. Unresolved provenance requires softened speech (honesty principle 3), not silent confidence.

### 7.1 Worked example: Coverage chain

| Link | Illustration |
|------|----------------|
| **Concept** | Coverage |
| **Authoritative definition** | §5.1; Constitution Study Progress (“honest coverage… without claiming competence”) |
| **Source evidence** | Verified Study Progress completions for syllabus units in the active curriculum context |
| **Calculation / interpretation** | Count completed verified units ÷ explicit syllabus denominator (honesty path) |
| **Claim** | “You have covered N of M syllabus topics” (exposure narration) |

A Coverage claim that instead used Exam Readiness % or Estimated Knowledge as its “calculation” link would be a **provenance failure**, even if the number looked tidy.

### 7.2 Worked example: Exam Readiness chain

| Link | Illustration |
|------|----------------|
| **Concept** | Exam Readiness |
| **Authoritative definition** | §5.3; Constitution Readiness; LO-07 (“Are we honestly ready for this sitting?”) |
| **Source evidence** | Relevant available evidence for the sitting: at minimum the current candidate dimensions (coverage posture, pace/calendar context, demonstrated evidence), each drawn from its lawful sources |
| **Calculation / interpretation** | Whole-syllabus **synthesis judgement** over those dimensions under honest warrant. Exact live engine/weights are **not** frozen by this contract; the chain must still name which engine ran |
| **Claim** | “Preparation looks provisional / credible / not yet claimable for [sitting] because [named warrant],” never “You’re ready” from coverage % or streak alone |

An Exam Readiness claim whose calculation link is “coverage percentage only,” or whose source evidence cannot be named because multiple engines disagree without disclosure, is a **provenance failure**.

---

## 8. Observation / interpretation / judgement (three layers)

Educational speech and evaluators must distinguish three layers. Collapsing them produces false certainty.

| Layer | Meaning | Allowed confidence |
|-------|---------|--------------------|
| **Observation** | What was recorded (attempt outcome, completion event, qualifying study day) | High when the record exists; absent when it does not |
| **Interpretation** | What the observation means under an authored rule or model | Only as strong as the rule and the sample |
| **Judgement** | What the product is willing to claim for a decision or student narrative | Must refuse or soften when interpretation warrant is thin |

### 8.1 Worked example: Progression Readiness

| Layer | Illustration |
|-------|----------------|
| **Observation** | Student scored correct on 2 of 3 contracted items for objective `CS1-A-T01-LO01`; no critical misconception selected. |
| **Interpretation** | Under the authored 3-item conceptual contract (`ready_min_correct=2`), the evidence pattern maps to `READY`. |
| **Judgement** | Kwalitec may say the available evidence meets the progression requirement for **this objective** (informational panel). It must **not** judge Exam Readiness, mastery permanence, or “ready for the sitting” from this local result. |

If only 1 of 3 items is scored correct, interpretation yields `INSUFFICIENT_EVIDENCE` (`INSUFFICIENT_SAMPLE`). Judgement must refuse READY/NOT_READY theatre and say more evidence is needed.

### 8.2 Worked example: Exam Readiness

| Layer | Illustration |
|-------|----------------|
| **Observation** | Student has high verified Coverage; pace is on track vs exam date; demonstrated evidence is thin on many objectives (few scored assessments; many Progression results still `INSUFFICIENT_EVIDENCE`). |
| **Interpretation** | Coverage and pace candidate dimensions look strong; demonstrated-evidence candidate dimension is weak. |
| **Judgement** | Exam Readiness must **not** mint a high-confidence sitting-preparedness claim from coverage and pace alone. Lawful judgement is provisional / not yet claimable until demonstrated evidence warrants synthesis, or speech must explicitly bound confidence to what the weak dimension allows. |

---

## 9. Cross-concept invariants (testable)

These invariants are semantic acceptance tests for later implementation reconciliation. A compliant system must be able to exhibit (or must not forbid) the states below.

| ID | Invariant | Testable reading |
|----|-----------|------------------|
| **INV-01** | High Coverage does not imply high Progression Readiness. | A learner can have high verified Study Progress coverage while Progression Readiness remains `NOT_READY` or `INSUFFICIENT_EVIDENCE` on objectives whose Assessment Evidence fails or is thin. |
| **INV-02** | High Progression Readiness does not imply high Exam Readiness. | A learner can be `READY` on one or several locked objectives while Exam Readiness remains low or not-yet-claimable because syllabus-wide demonstrated evidence, coverage, or pace still fail honest warrant. |
| **INV-03** | High Exam Readiness does not imply Progression Readiness `READY` on every objective. | Global sitting preparedness may be provisional/credible while specific objectives remain `NOT_READY` or `INSUFFICIENT_EVIDENCE`; local gaps must remain speakable. |
| **INV-04** | High Streak does not imply high Coverage. | A learner can record many consecutive qualifying study days while completing few syllabus units (repetition, shallow sessions, or revisiting without Study Progress advancement). |
| **INV-05** | High Streak does not imply high Exam Readiness. | A long streak alone must never force a high Exam Readiness judgement or “ready for the sitting” claim. |
| **INV-06** | High Coverage does not imply high Exam Readiness. | Coverage is a candidate dimension only; without demonstrated evidence (and honest synthesis), Exam Readiness must refuse confident sitting-preparedness claims. |
| **INV-07** | Progression Readiness is not a percentage and is not Exam Readiness. | No compliant mapping may replace the ternary Progression result with an Exam Readiness % or treat them as aliases. |
| **INV-08** | Streak must not rewrite Coverage, Progression Readiness, or Exam Readiness. | Changing streak count alone, with other evidence held fixed, must not change Coverage totals, Progression results, or Exam Readiness judgements. |
| **INV-09** | Thin evidence prefers refusal over confident invention. | For Progression Readiness, thin evidence → `INSUFFICIENT_EVIDENCE` + reason. For Exam Readiness, thin warrant → not-yet-claimable / softened speech. For Coverage and Streak, missing verification → do not invent completed units or streak days. |
| **INV-10** | One weak signal must not alone mint a confident claim. | Holding all other inputs empty/thin, none of: coverage-only, streak-only, calendar-proximity-only, or single soft behavioural signal may produce high Exam Readiness or Progression `READY`. |
| **INV-11** | Absence of stronger coverage evidence must not erase weaker but valid historical exposure. | A learner with accepted LEGACY_COMPLETION and no VERIFIED_COMPLETION remains HISTORICALLY_COMPLETED for that canonical topic; missing verified Runtime C evidence alone must not force NOT_COVERED when legacy acceptance is met. |

---

## 10. Reconciliation posture (explicit non-goals of this document)

This locked contract deliberately does **not**:

1. Choose among competing live Exam Readiness engines or freeze weights for coverage / pace / demonstrated evidence.
2. Change student-facing copy, templates, or CSS.
3. Wire Progression Readiness into the Decision Engine.
4. Merge rival streak definitions (Honest Progress vs export Engine B vs consistency milestones).
5. Amend the Educational Constitution or LO-07 text.
6. Restate or revise per-objective Progression Readiness contracts (owned by the Progression Readiness design).

Later phases reconcile implementations **toward** this contract. They do not redefine these meanings casually in code comments.

---

**Phase 3 operational follow-through (separate from the original lock of this document):** Learner-facing Exam Readiness percentages are withheld; `calculate_readiness` is revoked as Exam Readiness authority; Progression Readiness remains an untouched semantic island. Coverage engine choice remains deferred.

## 11. Quick reference

| Concept | Question (short) | Grain | Primary shape | Must not become |
|---------|------------------|-------|---------------|-----------------|
| **Coverage** | What have I honestly studied? | Syllabus units | Completed counts / % | Mastery / readiness |
| **Progression Readiness** | May next material be introduced for this objective? | Per objective | READY / NOT_READY / INSUFFICIENT_EVIDENCE | Exam Readiness / % |
| **Exam Readiness** | How prepared am I becoming for this sitting? | Whole syllabus / sitting | Synthesis judgement (provisional) | Mission engine / pass guarantee |
| **Streak** | How many consecutive qualifying study days? | Learner-local days | Integer day count | Educational decision authority |

---

## 12. Document control

| Item | Value |
|------|-------|
| **Location rationale** | Locked product semantic designs live under `knowledge/product/<topic>/`, beside [`../progression_readiness/`](../progression_readiness/) and [`../numeric_assessment/`](../numeric_assessment/). ADRs record architecture decisions; they are not the home for this four-concept semantic contract. |
| **Amendments** | Require an explicit documentation brief. Formula or display reconciliation requires a separate implementation brief that cites this contract. |
| **Companion** | Progression Readiness evaluator detail: [`../progression_readiness/PROGRESSION_READINESS_DESIGN.md`](../progression_readiness/PROGRESSION_READINESS_DESIGN.md) |
