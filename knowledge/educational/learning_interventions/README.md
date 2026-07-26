# Learning Intervention Framework

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS003 — Learning Intervention Framework  
**Classification:** Educational reasoning specification — selection and explanation of educational responses after obstacle diagnosis  
**Status:** APPROVED — governing for Learning Coach intervention meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec selects and explains educational interventions after an explicit Learning Obstacle diagnosis**.

It answers *what educational response is most appropriate*, *which interventions an expert IFoA tutor may recommend*, *how selection is justified without numerical scoring*, *what the Learning Coach may and may not change*, and *how interventions are explained in supportive, evidence-based language*.

It does **not** implement Runtime A, scoring systems, analytics, databases, UI, services, or algorithms.

> **The Learning Intervention Framework answers:  
> “What is the most educationally appropriate response to this diagnosed obstacle?”  
> No intervention may exist without a diagnosed obstacle —  
> or an explicit evidence-gathering recommendation when diagnostic warrant is insufficient.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Learning Coach MS001)
8. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md) (Programme VI / Learning Coach MS002)
9. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)
10. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
11. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Daily Coach MS001)

Related (non-authoritative for educational meaning):

- [`../learning_coach/LEARNING_INTERVENTIONS.md`](../learning_coach/LEARNING_INTERVENTIONS.md) — MS001 seed catalogue; **superseded for governing meaning by this corpus** (retained as compatibility pointer)
- [`knowledge/architecture/INTERVENTION_MODEL.md`](../../architecture/INTERVENTION_MODEL.md) — architectural orchestration DTOs; educational claim law remains this Framework
- Educational Validation Framework EC-03 (Learning Coach) — quality release lens, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`LEARNING_INTERVENTION_FRAMEWORK.md`](LEARNING_INTERVENTION_FRAMEWORK.md) | Constitutional overview: what an intervention is, four-layer chain, tutor posture |
| [`INTERVENTION_CATALOGUE.md`](INTERVENTION_CATALOGUE.md) | Named educational interventions for IFoA preparation |
| [`INTERVENTION_SELECTION.md`](INTERVENTION_SELECTION.md) | How an expert tutor selects an intervention after diagnosis |
| [`INTERVENTION_BOUNDARIES.md`](INTERVENTION_BOUNDARIES.md) | What the Learning Coach may and may not change |
| [`INTERVENTION_EXPLAINABILITY.md`](INTERVENTION_EXPLAINABILITY.md) | How interventions are explained supportively to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Learning Coach MS001 — Learning Progression Model** | Decide *whether the student is genuinely learning over time* |
| **Learning Coach MS002 — Learning Obstacle Model** | Decide *why learning is not progressing as expected* |
| **Learning Coach MS003 — this corpus** | Decide *what educational response is warranted by that diagnosis* |

```
Accumulated Educational Evidence (EIP-002 / Learning Evidence Model)
     +  Progression judgement / posture (Learning Progression Model)
           →  Learning Obstacle Model (MS002)
                 →  Explicit educational diagnosis (obstacle + confidence posture)
                       →  Learning Intervention Framework (this milestone)
                             →  Named educational intervention + explainability
                                   →  Future evidence (does the response work?)
                       →  Informs Daily Coach emphasis / Profile re-consultation /
                          Master Planner escalation when envelopes break
                       (Runtime A / Twin writers / UI later — out of scope)
```

Progression asks: *Is learning progressing?*  
Diagnosis asks: *Why not — or why unevenly?*  
**Intervention asks: What should change educationally in response?**  
Future evidence asks: *Did that change improve the trail?*

## Architectural requirement

**Evidence, diagnosis, intervention, and future evidence are separate constitutional layers.**

```
Evidence
    ↓
Diagnosis
    ↓
Intervention
    ↓
Future evidence
```

| Layer | Question | Lawful product | Unlawful collapse |
|-------|----------|----------------|-------------------|
| **Evidence** | What was observed educationally? | Attributable observations and accumulation patterns | Renaming a recommendation as an observation |
| **Diagnosis** | What educational barrier best explains the trail? | Named obstacle (or explicit insufficient warrant) | Treating a tip as proof of a cause |
| **Intervention** | What educational response is warranted? | Tutor-style recommendation linked to a diagnosis | Generic advice without an explicit obstacle |
| **Future evidence** | Did the response improve learning? | New observations after the intervention | Declaring success because the tip was followed |

Hard rules:

1. **No intervention without explicit educational diagnosis** (or an explicit insufficient-warrant posture whose only lawful recommendation is further evidence gathering).
2. Intervention **responds** to diagnosis; it does not rewrite diagnosis by wishful coaching copy.
3. Intervention **must not** silently rewrite the Canonical Study Plan, override Daily Coach authority, redefine mastery, or change long-term educational strategy.
4. Long-term structural change **escalates** through existing planning / Daily Coach pathways.
5. Completion, understanding, retrieval, application, durable knowledge, and exam readiness remain distinct when judging whether an intervention succeeded.

## Out of scope (MS003)

- Runtime A integration, feature flags, or services
- Scoring systems, intervention “priority maths,” or numerical confidence scores
- Analytics pipelines, dashboards, or instrumentation
- Database models, schemas, or ORM entities
- UI components or intervention theatre widgets
- Algorithms, ML models, or software class designs
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Progression Model, or Obstacle Model meanings (consume them; do not redefine them)

## How to use this corpus

1. Read `LEARNING_INTERVENTION_FRAMEWORK.md` first.
2. Confirm an explicit obstacle diagnosis (or insufficient-warrant evidence-gathering posture) under [`../learning_obstacles/`](../learning_obstacles/).
3. Name candidate interventions only from `INTERVENTION_CATALOGUE.md`.
4. Select under `INTERVENTION_SELECTION.md` — required diagnosis, objective, expected improvement evidence, and non-use cases.
5. Respect authority limits in `INTERVENTION_BOUNDARIES.md`.
6. Require explainability contracts from `INTERVENTION_EXPLAINABILITY.md` before student-facing intervention narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
