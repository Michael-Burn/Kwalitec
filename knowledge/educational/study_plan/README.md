# Canonical Study Plan Model

**Programme:** VI — Master Planner  
**Milestone:** MS007 — Canonical Study Plan Model  
**Classification:** Educational artefact specification — completed Study Plan as coaching contract  
**Status:** APPROVED — governing for Study Plan educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **what a Study Plan is after successful scheduling** — the educational content, structure, lifecycle, validation, and explainability of the completed artefact.

It answers *what educational contract downstream coaching must honour*, *which structural components compose a lawful plan*, *how the plan lives and changes educationally*, *what makes it valid*, and *how it is explained to students*.

It does **not** invent educational structure, diagnose students, choose strategy, produce planning decisions, allocate calendars, or implement Runtime A services.

> **The Study Plan is derived entirely from Scheduling Engine output.  
> It introduces no new educational reasoning or scheduling behaviour.  
> Every future subsystem treats this corpus as the authoritative educational contract for planning.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / MS002)
7. [`../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`](../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md) (Programme VI / MS003)
8. [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) (Programme VI / MS001)
9. [`../planning_engine/PLANNING_DECISION_ENGINE.md`](../planning_engine/PLANNING_DECISION_ENGINE.md) (Programme VI / MS004)
10. [`../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md`](../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md) (Programme VI / MS005)
11. [`../scheduling/SCHEDULING_ENGINE.md`](../scheduling/SCHEDULING_ENGINE.md) (Programme VI / MS006)

Sole educational input for derivation:

- **Scheduling Engine output** — an approved Study Timetable produced under MS006 from an approved Planning Blueprint

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map

## Contents

| Document | Role |
|---|---|
| [`CANONICAL_STUDY_PLAN.md`](CANONICAL_STUDY_PLAN.md) | Constitutional overview: what the Study Plan is, guarantees, integrity, stack position |
| [`STUDY_PLAN_COMPONENTS.md`](STUDY_PLAN_COMPONENTS.md) | Educational building blocks of a completed plan (phases, sessions, protections, commitments) |
| [`STUDY_PLAN_LIFECYCLE.md`](STUDY_PLAN_LIFECYCLE.md) | Educational lifecycle states and lawful transitions |
| [`STUDY_PLAN_VALIDATION.md`](STUDY_PLAN_VALIDATION.md) | What makes a Study Plan educationally valid |
| [`STUDY_PLAN_EXPLAINABILITY.md`](STUDY_PLAN_EXPLAINABILITY.md) | How a completed plan is explained to students |

## Relationship to MS001–MS006

| Horizon | Job |
|---------|-----|
| **MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **MS003 — Educational Strategy** | Choose *which overall educational approach to adopt* |
| **MS001 — Educational Planning Model** | Define *design law* (objectives, constraints, phases, decision classes) |
| **MS004 — Planning Decision Engine** | Produce *structured planning decisions* (Planning Decision Package) |
| **MS005 — Planning Blueprint** | Organise those decisions into a *date-independent study journey* |
| **MS006 — Scheduling Engine** | Allocate that journey onto a *concrete, explainable timetable* |
| **MS007 — this corpus** | Define the *canonical educational artefact* consumed by downstream coaching |

```
Profile (diagnosis)
     →  Strategy (approach)
           →  Planning Model (design law)
                 →  Planning Decision Engine
                       →  Planning Decision Package
                             →  Planning Blueprint
                                   →  Scheduling Engine
                                         →  Study Timetable
                                               →  Canonical Study Plan (this milestone)
                                                     →  Daily Coach (Programme VI / Workstream 2)
                                                           (mission / session consumers later)
```

MS006 settles *where authorised work sits on the calendar*.  
MS007 defines *what that completed artefact means educationally* as the shared contract — without inventing new educational meaning.  
Daily Coach (Workstream 2) interprets that contract for *today’s* educational priority — without redesigning the plan.

## Architectural requirement

Every element of a Canonical Study Plan must be **derived entirely from Scheduling Engine output** (and the MS001–MS006 authorities that output already cites).

| Lawful | Unlawful |
|--------|----------|
| Represent timetable phases, sessions, protections, and explainability as the plan contract | Invent phases, intensity, revision meaning, or recovery law at plan layer |
| Name educational commitments already authorised upstream | Add new educational reasoning, triage, or scheduling behaviour |
| Carry Profile / Strategy / Blueprint / Timetable traces forward | Re-diagnose the student or re-select strategy while “finalising” the plan |
| Explain the completed plan to students | Claim mastery or guaranteed pass from calendar density |

If a plan element appears to require new educational judgement, **that judgement belongs upstream** and must not be introduced here.

## Out of scope (MS007)

- Database models, schemas, or ORM entities
- Runtime A integration, feature flags, or services
- Serialisation formats or API contracts
- Scheduling algorithms, optimisation, or packing heuristics
- New educational reasoning (diagnosis, strategy, decisions, blueprint structure, allocation)
- Software class designs or service interfaces

## How to use this corpus

1. Read `CANONICAL_STUDY_PLAN.md` first.
2. Treat components in `STUDY_PLAN_COMPONENTS.md` as the complete educational inventory of a completed plan.
3. Apply lifecycle meaning from `STUDY_PLAN_LIFECYCLE.md` — educational posture, not database enums alone.
4. Gate publication and coaching consumption with `STUDY_PLAN_VALIDATION.md`.
5. Require explainability contracts from `STUDY_PLAN_EXPLAINABILITY.md` before student-facing plan narration.
6. Do not implement coaching that invents plan structure outside a Study Plan derived from lawful Scheduling Engine output.
7. Consume plan meaning via [`../daily_coach/`](../daily_coach/) for day-to-day educational priority — Daily Coach must not redesign this contract.
8. Do not implement algorithms that contradict this corpus without amending it first.
