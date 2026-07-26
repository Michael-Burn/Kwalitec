# Scheduling Engine

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Highest allocation authority for calendar placement within Programme VI  
**Status:** APPROVED — governing for scheduling / timetable allocation  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Scheduling Engine** for Kwalitec.

It is subordinate to the Educational Constitution and specialised educational models. It governs **how an approved Planning Blueprint becomes a concrete study timetable**. It does not authorise implementation shortcuts that contradict the Constitution, and it does not invent educational meaning absent from the Planning Blueprint.

Authority order for Master Planner personalisation:

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Student Educational Profile (MS002) diagnoses who the student is educationally now.  
> Educational Strategy Framework (MS003) chooses which overall educational approach to adopt.  
> Educational Planning Model (MS001) defines how an expert tutor designs the journey under that strategy.  
> Planning Decision Engine (MS004) transforms Profile + Strategy + Planning Model into a Planning Decision Package.  
> Planning Blueprint (MS005) organises that package into a date-independent study journey.  
> **This Scheduling Engine (MS006) allocates that blueprint onto a realistic calendar.**  
> Runtime A study-plan services must consume this allocation law — never redefine educational structure while packing.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabuses such as CM1/CS1 and peers).

An expert IFoA tutor does not invent a new educational journey while filling a diary. After the journey structure is settled — phases, components, intensity envelopes, revision protection, buffers, recovery, milestones — the tutor answers a different class of question:

1. Given this student’s real available days and hours, where do these components fit?
2. How do we protect revision, buffers, and recovery *as already reserved* when packing the calendar?
3. How do rest days, leave, and holidays create zero- or reduced-capacity regions?
4. When the student misses a week or gains extra time, how do we move cells without rewriting educational law?
5. How do we explain why a session sits on Tuesday evening rather than inventing a story about “optimised learning”?

That product — a **Study Timetable** produced by faithful allocation — is what this Engine specifies.

> **The Scheduling Engine describes allocation mechanics.  
> It does not introduce educational reasoning.**

This document records that tutor posture so every future Master Planner packing algorithm has a single reference for *how blueprint becomes calendar*.

---

## 2. What the Scheduling Engine Is

The **Scheduling Engine** is the allocation process that maps an approved Planning Blueprint onto concrete calendar capacity.

| Input | Role |
|-------|------|
| **Planning Blueprint** | Settled educational journey structure (MS005) — phases, components, progression, envelopes, protection regions, explainability |
| **Study availability** | Declared days, hours, preferred windows, session-length preferences (practical, not educational diagnosis) |
| **Leave & holidays** | Known zero/reduced-capacity periods |
| **Sitting horizon** | Exam / sitting date already bound upstream |

into:

| Output | Role |
|--------|------|
| **Study Timetable** | Ordered calendar placement of blueprint components as weeks, days, sessions, and study blocks — with explainability attachments |

It answers:

| Question | Allocation answer |
|----------|-------------------|
| What gets placed? | Only blueprint phases and components already authorised |
| Where does it go? | Into available study capacity after leave, holidays, and rest rules |
| In what order? | Blueprint ordering and prerequisite sequencing preserved |
| What is protected? | Revision regions, buffers, recovery capacity, intensity envelopes |
| What is still deferred? | Runtime A persistence, UI, optimiser heuristics beyond deterministic rules |

The Engine is:

- **blueprint-faithful** — every placed cell traces to a blueprint element;
- **capacity-honest** — never exceeds declared available study time;
- **deterministically allocative** — same blueprint + same availability inputs yield the same timetable posture;
- **explainable** — students can understand why sessions appear where they do;
- **non-inventive** — allocates existing educational structure; does not add educational reasoning;
- **reschedule-capable** — adapts placement when reality diverges while preserving blueprint intent.

The Engine is **not**:

- a second Decision Engine, Strategy selector, or Profile diagnostician;
- a licence to invent phases, revision windows, or intensity bands during packing;
- a Learning Mode / Revision Mode switch (modes retain daily constitutional authority);
- a claim that following the timetable guarantees a pass;
- an optimisation contest that may violate educational constraints for a “better” packed calendar;
- a software class design or Runtime A service interface.

---

## 3. Allocation-Only Rule (Binding)

### 3.1 Sole educational input

Allocation consumes **only** an approved Planning Blueprint (and the MS001–MS005 authorities that blueprint already cites).

It must **not** introduce:

