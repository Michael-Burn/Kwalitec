# Completion Criteria

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS003 — Workflow Completion Model  
**Classification:** Constitutional conditions under which workflow orchestration responsibilities are fulfilled  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional conditions indicate that an educational workflow has fulfilled its orchestration purpose**.

Subordinate to:

1. [`WORKFLOW_COMPLETION_MODEL.md`](WORKFLOW_COMPLETION_MODEL.md)
2. [`../workflows/EDUCATIONAL_WORKFLOW_MODEL.md`](../workflows/EDUCATIONAL_WORKFLOW_MODEL.md)
3. [`../workflows/WORKFLOW_STAGES.md`](../workflows/WORKFLOW_STAGES.md)
4. [`../workflows/WORKFLOW_OBJECTIVES.md`](../workflows/WORKFLOW_OBJECTIVES.md)
5. [`../workflows/WORKFLOW_BOUNDARIES.md`](../workflows/WORKFLOW_BOUNDARIES.md)
6. [`../workflow_transitions/WORKFLOW_TRANSITION_FRAMEWORK.md`](../workflow_transitions/WORKFLOW_TRANSITION_FRAMEWORK.md)
7. [`../workflow_transitions/TRANSITION_CATALOGUE.md`](../workflow_transitions/TRANSITION_CATALOGUE.md)
8. [`../workflow_transitions/TRANSITION_CONDITIONS.md`](../workflow_transitions/TRANSITION_CONDITIONS.md)
9. Programme VI constitutional corpora (as participants — never as redefined educational success gates)

> **Completion criteria are orchestration conditions — not educational success dimensions, mastery thresholds, or timer checks.  
> Fulfilment is judged from constitutional stage and transition trail, not elapsed time.**

---

## 1. Purpose

Without explicit completion criteria, workflows either never close (permanent open orchestration) or close falsely (a timer fired, a UI step finished, or a coach recommendation appeared without lawful stages).

With explicit criteria, an expert tutor can affirm that coordination duties are done — while refusing mastery theatre and unfinished orchestration responsibilities.

---

## 2. Criteria Principles

1. **Orchestration first.** Criteria describe fulfilled coordination duties, not educational outcomes.
2. **Evidence-bound.** Each criterion requires supporting trail under `COMPLETION_EVIDENCE.md`.
3. **Stage-faithful.** Criteria respect MS001 S0–S7 and mandatory authority checks for the claimed outcome.
4. **Transition-faithful.** Lawful MS002 transitions (including handoffs and explain) are accounted for.
5. **Authority-preserving.** Meeting criteria never redefines Programme VI meaning.
6. **Non-certifying.** Meeting criteria does not certify learner mastery or coach educational success.
7. **Non-temporal.** No criterion is satisfied merely because time passed or a job ran long/short.
8. **Speakable.** Criteria must be explainable in plain educational language (`COMPLETION_EXPLAINABILITY.md`).

---

## 3. Criterion Catalogue

IDs (`WCC-XX`) exist for audit and cross-reference. They must not appear as student-facing jargon.

### WCC-01 — Required constitutional stages completed

**Definition.** All MS001 stages required for this workflow’s outcome class have produced their lawful stage outputs — including mandatory authority checks when a student-facing educational recommendation is claimed.

**Tutor rationale.** Orchestration that skips S1–S5 while claiming a recommendation is unfinished coordination, even if product copy looks complete. Thin no-op paths may lawfully short-circuit under MS002; recommendation paths may not.

**Success looks like:**

- For material recommend / hand off / refuse / escalate outcomes: S0→S5 completed with S6 explainability present before close.
- For lawful S1 no-op / refuse early close: the short-circuit is documented under MS002 conditions — not silent skip.
- Stage outputs match MS001 stage definitions (event recorded, primary selected, inputs assembled, Programme VI invoked where required, conflict cleared, outcome authorised, explanation produced).

**Must not:**

- Treat UI navigation completion as stage completion.
- Skip S6 for material student-facing outcomes.
- Claim WCC-01 because “enough time was spent in the pipeline.”

**Evidence posture:** Requires WCE-01; typically supported by WCE-02.

---

### WCC-02 — Required coach consultations concluded

**Definition.** Every Programme VI consultation that this workflow instance was constitutionally required to obtain — as primary authority at S3, or as a named required sibling input at S4 — has either produced its lawful artefact **or** been honestly refused / redirected under Programme VI and MS001/MS002 rules.

**Tutor rationale.** A workflow that opened to consult Recovery Coach (or Daily Coach, Learning Coach, etc.) is not orchestration-complete while that consultation remains outstanding. “Concluded” means the consultation duty is finished as coordination — not that the coach’s educational answer was “successful.”

