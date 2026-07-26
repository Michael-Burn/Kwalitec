# Scheduling Rules

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Deterministic allocation rules for Study Timetables  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **deterministic allocation rules** that transform an approved Planning Blueprint into calendar placement.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `SCHEDULING_ENGINE.md`
3. `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md`
4. `../planning_blueprint/BLUEPRINT_PHASES.md`
5. `../planning_blueprint/BLUEPRINT_COMPONENTS.md`
6. `../planning_blueprint/BLUEPRINT_PROGRESSION.md`
7. `../planning/PLANNING_CONSTRAINTS.md`

Rules below are **allocation mechanics**. They preserve educational intent already settled in the blueprint. They introduce **no new educational reasoning**.

> **If a rule appears to require educational judgement, that judgement belongs upstream.**

---

## 1. Purpose

Packing without rules becomes either fiction (ignore capacity) or invention (rewrite the journey while filling days).

These rules encode how an expert tutor places an already-approved journey onto a real diary: order preserved, protections first, capacity honest, rest respected, overflow named.

---

## 2. Rule Categories

| Category | Meaning |
|----------|---------|
| **Hard** | Violation → timetable is allocation-invalid |
| **Conditional hard** | Hard whenever the triggering condition exists |
| **Ordering** | Hard rules about sequence and prerequisites |
| **Protection** | Hard rules about revision, buffer, recovery, intensity |

All rules below are **Hard**, **Conditional hard**, **Ordering**, or **Protection** unless marked otherwise.

Identifiers (SR-XX) exist for traceability. Educational meaning remains in the blueprint; these IDs name allocation obligations.

---

## 3. Blueprint Fidelity Rules

### SR-01 — Preserve blueprint ordering

Place phases and components in the order the blueprint establishes. Interleaving authorised by the blueprint (e.g. BP-02 / BP-03 beside BP-01) remains lawful; inventing new interleave patterns is not.

**Tutor rationale.** Order is educational law already decided. Packing must not shuffle the journey for calendar aesthetics.

### SR-02 — Respect prerequisite sequencing

Within BC-01 learning blocks, do not schedule primary first-pass study of a unit before its prerequisites are covered (or lawfully waived upstream and disclosed). Calendar convenience never authorises silent prerequisite skip.

**Tutor rationale.** Curriculum primacy and C6–C7 survive packing.

### SR-03 — Place only authorised components

Every session/block must cite a blueprint component instance (or an explicit rest / leave capacity cell). Invented task types with new educational jobs are forbidden.

**Tutor rationale.** Schedulers place authorised blocks; they do not mint pedagogy.

### SR-04 — Honour feasibility posture

If the blueprint / package marks the sitting infeasible or triage-reduced, the timetable must not present a complete “everything fits” theatre. Reduced placements must remain honest.

**Tutor rationale.** Fiction at packing layer is still fiction.

### SR-05 — No new educational reasoning

Allocation may use practical facts (availability, leave, holidays, missed sessions). It must not create new intensity bands, revision meanings, practice densities, weakness claims, or phase missions.

**Tutor rationale.** Architectural requirement of MS006.

---

## 4. Capacity Honesty Rules

### SR-06 — Never exceed available study time

Daily and weekly placed load must fit inside declared available study time after leave, holidays, and mandated rest capacity.

**Tutor rationale.** C1–C3; plans that ignore real hours are fiction.

### SR-07 — Respect study-day pattern

Place sessions only on days and within windows the student can actually use. Do not silently relocate weekly hours onto unavailable days.

**Tutor rationale.** “Average hours per week” is not a licence to invent free evenings.

### SR-08 — Honour intensity envelopes

Placed working load for a day/week must stay inside the blueprint’s BC-12 intensity envelope. Exceeding the envelope to clear backlog is unlawful without upstream replan.

**Tutor rationale.** Sustainable intensity is package law, not a soft packing hint.

### SR-09 — Prefer incomplete honesty over silent overflow