- new objectives, constraints, phases, or component meanings;
- new strategy privileges or Profile diagnoses;
- new sequencing, intensity, practice density, or feasibility judgements;
- new revision, buffer, or recovery *educational* law.

Practical facts (availability, leave, holidays, missed sessions, extra time) are **allocation inputs**. Using them to place or move cells is lawful. Using them to invent educational meaning is unlawful.

### 3.2 Organisation of time, not invention of education

| Engine may… | Engine must not… |
|-------------|-------------------|
| Map BP phases onto calendar regions honouring package-derived boundaries | Invent a “revision phase” because leftover weeks appeared |
| Split BC-01 across multiple study days without changing topic order | Reorder syllabus topics for engagement or packing density |
| Place BC-04 only inside the protected revision region | Cannibalise revision for unfinished first-pass by default |
| Leave BC-07 unused until slip occurs | Delete buffers to make an infeasible timetable look complete |
| Insert recovery *cells* when the blueprint already authorised BC-06 / PD-07 / PD-16 responses | Invent recovery pedagogy or punishment catch-up |
| Surface allocation infeasibility when capacity cannot host the blueprint | Quietly compress envelopes or hide impossibility |

### 3.3 Escalation upstream

If faithful allocation cannot place the blueprint without violating educational protections or capacity honesty:

1. **Do not invent** a new educational compromise in packing code.
2. **Surface** allocation infeasibility / overflow honestly.
3. **Escalate** to re-run of the Planning Decision Engine (and rebuild of the blueprint) when educational law must change — buffers, intensity, triage, sitting counsel.

Rescheduling that stays inside blueprint envelopes is allocation. Changing educational envelopes is upstream work.

### 3.4 Determinism of allocation

Given the same complete Planning Blueprint and the same practical availability / leave / holiday inputs, the Engine must produce the same timetable posture.

Variation is allowed only when:

- the blueprint changes (upstream re-package / re-blueprint); or
- practical inputs change (availability, leave, holidays); or
- observed divergence events trigger lawful rescheduling under `RESCHEDULING_POLICY.md`.

Random topic shuffling, stochastic “variety,” or opaque optimiser churn of educational order is forbidden.

---

## 4. Tutor Posture (Binding Metaphor)

When allocating a timetable, the system must behave as an expert IFoA tutor would:

1. **Structure before packing.** No calendar cell invents a mission the blueprint never authorised.
2. **Work backwards from the sitting in dates.** Place protected revision and final-approach regions first as calendar regions because the blueprint reserved them — not because packing leftovers happened to remain.
3. **Honour official order.** First-pass learning cells follow blueprint sequencing; prerequisites are never skipped for packing convenience.
4. **Fit real life.** Place work only where the student declared availability; leave and holidays are capacity truth.
5. **Protect sustainability.** Respect intensity envelopes; prefer rest and recovery capacity already in the blueprint over heroic seven-day grind.
6. **Prefer buffers over fiction.** Use reserved buffer when slip occurs; do not pretend missed weeks never happened.
7. **Escalate honestly.** When the blueprint no longer fits remaining capacity, say so — then seek upstream replan — rather than silent impossible compression.
8. **Explain placement.** Students should understand *why this session is here* and *why the timetable moved*.
9. **Refuse forbidden packing.** Consuming protected revision for first-pass by default, packing into leave, punishment catch-up, and hidden infeasibility remain unlawful at scheduling layer.
10. **Leave daily modes intact.** Timetable phase emphasis does not silently commandeer Learning Mode topic authority.

---

## 5. Position in the Master Planner Stack

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
SCHEDULING ENGINE (MS006 — this corpus)
     ↓
STUDY TIMETABLE
     ↓  educational representation of successful allocation
CANONICAL STUDY PLAN (MS007)
     (Runtime A consumption out of scope for MS006)
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

Binding rule for future algorithms:

> **Consume an approved Planning Blueprint before allocating calendar cells.**  
> Timetables that invent phases, revision windows, or intensity envelopes reinvent educational reasoning in packing code.

---

## 6. Timetable Contents (Required)

Every complete Study Timetable must include:

