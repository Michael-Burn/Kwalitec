# Examination Strategy Framework

**Programme:** VI — Workstream 6 — Exam Coach  
**Milestone:** MS002 — Examination Strategy Framework  
**Classification:** Educational reasoning specification — kinds of assessment preparation approaches once examination preparation is warranted  
**Status:** APPROVED — governing for Exam Coach strategy meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec selects an appropriate examination preparation strategy** once the Exam Coach has determined that examination preparation is warranted.

It answers *what kind of examination preparation is educationally appropriate for this learner at this stage*, *how an expert IFoA tutor selects among strategies without numerical scoring*, *how examination strategies evolve*, *when authority must return to Learning, Recovery, or Revision Coaches*, and *how strategy choices are explained to students*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Examination Strategy Framework answers:  
> “What kind of examination preparation is educationally appropriate for this learner at this stage?”  
> Preparation strategies optimise examination readiness while remaining faithful to the Learning, Recovery and Revision Coaches.  
> They must never compensate for absent learning, override Revision Coach recommendations, redefine mastery, or modify the Canonical Study Plan.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../exam/EDUCATIONAL_EXAMINATION_MODEL.md`](../exam/EDUCATIONAL_EXAMINATION_MODEL.md) (Programme VI / Exam Coach MS001)
8. [`../exam/EXAM_OBJECTIVES.md`](../exam/EXAM_OBJECTIVES.md)
9. [`../exam/EXAM_PREPARATION_TRIGGERS.md`](../exam/EXAM_PREPARATION_TRIGGERS.md)
10. [`../exam/EXAM_PRIORITIES.md`](../exam/EXAM_PRIORITIES.md)
11. [`../exam/EXAM_BOUNDARIES.md`](../exam/EXAM_BOUNDARIES.md)
12. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
13. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
14. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
15. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
16. [`../learning_coach/LEARNING_EVIDENCE_MODEL.md`](../learning_coach/LEARNING_EVIDENCE_MODEL.md)
17. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md)
18. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md)
19. [`../recovery/EDUCATIONAL_RECOVERY_MODEL.md`](../recovery/EDUCATIONAL_RECOVERY_MODEL.md) (Programme VI / Workstream 4 / MS001)
20. [`../revision/EDUCATIONAL_REVISION_MODEL.md`](../revision/EDUCATIONAL_REVISION_MODEL.md) (Programme VI / Workstream 5 / MS001)
21. [`../revision_strategies/REVISION_STRATEGY_FRAMEWORK.md`](../revision_strategies/REVISION_STRATEGY_FRAMEWORK.md) (Programme VI / Workstream 5 / MS002)
22. [`../revision_completion/REVISION_COMPLETION_MODEL.md`](../revision_completion/REVISION_COMPLETION_MODEL.md) (Programme VI / Workstream 5 / MS003)
23. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md)

Related (non-authoritative for educational meaning):

- [`../exam/EXAM_EXPLAINABILITY.md`](../exam/EXAM_EXPLAINABILITY.md) — MS001 examination speech contract; this corpus specialises strategy-level explainability
- Educational Validation Framework EC-06 (Exam Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`EXAMINATION_STRATEGY_FRAMEWORK.md`](EXAMINATION_STRATEGY_FRAMEWORK.md) | Constitutional overview: what an examination strategy is, stack position, integrity rules |
| [`STRATEGY_CATALOGUE.md`](STRATEGY_CATALOGUE.md) | Named educational examination preparation strategies for IFoA assessment |
| [`STRATEGY_SELECTION.md`](STRATEGY_SELECTION.md) | How an expert tutor selects a strategy after an examination preparation warrant |
| [`STRATEGY_TRANSITIONS.md`](STRATEGY_TRANSITIONS.md) | How strategies evolve, succeed, change, or hand off to upstream coaches |
| [`STRATEGY_EXPLAINABILITY.md`](STRATEGY_EXPLAINABILITY.md) | How strategy decisions are explained to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract, including examination-facing windows |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach (WS4)** | Decide *how the student should recover educationally after meaningful disruption* |
| **Revision Coach (WS5)** | Decide *what previously learned material should be revised*, *what kind of revision fits*, and *whether consolidation has strengthened knowledge enough* |
| **Exam Coach MS001 — Educational Examination Model** | Decide *whether examination preparation is warranted*, *which assessment-facing goods*, and *qualitative priority emphasis* |
| **Exam Coach MS002 — this corpus** | Decide *what kind of examination preparation is educationally appropriate for this learner at this stage* |
| **Exam Coach MS003 — Examination Preparation Completion Model** | Decide *whether examination preparation has fulfilled its educational purpose* and *what educational transition follows* ([`../exam_completion/`](../exam_completion/)) |

```
Examination preparation warrant + priority emphasis (MS001)
     +  Examination objectives in focus (EXO-XX)
     +  Qualitative priority factors (EXP)
     +  Accumulated Educational Evidence
     +  Canonical Study Plan posture (including exam-facing windows)
     +  Student Educational Profile
     +  Learning Coach progression / evidence meaning (consumed, not overridden)
     +  Recovery Coach posture (respected — never replaced)
     +  Revision Coach warrant / strategy / completion meaning (consumed, not redefined)
     +  Daily Coach day authority (coordinated, not bypassed)
           →  Examination Strategy Framework (this milestone)
                 →  Named strategy (EXS-XX) + selection rationale
                    + transition posture + strategy explainability
                       →  Informs how assessment-facing emphasis is shaped
                       →  Informs Daily Coach / session design within envelopes
                       →  Examination Preparation Completion Model (MS003)
                             →  Completion judgement + ExCT transition
                       →  Escalates to Learning / Recovery / Revision Coaches
                          when unresolved educational weaknesses appear
                       (Runtime A / Twin writers / UI later — out of scope)
