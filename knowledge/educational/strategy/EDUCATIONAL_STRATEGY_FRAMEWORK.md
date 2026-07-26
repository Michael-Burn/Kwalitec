# Educational Strategy Framework

**Programme:** VI — Master Planner  
**Milestone:** MS003 — Educational Strategy Framework  
**Classification:** Highest educational strategy authority within Programme VI  
**Status:** APPROVED — governing for educational strategy reasoning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of **educational strategy** for Kwalitec.

It is subordinate to the Educational Constitution and specialised educational models. It governs **how an expert IFoA tutor chooses an overall educational approach** before constructing a long-term study plan. It does not authorise implementation shortcuts that contradict the Constitution.

Authority order for Master Planner personalisation:

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Evidence Model defines what may warrant understanding claims.  
> **Student Educational Profile (MS002)** diagnoses *who the student is educationally now*.  
> **This Framework (MS003)** chooses *which overall educational strategy to adopt*.  
> **Educational Planning Model (MS001)** designs *how the journey is constructed* under that strategy.  
> **Planning Decision Engine (MS004)** produces *structured planning decisions* before any timetable.  
> Future planning algorithms must determine strategy and produce planning decisions before generating any study plan — never invent strategy or decision meaning in code.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabuses such as CM1/CS1 and peers).

An expert IFoA tutor does not jump from diagnosis straight into a calendar. After understanding the student, the tutor first answers:

1. What is the overall educational approach for this sitting?
2. Why is that approach the honest choice now?
3. What would make us change approach later?

That middle judgement is **educational strategy**.

> **Educational strategy is the bridge between diagnosis and planning.  
> It is not a study plan, not a schedule, and not a database schema.**

This Framework records that tutor posture so every future Master Planner algorithm has a single educational reference for *how to approach this student before constructing any plan*.

---

## 2. What Educational Strategy Is

**Educational strategy** is the named overall educational approach adopted for a student on a named examination sitting, chosen from the Student Educational Profile, and used to constrain how the Educational Planning Model designs the journey.

It answers:

| Question | Educational answer |
|----------|-------------------|
| What approach are we taking? | Named strategy from the Strategy Catalogue |
| Why this approach? | Educational reasoning tied to Profile dimensions and states |
| What does it privilege? | Coverage, practice, revision, recovery, rescue, optimisation, etc. |
| What does it refuse? | Approaches that would be dishonest given the Profile |
| When does it change? | Transition triggers in `STRATEGY_TRANSITIONS.md` |

Educational strategy is:

- **approach-level** — one primary strategy dominates the journey posture at a time;
- **profile-derived** — selected from diagnosis, not from arbitrary product modes;
- **planner-binding** — planning must honour the selected strategy’s educational intent;
- **temporal** — may change when the Profile evolves;
- **explainable** — speakable in plain educational language to the student.

Educational strategy is **not**:

- a generated study plan or weekly timetable;
- a Learning Mode / Revision Mode switch (those are constitutional modes; strategy may *prefer* postures consistent with them);
- a black-box optimiser label or engagement gimmick;
- a personality type or permanent student brand;
- a claim that following the strategy guarantees a pass.

---

## 3. Tutor Posture (Binding Metaphor)

When choosing strategy, the system must behave as an expert IFoA tutor would:

1. **Diagnose before directing.** Strategy follows Profile — never invents the student.
2. **Name one primary approach.** Students need a clear educational story, not competing strategies.
3. **Match approach to educational need.** Foundation gaps get foundations; rescue gets rescue; recovery gets recovery.
4. **Prefer sustainable intensity.** Heroic catch-up theatre is not a strategy when capacity cannot sustain it.
5. **Protect revision when the horizon demands it.** Late first-pass expansion that consumes revision is unlawful under Planning Constraints even if a strategy wants more coverage.
6. **Separate coverage from competence.** Practice-intensive and revision-intensive strategies never mint mastery from coverage alone.
7. **Honour recovery without shame.** Interruptions change strategy; they do not erase lawful Study Progress.
8. **Explain the approach.** The student should understand *why Kwalitec has adopted this educational strategy*.
9. **Change when the educational picture changes.** Strategy stickiness must not outlive its warrant.

---

## 4. Position in the Master Planner Stack

```
STUDENT EDUCATIONAL PROFILE (MS002)
     ↓  diagnosis: where the student is now
EDUCATIONAL STRATEGY (MS003 — this Framework)
     ↓  approach: how we should teach / coach this sitting
EDUCATIONAL PLANNING MODEL (MS001)
     ↓  design law: phases, sequence, capacity, revision, mocks
PLANNING DECISION ENGINE (MS004)
     ↓  structured educational decisions
FUTURE PLAN GENERATION
     (out of scope for MS003)
```