1. **Blueprint binding** — identity of the approved Planning Blueprint (examination, sitting, strategy ID carried forward).
2. **Feasibility posture** — inherits blueprint / package feasibility; allocation must not present a complete timetable theatre over an infeasible blueprint.
3. **Horizon anchors** — start reference, sitting / exam date, and known leave / holiday capacity map.
4. **Availability map** — declared study days, hours, and session windows used for placement.
5. **Phase calendar regions** — blueprint phases mapped onto contiguous or interleaved calendar spans honouring order and protection.
6. **Session / block inventory** — concrete placements of BC-01…BC-14 instances (as applicable) into weeks, days, and study blocks.
7. **Protection placements** — revision region, buffers, recovery, and rest capacity placed as first-class calendar capacity — not residual scraps.
8. **Overflow / infeasibility record** — explicit statement of any components that could not be placed lawfully, or confirmation that placement completed inside capacity.
9. **Explainability attachments** — placement-level and change-level plain-language reasons (see `SCHEDULING_EXPLAINABILITY.md`).
10. **Traceability** — every material session cites blueprint phase/component IDs (BP-XX / BC-XX) and inherits package / Profile / Strategy traces already on those elements.

### 6.1 Completeness rule

A timetable that places first-pass ambition by consuming the protected revision region, or that packs normal load into declared leave, or that presents a complete theatre while the blueprint marked the sitting infeasible, is allocation-invalid — even if every calendar cell looks filled.

### 6.2 What the timetable is not

- New educational diagnosis or strategy
- A second blueprint with different phases
- Generated lesson content
- Pass/fail probability claims
- A substitute for Learning Mode daily topic authority
- A Runtime A database schema

---

## 7. Core Allocation Concerns

The Engine must address the following mechanical concerns (detail in companion documents):

| Concern | Document |
|---------|----------|
| Weekly allocation of component load | `CALENDAR_ALLOCATION.md` |
| Session placement within available windows | `CALENDAR_ALLOCATION.md` |
| Rest day handling | `SCHEDULING_RULES.md`, `SCHEDULING_CONSTRAINTS.md` |
| Revision block placement | `SCHEDULING_RULES.md`, `CALENDAR_ALLOCATION.md` |
| Buffer utilisation | `RESCHEDULING_POLICY.md` |
| Recovery insertion on the calendar | `RESCHEDULING_POLICY.md` |
| Leave periods | `SCHEDULING_CONSTRAINTS.md` |
| Holiday handling | `SCHEDULING_CONSTRAINTS.md` |
| Study availability | `CALENDAR_ALLOCATION.md`, `SCHEDULING_CONSTRAINTS.md` |

---

## 8. Interaction With Downstream Systems

| Consumer | May use the timetable to… | Must not use it to… |
|----------|---------------------------|---------------------|
| Future Runtime A study-plan services | Persist and serve allocated sessions | Invent educational structure during packing |
| Daily mission / session systems | Respect scheduled phase emphasis and intensity envelopes | Silently commandeer Learning Mode topic authority |
| Student-facing narration | Explain why sessions sit where they do | Claim mastery or guaranteed pass from calendar density |
| Recommendation / advisory layers | Advise within timetable + blueprint envelopes | Override mandatory blueprint protections via “helpful” packing tweaks |

The timetable sets lawful calendar placement. It does not replace constitutional daily authorities or upstream educational law.

---

## 9. Out of Scope (MS006)

This milestone does **not**:

- implement Runtime A scheduling services, calendar UI, or database models;
- define software classes, APIs, or feature flags;
- introduce numeric weighting, ML classifiers, or optimisation algorithms beyond deterministic allocation rules;
- invent educational reasoning beyond placing the Planning Blueprint;
- modify Runtime A application code.

Documentation of allocation mechanics only.

---

## 10. Success Condition

MS006 is complete when future packing algorithms can consume an approved Planning Blueprint under this Engine without redefining:

- which educational phases and components exist and why;
- intensity, revision, buffer, and recovery law;
- sequencing and prerequisite order;
- how placement and rescheduling are explained.

The Scheduling Engine’s responsibility is **faithful execution of the blueprint within real-world constraints**.

---

## 11. Cross References

- `SCHEDULING_RULES.md` — deterministic allocation rules
- `CALENDAR_ALLOCATION.md` — weeks, days, sessions, blocks
- `SCHEDULING_CONSTRAINTS.md` — hard capacity and calendar constraints
- `RESCHEDULING_POLICY.md` — adaptation when reality diverges
- `SCHEDULING_EXPLAINABILITY.md` — student-facing placement justification
- `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md` — blueprint authority
- `../planning_blueprint/BLUEPRINT_COMPONENTS.md` — what may be placed
- `../planning/PLANNING_CONSTRAINTS.md` — educational constraints the allocator must not violate
