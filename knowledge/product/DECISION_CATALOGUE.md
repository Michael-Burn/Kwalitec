# Decision Catalogue

**Programme:** ILE-011 — Student Decision Framework  
**Version:** 1.0  
**Status:** Active — permanent catalogue of major learner decisions  
**Effective:** 2026-07-28  
**Companion:** [`STUDENT_DECISION_FRAMEWORK.md`](STUDENT_DECISION_FRAMEWORK.md)  
**Related:** [`GUIDANCE_RESPONSIBILITY_MATRIX.md`](GUIDANCE_RESPONSIBILITY_MATRIX.md), [`DECISION_CONFIDENCE_MODEL.md`](DECISION_CONFIDENCE_MODEL.md)  

---

## Purpose

Catalogue every **significant learning decision** a student makes across a professional exam journey, and define for each:

- Decision owner  
- Evidence required  
- Confidence threshold  
- Explainability requirement  
- Permitted guidance  
- Forbidden guidance  

This is a product catalogue, not a runtime schema. Future capabilities map to Decision IDs below.

**Confidence threshold values** refer to levels in [`DECISION_CONFIDENCE_MODEL.md`](DECISION_CONFIDENCE_MODEL.md): Observation only · Emerging · Reliable · High · Insufficient.

---

## How to read an entry

| Field | Meaning |
|---|---|
| **Owner** | Who makes the final call (Student / Shared — student confirms Sensei proposal) |
| **Evidence required** | Minimum observations before guidance is lawful |
| **Confidence threshold** | Minimum level for primary guidance (lower levels may allow questions or soft context only) |
| **Explainability** | What the student must be able to learn if guidance is shown |
| **Permitted** | Lawful Sensei behaviours |
| **Forbidden** | Hard exclusions (never do) |

---

## Planning

### D-P01 — Should I create or refresh a study plan?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Exam date (or proxy), available study days/hours, syllabus selection |
| **Confidence threshold** | Emerging (for proposing wizard start); Reliable (for concrete plan structure claims) |
| **Explainability** | Why a plan is needed; what inputs drive allocation; what is still provisional |
| **Permitted** | Prompt to start/refresh wizard; explain exam-date-driven allocation; warn if plan is missing or stale relative to exam |
| **Forbidden** | Invent exam dates; silently overwrite Canonical Study Plan; promise a pass from planning alone |

### D-P02 — How should I allocate study time across the syllabus?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Syllabus structure/weights, exam date, availability, prior coverage if any |
| **Confidence threshold** | Reliable |
| **Explainability** | Why topic A gets more time than B (weight, coverage gap, prerequisites) |
| **Permitted** | Propose weighted allocation; flag under-allocated high-weight topics |
| **Forbidden** | Ignore official syllabus order/weights; allocate based on engagement metrics |

### D-P03 — Should I study today?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Plan/Mission existence, stated availability or recent pattern, workload signals if any |
| **Confidence threshold** | Emerging |
| **Explainability** | Why today matters (plan continuity, exam proximity, recovery) or why rest is coherent |
| **Permitted** | Suggest a proportional session; suggest rest when overload evidenced; clarify Mission existence |
| **Forbidden** | Guilt or streak-punishment; claim catastrophe from one missed day |

### D-P04 — How long should today’s session be?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Stated available time, Mission scope, workload/burnout signals |
| **Confidence threshold** | Emerging |
| **Explainability** | How duration was scoped to available time and priorities |
| **Permitted** | Shorten Mission; propose a minimum viable session; warn if planned effort exceeds availability |
| **Forbidden** | Prescribe marathon sessions against availability; use duration as vanity engagement |

### D-P05 — Should I change my exam date or sitting?

| Field | Value |
|---|---|
| **Owner** | Student |
| **Evidence required** | Pace vs deadline signals (optional support only); student-stated constraints |
| **Confidence threshold** | High (for any strong pacing honesty); else Insufficient → silence or soft readiness context only |
| **Explainability** | What pace/readiness evidence shows — without deciding the sitting |
| **Permitted** | Show pace-risk and coverage honesty; invite student to reconsider plan inputs |
| **Forbidden** | Book/cancel sittings; declare “you must postpone”; financial/career advice about sitting choice |

