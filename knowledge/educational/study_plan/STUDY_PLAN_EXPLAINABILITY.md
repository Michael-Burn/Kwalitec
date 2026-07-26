# Study Plan Explainability

**Programme:** VI — Master Planner  
**Milestone:** MS007 — Canonical Study Plan Model  
**Classification:** Explainability contract for completed Canonical Study Plans  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how a **completed Study Plan** must be explained in **plain educational language**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `CANONICAL_STUDY_PLAN.md`
4. `STUDY_PLAN_COMPONENTS.md`
5. `STUDY_PLAN_LIFECYCLE.md`
6. `STUDY_PLAN_VALIDATION.md`
7. `../scheduling/SCHEDULING_EXPLAINABILITY.md`
8. `../planning_blueprint/BLUEPRINT_EXPLAINABILITY.md`
9. `../planning_engine/DECISION_EXPLAINABILITY.md`
10. `../planning/PLANNING_EXPLAINABILITY.md`

This document **carries timetable and blueprint explainability forward into plan-level speech**. It does not invent educational certainty, and it does not weaken claim-type rules (Observed Fact / Derived Fact / Evidence-backed Estimate / Educational Advice).

> **Explainability improves understanding of a plan already authorised by Scheduling Engine output.  
> It never invents educational reasoning or readiness claims.**

---

## 1. Purpose

Students should understand:

1. **why the plan exists,**
2. **why it is structured this way,**
3. **what educational commitments it makes,**
4. **and under what circumstances it will change.**

Silent plan theatre is forbidden. Opaque “optimised for success” speech is forbidden. Calendar density must not be narrated as guaranteed readiness.

---

## 2. Traceability Obligation (Architectural)

Every material plan element and every material lifecycle change must be traceable through:

| Trace link | Student-facing role |
|------------|---------------------|
| **Student Educational Profile** | “Given where you are now…” (inherited; not re-diagnosed at plan layer) |
| **Educational Strategy** | “Under this approach…” (inherited) |
| **Educational Planning Model** | “Because a lawful plan must…” (inherited) |
| **Planning Decision Package** | “We decided…” (inherited) |
| **Planning Blueprint** | “Your journey is structured as…” |
| **Scheduling allocation** | “So this work sits on your calendar as…” |
| **Canonical Study Plan** | “So your Study Plan commits to…” |

Internal IDs (SPC-XX, SPL-XX, SPV-XX, SR-XX, BP-XX, BC-XX, PD-XX) may exist for algorithms and audits. They must not appear as student-facing jargon.

A plan element with no timetable / blueprint warrant is invalid — even if the explanation sounds motivating.

---

## 3. Explainability Principles

1. **The whole plan speaks.** Existence, structure, commitments, and change conditions are all material.
2. **One primary reason** per surface — not a dump of every constraint ID.
3. **Separate educational why from calendar why.** Educational mission comes from blueprint / package; calendar seat comes from availability, leave, holidays, and protection rules.
4. **Carry upstream speech forward.** Prefer existing timetable / blueprint / package explainability; add only plan-contract and lifecycle reasons.
5. **Facts and estimates stay distinct.** Exam date, leave, and scheduled hours are plain facts; readiness language stays estimated or advisory.
6. **Commitments and refusals are both spoken.** Students hear what the plan promises *and* what it refuses to promise.
7. **Trade-offs are spoken aloud** when buffer use, recovery, deferred consolidation, or escalation was required.
8. **Internal machinery stays invisible.** No optimiser names, score vectors, twin facets, or registry IDs in student speech.
9. **Uncertainty is named** when capacity inputs used defaults or evidence was thin.
10. **Advice does not commandeer Learning Mode** without disclosure.
11. **Infeasibility / overflow is first-class speech.**
12. **Readiness language stays honest.** A complete plan does not claim the student will pass.
13. **Lifecycle changes answer “what changed?”** after Adapted / Recovered / Superseded transitions.
14. **Continuity is spoken on replacement.** New plans do not narrate false educational amnesia.

---

## 4. Four-Question Contract (Binding)

For every complete Canonical Study Plan, student-facing narration must be able to answer:

| # | Question | Guidance |
|---|----------|----------|
| 1 | **Why does this plan exist?** | Sitting / examination aim; Profile starting point; strategy chosen; that scheduling seated an approved blueprint |
| 2 | **Why is it structured this way?** | Phase order; protected revision; practice/mocks placement; buffers/recovery; intensity honesty — carried from blueprint + timetable reasons |
| 3 | **What educational commitments does it make?** | SPC-10 promises and refusals in plain language |
| 4 | **Under what circumstances will it change?** | Adaptation after missed study/leave; recovery after illness; escalation / new plan when envelopes no longer fit; supersession on sitting or strategy/blueprint change |

Optional fifth when relevant:

| # | Question | When required |
|---|----------|---------------|
| 5 | **What changed?** | After Adapted, Recovered, Superseded, or material assumption correction |

A plan that cannot answer questions 1–4 fails SPV-12 (`STUDY_PLAN_VALIDATION.md`).

---

## 5. Plan-Level Speech Patterns

### 5.1 Why the plan exists

**Lawful pattern:**

> “You are preparing for [exam] on [sitting]. Given where you are now in the syllabus, and under [strategy in plain words], we built a study journey and placed it on your real calendar. This Study Plan is that journey — the preparation frame to follow.”

**Unlawful patterns:**

- “Our algorithm optimised your pass probability.”
- “This plan guarantees you are exam-ready.”
- “Because the Digital Twin says…”

### 5.2 Why it is structured this way

**Lawful pattern:**

