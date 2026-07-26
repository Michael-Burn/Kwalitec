# Planning Decision Engine

**Programme:** VI — Master Planner  
**Milestone:** MS004 — Planning Decision Engine  
**Classification:** Educational decision engine — bridge from diagnosis and strategy to structured planning decisions  
**Status:** APPROVED — governing for educational planning-decision reasoning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how an excellent IFoA tutor transforms educational diagnosis into educational planning decisions** before any timetable or schedule is constructed.

It answers *what planning decisions should be made*, *in what reasoning order*, *how conflicts are resolved*, and *how each decision is explained*.

It does **not** generate study plans, calendars, optimisation runs, or Runtime A services.

> **This engine produces planning decisions.  
> Future planning algorithms consume these decisions — they never redefine educational reasoning in scheduling code.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
5. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / MS002)
6. [`../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`](../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md) (Programme VI / MS003)
7. [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) (Programme VI / MS001)

Companion decision catalogue (what may be decided):

- [`../planning/PLANNING_DECISION_MODEL.md`](../planning/PLANNING_DECISION_MODEL.md) — mandatory / adaptive / forbidden decision classes

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map

## Contents

| Document | Role |
|---|---|
| [`PLANNING_DECISION_ENGINE.md`](PLANNING_DECISION_ENGINE.md) | Constitutional overview: inputs, outputs, tutor posture, stack position |
| [`DECISION_PIPELINE.md`](DECISION_PIPELINE.md) | Complete educational reasoning sequence and decision catalogue |
| [`DECISION_PRIORITY_MODEL.md`](DECISION_PRIORITY_MODEL.md) | How conflicting educational objectives are prioritised |
| [`DECISION_CONFLICT_RESOLUTION.md`](DECISION_CONFLICT_RESOLUTION.md) | How an expert tutor resolves planning conflicts |
| [`DECISION_EXPLAINABILITY.md`](DECISION_EXPLAINABILITY.md) | How every planning decision must be justified to students |

## Relationship to MS001–MS003

| Horizon | Job |
|---------|-----|
| **MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **MS003 — Educational Strategy** | Choose *which overall educational approach to adopt* |
| **MS001 — Educational Planning Model** | Define *how the journey should be constructed* (objectives, constraints, phases, decision classes) |
| **MS004 — this corpus** | Produce *structured planning decisions* from Profile + Strategy + Planning Model |

```
Profile (diagnosis)
     →  Strategy (approach)
           →  Planning Model (design law)
                 →  Planning Decision Engine (this milestone)
                       →  Planning Decision Package
                             →  Planning Blueprint (MS005)
                                   →  Scheduling Engine (MS006)
```

MS001 defines the educational law of planning.  
MS004 applies that law, under a chosen strategy, to a diagnosed student — and stops at decisions.  
MS005 organises those decisions into date-independent journey structure — still before any calendar.  
MS006 allocates that structure onto a concrete timetable — without inventing educational meaning.

Downstream journey structure and allocation (Programme VI):

- [`../planning_blueprint/`](../planning_blueprint/) — Planning Blueprint Model (MS005)
- [`../scheduling/`](../scheduling/) — Scheduling Engine Specification (MS006)

## Architectural requirement

Every educational decision this engine produces must be traceable back to:

1. **Student Educational Profile** — diagnosis that warrants the decision  
2. **Educational Strategy** — approach that privileges or refuses the emphasis  
3. **Educational Planning Model** — objective, constraint, phase, or decision class that authorises it  

No decision may exist without an educational justification.

## Out of scope (MS004)

- Study plan generation or rebalancing code
- Scheduling / calendar generation
- Optimisation algorithms or numeric weighting schemes
- Recommendation engines
- Database models, feature flags, or Runtime A integration
- Collection UX for profile or planning inputs
- Software class designs or service interfaces

## How to use this corpus

1. Read `PLANNING_DECISION_ENGINE.md` first.
2. Trace reasoning through `DECISION_PIPELINE.md` — do not invent parallel pipelines in code.
3. Resolve objective tension with `DECISION_PRIORITY_MODEL.md` (educational reasoning only — no numeric weights).
4. Apply `DECISION_CONFLICT_RESOLUTION.md` when life, time, or adherence breaks the intended trajectory.
5. Require explainability contracts from `DECISION_EXPLAINABILITY.md` before student-facing decision narration.
6. Do not implement algorithms that schedule work without first producing (or consuming) decisions authorised here.
7. Do not implement algorithms that contradict this corpus without amending it first.