---

## Learning

### D-L01 — What should I study now?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Plan/Mission or syllabus position, coverage, prerequisites, recent evidence |
| **Confidence threshold** | Reliable (primary “study next”); Emerging (soft alternatives labelled uncertain) |
| **Explainability** | What / why this now / what next / what is uncertain |
| **Permitted** | Single primary next-action recommendation aligned to plan and curriculum |
| **Forbidden** | Competing tip storms; invent topics outside syllabus; replace Mission without labelling advice |

### D-L02 — Should I continue on this topic?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Session progress, check outcomes, time remaining, plan focus |
| **Confidence threshold** | Emerging |
| **Explainability** | Why continue (incomplete loop, thin evidence) or why stop (session done, overload) |
| **Permitted** | Encourage completing authorised focus; suggest stopping when proportional |
| **Forbidden** | Force endless practice for score theatre; interrupt mid-Mission with unrelated tips |

### D-L03 — Should I move on to the next topic?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Coverage of current topic, prerequisite readiness, plan coherence |
| **Confidence threshold** | Reliable |
| **Explainability** | Prerequisites OK / not OK; coverage vs understanding honesty |
| **Permitted** | Recommend progression when lawful; recommend staying when foundation weak |
| **Forbidden** | Advance to inflate coverage; block forever without explainable deficit |

### D-L04 — Should I revisit fundamentals / prerequisites?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Weak prerequisite signals, failed checks with foundation failure modes, curriculum graph |
| **Confidence threshold** | Reliable |
| **Explainability** | Which foundation blocks progress and what evidence shows it |
| **Permitted** | Recovery path to fundamentals; calm challenge of false mastery |
| **Forbidden** | Shame language; send student to unrelated “basics” without warrant |

### D-L05 — Which learning resource should I use now?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Current topic decision, resource type hints if configured; otherwise topic focus only |
| **Confidence threshold** | Emerging |
| **Explainability** | Why this activity type now (read / practice / revise) — not which publisher is “best” |
| **Permitted** | Guide *into* textbooks, notes, videos, past papers as instruments for the current decision |
| **Forbidden** | Replace professional materials; claim Kwalitec content is the syllabus; rank commercial products as endorsements |

---

## Revision

### D-R01 — Should I revise?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Prior study/coverage of the topic; spacing/decay or practice weakness; or exam-window warrant |
| **Confidence threshold** | Reliable |
| **Explainability** | Why revise now (decay, weight, exam proximity, blocker) |
| **Permitted** | Spaced revision recommendations; exam-oriented reinforcement of covered material |
| **Forbidden** | “Revise” topics never studied; revision purely for engagement |

### D-R02 — What should I revise first?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Weakness/spacing signals across studied topics; syllabus weights; exam proximity |
| **Confidence threshold** | Reliable |
| **Explainability** | Ranking rationale among studied topics |
| **Permitted** | Prioritised revision order; proportional slice for today’s time |
| **Forbidden** | Dump entire syllabus as “revise everything”; contradict authorised Mission without labelling |

### D-R03 — Should I re-learn rather than lightly revise?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Fragile or contradictory understanding; recovery warrants |
| **Confidence threshold** | Reliable |
| **Explainability** | Why light revision is insufficient given evidence |
| **Permitted** | Recommend deeper recovery / re-study path |
| **Forbidden** | Inflate severity; prescribe re-learning without evidence of fragility |

---

## Assessment

### D-A01 — Should I attempt a learning check / assessment now?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Recent study on the topic (or explicit readiness check intent); session type policy |
| **Confidence threshold** | Emerging |
| **Explainability** | Purpose of the check (evidence, not exam simulation theatre) |
| **Permitted** | Suggest proportional checks after study; readiness checks when warranted |
| **Forbidden** | Endless question grinding as primary product; imply one check = exam readiness |

