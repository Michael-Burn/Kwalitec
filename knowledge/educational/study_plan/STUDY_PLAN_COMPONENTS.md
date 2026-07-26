# Study Plan Components

**Programme:** VI — Master Planner  
**Milestone:** MS007 — Canonical Study Plan Model  
**Classification:** Educational building-block catalogue for completed Study Plans  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **educational components** of a Canonical Study Plan — the building blocks students and coaching systems recognise after successful scheduling.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `CANONICAL_STUDY_PLAN.md`
3. `../scheduling/SCHEDULING_ENGINE.md`
4. `../scheduling/CALENDAR_ALLOCATION.md`
5. `../planning_blueprint/BLUEPRINT_PHASES.md`
6. `../planning_blueprint/BLUEPRINT_COMPONENTS.md`
7. `../EDUCATIONAL_CONTINUITY_STANDARD.md`

Components **represent Scheduling Engine output** as educational structure. They introduce **no new educational reasoning** and define **no implementation fields**.

---

## 1. Purpose

A completed Study Plan is more than a list of dates. Students and coaching surfaces need a shared educational inventory: phases, milestones, study sessions, revision windows, recovery capacity, checkpoints, assumptions, and educational commitments.

This document catalogues those elements so downstream systems consume *authorised plan components*, not invented journey fragments.

Identifiers (SPC-XX) exist for traceability. Educational meaning is binding; display labels may vary. Implementation field names are out of scope.

---

## 2. Component Principles

1. **Timetable-derived.** Every component instance traces to Scheduling Engine output (and through it to blueprint BC-XX / BP-XX and package PD-XX warrants).
2. **Educationally typed.** Type names educational job, not UI widget or database column.
3. **Envelope-bound.** Intensity, practice density, and recovery load stay inside envelopes already allocated.
4. **Composable.** Sessions nest inside phases; protections and commitments may span phase boundaries.
5. **Explainable.** Material components inherit timetable / blueprint explainability (see `STUDY_PLAN_EXPLAINABILITY.md`).
6. **Non-mastery-minting.** Completing a session advances honest work; it does not create mastery claims.
7. **Field-free.** This catalogue defines educational meaning — not schemas, APIs, or serialisation.

---

## 3. Component Catalogue

| ID | Component | Educational job | Primary warrants |
|----|-----------|-----------------|------------------|
| SPC-01 | Phase | Ordered educational mission region of the journey as allocated | Blueprint phases + phase calendar regions |
| SPC-02 | Milestone | Legible educational marker the student can recognise | BC-08 / timetable milestone placements |
| SPC-03 | Study session | Concrete study appointment the student is asked to honour | Timetable sessions / study blocks |
| SPC-04 | Revision window | Protected consolidation region under revision emphasis | BC-04 region + protection placements |
| SPC-05 | Recovery capacity | Lighter-load allowance after dense work, mocks, illness, or disruption | BC-06 + recovery cells |
| SPC-06 | Checkpoint | Focused educational check of recent learning / revision quality | BC-09 / review checkpoint placements |
| SPC-07 | Buffer capacity | Spare educational capacity for slip, illness, replan | BC-07 + buffer placements |
| SPC-08 | Rest / freshness capacity | Planned light or zero-study capacity beyond leave | BC-11 + rest rules |
| SPC-09 | Assumption set | Explicit premises the plan rests on (capacity, leave, evidence, horizon) | Timetable capacity map + package assumptions |
| SPC-10 | Educational commitments | What the plan promises educationally — and refuses to promise | Package / blueprint / timetable guarantees |
| SPC-11 | Practice commitment | Authorised application / question practice within the plan | BC-02 placements |
| SPC-12 | Consolidation commitment | Spaced return to recent topics during first-pass | BC-03 placements |
| SPC-13 | Mock / exam-simulation commitment | Timed exam craft rehearsal near lawful final approach | BC-05 placements |
| SPC-14 | Transition marker | Explicit change of educational mission between phases or postures | BC-10 |
| SPC-15 | Intensity envelope | Sustainable daily/weekly load band the plan must respect | BC-12 |
| SPC-16 | Overflow / infeasibility record | Honest statement of what could not be placed or what remains unresolved | Timetable overflow record |

Milestone examples in the programme brief (phases, milestones, study sessions, revision windows, recovery capacity, checkpoints, assumptions, educational commitments) map onto SPC-01…SPC-10.

