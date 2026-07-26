# Transition Conditions

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS002 — Workflow Transition Framework  
**Classification:** Constitutional conditions that permit workflow transitions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional conditions** that must hold before a catalogue transition (WT-xx) may occur.

It is subordinate to:

1. [`WORKFLOW_TRANSITION_FRAMEWORK.md`](WORKFLOW_TRANSITION_FRAMEWORK.md)
2. [`TRANSITION_CATALOGUE.md`](TRANSITION_CATALOGUE.md)
3. [`TRANSITION_BOUNDARIES.md`](TRANSITION_BOUNDARIES.md)
4. [`../workflows/WORKFLOW_STAGES.md`](../workflows/WORKFLOW_STAGES.md)
5. [`../workflows/WORKFLOW_EVENTS.md`](../workflows/WORKFLOW_EVENTS.md)
6. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md)
7. Programme VI models for availability of educational outputs (without redefining those models)

> **Conditions permit orchestration movement.  
> Conditions do not invent educational recommendations.**

---

## 1. Purpose

Transitions without conditions become product convenience. Conditions without a catalogue become unenforceable folklore.

This document states **what must be true** — in educational and orchestration terms — for each WT-xx move. It introduces **no runtime algorithms, scores, timers-as-tutors, or scheduling logic**.

---

## 2. Condition Families

Every permitting check is expressed using one or more of these families:

| Family | Meaning | Asks |
|--------|---------|------|
| **C-STATE** | Workflow state / posture | Where is the instance now? |
| **C-AUTH** | Constitutional authority | Whose question is primary? Is mutation forbidden? |
| **C-OUTPUT** | Availability of educational outputs | Is the required Programme VI / evidence artefact present? |
| **C-PREREQ** | Completion of prerequisite stages | Have mandatory prior stages produced their outputs? |

Optional supporting family (never a substitute for the four above):

| Family | Meaning |
|--------|---------|
| **C-EVENT** | A classified WE-xx initiate/continue/supersede stimulus is present when the catalogue requires it |

Conditions are **qualitative constitutional facts**, not computed rankings.

---

## 3. Global Preconditions (All Transitions)

Before **any** WT-xx transition:

| # | Condition | Family |
|---|-----------|--------|
| G1 | The proposed move is a named catalogue transition (or explicit documented composite) | C-STATE |
| G2 | The move does not require redefining Programme VI coach / planner meaning | C-AUTH |
| G3 | The move does not mutate Canonical Study Plan educational intent | C-AUTH |
| G4 | The move does not reinterpret Educational Evidence or mint mastery from movement alone | C-AUTH / C-OUTPUT |
| G5 | At most one primary educational decider remains after the move (unless documented read-only inputs) | C-AUTH |
| G6 | Learner-owned educational history is preserved (EIP-005) | C-AUTH |

Failure of any global precondition ⇒ **transition refused**; remain in current stage/posture and explain.

---

## 4. Conditions by Transition

### WT-01 — Event received → workflow initiated

| # | Condition | Family |
|---|-----------|--------|
| 01.1 | A classified educational event WE-xx is recognised (not a non-event) | C-EVENT |
| 01.2 | Current posture for this concern is `unopened` (or prior no-op may be replaced by a new warrant) | C-STATE |
| 01.3 | Opening does not create a second conflicting primary without applying WT-07 supersede rules | C-AUTH |
| 01.4 | Initiation records event class only — no recommendation artefact required or invented | C-OUTPUT |

**Fails when:** stimulus is infrastructure/analytics-only; a conflicting primary is already active and supersede is not warranted; initiation would be used to skip S1–S5.

---

### WT-02 — Stage completed → next stage

| # | Condition | Family |
|---|-----------|--------|
| 02.1 | Instance is `in_stage (Sn)` for Sn ∈ {S0…S6} | C-STATE |
| 02.2 | Current stage has produced its MS001-defined stage outputs (or a documented lawful early exit applies) | C-PREREQ / C-OUTPUT |
| 02.3 | Destination is the next ordered stage, or a catalogue-permitted short-circuit destination | C-STATE |
| 02.4 | If destination claims a path toward student-facing recommendation, S1 primary authority selection has already occurred (or is the destination) | C-AUTH / C-PREREQ |
| 02.5 | Required educational outputs for the *destination* stage are available, **or** the move is instead WT-03 (pause) | C-OUTPUT |

