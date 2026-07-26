# Strategy Selection Model

**Programme:** VI — Master Planner  
**Milestone:** MS003 — Educational Strategy Framework  
**Classification:** Educational reasoning for choosing a primary strategy  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **how an expert IFoA tutor chooses an educational strategy** from the Student Educational Profile.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_STRATEGY_FRAMEWORK.md`
3. `STRATEGY_CATALOGUE.md`
4. `student_profile/STUDENT_EDUCATIONAL_PROFILE.md`
5. `student_profile/PROFILE_DIMENSIONS.md`
6. `student_profile/PROFILE_STATES.md`
7. `planning/PLANNING_CONSTRAINTS.md`

This is educational decision reasoning — not an algorithm, scoring formula, or decision tree implementation. Future algorithms must implement this reasoning; they must not replace it with opaque weights.

> **Strategy selection is Profile-driven educational judgement.  
> It is never an arbitrary product rule detached from diagnosis.**

---

## 1. Purpose

Given a Student Educational Profile, the tutor must answer:

1. Which Catalogue strategy should be primary?
2. Why educationally?
3. What secondary emphasis (if any) is lawful?
4. When must selection refuse to publish a complete strategy?

This Model records that judgement so Master Planner algorithms select strategy the same way an excellent tutor would.

---

## 2. Selection Principles

1. **Profile first.** No complete strategy without consulting dimensions and primary state.
2. **One primary strategy.** Clarity over cocktail approaches.
3. **Need severity orders attention.** Feasibility crisis and recovery outrank optimisation polish.
4. **Understate readiness.** When torn, prefer Build / Restore / Triage over Approach optimisation.
5. **Hard facts outrank soft signals.** Capacity, coverage, time, and evidence beat mood alone — except when Confidence Restoration is *about* soft signals and hard facts are stable.
6. **Constraints bind selection.** A strategy that would require unlawful planning is not selectable as if constraints did not exist.
7. **Silence over theatre.** Intake Incomplete → gather facts; do not invent Foundation Building confidence from empty intake.
8. **Determinism.** Same Profile → same primary strategy.
9. **Explainability ready.** Selection must yield a primary educational reason speakable to the student.

---

## 3. Preconditions

### 3.1 Strategy selection may publish a complete primary strategy when

| Requirement | Why |
|-------------|-----|
| Examination / subject known (D1) | Strategy is sitting-scoped |
| Sitting / target date known (D1/D7) | Horizon shapes Build vs Triage vs Approach |
| Available capacity known (D6) | Intensity envelope exists |
| Coverage starting position known (D2) | Build vs Deepen vs Approach depends on it |
| Primary Profile state assignable | Dominant posture is named |

These align with MS001 mandatory planning inputs and MS002 planner-consumable diagnosis.

### 3.2 Selection must refuse complete strategy publication when

| Condition | Educational response |
|-----------|----------------------|
| **M1 Intake Incomplete** | Gather facts; discuss options only; no pretend complete strategy for planning |
| Conflicting hard inputs unresolved | Prefer continuity of lawful history; disclose uncertainty; understate |
| Profile marks **M3 Assumption-Reliant** on material axes | May select a *cautious* strategy only if assumptions are disclosed in explainability |

Thin evidence (**M2**) does **not** block selection — it biases toward Build / cautious Practice Intensive and away from Exam Ready–adjacent strategies.

---

## 4. Tutor Decision Sequence (Educational)

An expert tutor does not run a black box. The educational sequence is:

```
1. Is diagnosis complete enough to choose?
2. Is there an active restore need (recovery / confidence)?
3. Is there a triage need (rescue / late starter)?
4. What is the dominant journey posture (build / deepen / approach)?
5. Within that family, which Catalogue strategy fits best?
6. Is a secondary emphasis warranted without confusing the primary?
7. Can this strategy be explained in one primary reason?
```

This sequence is **priority of educational attention**, not a coded flowchart with numeric cutoffs.

---

## 5. Priority Lenses (Binding Attention Order)

When multiple strategies could argue for themselves, apply lenses in this order:

### L1 — Integrity & feasibility truth

If the Profile cannot support an honest complete journey under current capacity and time, **Triage** outranks comfort strategies.

- Prefer **ES-09 Exam Rescue** when the crisis is late-horizon infeasibility / At Risk near sitting.
- Prefer **ES-10 Late Starter Strategy** when short runway is present from the start (or effectively from restart) with large remaining first-pass.

**Educational reason:** Optimistic Steady Progression under known impossibility is educationally unlawful.

### L2 — Restore capacity and trust

If recovery history, broken consistency, or fragile confidence dominates the tutor conversation — and L1 does not require immediate triage — **Restore** outranks deepen/approach polish.

- Prefer **ES-08 Recovery Strategy** when interruption, burnout, or abandoned intensity is the main story.
- Prefer **ES-07 Confidence Restoration** when soft confidence/motivation is the main fracture but cadence and feasibility are otherwise workable.

**Educational reason:** Plans that ignore recovery produce abandonment; plans that ignore confidence produce empty adherence.

### L3 — Dominant journey posture

If L1–L2 are quiet, select from **Build / Deepen / Approach** using Profile state and dimensions:

| Dominant need | Prefer |
|---------------|--------|
| Early / prerequisite-heavy first-pass | ES-01 Foundation Building |
| Sustainable ongoing first-pass | ES-02 Steady Progression |
| Retention risk during long first-pass | ES-03 Knowledge Consolidation |
| Convert coverage → application evidence | ES-04 Practice Intensive |
| Fragile topics / foundations | ES-06 Weak Topic Reinforcement |
| Pre-exam consolidation dominant | ES-05 Revision Intensive |
| Strong warrant; refine exam craft | ES-11 High Performer Optimisation |
| Stable readiness; preserve | ES-12 Balanced Maintenance |

### L4 — Understatement tie-break

If two strategies remain equally plausible:

1. Prefer the strategy that understates readiness.
2. Prefer foundation / revision protection over expansion.
3. Prefer Steady Progression over High Performer Optimisation.
4. Prefer Weak Topic Reinforcement over Balanced Maintenance when weakness warrant exists.

---

## 6. Profile → Strategy Reasoning Map

The following map is **educational guidance**. It is not a hard state machine identity. Selection still applies L1–L4.

| Primary Profile state | Common primary strategies | Educational rationale |
|-----------------------|---------------------------|------------------------|
| S1 Beginning Study | ES-01; ES-10 if short runway | Establish foundations or honest compression |
| S2 Building Foundation | ES-01; ES-02 | First-pass spine; steady if underway |
| S3 Practising | ES-04; ES-02; ES-03 | Practice emphasis or continued progress with consolidation |
| S4 Strengthening | ES-06; ES-04 | Reinforce fragility before secure progress claims |
| S5 Revising | ES-05; ES-03 | Revision dominant or consolidation if still mid-journey |
| S6 Exam Preparation | ES-05; ES-11; ES-09 if At Risk | Approach sitting; rescue if feasibility breaks |
| S7 Recovering | ES-08; ES-07 | Restore trajectory; confidence if that is the fracture |
| S8 Returning After Break | ES-08; ES-01/ES-03 as re-orient | Re-establish cadence; then build/consolidate honestly |
| S9 At Risk | ES-09; ES-10; ES-06; ES-08 | Triage or reinforce depending on risk shape |
| S10 Exam Ready | ES-12; ES-11 | Maintain or lightly optimise — provisional |

### Dimension cues (supporting, not solo)

| Dimension cue | Strategy lean |
|---------------|---------------|
| D2 low + D7 adequate | ES-01 / ES-02 |
| D2 low + D7 short | ES-10 |
| D13 elevated mid first-pass | ES-03 |
| D15 thin vs D2 advanced on scope | ES-04 |
| D3/D4/D16 weak | ES-06 |
| D8 must rise + D7 shortening | ES-05 |
| D12 active / D5 broken | ES-08 |
| D11 fragile, hard facts stable | ES-07 |
| D18 elevated late | ES-09 |
| Strong D2/D3/D4/D8/D15, calm D18 | ES-11 / ES-12 |
| D9 retake with weak areas | ES-06 / ES-05 (not automatic ES-01 wipe) |

Soft dimensions alone never select ES-11 or ES-12.

---

## 7. Educational Reasoning by Strategy

Each Catalogue strategy has a core educational warrant. Selection must be able to state it.

| ID | Core warrant (why a tutor chooses it) |
|----|----------------------------------------|
| ES-01 | Without foundations, later study is hollow |
| ES-02 | Consistency on a lawful sequence compounds readiness |
| ES-03 | Long syllabuses forget themselves without return |
| ES-04 | IFoA exams reward application; coverage alone is incomplete |
| ES-05 | Near the sitting, consolidation outranks expansion |
| ES-06 | Uneven understanding is a readiness risk if ignored |
| ES-07 | Fragile confidence blocks productive learning even when the plan is feasible |
| ES-08 | Interrupted students need restart that still counts |
| ES-09 | Honesty under short time beats optimistic fiction |
| ES-10 | Late start needs compressed truth from day one |
| ES-11 | Strong evidence warrants polish, not reinvention |
| ES-12 | Stable readiness is protected by maintenance, not upheaval |

If the Profile cannot support the core warrant, that strategy is not primary.

---

## 8. Secondary Emphasis Rules

A secondary emphasis is allowed when it refines the primary without replacing it.

**Lawful examples:**

- Primary **ES-02 Steady Progression** + secondary **Weak Topic Reinforcement** on a known fragile unit.
- Primary **ES-05 Revision Intensive** + secondary **Practice Intensive** as revision method.
- Primary **ES-08 Recovery Strategy** + secondary **Confidence Restoration** tone.

**Unlawful examples:**

- Primary **ES-12 Balanced Maintenance** + secondary **Late Starter** (contradictory stories).
- Primary **ES-01 Foundation Building** + secondary **High Performer Optimisation**.
- Two triage strategies both presented as equal primaries.

Student explainability must lead with the **primary** strategy name and reason.

---

## 9. Mandatory / Adaptive / Forbidden Selection Behaviours

| Class | Behaviours |
|-------|------------|
| **Mandatory** | Consult Profile; choose one primary Catalogue strategy when publishing for planning; attach explainability reason; respect Planning Constraints; refuse complete strategy under M1 |
| **Adaptive** | Which strategy within L3; secondary emphasis; cautious vs assertive wording under M2/M3 |
| **Forbidden** | Strategy without Profile; non-Catalogue names; random variety; soft-signal override of hard infeasibility; selecting ES-12/ES-11 from coverage ticks alone; selecting ES-05 as main story with no studied material to revise |

---

## 10. Worked Educational Vignettes

These vignettes illustrate reasoning — they are not test fixtures with numeric thresholds.

### V1 — Early CM1 candidate with time

**Profile sketch:** S2 Building Foundation; D2 early; D7 ample; D18 calm; thin D3.

**Selection:** ES-01 Foundation Building (or ES-02 if first-pass already stably underway).

**Why:** Need is sequential foundations, not rescue or revision theatre.

### V2 — Mid-syllabus, forgetting earlier topics

**Profile sketch:** S3; D2 mid; D13 elevated; practice present but retention worry.

**Selection:** ES-03 Knowledge Consolidation (primary), possibly with ES-04 secondary on weak returns.

**Why:** Long first-pass retention risk dominates.

### V3 — Strong coverage, weak question performance

**Profile sketch:** S4; D2 advanced; D4 weak; D15 rising need.

**Selection:** ES-06 Weak Topic Reinforcement or ES-04 Practice Intensive.

**Why:** Coverage without application evidence — deepen, don’t march onward blindly.

### V4 — Returned after three-month break

**Profile sketch:** S8 → S7; D12 active; D5 resetting; D2 persists.

**Selection:** ES-08 Recovery Strategy.

**Why:** Cadence and re-orientation first; not immediate Exam Rescue unless D7/D18 force L1.

### V5 — Six weeks out, large remainder, At Risk

**Profile sketch:** S9 overlay on S6; D7 short; D2 large remainder; D18 high.

**Selection:** ES-09 Exam Rescue.

**Why:** Feasibility truth; triage; freeze expansion fiction.

### V6 — Registered late with 10 hours/week

**Profile sketch:** S1; D2 near zero; D7 short for full syllabus; D6 limited.

**Selection:** ES-10 Late Starter Strategy.

**Why:** Compression honesty from the start — not Steady Progression theatre.

### V7 — Provisional Exam Ready, stable habits

**Profile sketch:** S10; strong D8/D15; calm D18.

**Selection:** ES-12 Balanced Maintenance (or ES-11 if mocks still need polish).

**Why:** Protect readiness; avoid upheaval.

---

## 11. Relationship to Planning

Once primary strategy is selected:

1. Planning (MS001) designs phases, sequence, intensity, revision, and mocks **under that strategy’s bias**.
2. Planning Constraints still veto unlawful designs even if strategy “wants” more coverage.
3. Replan events must **re-consult** Profile and **re-select** strategy (see `STRATEGY_TRANSITIONS.md`).
4. Daily missions remain under constitutional mode authority — strategy does not silently hijack Current Learning Topic.

---

## 12. Non-Goals

This Model does **not**:

- define numeric thresholds, scores, or ML classifiers;
- implement selection code;
- generate plans;
- map one-to-one Profile state → strategy as a rigid enum machine.

Educational judgement remains multi-dimensional; the lenses above discipline that judgement.

---

## 13. Cross References

- `STRATEGY_CATALOGUE.md` — meanings selected among
- `STRATEGY_TRANSITIONS.md` — when selection must run again
- `STRATEGY_EXPLAINABILITY.md` — how to speak the choice
- `../student_profile/PROFILE_EVOLUTION.md` — diagnosis change that triggers reselection
- `../planning/PLANNING_DECISION_MODEL.md` — planning decisions strategy will bias
