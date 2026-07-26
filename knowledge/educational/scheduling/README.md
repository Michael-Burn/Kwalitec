# Scheduling Engine

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Allocation specification — bridge from Planning Blueprint to concrete study timetable  
**Status:** APPROVED — governing for calendar allocation mechanics  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how an approved Planning Blueprint is placed onto a student’s real calendar** while respecting educational constraints already settled upstream and practical availability declared by the student.

It answers *how phases and components become weeks, days, and sessions*, *which allocation rules are deterministic*, *how leave and holidays are handled*, *how the timetable adapts when reality diverges*, and *how placement is explained*.

It does **not** invent educational structure, diagnose students, choose strategy, produce planning decisions, or implement Runtime A services.

> **This engine performs allocation only.  
> Educational reasoning remains upstream.  
> Future scheduling algorithms place an approved Planning Blueprint onto a calendar — they never invent educational structure in packing code.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
5. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / MS002)
6. [`../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`](../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md) (Programme VI / MS003)
7. [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) (Programme VI / MS001)
8. [`../planning_engine/PLANNING_DECISION_ENGINE.md`](../planning_engine/PLANNING_DECISION_ENGINE.md) (Programme VI / MS004)
9. [`../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md`](../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md) (Programme VI / MS005)

Sole educational input for allocation:

- **Planning Blueprint** produced under MS005 — the complete date-independent study journey structure for a named sitting

Practical inputs for allocation (non-educational reasoning):

- Declared study availability (days, hours, preferred session windows)
- Known leave and holiday periods
- Sitting / exam date (already bound in the blueprint / package)
- Observed calendar divergence events (missed sessions, illness, extra time) for rescheduling

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map

## Contents

| Document | Role |
|---|---|
| [`SCHEDULING_ENGINE.md`](SCHEDULING_ENGINE.md) | Constitutional overview: what the engine is, stack position, allocation-only rule |
| [`SCHEDULING_RULES.md`](SCHEDULING_RULES.md) | Deterministic allocation rules that preserve blueprint intent |
| [`CALENDAR_ALLOCATION.md`](CALENDAR_ALLOCATION.md) | How phases and components map onto weeks, days, sessions, and blocks |
| [`SCHEDULING_CONSTRAINTS.md`](SCHEDULING_CONSTRAINTS.md) | Hard calendar and capacity constraints the allocator must honour |
| [`RESCHEDULING_POLICY.md`](RESCHEDULING_POLICY.md) | How the timetable adapts when reality diverges from the plan |
| [`SCHEDULING_EXPLAINABILITY.md`](SCHEDULING_EXPLAINABILITY.md) | How placement and timetable changes are explained to students |

## Relationship to MS001–MS005

| Horizon | Job |
|---------|-----|
| **MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **MS003 — Educational Strategy** | Choose *which overall educational approach to adopt* |
| **MS001 — Educational Planning Model** | Define *design law* (objectives, constraints, phases, decision classes) |
| **MS004 — Planning Decision Engine** | Produce *structured planning decisions* (Planning Decision Package) |
| **MS005 — Planning Blueprint** | Organise those decisions into a *date-independent study journey* |
| **MS006 — this corpus** | Allocate that journey onto a *concrete, explainable timetable* |

```
Profile (diagnosis)
     →  Strategy (approach)
           →  Planning Model (design law)
                 →  Planning Decision Engine
                       →  Planning Decision Package
                             →  Planning Blueprint
                                   →  Scheduling Engine (this milestone)
                                         →  Study Timetable
                                               →  Canonical Study Plan (MS007)
                                                     (Runtime A integration out of scope)
```

MS005 settles *what educational structure* must be placed.  
MS006 places that structure onto *real calendar capacity* — without inventing new educational meaning.

Downstream educational contract (Programme VI):

- [`../study_plan/`](../study_plan/) — Canonical Study Plan Model (MS007)

## Architectural requirement

Every scheduling decision must be **traceable back to the Planning Blueprint** (and through it to the Planning Decision Package and MS001–MS004 law).

| Lawful | Unlawful |
|--------|----------|
| Place blueprint phases and components onto calendar cells honouring envelopes | Invent phases, components, intensity, or revision meaning in packing code |
| Split a learning block across study days without changing order | Reorder first-pass topics for “engagement” or optimiser convenience |
| Honour leave, holidays, and declared availability as zero/reduced capacity | Pack normal load into unavailable windows to make the plan “fit” |
| Consume buffer / insert recovery *as the blueprint already authorised* when slip occurs | Steal protected revision or invent recovery law absent from the blueprint |
| Explain placement using blueprint + capacity facts | Invent readiness, mastery, or pass claims from calendar density |

If a scheduling rule appears to require new educational judgement, **that judgement belongs upstream** and must not be introduced here.

## Out of scope (MS006)

- Runtime A integration or study-plan service implementation
- Database models, feature flags, or APIs
- Calendar UI / student-facing screens
- Optimisation algorithms, ML classifiers, or numeric weighting schemes
- New educational reasoning (diagnosis, strategy, decisions, blueprint structure)
- Software class designs or service interfaces

## How to use this corpus

1. Read `SCHEDULING_ENGINE.md` first.
2. Apply deterministic placement via `SCHEDULING_RULES.md`.
3. Map structure onto calendar units with `CALENDAR_ALLOCATION.md`.
4. Gate publication with `SCHEDULING_CONSTRAINTS.md`.
5. Handle divergence with `RESCHEDULING_POLICY.md` — preserve blueprint intent; escalate upstream when educational law must change.
6. Require explainability contracts from `SCHEDULING_EXPLAINABILITY.md` before student-facing timetable narration.
7. Do not implement packing that invents phases, intensity envelopes, or revision protection outside an approved Planning Blueprint.
8. Do not implement algorithms that contradict this corpus without amending it first.
