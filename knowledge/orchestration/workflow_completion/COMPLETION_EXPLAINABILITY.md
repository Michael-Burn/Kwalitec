# Completion Explainability

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS003 — Workflow Completion Model  
**Classification:** Explainability contract for workflow completion judgements  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **workflow completion** to students and developers.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`WORKFLOW_COMPLETION_MODEL.md`](WORKFLOW_COMPLETION_MODEL.md)
4. [`COMPLETION_CRITERIA.md`](COMPLETION_CRITERIA.md)
5. [`COMPLETION_EVIDENCE.md`](COMPLETION_EVIDENCE.md)
6. [`COMPLETION_TRANSITIONS.md`](COMPLETION_TRANSITIONS.md)
7. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md)
8. [`../workflow_transitions/TRANSITION_EXPLAINABILITY.md`](../workflow_transitions/TRANSITION_EXPLAINABILITY.md)
9. Programme VI explainability corpora for any invoked primary authority

> **Readers should understand:  
> why the workflow is complete,  
> what constitutional evidence supports completion,  
> which components participated,  
> and what orchestration responsibilities remain, if any.  
> Explainability never invents educational certainty.  
> Completion never implies educational success, mastery, or coach outcome success.**

---

## 1. Purpose

Students should never have to guess whether Kwalitec is still coordinating something — or feel that “all done” meant they had mastered the topic.

Developers should never have to reverse-engineer whether a close skipped stages, left handoffs dangling, or quietly certified educational success.

Completion explainability exists so every material completion judgement answers — in the right language for the audience — **why orchestration is complete (or not yet)**, **what constitutional evidence supports that**, **which components participated**, and **what orchestration responsibilities remain, if any**.

Without completion explainability:

- close feels arbitrary or like a product bug;
- students confuse workflow close with learning success;
- developers cannot prove authority preservation at archive;
- await / successor moves feel like abandonment or double-coaching;
- audits cannot separate orchestration fulfilment from educational claims.

With completion explainability:

- the student trusts that coordination finished without mastery theatre;
- developers can verify WCC/WCE discipline;
- claim types stay honest;
- remaining duties (if any) stay speakable.

---

## 2. Relationship to Upstream Explainability

| Layer | Document | Student / developer question |
|-------|----------|------------------------------|
| **Workflow orchestration** | [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) | Why did this workflow start? Who participated? Why this outcome? |
| **Stage transition** | [`../workflow_transitions/TRANSITION_EXPLAINABILITY.md`](../workflow_transitions/TRANSITION_EXPLAINABILITY.md) | Why did the flow *move* now? |
| **Workflow completion** | **This document** | Why is orchestration complete (or not)? What evidence? Who participated? What remains? |
| **Programme VI educational content** | Programme VI explainability corpora | What is the educational recommendation / judgement? |

Completion speech must remain consistent with MS001 / MS002 speech. It closes (or refuses to close) the **coordination** arc; it does not invent a second educational story or a mastery ceremony.

EIP-003’s educational-content questions remain owned by Programme VI. MS001 covers the orchestration path; MS002 covers movement; this document’s CQ1–CQ4 cover the **completion judgement**.

---

## 3. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | That today’s coordination is finished (or still waiting); what to do next from the Programme VI outcome; honest non-mastery | WCC/WCE/WCT/WT/WE/S IDs, queue names, Twin facets, optimiser jargon, “you’ve mastered this because the workflow finished” |
| **Developer / auditor** | Precise constitutional references | WCC set evaluated, WCE classes cited, WCT selected, participants, authority preservation, non-certification flags | Student-facing motivational fluff as a substitute for audit fields |

Student copy narrates coordination close in educational language. Developer traces cite completion IDs and evidence outcomes.

---

## 4. Traceability Obligation (Architectural)

Every material completion judgement must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Why complete / not yet** | “We’ve finished coordinating today’s guidance…” / “We’re still waiting for…” | WCC affirmation or failure set |
| **Evidence basis** | “Because the right checks and coach input finished…” | WCE-01…WCE-07 citations |
| **Explicit non-grounds (when useful)** | “This isn’t just because time passed…” | Non-reliance on duration / timers |
| **Components participated** | “Your study plan and daily guidance…” (plain) | Primary + sibling authorities named |
| **What remains** | “Nothing else to coordinate right now…” / “Next we’ll pick this up when…” | Outstanding duties or WCT-03/WCT-05 |
| **What changes next** | Next Programme VI-owned step, or honest wait | WCT-01…WCT-05 |
| **Authority preservation** | Implicit: no sudden plan rewrite speech | WCE-07 / boundary pass |
| **Non-certification** | “This doesn’t mean everything is mastered.” | Explicit non-claim of educational success / mastery / coach success |

Internal IDs (WCC-XX, WCE-XX, WCT-XX) may exist for algorithms and audits. They must not appear as student-facing jargon.

Architectural requirement restated:

> **Workflow completion confirms only that orchestration responsibilities have been fulfilled.  
> It must never be interpreted as educational success, learner mastery, or coach completion.**

