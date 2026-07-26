# Scheduling Explainability

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Explainability contract for Study Timetable placement and changes  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how **calendar placement and rescheduling** must be explained in **plain language**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `SCHEDULING_ENGINE.md`
4. `../planning_blueprint/BLUEPRINT_EXPLAINABILITY.md`
5. `../planning_engine/DECISION_EXPLAINABILITY.md`
6. `../planning/PLANNING_EXPLAINABILITY.md`
7. `SCHEDULING_RULES.md`
8. `RESCHEDULING_POLICY.md`

This document **carries blueprint explainability forward into timetable speech**. It does not invent educational certainty, and it does not weaken claim-type rules (Observed Fact / Derived Fact / Evidence-backed Estimate / Educational Advice).

> **Explainability improves understanding of placement already authorised by the Planning Blueprint.  
> It never invents educational reasoning or readiness claims.**

---

## 1. Purpose

Students should understand:

1. **why sessions appear on particular days and times,**
2. **why revision, buffers, and recovery sit where they do,**
3. **why the timetable changes after missed study, leave, illness, or extra time.**

Silent calendar theatre is forbidden. Opaque “optimisation” speech is forbidden.

---

## 2. Traceability Obligation (Architectural)

Every material session and every material timetable change must be traceable to the Planning Blueprint, which already traces to:

| Trace link | Student-facing role |
|------------|---------------------|
| **Student Educational Profile** | “Given where you are now…” (inherited; not re-diagnosed in packing) |
| **Educational Strategy** | “Under this approach…” (inherited) |
| **Educational Planning Model** | “Because a lawful plan must…” (inherited) |
| **Planning Decision Package** | “We decided…” (inherited) |
| **Planning Blueprint** | “Your journey is structured as…” |
| **Scheduling allocation** | “So this work sits on your calendar as…” |

Internal IDs (SR-XX, SC-XX, RD-XX, BP-XX, BC-XX, PD-XX) may exist for algorithms and audits. They must not appear as student-facing jargon.

A session with no blueprint warrant is invalid — even if the calendar cell was convenient.

---

## 3. Explainability Principles

1. **Placement speaks.** Day, duration, phase emphasis, revision protection, buffers, recovery, and overflow are material.
2. **One primary reason** per surface — not a dump of every constraint ID.
3. **Separate educational why from calendar why.** Educational mission comes from the blueprint; calendar seat comes from availability, leave, holidays, and protection rules.
4. **Carry blueprint speech forward.** Prefer existing journey explainability; add only placement/change reasons.
5. **Facts and estimates stay distinct.** Available hours, leave, and exam date are plain facts; readiness language stays estimated or advisory.
6. **Trade-offs are spoken aloud** when buffer use, deferred consolidation, or escalation was required.
7. **Internal machinery stays invisible.** No optimiser names, score vectors, twin facets, or registry IDs in student speech.
8. **Uncertainty is named** when capacity inputs used defaults or were thin.
9. **Advice does not commandeer Learning Mode** without disclosure.
10. **Infeasibility / overflow is first-class speech.**
11. **Readiness language stays honest.** A dense calendar does not claim the student will pass.
12. **Changes answer “what changed?”** after rescheduling.

---

## 4. Placement Four-Question Contract

For the timetable as a whole, and for each material session or region, answer:

| # | Question | Guidance |
|---|----------|----------|
| 1 | **What** is scheduled? | Concrete work (e.g. “first-pass learning on [topics]”, “protected revision”, “recovery week”) |
| 2 | **Why** does this work exist educationally? | One primary reason carried from blueprint / package explainability |
| 3 | **Why here on the calendar?** | Availability, leave/holiday avoidance, revision/buffer protection, session preference, weekly envelope |
| 4 | **How does this help exam readiness?** | Honest contribution (coverage, retention, application, craft, freshness) — not pass probability |

Optional fifth when relevant:

| # | Question | When required |
|---|----------|---------------|
| 5 | **What changed?** | After rescheduling, buffer use, recovery insertion, overflow disclosure, or re-allocation |

---

## 5. Calendar-Why Catalogue (Allocation Speech)

Use these as primary *calendar* reasons. They do not replace educational why.

| Situation | Plain-language pattern |
|-----------|------------------------|
| Preferred window | “This sits on Tuesday evening because that is when you said you can study.” |
| Earlier tie-break | “Both evenings worked; we placed it on the earlier available night to keep your week steady.” |
| Contiguity | “We kept this next to yesterday’s learning block so the topic continues cleanly.” |
| Rest day | “Friday is kept light/empty so you have a planned rest day.” |
| Leave | “Nothing is scheduled that week because you marked leave.” |
| Holiday | “This holiday is treated as unavailable unless you choose to study then.” |
| Revision protected | “These weeks are reserved for revision — we did not fill them with unfinished first-pass by default.” |
| Buffer held | “Some spare time is kept free for slip, illness, or catch-up without breaking the plan.” |
| Recovery | “After the mock / illness, this lighter stretch is intentional recovery — not lost ambition.” |
| Envelope | “We stopped at this duration so the day stays inside a sustainable load.” |
| Overflow | “Some planned work could not fit in the remaining time without breaking revision or overload rules — we need an honest replan.” |
| Extra time | “You gained an evening; we used it for the next authorised topic — not for inventing extra syllabus.” |
| Missed session move | “We moved the missed work into spare/buffer time so your topic order stays intact.” |

