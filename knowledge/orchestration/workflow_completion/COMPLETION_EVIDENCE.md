# Completion Evidence

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS003 — Workflow Completion Model  
**Classification:** Constitutional evidence supporting workflow completion judgements  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what constitutional evidence may support a workflow completion judgement**.

Subordinate to:

1. [`WORKFLOW_COMPLETION_MODEL.md`](WORKFLOW_COMPLETION_MODEL.md)
2. [`COMPLETION_CRITERIA.md`](COMPLETION_CRITERIA.md)
3. [`../workflows/EDUCATIONAL_WORKFLOW_MODEL.md`](../workflows/EDUCATIONAL_WORKFLOW_MODEL.md)
4. [`../workflows/WORKFLOW_STAGES.md`](../workflows/WORKFLOW_STAGES.md)
5. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md)
6. [`../workflow_transitions/TRANSITION_CATALOGUE.md`](../workflow_transitions/TRANSITION_CATALOGUE.md)
7. [`../workflow_transitions/TRANSITION_CONDITIONS.md`](../workflow_transitions/TRANSITION_CONDITIONS.md)
8. [`../workflow_transitions/TRANSITION_BOUNDARIES.md`](../workflow_transitions/TRANSITION_BOUNDARIES.md)
9. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002) — educational evidence law remains binding for Programme VI claims; this document does **not** invent a second Educational Evidence Model
10. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001)

> **Completion evidence demonstrates stage completion, lawful transitions, preserved authority, and successful orchestration.  
> Do not infer completion from elapsed time or execution duration.  
> Orchestration evidence is not Educational Evidence of learning.**

---

## 1. Purpose

Without evidence law, “workflow complete” becomes either optimistic theatre (a timer, a UI tick) or opaque optimiser speech.

With evidence law, completion claims remain constitutionally honest: orchestration fulfilment may be affirmed when the trail supports it; educational success speech stays forbidden; thin or incomplete trails yield “not yet” rather than false close.

---

## 2. What Completion Evidence Is (and Is Not)

### 2.1 Orchestration evidence

**Workflow completion evidence** is the constitutional trail that coordination duties were performed lawfully: stages produced outputs, transitions were permitted, consultations concluded, handoffs completed, outcomes authorised, authority preserved.

### 2.2 Not Educational Evidence of learning

EIP-002 Educational Evidence remains the law for claims about learning, continuity, mastery-adjacent safety, and coach educational judgements.

This corpus:

- **may cite** that a Programme VI artefact *exists* as an orchestration input/output (consultation concluded);
- **must not** reinterpret that artefact’s educational meaning;
- **must not** treat Educational Evidence accumulation as proof that orchestration is complete (or vice versa);
- **must not** mint understanding or readiness from orchestration close.

Architectural requirement restated:

> **Do not infer workflow completion from elapsed time or execution duration.**

---

## 3. What Completion Evidence Is For

Completion evidence supports claims about **fulfilled orchestration responsibilities** (WCC-XX).

It does **not** by itself authorise:

- Estimated Mastery uplift;
- exam-readiness certainty;
- educational recovery / revision / learning completion judgements;
- rewriting of Canonical Study Plan envelopes;
- silent mutation of coach recommendations.

---

## 4. Evidence Class Catalogue

IDs (`WCE-XX`) exist for audit and cross-reference. They must not appear as student-facing jargon.

### WCE-01 — Stage completion trail

**Definition.** Recorded MS001 stage outputs showing required stages for this path produced their lawful artefacts (event classification, warrant/primary, input assembly, invocation, conflict clearance, outcome, explanation as applicable).

**May support:** WCC-01, WCC-04, WCC-05.

**May include:**

- Stage markers S0…S7 (or documented lawful short-circuit) with outputs matching stage definitions;
- Explicit record of which stages were required for the outcome class;
- No silent jump from recognition to recommendation without intermediate authority checks.

**Must not treat as sufficient alone:**

- A single “pipeline finished” flag without stage outputs;
- UI screen progression;
- Time spent in each stage.

---

### WCE-02 — Lawful transition trail

**Definition.** Recorded MS002 transitions (WT-xx) showing stage movement was condition-gated — including WT-02 advances, WT-09 explain move, and any WT-03/WT-04 pause/resume honesty on the path to close.

