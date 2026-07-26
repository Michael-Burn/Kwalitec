# Transition Catalogue

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS002 — Workflow Transition Framework  
**Classification:** Named lawful workflow transition kinds  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional catalogue of workflow transitions** — the named kinds of lawful movement between MS001 orchestration stages and lifecycle postures.

It is subordinate to:

1. [`WORKFLOW_TRANSITION_FRAMEWORK.md`](WORKFLOW_TRANSITION_FRAMEWORK.md)
2. [`../workflows/EDUCATIONAL_WORKFLOW_MODEL.md`](../workflows/EDUCATIONAL_WORKFLOW_MODEL.md)
3. [`../workflows/WORKFLOW_EVENTS.md`](../workflows/WORKFLOW_EVENTS.md)
4. [`../workflows/WORKFLOW_STAGES.md`](../workflows/WORKFLOW_STAGES.md)
5. [`TRANSITION_CONDITIONS.md`](TRANSITION_CONDITIONS.md)
6. [`TRANSITION_BOUNDARIES.md`](TRANSITION_BOUNDARIES.md)

> **Transitions represent orchestration only.  
> They do not create educational meaning.**

---

## 1. Purpose

Without a shared transition vocabulary, orchestration either jumps stages silently or invents “reasons” that sound like educational decisions.

This catalogue names **what kinds of movement may lawfully occur**. Permitting conditions live in `TRANSITION_CONDITIONS.md`. Hard stops live in `TRANSITION_BOUNDARIES.md`.

Each transition has an ID for audit/developer use. Student-facing speech must not dump these IDs.

---

## 2. Catalogue Principles

1. **Orchestration, not meaning.** A transition moves stage or posture; it does not answer a coach question.
2. **Named and auditable.** Every material stage movement maps to a WT-xx class (or an explicit composite of named classes).
3. **Stage-faithful.** Destinations respect MS001 S0–S7 and lifecycle postures (`awaiting_continuation`, `concluded`, `superseded`).
4. **Deterministic classification.** The same stage + same lawful situation maps to the same transition kind.
5. **Composition is explicit.** Pause then later resume are two transitions, not one opaque “eventually.”
6. **Absence is speakable.** “No transition warranted” (remain in stage) is lawful when conditions fail.

---

## 3. Lifecycle Postures (Adjacent to Stages)

In addition to MS001 stages S0–S7, transitions may refer to these orchestration postures:

| Posture | Meaning |
|---------|---------|
| **unopened** | No workflow instance for this educational concern |
| **in_stage (Sn)** | Active instance currently at stage Sn |
| **awaiting_output** | Paused pending a named educational or evidence output |
| **awaiting_continuation** | Parked until a continuation event (WE-xx) arrives |
| **concluded** | Educational concern settled for now |
| **superseded** | Replaced by a higher-priority workflow path |
| **no_op_recorded** | Event classified; no orchestration progression |

---

## 4. Transition Catalogue

### WT-01 — Event received → workflow initiated

| Aspect | Meaning |
|--------|---------|
| **Definition** | A classified educational event (WE-xx) opens a new workflow instance and enters **S0 — Recognise educational event** (then progresses under subsequent transitions) |
| **From** | `unopened` (or `no_op_recorded` superseded by a new warrant) |
| **To** | `in_stage (S0)` with event class recorded |
| **Orchestrates** | Lifecycle open; does not select today’s objective or any coach recommendation |
| **Must not imply** | Initiation equals educational advice; initiation equals mastery; initiation mutates the Canonical Study Plan |
| **Typical companions** | Followed by WT-02 toward S1 when warrant classification is required |

---

### WT-02 — Stage completed → next stage

| Aspect | Meaning |
|--------|---------|
| **Definition** | The current MS001 stage has produced its lawful stage outputs; the workflow advances to the next ordered stage in S0→S7 |
| **From** | `in_stage (Sn)` where Sn ∈ {S0…S6} |
| **To** | `in_stage (S{n+1})` — or a documented lawful short-circuit destination only when `TRANSITION_CONDITIONS.md` permits (e.g. no-op exit from S1) |
| **Orchestrates** | Ordered stage progression; accumulates explainability artefacts |
| **Must not imply** | Stage completion invents Programme VI reasoning; skipping S1–S5 while claiming a recommendation |
| **Canonical advances** | S0→S1, S1→S2, S2→S3, S3→S4, S4→S5, S5→S6, S6→S7 |

**Lawful short-circuits (still WT-02 subclass destinations, not new meanings):**

