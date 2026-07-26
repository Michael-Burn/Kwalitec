# Learning Obstacle Model

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS002 — Learning Obstacle Model  
**Classification:** Educational reasoning specification — diagnosis of barriers to genuine learning progression  
**Status:** APPROVED — governing for Learning Coach obstacle meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec identifies obstacles that prevent genuine learning progression**.

It answers *why learning is not progressing as expected*, *which educational barriers an expert tutor distinguishes*, *how symptoms differ from underlying causes*, *how accumulated evidence supports or weakens a diagnosis*, and *how obstacles are explained in constructive educational language*.

It does **not** implement Runtime A, scoring systems, analytics, databases, UI, services, or algorithms.

> **The Learning Obstacle Model diagnoses educational barriers before recommending interventions.  
> Evidence, diagnosis, and intervention remain separate constitutional layers.  
> No intervention may be recommended without an explicit educational diagnosis.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Learning Coach MS001)
8. [`../learning_coach/LEARNING_EVIDENCE_MODEL.md`](../learning_coach/LEARNING_EVIDENCE_MODEL.md) (Programme VI / Learning Coach MS001)
9. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)
10. [`../reflection/EDUCATIONAL_REFLECTION_MODEL.md`](../reflection/EDUCATIONAL_REFLECTION_MODEL.md) (Programme VI / Daily Coach MS003)

Related (non-authoritative for educational meaning):

- [`knowledge/architecture/EVIDENCE_MODEL.md`](../../architecture/EVIDENCE_MODEL.md) — architectural Evidence Model; educational claim law remains EIP-002
- [`../learning_interventions/`](../learning_interventions/) — Learning Intervention Framework (MS003; governing downstream response vocabulary)

## Contents

| Document | Role |
|---|---|
| [`LEARNING_OBSTACLE_MODEL.md`](LEARNING_OBSTACLE_MODEL.md) | Constitutional overview: what a learning obstacle is, three-layer separation, tutor posture |
| [`OBSTACLE_CATALOGUE.md`](OBSTACLE_CATALOGUE.md) | Named categories of educational obstacles for IFoA preparation |
| [`OBSTACLE_DIAGNOSIS.md`](OBSTACLE_DIAGNOSIS.md) | How an expert tutor differentiates causes from symptoms |
| [`OBSTACLE_EVIDENCE.md`](OBSTACLE_EVIDENCE.md) | How accumulated evidence supports or weakens a diagnosis |
| [`OBSTACLE_EXPLAINABILITY.md`](OBSTACLE_EXPLAINABILITY.md) | How obstacles are explained constructively to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Learning Coach MS001 — Learning Progression Model** | Decide *whether the student is genuinely learning over time* |
| **Learning Coach MS002 — this corpus** | Decide *why learning is not progressing as expected* (educational diagnosis) |
| **Learning Coach MS001 — Learning Interventions** | Seed response vocabulary — **superseded for governing meaning by MS003** |
| **Learning Coach MS003 — Learning Intervention Framework** | Recommend *what educational response to take* — only after diagnosis — see [`../learning_interventions/`](../learning_interventions/) |

```
Accumulated Educational Evidence (EIP-002 / Learning Evidence Model)
     +  Progression judgement / posture (Learning Progression Model)
     +  Student Educational Profile
     +  Session history & Educational Reflection outputs
           →  Learning Obstacle Model (this milestone)
                 →  Explicit educational diagnosis (obstacle + confidence posture)
                       →  Learning Intervention Framework (MS003)
                       →  Informs Daily Coach emphasis / Profile re-consultation
                       (Runtime A / Twin writers / UI later — out of scope)
```

Progression judgement answers: *Is learning progressing?*  
**Obstacle diagnosis answers: Why not — or why unevenly — when growth is stalled, inconsistent, or thin?**  
Intervention answers: *What should change educationally?* — and may fire only after diagnosis (MS003).

## Architectural requirement

**Evidence, diagnosis, intervention, and future evidence are separate constitutional layers.**

| Layer | Question | Lawful product | Unlawful collapse |
|-------|----------|----------------|-------------------|
| **Evidence** | What was observed educationally? | Attributable observations and accumulation patterns | Renaming a recommendation as an observation |
| **Diagnosis** | What educational barrier best explains the trail? | Named obstacle (or explicit insufficient warrant) | Treating a symptom label as a cause without differentiation |
| **Intervention** | What educational response is warranted? | Tutor-style recommendation linked to a diagnosis | Generic advice without an explicit obstacle |
| **Future evidence** | Did the response improve learning? | New observations after the intervention | Declaring success because the tip was followed |

Hard rules:

1. **No intervention without explicit educational diagnosis** (or an explicit statement that warrant is insufficient to diagnose — in which case the lawful “intervention” is further evidence gathering, not a pretended cure).
2. Diagnosis **interprets** evidence; it does not mint evidence.
3. Intervention **responds** to diagnosis; it does not rewrite diagnosis by wishful coaching copy.
4. Completion, understanding, retrieval, application, durable knowledge, and exam readiness remain distinct when reading evidence for diagnosis.
5. Long-term plan / Daily Coach / mastery / strategy changes escalate — they are not silent Learning Coach mutations (see MS003 Boundaries).

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Scoring systems, obstacle “severity” maths, or numerical confidence scores
- Analytics pipelines, dashboards, or instrumentation
- Database models, schemas, or ORM entities
- UI components or diagnosis theatre widgets
- Algorithms, ML models, or software class designs
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Progression Model meanings, or Intervention catalogue meanings (consume them; do not redefine them)

## How to use this corpus

1. Read `LEARNING_OBSTACLE_MODEL.md` first.
2. Name candidate obstacles only from `OBSTACLE_CATALOGUE.md`.
3. Differentiate causes under `OBSTACLE_DIAGNOSIS.md` — symptoms are not diagnoses.
4. Support or weaken diagnoses only under `OBSTACLE_EVIDENCE.md`, respecting EIP-002 and the Learning Evidence Model.
5. Require explainability contracts from `OBSTACLE_EXPLAINABILITY.md` before student-facing obstacle narration.
6. Recommend interventions only after an explicit diagnosis, using the [`../learning_interventions/`](../learning_interventions/) catalogue as the downstream response vocabulary.
7. Do not implement algorithms that contradict this corpus without amending it first.