**May support:** WCC-01, WCC-05, WCC-06.

**May include:**

- Ordered WT-02 advances with permitting conditions cited;
- WT-09 after material S5 outcomes;
- Documented WT-03 pauses and WT-04 resumes when outputs were awaited (proving invent-nothing honesty);
- Absence of unlawful silent skips.

**Must not:**

- Invent transitions after the fact to decorate a false close;
- Treat transition count or speed as quality of education;
- Use WT-06 itself as the only evidence that criteria were met (circular).

---

### WCE-03 — Consultation conclusion trail

**Definition.** Records that required Programme VI consultations for this instance concluded as orchestration duties — primary artefact present, or lawful refuse / escalate / no-op recorded.

**May support:** WCC-02, WCC-04.

**May include:**

- Reference to the Programme VI artefact identity (not a re-authored copy of its educational meaning);
- Named primary authority and consultation start/end as coordination events;
- Explicit waiver only where MS001/MS002 thin-context rules permit.

**Must not:**

- Fabricate coach content;
- Infer conclusion from wait duration;
- Treat consultation conclusion as educational success or mastery.

---

### WCE-04 — Handoff / escalate completion trail

**Definition.** Records that authorised WT-08 handoffs or WT-05 escalations completed their orchestration transfer — receiving authority named, dual-primary avoided, successor ownership clear when duties move.

**May support:** WCC-03, WCC-05, WCC-06.

**May include:**

- From-authority / to-authority names;
- S5 hand-off or escalate outcome linked to re-entry or successor instance ID (constitutional identity — not a runtime schema mandate);
- Confirmation that the prior primary no longer decides on this concern.

**Must not:**

- Leave ambiguous dual-primary states;
- Claim escalate complete while structural pathway never opened;
- Narrate handoff as educational failure or success of either coach.

**Applicability:** Required when handoff/escalate occurred; otherwise absent without blocking other criteria.

---

### WCE-05 — Authorised outcome and explainability trail

**Definition.** Recorded S5 outcome class and, for material student-facing paths, S6 explainability artefacts answering MS001 orchestration explainability questions.

**May support:** WCC-04, WCC-05.

**May include:**

- Outcome class: recommend / hand off / refuse / escalate / lawful no-op;
- Explainability fields: initiating event, participants, authority preservation, outcome provenance;
- Explicit non-claim of mastery from orchestration.

**Must not:**

- Use explanation to invent certainty Programme VI did not claim;
- Omit S6 for material recommend paths;
- Treat outcome presence as educational certification.

---

### WCE-06 — Negative / incompleteness evidence

**Definition.** Observations that **block** completion even if some positive signals exist.

**Must block or delay WCT-01 when present:**

- Required stage outputs missing for the claimed outcome class;
- Open `awaiting_output` for a consultation this instance still needs;
- Open `awaiting_continuation` (parked — not complete);
- Incomplete handoff / escalate with dual-primary or unnamed receiver;
- Missing S6 for material student-facing outcomes;
- Boundary breach: plan mutation, evidence reinterpretation, or independent workflow tip at close;
- Only temporal or duration signals available.

Correct “not yet” / await / successor beats false completion.

---

### WCE-07 — Authority preservation trail

**Definition.** Explicit confirmation that completion did not alter Programme VI educational meaning, Canonical Study Plan intent, or Educational Evidence reading.

**May support:** WCC-06; contributes honesty to all other WCC affirmations.

**May include:**

- Boundary check results from MS001 `WORKFLOW_BOUNDARIES.md` / MS002 `TRANSITION_BOUNDARIES.md` at close;
- Statement that coach artefacts are consumed by reference, not rewritten;
- Statement that plan / evidence writers remain as EIP-001 permits — workflow completion is not a writer.

**Must not:**

- Rubber-stamp preservation without checks when material outcomes exist;
- Use “authority preserved” speech while silently editing recommendations.

---

## 5. Forbidden Inference Patterns

The following inferences are **constitutionally unlawful** for workflow completion:

