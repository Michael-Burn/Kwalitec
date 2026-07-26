# Profile Evolution

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Temporal evolution of the Student Educational Profile  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **how educational profiles evolve over time**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `STUDENT_EDUCATIONAL_PROFILE.md`
3. `PROFILE_DIMENSIONS.md`
4. `PROFILE_STATES.md`
5. `PROFILE_INPUTS.md`
6. `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`
7. `EDUCATIONAL_EVIDENCE_MODEL.md`

> **The Profile represents educational growth — not a static intake form.  
> Evolution updates diagnosis; it does not by itself generate a new plan.**

---

## 1. Purpose

Students change. Coverage grows, evidence accumulates, motivation fluctuates, breaks happen, recovery restores trajectory.

An expert tutor revises their picture of the student as these events unfold. This document records those revision rules so algorithms refresh diagnosis instead of freezing a first-week stereotype.

---

## 2. Evolution Principles

1. **Growth is multi-axis.** Reading raises coverage; practice raises evidence; neither automatically raises the other.
2. **History persists.** Lawful Study Progress and Evidence belong to the learner across plan containers (unless informed reset).
3. **Decay is estimated, not erasure.** Suspected forgetting adjusts retention/revision posture; it does not silently delete coverage.
4. **Soft signals are volatile.** Motivation and felt confidence may move quickly; hard facts move through durable events.
5. **Recovery is constructive.** Return after interruption restores trajectory without shame narratives.
6. **Missed study changes reliability and confidence posture** — it does not invent incompetence.
7. **Re-diagnosis precedes replan.** When evolution is material, Master Planner must re-consult the Profile (MS001 recovery/replan posture).
8. **Deterministic succession.** Same event + same prior Profile → same educational update meaning.

---

## 3. Evolution Event Catalogue

### E1 — Reading / First-Pass Study Completion

**What happens educationally:** Coverage (D2) advances for the completed syllabus unit when lawful.

**Typically increases:** D2; may shift S1→S2 or deepen Building Foundation / Practising.

**Does not by itself increase:** D3 demonstrated understanding; Exam Ready warrant.

**Speech cue:** “You’ve covered more of the syllabus” — not “You now know this.”

---

### E2 — Question Practice / Performance Evidence

**What happens educationally:** Authorised results enter Evidence; D4 updates; D3/D10 may succeed provisionally.

**Typically increases:** Evidence density; topic-level estimates (up or down); Practising / Strengthening posture.

**May decrease:** Educational confidence (D10) if results contradict prior optimism; felt confidence may diverge.

**Does not:** Convert mission completion into mastery; erase coverage on poor performance.

---

### E3 — Revision & Spaced Return

**What happens educationally:** Revision maturity (D8) and retention posture (D13) improve when return is substantive.

**Typically supports:** Transition toward Revising / Exam Preparation; reduces estimated decay risk on revisited topics.

**Does not:** Create coverage for never-studied topics; guarantee Exam Ready.

---

### E4 — Mock / Exam Simulation

**What happens educationally:** High-value performance and stamina evidence; may reveal integrated weaknesses.

**Typically updates:** D4, D15, D10, possibly D18; may trigger Strengthening if gaps are material.

**Does not:** Prophesy pass/fail; permanently brand At Risk from one difficult mock without context.

---

### E5 — Missed Study / Broken Cadence

**What happens educationally:** Consistency (D5) and planning reliability (D14) degrade; soft motivation may fall; feasibility risk (D18) may rise if runway is short.

**Typically supports:** Overlay At Risk when material; or Recovering if student is restarting intentionally.

**Does not:** Delete Study Progress; invent weak understanding solely from absence.

**Speech cue:** Name the gap and capacity impact — never character attack.

---

### E6 — Declared Leave / Planned Interruption

**What happens educationally:** Calendar capacity adjusts; recovery history records planned pause; time remaining effective runway shrinks.

**Typically supports:** Pre-emptive plan buffers (planning concern); Profile marks known interruption.

**Does not:** Treat planned leave as reliability failure.

---

### E7 — Recovery / Re-engagement

**What happens educationally:** Recovery history (D12) advances positively; consistency begins to reset; trajectory restores.

**Typically supports:** Recovering → Building Foundation / Practising / Revising as substance returns.

**Does not:** Require heroic catch-up as the definition of recovery success.

---

### E8 — Returning After Break (Unplanned Gap End)

**What happens educationally:** Re-entry state; decay posture (D13) often elevated as estimate; coverage persists.

**Typically supports:** Returning After Break primary state; invite light strengthening/revision of rusty areas using evidence when available.

**Does not:** Zero the Profile; equate rust with never studied.

---

### E9 — Capacity Re-declaration

**What happens educationally:** Available study time (D6) updates; planning reliability baseline may reset; feasibility (D18) recomputed.

**Typically supports:** Honest intensity changes; may clear or raise At Risk.

**Does not:** Keep using obsolete hours after clear re-intake.

