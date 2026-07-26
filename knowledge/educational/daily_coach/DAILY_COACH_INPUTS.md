# Daily Coach Inputs

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS001 — Daily Coaching Model  
**Classification:** Educational input catalogue for day-to-day coaching  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **educational inputs** required before the Daily Coach may form today’s guidance.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `DAILY_COACH_MODEL.md`
3. `DAILY_COACH_DECISION_MODEL.md`
4. `../study_plan/CANONICAL_STUDY_PLAN.md`
5. `../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`
6. `../EDUCATIONAL_EVIDENCE_MODEL.md`
7. `EDUCATIONAL_LOGIC_REGISTRY.md` (EL-001–EL-011 as applicable)

> **Inputs are educational meaning requirements.  
> This milestone does not implement collection, persistence, or APIs.**

---

## 1. Purpose

An expert IFoA tutor does not invent today’s advice from vibes. The tutor consults the long-term plan, the student’s current educational state, what recently happened, and what today actually allows.

This catalogue names those inputs so future algorithms and surfaces **consult authorised educational truth** rather than inventing missing context.

Identifiers (DCI-XX) exist for traceability. Educational meaning is binding; field names and schemas are out of scope.

---

## 2. Input Principles

1. **Consult, don’t invent.** Missing mandatory inputs yield incomplete or refused coaching — not fabricated certainty.
2. **Plan is primary contract.** Canonical Study Plan inputs dominate long-term intent.
3. **Profile is diagnosis, not re-strategy.** Profile informs today’s interpretation; it does not authorise silent strategy change at Daily Coach layer.
4. **Evidence is typed.** Soft signals and hard evidence are not interchangeable (Evidence Model).
5. **Capacity is truth.** Declared available time and interruptions constrain load before ambition.
6. **Lifecycle matters.** Only Active-class plans are coaching authority for plan-based days.
7. **Collection is out of scope.** UX and pipelines may gather these inputs later; educational requirement remains.
8. **Privacy & minimality.** Only educationally necessary inputs are required for today’s decision.

---

## 3. Input Catalogue

| ID | Input | Educational job | Mandatory for plan-based day? |
|----|-------|-----------------|-------------------------------|
| DCI-01 | Canonical Study Plan (Active-class) | Long-term educational contract being interpreted | Yes |
| DCI-02 | Plan lifecycle posture | Whether coaching, recovery, or refusal applies | Yes |
| DCI-03 | Today’s authorised plan work | Sessions / phase emphasis / protections for today | Yes |
| DCI-04 | Student Educational Profile | Current educational diagnosis | Yes (at least capacity + coverage posture) |
| DCI-05 | Mode & topic authority | Learning Mode / Current Learning Topic when learning job applies | Yes when today’s job is first-pass learning |
| DCI-06 | Recent learning evidence | Lawful observations that may modulate emphasis | Preferred; thin evidence must be named |
| DCI-07 | Session completion history | What planned work was recently done or missed | Yes for continuity / escalation honesty |
| DCI-08 | Available study time today | Capacity ceiling for recommended blocks | Yes |
| DCI-09 | Planned interruptions | Known meetings, leave fragments, non-study commitments today | Yes when declared / known |
| DCI-10 | Recovery state | Whether recovery / lighter load is active | Yes |
| DCI-11 | Intensity / protection envelopes | Load and protection bounds inherited from the plan | Yes |
| DCI-12 | Escalation / feasibility flags | Whether plan already signals infeasibility or pending replan | Yes when present |

---

## 4. Input Specifications

### DCI-01 — Canonical Study Plan (Active-class)

| Aspect | Specification |
|--------|----------------|
| **What** | The authorised preparation contract for the sitting (MS007) |
| **Must include** | Phase structure, session inventory, protections, commitments, explainability traces |
| **Educational use** | Source of long-term intent and today’s authorised work types |
| **Must not** | Be substituted by a dashboard heuristic or local task list |
| **If missing / non-Active** | Refuse plan-based Daily Coach theatre (DCD-01) |

### DCI-02 — Plan lifecycle posture

| Aspect | Specification |
|--------|----------------|
| **What** | Educational lifecycle state under `STUDY_PLAN_LIFECYCLE.md` |
| **Educational use** | Distinguishes Active vs Adapted vs Recovered coaching posture; blocks Draft / Archived / Superseded authority |
| **Must not** | Treat lifecycle labels as licence to rewrite educational law |

### DCI-03 — Today’s authorised plan work

| Aspect | Specification |
|--------|----------------|
| **What** | The plan’s sessions, commitments, and protection regions that apply to today’s calendar / study window |
| **Includes** | Work type (learning, practice, consolidation, revision, mock, recovery, rest); syllabus / component warrants; ordering |
| **Educational use** | Primary material for priority ladder resolution (DCD-03 / DCD-04) |
| **Must not** | Invent sessions the plan did not authorise |

### DCI-04 — Student Educational Profile

| Aspect | Specification |
|--------|----------------|
| **What** | Current educational diagnosis (MS002) — coverage posture, attempts, estimates where lawful, capacity context, educational states |
| **Educational use** | Interpret today’s advice for *this* student without re-selecting strategy |
| **Must not** | Be freshly invented at Daily Coach layer; re-diagnosis belongs upstream when material |
| **Minimum for coaching** | Enough to know capacity context and coverage / continuity posture; thin profiles require understatement |

