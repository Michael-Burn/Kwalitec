# Educational Recovery Model

**Programme:** VI — Workstream 4 — Recovery Coach  
**Milestone:** MS001 — Educational Recovery Model  
**Classification:** Educational reasoning specification — restorative coaching after meaningful disruption  
**Status:** APPROVED — governing for Recovery Coach educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec restores educational progress after disruption while preserving the integrity of the long-term educational plan**.

It answers *when recovery is warranted*, *what educational goals recovery pursues*, *which restorative strategies an expert IFoA tutor may recommend*, *what the Recovery Coach may and may not change*, and *how recovery is explained in plain educational language*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Recovery Coach answers:  
> “How should this student recover educationally after meaningful disruption?”  
> Recovery restores progress; it does not replace planning.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-008, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
8. [`../study_plan/STUDY_PLAN_LIFECYCLE.md`](../study_plan/STUDY_PLAN_LIFECYCLE.md) (Programme VI / Master Planner MS007 — especially Recovered)
9. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
10. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
11. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
12. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md) (Programme VI / Workstream 3 / MS002)
13. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md) (Programme VI / Workstream 3 / MS003)
14. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)

Related (non-authoritative for educational meaning):

- [`knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md`](../../product/LEARNING_EXPERIENCE_PROGRAMME.md) — product daily-loop design (consumes, does not redefine, this educational law)
- Educational Validation Framework EC-04 (Recovery Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_RECOVERY_MODEL.md`](EDUCATIONAL_RECOVERY_MODEL.md) | Constitutional overview: what the Recovery Coach is, responsibilities, integrity, stack position |
| [`RECOVERY_OBJECTIVES.md`](RECOVERY_OBJECTIVES.md) | Educational goals recovery must optimise |
| [`RECOVERY_TRIGGERS.md`](RECOVERY_TRIGGERS.md) | Situations that warrant recovery vs temporary fluctuation |
| [`RECOVERY_STRATEGIES.md`](RECOVERY_STRATEGIES.md) | Educational recovery approaches that preserve long-term intent |
| [`RECOVERY_BOUNDARIES.md`](RECOVERY_BOUNDARIES.md) | What the Recovery Coach may and may not change |
| [`RECOVERY_EXPLAINABILITY.md`](RECOVERY_EXPLAINABILITY.md) | How recovery decisions are explained to students |

Downstream (consumes this corpus; does not redefine it):

| Document | Role |
|---|---|
| [`../recovery_pathways/`](../recovery_pathways/) | MS002 — Recovery Pathway Framework — named restorative journey types (RP-XX) selected after a lawful warrant |
| [`../recovery_completion/`](../recovery_completion/) | MS003 — Recovery Completion Model — whether recovery has been achieved and what educational transition follows |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what educational response is warranted* |
| **Recovery Coach MS001 — this corpus** | Decide *how the student should recover educationally after meaningful disruption* |
| **Recovery Coach MS002 — Recovery Pathway Framework** | Decide *what type of recovery journey is educationally appropriate for this disruption* ([`../recovery_pathways/`](../recovery_pathways/)) |
| **Recovery Coach MS003 — Recovery Completion Model** | Decide *whether recovery has been achieved* and *what educational transition follows* ([`../recovery_completion/`](../recovery_completion/)) |

```
Observed educational disruption
     +  Accumulated Educational Evidence
     +  Canonical Study Plan posture (Active / Adapted / Recovered)
     +  Student Educational Profile (capacity, reliability, recovery posture)
     +  Daily Coach day authority (consumed, not bypassed)
     +  Learning Coach evidence / obstacle / intervention meaning (consumed, not bypassed)
           →  Recovery Coach / Educational Recovery Model (this milestone)
                 →  Recovery warrant, objectives, restorative strategies,
                    boundary posture, recovery explainability
                       →  Informs Daily Coach emphasis within envelopes
                       →  Escalates to Rescheduling / Master Planner when
                          structural change is required
                       (Runtime A / Twin writers / UI later — out of scope)
```

Daily Coach settles *today’s educational priority*.  
Learning Coach settles *whether sittings constitute genuine growth* and *what learning response is warranted*.  
**Recovery Coach settles how educational progress is restored after meaningful disruption — without replacing planning.**

## Architectural requirement

Recovery recommendations must be **traceable to observed educational disruption and accumulated evidence**.

**Recovery is restorative, not corrective planning.**

| Lawful | Unlawful |
|--------|----------|
| Recommend restorative adaptations that restore momentum, consistency, and confidence | Rewrite the Canonical Study Plan independently |
| Distinguish temporary fluctuation from meaningful disruption | Treat every missed evening as a recovery episode |
| Preserve educational intent while adjusting near-term emphasis | Redefine educational strategy by Recovery Coach fiat |
| Consume Learning Coach evidence honestly | Infer mastery from rest, catch-up volume, or resumed ticks |
| Inform Daily Coach emphasis within plan envelopes | Bypass Daily Coach day-priority authority |
| Escalate structural change through Master Planner / rescheduling | Absorb long-term planning authority “to get the student back on track” |
| Explain why recovery is needed and when normal progression should resume | Shame language, punishment catch-up, or opaque optimiser speech |

Any permanent alteration to long-term educational intent must escalate through the **Master Planner** and established replanning pathways.

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or recovery theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “recovery scores”
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, or Learning Coach meanings (consume them; do not redefine them)

## How to use this corpus

1. Read `EDUCATIONAL_RECOVERY_MODEL.md` first.
2. Treat objectives in `RECOVERY_OBJECTIVES.md` as binding educational goals for recovery.
3. Classify disruption under `RECOVERY_TRIGGERS.md` — refuse recovery theatre for temporary fluctuation.
4. Select restorative approaches only under `RECOVERY_STRATEGIES.md`.
5. Respect authority limits in `RECOVERY_BOUNDARIES.md`.
6. Require explainability contracts from `RECOVERY_EXPLAINABILITY.md` before student-facing recovery narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
