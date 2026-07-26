# Profile States

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Named educational states of the Student Educational Profile  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **educational states** — named postures describing where a student is on the learning journey.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `STUDENT_EDUCATIONAL_PROFILE.md`
3. `PROFILE_DIMENSIONS.md`
4. `planning/EDUCATIONAL_PLANNING_MODEL.md` (journey phases)
5. `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`

States are educational meanings — not database enums, UI badges, or optimiser modes. Implementations may map storage labels onto these meanings; they may not redefine the meanings in code.

> **States describe educational posture.  
> They do not schedule work and do not mint mastery.**

---

## 1. Purpose

An expert tutor summarises a student in plain educational language: *beginning*, *building foundations*, *practising*, *revising*, *recovering*, *at risk*, *exam ready*.

These states capture that summary so Master Planner and student-facing narration share one vocabulary.

A student may exhibit secondary colouring (e.g. Practising while At Risk on feasibility). The **primary educational state** is the dominant journey posture; risk and recovery may overlay.

---

## 2. State Principles

1. **Meaning before labels.** UI copy may vary; educational meaning must match this catalogue.
2. **Evidence-aware.** States that imply understanding require warrant; coverage-heavy states must not smuggle competence.
3. **Non-punitive.** Recovering, Returning After Break, and At Risk are diagnostic — never shame categories.
4. **Reversible.** Students move among states as inputs evolve (see `PROFILE_EVOLUTION.md`).
5. **Explainable.** Every assigned state must answer why (see `PROFILE_EXPLAINABILITY.md`).
6. **Not a plan phase clone.** Planning phases (MS001) are journey design; Profile states are diagnosis. They often align but are not identical objects.
7. **Silence over stretch.** Prefer a more cautious adjacent state when warrant is thin.

---

## 3. Primary Educational States

### S1 — Beginning Study

**Educational meaning:** The student is at or near the start of lawful preparation for the named examination. Coverage is minimal or unset; practice evidence is typically empty; capacity and sitting may just have been established.

**Tutor reading:** “We are establishing the journey, not claiming progress.”

**Typical dimension pattern:**
- D2 coverage low / intake
- D3 understanding thin or absent
- D1/D6/D7 may be present (intake) or incomplete

**Must not claim:** Exam readiness; demonstrated mastery; that a plan alone equals learning.

**Adjacent states:** Building Foundation; Intake Incomplete (meta); Returning After Break (if prior history exists but restart is true beginning of *this* sitting).

---

### S2 — Building Foundation

**Educational meaning:** The student is in honest first-pass learning — covering official syllabus units in educational order, establishing prerequisites, with understanding evidence still early or uneven.

**Tutor reading:** “Foundations first; coverage is growing; competence claims stay provisional.”

**Typical dimension pattern:**
- D2 rising through early/mid syllabus
- D19 Learning Mode posture dominant
- D3 sparse-to-emerging
- D8 revision maturity low

**Must not claim:** That finishing early chapters equals exam readiness; that light practice proves mastery.

**Adjacent states:** Beginning Study; Practising; Strengthening (if foundations need repair).

---

### S3 — Practising

**Educational meaning:** The student has enough coverage on current material to spend meaningful effort on application — question practice informs estimates — while first-pass learning may still continue elsewhere.

**Tutor reading:** “We are converting study into demonstrated application where evidence allows.”

**Typical dimension pattern:**
- D4 question performance active
- D3 estimates forming on practised topics
- D15 practice depth increasing
- D2 may still be incomplete overall

**Must not claim:** Practice alone completed the syllabus; one strong set equals durable competence.

**Adjacent states:** Building Foundation; Strengthening; Revising (when return/consolidation dominates).

---

### S4 — Strengthening

**Educational meaning:** The student needs deliberate reinforcement of weak or shaky areas — foundations, weak topics, or uneven estimates — before it is educationally honest to treat progress as secure.

**Tutor reading:** “We reinforce what is fragile; we do not pretend even coverage.”

**Typical dimension pattern:**
- D3/D4 show topic weaknesses
- D16 foundation integrity concerns possible
- D10 educational confidence uneven
- May follow poor mocks or thin understanding despite coverage

**Must not claim:** Strengthening is punishment; that weakness discovery means the student “fell behind” if coverage was never evidenced.

**Adjacent states:** Practising; Building Foundation; Revising; Recovering.

---

### S5 — Revising

**Educational meaning:** The student is consolidating previously studied material in educational substance — spaced return, deepening application, Revision Mode posture — not merely re-reading casually.

**Tutor reading:** “We protect retention and deepen what was already studied.”

**Typical dimension pattern:**
- D8 revision maturity rising
- D19 Revision Mode substance present
- D13 decay risk being addressed
- D2 first-pass largely advanced *or* revision interleaved under lawful consolidation

**Must not claim:** Any calendar week labelled “revision” without substance; that revision invents coverage never studied.

**Adjacent states:** Practising; Exam Preparation; Strengthening.

---

### S6 — Exam Preparation

**Educational meaning:** The student is in the final-approach educational posture — emphasis on high-value revision, exam behaviour, stamina, and stabilisation; new first-pass expansion is tightly constrained or frozen.

**Tutor reading:** “We stabilise for the sitting; we do not open new syllabus frontiers lightly.”

**Typical dimension pattern:**
- D7 short runway
- D8 high revision substance
- D15 mocks / timed exposure present or due
- D18 risk narration explicit if capacity tight

**Must not claim:** Exam Preparation equals Exam Ready; pass guarantees from proximity alone.

**Adjacent states:** Revising; Exam Ready; At Risk.