When remaining capacity cannot host remaining components under SR-01…SR-08, record overflow / allocation infeasibility. Do not hide overflow by shrinking protected regions.

**Tutor rationale.** C18 — no silent infeasible plans.

---

## 5. Protection Rules

### SR-10 — Protect revision windows

Map the blueprint’s protected revision region (BP-04 / BC-04 / PD-03) onto calendar capacity **before** packing unconstrained first-pass leftovers into that span. First-pass must not consume revision capacity by default packing.

**Tutor rationale.** C10; revision is mandatory educational capacity, not leftover scraps.

### SR-11 — Preserve recovery capacity

When the blueprint includes BC-06 recovery (including post-mock recovery), reserve corresponding calendar capacity. Do not fill recovery cells with dense first-pass or punishment catch-up as the default.

**Tutor rationale.** Recovery is structural; packing must not erase it.

### SR-12 — Preserve buffer capacity

When the blueprint includes non-zero BC-07 buffer policy, keep that capacity visible on the calendar as unallocated or lightly held spare — available for lawful slip — until rescheduling lawfully consumes it.

**Tutor rationale.** Buffers make recovery possible; deleting them to “fit” the plan hides risk.

### SR-13 — Honour official curriculum sequencing where required

Where the blueprint’s sequencing policy requires official syllabus order, calendar placement must not reorder for engagement, variety, or optimiser metrics.

**Tutor rationale.** Constitution and C6; order is not a packing preference.

### SR-14 — Protect final-approach freeze

When BP-06 / final preparation is active in the blueprint, do not schedule unbounded new first-pass expansion into that calendar region.

**Tutor rationale.** Freeze is educational mission already decided; packing must not reopen syllabus sprawl.

### SR-15 — Mock placement respects coverage and recovery

Place BC-05 only inside blueprint-authorised mock windows, with coverage maturity and post-mock recovery capacity already structured upstream. Do not invent early meaningless mocks or late mocks that erase recovery/revision.

**Tutor rationale.** C11; allocator places authorised mocks, does not redesign mock pedagogy.

---

## 6. Rest, Leave, and Holiday Rules

### SR-16 — Rest day handling

When the blueprint or package includes rest / freshness capacity (BC-11 / D17), or when declared availability implies non-study days, treat those days as zero or light capacity. Do not fill every calendar day by default.

**Tutor rationale.** Cognitive freshness is an educational resource already recognised upstream; packing must not grind seven days unless lawfully authorised.

### SR-17 — Leave periods are zero/reduced capacity

Declared leave windows receive no normal working load. Optional ultra-light continuity touches are allowed only if the blueprint / package explicitly authorised them; otherwise leave is empty.

**Tutor rationale.** C13; ignoring leave is impossible workload.

### SR-18 — Holiday handling

Public / institutional holidays declared as unavailable (or reduced) are treated like leave for capacity maths. Preferable study on a holiday occurs only if the student declared that day available.

**Tutor rationale.** Holidays are practical capacity facts, not educational opportunities invented by the allocator.

### SR-19 — Exam horizon hard stop

No working cells for this sitting may be placed after the sitting / exam date. All capacity derives from time remaining until that horizon.

**Tutor rationale.** C12 / F13.

---

## 7. Placement Mechanics Rules

### SR-20 — Protect regions first, then fill forward

Allocation order of operations:

1. Anchor sitting date and build capacity map (availability − leave − holidays − mandated rest).
2. Reserve protected revision, final-approach, mock+recovery, and buffer regions on the calendar.
3. Place remaining phase regions in blueprint order into residual capacity.
4. Split components into sessions/blocks within those regions.
5. Record overflow if residual capacity is insufficient.

**Tutor rationale.** Working backwards from the sitting protects what packing pressure would otherwise steal.

### SR-21 — Session length within safe bands

Session durations should prefer student preferences when stated, but must remain inside sustainable bands implied by BC-12 and declared daily capacity. Preferences yield to constraints.

**Tutor rationale.** Soft preferences are not constraints (MS001 §9).

### SR-22 — Split blocks without breaking order