A completion message with no evidence link — or one that cites only elapsed time, duration, or UI ticks — is invalid.

---

## 5. Completion Questions (CQ1–CQ4)

Every material completion judgement must be able to answer:

### CQ1 — Why is the workflow complete (or not yet)?

| Audience | Expectation |
|----------|-------------|
| Student | Plain reason: coordination finished / still waiting for a sitting / still assembling what we need |
| Developer | Applicable WCC results; link to stage path and outcome class |

### CQ2 — What constitutional evidence supports completion?

| Audience | Expectation |
|----------|-------------|
| Student | Brief, non-jargon: checks finished, coach input received, no open coordination left |
| Developer | WCE classes; explicit non-reliance on time/duration; WCE-06 blockers if not complete |

### CQ3 — Which components participated?

| Audience | Expectation |
|----------|-------------|
| Student | Educational roles in plain language (plan, today’s guidance, recovery, etc.) |
| Developer | Named Programme VI primaries/siblings; MS001 stage participation set |

### CQ4 — What orchestration responsibilities remain, if any?

| Audience | Expectation |
|----------|-------------|
| Student | Clear next coordination posture: nothing pending / wait for next study moment / continue under another focus |
| Developer | Empty duty set → WCT-01; else WCT-02 / WCT-03 / WCT-05 with named remaining duties |

---

## 6. Speech Patterns by Transition

### 6.1 WCT-01 Archive (complete)

**Student (illustrative posture, not mandated copy):**  
“We’ve finished putting today’s guidance together. Your plan hasn’t changed — and finishing this coordination doesn’t mean the topic is mastered.”

**Developer must record:** WCC core set, WCE trail, WT-06, WCE-07, non-certification.

### 6.2 WCT-02 Successor

**Student:**  
“We’re shifting focus to the next educational question — still under your authorised plan.”

**Developer must record:** prior instance close status, successor primary, no dual-primary, no new meaning from Programme VII.

### 6.3 WCT-03 Await

**Student:**  
“Nothing more to coordinate until the next study moment / until this sitting finishes.”

**Developer must record:** expected WE-xx or park posture; duties owned vs not complete.

### 6.4 WCT-04 Audit

**Student:** usually silent (audit is developer/continuity facing); student speech remains CQ1–CQ4.  
**Developer:** full trace package per §4.

### 6.5 WCT-05 Continue (not complete)

**Student:**  
“We’re not finished coordinating yet — still waiting on / still checking…”

**Developer must record:** failed WCC / WCE-06 blockers; next MS002 move.

---

## 7. Forbidden Explanation Patterns

| Forbidden speech | Why |
|------------------|-----|
| “Workflow complete — you’ve mastered this” | Scope violation |
| “Complete because the job finished quickly” | Temporal theatre |
| “Complete because you finished the session” | Event ≠ orchestration fulfilment alone |
| Opaque “system processed successfully” as the only reason | Fails CQ1–CQ2 |
| Blame / shame for unfinished orchestration | Continuity and dignity violation |
| Exposing WCC/WCE/WCT IDs to students | Audience violation |
| Claiming coach “succeeded” because orchestration archived | Educational meaning theft |
| Using completion speech to announce a plan rewrite | Authority violation |

---

## 8. Consistency with Programme VI Completion Speech

When a Programme VI educational completion model (e.g. Recovery Completion, Revision Completion) also speaks:

| Rule | Meaning |
|------|---------|
| **Separate claims** | Educational completion and orchestration completion may coincide in time; speech must not collapse them |
| **Programme VI owns educational success language** | Workflow completion may say coordination finished; it must not borrow “you’ve recovered” / “revision succeeded” as its own proof |
| **Orchestration may narrate sequencing** | “We’ve finished coordinating that recovery guidance for now” — without certifying recovery educational success unless Programme VI does |

---

## 9. Anti-Patterns (Forbidden)

- Mastery celebrations triggered by WCT-01
- Student-facing latency or queue metrics as completion reasons
- Silent archive without CQ1–CQ4 answerability
- Dual speech streams that contradict (UI says done; audit shows awaiting_output)
- Using explainability to justify unlawful skips

---

## 10. Cross References

| Document | Role |
|----------|------|
| [`WORKFLOW_COMPLETION_MODEL.md`](WORKFLOW_COMPLETION_MODEL.md) | Constitutional overview |
| [`COMPLETION_CRITERIA.md`](COMPLETION_CRITERIA.md) | What CQ1 evaluates |
| [`COMPLETION_EVIDENCE.md`](COMPLETION_EVIDENCE.md) | What CQ2 cites |
| [`COMPLETION_TRANSITIONS.md`](COMPLETION_TRANSITIONS.md) | What CQ4 selects |
| [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) | Upstream orchestration Q1–Q4 |
| [`../workflow_transitions/TRANSITION_EXPLAINABILITY.md`](../workflow_transitions/TRANSITION_EXPLAINABILITY.md) | Upstream transition TQ1–TQ4 |
| [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) | EIP-003 governing standard |