### D-A02 — Should I attempt another assessment?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Outcomes of prior check(s); time since last; uncertainty cause |
| **Confidence threshold** | Emerging |
| **Explainability** | Whether another check reduces uncertainty or risks fatigue/overclaim |
| **Permitted** | Suggest later confirmation check; suggest study-first when evidence too thin |
| **Forbidden** | “Keep answering until the score turns green”; treat volume as mastery |

### D-A03 — Am I ready? (topic / module / exam)

| Field | Value |
|---|---|
| **Owner** | Shared (honesty); **Student** owns exam-entry choice |
| **Evidence required** | Coverage, practice evidence, uncertainty, exam proximity, plan pace |
| **Confidence threshold** | Reliable for provisional readiness language; High for strong readiness claims; Insufficient → admit uncertainty |
| **Explainability** | What readiness means here; what evidence supports/limits the claim; what remains unknown |
| **Permitted** | Honest readiness / pass-risk *signals*; provisional labels; next actions that improve evidence |
| **Forbidden** | Guarantee pass/fail; fake precision; override student’s booking choice |

### D-A04 — Should I use past papers / mock conditions now?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Coverage of relevant topics; exam window; prior practice quality |
| **Confidence threshold** | Emerging–Reliable depending on claim strength |
| **Explainability** | Why timed practice now vs topic-focused practice |
| **Permitted** | Recommend past-paper practice for covered, weighted topics; scope to available time |
| **Forbidden** | Claim Kwalitec is the official exam; confuse mocks with certified readiness guarantees |

---

## Reflection

### D-F01 — What did today’s study achieve?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Session/Mission outcomes, attempts, decision journal entries |
| **Confidence threshold** | Emerging |
| **Explainability** | Concrete evidence gained (coverage, checks) vs remaining uncertainty |
| **Permitted** | Reflective summary; Decision Journal visibility; no judgement of worth |
| **Forbidden** | Shame for incomplete sessions; inflate mastery from activity alone |

### D-F02 — Should I accept, defer, or dismiss this recommendation?

| Field | Value |
|---|---|
| **Owner** | Student |
| **Evidence required** | Recommendation + explanation already shown |
| **Confidence threshold** | N/A (student agency always) |
| **Explainability** | Why the tip was offered (already required on the tip itself) |
| **Permitted** | Honour accept/defer/dismiss; learn from journal patterns for future guidance quality |
| **Forbidden** | Punish dismissal; re-nag immediately; hide dismiss |

### D-F03 — How should I interpret a setback (missed day, weak check)?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Specific event + recovery path availability |
| **Confidence threshold** | Emerging |
| **Explainability** | Normalise without denial; show clear recovery action |
| **Permitted** | Reassure with evidence; propose recovery into authorised focus |
| **Forbidden** | Catastrophise; invent “you’re behind forever”; empty praise without path |

---

## Wellbeing

### D-W01 — Should I take a break / slow down?

| Field | Value |
|---|---|
| **Owner** | Shared |
| **Evidence required** | Workload/burnout signals, impossible Mission vs availability, sustained intensity flags |
| **Confidence threshold** | Reliable for strong slow-down recommendation; Emerging for soft pacing tips |
| **Explainability** | What overload evidence was observed; what sustainable alternative looks like |
| **Permitted** | Suggest shorter session, rest day, reduced scope; elevate wellbeing when overload evidenced |
| **Forbidden** | Diagnose medical/mental health conditions; guilt for resting; use breaks as cover to invent unrelated tips |

### D-W02 — Should I push harder / intensify?

| Field | Value |
|---|---|
| **Owner** | Shared (cautious) |
| **Evidence required** | Capacity + exam proximity + clear educational deficit — without overload |
| **Confidence threshold** | High (rare); otherwise Emerging soft “if capacity allows” only |
| **Explainability** | Why intensity is proportional and temporary |
| **Permitted** | Modest intensity within sustainable bounds when evidence supports |
| **Forbidden** | Hustle theatre; streak maximisation; intensity that contradicts burnout signals |

### D-W03 — Should I seek external help (tutor, mentor, peer, provider)?