| At stage | Lawful destination when conditions hold | Meaning |
|----------|-------------------------------------------|---------|
| S1 | Conclude via WT-06 / record no-op | Warrant fails — no orchestration needed |
| S1 | Remain / supersede path (WT-07) | Higher-priority warrant replaces this path |
| S5 | S6 then S7 | Outcome authorised — explain and close or continue |

Silent jumps from S0 to S5 (or S3) while claiming a student-facing recommendation are **unlawful**, even if labelled WT-02.

---

### WT-03 — Workflow paused awaiting evidence or educational output

| Aspect | Meaning |
|--------|---------|
| **Definition** | The workflow cannot lawfully advance because a named prerequisite educational output or lawful evidence artefact is not yet available |
| **From** | `in_stage (Sn)` — commonly S2 (inputs), S3 (awaiting Programme VI artefact), or S7 continuation park |
| **To** | `awaiting_output` with a named awaited artefact class |
| **Orchestrates** | Honest waiting; preserves open concern without inventing missing truth |
| **Must not imply** | Pause fabricates evidence; pause reinterprets thin trails as understanding; pause rewrites the plan “to keep moving” |
| **Examples of awaited artefacts (illustrative)** | Lawful Educational Evidence write; Reflection coaching notes; Recovery warrant artefact; Revision completion judgement; Exam Coach warrant evaluation result; Master Planner structural response |

---

### WT-04 — Workflow resumed

| Aspect | Meaning |
|--------|---------|
| **Definition** | A paused or continuation-parked workflow re-enters active stage progression because the awaited output is available **or** a lawful continuation event has arrived |
| **From** | `awaiting_output` or `awaiting_continuation` |
| **To** | `in_stage (Sn)` — typically the stage that was waiting, or the next stage whose conditions are now satisfied |
| **Orchestrates** | Continuation of the same educational concern; does not open a conflicting second primary path without supersede rules |
| **Must not imply** | Resume invents the awaited meaning; resume overrides coach authority; resume equals mastery from waiting |

**Resume subtypes (same WT-04 class, distinct condition keys):**

| Subtype | Trigger posture | Meaning |
|---------|-----------------|---------|
| **Output-available resume** | Awaited artefact now present | Continue assembly or invocation |
| **Continuation-event resume** | WE-xx continue pattern | e.g. session complete → reflection path |

---

### WT-05 — Workflow escalated

| Aspect | Meaning |
|--------|---------|
| **Definition** | The living educational concern cannot be resolved within current coach envelopes; orchestration transfers the primary structural question to Master Planner / Scheduling pathways (or records S5 **escalate** and moves accordingly) |
| **From** | Typically `in_stage (S4)` or `in_stage (S5)` after conflict / envelope failure; may also arise from S1 when structural signal (WE-08) is primary |
| **To** | Hand-off posture toward Master Planner primary authority — stages S2–S5 under Master Planner / Scheduling meaning — or `awaiting_output` for structural response |
| **Orchestrates** | Named structural escalation; preserves coach meanings that triggered the need |
| **Must not imply** | Escalation silently rewrites the Canonical Study Plan; escalation invents a temporary plan; coaches may mutate envelopes “while escalating” |

Escalation is a **transition of orchestration primary**, not a licence for Programme VII to author plan educational intent.

---

### WT-06 — Workflow completed (concluded)

| Aspect | Meaning |
|--------|---------|
| **Definition** | The educational concern for this workflow instance is settled for now; the instance moves to `concluded` after S7 (or after a lawful S1 no-op / refuse path that requires no further stages) |
| **From** | `in_stage (S7)` with conclude decision; or early lawful no-op / refuse close |
| **To** | `concluded` |
| **Orchestrates** | Lifecycle close; preserves educational history |
| **Must not imply** | Conclusion equals mastery, readiness, or exam certainty; conclusion erases learner-owned records; conclusion invents a final tip |

---

### WT-07 — Workflow superseded

| Aspect | Meaning |
|--------|---------|
| **Definition** | A higher-priority warrant (e.g. meaningful disruption WE-04, structural signal WE-08) pauses or ends a lower-priority open workflow with explicit explanation |
| **From** | `in_stage (Sn)` or `awaiting_*` on the lower-priority path |
| **To** | `superseded` for the lower path; new or continuing higher-priority path via WT-01 / WT-04 as applicable |
| **Orchestrates** | Single primary decision integrity (MS001 WO / stages) |
| **Must not imply** | Supersede merges coaches into a hybrid tip; supersede deletes educational history; supersede rewrites the plan |