**Success looks like:**

- Named primary authority invocation completed (artefact present) or lawful refusal / escalation recorded.
- Required sibling inputs for conflict check are present or explicitly waived under documented thin-context rules.
- No open “awaiting_output” pause remains for a consultation this instance still claims to need before close.

**Must not:**

- Infer consultation complete from elapsed wait time.
- Treat consultation conclusion as certification of educational success or mastery.
- Fabricate a coach artefact to satisfy the criterion.

**Evidence posture:** Requires WCE-03; may be supported by WCE-02 / WCE-04.

---

### WCC-03 — Lawful handoffs completed

**Definition.** Every authority handoff (MS002 WT-08) or escalate path (WT-05) that this instance authorised has been completed as orchestration — the receiving primary is named, the transfer is recorded, and no dangling half-handoff remains for this instance’s responsibilities.

**Tutor rationale.** “Hand off to Learning Coach” that never re-enters S1/S2 under the new primary leaves orchestration unfinished. Escalation that never reaches Master Planner pathways similarly leaves duties open. Completing the handoff is coordination honesty — not a claim that the receiving coach finished its educational job.

**Success looks like:**

- S5 hand-off / escalate outcome has a corresponding completed transfer record, **or** this instance’s duty ends at emitting the handoff and a successor instance owns continuation (then WCT-02 applies).
- No ambiguous dual-primary state remains.
- Authority names before and after the handoff are explicit.

**Must not:**

- Merge two primaries to avoid finishing a handoff.
- Claim handoff complete while both old and new primaries still decide.
- Treat handoff completion as educational success of either coach.

**Evidence posture:** Requires WCE-04 when handoff/escalate was part of the path; otherwise not applicable.

**Applicability rule:**

> **WCC-03 is binding when this instance authorised hand off or escalate.  
> It is not required for pure recommend / refuse closes with no transfer.**

---

### WCC-04 — Authorised outcome present and explainable

**Definition.** An authorised S5 outcome class exists (recommend / hand off / refuse / escalate / lawful no-op), and material student-facing outcomes have S6 explainability artefacts satisfying MS001 `WORKFLOW_EXPLAINABILITY.md`.

**Tutor rationale.** Orchestration that never authorises an outcome has not finished its coordination job. Explanation is part of fulfilment for material outcomes — not optional polish.

**Success looks like:**

- Exactly one outcome class is recorded for the instance’s close path.
- Explainability answers why the workflow started, who participated, how authority was preserved, and why the outcome emerged — for material paths.
- Outcome content remains Programme VI–owned; the workflow does not invent a fifth tip.

**Must not:**

- Invent an outcome to force close.
- Use explanation to justify unlawful skips.
- Treat outcome presence as proof of educational success.

**Evidence posture:** Requires WCE-05; supported by WCE-01 / WCE-02.

---

### WCC-05 — No outstanding orchestration responsibilities

**Definition.** For this workflow instance, no required coordination duty remains: no unfinished required stage, no open required consultation, no incomplete handoff owned by this instance, no unresolved conflict check that blocks authorisation, and no pending explainability duty for a material outcome.

**Tutor rationale.** Completion is the absence of remaining orchestration work for this concern — not the presence of a “done” badge. Parking for a future event (WT-10) means the instance is **not** complete; it is awaiting continuation.

**Success looks like:**

- Checklist of this instance’s duties is empty.
- Posture is ready for `concluded` (WT-06) rather than `awaiting_output` or `awaiting_continuation`.
- Any remaining educational work belongs to Programme VI or to a future / successor workflow — not to this instance’s open orchestration queue.

**Must not:**

- Declare no outstanding duties while paused awaiting evidence or coach output.
- Declare completion while parked for a continuation event (use await / successor patterns instead).
- Hide outstanding duties by renaming them as “product backlog.”

**Evidence posture:** Synthesis criterion — affirmed only when applicable WCC-01…WCC-04 hold and WCE-06 blockers are absent.

---

### WCC-06 — Authority preservation affirmed

**Definition.** The completion judgement can honestly affirm that Programme VI educational meaning, Canonical Study Plan intent, and Educational Evidence reading were **not** altered by the act of completing the workflow.

**Tutor rationale.** A close that quietly rewrote a coach tip, plan envelope, or evidence interpretation has failed constitutional integrity even if stages look finished.

**Success looks like:**

- Boundary checks from MS001 / MS002 remain satisfied at close.
- Completion artefacts cite authority preservation rather than new educational claims.
- Any educational meaning change that occurred during the workflow is attributable to Programme VI authorities — not to the completion judgement.

