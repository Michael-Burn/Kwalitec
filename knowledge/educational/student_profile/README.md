# Student Educational Profile

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Educational diagnosis specification — canonical student educational state before long-term planning  
**Status:** APPROVED — governing for educational profile meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec understands a student’s current academic state** before generating any long-term study plan.

It answers *what an experienced IFoA tutor wants to know* before recommending any study strategy.

It does **not** generate plans, schedules, recommendations, or Runtime A services.

> **This profile is educational diagnosis.  
> Future Master Planner algorithms personalise journeys by consulting this profile — they never invent educational meaning absent from it.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
4. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
5. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
6. [`planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) (Programme VI / MS001)

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map
- Digital Twin / Runtime educational state stores — implementation concerns, not profile law

## Contents

| Document | Role |
|---|---|
| [`STUDENT_EDUCATIONAL_PROFILE.md`](STUDENT_EDUCATIONAL_PROFILE.md) | Canonical overview: what the profile is, tutor posture, relationship to planning |
| [`PROFILE_DIMENSIONS.md`](PROFILE_DIMENSIONS.md) | Educational dimensions required to understand a student |
| [`PROFILE_INPUTS.md`](PROFILE_INPUTS.md) | Where educational evidence and declarations for the profile originate |
| [`PROFILE_STATES.md`](PROFILE_STATES.md) | Named educational states and their meaning |
| [`PROFILE_EVOLUTION.md`](PROFILE_EVOLUTION.md) | How the profile grows, stalls, recovers, and ages over time |
| [`PROFILE_EXPLAINABILITY.md`](PROFILE_EXPLAINABILITY.md) | How the profile must be explained in plain language |

## Relationship to MS001 and MS003

| Horizon | Job |
|---------|-----|
| **MS002 — this corpus** | Diagnose *where the student is now* educationally |
| **MS003 — strategy corpus** | Choose *which overall educational strategy to adopt* |
| **MS001 — planning corpus** | Design *how the journey should be constructed* under that strategy |

Downstream:

- [`../strategy/`](../strategy/) — Educational Strategy Framework (consumes this Profile)
- [`../planning/`](../planning/) — Educational Planning Model (consumes strategy + this Profile)

Planning without diagnosis invents the student.  
Diagnosis without strategy/planning is incomplete product behaviour — but this milestone correctly stops at diagnosis.

## Out of scope (MS002)

- Database models, schemas, or ORM entities
- Runtime A integration, feature flags, or services
- Recommendation logic, scheduling, or optimisation algorithms
- Application UI / intake collection UX
- Plan generation or rebalancing

## How to use this corpus

1. Read `STUDENT_EDUCATIONAL_PROFILE.md` first.
2. Treat dimensions as the complete educational lens for pre-plan diagnosis.
3. Map observations and declarations through `PROFILE_INPUTS.md` — never invent missing inputs.
4. Assign educational states from `PROFILE_STATES.md` by meaning, not by UI labels.
5. Expect profiles to evolve per `PROFILE_EVOLUTION.md`.
6. Require explainability contracts from `PROFILE_EXPLAINABILITY.md` before student-facing profile narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