---

## 6. Educational-Why Inheritance

Do not invent new educational speeches at scheduling layer. Inherit and briefly restate:

| Blueprint feature | Inherited speech direction |
|-------------------|----------------------------|
| BP-01 learning | Building syllabus coverage in official order |
| BP-02 practice | Applying material already studied |
| BP-03 consolidation | Returning briefly so retention does not collapse |
| BP-04 revision | Consolidating under revision emphasis before the sitting |
| BP-05 mock | Rehearsing exam craft — not predicting a pass |
| BP-06 final | Stabilising focus and freshness; freezing expansion |
| BP-07 recovery | Restarting sustainably after interruption |

Detail patterns: `../planning_blueprint/BLUEPRINT_EXPLAINABILITY.md`.

---

## 7. Rescheduling Explainability Contract

Every material timetable change must answer:

| # | Question | Guidance |
|---|----------|----------|
| 1 | **What** changed on the calendar? | Which sessions moved, shortened, emptied, or were added |
| 2 | **What** practical event caused it? | Missed sessions, reduced hours, leave, illness, extra time, holiday correction |
| 3 | **What** did we preserve? | Topic order, revision protection, sustainable load, buffers used vs held |
| 4 | **What** did we refuse? | Punishment catch-up, revision theft, packing into leave — when relevant |
| 5 | **What** happens next? | Continue with adjusted timetable **or** escalate to replan (spoken honestly) |

### 7.1 Example change speeches

**Missed sessions**

> “You missed Tuesday and Wednesday. We kept the same learning order and moved that work into spare time later this week so revision weeks stay protected.”

**Illness**

> “Illness removed two study weeks. We cleared those dates, planned a lighter return week, and used buffer time for what was displaced. We will not double-load evenings to ‘make up’ every hour.”

**Reduced availability**

> “Your available evenings dropped. Sessions are shorter/fewer so load stays realistic. If the remaining syllabus still will not fit, we will replan honestly rather than hide the problem.”

**Extra time**

> “You have an extra evening. We scheduled the next topic already in your plan — we did not invent new work just to fill the gap.”

**Overflow / escalation**

> “There is not enough remaining time to finish first-pass without using your protected revision weeks or overloading your days. That needs a planning conversation — not a silently impossible timetable.”

---

## 8. Surfaces and Depth

| Surface | Depth |
|---------|-------|
| Session card / day view | What + short calendar why (+ educational why one line) |
| Week overview | Pattern rationale (rest days, weekly load, interleave) |
| Journey / phase region | Blueprint educational why + why this calendar span |
| After reschedule notification | Full five-question change contract |
| Overflow / infeasibility banner | Explicit honesty; next step = replan |
| Audit / tutor tooling | Full trace IDs allowed |

Student surfaces prefer plain language. Audit surfaces may show SR/SC/RD/BP/BC/PD identifiers.

---

## 9. Forbidden Speech

| Forbidden | Why |
|-----------|-----|
| “The optimiser decided…” | Machinery speech; hides reasons |
| “You’re behind so revision is cancelled” | Unlawful default; educational theft dressed as help |
| “This packed week means you’re ready” | Calendar density ≠ mastery or pass claim |
| “We added advanced topics because you had a free night” | New educational ambition invented in packing |
| “Make up all missed hours this weekend” | Punishment pacing |
| Silent move with no change notice for material shifts | Breaks trust |
| Fake completeness while overflow exists | Feasibility theatre |

---

## 10. Claim-Type Discipline

| Claim type | Scheduling examples |
|------------|---------------------|
| **Observed Fact** | Declared Tuesday availability; leave dates; exam date; session was missed |
| **Derived Fact** | Weekly residual minutes after leave; session moved into buffer pocket |
| **Evidence-backed Estimate** | Only if inherited from upstream (e.g. weak-area emphasis already decided) — scheduling must not mint new weakness estimates |
| **Educational Advice** | “Keep Friday rest”; “use this extra evening for the next planned topic” |

Scheduling explainability is mostly Observed/Derived Fact about placement, plus inherited Educational Advice from the blueprint — not new diagnosis.

---

## 11. Completeness Rule

A timetable is explainability-incomplete when:

- material sessions lack a calendar why;
- revision/buffer/recovery placement is unexplained;
- rescheduling occurs without answering “what changed?”;
- overflow is hidden;
- educational why invents claims absent from the blueprint.

Incomplete explainability blocks student-facing publication of those elements.

---

## 12. Cross References

- `SCHEDULING_ENGINE.md` — allocation constitution
- `CALENDAR_ALLOCATION.md` — what is being explained geometrically
- `RESCHEDULING_POLICY.md` — change events that require speech
- `../planning_blueprint/BLUEPRINT_EXPLAINABILITY.md` — inherited journey speech
- `../EDUCATIONAL_EXPLAINABILITY_STANDARD.md` — EIP-003 claim discipline
