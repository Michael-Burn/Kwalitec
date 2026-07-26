# Educational Reflection Model

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS003 — Educational Reflection Model  
**Classification:** Educational reasoning specification — post-session interpretation that closes the daily coaching loop  
**Status:** APPROVED — governing for Educational Reflection educational meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec interprets the outcome of a completed learning session**.

It answers *what an experienced IFoA tutor would conclude after today’s study*, *which educational questions reflection must settle*, *which post-session evidence may be used*, *how conclusions are formed without scoring theatre*, *what educational outcomes reflection may emit*, and *how today’s learning is explained before tomorrow’s coaching*.

It does **not** implement Runtime A, evidence scoring, analytics, databases, UI, or application code.

> **The Educational Reflection Model answers: “What did we learn from today’s study?”  
> It may update educational understanding and recommendations.  
> It must never directly rewrite the Canonical Study Plan.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-002, EL-003, EL-008, EL-009, EL-010, EL-011
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../daily_coach/DAILY_COACH_MODEL.md`](../daily_coach/DAILY_COACH_MODEL.md) (Programme VI / Daily Coach MS001)
8. [`../learning_session/LEARNING_SESSION_MODEL.md`](../learning_session/LEARNING_SESSION_MODEL.md) (Programme VI / Daily Coach MS002)
9. [`../study_plan/CANONICAL_STUDY_PLAN.md`](../study_plan/CANONICAL_STUDY_PLAN.md) (Programme VI / Master Planner MS007)
10. [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) (Programme VI / Master Planner MS006 — when lived divergence requires allocation change)

Related (non-authoritative for educational meaning):

- [`knowledge/research/RIP-001_DAILY_REFLECTION_AND_PRODUCT_CHECKIN.md`](../../research/RIP-001_DAILY_REFLECTION_AND_PRODUCT_CHECKIN.md) — product research check-in (observes product experience; must not write educational understanding)
- Educational Validation Framework EC-02 (Daily Coach) — quality release lens, not educational meaning authority

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_REFLECTION_MODEL.md`](EDUCATIONAL_REFLECTION_MODEL.md) | Constitutional overview: what Educational Reflection is, responsibilities, integrity, stack position |
| [`REFLECTION_OBJECTIVES.md`](REFLECTION_OBJECTIVES.md) | What educational reflection seeks to establish after a session |
| [`REFLECTION_INPUTS.md`](REFLECTION_INPUTS.md) | Educational evidence available after a study session |
| [`REFLECTION_INTERPRETATION.md`](REFLECTION_INTERPRETATION.md) | How an expert tutor forms educational conclusions from today’s evidence |
| [`REFLECTION_OUTPUTS.md`](REFLECTION_OUTPUTS.md) | Educational outcomes reflection may produce |
| [`REFLECTION_EXPLAINABILITY.md`](REFLECTION_EXPLAINABILITY.md) | How today’s achievement, remaining gaps, and coaching influence are explained |

## Relationship in the Programme VI stack

| Horizon | Job |
|---------|-----|
| **Master Planner MS007 — Canonical Study Plan** | Publish the authorised preparation contract |
| **Daily Coach MS001 — Daily Coaching Model** | Decide *what is most educationally valuable to do today* |
| **Daily Coach MS002 — Learning Session Model** | Decide *how the student should study that objective in one session* |
| **Daily Coach MS003 — this corpus** | Decide *what today’s session taught us educationally, and what that implies for tomorrow* |

```
Learning Session closes (aims, phases, local adaptation complete)
     +  Post-session educational evidence (completion, retrieval, practice,
        self-reflection, misconceptions, confidence, interruptions)
     +  Today’s Daily Coach objective as the reflection warrant
           →  Educational Reflection Model (this milestone)
                 →  Updated understanding posture, reinforcement /
                    continuation / escalation recommendations,
                    coaching notes, reflection explainability
                       →  Feeds Daily Coach inputs for subsequent days
                          (DCI-06 / DCI-07 modulation — never plan rewrite)
                       (Runtime A / Twin writers / UI later — out of scope)
```

Daily Coach settles *today’s educational priority*.  
Learning Session settles *how that priority is studied*.  
Educational Reflection settles *what the session produced educationally* — closing the loop into tomorrow’s coaching.

## Architectural requirement

Reflection may **update educational understanding and recommendations**.

It must **never directly rewrite** the Canonical Study Plan.

| Lawful | Unlawful |
|--------|----------|
| Interpret today’s session against today’s Daily Coach objective | Claim mastery from session completion alone |
| Recommend reinforcement, continuation, or confidence adjustment inside plan envelopes | Silently redesign phase meaning, intensity, or sitting ambition |
| Name misconceptions and remaining uncertainty honestly | Invent evidence or fill thin history with certainty theatre |
| Escalate when long-term change is required | Directly rewrite Canonical Study Plan commitments |
| Feed tomorrow’s Daily Coach via established input meanings (recent evidence / session history) | Bypass Daily Coach rescheduling / replanning pathways for structural change |
| Explain what was achieved and what remains | Speak opaque scores, optimiser language, or product-survey results as learning proof |

Any recommendation requiring long-term change must escalate through the established **Daily Coach rescheduling or replanning pathways** — Reflection does not absorb Master Planner authority.

## Hard boundary — Educational vs product reflection

| Domain | Authority | May write educational understanding? |
|--------|-----------|--------------------------------------|
| **Educational Reflection (this corpus)** | Learning interpretation after a study session | Yes — via lawful Evidence → Inference pathways governed elsewhere |
| **Product Daily Reflection / check-in (RIP-001)** | Product experience research | **No** |

Product feedback must never be renamed as Educational Reflection outcomes.

## Out of scope (MS003)

- Runtime A integration, feature flags, or services
- Evidence scoring engines, analytics pipelines, or dashboards
- Database models, schemas, or ORM entities
- Digital Twin write implementations (governed by Evidence Model / Twin authority — not redefined here)
- UI components, notifications, or survey widgets
- Mission generation algorithms
- Serialisation formats or API contracts
- Software class designs or service interfaces
- Amendments to Canonical Study Plan structure (Master Planner MS007)

## How to use this corpus

1. Read `EDUCATIONAL_REFLECTION_MODEL.md` first.
2. Treat aims in `REFLECTION_OBJECTIVES.md` as binding questions reflection must answer.
3. Require inputs from `REFLECTION_INPUTS.md` — never invent missing educational truth.
4. Form conclusions only under `REFLECTION_INTERPRETATION.md`, respecting Evidence Model principles.
5. Emit only educational outputs defined in `REFLECTION_OUTPUTS.md`.
6. Require explainability contracts from `REFLECTION_EXPLAINABILITY.md` before student-facing reflection narration.
7. Escalate structural plan change; never silent rewrite.
8. Do not implement algorithms that contradict this corpus without amending it first.
