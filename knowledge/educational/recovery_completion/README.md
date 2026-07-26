# Recovery Completion Model

**Programme:** VI — Workstream 4 — Recovery Coach  
**Milestone:** MS003 — Recovery Completion Model  
**Classification:** Educational reasoning specification — when educational recovery has been achieved and what follows  
**Status:** APPROVED — governing for Recovery Coach completion meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec determines whether educational recovery has been achieved** and **what educational transitions follow that judgement**.

It answers *whether the learner has recovered sufficiently to resume normal educational progression*, *what educational conditions and evidence justify that conclusion*, *what may follow completion (or non-completion)*, and *how completion is explained without inventing mastery*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Recovery Completion Model answers:  
> “Has this learner recovered sufficiently to resume normal educational progression?”  
> Recovery completion is an educational judgement, not a time-based milestone.  
> Completion restores educational continuity; it does not imply mastery.**

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
12. [`../recovery/RECOVERY_EXPLAINABILITY.md`](../recovery/RECOVERY_EXPLAINABILITY.md)
13. [`../recovery_pathways/RECOVERY_PATHWAY_FRAMEWORK.md`](../recovery_pathways/RECOVERY_PATHWAY_FRAMEWORK.md) (Programme VI / Recovery Coach MS002)
14. [`../recovery_pathways/PATHWAY_TRANSITIONS.md`](../recovery_pathways/PATHWAY_TRANSITIONS.md)
15. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
16. [`../study_plan/STUDY_PLAN_LIFECYCLE.md`](../study_plan/STUDY_PLAN_LIFECYCLE.md)
17. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
18. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
19. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
20. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md)
21. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md)
22. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md)

Related (non-authoritative for educational meaning):

- Educational Validation Framework EC-04 (Recovery Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`RECOVERY_COMPLETION_MODEL.md`](RECOVERY_COMPLETION_MODEL.md) | Constitutional overview: what completion is, stack position, integrity rules |
| [`COMPLETION_CRITERIA.md`](COMPLETION_CRITERIA.md) | Educational conditions that indicate recovery has been successful |
| [`COMPLETION_EVIDENCE.md`](COMPLETION_EVIDENCE.md) | Educational evidence that may support completion judgements |
| [`COMPLETION_TRANSITIONS.md`](COMPLETION_TRANSITIONS.md) | Educational transitions following completion or non-completion |
| [`COMPLETION_EXPLAINABILITY.md`](COMPLETION_EXPLAINABILITY.md) | How recovery completion is explained to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach MS001 — Educational Recovery Model** | Decide *whether recovery is warranted* and *which restorative objectives / strategies apply* |
| **Recovery Coach MS002 — Recovery Pathway Framework** | Decide *what type of recovery journey is educationally appropriate* |
| **Recovery Coach MS003 — this corpus** | Decide *whether recovery has been achieved* and *what educational transition follows* |

```
Active recovery warrant + pathway (MS001 / MS002)
     +  Accumulated Educational Evidence (EIP-002)
     +  Recovery objectives in focus (RO-XX)
     +  Canonical Study Plan posture & envelopes
     +  Student Educational Profile (capacity, reliability, recovery posture)
     +  Daily Coach / Learning Coach meaning (consumed)
           →  Recovery Completion Model (this milestone)
                 →  Completion judgement (achieved / not yet / incomplete destination)
                    + completion criteria & evidence trail
                    + completion transition (CT-XX)
                    + completion explainability
                       →  Return authority to normal Daily Coach pipeline
                       →  Continued monitoring where warranted
                       →  Alternative pathway or escalation when recovery is insufficient
                       (Runtime A / Twin writers / UI later — out of scope)
```

MS001 settles *that recovery is needed* and *which restorative goods and tactics are lawful*.  
MS002 settles *which recovery journey type fits*.  
**MS003 settles whether the restorative journey has restored continuity enough to return authority to normal coaching — without claiming mastery or rewriting long-term intent.**

## Completion vs neighbours

| Concept | Owner | Question |
|---------|-------|----------|
| **Trigger (RT-XX)** | MS001 | Is recovery warranted? |
| **Objective (RO-XX)** | MS001 | What educational goods must recovery restore? |
| **Strategy (RS-XX)** | MS001 | Which restorative tactics may be recommended? |
| **Pathway (RP-XX)** | MS002 | What *type* of recovery journey is appropriate? |
| **Pathway transition (T1–T5)** | MS002 | How may pathways change, resume, or escalate? |
| **Completion criteria (RCC-XX)** | **This corpus** | What educational conditions count as recovery achieved? |
| **Completion evidence (RCE-XX)** | **This corpus** | What accumulated evidence may support that judgement? |
| **Completion transition (CT-XX)** | **This corpus** | What educational move follows the completion judgement? |

MS002 `PATHWAY_TRANSITIONS.md` T1–T5 remains the pathway-level transition vocabulary.  
This corpus **specialises educational completion judgement** — especially successful resume — with criteria, evidence law, and student-facing completion speech. It does not invent a rival transition authority.

## Architectural requirement

Recovery completion must be **justified by accumulated educational evidence**.

| Lawful | Unlawful |
|--------|----------|
| Judge completion from restored continuity, consistency, confidence, and (where warranted) prerequisite safety | Treat elapsed calendar days as completion |
| Require evidence accumulation — not a single resumed tick | Infer completion from attendance or session completion alone |
| Return day-priority authority to ordinary Daily Coach under the authorised plan | Keep punishment catch-up after declaring completion |
| Preserve long-term educational intent unchanged by completion itself | Rewrite Canonical Study Plan, strategy, or mastery by “completion” fiat |
| State ongoing monitoring honestly when residual risk remains | Claim mastery, exam readiness, or wiped disruption history from completion |
| Escalate or change pathway when completion cannot be honestly affirmed | Fake local success to avoid Master Planner / Learning Coach handoff |

**Completion does not imply mastery.**  
**Successful recovery restores educational continuity and returns authority to the normal coaching pipeline without modifying long-term educational intent.**

## Out of scope (MS003)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or completion theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “recovery completion scores”
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, MS001, or MS002 meanings (consume them; do not redefine them)

## How to use this corpus

1. Confirm an active recovery warrant and pathway under MS001 / MS002 — refuse completion theatre for episodes that never lawfully began.
2. Read `RECOVERY_COMPLETION_MODEL.md` for stack position and integrity rules.
3. Evaluate educational conditions under `COMPLETION_CRITERIA.md`.
4. Require supporting trail under `COMPLETION_EVIDENCE.md` — respect EIP-002; refuse attendance-only or session-completion-only proofs.
5. Select the lawful post-judgement move under `COMPLETION_TRANSITIONS.md`.
6. Require explainability contracts from `COMPLETION_EXPLAINABILITY.md` before student-facing completion narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