---

### E10 — Sitting Date Change

**What happens educationally:** Time remaining (D7) and feasibility rewrite; Exam Preparation / Exam Ready may cease to apply.

**Typically supports:** Full re-diagnosis; old runway maths void (Planning Assumption A6 break).

**Does not:** Preserve Exam Ready labels from the previous sitting horizon without re-check.

---

### E11 — Previous Attempt Outcome Recorded

**What happens educationally:** D9 updates; risk posture recalibrates; strengths/weaknesses priors may shift.

**Typically supports:** More cautious Exam Ready threshold; Strengthening emphasis on weak areas.

**Does not:** Shame; wipe rightful coverage from the failed sitting’s study history without informed reset.

---

### E12 — Reflection / Felt Confidence / Motivation Update

**What happens educationally:** Soft dimensions (D11) update; coaching tone may change.

**Typically supports:** Sensitivity in Recovering / At Risk narration.

**Does not:** Rewrite D3/D10 educational warrant; author mastery.

---

### E13 — Concurrent Load Change

**What happens educationally:** Effective capacity and D17 update; D18 may move.

**Typically supports:** Feasibility honesty when a second subject or work peak appears.

---

### E14 — Evidence Decay / Long Silence on Practised Topics

**What happens educationally:** Retention posture (D13) worsens as estimate; educational confidence on stale estimates may thin.

**Typically supports:** Revising / Strengthening emphasis.

**Does not:** Delete coverage; fabricate precise forgetting percentages as Observed Fact.

---

### E15 — Informed Educational Reset (Rare)

**What happens educationally:** Explicit student-informed reset of selected history per continuity law.

**Typically supports:** Return toward Beginning Study / Intake for reset scope only.

**Does not:** Happen silently; happen as a side effect of disposing a study plan container.

---

## 4. State Transition Patterns (Illustrative)

These patterns are educational expectations — not an exhaustive finite-state machine.

```
Beginning Study
    → Building Foundation          (first-pass coverage starts)
    → Returning After Break        (history exists; re-entry)

Building Foundation
    → Practising                   (application work becomes material)
    → Strengthening                (foundation cracks evidenced)
    → Recovering                   (interruption)

Practising
    → Strengthening                (weaknesses dominate)
    → Revising                     (return/consolidation dominates)
    → At Risk                      (feasibility overlay / primary)

Revising
    → Exam Preparation             (final approach posture)
    → Strengthening                (mock/evidence reveals gaps)
    → Exam Ready                   (provisional warrant met)

Exam Preparation
    → Exam Ready                   (provisional)
    → At Risk                      (runway/capacity break)
    → Strengthening                (late gaps)

Recovering / Returning After Break
    → Building Foundation | Practising | Revising   (substance resumes)
    → At Risk                      (if runway already critical)

Exam Ready
    → Exam Preparation / Revising  (maintenance)
    → At Risk                      (new adverse evidence or date shock)
```

---

## 5. What Evolution Must Preserve

| Preserve | Rule |
|----------|------|
| Claim types | Coverage growth ≠ understanding growth in speech or state jumps |
| Learner-owned history | Plan replace does not wipe Profile dimensions unlawfully |
| Soft vs hard | Soft updates never silently rewrite hard dimensions |
| Understatement | Adverse evolution may lower readiness states; favourable evolution must not leap to Exam Ready without warrant |
| Explainability | Material state changes require a “what changed” explanation |

---

## 6. Material vs Immaterial Evolution

| Material (must re-consult Profile for planning) | Immaterial (may refresh soft tone only) |
|-------------------------------------------------|----------------------------------------|
| Coverage milestone blocks; mock outcomes; date change; capacity re-intake; multi-week gap; At Risk threshold cross; recovery completion | Single reflection mood; one missed day with buffer; minor felt-confidence wobble |

Materiality is educational judgement for future algorithms — when uncertain, treat as material.

---

## 7. Growth Narrative (Tutor Summary)

An honest Profile over a full sitting often tells a story like:

1. Intake establishes exam, time, and starting coverage.
2. Reading and study raise coverage while evidence stays thin.
3. Practice thickens understanding estimates unevenly.
4. Consistency and reliability reveal the real sustainable pace.
5. Consolidation and revision protect retention as the syllabus lengthens.
6. Interruptions appear; recovery restores trajectory without erasing history.
7. Mocks calibrate stamina and expose late gaps.
8. Final approach either supports provisional Exam Ready language — or honest At Risk / replan conversation.

That story is educational growth. Static profiles that never change after wizard day one fail this Model.

---

## 8. Cross References

- `PROFILE_STATES.md` — state meanings
- `PROFILE_INPUTS.md` — events that arrive as inputs
- `PROFILE_EXPLAINABILITY.md` — narrating change
- `planning/EDUCATIONAL_PLANNING_MODEL.md` — Recovery / Replan phase
- `EDUCATIONAL_CONTINUITY_STANDARD.md` — continuity law
