# Workflow Stages

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS001 — Educational Workflow Model  
**Classification:** Constitutional stages of educational workflow orchestration  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional stages** of an educational workflow — how educational reasoning passes between Programme VI components while preserving authority boundaries.

It is subordinate to:

1. [`EDUCATIONAL_WORKFLOW_MODEL.md`](EDUCATIONAL_WORKFLOW_MODEL.md)
2. [`WORKFLOW_OBJECTIVES.md`](WORKFLOW_OBJECTIVES.md)
3. [`WORKFLOW_EVENTS.md`](WORKFLOW_EVENTS.md)
4. [`WORKFLOW_BOUNDARIES.md`](WORKFLOW_BOUNDARIES.md)
5. Programme VI constitutional models for each participating authority

> **Stages sequence participation.  
> Stages do not redefine educational meaning.**

---

## 1. Purpose

An expert tutor moves through recognisable steps: notice what happened, decide whose question it is, gather lawful inputs, let that authority reason, hand off if needed, produce an explainable outcome, and close the loop.

These stages bind Educational Workflow Engine behaviour so orchestration remains auditable and authority-safe.

---

## 2. Stage Principles

1. **Ordered and skip-disciplined.** Stages may be brief under thin context; mandatory authority checks may not be silently omitted when an educational recommendation is claimed.
2. **One primary decider per active path.** Sibling components may contribute read-only inputs.
3. **Explainability accumulates.** Each stage leaves traceable artefacts for `WORKFLOW_EXPLAINABILITY.md`.
4. **Refusal is a stage outcome.** “No recommendation” and “escalate” are first-class conclusions.
5. **Deterministic transitions.** Same classification + context ⇒ same next stage.

---

## 3. Canonical Stage Sequence

```text
S0  Recognise educational event
       ↓
S1  Classify warrant & select primary authority
       ↓
S2  Assemble lawful educational inputs
       ↓
S3  Invoke primary Programme VI reasoning
       ↓
S4  Coordinate sibling inputs / conflict check
       ↓
S5  Authorise outcome (recommend / hand off / refuse / escalate)
       ↓
S6  Explain orchestration
       ↓
S7  Conclude or continue
       ↓
(return on continuation events)
```

---

## 4. Stage Definitions

### S0 — Recognise educational event

**Responsibility**  
Detect and record that a classified educational event has occurred (`WORKFLOW_EVENTS.md`).

**Inputs**  
Observable stimulus (login, session end, evidence write, disruption signal, revision completion, examination proximity, plan signal, student request, etc.).

**Outputs**  
Event instance with class ID (WE-xx), timestamp context, and learner / plan identity references — **not** an educational recommendation.

**Must not**  
Treat recognition as licence to coach; invent missing evidence; mutate Canonical Study Plan.

**Authority preserved**  
No Programme VI decider yet — orchestration only.

---

### S1 — Classify warrant and select primary authority

**Responsibility**  
Judge whether orchestration is warranted and which Programme VI component owns the primary educational question.

**Inputs**  
Event class; Active-class Canonical Study Plan presence/state; current recovery / revision / exam postures; open workflow state; simultaneous warrant set.

**Outputs**  
One of:

| Outcome | Meaning |
|---------|---------|
| **Primary authority selected** | Named Programme VI component will decide |
| **No-op** | Event noted; no workflow progression |
| **Supersede** | Higher-priority warrant replaces a lower open path (explained) |

**Selection guide (qualitative — not a score):**

| If the living educational question is… | Primary authority |
|----------------------------------------|-------------------|
| What should I do today under the plan? | Daily Coach |
| How should this sitting be structured / what did it mean? | Learning Session / Reflection |
| Is learning progressing / what obstacle / what intervention? | Learning Coach |
| How restore progress after meaningful disruption? | Recovery Coach |
| What revise now, and why? | Revision Coach |
| How prepare for / approach the exam? | Exam Coach |
| Do envelopes / plan structure need change? | Master Planner / Scheduling |

**Must not**  
Blend authorities into a hybrid decider; let the workflow invent a primary recommendation; select Exam Coach solely from calendar theatre when Exam Coach warrant fails.

---

### S2 — Assemble lawful educational inputs

**Responsibility**  
Collect only the educational inputs the primary authority is allowed to consume — plan contract, profile, evidence, session history, capacity, sibling coach *meanings already produced*, mode authority.

**Inputs**  
Canonical Study Plan; Student Educational Profile; Educational Evidence trail; recent session/reflection notes; recovery/revision/exam posture artefacts; capacity / interruptions.

**Outputs**  
An input bundle tagged by source authority — ready for Programme VI reasoning.

**Must not**  
Invent missing educational truth; reinterpret evidence; silently substitute coverage for mastery; pull Twin mutation rights into orchestration.

**Authority preserved**  
EIP-001 readers may read; writers remain as Matrix permits. Workflow assembles; it does not author educational states.

---

### S3 — Invoke primary Programme VI reasoning

**Responsibility**  
Hand the living educational question to the selected Programme VI authority under that authority’s constitutional model.

**Inputs**  
S2 input bundle; primary authority identity.

**Outputs**  
Primary educational reasoning artefact as defined by that Programme VI corpus (e.g. today’s guidance, recovery warrant, revision emphasis, exam approach, progression judgement, planning/reschedule need).