| Observed | Unlawful inference |
|----------|-------------------|
| N milliseconds / minutes elapsed | Workflow orchestration complete |
| Job / saga / queue marked done | Constitutional stages and consultations complete |
| Session or mission marked complete | Workflow orchestration complete |
| Student logged in or attended | Orchestration complete |
| Coach recommendation string present | All WCC criteria met / educational success certified |
| Programme VI educational completion declared | Programme VII orchestration automatically complete |
| Analytics `workflow_completed` event | Constitutional fulfilment without WCE trail |
| UI funnel last step reached | S0–S7 duties fulfilled |
| No errors in logs | Authority preserved and handoffs complete |

Hard rule:

> **Do not infer completion from elapsed time or execution duration.**

---

## 6. Accumulation and Sufficiency

### 6.1 Accumulation

Evidence for completion **accumulates along the stage path**. Interpreters revise the completion judgement as stages and transitions complete. Early S0 recognition never suffices for recommend-path close.

### 6.2 Sufficiency (qualitative)

A completion judgement is evidence-sufficient when:

1. Applicable WCC criteria each have supporting WCE classes (not merely hoped);
2. WCE-06 blockers are absent or honestly redirected to continue / await / successor;
3. Claims remain orchestration-scoped — no educational success speech from WCE alone;
4. Explainability can name the trail in plain language without inventing certainty.

This Model does **not** define numerical sample sizes, scores, or latency SLAs as constitutional completion law. Sufficiency is orchestration judgement under stage/transition discipline.

### 6.3 Thin trail rule

When the trail is thin (e.g. early no-op):

- Affirm only the short-circuit path MS002 permits;
- Prefer continue / await over false recommend-path completion;
- Never fill thin orchestration history with mastery or coach-success speech.

---

## 7. Relationship to Educational Evidence (EIP-002)

| Situation | Evidence reading | Completion implication |
|-----------|------------------|------------------------|
| Programme VI artefact exists | WCE-03 may cite existence | Supports consultation concluded — not educational success |
| Educational Evidence accumulates during the workflow | Owned by EIP-002 / permitted writers | Does not by itself complete orchestration |
| Thin educational history | Programme VI may understate | Orchestration may still complete a refuse / escalate / await path honestly |
| Educational completion model fires (e.g. recovery complete) | May be WE-xx / S3 input for a *new* or continuing educational concern | Does not auto-complete this or any workflow without WCC/WCE |

Hard rule:

> **Orchestration completion evidence must not bypass or redefine Educational Evidence.  
> Closing a workflow is not proof that learning progressed.**

---

## 8. Traceability Obligation

Every material completion judgement must be traceable through:

| Trace link | Role |
|------------|------|
| Workflow instance / educational concern | What orchestration is being closed |
| Applicable WCC criteria | Which orchestration conditions were evaluated |
| Supporting WCE classes | What constitutional trail was cited |
| Explicit non-reliance statement (when relevant) | What was *not* used (time alone, duration alone, UI ticks alone) |
| Resulting WCT transition | What orchestration move follows |
| Authority preservation | Explicit non-mutation of Programme VI / plan / evidence meaning |
| Non-certification | Explicit non-claim of educational success / mastery / coach success |

A completion declaration with only elapsed time, execution duration, or UI ticks in the trail is invalid.

---

## 9. Anti-Patterns (Forbidden)

- Completion dashboards powered by latency or queue depth as constitutional truth
- Silent Twin mastery writes triggered by workflow-complete events
- “Evidence” that is only a desired product outcome renamed as stage trail
- Selective citation of S5 recommend while ignoring missing S6 or open handoffs
- Using completion evidence vocabulary to invent a second Educational Evidence Model

---

## 10. Cross References

| Document | Role |
|----------|------|
| [`COMPLETION_CRITERIA.md`](COMPLETION_CRITERIA.md) | Conditions evidence must support |
| [`COMPLETION_TRANSITIONS.md`](COMPLETION_TRANSITIONS.md) | Moves when evidence is sufficient or not |
| [`COMPLETION_EXPLAINABILITY.md`](COMPLETION_EXPLAINABILITY.md) | How evidence is spoken |
| [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) | Governing EIP-002 educational evidence law |
| [`../workflow_transitions/TRANSITION_CONDITIONS.md`](../workflow_transitions/TRANSITION_CONDITIONS.md) | Conditions for WT-06 and related moves |