---

### WT-08 — Primary authority handoff (within orchestration)

| Aspect | Meaning |
|--------|---------|
| **Definition** | The living educational question changes; orchestration transfers **primary** Programme VI authority to a named sibling (or from coach to planner) while remaining inside the workflow instance — typically expressed at S5 as **hand off**, then re-entering S1/S2 under the new primary |
| **From** | `in_stage (S5)` hand-off outcome (or S4 forced handoff) |
| **To** | `in_stage (S1)` or `in_stage (S2)` with new primary authority named |
| **Orchestrates** | Explicit authority transfer; one primary at a time |
| **Must not imply** | Handoff blends two primaries; handoff redefines the receiving coach’s question; handoff modifies the prior coach’s artefact |

---

### WT-09 — Outcome authorised → explain

| Aspect | Meaning |
|--------|---------|
| **Definition** | S5 has emitted recommend / hand off / refuse / escalate; orchestration moves to **S6 — Explain orchestration** |
| **From** | `in_stage (S5)` with authorised outcome class |
| **To** | `in_stage (S6)` |
| **Orchestrates** | Mandatory explainability before material student-facing close |
| **Must not imply** | Explanation invents certainty; explanation justifies unlawful outcomes; explanation rewrites Programme VI content |

WT-09 is the specialised S5→S6 case of WT-02, named so explainability cannot be “optimised away.”

---

### WT-10 — Park awaiting continuation event

| Aspect | Meaning |
|--------|---------|
| **Definition** | At S7, the concern is not fully settled for the journey, but further progress requires a future educational event (e.g. session sitting to complete before reflection) |
| **From** | `in_stage (S7)` with continue decision |
| **To** | `awaiting_continuation` |
| **Orchestrates** | Honest parking; links to WE-xx continue patterns |
| **Must not imply** | Parking invents interim coaching; parking equals abandonment; parking mutates plan envelopes |

Resume from this posture uses WT-04 (continuation-event resume).

---

## 5. Catalogue Map (Summary)

| ID | Transition | Primary job |
|----|------------|-------------|
| **WT-01** | Event → initiated | Open workflow at S0 |
| **WT-02** | Stage → next stage | Ordered S0–S7 advance |
| **WT-03** | Pause awaiting output | Honest wait for evidence / Programme VI artefact |
| **WT-04** | Resume | Re-enter stage progression |
| **WT-05** | Escalate | Structural / Master Planner pathway |
| **WT-06** | Complete | Conclude instance |
| **WT-07** | Supersede | Higher-priority warrant wins |
| **WT-08** | Authority handoff | Named primary transfer |
| **WT-09** | Authorise → explain | Force S6 after S5 |
| **WT-10** | Park continuation | Await next WE-xx |

```text
unopened
   │ WT-01
   ▼
 S0 ──WT-02──► S1 ──WT-02──► S2 ──WT-02──► S3 ──WT-02──► S4 ──WT-02──► S5
                │              │              │                         │
                │              │ WT-03         │ WT-03                   │ WT-09
                │              ▼              ▼                         ▼
                │         awaiting_output ◄──┘                         S6
                │              │ WT-04                                   │ WT-02
                │              ▼                                         ▼
                │             Sn                                        S7
                │                                          ┌────────────┼────────────┐
                │                                          │            │            │
                │                                       WT-06        WT-10        WT-05
                │                                          │            │            │
                │                                          ▼            ▼            ▼
                │                                     concluded  awaiting_cont  escalate path
                │
                └── WT-07 supersede / WT-08 handoff (re-enter S1/S2 under new primary)
```

---

## 6. What Is Not a Workflow Transition

| Non-transition | Why |
|----------------|-----|
| Changing a coach recommendation text | Programme VI meaning change — not orchestration movement |
| Rewriting Canonical Study Plan cells | Master Planner / Scheduling mutation — forbidden to Programme VII |
| Re-labelling evidence as understanding | Evidence Model violation |
| UI route change without stage movement | Product navigation, not transition law |
| Background job retry | Infrastructure |
| A/B experiment arm flip | Analytics / experiment framework |
| Timer tick alone forcing S3→S5 | Unlawful skip; no timer-as-tutor |

---

## 7. Binding Rule

No Educational Workflow Engine behaviour may advance, pause, resume, escalate, supersede, hand off, or conclude a workflow under a label absent from this catalogue — or invent educational meaning while doing so. Classify the transition; verify conditions; preserve authority; explain.
