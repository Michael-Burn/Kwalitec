# Transition Boundaries

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS002 — Workflow Transition Framework  
**Classification:** Authority limits — what workflow transitions may and may not do  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **workflow transition authority**: what stage movement may lawfully do, and what must remain with Programme VI, EIP, and MS001 orchestration law.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md)
3. [`WORKFLOW_TRANSITION_FRAMEWORK.md`](WORKFLOW_TRANSITION_FRAMEWORK.md)
4. [`TRANSITION_CATALOGUE.md`](TRANSITION_CATALOGUE.md)
5. [`TRANSITION_CONDITIONS.md`](TRANSITION_CONDITIONS.md)
6. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md)
7. Programme VI coach and Master Planner boundary corpora

> **Workflow transitions may move workflows between constitutional stages,  
> preserve coach authority,  
> and coordinate educational flow.  
> They must not reinterpret educational evidence,  
> modify coach recommendations,  
> rewrite educational plans,  
> or introduce independent educational decisions.**

---

## 1. Purpose

A transition that quietly becomes a tutor — rewriting plans, editing coach tips, or reinterpreting evidence “so the flow can continue” — destroys constitutional layering and student trust.

This document draws a bright line between **lawful stage movement** (MS002) and **educational meaning / mutation authority** (Programme VI + EIP), while remaining consistent with MS001 workflow boundaries.

---

## 2. Boundary Principles

1. **Move flow, do not educate by substitute.** Transitions advance stages; Programme VI answers educational questions.
2. **Preserve coach authority.** Transition never alters Daily, Learning, Recovery, Revision, or Exam meanings.
3. **Plan non-mutation.** Canonical Study Plan remains Master Planner / Scheduling contract.
4. **Evidence non-reinterpretation.** Evidence Model and permitted writers own observational truth.
5. **No independent recommendations.** Stage movement never mints a tip of its own.
6. **No recommendation mutation.** Already-emitted Programme VI artefacts are inputs, not editable props.
7. **State Matrix supremacy.** Transitions never gain mutation rights by renaming themselves.
8. **Conditions over convenience.** Failed conditions ⇒ remain / pause / refuse / escalate — not force-advance.
9. **MS001 boundaries inherited.** B1–B7 in `WORKFLOW_BOUNDARIES.md` remain binding during every transition.
10. **Explain the limit.** Students and developers should hear when movement stops and another authority must act.

---

## 3. What Workflow Transitions May Do (Lawful)

| Lawful action | Educational / orchestration meaning |
|---------------|-------------------------------------|
| **Move between constitutional stages** | Advance S0→S7 when WT-02 conditions hold |
| **Open and close lifecycle postures** | Initiate (WT-01), conclude (WT-06), park (WT-10) |
| **Pause awaiting outputs** | WT-03 when educational / evidence artefacts are missing |
| **Resume when outputs or continuation events arrive** | WT-04 without inventing meaning |
| **Escalate structural concerns** | WT-05 naming Master Planner / Scheduling pathways |
| **Supersede lower-priority paths** | WT-07 under MS001 conflict rules |
| **Hand off primary authority by name** | WT-08 without blending coaches |
| **Require explainability after outcomes** | WT-09 S5→S6 |
| **Preserve coach authority during movement** | Record that Programme VI meanings were not altered by the transition |
| **Coordinate educational flow** | Keep one primary decision path; sequence participation |

These actions **coordinate stage movement**. They do **not** publish a new Study Plan, mint mastery, reinterpret evidence, edit coach recommendations, or replace any coach.

---

## 4. What Workflow Transitions Must NOT Do