### DCI-05 — Mode & topic authority

| Aspect | Specification |
|--------|----------------|
| **What** | Active educational mode and, under Learning Mode, Current Learning Topic / Study Progress spine |
| **Educational use** | Align primary learning objectives with EL-002 / EL-003 / EL-009 |
| **Must not** | Be overridden silently by recommendations (EL-008) |

### DCI-06 — Recent learning evidence

| Aspect | Specification |
|--------|----------------|
| **What** | Recent Educational Evidence relevant to today’s topics / practice (Evidence Model) |
| **Educational use** | Modulate emphasis inside envelopes (DCD-05); never mint mastery alone |
| **Quality rule** | Thin, soft, or absent evidence must be named in speech; must not be filled with invented certainty |
| **Collection** | Out of scope |

### DCI-07 — Session completion history

| Aspect | Specification |
|--------|----------------|
| **What** | Recent record of planned sessions / study blocks completed, partial, or missed |
| **Educational use** | Continuity repair, consistency judgement, escalation triggers |
| **Claim type** | Observed / derived journey facts — not understanding proof |
| **Must not** | Equate completion with competence |

### DCI-08 — Available study time today

| Aspect | Specification |
|--------|----------------|
| **What** | Declared or otherwise known study minutes / windows available today |
| **Educational use** | Cap recommended study blocks; trigger P1 when zero |
| **Must not** | Be ignored in favour of plan session length alone |

### DCI-09 — Planned interruptions

| Aspect | Specification |
|--------|----------------|
| **What** | Known breaks in today’s capacity (meetings, caring duties, travel fragments, partial leave) |
| **Educational use** | Shape realistic block boundaries; preserve honesty about fragmented evenings |
| **If unknown** | Coach with stated uncertainty; do not invent a clear six-hour evening |

### DCI-10 — Recovery state

| Aspect | Specification |
|--------|----------------|
| **What** | Whether the student / plan is in recovery posture (Recovered lifecycle, engaged SPC-05, post-illness lighter load, freshness needs) |
| **Educational use** | Elevate P1/P2 priorities; forbid punishment catch-up |
| **Must not** | Invent recovery pedagogy absent from plan / rescheduling warrant when claiming plan-faithful recovery |

### DCI-11 — Intensity / protection envelopes

| Aspect | Specification |
|--------|----------------|
| **What** | SPC-15 intensity envelope plus protection regions (revision, buffer, recovery, rest) carried on the plan |
| **Educational use** | Bound adaptive scope; detect escalation when today’s pressure would breach them |
| **Must not** | Be treated as soft suggestions the Daily Coach may quietly exceed |

### DCI-12 — Escalation / feasibility flags

| Aspect | Specification |
|--------|----------------|
| **What** | Existing signals that the plan is infeasible, overflow remains, replan is pending, or reschedule is required |
| **Educational use** | Prevent fake “business as usual” coaching over a broken contract |
| **Must not** | Be hidden to preserve motivational theatre |

---

## 5. Input Completeness Rules

| Situation | Lawful Daily Coach posture |
|-----------|----------------------------|
| All mandatory inputs present | Full plan-based daily guidance |
| Plan Active-class but today’s capacity unknown | Ask / require capacity truth before dense recommendations; otherwise understate and prefer smaller continuity-safe objective |
| Evidence thin | Plan-led guidance with explicit uncertainty; no confident understanding claims |
| Profile thin but plan valid | Coach from plan + capacity; avoid Profile-invented diagnoses |
| Plan missing / non-coaching lifecycle | Refuse plan-based coaching theatre |
| Escalation flags present | Prefer escalation-aware interim guidance (Decision Model §8) |

**Binding rule:** The Daily Coach must not invent missing educational inputs to appear complete.

---

## 6. Inputs the Daily Coach Must Not Require as Educational Authority

The following may exist in product systems but are **not** educational authority for today’s primary objective:

- Engagement / streak metrics as proof of educational value  
- Raw optimiser scores or Twin facet dumps as student-facing decision drivers  
- Unvalidated self-reported “I know this” as mastery warrant  
- Marketing urgency (“exam soon!”) as licence to steal protected revision  
- UI layout preferences that reorder educational priority  

Practical telemetry may support implementation later; it must not redefine educational meaning.

---

## 7. Relationship to Collection

Collection UX, calendars, check-ins, and evidence pipelines are **out of scope** for MS001.

Educational requirement remains: future implementations must be able to supply DCI-01…DCI-12 meanings (or refuse honestly when they cannot).

---

## 8. Cross References

| Document | Relationship |
|----------|----------------|
| [`DAILY_COACH_DECISION_MODEL.md`](DAILY_COACH_DECISION_MODEL.md) | How inputs are consumed |
| [`DAILY_COACH_OUTPUTS.md`](DAILY_COACH_OUTPUTS.md) | What inputs authorise |
| [`../student_profile/PROFILE_INPUTS.md`](../student_profile/PROFILE_INPUTS.md) | Upstream diagnosis input law |
| [`../EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) | Evidence claim lawfulness for DCI-06 |
