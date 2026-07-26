# Workflow Objectives

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS001 — Educational Workflow Model  
**Classification:** Educational optimisation targets for educational orchestration  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what educational orchestration must optimise**.

It is subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`EDUCATIONAL_WORKFLOW_MODEL.md`](EDUCATIONAL_WORKFLOW_MODEL.md)
3. Programme VI constitutional models (planning and coach meaning authorities)
4. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md)

Algorithms may introduce numerical or operational proxies for these objectives. Proxies never redefine the educational meaning stated here.

> **Workflow objectives specialise product coherence for orchestration.  
> They never authorise contradicting Programme VI educational meaning or Canonical Study Plan commitments.**

---

## 1. Purpose

An expert IFoA tutor does not optimise “number of systems touched.” The tutor optimises **coherent educational action**: the right constitutional voice answers the right educational question after the right educational event, without conflict or invented meaning.

These objectives bind every Educational Workflow Engine behaviour and surface.

---

## 2. Primary Objective

### WO-01 — Coordinate educational reasoning across constitutional components

**Definition.** Ensure that after a classified educational event, the correct Programme VI authorities participate in the correct order so that the student receives one coherent educational outcome — recommendation, handoff, refusal, or escalation — grounded in existing educational meaning.

**Includes:**

- Routing day-level questions to Daily Coach under an Active-class Canonical Study Plan.
- Inviting Learning Coach when the living question is longitudinal progression, obstacle, or intervention.
- Inviting Recovery Coach when meaningful disruption is primary.
- Inviting Revision Coach when consolidating previously learned material is primary.
- Inviting Exam Coach when assessment-facing preparation is primary.
- Escalating structural envelope change to Master Planner / rescheduling pathways.
- Closing the loop so session / reflection outcomes feed subsequent coaching inputs without rewriting the plan.

**Excludes:**

- Merging multiple coach meanings into a single undifferentiated “AI tutor” answer.
- Optimising for throughput of workflow instances as a substitute for educational coherence.
- Treating every event as requiring every coach.
- Inventing a recommendation when no Programme VI authority is warranted.

**Tutor rationale.** Professional exam preparation fails when the student hears conflicting advice from planning, today, recovery, and revision at once. Coordination is educational care.

---

## 3. Supporting Objectives

### WO-02 — Preserve constitutional authority

**Definition.** Ensure orchestration never absorbs, redefines, or silently overrides Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach, Evidence, or Twin mutation authorities.

**Tutor rationale.** Authority leakage destroys trust and constitutional layering. A workflow that “helpfully” rewrites the plan or invents mastery speech is educationally unlawful — even if the UI feels smoother.

**Manifestations:**

- Each stage records which authority owns the educational question.
- Handoffs name the receiving authority explicitly.
- Forbidden actions in `WORKFLOW_BOUNDARIES.md` are hard stops, not soft preferences.

---

### WO-03 — Ensure deterministic educational flow

**Definition.** Given the same classified event and the same educational context inputs, produce the same lawful stage path and participation set.

**Tutor rationale.** Students and auditors must be able to reproduce why a workflow unfolded as it did. Non-deterministic orchestration is indistinguishable from arbitrary tutoring.

**Manifestations:**

- Stable event classification (`WORKFLOW_EVENTS.md`).
- Ordered stages without random coach lottery (`WORKFLOW_STAGES.md`).
- Explicit conflict rules when multiple warrants appear simultaneously.
- Refusal / no-op paths that are themselves deterministic.

---

### WO-04 — Support explainable decision making

**Definition.** Ensure every material orchestrated outcome can answer why the workflow started, which components participated, how authority was preserved, and why the resulting educational recommendation (or handoff / refusal) emerged.

**Tutor rationale.** Opaque orchestration feels like a black box even when Programme VI reasoning underneath is sound. Explainability is part of educational integrity (EIP-003).

**Manifestations:**

- Trace links from event → stages → authorities → outcome (`WORKFLOW_EXPLAINABILITY.md`).
- Student-facing language that cites educational reasons, not infrastructure.
- Developer-facing audit language that cites document IDs without leaking them into student copy.

---

### WO-05 — Prevent conflicting educational actions

**Definition.** Ensure that for a given active workflow instance, at most one primary educational decision is authorised, and that parallel participation is limited to lawful read-only inputs into that primary decider.

**Tutor rationale.** Conflicting actions — e.g. Recovery catch-up intensity and protected revision theft on the same day — destroy plan fidelity and student trust.

**Manifestations:**

- Primary-decider selection rules at warrant stage.
- Suppression or deferral of secondary coach actions until handoff.
- Explicit “input only” posture for sibling coaches (they inform; they do not commandeer).

---

### WO-06 — Preserve Canonical Study Plan fidelity through orchestration

**Definition.** Ensure workflows reinforce — rather than erode — the educational commitments, protections, and envelopes of the Active-class Canonical Study Plan.

**Tutor rationale.** Orchestration that silently consumes revision windows or invents catch-up intensity for “workflow completeness” is plan sabotage.

**Manifestations:**

- Plan mutation never appears as a workflow stage outcome.
- Structural change always escalates to Master Planner / Scheduling pathways.
- Day coaching remains plan-faithful when Daily Coach is primary.

---

### WO-07 — Honour educational continuity and evidence honesty

**Definition.** Ensure orchestration does not erase learner-owned educational history, and does not mint understanding or readiness from workflow completion, login, or calendar proximity alone.

**Tutor rationale.** Completing a workflow is not mastery. Login is not need. Examination proximity is not readiness.

**Manifestations:**

- Continuity Standard (EIP-005) respected across handoffs.
- Evidence Model / Knowledge & Mastery claim types preserved in outcome speech.
- Refusal to treat event occurrence as Educational Evidence of understanding.

---

## 4. Objective Priority When Tension Appears

When objectives appear to conflict, apply this order:

1. **WO-02 — Preserve constitutional authority** (never sacrifice for smoother flow)
2. **WO-06 — Plan fidelity** and **WO-07 — Continuity / evidence honesty**
3. **WO-05 — Prevent conflicting actions**
4. **WO-03 — Deterministic flow**
5. **WO-01 — Coordinate reasoning**
6. **WO-04 — Explainability** (always required for material outcomes, but never used to justify unlawful coordination)

Explainability never legitimises an unlawful orchestration. Determinism never legitimises absorbing coach authority.

---

## 5. Non-Objectives

The Educational Workflow Engine does **not** optimise for:

| Non-objective | Why |
|---------------|-----|
| Maximum coach invocations per day | Noise, not tutoring |
| Shortest path to a recommendation | May skip mandatory authority checks |
| Engagement metrics / streak theatre | Product analytics, not educational orchestration law |
| Pass-rate prediction | Out of scope; not an educational claim this Model may mint |
| Infrastructure utilisation | Engineering concern; not educational meaning |

---

## 6. Binding Rule

Any proposed Educational Workflow Engine behaviour that advances a non-objective at the expense of WO-01…WO-07 is educationally unlawful under this corpus — even if Runtime A, UI, or analytics find it convenient.