---

## 4. Component Specifications

### SPC-01 — Phase

| Aspect | Specification |
|--------|----------------|
| **What** | An ordered educational mission region of the sitting journey as seated on the calendar |
| **Educational meaning** | Tells the student *which job this stretch of the plan is doing* (e.g. foundation first-pass, revision emphasis, final preparation) |
| **Must include** | Mission statement carried from blueprint phase; calendar span as allocated; component inventory belonging to the phase |
| **Must not** | Invent a phase the blueprint never authorised; reorder phases for coaching convenience |
| **Lifecycle note** | Phase emphasis may shift in narration as the plan becomes Active / Adapted; educational phase meaning remains blueprint-bound |

### SPC-02 — Milestone

| Aspect | Specification |
|--------|----------------|
| **What** | A legible educational checkpoint in the journey (not a pass/fail prophecy) |
| **Educational meaning** | Marks progress of honest work — e.g. end of a first-pass stretch, entry to protected revision, completion of a mock window |
| **Must include** | Educational job; position relative to phases; explainability attachment |
| **Must not** | Mint mastery; claim readiness certainty from reaching a date |

### SPC-03 — Study session

| Aspect | Specification |
|--------|----------------|
| **What** | A concrete study appointment within available capacity |
| **Educational meaning** | The unit of lived commitment — what the student is asked to do on a given day/window |
| **Must include** | Educational work type (learning, practice, consolidation, revision, mock, recovery, rest); syllabus / component warrant; placement reason |
| **Must not** | Exist without blueprint/timetable warrant; pack into leave or zero-capacity days; silently redefine Learning Mode topic authority |

Sessions may contain one or more study blocks (fragments of blueprint components). The educational contract speaks in sessions; audits may speak in blocks.

### SPC-04 — Revision window

| Aspect | Specification |
|--------|----------------|
| **What** | Protected calendar region reserved for revision emphasis |
| **Educational meaning** | First-class commitment to consolidation under revision posture — not leftover weeks |
| **Must include** | Protection status; authorised revision work; relationship to sitting horizon |
| **Must not** | Be cannibalised for unfinished first-pass by default; disappear from student-facing plan speech |

### SPC-05 — Recovery capacity

| Aspect | Specification |
|--------|----------------|
| **What** | Lighter-load allowance already authorised for dense work, mocks, illness, or disruption |
| **Educational meaning** | Sustainable coaching: recovery is planned capacity, not punishment absence |
| **Must include** | When recovery may be used; what lighter load means educationally |
| **Must not** | Invent recovery pedagogy absent from blueprint; become silent “catch-up grind” |

### SPC-06 — Checkpoint

| Aspect | Specification |
|--------|----------------|
| **What** | Focused check of recent learning or revision quality |
| **Educational meaning** | Honest quality signal for coaching — not mastery fiat |
| **Must include** | Scope of what is being checked; claim-type humility |
| **Must not** | Declare Mastered from a checkpoint alone |

### SPC-07 — Buffer capacity

| Aspect | Specification |
|--------|----------------|
| **What** | Spare educational capacity reserved for slip, illness, or replan |
| **Educational meaning** | Honesty about uncertainty — buffers absorb divergence before heroics |
| **Must include** | That buffers exist; that using them is a material plan change |
| **Must not** | Be deleted to make an infeasible plan look complete |

### SPC-08 — Rest / freshness capacity

| Aspect | Specification |
|--------|----------------|
| **What** | Planned light or zero-study capacity beyond declared leave |
| **Educational meaning** | Sustainability and freshness as educational goods |
| **Must not** | Be filled with normal load to “use the day” |

### SPC-09 — Assumption set

| Aspect | Specification |
|--------|----------------|
| **What** | Explicit premises the completed plan rests on |
| **Typical assumptions** | Declared weekly availability; known leave and holidays; sitting / exam date; evidence thinness already named upstream; intensity envelope; that protected revision remains protected |
| **Educational meaning** | Students and coaches know *what must stay true* for the plan to remain honest |
| **Must include** | Capacity assumptions; horizon assumptions; any thin-evidence or default assumptions carried from package/timetable |
| **Must not** | Hide critical assumptions; invent optimistic free time as fact |

### SPC-10 — Educational commitments