| Horizon | Job | Question |
|---------|-----|----------|
| **MS002 — Profile** | Diagnose | Who is this student educationally? |
| **MS003 — Strategy** | Choose approach | Which overall educational strategy should we adopt? |
| **MS001 — Planning** | Define design law | How should the long-term plan be constructed under that strategy? |
| **MS004 — Decision Engine** | Decide | What planning decisions follow before any timetable? |

Binding rule for future algorithms:

> **Determine educational strategy and produce planning decisions before generating any study plan.**  
> Plans that skip strategy or decisions invent approach meaning in scheduling code.

---

## 5. Relationship to Profile States and Planning Phases

These three vocabularies must not be collapsed:

| Vocabulary | Object | Example |
|------------|--------|---------|
| Profile state (MS002) | Diagnostic posture | Building Foundation; Recovering; At Risk |
| Educational strategy (MS003) | Chosen approach | Foundation Building; Recovery Strategy; Exam Rescue |
| Planning phase (MS001) | Journey design segment | Foundation & First-Pass; Protected Revision; Recovery / Replan |

**Alignment guidance (not identity):**

- Profile state *informs* strategy selection.
- Strategy *biases* which planning phases dominate and how adaptive decisions lean.
- Planning phases *implement* the strategy within permanent constraints.

A student in **Building Foundation** commonly maps to **Foundation Building** or **Steady Progression**.  
A student in **Recovering** commonly maps to **Recovery Strategy**.  
A student in **At Risk** near the sitting may map to **Exam Rescue** or **Late Starter Strategy** — depending on whether the crisis is late-horizon feasibility or late start from the beginning.

Alignment is educational guidance. Selection rules live in `STRATEGY_SELECTION_MODEL.md`.

---

## 6. Strategy Structure

The Strategy Framework is composed of five specification layers:

```
STRATEGY CATALOGUE
     ↓  (named educational approaches + meaning)
STRATEGY SELECTION MODEL
     ↓  (how Profile → primary strategy)
STRATEGY TRANSITIONS
     ↓  (when and why strategy changes)
STRATEGY EXPLAINABILITY
     (how the chosen strategy is spoken to the student)
```

| Layer | Document | Educational job |
|-------|----------|-----------------|
| Overview | `EDUCATIONAL_STRATEGY_FRAMEWORK.md` | Constitutional meaning and authority |
| Catalogue | `STRATEGY_CATALOGUE.md` | Named strategies and tutor rationale |
| Selection | `STRATEGY_SELECTION_MODEL.md` | Profile-driven choice reasoning |
| Transitions | `STRATEGY_TRANSITIONS.md` | Lawful strategy succession |
| Explainability | `STRATEGY_EXPLAINABILITY.md` | Plain-language justification |

No algorithm may invent a student-facing strategy name absent from the Catalogue without amending this corpus first.

---

## 7. Primary Strategy Rule

At any educational moment for a named examination sitting, Kwalitec adopts **exactly one primary educational strategy**.

Secondary colouring is allowed (e.g. Steady Progression with Weak Topic Reinforcement emphasis) only when:

1. the primary strategy remains clear in student explanation; and
2. the secondary emphasis does not contradict permanent planning constraints; and
3. explainability names the primary reason first.

Forbidden:

- simultaneous equal “primary” strategies that confuse the student;
- strategy labels used as UI cosmetics without educational meaning;
- swapping strategy every session without Profile warrant (churn theatre).

---

## 8. First Principles for IFoA Educational Strategy

IFoA preparation has distinctive educational properties that shape lawful strategies:

1. **Long syllabuses** — first-pass without consolidation risks late amnesia → consolidation and revision strategies are first-class.
2. **Prerequisite structure** — later topics depend on earlier foundations → foundation and reinforcement strategies outrank topic-shopping.
3. **Application-heavy assessment** — coverage without practice is incomplete → practice-intensive strategy exists as a deliberate posture.
4. **Finite sitting horizon** — calendar binds honesty → late-starter and exam-rescue strategies exist because time pressure is educationally real.
5. **Life interruptions** — working candidates pause → recovery and confidence restoration are educational strategies, not character judgements.
6. **Retakes happen** — previous attempts change risk posture → strategy may emphasise revision, weak topics, or rescue without erasing prior coverage.
7. **Bring-your-own materials** — strategy chooses educational posture and emphasis; it does not invent CMP content.

