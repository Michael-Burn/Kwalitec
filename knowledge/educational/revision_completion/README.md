# Revision Completion Model

**Programme:** VI — Workstream 5 — Revision Coach  
**Milestone:** MS003 — Revision Completion Model  
**Classification:** Educational reasoning specification — when revision has achieved its consolidating purpose and what follows  
**Status:** APPROVED — governing for Revision Coach completion meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec determines whether a revision objective has been achieved** and **what educational transitions follow that judgement**.

It answers *whether revision has successfully strengthened the learner’s existing knowledge*, *what educational conditions and evidence justify that conclusion*, *what may follow completion (or non-completion)*, and *how completion is explained without inventing first learning or mastery*.

It does **not** implement Runtime A, algorithms, databases, UI, services, analytics, or scoring systems.

> **The Revision Completion Model answers:  
> “Has this revision successfully strengthened the learner’s existing knowledge?”  
> Revision completion is an educational judgement based on accumulated evidence, not elapsed time or session count.  
> Completion strengthens confidence in existing learning; it does not imply first learning or mastery.**

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
12. [`../revision/REVISION_EXPLAINABILITY.md`](../revision/REVISION_EXPLAINABILITY.md)
13. [`../revision_strategies/REVISION_STRATEGY_FRAMEWORK.md`](../revision_strategies/REVISION_STRATEGY_FRAMEWORK.md) (Programme VI / Revision Coach MS002)
14. [`../revision_strategies/STRATEGY_TRANSITIONS.md`](../revision_strategies/STRATEGY_TRANSITIONS.md)
15. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
16. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006)
17. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
18. [`../learning_coach/LEARNING_PROGRESSION_MODEL.md`](../learning_coach/LEARNING_PROGRESSION_MODEL.md) (Programme VI / Workstream 3 / MS001)
19. [`../learning_coach/LEARNING_EVIDENCE_MODEL.md`](../learning_coach/LEARNING_EVIDENCE_MODEL.md)
20. [`../learning_obstacles/LEARNING_OBSTACLE_MODEL.md`](../learning_obstacles/LEARNING_OBSTACLE_MODEL.md)
21. [`../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md`](../learning_interventions/LEARNING_INTERVENTION_FRAMEWORK.md)
22. [`../recovery/EDUCATIONAL_RECOVERY_MODEL.md`](../recovery/EDUCATIONAL_RECOVERY_MODEL.md) (Programme VI / Workstream 4 / MS001)
23. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md)

Related (non-authoritative for educational meaning):

- Educational Validation Framework EC-05 (Revision Coach) — quality release lens when activated, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`REVISION_COMPLETION_MODEL.md`](REVISION_COMPLETION_MODEL.md) | Constitutional overview: what completion is, stack position, integrity rules |
| [`COMPLETION_CRITERIA.md`](COMPLETION_CRITERIA.md) | Educational conditions that indicate revision has fulfilled its purpose |
| [`COMPLETION_EVIDENCE.md`](COMPLETION_EVIDENCE.md) | Educational evidence that may support completion judgements |
| [`COMPLETION_TRANSITIONS.md`](COMPLETION_TRANSITIONS.md) | Educational transitions following completion or non-completion |
| [`COMPLETION_EXPLAINABILITY.md`](COMPLETION_EXPLAINABILITY.md) | How revision completion is explained to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract, including protected revision windows |
| **Daily Coach (WS2)** | Decide *what is most educationally valuable to do today* under that contract |
| **Learning Coach (WS3)** | Decide *whether the student is genuinely learning*, *why not*, and *what learning response is warranted* |
| **Recovery Coach (WS4)** | Decide *how the student should recover educationally after meaningful disruption* |
| **Revision Coach MS001 — Educational Revision Model** | Decide *what previously learned material should be revised now, and why* |
| **Revision Coach MS002 — Revision Strategy Framework** | Decide *what kind of revision is educationally appropriate for this knowledge at this time* |
| **Revision Coach MS003 — this corpus** | Decide *whether revision has strengthened existing knowledge enough* and *what educational transition follows* |

