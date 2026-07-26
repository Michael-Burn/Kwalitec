# Planning Decision Model

**Programme:** VI — Master Planner  
**Milestone:** MS001 — Educational Planning Model  
**Classification:** Educational decision catalogue for long-term study plans  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document catalogues educational decisions an expert IFoA tutor makes when designing a long-term study plan, and classifies each as **mandatory**, **adaptive**, or **forbidden**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_PLANNING_MODEL.md`
3. `PLANNING_OBJECTIVES.md`
4. `PLANNING_CONSTRAINTS.md`

---

## 1. Purpose

Future planning algorithms must implement decisions from this catalogue — not invent parallel educational meanings in code.

For each decision:

- **What** is decided
- **Why** it exists educationally
- **Class** (mandatory / adaptive / forbidden)
- **Inputs that lawfully influence it**
- **Explainability obligation** (summary; detail in `PLANNING_EXPLAINABILITY.md`)

---

## 2. Decision Classes

| Class | Rule for algorithms |
|-------|---------------------|
| **Mandatory** | Must be made for every complete plan; fixed educational policy with limited parameterisation |
| **Adaptive** | May vary within constraint bounds using lawful inputs and evidence |
| **Forbidden** | Must never appear as a planning output or silent side effect |

---

## 3. Mandatory Decisions

### D1 — Examination & sitting anchor

| Aspect | Specification |
|--------|----------------|
| **What** | Bind the plan to one official examination/subject and one sitting/target date |
| **Why** | Without a syllabus spine and deadline, “planning” is calendar decoration |
| **Class** | Mandatory |
| **Inputs** | Examination, sitting date, supported-subject status |
| **Explain** | “This plan prepares you for {exam} on {date}.” |

### D2 — Topic sequencing policy

| Aspect | Specification |
|--------|----------------|
| **What** | Establish the ordered first-pass learning sequence from official curriculum traversal and prerequisites |
| **Why** | Learning is normally sequential; foundations enable later topics |
| **Class** | Mandatory |
| **Inputs** | Curriculum structure (V1/V2), prerequisite relationships, current Study Progress |
| **Explain** | “You study topics in official syllabus order so later material builds on earlier foundations.” |

### D3 — Starting coverage position

| Aspect | Specification |
|--------|----------------|
| **What** | Begin first-pass allocation from the student’s lawful current syllabus progress — do not re-teach completed coverage as if new without educational reason |
| **Why** | Continuity and respect for honest prior work |
| **Class** | Mandatory |
| **Inputs** | Study Progress / Learning Progress context; prior plan history |
| **Explain** | “We start from where you have already completed studying.” |

### D4 — Capacity envelope

| Aspect | Specification |
|--------|----------------|
| **What** | Compute the educationally usable study capacity to the exam after leave, working schedule, and mandatory phase reservations |
| **Why** | Feasibility is the tutor’s first honesty check |
| **Class** | Mandatory |
| **Inputs** | Weekly time, study-day pattern, leave, exam date |
| **Explain** | “Given your available hours and leave, this is the study capacity we can lawfully use.” |

### D5 — Revision window reservation

| Aspect | Specification |
|--------|----------------|
| **What** | Reserve a protected revision period before the sitting before packing first-pass density |
| **Why** | Retention and exam readiness require consolidation time (O5, C10) |
| **Class** | Mandatory |
| **Inputs** | Exam date, syllabus size, available capacity, revision expectations |
| **Explain** | “Revision is reserved before the exam so first-pass learning does not consume it.” |

### D6 — First-pass vs revision phase boundary

| Aspect | Specification |
|--------|----------------|
| **What** | Define when the journey shifts educational posture from Learning Mode first-pass to Revision Mode emphasis |
| **Why** | Students need a clear educational change of mission — not silent topic hopping |
| **Class** | Mandatory |
| **Inputs** | Reserved revision start, coverage status, exam proximity |
| **Explain** | “From {date}, the plan prioritises consolidating what you have studied.” |

### D7 — Sustainable intensity band

| Aspect | Specification |
|--------|----------------|
| **What** | Set a default daily/weekly intensity ceiling inside declared available time |
| **Why** | Prevents burnout and impossible days (O4, C1–C5) |
| **Class** | Mandatory (band exists); exact minutes within band may be adaptive |
| **Inputs** | Available time, preferences, burnout history if known |
| **Explain** | “Daily study stays within a sustainable range so you can keep the plan.” |

### D8 — Feasibility judgement

| Aspect | Specification |
|--------|----------------|
| **What** | Explicitly judge whether remaining syllabus work + revision + recovery fit capacity; surface infeasibility when they do not |
| **Why** | Expert tutors refuse fantasy schedules (O8, C18) |
| **Class** | Mandatory |
| **Inputs** | Capacity envelope, remaining topics, phase reservations |
| **Explain** | Either “This sitting fits your hours” or “This sitting is not feasible without changing hours, scope, or sitting — here are lawful options.” |

### D9 — Explainability attachment

| Aspect | Specification |
|--------|----------------|
| **What** | Attach plain-language educational reasons to material plan features |
| **Why** | Trust precedes optimisation; silent steering is forbidden |
| **Class** | Mandatory |
| **Inputs** | Decision codes / rationale keys from this catalogue |
| **Explain** | Itself the explainability layer |

---

## 4. Adaptive Decisions

Adaptive decisions vary **within** constraints. They never authorise forbidden behaviours.

### D10 — Study intensity within the safe band

| Aspect | Specification |
|--------|----------------|
| **What** | Raise or lower planned minutes/session density inside the sustainable band |
| **Why** | Match remaining work and evidence of adherence without breaking burnout constraints |
| **Class** | Adaptive |
| **Lawful drivers** | Time pressure, missed weeks, student preference, recovery needs |
| **Unlawful drivers** | Opaque score maximisation; punishment for honesty about missed study |

### D11 — Consolidation / spaced return density

| Aspect | Specification |
|--------|----------------|
| **What** | How often and how heavily to interleave return to recent topics during first pass |
| **Why** | Protects retention on long syllabuses without abandoning sequence |
| **Class** | Adaptive |
| **Lawful drivers** | Syllabus length, evidence of forgetting/weak recall estimates, available capacity |

### D12 — Buffer allocation

| Aspect | Specification |
|--------|----------------|
| **What** | Place spare days/hours for slip, illness, and replan |
| **Why** | Real candidates interrupt; buffers make recovery educationally possible (O6) |
| **Class** | Adaptive (amount); non-zero buffer policy is strongly expected when horizon allows |
| **Lawful drivers** | Horizon length, historical interruptions, leave uncertainty |

### D13 — Recovery allowance after dense work or mocks

| Aspect | Specification |
|--------|----------------|
| **What** | Schedule lighter load after high-intensity blocks or exam simulations |
| **Why** | Learning from mocks and dense study requires cognitive recovery |
| **Class** | Adaptive |
| **Lawful drivers** | Mock placement, intensity peaks, burnout signals |

### D14 — Milestone placement

| Aspect | Specification |
|--------|----------------|
| **What** | Place educational checkpoints (e.g. section coverage complete, revision start, final approach) |
| **Why** | Makes progress legible and supports earned confidence (O7) |
| **Class** | Adaptive in calendar position; milestones themselves are educationally expected |
| **Lawful drivers** | Curriculum structure, phase boundaries, student preference for checkpoint granularity |

### D15 — Mock timing

| Aspect | Specification |
|--------|----------------|
| **What** | Choose when timed exam simulations occur |
| **Why** | Build exam craft when coverage makes the exercise meaningful; leave recovery and final revision |
| **Class** | Adaptive within C11 |
| **Lawful drivers** | Coverage progress, exam date, preference windows, previous attempt history |

### D16 — Revision emphasis mix

| Aspect | Specification |
|--------|----------------|
| **What** | Within revision, allocate attention across topics (breadth vs weak-area depth) |
| **Why** | Evidence-backed weak areas deserve more return; untouched topics still need coverage honesty |
| **Class** | Adaptive |
| **Lawful drivers** | Evidence-backed estimates, declared weaknesses, mock outcomes, remaining revision capacity |
| **Guard** | Must label estimates; must not invent cold-start diagnosis as fact |

### D17 — Rest periods

| Aspect | Specification |
|--------|----------------|
| **What** | Planned light or zero-study days beyond declared leave |
| **Why** | Sustainability and cognitive freshness; prevents seven-day grind as default |
| **Class** | Adaptive |
| **Lawful drivers** | Working schedule, intensity, student preference, burnout prevention |

### D18 — Catch-up / compression response

| Aspect | Specification |
|--------|----------------|
| **What** | After missed study, choose among: use buffers, reduce intensity elsewhere, defer low-priority consolidation, escalate infeasibility — not silent impossible compression |
| **Why** | Recovery that still counts (O6) without violating C1/C10/C18 |
| **Class** | Adaptive choice among lawful options; heroic compression as default is forbidden |
| **Lawful drivers** | Remaining capacity, buffers left, phase proximity to exam |

### D19 — Preference fit

| Aspect | Specification |
|--------|----------------|
| **What** | Align session shape and timing with study preferences |
| **Why** | Adherence improves when lawful preferences are honoured |
| **Class** | Adaptive |
| **Guard** | Preferences yield to constraints and sequencing law |

### D20 — Previous-attempt risk posture

| Aspect | Specification |
|--------|----------------|
| **What** | Increase revision/mock emphasis and feasibility caution after prior unsuccessful attempts |
| **Why** | Repeat sitters need more consolidation and honesty about time — not more false coverage speed |
| **Class** | Adaptive |
| **Lawful drivers** | Previous attempts history, evidence of persistent weak areas |

---

## 5. Forbidden Decisions

These must never be produced.

### F1 — Impossible daily or weekly load

Scheduling more than available time (or beyond sustainable cognitive limits) as the primary plan.

### F2 — Consume protected revision for first-pass by default

“Borrowing” the revision window to finish learning without surfacing a feasibility crisis and student-visible trade-off.

### F3 — Silent prerequisite skipping

Placing advanced topics as primary learning before foundations without constitutional mode disclosure.

### F4 — Random or engagement-driven reordering

Shuffling syllabus order for variety, gamification, or opaque personalisation.

### F5 — Mastery-by-coverage planning claims

Building or narrating the plan as if completing topics equals mastery or a predicted pass.

### F6 — Invented diagnosis at cold start

Assigning definitive “weak/strong” revision weights without evidence or labelled declaration.

### F7 — Content fabrication

Generating actuarial teaching content, unofficial syllabus substitutes, or mark-scheme inventions as plan substance.

### F8 — Silent Learning Mode commandeering

Replacing Today’s Mission / Current Learning Topic authority with advisory focus without disclosure.

### F9 — Punishment pacing

Increasing load to “discipline” missed days rather than educationally replanning.

### F10 — Hidden infeasibility

Publishing a complete-looking plan that cannot fit remaining capacity.

### F11 — Erasure of learner history via plan ops

Treating plan delete/replace as licence to wipe Study Progress, attempts, or evidence posture.

### F12 — Black-box unexplained schedules

Material week structures with no educational reason the student can understand.

### F13 — Post-exam study counted toward this sitting

Assuming study after the sitting date contributes to this sitting’s readiness.

### F14 — Unsupported-subject complete plans

Issuing full journey plans for subjects lacking official supported syllabus integrity.

---

## 6. Decision Map (Tutor Workflow)

Educational order an expert tutor follows (algorithms should preserve this causality):

```
1. Anchor exam + sitting (D1)
2. Establish capacity & leave (D4, C13)
3. Reserve revision (+ mock/recovery scaffolding) (D5, D15 scaffolding)
4. Determine starting coverage (D3)
5. Fix sequencing policy (D2)
6. Judge feasibility (D8) → if fail, stop or trade-off; do not pack fantasy
7. Allocate first-pass under intensity band (D7, D10)
8. Place consolidation, buffers, rest (D11, D12, D17)
9. Place milestones and mocks (D14, D15)
10. Define revision boundary & emphasis policy (D6, D16)
11. Attach explanations (D9)
12. Only then allow adaptive preference fit (D19)
```

Packing first-pass before steps 3 and 6 is educationally unlawful.

---

## 7. Interaction With Daily Systems

| Planning decision | Downstream educational effect |
|-------------------|-------------------------------|
| Sequencing policy (D2) | Constrains Learning Mode topic advancement |
| Intensity band (D7/D10) | Bounds mission/session duration expectations |
| Revision boundary (D6) | Authorises Revision Mode posture timing |
| Mock timing (D15) | Creates exam-simulation milestones — not pass prophecy |
| Recovery (D13/D18) | Informs lighter missions after disruption |

Planning does not replace mission generation; it sets lawful envelopes.

---

## 8. Cross References

- `PLANNING_OBJECTIVES.md` — why decisions exist
- `PLANNING_CONSTRAINTS.md` — bounds on adaptive decisions
- `PLANNING_ASSUMPTIONS.md` — what decisions may assume
- `PLANNING_EXPLAINABILITY.md` — student-facing justification patterns
