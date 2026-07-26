# Educational Examination Model

**Programme:** VI — Workstream 6 — Exam Coach  
**Milestone:** MS001 — Educational Examination Model  
**Classification:** Educational reasoning specification — preparing learners for professional assessment using accumulated educational evidence  
**Status:** APPROVED — governing for Exam Coach educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec prepares learners for professional examinations** using the educational understanding established by Learning Coach, Recovery Coach, Revision Coach, Daily Coach, and Master Planner authorities.

It answers *what educational goals examination preparation pursues*, *when examination preparation is warranted*, *how an expert tutor prioritises examination preparation emphasis*, *what the Exam Coach may and may not do*, and *how examination preparation recommendations are explained in plain educational language*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Exam Coach answers:  
> “How should this learner prepare for and approach the examination?”  
> The Exam Coach prepares learners for assessment.  
> It does not replace learning, revision, recovery, or planning.**

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
12. [`../recovery/EDUCATIONAL_RECOVERY_MODEL.md`](../recovery/EDUCATIONAL_RECOVERY_MODEL.md) (Programme VI / Workstream 4 / MS001)
13. [`../revision/EDUCATIONAL_REVISION_MODEL.md`](../revision/EDUCATIONAL_REVISION_MODEL.md) (Programme VI / Workstream 5 / MS001)
14. [`../revision_strategies/REVISION_STRATEGY_FRAMEWORK.md`](../revision_strategies/REVISION_STRATEGY_FRAMEWORK.md) (Programme VI / Workstream 5 / MS002)
15. [`../revision_completion/REVISION_COMPLETION_MODEL.md`](../revision_completion/REVISION_COMPLETION_MODEL.md) (Programme VI / Workstream 5 / MS003)
16. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)

Related (non-authoritative for educational meaning):

