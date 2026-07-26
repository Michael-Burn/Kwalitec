# Learning Session Model

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS002 — Learning Session Model  
**Classification:** Educational reasoning specification — anatomy of an individual study session under Daily Coach guidance  
**Status:** APPROVED — governing for Learning Session educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec structures an individual study session once the Daily Coach has selected today’s educational objective**.

It answers *how an expert IFoA tutor would run one coaching session on that objective*, *which educational aims a session may pursue*, *which phases belong in an effective session*, *when to move between phases*, *how to adapt locally without redefining the day*, and *how session structure is explained in plain educational language*.

It does **not** implement mission generation, timers, Runtime A, UI, or application code.

> **The Learning Session Model preserves the Daily Coach’s educational objective.  
> It may optimise *how* the student studies, but it must never redefine *what* the student is expected to accomplish that day.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-002, EL-003, EL-008, EL-009, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Daily Coach MS001)
8. [`../daily_coach/DAILY_COACH_OUTPUTS.md`](../daily_coach/DAILY_COACH_OUTPUTS.md) — especially DCO-01 (today’s primary objective)
9. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)

Related (non-authoritative for educational meaning):

- [`knowledge/version2/LEARNING_SESSION_EXPERIENCE.md`](../../version2/LEARNING_SESSION_EXPERIENCE.md) — product experience design (consumes, does not redefine, this educational law)
- [`knowledge/version2/LEARNING_ACTIVITY_ENGINE.md`](../../version2/LEARNING_ACTIVITY_ENGINE.md) — activity execution structure (implementation consumer)
- Educational Validation Framework EC-02 (Daily Coach) — quality release lens, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`LEARNING_SESSION_MODEL.md`](LEARNING_SESSION_MODEL.md) | Constitutional overview: what a Learning Session is, responsibilities, integrity, stack position |
| [`SESSION_OBJECTIVES.md`](SESSION_OBJECTIVES.md) | Educational aims a session may pursue under today’s Daily Coach objective |
| [`SESSION_STRUCTURE.md`](SESSION_STRUCTURE.md) | Educational phases of an effective study session |
| [`SESSION_TRANSITIONS.md`](SESSION_TRANSITIONS.md) | When and why the student should move between phases |
| [`SESSION_ADAPTATION.md`](SESSION_ADAPTATION.md) | Local session adjustment vs escalation back to the Daily Coach |
| [`SESSION_EXPLAINABILITY.md`](SESSION_EXPLAINABILITY.md) | How session structure, order, and learning contribution are explained |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract |
| **Daily Coach MS001 — Daily Coaching Model** | Decide *what is most educationally valuable to do today* |
| **Daily Coach MS002 — this corpus** | Decide *how the student should study that objective in one session* |
| **Daily Coach MS003 — Educational Reflection Model** | Decide *what the completed session taught us educationally* ([`../reflection/`](../reflection/)) |

```
Daily Coach primary objective (DCO-01)
     +  Authorised work type / practice focus / capacity envelopes
     +  Topic / syllabus warrant from plan + mode authority
     +  Session-local evidence emerging during study
           →  Learning Session Model (this milestone)
                 →  Session aims, phase structure, transitions,
                    local adaptation, session explainability
                       →  Educational Reflection Model (MS003)
                             →  Post-session interpretation for tomorrow’s coaching
                       (mission / Runtime A / UI later — out of scope)
```

Daily Coach settles *today’s educational priority*.  
Learning Session settles *the educational anatomy of studying that priority*.  
Educational Reflection settles *what that anatomy produced* after the sitting closes.

## Architectural requirement

The Learning Session Model must **preserve the Daily Coach’s educational objective**.

| Lawful | Unlawful |
|--------|----------|
| Choose phase emphasis, activity order, and depth that best serve today’s objective | Replace today’s objective with a different educational job |
| Adapt pace, scaffolding, and practice mix inside the session | Invent a new day’s priority, phase meaning, or sitting ambition |
| Shorten or reorder phases when educational progress warrants | Convert a revision / recovery day into undeclared first-pass theatre |
| Escalate when the session cannot honestly serve today’s objective | Silently redefine what the student was expected to accomplish today |
| Explain why this session is structured this way | Speak opaque optimiser scores or engineering jargon |

If serving today’s objective honestly requires changing the day’s educational job, the Learning Session **escalates to the Daily Coach** — it does not absorb Daily Coach authority.

## Out of scope (MS002)

- Mission generation algorithms or Today’s Mission selection code
- Runtime A integration, feature flags, or services
- Database models, schemas, or ORM entities
- Timers, clocks, or duration-as-law mechanisms
- UI components, notifications, or push scheduling
- Learning Activity Engine / Learning Session Runtime implementation
- Serialisation formats or API contracts
- Software class designs or service interfaces

## How to use this corpus

1. Read `LEARNING_SESSION_MODEL.md` first.
2. Treat aims in `SESSION_OBJECTIVES.md` as lawful session purposes under today’s Daily Coach objective.
3. Compose sessions from phases in `SESSION_STRUCTURE.md` — principles first, not fixed templates.
4. Move between phases using `SESSION_TRANSITIONS.md` (progress-led, not clock-led alone).
5. Keep adaptations local per `SESSION_ADAPTATION.md`; escalate when the day’s objective must change.
6. Require explainability contracts from `SESSION_EXPLAINABILITY.md` before student-facing session narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