**Stage-specific completion marks (constitutional, not algorithmic):**

| Leaving | Completion mark (must be present) |
|---------|-----------------------------------|
| S0 | Event instance with WE-xx class recorded |
| S1 | Primary authority selected, **or** no-op / supersede decision recorded |
| S2 | Input bundle tagged by source authority — without invented truth |
| S3 | Primary Programme VI reasoning artefact present (owned by that corpus) |
| S4 | Conflict clearance, forced handoff, supersede, or refuse recorded |
| S5 | Outcome class: recommend / hand off / refuse / escalate |
| S6 | Explainability artefacts answering orchestration Q1–Q4 (MS001) and transition TQ1–TQ4 (MS002) as applicable |

**Fails when:** outputs are missing and pause was skipped; destination would emit a recommendation without S1–S5 completion; “completion” is asserted by UI convenience alone.

---

### WT-03 — Workflow paused awaiting evidence or educational output

| # | Condition | Family |
|---|-----------|--------|
| 03.1 | Instance is `in_stage (Sn)` and further WT-02 advance would require a missing artefact | C-STATE / C-OUTPUT |
| 03.2 | The awaited artefact is **named** (evidence class, Reflection notes, coach warrant artefact, planner structural response, etc.) | C-OUTPUT |
| 03.3 | Pause does not author, reinterpret, or substitute for the awaited artefact | C-AUTH |
| 03.4 | Pause does not emit an independent educational recommendation to “fill the gap” | C-AUTH |
| 03.5 | Continuity of the open educational concern is preserved for later WT-04 | C-STATE |

**Fails when:** “pause” is used to hide an invented tip; awaited item is unspecified; pause mutates plan or evidence to unblock progress.

---

### WT-04 — Workflow resumed

| # | Condition | Family |
|---|-----------|--------|
| 04.1 | Instance posture is `awaiting_output` or `awaiting_continuation` | C-STATE |
| 04.2a | **Output-available resume:** the named awaited artefact is now lawfully present | C-OUTPUT |
| 04.2b | **Continuation-event resume:** a classified WE-xx continue stimulus for this concern is present | C-EVENT |
| 04.3 | Resume re-enters a stage whose prerequisite outputs are satisfied (C-PREREQ) | C-PREREQ |
| 04.4 | Resume does not change Programme VI meanings produced while waiting; it consumes them as inputs | C-AUTH |
| 04.5 | Resume does not create a conflicting second primary (apply WT-07 if needed) | C-AUTH |

**Fails when:** resume fires without the awaited artefact or continuation event; resume rewrites the artefact; resume skips mandatory stages to “catch up.”

---

### WT-05 — Workflow escalated

| # | Condition | Family |
|---|-----------|--------|
| 05.1 | A structural / envelope failure is recognised under MS001 outcome class **escalate**, or WE-08 is primary | C-STATE / C-EVENT |
| 05.2 | Current Programme VI primary cannot lawfully resolve the concern within plan envelopes | C-AUTH |
| 05.3 | Escalation names Master Planner / Scheduling (or equivalent structural pathway) as receiving primary | C-AUTH |
| 05.4 | Coach artefacts that motivated escalation remain intact as inputs — not rewritten by the transition | C-OUTPUT / C-AUTH |
| 05.5 | Escalation does not itself mutate Canonical Study Plan educational intent | C-AUTH |

**Fails when:** “escalate” is used as a synonym for silent plan edit; receiving authority is unnamed; escalation invents interim educational tips.

---

### WT-06 — Workflow completed (concluded)

| # | Condition | Family |
|---|-----------|--------|
| 06.1 | Instance is at S7 with conclude decision, **or** lawful early close from S1 no-op / refuse path that requires no further stages | C-STATE |
| 06.2 | If a material student-facing educational outcome was emitted, S5 outcome class and S6 explainability are present | C-PREREQ / C-OUTPUT |
| 06.3 | Conclusion does not claim mastery, readiness, or exam certainty from orchestration alone | C-AUTH |
| 06.4 | Learner-owned educational history is retained | C-AUTH |
| 06.5 | No open mandatory await remains without either resolving via WT-04 or explicitly cancelling under supersede / refuse rules | C-STATE / C-OUTPUT |

**Fails when:** conclude hides an unfinished recommendation claim; conclude erases history; conclude is used to drop explainability obligations.

---

