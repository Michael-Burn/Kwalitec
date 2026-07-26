# Workflow Explainability

**Programme:** VII — Workstream 1 — Educational Workflow Engine  
**Milestone:** MS001 — Educational Workflow Model  
**Classification:** Explainability contract for educational workflow orchestration  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **workflow orchestration** to students and developers.

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
3. [`EDUCATIONAL_WORKFLOW_MODEL.md`](EDUCATIONAL_WORKFLOW_MODEL.md)
4. [`WORKFLOW_OBJECTIVES.md`](WORKFLOW_OBJECTIVES.md) (especially WO-04)
5. [`WORKFLOW_EVENTS.md`](WORKFLOW_EVENTS.md)
6. [`WORKFLOW_STAGES.md`](WORKFLOW_STAGES.md)
7. [`WORKFLOW_BOUNDARIES.md`](WORKFLOW_BOUNDARIES.md)
8. Programme VI explainability corpora for the invoked primary authority

> **Explainability improves understanding of orchestration already authorised.  
> It never invents educational certainty or independent recommendations.**

---

## 1. Purpose

Students should never have to guess why Kwalitec suddenly shifted from ordinary study to recovery, revision, or exam preparation — or why conflicting advice did not appear.

Developers should never have to reverse-engineer which constitutional component owned a decision.

Workflow explainability exists so every material orchestration answers — in the right language for the audience — **why a workflow started**, **which constitutional components participated**, **how authority was preserved**, and **why the resulting educational recommendation emerged**.

Without workflow explainability:

- day / recovery / revision / exam shifts feel arbitrary;
- coaches appear to argue in the UI;
- escalation feels like product breakage;
- audits cannot prove authority preservation.

With workflow explainability:

- the student trusts the tutor posture across transitions;
- developers can verify Programme VII did not invent meaning;
- claim types stay honest;
- refusals and escalations remain dignified and clear.

---

## 2. Two Audiences

| Audience | Language | Must include | Must exclude |
|----------|----------|--------------|--------------|
| **Student** | Plain educational speech | Why guidance changed or stayed; what to do next; honest limits | WE/WO/S IDs, queue names, Twin facets, optimiser jargon |
| **Developer / auditor** | Precise constitutional references | Event class, stages, primary authority, boundary checks, outcome class | Student-facing motivational fluff as a substitute for audit fields |

Student copy narrates educational reasons. Developer traces cite document IDs and stage outcomes.

---

## 3. Traceability Obligation (Architectural)

Every material orchestrated outcome must be traceable through:

| Trace link | Student-facing role | Developer-facing role |
|------------|---------------------|------------------------|
| **Educational event** | “Because you returned to study / finished today’s sitting / …” | WE-xx classification |
| **Warrant / primary authority** | “So today’s question is… / So we need to restore progress…” | S1 primary authority name |
| **Lawful inputs** | “Given your Study Plan and where you are now…” | S2 input sources |
| **Programme VI reasoning** | “Your coach recommends…” (using that coach’s explainability contract) | Invoked Programme VI artefact reference |
| **Conflict / handoff check** | “We’re focusing on recovery first, so ordinary study waits…” | S4 clearance or supersede record |
| **Outcome class** | Clear next step, or honest “we need to adjust your plan” | Recommend / hand off / refuse / escalate |
| **Authority preservation** | Implicit in speech that does not invent plan rewrites | Explicit B1–B7 boundary test pass |

A recommendation with no event → authority → Programme VI artefact chain is invalid — even if the explanation sounds motivating.

---

## 4. Four Orchestration Questions (Binding)

Every material workflow outcome must answer these four questions.

### Q1 — Why did this workflow start?

**Student examples:**

- “You’ve come back to study, so we’ll choose the most useful thing for today under your Study Plan.”
- “Your last study sitting finished, so we’ll take a short look at what it showed before planning next steps.”
- “There’s been a break in your study rhythm, so we’ll focus on getting you back on track sustainably.”
- “Your exam is getting closer, so we’ll check whether exam-style preparation is the right focus *yet*.”

**Developer requirements:**

- Record WE-xx, initiate vs continue vs supersede, and no-op rationale when applicable.

### Q2 — Which constitutional components participated?