| Field | Value |
|---|---|
| **Owner** | Student |
| **Evidence required** | Persistent blockers after recovery attempts (optional context) |
| **Confidence threshold** | Emerging (for suggesting *that* human help may help — never whom to hire) |
| **Explainability** | Which educational stuck-point suggests human dialogue may help |
| **Permitted** | Suggest seeking a tutor/teacher for deep explanation; respect existing provider relationships |
| **Forbidden** | Rank commercial tutors; sell leads; claim Kwalitec replaces pastoral care |

---

## Long-term progression

### D-T01 — Am I on pace for the exam?

| Field | Value |
|---|---|
| **Owner** | Shared (signal); Student owns response |
| **Evidence required** | Plan, coverage trajectory, exam date, historical completion rate |
| **Confidence threshold** | Reliable for pace signals; High for strong “at risk” language |
| **Explainability** | Pace assumptions, uncertainty, and adjustable levers (hours, scope, date) |
| **Permitted** | Projected pace and pass-risk *signals*; invite plan refresh |
| **Forbidden** | Destiny claims; “you will fail”; silent plan mutation |

### D-T02 — Should I postpone the exam?

| Field | Value |
|---|---|
| **Owner** | Student only |
| **Evidence required** | Pace/readiness honesty as optional input |
| **Confidence threshold** | Insufficient for Sensei *decision*; High only for presenting stark evidence context if asked |
| **Explainability** | Evidence of pace/readiness — never a booking instruction |
| **Permitted** | Present evidence; ask clarifying questions about constraints; remain silent if evidence thin |
| **Forbidden** | Decide postpone/sit; process exam-body administration; career/financial advice |

### D-T03 — Should I change qualification / career path?

| Field | Value |
|---|---|
| **Owner** | Student only |
| **Evidence required** | N/A for Sensei decision |
| **Confidence threshold** | Insufficient (always out of educational decision scope) |
| **Explainability** | N/A — Silence Principle |
| **Permitted** | None as career advice; may continue educational support for the *current* syllabus if student stays |
| **Forbidden** | Career counselling as product; aptitude stereotypes; “switch exams” recommendations |

### D-T04 — How should I sequence modules / papers across sittings?

| Field | Value |
|---|---|
| **Owner** | Student (primary); Shared only for *within*-syllabus study order of a chosen sitting |
| **Evidence required** | Official syllabus prerequisites for in-scope sequencing; institute rules are student’s domain |
| **Confidence threshold** | Reliable for within-curriculum topic order; Insufficient for multi-year career sequencing |
| **Explainability** | Prerequisite and weight rationale within the loaded curriculum |
| **Permitted** | Guide topic order inside an active plan; note prerequisite blockers |
| **Forbidden** | Prescribe multi-year paper strategy as authoritative; contradict exam-body rules |

### D-T05 — Should I book the exam?

| Field | Value |
|---|---|
| **Owner** | Student only |
| **Evidence required** | Optional readiness/pace context |
| **Confidence threshold** | Insufficient for Sensei decision |
| **Explainability** | Readiness honesty if shown — separate from booking |
| **Permitted** | Show readiness signals when asked; link to student’s own admin process |
| **Forbidden** | Book the exam; treat booking as a Mission task owned by Kwalitec |

---

## Cross-cutting notes

1. **Primary recommendation rule:** At most one primary tip per surface moment, ranked under P-001.3 when multiple catalogue decisions compete.
2. **Mission coherence:** D-L01 / D-R02 must not silently fight Today’s Mission (Responsibility Matrix + P-001.3 Rank 2).
3. **V1/V2 curricula:** Catalogue decisions assume official syllabus traversal via CurriculumService helpers; flat and hierarchical curricula both apply.
4. **Extension:** New Decision IDs may be added in future ILE programmes without changing educational algorithms — until implementation programmes map them to runtime.

---

## Index by group

| Group | IDs |
|---|---|
| Planning | D-P01 … D-P05 |
| Learning | D-L01 … D-L05 |
| Revision | D-R01 … D-R03 |
| Assessment | D-A01 … D-A04 |
| Reflection | D-F01 … D-F03 |
| Wellbeing | D-W01 … D-W03 |
| Long-term progression | D-T01 … D-T05 |

---

**End of DECISION_CATALOGUE**