```
Active revision warrant + strategy (MS001 / MS002)
     +  Accumulated Educational Evidence (EIP-002)
     +  Revision objectives in focus (RVO-XX)
     +  Canonical Study Plan posture (including protected revision)
     +  Student Educational Profile (strengths, decay risk, revision maturity)
     +  Learning Coach / Daily Coach / Recovery Coach meaning (consumed)
           →  Revision Completion Model (this milestone)
                 →  Completion judgement (achieved / not yet / incomplete destination)
                    + completion criteria & evidence trail
                    + completion transition (RvCT-XX)
                    + completion explainability
                       →  Maintenance revision (RVS-07) where warranted
                       →  Return authority to ordinary Daily Coach guidance
                       →  Alternative revision strategy when consolidating need evolves
                       →  Escalation to Learning Coach when revision has not resolved
                          the underlying educational issue
                       (Runtime A / Twin writers / UI later — out of scope)
```

MS001 settles *that revision is warranted*, *which material*, and *which consolidating goods*.  
MS002 settles *which consolidating approach fits*.  
**MS003 settles whether that consolidating job has strengthened existing knowledge enough to lighten, resume ordinary coaching, change strategy, or hand unresolved learning problems back to the Learning Coach — without claiming first learning or mastery.**

## Completion vs neighbours

| Concept | Owner | Question |
|---------|-------|----------|
| **Trigger (RVT-XX)** | MS001 | Is revision warranted? |
| **Objective (RVO-XX)** | MS001 | What consolidating goods must revision pursue? |
| **Priority (RVP)** | MS001 | What should be revised first among known material? |
| **Strategy (RVS-XX)** | MS002 | What *kind* of consolidating approach fits? |
| **Strategy transition (ST1–ST7)** | MS002 | How may strategies succeed, change, or escalate? |
| **Completion criteria (RvCC-XX)** | **This corpus** | What educational conditions count as revision achieved? |
| **Completion evidence (RvCE-XX)** | **This corpus** | What accumulated evidence may support that judgement? |
| **Completion transition (RvCT-XX)** | **This corpus** | What educational move follows the completion judgement? |

MS002 `STRATEGY_TRANSITIONS.md` ST1–ST7 remains the strategy-level transition vocabulary.  
This corpus **specialises educational completion judgement** — especially successful strengthening → maintenance / ordinary coaching, and honest Learning Coach escalation — with criteria, evidence law, and student-facing completion speech. It does not invent a rival transition authority.

## Architectural requirement

Revision completion must be **justified by accumulated educational evidence**.

| Lawful | Unlawful |
|--------|----------|
| Judge completion from strengthened retrieval, durability, integration, prerequisite stability, and exam-usable readiness of *already learned* material | Treat elapsed calendar days or session count as completion |
| Require evidence accumulation — not a single revision tick | Infer completion from attendance, repetition count, or session completion alone |
| Strengthen confidence in existing learning | Interpret completion as first learning or mastery |
| Return day-priority authority to ordinary Daily Coach when intensive revision has done enough | Keep intensive revision indefinitely “to be safe” |
| Move to maintenance revision when light keep-alive is the honest next posture | Narrate maintenance while acute fragility remains |
| Escalate to Learning Coach when consolidating approaches have not resolved the underlying educational issue | Extend revision loops to paper over Learning Coach problems |
| Preserve Canonical Study Plan and sibling coach authorities | Rewrite plan, strategy, or mastery by “completion” fiat |

**Revision completion strengthens confidence in existing learning.**  
**It must never be interpreted as evidence of first learning or mastery.**  
**Where revision evidence reveals unresolved learning obstacles, authority must transition back to the Learning Coach rather than extending revision indefinitely.**

## Out of scope (MS003)

- Runtime A integration, feature flags, or services
- Algorithms, ML models, or software class designs
- Database models, schemas, or ORM entities
- UI components, notifications, or completion theatre widgets
- Analytics pipelines, dashboards, or instrumentation
- Scoring systems or numerical “revision completion scores”
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, Daily Coach, Learning Coach, Recovery Coach, MS001, or MS002 meanings (consume them; do not redefine them)

## How to use this corpus

1. Confirm an active revision warrant and strategy under MS001 / MS002 — refuse completion theatre for consolidating episodes that never lawfully began, or for material without prior exposure.
2. Read `REVISION_COMPLETION_MODEL.md` for stack position and integrity rules.
3. Evaluate educational conditions under `COMPLETION_CRITERIA.md`.
4. Require supporting trail under `COMPLETION_EVIDENCE.md` — respect EIP-002; refuse attendance-only, repetition-count-only, or session-completion-only proofs.
5. Select the lawful post-judgement move under `COMPLETION_TRANSITIONS.md`.
6. Require explainability contracts from `COMPLETION_EXPLAINABILITY.md` before student-facing completion narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