- [`knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md`](../../product/LEARNING_EXPERIENCE_PROGRAMME.md) — product daily-loop design (consumes, does not redefine, this educational law)
- Educational Validation Framework EC-06 (Exam Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_EXAMINATION_MODEL.md`](EDUCATIONAL_EXAMINATION_MODEL.md) | Constitutional overview: what the Exam Coach is, responsibilities, integrity, stack position |
| [`EXAM_OBJECTIVES.md`](EXAM_OBJECTIVES.md) | Educational goals examination preparation must optimise |
| [`EXAM_PREPARATION_TRIGGERS.md`](EXAM_PREPARATION_TRIGGERS.md) | Situations that activate Exam Coach vs learning, revision, or recovery |
| [`EXAM_PRIORITIES.md`](EXAM_PRIORITIES.md) | How an expert tutor prioritises examination preparation without numerical scoring |
| [`EXAM_BOUNDARIES.md`](EXAM_BOUNDARIES.md) | What the Exam Coach may and may not do |
| [`EXAM_EXPLAINABILITY.md`](EXAM_EXPLAINABILITY.md) | How examination preparation recommendations are explained to students |

Downstream (consumes this corpus; does not redefine it):

| Document | Role |
|---|---|
| [`../exam_strategies/`](../exam_strategies/) | MS002 — Examination Strategy Framework — what *kind* of examination preparation is educationally appropriate for this learner at this stage |
| [`../exam_completion/`](../exam_completion/) | MS003 — Examination Preparation Completion Model — whether examination preparation has fulfilled its educational purpose and what transition follows |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract, including examination-facing windows |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach (WS4)** | Decide *how the student should recover educationally after meaningful disruption* |
| **Revision Coach (WS5)** | Decide *what previously learned material should be revised*, *what kind of revision fits*, and *whether consolidation has strengthened knowledge enough* |
| **Exam Coach MS001 — this corpus** | Decide *whether examination preparation is warranted*, *which assessment-facing goods*, and *qualitative priority* |
| **Exam Coach MS002 — Examination Strategy Framework** | Decide *what kind of examination preparation is educationally appropriate for this learner at this stage* ([`../exam_strategies/`](../exam_strategies/)) |
| **Exam Coach MS003 — Examination Preparation Completion Model** | Decide *whether examination preparation has fulfilled its educational purpose* and *what educational transition follows* ([`../exam_completion/`](../exam_completion/)) |

```
Accumulated Educational Evidence
     +  Canonical Study Plan posture (including exam-facing windows)
     +  Student Educational Profile (readiness posture, capacity, exam context)
     +  Learning Coach progression / evidence meaning (consumed, not overridden)
     +  Recovery Coach posture (respected — never replaced)
     +  Revision Coach warrant / strategy / completion meaning (consumed, not redefined)
     +  Daily Coach day authority (coordinated, not bypassed)
           →  Exam Coach / Educational Examination Model (this milestone)
                 →  Examination preparation warrant, objectives, priority emphasis,
                    boundary posture, examination explainability
                       →  Examination Strategy Framework (MS002)
                             →  Named strategy (EXS-XX) after warrant
                       →  Examination Preparation Completion Model (MS003)
                             →  Completion judgement + ExCT transition
                       →  Informs Daily Coach emphasis within envelopes
                       →  Escalates when first learning, revision, recovery, or
                          structural planning is the true need
                       (Runtime A / Twin writers / UI later — out of scope)
```

Daily Coach settles *today’s educational priority*.  
Learning Coach settles *whether sittings constitute genuine growth*.  
Recovery Coach settles *how progress is restored after meaningful disruption*.  
Revision Coach settles *what previously learned material should be consolidated — and how / whether enough*.  
**Exam Coach MS001 settles whether examination preparation is warranted, which assessment-facing goods apply, and qualitative priority — without replacing learning, revision, recovery, or planning.**  
**Exam Coach MS002 settles what kind of examination preparation approach fits this learner at this stage.**  
**Exam Coach MS003 settles whether that assessment-facing job has fulfilled Exam Coach responsibilities enough to proceed, monitor, maintain, hand upstream, or reflect after the sitting — without claiming mastery or guaranteed examination performance.**

## Architectural requirement

The Exam Coach prepares learners for assessment using **accumulated educational evidence**.

It must **never** substitute for learning, revision, or recovery, and it must preserve all established Programme VI authority boundaries.

| Lawful | Unlawful |
|--------|----------|
| Recommend examination preparation posture and emphasis | Introduce first learning labelled as “exam prep” |
| Coordinate with Daily Coach within plan envelopes | Bypass Daily Coach day-priority authority |
| Reinforce examination strategy and approach | Replace Revision Coach consolidating responsibilities |
| Consume Learning Coach, Recovery Coach, and Revision Coach meaning honestly | Override Learning Coach evidence or redefine mastery |
| Respect Recovery Coach when disruption is the true problem | Replace Recovery Coach restorative responsibilities |
| Protect Canonical Study Plan exam-facing intent | Rewrite the Canonical Study Plan independently |
| Explain why preparation is changing, what evidence, what outcome | Opaque optimiser speech or numeric readiness theatre |

The Exam Coach should **consume** the outputs of the Learning Coach, Recovery Coach, and Revision Coach **without redefining their educational meaning**.

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or exam / readiness theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “readiness scores” / priority indices
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, Recovery Coach, or Revision Coach meanings (consume them; do not redefine them)

## How to use this corpus

1. Read `EDUCATIONAL_EXAMINATION_MODEL.md` first.
2. Treat objectives in `EXAM_OBJECTIVES.md` as binding educational goals for examination preparation.
3. Classify warrant under `EXAM_PREPARATION_TRIGGERS.md` — refuse exam theatre for unlearned material, unfinished revision meaning, or recovery-owned disruption.
4. Prioritise emphasis only under `EXAM_PRIORITIES.md` — qualitative tutor reasoning, never numeric scoring.
5. Respect authority limits in `EXAM_BOUNDARIES.md`.
6. Require explainability contracts from `EXAM_EXPLAINABILITY.md` before student-facing examination preparation narration.
7. After a lawful warrant, select examination preparation *approach* under [`../exam_strategies/`](../exam_strategies/) (MS002) — do not invent strategies without warrant.
8. Judge whether preparation has fulfilled Exam Coach purpose under [`../exam_completion/`](../exam_completion/) (MS003) — refuse time-only, checklist-only, or proximity-only completion.
9. Do not implement algorithms that contradict this corpus without amending it first.