**Student examples:**

- “This comes from your Study Plan and today’s coaching.”
- “Recovery coaching is leading right now; ordinary daily priorities take a back seat until continuity is restored.”
- “Revision emphasis informed today’s choice; it didn’t replace your plan.”

**Developer requirements:**

- List primary authority and any sibling input authorities.
- Record S3 invocation and S4 conflict result.

### Q3 — How was authority preserved?

**Student examples:**

- “We’re not rewriting your Study Plan — we’re working inside it.”
- “Finishing this step doesn’t mean you’ve mastered the topic.”
- “If your plan no longer fits real life, we’ll say so and adjust the plan properly — not silently.”

**Developer requirements:**

- Evidence of boundary tests B1–B7.
- Explicit confirmation: no plan mutation, no evidence reinterpretation, no independent recommendation, no coach-meaning rewrite.

### Q4 — Why did this educational recommendation (or handoff / refusal) emerge?

**Student examples:**

- “Given your plan’s focus and what today allows, the most valuable thing is…”
- “Because disruption is the main issue, today’s job is restorative — not heroic catch-up.”
- “Exam-style work isn’t the priority yet — there’s still first learning / consolidation needed.”
- “We can’t give a safe recommendation until a Study Plan is in place.”

**Developer requirements:**

- Outcome class (recommend / hand off / refuse / escalate).
- Pointer to Programme VI explainability answers for the educational content itself (Daily Coach / Recovery / etc.).

---

## 5. Explainability Principles

1. **Event + authority + outcome.** Never narrate a tip without the chain.
2. **One primary story.** Prefer a single clear educational purpose over multi-coach dumps.
3. **Name handoffs.** When primary authority changes, say so.
4. **Facts and estimates stay distinct.** Workflow completion ≠ mastery.
5. **Protections spoken as intentional.** Recovery and revision waits are coaching commitments, not apologies.
6. **Refusal is dignified.** Missing plan or failed warrant is plain speech, not error theatre.
7. **Escalation is plain.** Structural change is “adjust the plan,” not silent rewrite.
8. **Internal machinery stays invisible to students.** No stage IDs, saga names, or registry codes in student copy.
9. **Uncertainty is named** when inputs are thin.
10. **No new algorithms in speech.** Copy narrates authorised orchestration; it does not invent scores.

---

## 6. EIP-003 Alignment

EIP-003’s four questions (what we know, what we estimate, why this advice, what next) remain binding for the **educational content** produced by Programme VI.

This document adds an **orchestration layer** that must be answerable *in addition* when the path to that content involved Programme VII coordination:

| Layer | Owner | Questions |
|-------|-------|-----------|
| Educational content | Programme VI coach / planner explainability | EIP-003 specialised per corpus |
| Orchestration path | This document | Q1–Q4 above |

Both layers are required for material orchestrated outcomes. Orchestration explainability never replaces coach explainability.

---

## 7. Anti-Patterns

| Anti-pattern | Why unlawful |
|--------------|--------------|
| “The system decided…” with no educational reason | Opaque orchestration |
| Blended coach voice with no primary named | Authority erasure |
| Claiming mastery because a workflow completed | Evidence / mastery dishonesty |
| Hiding plan rewrite as “personalisation” | Boundary violation |
| Student-facing WE/S/WO identifiers | Jargon leakage |
| Motivational copy that contradicts Programme VI refusal | Invented certainty |

---

## 8. Minimal Explainability Record (Developer)

For each material workflow instance, retain at least:

1. Event class (WE-xx) and initiate/continue/supersede/no-op  
2. Primary authority selected at S1  
3. Sibling input authorities (if any)  
4. Outcome class at S5  
5. Boundary test results (B1–B7)  
6. Reference to Programme VI artefact used for educational content  
7. Student-facing explanation draft satisfying Q1–Q4 without internal IDs  

Persistence format is out of scope for MS001. The **obligation** to be able to produce this record is in scope.

---

## 9. Binding Rule

Any Educational Workflow Engine behaviour that emits a material student-facing educational outcome without answering Q1–Q4 — and without preserving a developer trace of event, primary authority, boundary preservation, and Programme VI provenance — is educationally unlawful under this corpus.
