# Recovery Pathway Framework

**Programme:** VI — Workstream 4 — Recovery Coach  
**Milestone:** MS002 — Recovery Pathway Framework  
**Classification:** Educational reasoning specification — types of restorative journeys after meaningful disruption  
**Status:** APPROVED — governing for Recovery Coach pathway meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **which type of educational recovery is most appropriate after a meaningful disruption**.

It answers *what recovery pathway fits this disruption profile*, *how an expert IFoA tutor selects among pathways without numerical scoring*, *how recovery may progress between pathways*, *when normal coaching resumes*, *when escalation to Master Planner / Daily Coach pathways is required*, and *how pathway decisions are explained to students*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Recovery Pathway Framework answers:  
> “What type of recovery is most educationally appropriate for this disruption?”  
> Pathways adapt educational execution.  
> They do not independently rewrite long-term planning, strategy, or mastery.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-008, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../recovery/EDUCATIONAL_RECOVERY_MODEL.md`](../recovery/EDUCATIONAL_RECOVERY_MODEL.md) (Programme VI / Recovery Coach MS001)
8. [`../recovery/RECOVERY_OBJECTIVES.md`](../recovery/RECOVERY_OBJECTIVES.md)
9. [`../recovery/RECOVERY_TRIGGERS.md`](../recovery/RECOVERY_TRIGGERS.md)
10. [`../recovery/RECOVERY_STRATEGIES.md`](../recovery/RECOVERY_STRATEGIES.md)
11. [`../recovery/RECOVERY_BOUNDARIES.md`](../recovery/RECOVERY_BOUNDARIES.md)
12. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
13. [`../study_plan/STUDY_PLAN_LIFECYCLE.md`](../study_plan/STUDY_PLAN_LIFECYCLE.md)
14. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
15. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
16. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
17. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md)
18. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md)
19. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md)

Related (non-authoritative for educational meaning):

- [`../recovery/RECOVERY_EXPLAINABILITY.md`](../recovery/RECOVERY_EXPLAINABILITY.md) — MS001 recovery speech contract; this corpus specialises pathway-level explainability
- Educational Validation Framework EC-04 (Recovery Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`RECOVERY_PATHWAY_FRAMEWORK.md`](RECOVERY_PATHWAY_FRAMEWORK.md) | Constitutional overview: what a pathway is, stack position, integrity rules |
| [`PATHWAY_CATALOGUE.md`](PATHWAY_CATALOGUE.md) | Named educational recovery pathways for IFoA preparation |
| [`PATHWAY_SELECTION.md`](PATHWAY_SELECTION.md) | How an expert tutor selects a pathway after a recovery warrant |
| [`PATHWAY_TRANSITIONS.md`](PATHWAY_TRANSITIONS.md) | How recovery progresses between pathways, resumes normal coaching, or escalates |
| [`PATHWAY_EXPLAINABILITY.md`](PATHWAY_EXPLAINABILITY.md) | How pathway decisions are explained to students |

Downstream (consumes this corpus; does not redefine it):

| Document | Role |
|---|---|
| [`../recovery_completion/`](../recovery_completion/) | MS003 — Recovery Completion Model — whether recovery has been achieved and what educational transition follows |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach MS001 — Educational Recovery Model** | Decide *whether recovery is warranted* and *which restorative objectives / strategies apply* |
| **Recovery Coach MS002 — this corpus** | Decide *what type of recovery journey is educationally appropriate for this disruption* |
| **Recovery Coach MS003 — Recovery Completion Model** | Decide *whether recovery has been achieved* and *what educational transition follows* ([`../recovery_completion/`](../recovery_completion/)) |

```
Meaningful disruption + recovery warrant (MS001)
     +  Recovery objectives in focus (RO-XX)
     +  Accumulated Educational Evidence
     +  Canonical Study Plan posture & phase emphasis
     +  Student Educational Profile
     +  Daily Coach / Learning Coach meaning (consumed)
           →  Recovery Pathway Framework (this milestone)
                 →  Named pathway (RP-XX) + selection rationale
                    + transition posture + pathway explainability
                       →  Informs which MS001 strategies to emphasise
                       →  Informs Daily Coach emphasis within envelopes
                       →  Escalates to Rescheduling / Master Planner when
                          recovery alone is inadequate
                       (Runtime A / Twin writers / UI later — out of scope)
```

MS001 settles *that recovery is needed* and *which restorative goods and tactics are lawful*.  
**MS002 settles which recovery journey type best fits the disruption — without replacing planning.**

## Pathway vs strategy vs trigger

| Concept | Owner | Question |
|---------|-------|----------|
| **Trigger (RT-XX)** | MS001 | Is this meaningful disruption — and of what kind? |
| **Objective (RO-XX)** | MS001 | What educational goods must recovery restore? |
| **Strategy (RS-XX)** | MS001 | Which restorative tactics may be recommended? |
| **Pathway (RP-XX)** | **This corpus** | What *type* of recovery journey is educationally appropriate? |

A pathway is a **named restorative journey archetype**.  
Strategies are **tactics used inside** a pathway.  
Triggers **warrant** recovery; they do not automatically select a pathway by label matching alone.

## Architectural requirement

Recovery pathways may **adapt educational execution** (near-term emphasis, restorative framing, temporary load posture within envelopes) but must **not independently modify**:

- long-term planning / Canonical Study Plan envelopes,
- educational strategy,
- mastery judgements.

Where recovery is insufficient, escalation must follow the established **Master Planner** and **Daily Coach** pathways (including Rescheduling), consistent with `../recovery/RECOVERY_BOUNDARIES.md`.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or pathway theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “pathway fitness” metrics
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, or MS001 recovery meanings (consume them; do not redefine them)

## How to use this corpus

1. Confirm a lawful recovery warrant under `../recovery/RECOVERY_TRIGGERS.md` — refuse pathway theatre for temporary fluctuation.
2. Read `RECOVERY_PATHWAY_FRAMEWORK.md` for stack position and integrity rules.
3. Select a named pathway only from `PATHWAY_CATALOGUE.md`.
4. Justify selection under `PATHWAY_SELECTION.md` — no numerical scoring.
5. Govern change of pathway, resume, or escalation under `PATHWAY_TRANSITIONS.md`.
6. Require explainability contracts from `PATHWAY_EXPLAINABILITY.md` before student-facing pathway narration.
7. Consume MS001 strategies / boundaries; do not invent a rival recovery law.
8. Do not implement algorithms that contradict this corpus without amending it first.
