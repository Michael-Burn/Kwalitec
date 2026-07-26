# Learning Progression Model

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS001 — Learning Progression Model  
**Classification:** Educational reasoning specification — long-term learning progression across study sessions  
**Status:** APPROVED — governing for Learning Coach educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec understands and supports learning progression over time**.

It answers *whether the student is genuinely learning*, *what successful learning means for IFoA preparation*, *how educational evidence accumulates across sessions*, *which progression postures an expert tutor recognises*, *how the tutor responds when progression stalls, accelerates, or becomes inconsistent*, and *how progression is explained in plain educational language*.

It does **not** implement Runtime A, scoring systems, analytics, databases, UI, services, or algorithms.

> **The Learning Coach interprets educational evidence across multiple study sessions.  
> It never confuses a single day’s completion with lasting educational growth.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)
8. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Workstream 2 / MS001)
9. [`../reflection/EDUCATIONAL_REFLECTION_MODEL.md`](../reflection/EDUCATIONAL_REFLECTION_MODEL.md) (Programme VI / Workstream 2 / MS003)

Related (non-authoritative for educational meaning):

- [`knowledge/architecture/EVIDENCE_MODEL.md`](../../architecture/EVIDENCE_MODEL.md) — architectural Evidence Model (MS-006); educational claim law remains EIP-002
- Educational Validation Framework EC-03 (Learning Coach) — quality release lens, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`LEARNING_PROGRESSION_MODEL.md`](LEARNING_PROGRESSION_MODEL.md) | Constitutional overview: what the Learning Coach is, responsibilities, integrity, stack position |
| [`LEARNING_OBJECTIVES.md`](LEARNING_OBJECTIVES.md) | What successful learning means for IFoA preparation |
| [`LEARNING_EVIDENCE_MODEL.md`](LEARNING_EVIDENCE_MODEL.md) | How educational evidence accumulates across sessions without numerical scoring |
| [`LEARNING_PROGRESSION_STATES.md`](LEARNING_PROGRESSION_STATES.md) | Meaningful educational progression postures over time |
| [`LEARNING_INTERVENTIONS.md`](LEARNING_INTERVENTIONS.md) | MS001 seed catalogue of tutor responses — **governing educational meaning superseded by** [`../learning_interventions/`](../learning_interventions/) (MS003) |
| [`LEARNING_EXPLAINABILITY.md`](LEARNING_EXPLAINABILITY.md) | How learning progression is explained to students |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract |
| **Daily Coach MS001 — Daily Coaching Model** | Decide *what is most educationally valuable to do today* |
| **Daily Coach MS002 — Learning Session Model** | Decide *how the student should study that objective in one session* |
| **Daily Coach MS003 — Educational Reflection Model** | Decide *what today’s session taught us educationally* |
| **Learning Coach MS001 — this corpus** | Decide *whether the student is genuinely learning over time* |
| **Learning Coach MS002 — Learning Obstacle Model** | Decide *why learning is not progressing as expected* (diagnosis before intervention) — see [`../learning_obstacles/`](../learning_obstacles/) |
| **Learning Coach MS003 — Learning Intervention Framework** | Decide *what educational response is warranted* after diagnosis — see [`../learning_interventions/`](../learning_interventions/) |

```
Student Educational Profile (current diagnosis)
     +  Accumulated Educational Evidence across sessions
     +  Session history & Educational Reflection outputs over time
     +  Knowledge & Mastery ladder (coverage ≠ understanding ≠ mastery)
           →  Learning Coach / Learning Progression Model (this milestone)
                 →  Progression judgement, progression posture,
                    progression explainability
                       →  Learning Obstacle Model (MS002) when growth is stalled,
                          inconsistent, decaying, thin, or falsely ready
                            →  Explicit educational diagnosis
                                 →  Learning Intervention Framework (MS003)
                       →  Informs Profile evolution, Daily Coach emphasis,
                          Master Planner re-consultation when warranted
                       (Runtime A / Twin writers / UI later — out of scope)
```

Daily Coach settles *today’s educational priority*.  
Educational Reflection settles *what one sitting meant*.  
**Learning Coach settles whether those sittings, taken together, constitute genuine educational growth.**  
**Learning Obstacle Model (MS002) settles why growth is blocked — before any intervention recommendation.**  
**Learning Intervention Framework (MS003) settles what educational response is warranted — without rewriting the Canonical Study Plan or overriding Daily Coach authority.**

Architectural companion rule (MS002/MS003): evidence, diagnosis, intervention, and future evidence remain separate layers; no Learning Intervention may be recommended without an explicit educational diagnosis (or explicit insufficient-warrant evidence gathering).

## Architectural requirement

The Learning Coach must **never infer mastery from completion alone**.

Every judgement about progression must be **traceable to accumulated educational evidence** and remain consistent with the Educational Evidence Model and the Student Educational Profile.

| Lawful | Unlawful |
|--------|----------|
| Interpret growth from accumulated observations across sessions | Claim mastery because missions or days were completed |
| Distinguish coverage, familiarity, understanding, retrieval, application, retention, and exam readiness | Collapse any of those into a single checkbox or opaque score |
| Name progression postures provisionally when warrant exists | Invent certainty from thin or single-session history |
| Recommend educational interventions (reinforcement, retrieval, prerequisites, challenge) **after** an explicit obstacle diagnosis when progression is blocked (see MS002 / MS003) | Implement scoring, analytics, or Runtime A decision engines in this corpus; recommend interventions without educational diagnosis; silently rewrite Canonical Study Plan or override Daily Coach |
| Explain why Kwalitec believes learning is (or is not) progressing | Speak optimiser jargon or numeric theatre as educational proof |
| Feed Profile / Daily Coach / Master Planner with progression meaning | Silently rewrite the Canonical Study Plan or Twin states by fiat |

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Scoring systems, mastery formulae, or numerical progression metrics
- Analytics pipelines, dashboards, or A/B instrumentation
- Database models, schemas, or ORM entities
- UI components, charts, or progress theatre
- Algorithms, ML models, or software class designs
- Serialisation formats or API contracts
- Amendments to Constitution, Evidence Model, or Profile meaning (consume them; do not redefine them)

## How to use this corpus

1. Read `LEARNING_PROGRESSION_MODEL.md` first.
2. Treat objectives in `LEARNING_OBJECTIVES.md` as the educational meanings of successful learning.
3. Accumulate and interpret evidence only under `LEARNING_EVIDENCE_MODEL.md`, respecting EIP-002 quality and claim law.
4. Assign progression postures only under `LEARNING_PROGRESSION_STATES.md`.
5. Recommend interventions only as educational guidance under [`../learning_interventions/`](../learning_interventions/) (MS003); `LEARNING_INTERVENTIONS.md` is a compatibility pointer to that corpus.
6. Require explainability contracts from `LEARNING_EXPLAINABILITY.md` (progression) and [`../learning_interventions/INTERVENTION_EXPLAINABILITY.md`](../learning_interventions/INTERVENTION_EXPLAINABILITY.md) (responses) before student-facing narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
