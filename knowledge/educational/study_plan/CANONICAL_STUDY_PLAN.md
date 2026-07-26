# Canonical Study Plan

**Programme:** VI — Master Planner  
**Milestone:** MS007 — Canonical Study Plan Model  
**Classification:** Highest educational authority for completed Study Plan meaning within Programme VI  
**Status:** APPROVED — governing for Study Plan educational contract  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Canonical Study Plan** for Kwalitec.

It is subordinate to the Educational Constitution and specialised educational models. It governs **what a Study Plan is after successful scheduling** — the educational artefact shared across the Kwalitec ecosystem. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning absent from Scheduling Engine output.

Authority order for Master Planner personalisation:

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Student Educational Profile (MS002) diagnoses who the student is educationally now.  
> Educational Strategy Framework (MS003) chooses which overall educational approach to adopt.  
> Educational Planning Model (MS001) defines how an expert tutor designs the journey under that strategy.  
> Planning Decision Engine (MS004) transforms Profile + Strategy + Planning Model into a Planning Decision Package.  
> Planning Blueprint (MS005) organises that package into a date-independent study journey.  
> Scheduling Engine (MS006) allocates that blueprint onto a realistic calendar.  
> **This Canonical Study Plan (MS007) defines the educational contract of that completed allocation.**  
> Downstream coaching capabilities must consume this contract — never redefine educational structure while serving the plan.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabi such as CM1/CS1 and peers).

An expert IFoA tutor does not hand the student a raw packing log. After the journey is diagnosed, strategised, decided, blueprinted, and seated on a real calendar, the tutor presents a **Study Plan**: a coherent educational promise the student can live by.

That product answers:

1. What educational journey am I committed to for this sitting?
2. What phases, sessions, revision windows, and recovery capacity compose it?
3. What must remain true for the plan to stay educationally honest?
4. When and why may the plan change?
5. How do I understand why this plan exists — not merely what dates appear?

> **The Canonical Study Plan describes the educational artefact.  
> It does not invent educational reasoning or scheduling behaviour.**

This document records that tutor posture so every future coaching subsystem has a single educational reference for *what a completed Study Plan is*.

---

## 2. What the Canonical Study Plan Is

The **Canonical Study Plan** is the educational representation of a successfully scheduled study journey for a named examination sitting.

| Input | Role |
|-------|------|
| **Scheduling Engine output (Study Timetable)** | Faithful calendar placement of an approved Planning Blueprint (MS006) — sessions, regions, protections, overflow record, explainability |

into:

| Output | Role |
|--------|------|
| **Canonical Study Plan** | Single educational contract: content, structure, lifecycle posture, validation status, and explainability for downstream coaching |

It answers:

| Question | Educational answer |
|----------|-------------------|
| What is the plan? | The authorised preparation frame for this student, syllabus, strategy, and sitting — after lawful scheduling |
| What is it made of? | Phases, milestones, study sessions, revision windows, recovery capacity, checkpoints, assumptions, and educational commitments |
| What does it guarantee? | Traceability, protection honesty, capacity honesty, continuity of learner history, and speakable reasons — not a pass |
| What must consumers not invent? | New phases, revision meaning, intensity, recovery law, or strategy |
| What is still deferred? | Runtime A persistence, APIs, UI, serialisation |

The Study Plan is:

- **timetable-derived** — every material element traces to Scheduling Engine output;
- **blueprint-faithful** — inherits journey structure already authorised by the Planning Blueprint;
- **educationally deterministic** — same complete timetable yields the same plan posture;
- **explainable** — students can understand why the plan exists and how it is structured;
- **coaching-ready** — explicit enough for missions, sessions, advisory layers, and narration to consume without re-planning;
- **non-inventive** — represents existing educational law; does not add educational reasoning;
- **lifecycle-aware** — has educational states (draft through archived) with meaning, not mere labels;
- **disposable as container** — planning artefacts may be superseded or archived; learner educational history survives (EIP-005 / EL-011).

The Study Plan is **not**:

- a second Scheduling Engine, Decision Engine, Strategy selector, or Profile diagnostician;
- a licence to invent phases, revision windows, or intensity bands after packing;
- a Learning Mode / Revision Mode switch (modes retain daily constitutional authority);
- a claim that following the plan guarantees a pass;
- ownership of Study Progress, Educational Evidence, or Twin understanding;
- a software class design, database schema, or Runtime A service interface.

---

## 3. Educational Purpose

The Canonical Study Plan exists so that:

