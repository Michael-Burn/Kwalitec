# Revision Strategy Framework

**Programme:** VI — Workstream 5 — Revision Coach  
**Milestone:** MS002 — Revision Strategy Framework  
**Classification:** Educational reasoning specification — kinds of consolidating approaches for previously learned material  
**Status:** APPROVED — governing for Revision Coach strategy meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec selects an appropriate revision strategy for previously learned material**.

It answers *what kind of revision is educationally appropriate for this knowledge at this time*, *how an expert IFoA tutor selects among strategies without numerical scoring*, *how revision strategies evolve*, *when escalation back to the Learning Coach is required*, and *how strategy choices are explained to students*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Revision Strategy Framework answers:  
> “What kind of revision is educationally appropriate for this knowledge at this time?”  
> Strategies optimise how previously learned knowledge is reinforced.  
> They do not introduce first learning, bypass Recovery Coach, redefine mastery, or modify long-term educational planning.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../revision/EDUCATIONAL_REVISION_MODEL.md`](../revision/EDUCATIONAL_REVISION_MODEL.md) (Programme VI / Revision Coach MS001)
8. [`../revision/REVISION_OBJECTIVES.md`](../revision/REVISION_OBJECTIVES.md)
9. [`../revision/REVISION_TRIGGERS.md`](../revision/REVISION_TRIGGERS.md)
10. [`../revision/REVISION_PRIORITIES.md`](../revision/REVISION_PRIORITIES.md)
11. [`../revision/REVISION_BOUNDARIES.md`](../revision/REVISION_BOUNDARIES.md)
12. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
13. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
14. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
15. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
16. [`../learning_coach/LEARNING_EVIDENCE_MODEL.md`](../learning_coach/LEARNING_EVIDENCE_MODEL.md)
17. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md)
18. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md)
19. [`../recovery/EDUCATIONAL_RECOVERY_MODEL.md`](../recovery/EDUCATIONAL_RECOVERY_MODEL.md) (Programme VI / Workstream 4 / MS001)
20. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md)

Related (non-authoritative for educational meaning):

- [`../revision/REVISION_EXPLAINABILITY.md`](../revision/REVISION_EXPLAINABILITY.md) — MS001 revision speech contract; this corpus specialises strategy-level explainability
- Educational Validation Framework EC-05 (Revision Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`REVISION_STRATEGY_FRAMEWORK.md`](REVISION_STRATEGY_FRAMEWORK.md) | Constitutional overview: what a revision strategy is, stack position, integrity rules |
| [`STRATEGY_CATALOGUE.md`](STRATEGY_CATALOGUE.md) | Named educational revision strategies for IFoA preparation |
| [`STRATEGY_SELECTION.md`](STRATEGY_SELECTION.md) | How an expert tutor selects a strategy after a revision warrant |
| [`STRATEGY_TRANSITIONS.md`](STRATEGY_TRANSITIONS.md) | How strategies evolve, succeed, change, or escalate to Learning Coach |
| [`STRATEGY_EXPLAINABILITY.md`](STRATEGY_EXPLAINABILITY.md) | How strategy decisions are explained to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract, including protected revision windows |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach (WS4)** | Decide *how the student should recover educationally after meaningful disruption* |
| **Revision Coach MS001 — Educational Revision Model** | Decide *what previously learned material should be revised now, and why* |
| **Revision Coach MS002 — this corpus** | Decide *what kind of revision is educationally appropriate for this knowledge at this time* |
| **Revision Coach MS003 — Revision Completion Model** | Decide *whether revision has strengthened existing knowledge enough* and *what educational transition follows* ([`../revision_completion/`](../revision_completion/)) |

```
Prior exposure + revision warrant (MS001)
     +  Revision objectives in focus (RVO-XX)
     +  Qualitative priority emphasis (RVP)
     +  Accumulated Educational Evidence
     +  Canonical Study Plan posture (including protected revision)
     +  Student Educational Profile
     +  Learning Coach progression / evidence meaning (consumed, not overridden)
     +  Daily Coach day authority (coordinated, not bypassed)
     +  Recovery Coach posture (respected — never replaced)
           →  Revision Strategy Framework (this milestone)
                 →  Named strategy (RVS-XX) + selection rationale
                    + transition posture + strategy explainability
                       →  Revision Completion Model (MS003)
                             →  Completion judgement when consolidating
                                purpose is evaluated
                       →  Informs how consolidating emphasis is shaped
                       →  Informs Daily Coach / session design within envelopes
                       →  Escalates to Learning Coach when revision evidence
                          shows a deeper learning problem
                       (Runtime A / Twin writers / UI later — out of scope)
```

MS001 settles *that revision is warranted*, *which material*, *which consolidating goods*, and *qualitative topic priority*.  
**MS002 settles which revision approach best fits this knowledge at this time — without replacing first learning, recovery, or planning.**  
**MS003 settles whether that consolidating job has strengthened existing knowledge enough — and what follows — without claiming first learning or mastery.**

Downstream (consumes this corpus; does not redefine it):

| Document | Role |
|---|---|
| [`../revision_completion/`](../revision_completion/) | MS003 — Revision Completion Model — specialises ST1–ST7 completion judgement with criteria, evidence law, and completion speech |

## Strategy vs objective vs trigger vs priority

| Concept | Owner | Question |
|---------|-------|----------|
| **Trigger (RVT-XX)** | MS001 | Is consolidating return warranted — and of what kind? |
| **Objective (RVO-XX)** | MS001 | What educational goods must revision advance? |
| **Priority (RVP-XX)** | MS001 | Among lawful candidates, what should be revised first? |
| **Strategy (RVS-XX)** | **This corpus** | What *kind* of revision approach is educationally appropriate now? |
| **Completion (RvCC / RvCE / RvCT)** | MS003 | Has consolidating revision strengthened existing knowledge enough — and what follows? |

A strategy is a **named consolidating approach archetype**.  
Objectives are the **goods** the approach pursues.  
Triggers **warrant** revision; they do not automatically select a strategy by label matching alone.  
Priorities order **which material**; strategies shape **how** that material is revised.

Identifier note: Revision Strategies use **RVS-XX** so they never collide with Recovery Strategies (**RS-XX**) or Master Planner educational strategy meanings.

## Architectural requirement

Revision strategies may **optimise how previously learned knowledge is reinforced**.

They must **not**:

- introduce first learning under a revision label,
- bypass Recovery Coach responsibilities,
- redefine mastery,
- modify long-term educational planning / Canonical Study Plan envelopes independently.

Where revision evidence indicates a **deeper learning problem**, authority must transition back to the **Learning Coach** rather than compensating through repeated revision.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or strategy theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “strategy fitness” metrics
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, Recovery Coach, or MS001 revision meanings (consume them; do not redefine them)

## How to use this corpus

1. Confirm a lawful revision warrant under [`../revision/REVISION_TRIGGERS.md`](../revision/REVISION_TRIGGERS.md) — refuse strategy theatre for unlearned material or recovery-owned disruption.
2. Read `REVISION_STRATEGY_FRAMEWORK.md` for stack position and integrity rules.
3. Select a named strategy only from `STRATEGY_CATALOGUE.md`.
4. Justify selection under `STRATEGY_SELECTION.md` — no numerical scoring.
5. Govern strategy change, success, or Learning Coach escalation under `STRATEGY_TRANSITIONS.md`.
6. Require explainability contracts from `STRATEGY_EXPLAINABILITY.md` before student-facing strategy narration.
7. Consume MS001 objectives / priorities / boundaries; do not invent a rival revision law.
8. Do not implement algorithms that contradict this corpus without amending it first.