**Must not**  
Substitute workflow heuristics for Programme VI decision models; alter the authority’s objectives or boundaries mid-invocation.

**Authority preserved**  
Educational meaning remains 100% with the invoked Programme VI document set.

---

### S4 — Coordinate sibling inputs and conflict check

**Responsibility**  
If sibling coaches provide inputs, ensure they remain **inputs** — and verify that the emerging primary outcome does not conflict with plan protections, mode authority, or a higher-priority warrant.

**Inputs**  
Primary reasoning artefact; optional sibling meanings (e.g. Revision Coach emphasis as Daily Coach input); plan protections; open higher-priority warrants.

**Outputs**  
Conflict-cleared primary artefact, or forced handoff / supersede / refuse.

**Must not**  
Average conflicting coaches into a compromise tip; allow Recovery catch-up to steal protected revision; allow Exam Coach theatre to bypass unfinished first learning when Programme VI forbids it.

**Illustrative coordination (authority-preserving):**

```text
Canonical Study Plan
        │
        ▼
Daily Coach (primary for WE-01 day path)
   ▲            ▲            ▲
   │            │            │
Revision     Recovery     Learning
(input)      (input or    Coach
             supersede    (input)
             if primary)
```

When Recovery warrant is primary, Daily Coach yields; it does not “merge” recovery into a fake ordinary study day without Recovery Coach meaning.

---

### S5 — Authorise outcome

**Responsibility**  
Emit exactly one authorised orchestration outcome class:

| Outcome class | Meaning |
|---------------|---------|
| **Recommend** | Surface the Programme VI educational recommendation as the workflow result |
| **Hand off** | Transfer primary authority to another Programme VI component (named) |
| **Refuse** | Honestly decline to recommend (missing plan, thin warrant, unlawful request) |
| **Escalate** | Structural or envelope change required — Master Planner / Scheduling pathway |

**Must not**  
Invent a fifth outcome that is “workflow’s own tip”; mutate the Canonical Study Plan as an outcome; mint mastery from authorisation alone.

---

### S6 — Explain orchestration

**Responsibility**  
Produce explainability artefacts answering why the workflow started, who participated, how authority was preserved, and why the outcome emerged (`WORKFLOW_EXPLAINABILITY.md`).

**Must not**  
Use explanation to justify unlawful decisions; expose internal IDs in student-facing speech; claim certainty the Programme VI artefact did not claim.

---

### S7 — Conclude or continue

**Responsibility**  
Close the workflow instance when the educational concern is settled for now, or park it awaiting a continuation event (e.g. session complete → reflection).

**Outputs**  
`concluded` | `awaiting_continuation` | `superseded` — with continuity of history preserved.

**Must not**  
Erase learner-owned educational history on conclude; reopen endlessly without new events; treat conclude as mastery.

---

## 5. Worked Illustrations (Educational, Not Implementation)

### 5.1 Student login with Active plan (ordinary day)

| Stage | What happens |
|-------|----------------|
| S0 | WE-01 recognised |
| S1 | Primary = Daily Coach |
| S2 | Plan + profile + recent history + capacity assembled |
| S3 | Daily Coach forms today’s guidance |
| S4 | Optional Revision/Recovery inputs checked; no supersede |
| S5 | Recommend today’s objective |
| S6 | Explain plan + today rationale |
| S7 | Conclude day orchestration (session may open a continuation later) |

### 5.2 Study session completion

| Stage | What happens |
|-------|----------------|
| S0 | WE-02 recognised |
| S1 | Primary = Reflection (then Daily Coach as consumer) |
| S2–S3 | Reflection interprets the sitting under Programme VI Reflection Model |
| S4 | Conflict check — no plan rewrite |
| S5 | Hand off coaching notes into later Daily Coach inputs |
| S6–S7 | Explain; await next day / continue Learning Coach only if progression warrant exists |

### 5.3 Disruption detected mid-journey

| Stage | What happens |
|-------|----------------|
| S0 | WE-04 recognised |
| S1 | Primary = Recovery Coach (may supersede ordinary day path) |
| S2–S3 | Recovery warrant and restorative reasoning under Recovery Model |
| S4 | Daily/Revision/Exam emphases deferred if Recovery is primary |
| S5 | Recommend recovery posture **or** escalate if envelopes break |
| S6–S7 | Explain disruption → recovery; conclude or continue on recovery pathway events |

### 5.4 Examination proximity with unfinished first learning

| Stage | What happens |
|-------|----------------|
| S0 | WE-06 recognised |
| S1 | Exam Coach warrant evaluated — **fails** if Programme VI says learning still primary |
| S3–S5 | Primary remains Learning / Daily Coach path; Exam Coach may contribute only lawful input or no participation |
| S6 | Explain why exam theatre was refused |

---

## 6. Parallel Reads vs Parallel Decides

| Pattern | Lawful? | Meaning |
|---------|---------|---------|
| Parallel **reads** into one primary | Yes | Sibling meanings as inputs |
| Parallel **primary decides** | No | Conflicting educational actions |
| Sequential handoff | Yes | Named transfer of primary authority |
| Silent authority merge | No | Redefines coach meaning |

---

## 7. Binding Rule

Any Educational Workflow Engine behaviour that emits a student-facing educational recommendation without completing S1–S5 (with S6 for material outcomes) is educationally unlawful — even if the recommendation text was copied from a Programme VI document.