---

### S7 — Recovering

**Educational meaning:** The student is restoring a viable trajectory after interruption, illness, leave, burnout, or abandoned intensity. Educational history still belongs to the learner; load is reduced before heroic catch-up.

**Tutor reading:** “Restart that still counts — without shame or false diagnosis.”

**Typical dimension pattern:**
- D12 recovery history active
- D5 consistency temporarily disrupted
- D14 reliability may need recalibration
- D11 motivation may be fragile

**Must not claim:** Recovery erases lawful coverage; that the student must “make up every lost hour” immediately.

**Adjacent states:** Returning After Break; Building Foundation; Practising; At Risk.

---

### S8 — Returning After Break

**Educational meaning:** The student is re-entering study after a significant gap. Diagnosis must re-establish cadence and check retention risk without inventing discontinuity in rightful Study Progress.

**Tutor reading:** “Welcome back — we re-orient honestly to where coverage and evidence stand now.”

**Typical dimension pattern:**
- D12 gap then re-engagement
- D13 decay posture elevated (estimated)
- D5 resetting
- D2 coverage persists unless explicitly reset

**Must not claim:** Break equals zero progress; that felt rust equals wiped Study Progress.

**Adjacent states:** Recovering; Beginning Study (true cold restart of sitting); Strengthening; Revising.

---

### S9 — At Risk

**Educational meaning:** Feasibility, consistency, foundation integrity, or evidence patterns indicate material danger to honest exam readiness under current capacity and time — without asserting a numeric fail probability theatre.

**Tutor reading:** “We name the risk early so strategy can change.”

**Typical dimension pattern:**
- D18 elevated risk
- Often D7 short + D2 large remainder, and/or D14 poor reliability, and/or D16 foundation breaks
- May overlay any primary journey state

**Usage rule:** At Risk may be a **primary** state when risk dominates the tutor conversation, or an **overlay** on another primary state (e.g. Revising + At Risk).

**Must not claim:** Moral failure; precise pass/fail odds; that motivation alone clears risk.

**Adjacent states:** Recovering; Exam Preparation; Strengthening.

---

### S10 — Exam Ready

**Educational meaning:** Provisional educational judgement that coverage, revision substance, practice depth, and evidence warrant support sitting with honest preparedness language — always provisional, never a guarantee.

**Tutor reading:** “On present evidence, preparation looks exam-credible — still provisional.”

**Typical dimension pattern:**
- D2 first-pass substantially complete for the sitting scope
- D8 revision maturity adequate
- D15 meaningful assessment exposure
- D3/D4 not critically hollow on core syllabus
- D10 educational confidence sufficient to speak readiness *as estimate*
- D18 not dominating with unresolved infeasibility

**Must not claim:** Guaranteed pass; that Exam Ready freezes forever; that coverage ticks alone suffice.

**Adjacent states:** Exam Preparation; Revising; At Risk (if new evidence or time shock appears).

---

## 4. Meta / Envelope States

These are not journey postures but diagnostic envelope labels.

### M1 — Intake Incomplete

**Meaning:** Mandatory profile inputs for planner-consumable diagnosis are missing (exam, sitting, capacity, and/or coverage starting position).

**Consequence:** Gather facts; do not publish complete long-term plans as if diagnosis were whole.

### M2 — Thin Evidence

**Meaning:** Coverage and calendar may exist, but understanding warrant is sparse.

**Consequence:** Narrate coverage; understate understanding and readiness; invite practice evidence.

### M3 — Assumption-Reliant

**Meaning:** Material dimension values rest on explicit Planning Assumptions rather than observed inputs.

**Consequence:** Disclose assumptions in explainability; prefer re-intake when assumptions break.

---

## 5. Relationship to Planning Phases (MS001)

| Planning phase (MS001) | Commonly aligned Profile states |
|------------------------|-----------------------------------|
| Registration & Intake | Beginning Study; Intake Incomplete |
| Foundation & First-Pass | Building Foundation; Practising |
| Consolidation Windows | Practising; Revising (light); Strengthening |
| Protected Revision | Revising; Exam Preparation |
| Mock & Exam Simulation | Exam Preparation; Strengthening; Practising |
| Final Approach | Exam Preparation; Exam Ready; At Risk |
| Recovery / Replan | Recovering; Returning After Break; At Risk |

Alignment is educational guidance for readers — not a hard state machine identity.

---

## 6. State Assignment Rules (Educational)

1. Assign the **primary state** that best matches dominant educational posture.
2. Allow **At Risk** and meta states as overlays when warranted.
3. Prefer **Recovering / Returning After Break** over silent “behind” rhetoric after gaps.
4. Do not assign **Exam Ready** from coverage percentage alone.
5. Do not assign **Revising** from a UI mode switch without revision substance.
6. Same inputs → same primary state (determinism).
7. When torn between two states, choose the one that understates readiness.

---

## 7. Forbidden State Theatre

| Theatre | Why forbidden |
|---------|----------------|
| “Elite” / gamified ranks as educational state | Not tutor diagnosis |
| Red/amber/green only, without meaning | Hides educational content |
| Permanent At Risk branding after one missed week | Disproportionate; use Recovering |
| Exam Ready from wizard completion | Plan existence ≠ readiness |

---

## 8. Cross References

- `PROFILE_DIMENSIONS.md` — axes behind states
- `PROFILE_EVOLUTION.md` — transitions among states
- `PROFILE_EXPLAINABILITY.md` — how to speak states
- `planning/EDUCATIONAL_PLANNING_MODEL.md` — journey phases
