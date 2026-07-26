# Educational Strategy Framework

**Programme:** VI — Master Planner  
**Milestone:** MS003 — Educational Strategy Framework  
**Classification:** Educational strategy layer — bridge from diagnosis to long-term planning  
**Status:** APPROVED — governing for educational strategy reasoning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how an excellent IFoA tutor chooses an overall educational approach** before constructing a long-term study plan.

It answers *which educational strategy should be adopted*, *why*, and *when it should change*, given the Student Educational Profile.

It does **not** generate study plans, schedules, recommendations, or Runtime A services.

> **This framework is educational strategy.  
> Future Master Planner algorithms determine strategy before generating any study plan — they never invent strategy meaning absent from this corpus.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
5. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / MS002)
6. [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) (Programme VI / MS001)

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_STRATEGY_FRAMEWORK.md`](EDUCATIONAL_STRATEGY_FRAMEWORK.md) | Constitutional overview: what strategy is, tutor posture, stack position |
| [`STRATEGY_CATALOGUE.md`](STRATEGY_CATALOGUE.md) | Named IFoA educational strategies and meanings |
| [`STRATEGY_SELECTION_MODEL.md`](STRATEGY_SELECTION_MODEL.md) | How Profile diagnosis drives strategy choice |
| [`STRATEGY_TRANSITIONS.md`](STRATEGY_TRANSITIONS.md) | When and why strategy changes |
| [`STRATEGY_EXPLAINABILITY.md`](STRATEGY_EXPLAINABILITY.md) | How strategy must be justified to students |

## Relationship to MS001 and MS002

| Horizon | Job |
|---------|-----|
| **MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **MS003 — this corpus** | Choose *which overall educational strategy to adopt* |
| **MS001 — Educational Planning Model** | Define *how the journey should be constructed* under that strategy |
| **MS004 — Planning Decision Engine** | Produce *structured planning decisions* before any timetable |

```
Profile (diagnosis)
     →  Strategy (approach)
           →  Planning Model (design law)
                 →  Planning Decision Engine (decisions)
                       →  Future plan generation (out of scope)
```

Planning without strategy invents approach in scheduling code.  
Strategy without profile invents the student.  
Plan generation without the Decision Engine reinvents educational reasoning in calendar code.

## Out of scope (MS003)

- Study plan generation or rebalancing code
- Scheduling / optimisation algorithms
- Recommendation engines
- Database models, feature flags, or Runtime A integration
- Collection UX for profile inputs
- Numeric scoring or ML classifiers for strategy choice

## How to use this corpus

1. Read `EDUCATIONAL_STRATEGY_FRAMEWORK.md` first.
2. Treat the Catalogue as the only lawful student-facing strategy vocabulary.
3. Select strategy from the Profile using `STRATEGY_SELECTION_MODEL.md` — never arbitrary rules detached from diagnosis.
4. Expect strategy to change only under `STRATEGY_TRANSITIONS.md`.
5. Require explainability contracts from `STRATEGY_EXPLAINABILITY.md` before student-facing strategy narration.
6. Do not implement planning algorithms that skip strategy determination.
7. Do not implement algorithms that contradict this corpus without amending it first.