```

MS001 settles *that examination preparation is warranted*, *which assessment-facing goods*, and *qualitative priority*.  
**MS002 settles which examination preparation approach best fits this learner at this stage — without replacing learning, revision, recovery, or planning.**  
**MS003 ([`../exam_completion/`](../exam_completion/)) settles whether that assessment-facing job has fulfilled Exam Coach educational responsibilities and what transition follows.**

## Strategy vs objective vs trigger vs priority

| Concept | Owner | Question |
|---------|-------|----------|
| **Trigger (EPT-XX)** | MS001 | Is assessment-facing preparation warranted — and of what kind? |
| **Objective (EXO-XX)** | MS001 | What examination educational goods must preparation advance? |
| **Priority (EXP-XX)** | MS001 | Among lawful emphases, what should lead? |
| **Strategy (EXS-XX)** | **This corpus** | What *kind* of examination preparation is educationally appropriate now? |

A strategy is a **named assessment-preparation approach archetype**.  
Objectives are the **goods** the approach pursues.  
Triggers **warrant** examination preparation; they do not automatically select a strategy by label matching alone.  
Priorities order **which emphasis**; strategies shape **how** that preparation is approached.

Identifier note: Examination Strategies use **EXS-XX** so they never collide with Revision Strategies (**RVS-XX**), Recovery Strategies (**RS-XX**), Recovery Pathways (**RP-XX**), or Master Planner educational strategy meanings.

## Architectural requirement

Examination strategies may **optimise assessment preparation**.

They must **not**:

- compensate for absent learning,
- override Revision Coach recommendations,
- redefine mastery,
- modify the Canonical Study Plan,
- replace Recovery Coach restorative ownership,
- invent readiness or pass certainty from mocks, volume, or phase labels.

Where examination preparation reveals **unresolved educational weaknesses**, authority must transition back to the **appropriate upstream coach** (Learning, Recovery, or Revision) rather than attempting to solve the problem within the Exam Coach.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or readiness / strategy theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “strategy fitness” / readiness metrics
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, or MS001 examination meanings (consume them; do not redefine them)

## How to use this corpus

1. Confirm a lawful examination preparation warrant under [`../exam/EXAM_PREPARATION_TRIGGERS.md`](../exam/EXAM_PREPARATION_TRIGGERS.md) — refuse strategy theatre for unlearned material, unfinished revision as primary job, or recovery-owned disruption.
2. Read `EXAMINATION_STRATEGY_FRAMEWORK.md` for stack position and integrity rules.
3. Select a named strategy only from `STRATEGY_CATALOGUE.md`.
4. Justify selection under `STRATEGY_SELECTION.md` — no numerical scoring.
5. Govern strategy change, success, or upstream-coach handoff under `STRATEGY_TRANSITIONS.md`.
6. Require explainability contracts from `STRATEGY_EXPLAINABILITY.md` before student-facing strategy narration.
7. Consume MS001 objectives / priorities / boundaries; do not invent a rival examination law.
8. After a lawful strategy emphasis, judge completion under [`../exam_completion/`](../exam_completion/) (MS003) — EST1–EST8 remain strategy-level vocabulary; ExCT-XX specialise completion judgement.
9. Do not implement algorithms that contradict this corpus without amending it first.
