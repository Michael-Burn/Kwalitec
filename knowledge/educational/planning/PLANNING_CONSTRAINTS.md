# Planning Constraints

**Programme:** VI — Master Planner  
**Milestone:** MS001 — Educational Planning Model  
**Classification:** Permanent educational constraints for long-term study plans  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **permanent constraints** every long-term study plan must respect.

Constraints are educational law for Master Planner. Soft preferences, heuristics, and optimiser convenience never override them.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_PLANNING_MODEL.md`
3. `PLANNING_OBJECTIVES.md`

---

## 1. Purpose

An expert IFoA tutor will refuse certain plans even if a student asks for them.

These constraints encode that refusal: what a lawful plan must never demand, ignore, or imply.

---

## 2. Constraint Categories

| Category | Meaning |
|----------|---------|
| **Hard** | Violation → plan is educationally invalid |
| **Conditional hard** | Hard whenever the triggering condition exists |
| **Structural** | Hard rules about syllabus and educational meaning |

All constraints below are **Hard** or **Structural** unless marked otherwise.

---

## 3. Capacity & Load Constraints

### C1 — No impossible daily workloads

A plan must not assign more study than a reasonable student can complete in a day given declared available time and cognitive limits.

**Tutor rationale.** Impossible days train abandonment. Overload is not ambition; it is design failure.

### C2 — Respect available study time

Weekly and daily planned load must fit inside the student’s declared available study time (after known leave and working schedule), allowing for the buffers required by recovery and revision constraints.

**Tutor rationale.** Plans that ignore real hours are fiction.

### C3 — Respect working schedule and study-day pattern

Study must be placed on days and times the student can actually use. “Average hours per week” may not silently relocate load onto unavailable days.

**Tutor rationale.** A candidate working long weekdays cannot honestly absorb a plan that assumes five free weekday evenings if they declared none.

### C4 — Avoid excessive cognitive overload

Dense blocks of new high-demand topics must not be stacked without recovery or consolidation allowance beyond sustainable intensity.

**Tutor rationale.** Professional syllabuses punish shallow marathon coverage. Cognitive freshness is an educational resource.

### C5 — Support sustainable study

Across the horizon, intensity must remain consistent with O3/O4 (consistency and burnout prevention). Temporary peaks require compensating recovery.

**Tutor rationale.** Sustainability is a constraint, not a vibe.

---

## 4. Curriculum & Sequencing Constraints

### C6 — Respect official syllabus structure

Planning must use the official curriculum spine (V1 flat or V2 hierarchical) as the organising truth. Ad-hoc topic invention or unofficial reordering as “clever shortcuts” is forbidden.

**Tutor rationale.** Curriculum primacy is constitutional.

### C7 — Respect prerequisite ordering

A topic that educationally depends on earlier foundations must not be scheduled as primary first-pass learning before those foundations are covered (or explicitly waived only under a constitutionally authorised mode disclosed to the student).

**Tutor rationale.** IFoA learning is cumulative. Skipping foundations creates false progress and later collapse.

### C8 — Preserve Learning Mode sequence authority

Long-term plans must not silently commandeer or contradict Current Learning Topic / Learning Mode authority. Adaptive advice may modulate density and timing; it must not secretly replace authorised sequence without disclosure and lawful mode.

**Tutor rationale.** Intelligence advises; it does not silently hijack the journey.

### C9 — Supported subject integrity

Plans may be produced only for subjects Kwalitec can educationally support with official syllabus material. Incomplete or unsupported subjects must not receive “complete plan” theatre.

**Tutor rationale.** Honesty about support boundaries protects students from misleading schedules.

---

## 5. Phase & Horizon Constraints

### C10 — Protect the revision period

A non-trivial revision window before the sitting must be reserved. First-pass learning must not consume it by default packing.

**Tutor rationale.** Revision is mandatory educational capacity, not leftover scraps.

### C11 — Protect mock educational meaning

Mocks must not be placed so early that syllabus coverage is educationally meaningless, nor so late that recovery and final revision are impossible (conditional on remaining horizon).

**Tutor rationale.** A mock without enough coverage wastes stamina; a mock with no recovery wastes learning from the mock.

### C12 — Honour exam date as hard horizon

No plan may assume study after the sitting date for that sitting’s readiness. All capacity derives from time remaining until the examination.

**Tutor rationale.** The exam date is the educational deadline, not a suggestion.

### C13 — Honour planned leave and known interruptions

Known leave and interruptions must be treated as zero- or reduced-capacity periods. Plans must not assign normal load into declared unavailable windows.

**Tutor rationale.** Ignoring leave is a form of impossible workload.

---

## 6. Educational Meaning Constraints

### C14 — Never equate coverage with mastery

Completing Study Progress for a topic must not be planned or narrated as mastery, “known,” or guaranteed exam competence.

**Tutor rationale.** Constitutional educational truth.

### C15 — Evidence before strong weakness/strength claims

Adaptive emphasis on “weak” or “strong” topics requires evidence warrant or clearly labelled student declaration. Plans must not invent diagnostic certainty at cold start.

**Tutor rationale.** False diagnosis destroys trust and misallocates revision.

### C16 — Continuity of learner history

Creating, replacing, or disposing of a Study Plan must not silently erase lawful Study Progress, attempts, evidence posture, or twin-owned estimates. Plans are disposable containers; learner history is not.

**Tutor rationale.** Continuity Standard; Constitution Article on journey continuity.

### C17 — No content generation as planning substitute

Planning must not invent actuarial teaching content, mark conversions, or textbook replacements. Resource assumptions remain bring-your-own materials (e.g. CMP).

**Tutor rationale.** Product and educational boundary: coach the journey, do not fabricate the syllabus content.

---

## 7. Truth & Feasibility Constraints

### C18 — No silent infeasible plans

If required first-pass + revision + mock/recovery capacity exceeds available time, the algorithm must surface infeasibility (and/or propose lawful trade-offs). It must not publish a quietly impossible schedule.

**Tutor rationale.** O8 — avoid unrealistic plans.

### C19 — Deterministic educational cores

Given the same educational inputs, the plan skeleton’s educational decisions must be reproducible. Random syllabus shuffling is forbidden.

**Tutor rationale.** Determinism of educational cores (Constitution).

### C20 — Explainability of material decisions

Material planning choices (sequence policy, intensity band, revision start, mock windows, major buffers) must be explainable per `PLANNING_EXPLAINABILITY.md`. Unexplainable steering is invalid.

**Tutor rationale.** Trust precedes optimisation.

---

## 8. Constraint Checklist (Algorithm Gate)

Before a plan is considered educationally publishable:

- [ ] Daily/weekly load ≤ available capacity (C1–C3)
- [ ] Sustainable intensity with recovery (C4–C5)
- [ ] Official syllabus + prerequisites respected (C6–C7)
- [ ] Learning Mode authority not silently overridden (C8)
- [ ] Subject is supported (C9)
- [ ] Revision window reserved (C10)
- [ ] Mock placement educationally meaningful if mocks are included (C11)
- [ ] Exam date / leave honoured (C12–C13)
- [ ] Coverage ≠ mastery preserved (C14–C15)
- [ ] Continuity preserved (C16)
- [ ] No content fabrication (C17)
- [ ] Feasibility disclosed if threatened (C18)
- [ ] Deterministic and explainable (C19–C20)

Any unchecked item blocks educational validity.

---

## 9. Soft Preferences (Not Constraints)

The following may guide comfort but **must yield** to constraints and objective conflict order:

- Preferred session length within safe bands
- Preferred time of day
- Preferred mock calendar week within lawful windows
- Aesthetic pacing variety that does not break order or capacity

If a preference would violate a constraint, the constraint wins and the refusal must be explained.

---

## 10. Cross References

- `PLANNING_OBJECTIVES.md` — what constraints protect
- `PLANNING_DECISION_MODEL.md` — decisions bounded by these constraints
- `PLANNING_ASSUMPTIONS.md` — capacity and honesty assumptions behind constraints
- `../EDUCATIONAL_CONTINUITY_STANDARD.md` — C16 detail