| Aspect | Specification |
|--------|----------------|
| **What** | The plan’s educational promises and refusals |
| **Promises (examples)** | Follow official syllabus order for first-pass; protect revision window; honour intensity envelopes; explain material structure and change; escalate when envelopes no longer fit |
| **Refusals (examples)** | No pass guarantee; no mastery from coverage alone; no silent commandeering of Learning Mode; no punishment catch-up; no erasure of learner history on plan change |
| **Educational meaning** | Converts upstream law into student-legible commitments |
| **Must not** | Add commitments the timetable / blueprint / package never authorised |

### SPC-11 — Practice commitment

Authorised application / question practice already placed. Advances competence work honestly; never mints mastery from volume alone.

### SPC-12 — Consolidation commitment

Spaced return during first-pass as authorised. Supports retention; does not invent weakness theatre.

### SPC-13 — Mock / exam-simulation commitment

Timed craft rehearsal as authorised near final approach. Educational craft practice — not a certified pass predictor.

### SPC-14 — Transition marker

Explicit educational mission change between phases or postures. Makes journey shape speakable.

### SPC-15 — Intensity envelope

Sustainable load band inherited from the blueprint / timetable. Coaching must not silently breach it for “motivation.”

### SPC-16 — Overflow / infeasibility record

If mandatory work could not be placed lawfully, the plan must carry that truth. Silent completeness theatre is forbidden. Incomplete publication rules apply (`CANONICAL_STUDY_PLAN.md` §5.3; `STUDY_PLAN_VALIDATION.md`).

---

## 5. Required Composition of a Complete Plan

A complete Canonical Study Plan must present at least:

| Required | Components |
|----------|------------|
| Journey shape | SPC-01 phases (as applicable to the blueprint) |
| Lived work | SPC-03 study sessions for placed mandatory work |
| Protections | SPC-04 revision window and/or explicit lawful absence if package/blueprint never reserved revision (rare; usually required) |
| Sustainability | SPC-05 and/or SPC-07 and/or SPC-08 as authorised |
| Honesty frame | SPC-09 assumptions + SPC-10 educational commitments |
| Integrity record | SPC-16 overflow / infeasibility record (including explicit “none”) |
| Markers | SPC-02 / SPC-06 / SPC-14 as authorised by the timetable |

Practice, consolidation, and mocks (SPC-11…SPC-13) appear when the timetable placed them.

### 5.1 Completeness rule

A plan that advertises full first-pass ambition without a protected revision window (when the blueprint reserved one), or that omits assumptions and commitments, or that hides overflow, is compositionally incomplete.

---

## 6. Relationship to Blueprint Components

| Blueprint component | Study Plan representation |
|---------------------|---------------------------|
| BC-01 Learning block | Sessions / blocks inside phases (SPC-01, SPC-03) |
| BC-02 Practice block | SPC-11 (+ sessions) |
| BC-03 Consolidation block | SPC-12 (+ sessions) |
| BC-04 Revision block | SPC-04 (+ sessions) |
| BC-05 Mock block | SPC-13 (+ sessions) |
| BC-06 Recovery capacity | SPC-05 |
| BC-07 Buffer period | SPC-07 |
| BC-08 Milestone | SPC-02 |
| BC-09 Review checkpoint | SPC-06 |
| BC-10 Transition point | SPC-14 |
| BC-11 Rest / freshness | SPC-08 |
| BC-12 Intensity envelope | SPC-15 |
| BC-13 / BC-14 Risk & confidence postures | Carried in SPC-09 / SPC-10 speech; not reinvented |

The Study Plan does not rename educational jobs. It seats them in the completed coaching contract.

---

## 7. What Components Are Not

- Database fields, JSON keys, or ORM columns
- UI cards, wizard steps, or template partials
- New educational diagnoses or strategy choices
- Pass probabilities or mastery certificates
- Licence to invent packing or recovery law

---

## 8. Cross References

- `CANONICAL_STUDY_PLAN.md` — required sections and derivation rule
- `STUDY_PLAN_LIFECYCLE.md` — how components behave across plan states
- `STUDY_PLAN_VALIDATION.md` — compositional validity gates
- `STUDY_PLAN_EXPLAINABILITY.md` — how components are narrated
- `../planning_blueprint/BLUEPRINT_COMPONENTS.md` — upstream component law
- `../scheduling/CALENDAR_ALLOCATION.md` — sessions, regions, blocks
