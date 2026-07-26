# Transition Explainability

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS002 — Workflow Transition Framework  
**Classification:** Explainability contract for educational workflow transitions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **workflow transitions** to students and developers.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`WORKFLOW_TRANSITION_FRAMEWORK.md`](WORKFLOW_TRANSITION_FRAMEWORK.md)
4. [`TRANSITION_CATALOGUE.md`](TRANSITION_CATALOGUE.md)
5. [`TRANSITION_CONDITIONS.md`](TRANSITION_CONDITIONS.md)
6. [`TRANSITION_BOUNDARIES.md`](TRANSITION_BOUNDARIES.md)
7. [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md)
8. Programme VI explainability corpora for any invoked primary authority

> **Explainability improves understanding of stage movement already authorised.  
> It never invents educational certainty or independent recommendations.**

---

## 1. Purpose

Students should never have to guess why Kwalitec paused for evidence, shifted from ordinary study to recovery, resumed after a sitting, or sent a structural problem to plan adjustment.

Developers should never have to reverse-engineer which condition permitted a stage jump — or whether a transition quietly edited coach authority.

Transition explainability exists so every material stage movement answers — in the right language for the audience — **why a transition occurred**, **what constitutional condition permitted it**, **which components participated**, and **why authority remained unchanged**.

Without transition explainability:

- pauses feel like bugs;
- resumes feel arbitrary;
- escalations feel like product breakage;
- handoffs feel like coaches arguing;
- audits cannot prove authority preservation across stage moves.

With transition explainability:

- the student trusts tutor posture across stage changes;
- developers can verify Programme VII moved flow without inventing meaning;
- claim types stay honest;
- refusals to advance remain dignified and clear.

---

## 2. Relationship to MS001 Workflow Explainability

| Layer | Document | Student question |
|-------|----------|------------------|
| **Workflow orchestration** | [`../workflows/WORKFLOW_EXPLAINABILITY.md`](../workflows/WORKFLOW_EXPLAINABILITY.md) | Why did this workflow start? Who participated? How was authority preserved? Why this recommendation / handoff / refusal? |
| **Stage transition** | **This document** | Why did the flow *move* now? What condition allowed the move? Who was involved in the move? Why did coach/plan/evidence authority stay the same? |

Transition speech must remain consistent with MS001 orchestration speech. It adds **movement clarity**; it does not invent a second educational story.

EIP-003’s educational-content questions remain owned by Programme VI explainability. MS001 Q1–Q4 cover the orchestration path. This document’s TQ1–TQ4 cover the **transition moment**.

---

## 3. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Why guidance waited, resumed, shifted, or needs plan adjustment; honest limits | WT/WE/S IDs, queue names, Twin facets, optimiser jargon |
| **Developer / auditor** | Precise constitutional references | WT-xx, from/to stage or posture, condition families satisfied, participants, T1–T8 results | Student-facing motivational fluff as a substitute for audit fields |

Student copy narrates educational reasons for movement. Developer traces cite transition IDs and condition outcomes.

---

## 4. Traceability Obligation (Architectural)

Every material workflow transition must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Transition kind** | “We’re waiting for…” / “We’re continuing…” / “We need to adjust your plan…” | WT-xx |
| **From → to** | Plain description of what changed in the tutoring posture | Prior stage/posture → new stage/posture |
| **Permitting condition** | “Because … is now available / not yet available / no longer the main issue…” | C-STATE / C-AUTH / C-OUTPUT / C-PREREQ (/ C-EVENT) keys |
| **Participating components** | “Your Study Plan and today’s coaching…” / “Recovery leading; daily priorities wait…” | Primary + sibling inputs; MS001 authorities |
| **Authority unchanged** | “We’re not rewriting your plan / not changing what your coach already decided / not claiming mastery from this step alone” | T2–T5 pass; no plan/evidence/recommendation mutation |
| **Outcome of the move** | What the student should understand next (wait, continue, escalate, done) | Post-transition posture |

A stage movement with no transition → condition → authority-preservation chain is invalid — even if the UI animation looks smooth.

---

## 5. Four Transition Questions (Binding)

Every material workflow transition must answer these four questions.

### TQ1 — Why did this transition occur?

**Student examples:**

- “You’ve come back to study, so we’ll start choosing today’s focus under your Study Plan.”
- “We’re waiting until your study sitting’s reflection notes are ready before updating what comes next.”
- “Those notes are ready, so we can continue from where we paused.”
- “There’s been a break in your study rhythm, so restoring continuity takes priority over ordinary daily priorities for now.”
- “Your current plan envelopes no longer fit — we’ll adjust the plan properly rather than quietly rewriting it.”
- “Today’s guidance is settled for now.”

**Developer requirements:**

- Record WT-xx and the educational/orchestration reason for movement (initiate, advance, pause, resume, escalate, supersede, handoff, explain, park, conclude).

### TQ2 — What constitutional condition permitted it?

**Student examples:**

- “Because a Study Plan is in place and today’s question is clear enough to continue.”
- “Because the evidence we need for the next step isn’t available yet — so we pause rather than guess.”
- “Because the reflection from your last sitting is now available.”
- “Because restoring progress after the disruption is the main educational question right now.”
- “Because changing the plan itself is required — coaches alone can’t stretch the envelopes safely.”

**Developer requirements:**

