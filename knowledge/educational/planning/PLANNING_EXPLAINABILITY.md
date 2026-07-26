# Planning Explainability

**Programme:** VI — Master Planner  
**Milestone:** MS001 — Educational Planning Model  
**Classification:** Explainability contract for long-term planning decisions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how future planning algorithms must justify recommendations in **plain educational language**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `EDUCATIONAL_PLANNING_MODEL.md`
4. `PLANNING_DECISION_MODEL.md`

Planning explainability specialises the platform Explainability Standard for **long-horizon study plan decisions**. It does not weaken claim-type rules (Observed Fact / Derived Fact / Evidence-backed Estimate / Educational Advice).

---

## 1. Purpose

Students should never have to reverse-engineer why their study plan looks the way it does.

If a week is heavy, revision starts on a date, a mock appears, or a sitting is marked infeasible, the student must receive an educational reason they can believe.

> **Explainability improves understanding of planning decisions already authorised.  
> It never invents educational certainty.**

---

## 2. Planning Explainability Principles

1. **Every material planning decision explains itself.** Sequence, intensity, revision, mocks, buffers, and feasibility outcomes are material.
2. **One primary educational reason** per decision surface — not a jargon dump of every internal factor.
3. **Facts and estimates stay distinct.** Coverage and calendar facts are plain; readiness/weakness language is estimated or suggested.
4. **Trade-offs are spoken aloud** when objectives conflict (e.g. revision protected → some first-pass deferred).
5. **Internal machinery stays invisible.** No twin facets, optimiser names, score vectors, or registry IDs in student speech.
6. **Uncertainty is named** when inputs are thin or assumptions are defaults.
7. **Advice does not commandeer Learning Mode** without disclosure.
8. **Infeasibility is a first-class explanation**, not a buried footnote.

---

## 3. Four-Question Contract (Planning)

Every material plan feature must answer:

| # | Question | Planning-specific guidance |
|---|----------|----------------------------|
| 1 | **What** is planned? | Concrete educational action or structure (topic window, phase, intensity, mock) |
| 2 | **Why** educationally? | One primary reason tied to objectives/constraints (readiness, retention, sustainability, prerequisites, revision protection) |
| 3 | **What next** if I follow it? | Clear forward consequence (e.g. “keeps revision intact”, “advances first-pass coverage”) |
| 4 | **Known vs estimated?** | Calendar/capacity/coverage vs estimated weakness/readiness |

Optional fifth when relevant:

| # | Question | When required |
|---|----------|---------------|
| 5 | **What changed?** | After replan, missed weeks, date change, or assumption break |

---

## 4. Claim Types in Planning Speech

| Claim type | Planning examples | Student cue |
|------------|-------------------|-------------|
| Observed Fact | Exam date; declared weekly hours; leave dates; topic marked studied | Plain factual language |
| Derived Fact | Syllabus coverage %; days remaining; whether capacity < required hours | Plain derived measure |
| Evidence-backed Estimate | “Estimated weaker on topic X from recent practice” | *Estimated* / *Suggested* |
| Educational Advice | Optional denser consolidation; preferred mock week within lawful window | *Recommended* / *Optional* |

Forbidden speech patterns:

- “You have mastered topic X because it is scheduled complete.”
- “You will pass if you follow this plan.”
- “Our model scored you 0.82 priority.”
- Silent swap of tonight’s mission topic “because the plan says so” without Learning Mode authority/disclosure.

---

## 5. Standard Explanation Patterns

Algorithms should emit rationale codes internally and map them to student language like the patterns below. Exact copy may evolve; educational meaning must not.

### 5.1 Sequencing

**Pattern:**  
“You study topics in the official syllabus order so later material builds on earlier foundations.”

**When used:** D2 mandatory sequencing.  
**Do not say:** “Personalised shuffle for engagement.”

### 5.2 Starting position

**Pattern:**  
“This plan starts from the topics you have already completed studying, so you do not redo finished coverage without reason.”

**When used:** D3.  
**Claim type:** Observed/Derived Fact about Study Progress — not mastery.

### 5.3 Intensity

**Pattern:**  
“Daily study stays around {band} because that fits the hours you said you have and keeps the pace sustainable.”

**When used:** D7/D10.  
**If raised:** explain remaining work or recovery context without punishment framing.

### 5.4 Revision reservation

**Pattern:**  
“Revision time before {exam date} is reserved first. First-pass learning is planned around that window so consolidation is not squeezed out.”

**When used:** D5/D6.  
**Trade-off speech when needed:** “To protect revision, some first-pass topics remain after the learning phase only if capacity allows — otherwise we must change hours, scope, or sitting.”

### 5.5 Retention / consolidation