**Must not:**

- Use completion as a licence to “tidy” recommendations.
- Mutate the Canonical Study Plan as a close side-effect.
- Reinterpret Educational Evidence to make the close look cleaner.

**Evidence posture:** Requires WCE-07; synthesis with WCE-01…WCE-05.

---

## 4. How Criteria Combine for Successful Completion

### 4.1 Core set (always required for WCT-01 archive / honest conclude)

Successful orchestration completion requires honest affirmation of:

1. **WCC-01** Required constitutional stages completed  
2. **WCC-02** Required coach consultations concluded  
3. **WCC-04** Authorised outcome present and explainable  
4. **WCC-05** No outstanding orchestration responsibilities  
5. **WCC-06** Authority preservation affirmed  

### 4.2 Conditional criteria

| Criterion | When required |
|-----------|---------------|
| **WCC-03** Lawful handoffs completed | When S5 authorised hand off or escalate, or WT-08 / WT-05 was used on this path |

### 4.3 Binding combination rule

> **All applicable criteria must be honestly affirmable from constitutional evidence.  
> Missing an applicable criterion means the workflow is not yet orchestration-complete — continue stages (MS002), await outputs, open a successor, or refuse false close.**

### 4.4 Relationship to WT-06

| Situation | Lawful posture |
|-----------|----------------|
| Applicable WCC set affirmed | WT-06 conclude may proceed; select WCT post-completion move |
| WCC fails; duties remain active | Remain in stage / resume path — do not WT-06 |
| Concern needs future WE-xx | WT-10 park / WCT-03 await — **not** completion |
| Concern continues under new orchestration instance | WCT-02 successor — prior instance may conclude only its own duties |

---

## 5. Explicit Non-Criteria (Forbidden Completion Grounds)

The following **never** complete a workflow by themselves:

| Non-criterion | Why forbidden |
|---------------|---------------|
| Elapsed wall-clock time / SLA timers | Time is not orchestration evidence |
| Execution duration or job runtime | Duration ≠ fulfilled stages / consultations |
| UI step / funnel completion | Product theatre, not constitutional stages |
| Session / mission / sitting completion ticks | Educational event may *initiate* a workflow; it does not complete orchestration alone |
| Coach recommendation exists | Artefact may support WCC-02/WCC-04 but does not certify educational success or skip stages |
| Programme VI educational completion (recovery/revision/etc.) | Educational completion ≠ orchestration fulfilment; may be an *input event*, not this criterion |
| Attendance / login / streak metrics | Activity without orchestration trail |
| Analytics “workflow_completed” events without WCE trail | Telemetry is not constitutional evidence |
| Comparison to other learners’ pace | Shame theatre, not orchestration criterion |

---

## 6. Relationship to Programme VI Educational Completion

| Programme VI concept | Workflow completion reading |
|----------------------|----------------------------|
| Recovery / Revision / etc. educational completion | May appear as a WE-xx event or Programme VI artefact consumed at S3 — **not** as proof that Programme VII orchestration is complete |
| Coach “success” speech | Owned by Programme VI explainability; workflow completion must not co-opt it |
| Mastery / readiness | Never implied by WCC criteria |

Hard rule:

> **Meeting workflow completion criteria means orchestration responsibilities are fulfilled.  
> It does not mean Learning Objectives were attained, recovery succeeded educationally, revision strengthened knowledge, or mastery was earned.**

---

## 7. Anti-Patterns (Forbidden)

- Declaring completion because “the job finished in under 200ms”
- Declaring completion because a session was marked complete
- Declaring completion while `awaiting_output` or `awaiting_continuation`
- Skipping explainability for material recommend outcomes
- Using criteria as numeric scores or dashboards presented as educational truth
- Narrating criteria IDs to students
- Claiming coach educational success from WCC affirmation

---

## 8. Cross References

| Document | Role |
|----------|------|
| [`COMPLETION_EVIDENCE.md`](COMPLETION_EVIDENCE.md) | What trail may support each criterion |
| [`COMPLETION_TRANSITIONS.md`](COMPLETION_TRANSITIONS.md) | What follows when criteria are / are not met |
| [`COMPLETION_EXPLAINABILITY.md`](COMPLETION_EXPLAINABILITY.md) | How criteria are spoken without jargon |
| [`../workflows/WORKFLOW_STAGES.md`](../workflows/WORKFLOW_STAGES.md) | S0–S7 duties WCC-01 references |
| [`../workflow_transitions/TRANSITION_CATALOGUE.md`](../workflow_transitions/TRANSITION_CATALOGUE.md) | WT-06 / WT-08 / WT-10 relationship |
