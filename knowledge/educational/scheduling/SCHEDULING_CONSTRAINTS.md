# Scheduling Constraints

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Hard calendar and capacity constraints for Study Timetables  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **hard constraints** every Study Timetable must respect at the allocation layer.

Constraints here **operationalise** educational constraints from MS001 (`PLANNING_CONSTRAINTS.md`) and blueprint protections from MS005 for calendar packing. They introduce **no new educational reasoning**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `SCHEDULING_ENGINE.md`
3. `SCHEDULING_RULES.md`
4. `../planning/PLANNING_CONSTRAINTS.md`
5. `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md`

Soft preferences, heuristics, and optimiser convenience never override these constraints.

---

## 1. Purpose

An expert IFoA tutor will refuse certain diaries even if every cell is “filled.”

These constraints encode that refusal for packing: what a lawful timetable must never demand, ignore, or imply.

---

## 2. Constraint Categories

| Category | Meaning |
|----------|---------|
| **Hard** | Violation → timetable is allocation-invalid |
| **Conditional hard** | Hard whenever the triggering condition exists |
| **Inherited educational** | Hard because upstream educational law forbids the packed outcome |

Identifiers (SC-XX) exist for traceability.

---

## 3. Capacity & Availability Constraints

### SC-01 — No impossible daily workloads

Do not assign more study on a day than declared available minutes and cognitive/intensity envelopes allow.

**Maps to:** C1; SR-06; SR-08.

### SC-02 — Weekly load within availability

Weekly placed minutes ≤ declared weekly available study time after leave, holidays, and mandated rest.

**Maps to:** C2; SR-06.

### SC-03 — Study-day pattern integrity

Do not place normal working sessions on days the student declared unavailable.

**Maps to:** C3; SR-07.

### SC-04 — Intensity envelope ceiling

Daily/weekly working load must remain inside blueprint BC-12 bands. Catch-up that breaches the envelope is unlawful without upstream replan.

**Maps to:** C4–C5; SR-08.

### SC-05 — No packing into leave

Declared leave periods are zero or reduced capacity. Normal learning/practice/revision load must not be assigned into them.

**Maps to:** C13; SR-17.

### SC-06 — Holiday capacity truth

Holidays marked unavailable are treated as leave. Study on a holiday requires declared availability for that date.

**Maps to:** SR-18.

### SC-07 — Rest day integrity

When rest / freshness capacity is required (BC-11 or declared non-study pattern), those days must not be filled with dense working load by default.

**Maps to:** SR-16; C4–C5.

---

## 4. Horizon & Protection Constraints

### SC-08 — Exam date hard horizon

No working cells for this sitting after the sitting / exam date.

**Maps to:** C12; SR-19.

### SC-09 — Protected revision inviolable by default

First-pass (and other non-revision missions) must not consume the reserved revision calendar region by default packing.

**Maps to:** C10; SR-10; F2 family upstream.

### SC-10 — Buffer visibility

If the blueprint includes non-zero buffer policy, the timetable must retain corresponding spare capacity until lawful rescheduling consumes it. Silent deletion to force a fit is forbidden.

**Maps to:** SR-12; PD-08 / BC-07.

### SC-11 — Recovery capacity preserved

Blueprint-authorised recovery cells (including post-mock recovery) must not be overwritten with dense make-up work as the default response to slip.

**Maps to:** SR-11; C11 (mock recovery aspect).

### SC-12 — Final-approach freeze

Do not schedule unbounded new first-pass expansion into BP-06 calendar regions.

**Maps to:** SR-14.

### SC-13 — Mock window honesty

Mocks appear only in blueprint-authorised windows with meaningful coverage posture and recovery space as already structured.

**Maps to:** C11; SR-15.

---

## 5. Sequencing & Curriculum Constraints

### SC-14 — Official sequencing preserved

Where the blueprint requires official syllabus order, calendar placement must not reorder topics for engagement or packing metrics.

**Maps to:** C6; SR-13.

### SC-15 — Prerequisite integrity

Do not place primary first-pass study of a dependent unit before its foundations are covered (unless upstream waiver already exists and is disclosed).

**Maps to:** C7; SR-02.

### SC-16 — Learning Mode authority not silently overridden

Timetable placement may schedule learning work consistent with blueprint envelopes; it must not secretly replace Current Learning Topic / Learning Mode constitutional authority without disclosure and lawful mode.