**Pattern:**  
“Light return to recent topics is included so earlier material is less likely to fade during a long syllabus.”

**When used:** D11.  
**Label:** Educational Advice / plan structure — not proof of retention.

### 5.6 Mock timing

**Pattern:**  
“A timed mock is placed after enough syllabus coverage to make the practice meaningful, with time afterward to learn from it.”

**When used:** D15.  
**Do not say:** “This mock predicts your pass result.”

### 5.7 Buffers and rest

**Pattern:**  
“Spare capacity is left for interruptions and recovery so one missed week does not collapse the plan.”

**When used:** D12/D13/D17.

### 5.8 Feasibility success

**Pattern:**  
“Given your available hours, leave, and the syllabus remaining, this sitting’s plan fits without impossible days.”

**When used:** D8 pass.

### 5.9 Feasibility failure

**Pattern:**  
“With your current hours and the work still required — including protected revision — this sitting is not realistic. Lawful options: increase study time, choose a later sitting, or accept a reduced scope where educationally allowed.”

**When used:** D8 fail / C18.  
**Tone:** Honest, calm, non-shaming.  
**Forbidden:** Publishing the impossible plan anyway with fine print.

### 5.10 Recovery replan

**Pattern:**  
“Because recent study time was lower than planned, the plan uses buffers / reduces intensity / revisits feasibility rather than packing impossible catch-up days.”

**When used:** D18.  
**Fifth question:** what changed.

### 5.11 Weak-area revision emphasis

**Pattern:**  
“Revision gives more time to topics with *estimated* weaker recent practice evidence. This is not the same as saying you have not studied them.”

**When used:** D16 with warrant.  
**Cold start:** do not use diagnostic weak-area speech; use uniform consolidation language.

### 5.12 Previous attempts

**Pattern:**  
“Because you have sat this exam before, the plan keeps stronger revision and mock emphasis and stays cautious about time.”

**When used:** D20.  
**Do not say:** “You failed because of X” without evidence warrant.

### 5.13 Preference fit

**Pattern:**  
“Session timing follows your preference where it still respects syllabus order and your available hours.”

**When used:** D19.  
**If preference refused:** explain the winning constraint.

### 5.14 Default / thin input

**Pattern:**  
“Some details used cautious defaults because {input} was not provided yet. You can improve the plan by adding that information.”

**When used:** cold-start defaults in `PLANNING_ASSUMPTIONS.md`.

---

## 6. Surface Contracts

### 6.1 Plan overview

Must explain:

- exam + sitting anchor;
- phase structure (learning → revision → final approach);
- capacity basis (hours/leave);
- feasibility posture.

### 6.2 Week or phase view

Must explain:

- why these topics/windows appear now (sequence + phase);
- intensity reason;
- any consolidation/mock/rest markers.

### 6.3 Replan / change events

Must explain:

- what changed (inputs or adherence);
- what decision class applied (recovery vs feasibility escalation);
- what still counts (continuity of Study Progress).

### 6.4 Infeasibility / trade-off UX

Must present lawful options as educational choices, not technical errors.

---

## 7. Good vs Bad Examples

### Good

> “Revision starts four weeks before the sitting. That window was reserved first so first-pass learning cannot quietly consume it.”

> “Tuesday is lighter after the mock so you can review mistakes without starting a new dense topic the same day.”

> “This sitting does not fit 6 hours/week with your remaining syllabus and protected revision. A later sitting or more weekly hours would be required.”

### Bad

> “Optimiser v3 allocated block weights using priority vector π.”

> “You have mastered Chapters 1–8 according to the plan.”

> “Catch up by doing 10-hour days for two weeks.” (unless student explicitly accepts a disclosed exceptional overload — still generally forbidden as default planning)

> “We’re switching tonight’s mission off syllabus order for engagement.” (silent/unlawful)

---

## 8. Algorithm Implementation Obligations (Non-Code Spec)

Future planning algorithms must:

1. Attach a **primary rationale key** to each material output element.
2. Map keys to student-facing patterns that obey claim types.
3. Prefer one reason; allow a single secondary trade-off clause when conflicts were resolved by `PLANNING_OBJECTIVES.md` order.
4. Pass explainability review before student release (Educational Explainability Standard Categories for speech).
5. Never treat missing explanation as acceptable if the decision is material.

MS001 does not implement these mechanisms — it binds them educationally.

---

## 9. Cross References

- `../EDUCATIONAL_EXPLAINABILITY_STANDARD.md` — platform speech law
- `PLANNING_DECISION_MODEL.md` — decisions requiring explanations
- `PLANNING_OBJECTIVES.md` — conflict language source
- `PLANNING_CONSTRAINTS.md` — constraint-refusal explanations
- `PLANNING_ASSUMPTIONS.md` — default and assumption-break speech
