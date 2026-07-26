# Educational Planning Model

**Programme:** VI — Master Planner  
**Milestone:** MS001 — Educational Planning Model  
**Classification:** Educational decision framework — constitutional reference for long-term study planning  
**Status:** APPROVED — governing for educational planning reasoning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how an excellent IFoA tutor would design a student’s complete journey from registration until examination**.

It answers *what educational decisions should be made* when constructing a long-term study plan.

It does **not** implement study plan generation, scheduling algorithms, optimisation engines, or Runtime A services.

> **This model governs future planning algorithms.  
> Algorithms never invent educational meaning absent from this model.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)

Upstream diagnosis and strategy (Programme VI):

- [`../student_profile/`](../student_profile/) — Student Educational Profile (MS002) — educational diagnosis consumed before strategy and planning
- [`../strategy/`](../strategy/) — Educational Strategy Framework (MS003) — overall educational approach chosen before plan construction

Downstream decision production and journey structure (Programme VI):

- [`../planning_engine/`](../planning_engine/) — Planning Decision Engine (MS004) — transforms Profile + Strategy + this Planning Model into a Planning Decision Package (before any timetable)
- [`../planning_blueprint/`](../planning_blueprint/) — Planning Blueprint Model (MS005) — organises that package into a date-independent study journey structure (before any calendar)

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map
- [`knowledge/architecture/INTERVENTION_MODEL.md`](../../architecture/INTERVENTION_MODEL.md) — intervention vocabulary (separate programme)

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_PLANNING_MODEL.md`](EDUCATIONAL_PLANNING_MODEL.md) | Constitutional overview: journey phases, inputs, decision classes, tutor posture |
| [`PLANNING_OBJECTIVES.md`](PLANNING_OBJECTIVES.md) | What the plan must optimise educationally |
| [`PLANNING_CONSTRAINTS.md`](PLANNING_CONSTRAINTS.md) | Permanent constraints every plan must respect |
| [`PLANNING_DECISION_MODEL.md`](PLANNING_DECISION_MODEL.md) | Mandatory, adaptive, and forbidden educational decisions |
| [`PLANNING_ASSUMPTIONS.md`](PLANNING_ASSUMPTIONS.md) | Assumptions future algorithms may rely on — and must not |
| [`PLANNING_EXPLAINABILITY.md`](PLANNING_EXPLAINABILITY.md) | How planning decisions must be justified to students |

## Out of scope (MS001)

- Study plan generation or rebalancing code
- Scheduling / optimisation algorithms
- Recommendation engines
- Database models, feature flags, or Runtime A integration
- Collection UX for planning inputs

## How to use this corpus

1. Read `EDUCATIONAL_PLANNING_MODEL.md` first.
2. Treat objectives and constraints as binding when designing any planner.
3. Classify every proposed planning behaviour under the Decision Model (mandatory / adaptive / forbidden).
4. Require explainability contracts before shipping student-facing plan recommendations.
5. Determine educational strategy (MS003) before generating any study plan.
6. Produce planning decisions via the Planning Decision Engine (MS004) before generating any study plan.
7. Organise decisions into a Planning Blueprint (MS005) before allocating calendar cells.
8. Do not implement algorithms that contradict this corpus without amending it first.