1. **The student has one authorised preparation frame** for the sitting — syllabus scope, strategy, journey shape, and concrete study commitments in one educational story.
2. **Downstream coaching speaks with one voice** — missions, sessions, recommendations, and analytics consume the same contract rather than each inventing local journey meaning.
3. **Educational integrity survives product surfaces** — coverage, estimates, and advice remain claim-typed and traceable to upstream law.
4. **Change remains honest** — adaptation, recovery, supersession, and archive have educational meaning students can understand.
5. **Continuity is protected** — replacing or deleting the plan container does not erase rightful learner history.

---

## 4. Educational Guarantees

A lawful Canonical Study Plan **guarantees** the following educational properties — not exam outcomes.

| Guarantee | Meaning |
|-----------|---------|
| **Derivation integrity** | Every material element is warranted by Scheduling Engine output (and through it Blueprint → Package → Profile / Strategy / Planning Model). |
| **Blueprint fidelity** | Phase order, component meanings, sequencing, revision protection, buffers, recovery, and intensity envelopes match the approved blueprint as allocated. |
| **Capacity honesty** | Placed study does not invent availability; leave, holidays, and rest remain capacity truth. |
| **Protection honesty** | Protected revision, buffers, and recovery capacity appear as first-class plan elements — not residual scraps or silent theatre. |
| **Constraint respect** | Educational and allocation constraints already settled upstream are not violated by the plan representation. |
| **Strategy & Profile alignment** | The plan remains consistent with the strategy and Profile postures carried on the timetable / blueprint / package. |
| **Explainability** | Material structure and material change can be narrated under `STUDY_PLAN_EXPLAINABILITY.md`. |
| **Continuity** | Plan lifecycle change does not erase learner-owned educational history (EIP-005). |
| **Non-mastery-minting** | Completing scheduled work advances honest study; it does not mint mastery or pass claims from the plan alone. |
| **Mode humility** | Plan phase emphasis does not silently commandeer Learning Mode topic authority. |

### 4.1 What the plan does *not* guarantee

- That the student will pass the examination.
- That every scheduled session will be completed as placed.
- That Estimated Knowledge / Mastery equals Study Progress.
- That advisory recommendations may override mandatory protections.
- That a dense calendar equals readiness.

---

## 5. Derivation Rule (Binding)

### 5.1 Sole educational input

Assembly of a Canonical Study Plan consumes **only** Scheduling Engine output — an approved Study Timetable (and the MS001–MS006 authorities that timetable already cites).

It must **not** introduce:

- new objectives, constraints, phases, or component meanings;
- new strategy privileges or Profile diagnoses;
- new sequencing, intensity, practice density, or feasibility judgements;
- new revision, buffer, or recovery *educational* law;
- new calendar placement or packing behaviour.

Practical facts already embodied in the timetable (availability, leave, holidays, reschedule events) may be **represented** as plan context. Using them to invent educational meaning at plan layer is unlawful.

### 5.2 Representation, not invention

| Study Plan may… | Study Plan must not… |
|-----------------|----------------------|
| Name phases and sessions as allocated on the timetable | Invent a “revision phase” because leftover weeks appeared after packing |
| Surface protected revision windows and recovery capacity already placed | Steal or redefine protections while “tidying” the plan for coaching |
| Record assumptions and commitments carried from upstream | Invent new commitments absent from timetable / blueprint / package |
| Carry explainability forward into plan-level speech | Invent readiness, mastery, or pass claims from calendar density |
| Enter lifecycle states (active, adapted, recovered, …) | Treat lifecycle labels as licence to rewrite educational law |

### 5.3 Completeness before coaching consumption

If the Scheduling Engine output is incomplete (e.g. unresolved overflow of mandatory components, infeasible blueprint theatre, missing protection placements), **no complete Canonical Study Plan may be published for coaching consumption**.

Incomplete or invalid timetables yield incomplete, draft-only, or refused plans — not invented completeness.

### 5.4 Educational determinism

Given the same complete Scheduling Engine output (same placements, protections, overflow record, and explainability attachments), the Canonical Study Plan must present the same educational posture.

Variation is allowed only when:

- the timetable changes (lawful rescheduling under MS006); or
- upstream educational law changes (re-package / re-blueprint / re-allocate); or
- the plan’s educational lifecycle state changes under `STUDY_PLAN_LIFECYCLE.md`.

---

## 6. Tutor Posture (Binding Metaphor)

When presenting a completed Study Plan, the system must behave as an expert IFoA tutor would:

1. **Schedule before promising.** No plan commitment exists without lawful timetable warrant.
2. **One story.** The student hears one journey — not conflicting mission, dashboard, and plan narratives.
3. **Protect what was reserved.** Revision, buffers, and recovery remain visible commitments.
4. **Separate coverage from competence.** Scheduled study advances honest work; it does not declare mastery.
5. **Name change conditions.** Students know when adaptation, recovery, or replan will occur.
6. **Escalate honestly.** When the plan no longer fits remaining capacity or educational envelopes, say so — then seek upstream replan — rather than silent impossible compression disguised as “the same plan.”
7. **Explain the whole.** Students should understand *why this plan exists* and *why it looks like this*.
8. **Refuse forbidden representation.** Consuming protected revision for first-pass theatre, packing into leave, punishment catch-up, and hidden infeasibility remain unlawful at plan layer.
9. **Leave daily modes intact.** Plan phase emphasis does not silently commandeer Learning Mode topic authority.
10. **Dispose the container, keep the history.** Superseding or archiving a plan never erases rightful Study Progress or evidence posture.

---

## 7. Position in the Master Planner Stack

```
STUDENT EDUCATIONAL PROFILE (MS002)
     ↓  diagnosis: where the student is now
EDUCATIONAL STRATEGY (MS003)
     ↓  approach: how we should teach / coach this sitting
EDUCATIONAL PLANNING MODEL (MS001)
     ↓  design law: phases, objectives, constraints, decision classes
PLANNING DECISION ENGINE (MS004)
     ↓  structured educational decisions
PLANNING DECISION PACKAGE
     ↓  organised into journey structure
PLANNING BLUEPRINT (MS005)
     ↓  allocated onto calendar
SCHEDULING ENGINE (MS006)
     ↓
STUDY TIMETABLE
     ↓  educational representation of successful allocation
CANONICAL STUDY PLAN (MS007 — this corpus)
     ↓
DAILY COACH (Programme VI / Workstream 2)
     ↓  today’s educational guidance
DOWNSTREAM EXPERIENCE
     (missions, sessions, advisory, analytics, narration —
      educational consumers; implementation deferred)
```

| Horizon | Job | Question |
|---------|-----|----------|
| **MS002 — Profile** | Diagnose | Who is this student educationally? |
| **MS003 — Strategy** | Choose approach | Which overall educational strategy should we adopt? |
| **MS001 — Planning Model** | Define design law | What must lawful journey design respect? |
| **MS004 — Decision Engine** | Decide | What planning decisions follow for this student now? |
| **MS005 — Blueprint** | Organise | What date-independent journey structure do those decisions form? |
| **MS006 — Scheduling** | Allocate | How does that structure map onto real weeks, days, and sessions? |
| **MS007 — Study Plan** | Contract | What educational artefact do all coaching systems consume? |
| **Daily Coach (WS2)** | Prioritise today | What is most educationally valuable to do today under that contract? |

Binding rule for future algorithms and coaching surfaces:

> **Consume a Canonical Study Plan derived from Scheduling Engine output before coaching against a long-term preparation frame.**  
> Surfaces that invent phases, revision windows, intensity envelopes, or commitments reinvent educational reasoning downstream of packing.  
> **Daily Coach interprets the contract for today — it must never invalidate or silently rewrite it.**

---

## 8. Required Sections

Every complete Canonical Study Plan must include the following **educational sections** (meanings — not implementation fields):

1. **Identity binding** — examination, sitting, strategy ID, blueprint binding, and timetable binding carried forward.
2. **Feasibility posture** — inherits package / blueprint / timetable feasibility; must not present complete plan theatre over an infeasible journey.
3. **Profile & strategy alignment statement** — explicit carrying-forward of the Profile and Strategy postures that authorised the journey (no re-diagnosis).
4. **Phase structure** — ordered educational phases as allocated on the calendar (see `STUDY_PLAN_COMPONENTS.md`).
5. **Session & study commitment inventory** — concrete study sessions / blocks the student is asked to honour.
6. **Protection regions** — revision windows, buffers, recovery capacity, and rest / freshness commitments as first-class plan elements.
7. **Milestones & checkpoints** — legible educational markers already authorised upstream.
8. **Assumptions** — capacity, leave, holidays, evidence thinness, and other assumptions the plan rests on.
9. **Educational commitments** — what the plan promises educationally (and what it refuses to promise).
10. **Lifecycle posture** — current educational state under `STUDY_PLAN_LIFECYCLE.md`.
11. **Validation posture** — result of checks under `STUDY_PLAN_VALIDATION.md`.
12. **Explainability attachments** — plan-level plain-language reasons (see `STUDY_PLAN_EXPLAINABILITY.md`).
13. **Traceability** — every material element cites timetable / blueprint / package IDs and inherits Profile + Strategy + Planning Model traces.
14. **Change conditions** — under what educational circumstances the plan will adapt, recover, escalate, be superseded, or archived.
15. **Continuity notice** — learner history ownership remains with the student; the plan is a disposable container.