### WT-07 — Workflow superseded

| # | Condition | Family |
|---|-----------|--------|
| 07.1 | A higher-priority warrant is classified under MS001 simultaneous-event / conflict rules | C-EVENT / C-AUTH |
| 07.2 | Lower-priority path is `in_stage` or `awaiting_*` | C-STATE |
| 07.3 | Supersede is explicit and explainable (not a silent merge of coaches) | C-AUTH |
| 07.4 | Educational history of the superseded path is preserved | C-AUTH |
| 07.5 | Exactly one primary path remains active for student-facing decisioning | C-AUTH |

**Fails when:** both primaries continue deciding; supersede averages conflicting tips; history is deleted.

---

### WT-08 — Primary authority handoff

| # | Condition | Family |
|---|-----------|--------|
| 08.1 | S4 or S5 records a named **hand off** to a receiving Programme VI authority | C-STATE / C-OUTPUT |
| 08.2 | The living educational question has changed such that the receiver owns it under Programme VI law | C-AUTH |
| 08.3 | Prior primary’s artefact (if any) is retained as input — not modified by the handoff transition | C-OUTPUT / C-AUTH |
| 08.4 | Destination re-enters S1 or S2 under the new primary (prerequisite stages for that primary’s invocation remain mandatory) | C-PREREQ / C-STATE |
| 08.5 | Handoff does not blend two primaries into one speech act | C-AUTH |

**Fails when:** receiving authority is unnamed; handoff rewrites prior coach output; handoff skips re-assembly / re-invocation stages.

---

### WT-09 — Outcome authorised → explain

| # | Condition | Family |
|---|-----------|--------|
| 09.1 | Instance is `in_stage (S5)` with an authorised outcome class recorded | C-STATE / C-OUTPUT |
| 09.2 | Outcome cites an invoked Programme VI authority for any recommend content (MS001 boundary B1) | C-AUTH / C-OUTPUT |
| 09.3 | Destination is S6; explainability obligations are accepted | C-PREREQ |
| 09.4 | Explanation will not invent educational certainty beyond the Programme VI artefact | C-AUTH |

**Fails when:** S5 is skipped; recommend content has no Programme VI provenance; S6 is bypassed for material outcomes.

---

### WT-10 — Park awaiting continuation event

| # | Condition | Family |
|---|-----------|--------|
| 10.1 | Instance is `in_stage (S7)` with continue (not conclude) decision | C-STATE |
| 10.2 | Further progress requires a future WE-xx continuation stimulus (named class expected) | C-EVENT / C-OUTPUT |
| 10.3 | Parking does not emit interim independent recommendations | C-AUTH |
| 10.4 | Parking preserves continuity for later WT-04 | C-STATE |

**Fails when:** park invents filler coaching; expected continuation event is unspecified; park mutates plan or evidence.

---

## 5. Condition Evaluation Posture (Non-Algorithmic)

Constitutional evaluation answers only:

1. **What is the current state/posture?** (C-STATE)
2. **What authority constraints apply?** (C-AUTH)
3. **Are required educational outputs present?** (C-OUTPUT)
4. **Have prerequisite stages completed?** (C-PREREQ)
5. **Is a required event present?** (C-EVENT, when applicable)

Evaluation does **not**:

- score urgency or “engagement”;
- schedule calendar cells;
- rank coaches numerically;
- invent missing evidence to force WT-02;
- use pure clock ticks as educational permission (timer-as-tutor remains forbidden).

Runtime systems may later implement checks that *observe* these facts. They must not redefine the facts as optimisation targets.

---

## 6. Refusal When Conditions Fail

When conditions fail:

| Lawful response | Meaning |
|-----------------|---------|
| **Remain** | Stay in current stage/posture; no WT-xx |
| **Pause (WT-03)** | If the failure is missing output and pause is itself permitted |
| **Refuse (via S5)** | If the educational request cannot be honoured |
| **Escalate (WT-05)** | If envelopes are broken and structural authority is required |
| **Explain** | Record why transition was refused |

Unlawful response: force WT-02 / WT-06 / WT-08 anyway “for product continuity.”

---

## 7. Binding Rule

No Educational Workflow Engine behaviour may execute a WT-xx transition unless global preconditions G1–G6 and the transition-specific conditions in this document hold. Missing conditions ⇒ remain, pause, refuse, or escalate — never invent educational meaning to unblock movement.
