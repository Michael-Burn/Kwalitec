# Educational Revision Model

**Programme:** VI — Workstream 5 — Revision Coach  
**Milestone:** MS001 — Educational Revision Model  
**Classification:** Educational reasoning specification — consolidating previously learned knowledge for durable exam preparation  
**Status:** APPROVED — governing for Revision Coach educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec consolidates previously learned knowledge into durable, retrievable understanding** in preparation for professional examinations.

It answers *what educational goals revision pursues*, *when revision is warranted*, *how an expert tutor prioritises revision emphasis*, *what the Revision Coach may and may not do*, and *how revision recommendations are explained in plain educational language*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Revision Coach answers:  
> “What should this student revise now, and why?”  
> Revision strengthens existing learning. It does not replace first learning, recovery, or long-term planning.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
8. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
9. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
10. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
11. [`../learning_coach/LEARNING_EVIDENCE_MODEL.md`](../learning_coach/LEARNING_EVIDENCE_MODEL.md) (Programme VI / Workstream 3 / MS001)
12. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md) (Programme VI / Workstream 3 / MS002)
13. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md) (Programme VI / Workstream 3 / MS003)
14. [`../recovery/EDUCATIONAL_RECOVERY_MODEL.md`](../recovery/EDUCATIONAL_RECOVERY_MODEL.md) (Programme VI / Workstream 4 / MS001)
15. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)

Related (non-authoritative for educational meaning):

- [`knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md`](../../product/LEARNING_EXPERIENCE_PROGRAMME.md) — product daily-loop design (consumes, does not redefine, this educational law)
- Educational Validation Framework EC-05 (Revision Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_REVISION_MODEL.md`](EDUCATIONAL_REVISION_MODEL.md) | Constitutional overview: what the Revision Coach is, responsibilities, integrity, stack position |
| [`REVISION_OBJECTIVES.md`](REVISION_OBJECTIVES.md) | Educational goals revision must optimise |
| [`REVISION_TRIGGERS.md`](REVISION_TRIGGERS.md) | Situations that warrant revision vs first learning or recovery |
| [`REVISION_PRIORITIES.md`](REVISION_PRIORITIES.md) | How an expert tutor prioritises revision emphasis without numerical scoring |
| [`REVISION_BOUNDARIES.md`](REVISION_BOUNDARIES.md) | What the Revision Coach may and may not do |
| [`REVISION_EXPLAINABILITY.md`](REVISION_EXPLAINABILITY.md) | How revision recommendations are explained to students |

Downstream (consumes this corpus; does not redefine it):

| Document | Role |
|---|---|
| [`../revision_strategies/`](../revision_strategies/) | MS002 — Revision Strategy Framework — what *kind* of revision is educationally appropriate for this knowledge at this time |
| [`../revision_completion/`](../revision_completion/) | MS003 — Revision Completion Model — whether consolidating revision has strengthened existing knowledge enough, and what follows |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract, including protected revision windows |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach (WS4)** | Decide *how the student should recover educationally after meaningful disruption* |
| **Revision Coach MS001 — this corpus** | Decide *what previously learned material should be revised now, and why* |
| **Revision Coach MS002 — Revision Strategy Framework** | Decide *what kind of revision is educationally appropriate for this knowledge at this time* ([`../revision_strategies/`](../revision_strategies/)) |
| **Revision Coach MS003 — Revision Completion Model** | Decide *whether revision has strengthened existing knowledge enough* and *what educational transition follows* ([`../revision_completion/`](../revision_completion/)) |

```
Prior exposure / authorised revision windows
     +  Accumulated Educational Evidence
     +  Canonical Study Plan posture (including protected revision)
     +  Student Educational Profile (strengths, decay risk, revision maturity)
     +  Learning Coach progression / evidence meaning (consumed, not overridden)
     +  Daily Coach day authority (coordinated, not bypassed)
     +  Recovery Coach posture (respected — never replaced)
           →  Revision Coach / Educational Revision Model (this milestone)
                 →  Revision warrant, objectives, priority emphasis,
                    boundary posture, revision explainability
                       →  Revision Strategy Framework (MS002)
                             →  Named consolidating approach (RVS-XX)
                       →  Revision Completion Model (MS003)
                             →  Completion judgement, criteria, evidence,
                                transitions, completion explainability
                       →  Informs Daily Coach emphasis within envelopes
                       →  Escalates when first learning, recovery, or a
                          deeper Learning Coach problem is the true need
                       (Runtime A / Twin writers / UI later — out of scope)
```

Daily Coach settles *today’s educational priority*.  
Learning Coach settles *whether sittings constitute genuine growth*.  
Recovery Coach settles *how progress is restored after meaningful disruption*.  
**Revision Coach MS001 settles what previously learned material should be consolidated now — and why — without replacing first learning, recovery, or planning.**  
**Revision Coach MS002 settles what kind of consolidating approach fits that knowledge at this time.**  
**Revision Coach MS003 settles whether consolidating revision has strengthened existing knowledge enough — and what follows — without claiming first learning or mastery.**

## Architectural requirement

Revision recommendations must be **traceable to accumulated educational evidence** and remain consistent with the Learning Coach, Recovery Coach, and Canonical Study Plan.

**Revision strengthens existing learning.**

| Lawful | Unlawful |
|--------|----------|
| Recommend revision emphasis on previously learned material | Introduce new syllabus content labelled as “revision” |
| Strengthen retrieval, durability, understanding, and exam readiness | Compensate for absent first learning |
| Coordinate with Daily Coach within plan envelopes | Bypass Daily Coach day-priority authority |
| Consume Learning Coach evidence honestly | Override Learning Coach evidence or redefine mastery |
| Respect Recovery Coach when disruption is the true problem | Replace Recovery Coach restorative responsibilities |
| Protect Canonical Study Plan revision windows as educational intent | Rewrite the Canonical Study Plan independently |
| Explain why this topic, what evidence, what outcome | Opaque optimiser speech or numeric revision theatre |

Revision must **never** be used to compensate for absent first learning or to bypass Recovery Coach responsibilities.

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or revision theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “revision scores” / priority indices
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, or Recovery Coach meanings (consume them; do not redefine them)

## How to use this corpus

1. Read `EDUCATIONAL_REVISION_MODEL.md` first.
2. Treat objectives in `REVISION_OBJECTIVES.md` as binding educational goals for revision.
3. Classify warrant under `REVISION_TRIGGERS.md` — refuse revision theatre for unlearned material or recovery-owned disruption.
4. Prioritise emphasis only under `REVISION_PRIORITIES.md` — qualitative tutor reasoning, never numeric scoring.
5. Respect authority limits in `REVISION_BOUNDARIES.md`.
6. Require explainability contracts from `REVISION_EXPLAINABILITY.md` before student-facing revision narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