### 8.1 Completeness rule

A Study Plan that shows first-pass ambition by consuming the protected revision region, or that presents a complete theatre while upstream marked the sitting infeasible, or that cannot explain why it exists, is educationally incomplete — even if every calendar cell looks filled.

### 8.2 What the plan sections are not

- Database columns or API payloads
- Generated lesson content
- Pass/fail probability claims
- A substitute for Learning Mode daily topic authority
- A second blueprint with different educational meaning

---

## 9. Educational Integrity

Educational integrity for the Canonical Study Plan means:

| Integrity duty | Failure mode |
|----------------|--------------|
| **One educational story** | Mission says one thing; plan roadmap invents another journey |
| **Honest claim types** | Plan density narrated as mastery or guaranteed pass |
| **Protection visibility** | Revision / buffer / recovery disappear from student-facing plan speech |
| **Traceability** | Sessions or phases with no timetable / blueprint warrant |
| **Continuity** | Plan delete/archive erases Study Progress or invents cold-start theatre |
| **Non-invention** | Coaching layer “improves” the plan by inventing educational structure |
| **Mode humility** | Plan phase emphasis silently steals Learning Mode topic authority |
| **Infeasibility speech** | Overflow or infeasible sitting hidden behind a complete-looking plan |

Relationship to EL-011: the Registry already defines Study Plan as the student’s authorised study context. This corpus **deepens** that meaning for Master Planner output — the completed educational contract after scheduling — without contradicting EL-011 ownership, continuity, or non-mastery rules.

---

## 10. Interaction With Downstream Systems

| Consumer | May use the Study Plan to… | Must not use it to… |
|----------|----------------------------|---------------------|
| Daily mission / session systems | Respect phase emphasis, intensity envelopes, and scheduled commitments | Silently commandeer Learning Mode topic authority |
| Recommendation / advisory layers | Advise within plan + blueprint envelopes | Override mandatory protections via “helpful” local rewrites |
| Student-facing narration | Explain why the plan exists and how it is structured | Claim mastery or guaranteed pass from schedule density |
| Analytics / progress surfaces | Summarise coverage and adherence against the plan frame | Conflate Study Progress with Estimated Mastery |
| Future Runtime A study-plan services | Persist and serve the educational contract | Invent educational structure during storage or UI packing |
| Recovery / reschedule flows | Represent adapted / recovered postures after lawful MS006 moves | Invent new educational law during “catch-up” |

The Study Plan sets the lawful educational contract. It does not replace constitutional daily authorities or upstream educational law.

---

## 11. Out of Scope (MS007)

This milestone does **not**:

- implement Runtime A study-plan services, database models, or APIs;
- define software classes, serialisation, or feature flags;
- introduce numeric weighting, ML classifiers, or scheduling algorithms;
- invent educational reasoning beyond representing Scheduling Engine output;
- modify Runtime A application code.

Documentation of educational meaning only.

---

## 12. Success Condition

MS007 is complete when every future subsystem can treat this corpus as the authoritative educational contract for a completed Study Plan without redefining:

- what a Study Plan is educationally;
- which structural components it contains and why;
- how it lives, adapts, recovers, completes, supersedes, and archives;
- what makes it educationally valid;
- how it is explained to students.

The Canonical Study Plan’s responsibility is **faithful educational representation of successful scheduling** — shared across the Kwalitec ecosystem.

---

## 13. Cross References

- `STUDY_PLAN_COMPONENTS.md` — educational building blocks
- `STUDY_PLAN_LIFECYCLE.md` — educational lifecycle states
- `STUDY_PLAN_VALIDATION.md` — educational validity gates
- `STUDY_PLAN_EXPLAINABILITY.md` — student-facing plan justification
- `../scheduling/SCHEDULING_ENGINE.md` — sole educational input authority
- `../scheduling/RESCHEDULING_POLICY.md` — lawful timetable adaptation that plans may represent
- `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md` — journey structure authority
- `../EDUCATIONAL_CONTINUITY_STANDARD.md` — history survival across plan change
- `../EDUCATIONAL_LOGIC_REGISTRY.md` — EL-011 Study Plan registry entry
