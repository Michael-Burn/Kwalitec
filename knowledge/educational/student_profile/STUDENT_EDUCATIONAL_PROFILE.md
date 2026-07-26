# Student Educational Profile

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Canonical educational diagnosis of a student’s academic state  
**Status:** APPROVED — governing for educational profile reasoning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document is the constitutional overview of the **Student Educational Profile** for Kwalitec.

It is subordinate to the Educational Constitution and specialised educational models. It governs **educational diagnosis** for Master Planner work. It does not authorise implementation shortcuts that contradict the Constitution.

Authority order for educational diagnosis before long-term planning:

> Constitution defines educational truth and curriculum primacy.  
> Knowledge & Mastery defines coverage ≠ understanding ≠ mastery.  
> Evidence Model defines what may warrant understanding claims.  
> **This Profile defines what the tutor must understand about the student *before* choosing strategy or designing the journey.**  
> Educational Strategy Framework (MS003) chooses which overall approach to adopt from this Profile.  
> Planning Model (MS001) defines how an expert tutor designs the journey under that strategy.  
> Planning Decision Engine (MS004) transforms Profile + Strategy + Planning Model into structured planning decisions.  
> Future planning algorithms must consume this Profile — never redefine diagnosis in code.

---

## 1. Purpose

Kwalitec coaches students preparing for demanding professional examinations (especially IFoA syllabuses such as CM1/CS1 and peers).

An expert IFoA tutor does not open a calendar and invent a schedule. The tutor first forms a coherent picture of the student:

1. What has already been studied — honestly?
2. What understanding is supported by evidence — provisionally?
3. How much time and energy remain before the sitting?
4. How reliable has study behaviour been so far?
5. What risks, recoveries, and previous attempts colour the journey?
6. How ready is the student educationally — without readiness theatre?

This Profile records that diagnostic posture so every future planning algorithm has a single educational reference for *who the student is academically right now*.

> **The Student Educational Profile is educational diagnosis.  
> It is not a study plan, not a recommendation, and not a database schema.**

---

## 2. What the Student Educational Profile Is

The **Student Educational Profile** is the complete educational description of a student’s current academic state for a named examination (or concurrent examination context), assembled from lawful inputs so that long-term planning can personalise without guessing.

It answers:

| Question | Educational answer |
|----------|-------------------|
| Who is this learner educationally? | Coverage, evidence posture, consistency, capacity, history |
| Where are they on the journey? | Named educational state (see `PROFILE_STATES.md`) |
| What is known vs estimated? | Facts, derived measures, and provisional beliefs — kept distinct |
| What must the planner respect? | Capacity, remaining time, prior attempts, recovery posture |
| What must the planner not invent? | Mastery from coverage; certainty from thin history; hidden motives |

The Profile is:

- **diagnostic** — describes educational reality as Kwalitec may lawfully claim it;
- **compositional** — built from dimensions, not a single opaque score;
- **temporal** — evolves as the student studies, practises, revises, pauses, and recovers;
- **explainable** — every material state claim can be spoken in plain language;
- **planner-consumable** — sufficient for Master Planner personalisation without additional invented diagnosis.

The Profile is **not**:

- a personality quiz or psychometric instrument;
- a black-box readiness percentage that hides its inputs;
- a substitute for official CMP / course materials;
- a plan, mission, or daily recommendation;
- a claim that finishing topics equals exam readiness.

---

## 3. Tutor Posture (Binding Metaphor)

When forming the Profile, the system must behave as an expert IFoA tutor would before recommending strategy:

1. **Ask where the student is starting from.** Coverage and prior attempts before optimism.
2. **Separate coverage from competence.** Studying advances Study Progress; practice informs estimates; neither invents mastery.
3. **Look at behaviour, not only intention.** Consistency and planning reliability matter as much as declared hours.
4. **Respect the calendar.** Available time and time remaining bound every honest diagnosis of feasibility posture.
5. **Name uncertainty.** Thin history produces cautious profiles — never confident theatre.
6. **Honour recovery.** Interruptions and returns are educational states, not character judgements.
7. **Keep soft signals soft.** Motivation and felt confidence inform coaching tone; they do not author understanding claims.
8. **Explain the diagnosis.** The student should understand *why Kwalitec believes they are in this educational state*.

---

## 4. Profile Structure

The Profile is composed of five specification layers:

```
PROFILE INPUTS
     ↓  (lawful observations, declarations, derived facts)
PROFILE DIMENSIONS
     ↓  (multi-axis educational understanding)
PROFILE STATES
     ↓  (named educational posture for the journey)
PROFILE EVOLUTION
     ↓  (how diagnosis changes over time)
PROFILE EXPLAINABILITY
     (how the diagnosis is spoken to the student)
```

| Layer | Document | Educational job |
|-------|----------|-----------------|
| Inputs | `PROFILE_INPUTS.md` | Where evidence and declarations come from |
| Dimensions | `PROFILE_DIMENSIONS.md` | What axes the tutor must understand |
| States | `PROFILE_STATES.md` | Named educational postures with meaning |
| Evolution | `PROFILE_EVOLUTION.md` | How growth, stall, and recovery rewrite the profile |
| Explainability | `PROFILE_EXPLAINABILITY.md` | Plain-language justification of diagnosis |

No single dimension is the Profile. Algorithms that collapse the Profile into one score for student-facing diagnosis violate this Model.

---

## 5. Scope of Diagnosis

### 5.1 In scope