A learning or practice component may span multiple days/sessions. Splitting must preserve internal topic order and must not strand prerequisite-dependent units earlier than their foundations.

**Tutor rationale.** Calendar granularity changes; educational order does not.

### SR-23 — Flexible capacity is residual, not rewrite authority

Flexible or unallocated capacity inside a week may absorb small slips or preference tweaks. It must not authorise new educational missions or silent consumption of protected regions.

**Tutor rationale.** Flexibility is packing slack, not a Decision Engine.

### SR-24 — Deterministic tie-breaks

When multiple lawful placements exist (e.g. Tuesday vs Wednesday evening, both available and envelope-safe), apply a fixed tie-break order, for example:

1. Prefer student’s stated preferred window  
2. Else prefer earlier available window in the same week  
3. Else prefer contiguous placement with the prior related block  
4. Else prefer the chronologically earlier day  

Document the active tie-break policy in implementation notes when Runtime A is built. Random choice is forbidden.

**Tutor rationale.** Deterministic educational cores (C19) extend to allocation posture.

---

## 8. Rescheduling Interface Rules

### SR-25 — Preserve educational intent on move

When moving cells after missed sessions, reduced availability, extra time, leave, or illness, preserve blueprint order, protections, and envelopes. Move *placement*; do not rewrite *mission*.

Detail: `RESCHEDULING_POLICY.md`.

### SR-26 — Consume buffer before inventing compression

Lawful first response to slip is use of BC-07 buffer capacity (and blueprint-authorised PD-16 options already structured). Heroic envelope breach is not a first response.

**Tutor rationale.** Matches blueprint progression recovery law.

### SR-27 — Escalate when allocation cannot preserve intent

If remaining capacity cannot host remaining blueprint work under SR-01…SR-26, stop silent adaptation and escalate for upstream re-package / re-blueprint.

**Tutor rationale.** Allocation ends where educational law must change.

---

## 9. Rule Checklist (Allocation Gate)

Before a Study Timetable is considered allocation-valid:

- [ ] Blueprint ordering preserved (SR-01)
- [ ] Prerequisites / official sequencing honoured (SR-02, SR-13)
- [ ] Only authorised components placed (SR-03)
- [ ] Feasibility posture honest (SR-04)
- [ ] No new educational reasoning (SR-05)
- [ ] Load ≤ available capacity; study-day pattern respected (SR-06, SR-07)
- [ ] Intensity envelopes honoured (SR-08)
- [ ] Overflow named if present (SR-09)
- [ ] Revision, recovery, buffer, final freeze protected (SR-10…SR-12, SR-14)
- [ ] Mocks placed only in authorised windows (SR-15)
- [ ] Rest / leave / holidays / exam horizon honoured (SR-16…SR-19)
- [ ] Protect-regions-first allocation order used (SR-20)
- [ ] Splits preserve order; flexible capacity not abused (SR-22, SR-23)
- [ ] Deterministic tie-breaks (SR-24)

Any unchecked Hard / Protection item blocks allocation validity.

---

## 10. Soft Preferences (Not Rules)

The following may guide comfort but **must yield** to SR-01…SR-27 and scheduling constraints:

- Preferred session start time within an available window
- Preferred mock calendar week within the blueprint-authorised mock window
- Aesthetic spacing variety that does not break order, protections, or capacity
- Mild front-loading or back-loading inside a week within envelope

If a preference would violate a hard rule, the rule wins and the refusal must be explainable.

---

## 11. Cross References

- `SCHEDULING_ENGINE.md` — allocation-only constitution
- `CALENDAR_ALLOCATION.md` — weeks, days, sessions, overflow
- `SCHEDULING_CONSTRAINTS.md` — constraint catalogue
- `RESCHEDULING_POLICY.md` — SR-25…SR-27 in depth
- `../planning_blueprint/BLUEPRINT_COMPONENTS.md` — §7 what scheduling may do
- `../planning/PLANNING_CONSTRAINTS.md` — C1–C20 educational constraints