**Maps to:** C8.

### SC-17 — Practice only on studied scope

Do not schedule practice blocks as coverage substitutes for never-studied units.

**Maps to:** Blueprint BC-02 law; Knowledge & Mastery separation.

---

## 6. Truth & Feasibility Constraints

### SC-18 — No silent infeasible timetables

If mandatory blueprint work cannot be placed under these constraints, surface overflow / allocation infeasibility (and escalate upstream). Do not publish quietly impossible completeness.

**Maps to:** C18; SR-09; SR-27.

### SC-19 — Feasibility posture inherited

An infeasible or triage blueprint must not be packed into a complete-looking timetable that hides that posture.

**Maps to:** SR-04.

### SC-20 — Deterministic allocation cores

Given the same blueprint and practical inputs, allocation posture must be reproducible. Random syllabus shuffling is forbidden.

**Maps to:** C19; SR-24.

### SC-21 — Explainability of material placements

Material placement choices (revision region dating, major session pattern, buffer location, overflow disclosure, reschedule moves) must be explainable per `SCHEDULING_EXPLAINABILITY.md`.

**Maps to:** C20; EIP-003.

### SC-22 — Coverage ≠ mastery preserved

Completing scheduled blocks must not be planned or narrated as mastery, “known,” or guaranteed exam competence.

**Maps to:** C14–C15.

### SC-23 — Continuity of learner history

Rescheduling and timetable replacement must not erase lawful Study Progress, attempts, evidence posture, or twin-owned estimates.

**Maps to:** C16; Continuity Standard.

### SC-24 — No content fabrication

Scheduling must not invent actuarial teaching content or substitute fabricated materials for official syllabus resources.

**Maps to:** C17.

### SC-25 — No new educational reasoning in packing

Any rule that would require diagnosing the student, choosing strategy, altering decision postures, or inventing blueprint structure is out of bounds for the Scheduling Engine.

**Maps to:** MS006 architectural requirement; SR-05.

---

## 7. Constraint Checklist (Publication Gate)

Before a Study Timetable is allocation-publishable:

- [ ] Daily/weekly load ≤ availability and envelopes (SC-01…SC-04)
- [ ] Leave, holidays, rest honoured (SC-05…SC-07)
- [ ] Exam horizon honoured (SC-08)
- [ ] Revision, buffer, recovery, final freeze protected (SC-09…SC-12)
- [ ] Mocks lawful (SC-13)
- [ ] Sequencing / prerequisites / mode authority / practice honesty (SC-14…SC-17)
- [ ] Feasibility and overflow honesty (SC-18…SC-19)
- [ ] Deterministic and explainable (SC-20…SC-21)
- [ ] Coverage ≠ mastery; continuity; no content fabrication (SC-22…SC-24)
- [ ] No new educational reasoning (SC-25)

Any unchecked Hard item blocks publication.

---

## 8. Soft Preferences (Not Constraints)

The following may guide comfort but **must yield** to SC-01…SC-25:

- Preferred session length within safe bands
- Preferred time of day within available windows
- Preferred mock calendar week within lawful mock windows
- Aesthetic pacing variety that does not break order or capacity
- Mild within-week front/back loading inside envelopes

If a preference would violate a constraint, the constraint wins and the refusal must be explained.

---

## 9. Relationship to Upstream Constraints

| Upstream (MS001) | Scheduling realisation |
|------------------|------------------------|
| C1–C5 capacity/load | SC-01…SC-04, SC-07 |
| C6–C8 curriculum/mode | SC-14…SC-16 |
| C10–C13 phases/horizon/leave | SC-05, SC-06, SC-08…SC-13 |
| C14–C17 meaning/continuity/content | SC-22…SC-24 |
| C18–C20 truth/determinism/explainability | SC-18…SC-21 |

Scheduling constraints do not replace MS001. They ensure packing cannot violate MS001 by calendar cleverness.

---

## 10. Cross References

- `SCHEDULING_RULES.md` — deterministic rules implementing these constraints
- `CALENDAR_ALLOCATION.md` — capacity map and overflow mechanics
- `RESCHEDULING_POLICY.md` — lawful adaptation without constraint breach
- `../planning/PLANNING_CONSTRAINTS.md` — educational constraint authority
- `../planning_blueprint/BLUEPRINT_COMPONENTS.md` — protection components