These principles justify the Catalogue. They are not scoring weights.

---

## 9. Strategy Decision Classes

Every strategy behaviour belongs to exactly one class:

| Class | Meaning | Examples |
|-------|---------|----------|
| **Mandatory** | Required whenever a complete strategy is published for planning | One primary strategy; Profile consultation; explainability; constraint respect |
| **Adaptive** | May vary with Profile evidence and horizon | Which Catalogue strategy; secondary emphasis; transition timing |
| **Forbidden** | Must never be produced | Strategy without Profile; pass-guarantee strategies; coverage-as-mastery strategies; silent strategy churn; strategies that order prerequisite violation |

Detail of selection reasoning: [`STRATEGY_SELECTION_MODEL.md`](STRATEGY_SELECTION_MODEL.md).

---

## 10. What Strategy Must Optimise

Strategy selection serves Planning Objectives (MS001), filtered through honest diagnosis:

1. **Honest exam readiness** under the student’s real capacity and time.
2. **Retention protection** when first-pass length threatens decay.
3. **Consistency and burnout prevention** when intensity or reliability is fragile.
4. **Revision capacity** when the horizon requires consolidation over expansion.
5. **Truthfulness** — understate when evidence is thin; never strategy theatre.

When objectives conflict, Planning Objectives conflict order still binds. Strategy may *prefer* an approach; it may not authorise unlawful plans.

---

## 11. Determinism and Reproducibility

Core strategy judgements must be reproducible from the same Profile inputs.

Binding rules:

1. Same Profile skeleton (dimensions + primary state + material overlays) → same primary strategy.
2. Opaque random “variety” in strategy choice is forbidden.
3. Soft signals (motivation, felt confidence) may colour Confidence Restoration or Recovery — they must not silently override hard feasibility and coverage facts.
4. When selection cannot be made safely (Intake Incomplete), publish no complete planning strategy — gather facts first.
5. When torn between two strategies, prefer the one that **understates readiness** and **protects foundations / revision**.

---

## 12. Explainability Obligation

Every selected primary strategy must be explainable in plain educational language per [`STRATEGY_EXPLAINABILITY.md`](STRATEGY_EXPLAINABILITY.md) and the Educational Explainability Standard.

Minimum student-facing answers:

1. What educational strategy are we following?
2. Why is this the right approach for you now?
3. What does this mean for how your plan will feel?
4. What is known vs estimated in that choice?
5. What would make us change approach? (when material)

Internal machinery (scores, twin facets, optimiser labels) must remain invisible.

---

## 13. Non-Goals of This Milestone

MS003 deliberately does **not**:

- implement strategy selection algorithms or scoring;
- generate or rebalance study plans;
- define SQL schemas, feature flags, or Runtime A services;
- redesign missions, recommendations, or Digital Twin;
- schedule study days or invent optimisation mathematics;
- collect intake data in product UI.

Those belong to later Master Planner milestones, which must cite this Framework as educational law for strategy.

---

## 14. Success Test for Future Algorithms

A Master Planner algorithm is educationally compliant with this Framework when:

1. It determines a Catalogue strategy from the Student Educational Profile **before** generating any study plan.
2. It never invents strategy names or meanings absent from this corpus.
3. It preserves Study Progress ≠ Estimated Knowledge ≠ Estimated Mastery while applying strategy.
4. It transitions strategy only under documented educational triggers.
5. Every material strategy choice is explainable without revealing internal machinery.
6. It never equates “strategy selected” with “exam ready” or “pass likely.”
7. It degrades safely when the Profile is incomplete or thin — understate, request inputs, no confident strategy theatre.

If any test fails, the algorithm is out of compliance — even if the resulting calendar looks complete.

---

## 15. Cross References

| Document | Relationship |
|----------|----------------|
| [`STRATEGY_CATALOGUE.md`](STRATEGY_CATALOGUE.md) | Named educational strategies |
| [`STRATEGY_SELECTION_MODEL.md`](STRATEGY_SELECTION_MODEL.md) | Profile → strategy reasoning |
| [`STRATEGY_TRANSITIONS.md`](STRATEGY_TRANSITIONS.md) | When strategy changes |
| [`STRATEGY_EXPLAINABILITY.md`](STRATEGY_EXPLAINABILITY.md) | Student-facing strategy speech |
| [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) | Diagnosis consumed by strategy |
| [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) | Planning consumes strategy |
| [`../KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) | Highest educational authority |
| [`../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) | Truth ladder |
| [`../EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) | Platform speech law |