- Current syllabus coverage posture (Study Progress / Learning Progress context)
- Demonstrated understanding posture (evidence-backed estimates where warranted)
- Question / practice performance posture
- Consistency of study behaviour over time
- Available study capacity and remaining calendar horizon
- Revision maturity and exam-approach posture
- Previous examination attempts and educational aftermath
- Educational confidence (platform warrant) distinct from felt confidence
- Motivation and engagement soft posture
- Recovery history and returning-after-break context
- Planning reliability (adherence vs declared capacity)
- Concurrent subjects / competing demands when declared
- Feasibility risk signals that diagnosis must surface before planning

### 5.2 Explicitly out of scope for this milestone

- Generating or rebalancing a study plan
- Choosing today’s mission or session tasks
- Scoring mathematics, ML models, or optimisation
- Database fields, APIs, or Runtime A wiring
- Collecting inputs in product UI (requirement is educational; collection is later)

---

## 6. Relationship to Educational Truth Ladder

The Profile must preserve constitutional separations:

| Concept | Profile role |
|---------|----------------|
| **Study Progress** | Coverage dimension — what has been studied |
| **Knowledge (Estimated)** | Understanding dimension — provisional, evidence-warranted |
| **Competence** | Application posture where evidence supports it — not Version 1 student mastery theatre |
| **Mastery (Estimated)** | Long-horizon durability claim — only when warrant exists; never implied by coverage |
| **Educational Guidance** | Consumes the Profile later — does not author it |

Binding rule:

> Completing studying never implies Knowledge.  
> Having Knowledge never implies Competence.  
> Having Competence never implies Mastery.  
> The Profile narrates each rung honestly — or stays silent.

---

## 7. Relationship to Long-Term Planning

Master Planner algorithms (governed by MS001 + MS003) must:

1. **Consult** the Student Educational Profile as the starting educational truth for personalisation.
2. **Determine educational strategy** (MS003) from this Profile before generating any study plan.
3. **Not invent** dimensions or states absent from this corpus.
4. **Degrade safely** when dimensions are thin (understate, request inputs, cautious defaults per Planning Assumptions).
5. **Re-consult** the Profile after material evolution (missed weeks, recovery, new evidence, date change).
6. **Explain diagnosis** using profile explainability, **explain strategy** using strategy explainability, and **explain plans** using planning explainability — without collapsing the three.

Diagnosis answers: *Who is this student educationally?*  
Strategy answers: *Given that, which overall educational approach should we adopt?*  
Planning answers: *Given diagnosis and strategy, how should the journey be designed?*

---

## 8. Cold Start and Sparse History

Cold-start and sparse-history students still have a Profile — a **cautious** one.

Rules:

1. Missing mandatory planning inputs (exam, date, capacity, coverage) yield an incomplete diagnostic envelope — planning must not pretend completeness (MS001 §5).
2. Absent practice evidence yields coverage narration without understanding certainty.
3. Soft signals alone never mint high educational confidence.
4. Default assumptions (Planning Assumptions) may fill *planning* gaps; they must be labelled as assumptions, not observed facts, when reflected in profile speech.
5. Silence beats invented readiness.

---

## 9. Determinism and Reproducibility

Core diagnostic judgements that name educational state must be reproducible from the same lawful inputs.

Binding rules:

1. Same inputs → same Profile skeleton (dimensions + state posture).
2. Opaque random “variety” in diagnosis is forbidden.
3. Soft dimensions (motivation, felt confidence) may be provisional and time-local — but must not silently rewrite hard dimensions (coverage, evidence, calendar).
4. When diagnosis cannot be made safely, the Profile understates and marks uncertainty rather than inventing a confident state.

---

## 10. Non-Goals of This Milestone

MS002 deliberately does **not**:

- implement profile storage or Twin projection code;
- define SQL schemas or feature flags;
- specify scoring or state-machine mathematics;
- redesign missions, recommendations, or Digital Twin algorithms;
- collect intake data in product UI;
- generate long-term plans.

Those belong to later milestones, which must cite this Profile as educational law for diagnosis.

---

## 11. Success Test for Future Algorithms

A Master Planner (or related) algorithm is educationally compliant with this Profile when:

1. It personalises long-term plans by consulting documented dimensions and states — not invented proxies.
2. It preserves Study Progress ≠ Estimated Knowledge ≠ Estimated Mastery.
3. It consumes only lawful inputs (or declared safe defaults labelled as such).
4. It treats soft signals as soft.
5. It re-evaluates diagnosis when evolution events change the educational picture.
6. Every material profile claim is explainable without revealing internal machinery.
7. It never equates “profile complete” with “exam ready.”

---

## 12. Cross References

| Document | Relationship |
|----------|----------------|
| `PROFILE_DIMENSIONS.md` | Axis catalogue |
| `PROFILE_INPUTS.md` | Evidence and declaration origins |
| `PROFILE_STATES.md` | Named educational postures |
| `PROFILE_EVOLUTION.md` | Temporal succession |
| `PROFILE_EXPLAINABILITY.md` | Student-facing diagnosis speech |
| [`../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`](../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md) | Strategy selection consumes this Profile (MS003) |
| [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) | Planning consumes strategy + this Profile (MS001) |
| [`../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) | Truth ladder |
| [`../EDUCATIONAL_EVIDENCE_MODEL.md`](../EDUCATIONAL_EVIDENCE_MODEL.md) | Warrant for understanding |
| [`../EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`](../EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md) | Broader state succession |
| [`../EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) | Platform speech law |
