# Daily Coaching Model

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS001 — Daily Coaching Model  
**Classification:** Educational reasoning specification — day-to-day coaching from a Canonical Study Plan  
**Status:** APPROVED — governing for Daily Coach educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec converts a Canonical Study Plan into meaningful day-to-day coaching**.

It answers *what an experienced IFoA tutor would choose for the student to do today*, *which educational inputs that choice requires*, *what educational outputs coaching may emit*, *how conflicts and recovery are decided*, and *how today’s advice is explained in plain educational language*.

It does **not** implement mission generation algorithms, Runtime A services, scheduling, notifications, or application code.

> **The Daily Coach interprets an authorised Canonical Study Plan.  
> It never redesigns, silently rewrites, or invents long-term educational intent.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-002, EL-003, EL-008, EL-009, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
8. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / Master Planner MS002)
9. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006 — when lived divergence requires allocation change)

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map
- [`knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md`](../../product/LEARNING_EXPERIENCE_PROGRAMME.md) — product daily-loop design (consumes, does not redefine, this educational law)
- Educational Validation Framework EC-02 (Daily Coach) — quality release lens, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`DAILY_COACH_MODEL.md`](DAILY_COACH_MODEL.md) | Constitutional overview: what the Daily Coach is, responsibilities, integrity, stack position |
| [`DAILY_COACH_OBJECTIVES.md`](DAILY_COACH_OBJECTIVES.md) | What day-to-day coaching must optimise educationally |
| [`DAILY_COACH_DECISION_MODEL.md`](DAILY_COACH_DECISION_MODEL.md) | Priority ordering, conflict handling, recovery, adaptation boundaries, escalation |
| [`DAILY_COACH_INPUTS.md`](DAILY_COACH_INPUTS.md) | Educational inputs required before today’s guidance may be formed |
| [`DAILY_COACH_OUTPUTS.md`](DAILY_COACH_OUTPUTS.md) | Educational outputs the Daily Coach may produce |
| [`DAILY_COACH_EXPLAINABILITY.md`](DAILY_COACH_EXPLAINABILITY.md) | How today’s recommendations must be explained |

## Relationship to Master Planner (Programme VI)

| Horizon | Job |
|---------|-----|
| **Master Planner MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **Master Planner MS003–MS006** | Choose strategy, decide, blueprint, and schedule the journey |
| **Master Planner MS007 — Canonical Study Plan** | Publish the *authorised preparation contract* for coaching |
| **Daily Coach MS001 — this corpus** | Decide *what is most educationally valuable to do today* under that contract |
| **Daily Coach MS002 — Learning Session Model** | Decide *how the student should study that objective in one session* ([`../learning_session/`](../learning_session/)) |
| **Daily Coach MS003 — Educational Reflection Model** | Decide *what today’s session taught us educationally* ([`../reflection/`](../reflection/)) — feeds subsequent Daily Coach days; never rewrites the Canonical Study Plan |

```
Canonical Study Plan (MS007)
     +  Student Educational Profile (current diagnosis)
     +  Recent learning evidence & session history
     +  Today’s capacity / interruptions / recovery posture
           →  Daily Coach (this milestone)
                 →  Educational guidance for today (DCO-01)
                       →  Learning Session Model (MS002)
                             →  Session aims, phases, transitions, local adaptation
                       →  Educational Reflection Model (MS003)
                             →  Attainment, evidence reading, reinforcement /
                                continuation / escalation, coaching notes
                             →  Feeds later Daily Coach inputs (DCI-06 / DCI-07)
                       (mission / Runtime A / UI later — out of scope)
```

Master Planner settles *the long-term educational promise*.  
Daily Coach settles *today’s educational priority within that promise*.  
Learning Session settles *how that priority is studied in one sitting* — without redefining the day.  
Educational Reflection settles *what the sitting meant* — closing the loop into tomorrow’s coaching without rewriting the plan.

## Architectural requirement

The Daily Coach must **never invalidate or silently rewrite** the Canonical Study Plan.

| Lawful | Unlawful |
|--------|----------|
| Select today’s objective from authorised plan sessions, phases, and protections | Invent a new phase, revision window, intensity band, or sitting ambition |
| Adapt today’s emphasis inside plan envelopes (e.g. honour recovery capacity already placed) | Convert recovery into punishment catch-up or steal protected revision |
| Respond to recent evidence without claiming mastery from completion alone | Mint understanding or readiness claims from ticks or calendar density |
| Identify when lived divergence requires rescheduling or upstream replan | Silently redesign long-term educational intent “for today’s convenience” |
| Explain today’s advice with plan + current context | Speak opaque optimisation or engineering jargon |

If today’s situation requires changing educational envelopes, protections, or sitting ambition, the Daily Coach **escalates** — it does not absorb Master Planner authority.

## Out of scope (MS001)

- Mission generation algorithms or Today’s Mission selection code
- Runtime A integration, feature flags, or services
- Database models, schemas, or ORM entities
- UI components, notifications, or push scheduling
- Calendar packing / rescheduling algorithms (owned by Master Planner MS006)
- Serialisation formats or API contracts
- Software class designs or service interfaces

## How to use this corpus

1. Read `DAILY_COACH_MODEL.md` first.
2. Treat objectives in `DAILY_COACH_OBJECTIVES.md` as binding optimisation targets for daily guidance.
3. Classify every proposed daily coaching behaviour under `DAILY_COACH_DECISION_MODEL.md`.
4. Require inputs from `DAILY_COACH_INPUTS.md` — never invent missing educational truth.
5. Emit only educational outputs defined in `DAILY_COACH_OUTPUTS.md`.
6. Require explainability contracts from `DAILY_COACH_EXPLAINABILITY.md` before student-facing daily narration.
7. Do not implement algorithms that contradict this corpus without amending it first.