| Forbidden action | Why | Lawful alternative |
|------------------|-----|--------------------|
| **Reinterpret Educational Evidence** | Evidence Model + permitted writers own observational truth | Await lawful writes (WT-03); consume as classified |
| **Modify coach recommendations** | Programme VI owns educational artefacts | Hand off or escalate; do not edit the tip to “fit” the next stage |
| **Rewrite educational plans** | Canonical Study Plan is Master Planner / Scheduling contract | WT-05 escalate; never silent cell/intent mutation |
| **Introduce independent educational decisions** | Recommendations require Programme VI warrant | Invoke S3; surface S5 from that artefact only |
| **Skip mandatory authority stages while claiming a recommendation** | MS001 stage discipline / B1 | Complete S1–S5 (and S6 for material outcomes) |
| **Invent evidence or coach outputs to unblock WT-02** | Honesty / C-OUTPUT | WT-03 pause |
| **Merge conflicting coaches during supersede or handoff** | Single primary / WO-05 | Explicit WT-07 or WT-08 |
| **Mint Estimated Knowledge / Mastery from transition completion** | EIP-006 / Twin / Evidence | Leave estimates to permitted writers |
| **Erase educational history on conclude or supersede** | EIP-005 Continuity | Change orchestration posture only |
| **Bypass State Authority Matrix** | EIP-001 | Readers assemble; writers remain listed |
| **Use timers or schedulers as educational permission** | No timer-as-tutor | Educational events and output availability only |
| **Redefine MS001 event or stage meaning via transition labels** | MS001 supremacy for those objects | Amend MS001 first if change is needed |

---

## 5. Authority Map

```
Educational Constitution / EIP
        │
        ▼
Programme VI — educational meaning (immutable to transitions)
  Master Planner ──► Canonical Study Plan
  Daily · Session · Reflection · Learning · Recovery · Revision · Exam
        │
        ▼
Programme VII MS001 — workflow events, stages, orchestration boundaries
        │
        ▼
Programme VII MS002 — workflow transitions (this corpus)
        │  may move stages / pause / resume / escalate / conclude
        │  must not alter Programme VI meaning or MS001 definitions
        ▼
Product / Runtime A / UI (future)
        │  must consume boundaries
```

---

## 6. Boundary Tests (Pass / Fail)

Use these tests before accepting any proposed transition behaviour:

| # | Test question | Pass means |
|---|---------------|------------|
| T1 | Does the move map to a named WT-xx with satisfied conditions? | Yes |
| T2 | Does the transition reinterpret Educational Evidence? | Must be No |
| T3 | Does the transition modify any Programme VI recommendation artefact? | Must be No |
| T4 | Does the transition rewrite Canonical Study Plan educational intent? | Must be No |
| T5 | Does the transition introduce an independent educational decision? | Must be No |
| T6 | After the move, is there at most one primary educational decider? | Yes |
| T7 | If a recommendation is claimed, were S1–S5 completed (and S6 for material outcomes)? | Yes |
| T8 | Can transition explainability answer why moved, which condition, who participated, and why authority was unchanged? | Yes |

Any **Fail** ⇒ educationally unlawful under this milestone.

MS001 tests B1–B7 remain in force; T1–T8 specialise them for stage movement.

---

## 7. Relationship to MS001 Workflow Boundaries

| MS001 (workflows) | MS002 (transitions) |
|-------------------|---------------------|
| What orchestration may do across a workflow | What *stage movement* may do at a moment of change |
| May open/continue/conclude workflows | May initiate/advance/pause/resume/escalate/conclude via WT-xx |
| Must not redefine coaches / plans / evidence / tips | Must not do those things *as side-effects of moving* |

A transition that would pass T1–T8 but fail B1–B7 is still unlawful. MS002 does not weaken MS001.

---

## 8. Relationship to Adjacent Architecture

| Adjacent artefact | Relationship |
|-------------------|--------------|
| Version 2 Educational Orchestration Model | May describe tutoring collaboration grain; **must not** override these transition boundaries |
| Design Principles (workflow-first navigation) | Product UX constraint; educational authority remains Programme VI + MS001/MS002 |
| Runtime state machines / sagas (future) | May implement WT-xx checks; must not redefine educational meaning |

Architecture implements boundaries. Architecture does not amend them by code convenience.

---

## 9. Binding Rule

If advancing a stage would be easier by reinterpreting evidence, editing a coach recommendation, rewriting the plan, or inventing an independent tip — **stop**. Pause, refuse, escalate, or amend the owning Programme VI / EIP / MS001 authorities first. Programme VII transitions do not gain educational meaning by shortcut.