- Cite satisfied condition IDs / families from `TRANSITION_CONDITIONS.md` (global G1–G6 + transition-specific).
- Record which family blocked the move when transition was refused.

### TQ3 — Which components participated?

**Student examples:**

- “This step is coordination under your Study Plan — Daily Coach will decide today’s focus.”
- “Recovery coaching is leading; ordinary daily priorities take a back seat until continuity is restored.”
- “We’re handing the structural question to planning — not inventing a temporary plan in coaching.”
- “Revision emphasis informed the inputs; it didn’t rewrite your plan.”

**Developer requirements:**

- List primary Programme VI authority and any sibling input authorities involved at the transition moment.
- Record MS001 stage from/to and any WE-xx that triggered initiate/resume/supersede.

### TQ4 — Why did authority remain unchanged?

**Student examples:**

- “Moving to the next step doesn’t change what your coach recommended — it carries that recommendation forward.”
- “Waiting doesn’t invent understanding; we’ll use evidence when it’s lawfully recorded.”
- “We’re not rewriting your Study Plan in this step.”
- “Finishing this coordination step doesn’t mean you’ve mastered the topic.”
- “If advice needs to change educationally, the owning coach or planner will decide — not the handoff itself.”

**Developer requirements:**

- Explicit confirmation: no evidence reinterpretation, no coach-recommendation mutation, no plan rewrite, no independent tip (T2–T5).
- Pointer to MS001 B1–B7 / MS002 T1–T8 results for the transition.

---

## 6. Explainability Principles

1. **Transition + condition + authority.** Never narrate a move without the chain.
2. **Name waiting honestly.** Pause is tutoring care, not system failure.
3. **Name resume as continuation.** Not a new invented agenda.
4. **Name escalation as plan adjustment need.** Not silent personalisation.
5. **Name handoffs.** When primary authority changes, say so.
6. **Facts and estimates stay distinct.** Transition completion ≠ mastery.
7. **Refusal to advance is dignified.** Failed conditions are plain speech, not error theatre.
8. **Internal machinery stays invisible to students.** No WT/S/WE identifiers in student copy.
9. **Uncertainty is named** when outputs are thin.
10. **No new algorithms in speech.** Copy narrates authorised movement; it does not invent scores or schedules.

---

## 7. Worked Illustrations (Speech, Not Implementation)

### 7.1 Pause awaiting reflection (WT-03)

| Audience | Speech / record |
|----------|-----------------|
| Student | “You’ve finished today’s sitting. We’ll take a short look at what it showed before planning next steps — that reflection isn’t ready yet, so we’re waiting rather than guessing.” |
| Developer | WT-03; from S2/S3 → `awaiting_output` (Reflection notes); C-OUTPUT missing; T2–T5 pass |

### 7.2 Resume when notes available (WT-04)

| Audience | Speech / record |
|----------|-----------------|
| Student | “Your reflection notes from that sitting are ready, so we can continue and update what comes next under your Study Plan.” |
| Developer | WT-04 output-available; awaited Reflection artefact present; re-enter S2/S3; authority unchanged |

### 7.3 Escalate broken envelopes (WT-05)

| Audience | Speech / record |
|----------|-----------------|
| Student | “Your Study Plan no longer fits real life safely. We’ll adjust the plan properly — we won’t silently rewrite it inside today’s coaching.” |
| Developer | WT-05; S5 escalate; receiving primary = Master Planner / Scheduling; plan intent not mutated by transition |

### 7.4 Supersede ordinary day by recovery (WT-07)

| Audience | Speech / record |
|----------|-----------------|
| Student | “There’s been a break in your study rhythm, so getting you back on track sustainably comes first. Ordinary daily priorities wait until continuity is restored.” |
| Developer | WT-07; WE-04 higher warrant; prior day path → `superseded`; Recovery primary; history preserved |

---

## 8. Anti-Patterns

| Anti-pattern | Why unlawful |
|--------------|--------------|
| “The system moved on…” with no educational reason | Opaque transition |
| Hiding pause as “all good — keep going” while inventing tips | Independent decision + evidence dishonesty |
| Claiming mastery because a transition completed | Evidence / mastery dishonesty |
| Hiding plan rewrite as “smooth handoff” | Boundary violation |
| Editing coach recommendation text “for continuity” | Recommendation mutation |
| Student-facing WT/S/WE identifiers | Jargon leakage |
| Motivational copy that contradicts a refused advance | Invented certainty |

---

## 9. Minimal Explainability Record (Developer)

For each material transition, retain at least:

1. Transition class (WT-xx) and from → to stage/posture  
2. Permitting condition keys (G1–G6 + transition-specific) — or refusal reason  
3. Participating primary and sibling authorities  
4. Triggering WE-xx when initiate/resume/supersede applies  
5. Boundary test results (T1–T8; and B1–B7 when a recommendation path is involved)  
6. Explicit authority-preservation flags (no evidence reinterpretation, no recommendation mutation, no plan rewrite, no independent tip)  
7. Student-facing explanation draft satisfying TQ1–TQ4 without internal IDs  

Persistence format is out of scope for MS002. The **obligation** to be able to produce this record is in scope.

---

## 10. Binding Rule

Any Educational Workflow Engine behaviour that executes a material workflow transition without answering TQ1–TQ4 — and without preserving a developer trace of transition kind, permitting conditions, participants, and authority preservation — is educationally unlawful under this corpus.