> “First you complete first-pass learning in syllabus order, with practice after topics you have studied. Protected revision sits before the exam — not as leftover weeks. Buffers exist because real life slips. Recovery capacity exists so illness or dense stretches do not become punishment catch-up.”

Carry specific phase/session reasons from `SCHEDULING_EXPLAINABILITY.md` and `BLUEPRINT_EXPLAINABILITY.md` rather than inventing a parallel catalogue.

**Unlawful patterns:**

- Inventing a motivational phase the blueprint never authorised
- Claiming revision is optional leftover
- Narrating rest days as laziness rather than freshness capacity

### 5.3 Educational commitments

**Lawful promises (examples):**

- Follow official syllabus order for first-pass learning under Learning Mode
- Protect the revision window already reserved
- Keep weekly load inside the sustainable envelope you declared capacity for
- Explain material changes when the diary moves
- Escalate honestly if the journey no longer fits remaining time

**Lawful refusals (examples):**

- We do not promise a pass
- Completing scheduled topics is Study Progress — not mastery as fact
- Recommendations may advise; they do not silently replace today’s learning focus
- We will not invent impossible catch-up by consuming protected revision by default

### 5.4 When the plan will change

**Lawful pattern:**

> “If you miss study or your availability changes, we may move sessions and use buffers — same educational journey, adapted dates. After illness, we may use recovery capacity for a lighter stretch. If protected revision or remaining capacity can no longer host the journey, we will say so and rebuild the plan rather than pretend.”

**Unlawful patterns:**

- Silent diary churn with no “what changed?”
- “We’ll just compress everything into the last fortnight”
- “Starting a new plan means starting from zero” (continuity violation)

---

## 6. Component-Level Explainability

Material components inherit upstream speech; plan layer adds contract framing only.

| Component | Student should understand |
|-----------|---------------------------|
| Phase (SPC-01) | What educational job this stretch is doing |
| Milestone (SPC-02) | What honest marker was reached — not pass prophecy |
| Study session (SPC-03) | What to do, why that work exists, why it sits here |
| Revision window (SPC-04) | That revision is protected and why |
| Recovery capacity (SPC-05) | That lighter load is intentional recovery, not failure |
| Checkpoint (SPC-06) | What is being checked, and that it is not mastery fiat |
| Buffer (SPC-07) | That spare capacity exists for slip |
| Assumptions (SPC-09) | What must stay true (hours, leave, exam date, uncertainty) |
| Commitments (SPC-10) | Promises and refusals |
| Overflow record (SPC-16) | What could not be placed, if anything |

Session-level four-question placement speech remains governed by `SCHEDULING_EXPLAINABILITY.md`. Plan explainability must not contradict it.

---

## 7. Lifecycle Explainability

| Transition | Required speech |
|------------|-----------------|
| Draft → Approved | “Your plan is ready — here is why it exists and what it commits to.” |
| Approved → Active | “This plan now guides your daily preparation.” |
| → Adapted | “What changed on the calendar, and that the educational journey is the same.” |
| → Recovered | “Recovery capacity is in use because [illness / dense stretch]; lighter load for a while.” |
| → Completed | “This preparation window has ended” — not “you have passed.” |
| → Superseded | “A new plan replaced this one because [sitting change / replan / new journey]; your study history continues.” |
| → Archived | “Kept for your records — not guiding today.” |

---

## 8. Claim-Type Discipline

| Claim type | Plan speech examples |
|------------|----------------------|
| **Observed Fact** | Exam date; declared study days; leave marked; sessions placed |
| **Derived Fact** | Phase spans from allocated regions; buffer remaining after known slip |
| **Evidence-backed Estimate** | Provisional readiness language only where upstream authorised estimates exist |
| **Educational Advice** | Suggestions within envelopes; never silent mission takeover |

Forbidden collapses:

- Schedule completeness → “you will pass”
- Study Progress → “Mastered”
- Dense calendar → “exam ready” as fact
- Twin / optimiser internals → student-facing certainty

---

## 9. Surfaces and Minimal Contracts

Wherever the Study Plan is narrated to students (overview, roadmap, activation, adaptation notice, archive/supersede notice), the surface must satisfy the Four-Question Contract at plan level, or clearly deep-link to a surface that does.

| Surface | Minimum |
|---------|---------|
| Plan overview | Questions 1–4 |
| Phase / roadmap view | Structure reasons + protections visible |
| Session detail | Scheduling four-question placement speech |
| Adaptation / recovery notice | Question 5 (“what changed?”) + continuity reassurance when relevant |
| Supersede / new plan | Why replaced + history continues |

Operator-only audit surfaces may show IDs; student surfaces must not.

---

## 10. Out of Scope

- Copywriting micro-variants for every UI string
- Marketing claims beyond educational truth
- New educational reasoning disguised as “better explanations”
- Twin or optimiser disclosure in student speech

---

## 11. Success Condition

Explainability is satisfied when a student can read their Canonical Study Plan and honestly answer:

> Why does this plan exist?  
> Why is it structured this way?  
> What does it commit to — and refuse?  
> When will it change?

without encountering silent theatre, pass prophecy, or invented educational meaning.

---

## 12. Cross References

- `CANONICAL_STUDY_PLAN.md` — educational guarantees and required sections
- `STUDY_PLAN_COMPONENTS.md` — what must be speakable
- `STUDY_PLAN_LIFECYCLE.md` — transition speech
- `STUDY_PLAN_VALIDATION.md` — SPV-12 gate
- `../scheduling/SCHEDULING_EXPLAINABILITY.md` — placement speech
- `../planning_blueprint/BLUEPRINT_EXPLAINABILITY.md` — journey structure speech
- `../EDUCATIONAL_EXPLAINABILITY_STANDARD.md` — claim-type law
