# Planning Assumptions

**Programme:** VI — Master Planner  
**Milestone:** MS001 — Educational Planning Model  
**Classification:** Explicit assumptions for educational planning reasoning  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document records **assumptions** Master Planner reasoning may rely on, and **non-assumptions** it must never treat as true.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_PLANNING_MODEL.md`
3. `PLANNING_CONSTRAINTS.md`

When an assumption is violated in reality, algorithms must degrade safely (understate, replan, request inputs) — not silently continue as if the assumption still holds.

---

## 1. Purpose

Expert tutors always plan under assumptions. Bad systems hide them. Kwalitec names them.

Clear assumptions:

- make feasibility judgements honest;
- prevent overclaiming;
- tell implementers when to ask for more input;
- protect educational truth when students behave differently than hoped.

---

## 2. Core Operating Assumptions

### A1 — Student follows missions honestly

**Assumption.** When the student marks study complete or records practice outcomes, they do so in good faith.

**Educational consequence.** Study Progress remains a coverage declaration system worthy of trust as *coverage*, not as proof of mastery.

**If violated.** Evidence systems may later contradict confidence estimates; plans must still not equate coverage with mastery. Integrity issues are evidence problems — not licence to invent surveillance theatre in planning docs.

### A2 — Study time estimates are reasonably accurate

**Assumption.** Declared weekly hours and study-day patterns are close enough to reality for capacity planning.

**Educational consequence.** Intensity bands and feasibility judgements are meaningful.

**If violated.** Missed weeks trigger recovery decisions (D18); repeated violation should prompt re-intake of capacity inputs rather than endless heroic compression.

### A3 — CMP (or equivalent official materials) remains the learning resource

**Assumption.** The student studies from lawful course materials (e.g. IFoA CMP / approved notes). Kwalitec coaches sequencing and practice honesty; it does not replace those materials.

**Educational consequence.** Plans allocate time for studying materials + practice, not for consuming generated textbook substitutes.

**If violated.** Planning cannot invent content to fill the gap; it may only note that materials access is a student responsibility outside plan generation.

### A4 — Question practice reflects actual understanding provisionally

**Assumption.** Practice attempts are honest attempts under the conditions the student records, and therefore may inform **estimates** of knowledge/competence.

**Educational consequence.** Adaptive revision emphasis may use practice evidence as warrant for estimates.

**If violated / thin history.** Estimates must be understated or withheld; cold-start diagnosis is forbidden (F6).

### A5 — Official syllabus is complete and authoritative for the subject

**Assumption.** For supported subjects, bundled official syllabus structure is the educational spine for sequencing.

**Educational consequence.** Prerequisite and ordering decisions are lawful.

**If violated (unsupported / incomplete subject).** Complete plans must not be issued (C9, F14).

### A6 — Examination date is fixed for the plan horizon

**Assumption.** The chosen sitting date is the true target unless the student explicitly changes it.

**Educational consequence.** Backward reservation of revision and feasibility maths are stable.

**If violated (date change).** Plan must be re-anchored; old capacity maths is void.

### A7 — Learner educational history persists across plan containers

**Assumption.** Study Progress, attempts, and evidence posture belong to the learner and survive plan dispose/replace unless an explicit informed reset occurs.

**Educational consequence.** Starting coverage position (D3) and continuity constraints (C16) hold.

### A8 — Deterministic cores are acceptable to the student

**Assumption.** Students prefer reproducible, explainable plans over randomised “surprise” schedules.

**Educational consequence.** Determinism constraints (C19) are educationally aligned with product thesis.

---

## 3. Soft Defaults (Cold Start)

When enriching inputs are missing, planning may use **cautious defaults**. Defaults are assumptions, must be disclosed when material, and must bias toward safety.

| Missing input | Cautious default posture |
|---------------|--------------------------|
| Strengths/weaknesses | No diagnostic emphasis; uniform revision policy until evidence exists |
| Previous attempts | Treat as first attempt; still protect revision |
| Preferences | Neutral session shape within sustainable band |
| Planned leave | Assume none; encourage disclosure; keep modest buffers if horizon allows |
| Burnout history | Prefer lower intensity within band |
| Mock preferences | Place mocks only when coverage + recovery windows exist; otherwise omit rather than force |

Cold-start defaults must never become confident personalisation theatre.

---

## 4. Non-Assumptions (Must Never Be Assumed)

| ID | Forbidden assumption | Why |
|----|----------------------|-----|
| N1 | Completing the plan guarantees a pass | Readiness is estimated; exams have irreducible uncertainty |
| N2 | Completing a topic means mastery | Constitutional coverage ≠ mastery |
| N3 | Students have unlimited catch-up capacity | Violates burnout and feasibility law |
| N4 | Missed days should be punished with overload | Forbidden decision F9 |
| N5 | Opaque optimiser output is self-justifying | Explainability is mandatory |
| N6 | Kwalitec materials replace CMP | Product/educational boundary |
| N7 | All subjects are supported | Supported-subject integrity |
| N8 | V1 and V2 curricula behave identically in weighting | Traversal is shared; weighting semantics differ — planners must use curriculum helpers, not flat assumptions |
| N9 | Advisory intelligence may silently override Learning Mode | Constitutionally forbidden without disclosure/mode authority |
| N10 | Thin practice history supports strong weak-area claims | Evidence before diagnosis |
| N11 | Plan deletion resets the learner | Continuity Standard |
| N12 | Studying after the exam date still counts for this sitting | C12 / F13 |

---

## 5. Assumption Dependency By Decision

| Decision area | Relies on | Breaks if |
|---------------|-----------|-----------|
| Capacity envelope | A2, A6 | Hours/date wrong → re-intake |
| Sequencing | A5 | Unsupported subject → refuse complete plan |
| Revision emphasis | A4 (when adaptive) | Thin evidence → uniform/cautious policy |
| Intensity | A2, A1 (adherence) | Chronic miss → recovery, not punishment |
| Feasibility | A2, A5, A6 | Any break → recompute and disclose |
| Materials time | A3 | No materials → cannot invent content |

---

## 6. Honesty Rules When Assumptions Fail

1. **Detect** when possible (missed capacity, date change, empty evidence).
2. **Disclose** in plain language that the plan premise changed.
3. **Replan** using Decision Model recovery options (D18) and feasibility (D8).
4. **Understate** readiness and diagnosis until warrant returns.
5. **Never** paper over failure with denser impossible schedules.

---

## 7. Cross References

- `PLANNING_DECISION_MODEL.md` — decisions that consume these assumptions
- `PLANNING_CONSTRAINTS.md` — hard stops when assumptions would cause violations
- `PLANNING_EXPLAINABILITY.md` — how to narrate defaults and assumption breaks
- `../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` — why A4 never upgrades to mastery fiat
