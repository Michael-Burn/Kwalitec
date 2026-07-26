# Decision Pipeline

**Programme:** VI — Master Planner  
**Milestone:** MS004 — Planning Decision Engine  
**Classification:** Educational reasoning sequence and planning-decision catalogue  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **complete educational reasoning sequence** by which the Planning Decision Engine transforms Profile + Strategy + Planning Model into a Planning Decision Package.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `PLANNING_DECISION_ENGINE.md`
3. `../planning/EDUCATIONAL_PLANNING_MODEL.md`
4. `../planning/PLANNING_DECISION_MODEL.md`
5. `../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`
6. `../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`

This document defines **educational reasoning**. It does not define software classes, services, or algorithms.

---

## 1. Purpose

An expert IFoA tutor reasons in a stable order. Later packing must not quietly undo earlier educational law.

This Pipeline records that order so future plan-generation algorithms preserve educational causality:

> Diagnose → Choose approach → Fix design law → Decide → Only then schedule.

---

## 2. Complete Reasoning Sequence

```
Student Educational Profile
        ↓
Educational Strategy Selection
        ↓
Planning Objectives (under Strategy)
        ↓
Constraint Evaluation
        ↓
Educational Decisions
        ↓
Planning Decision Package
```

### Stage A — Student Educational Profile

**Educational job:** Establish who the student is academically now for this sitting.

**Tutor questions:** What coverage is honest? What evidence warrants understanding claims? How much capacity and runway remain? What consistency, recovery, attempt history, and educational state colour the journey?

**Exit condition:** A lawful Profile snapshot exists (or declared safe defaults are explicit and understated). Without diagnosis, no downstream decision is educationally authorised.

**Must not:** Invent cold-start weakness/mastery; collapse coverage into readiness.

---

### Stage B — Educational Strategy Selection

**Educational job:** Choose one primary overall educational approach from the Strategy Catalogue.

**Tutor questions:** Given this Profile, should we build foundations, progress steadily, deepen practice, revise intensively, recover, rescue, start late honestly, optimise, or maintain?

**Exit condition:** One primary strategy (ES-XX) with student-speakable rationale. Strategy refuses and privileges are binding on later adaptive decisions.

**Must not:** Skip strategy and invent approach inside scheduling; run competing primary strategies at once.

Authority: MS003 (`STRATEGY_SELECTION_MODEL.md`).

---

### Stage C — Planning Objectives (under Strategy)

**Educational job:** Name what this decision package must optimise educationally, biased by strategy but still bound by Planning Objectives O1–O13.

**Tutor questions:** Under this strategy, what does honest exam readiness require now? Which supporting objectives (retention, consistency, revision protection, recovery, earned confidence, realism) are especially live?

**Exit condition:** An explicit objective posture — what success means for *this* package — without numeric weights.

**Examples of strategy colouring (not redefinition):**

| Strategy family | Objective colouring |
|-----------------|---------------------|
| Build (ES-01, ES-02) | Coverage honesty + sustainable consistency dominate daily posture |
| Deepen (ES-03, ES-04, ES-06) | Retention and evidenced application rise in emphasis |
| Approach (ES-05, ES-11, ES-12) | Revision protection + exam craft + stability dominate |
| Restore (ES-07, ES-08) | Recovery + burnout prevention + earned confidence outrank acceleration |
| Triage (ES-09, ES-10) | Feasibility honesty + revision minima outrank full leisurely syllabus fiction |

Authority: MS001 `PLANNING_OBJECTIVES.md`; priority when objectives conflict: `DECISION_PRIORITY_MODEL.md`.

---

### Stage D — Constraint Evaluation

**Educational job:** Identify hard educational bounds that no decision may violate.

**Tutor questions:** What capacity is usable? Which leave and study-day patterns bind? Are prerequisites and supported-subject integrity intact? Is protected revision still non-negotiable? Where would an impossible load appear?

**Exit condition:** Constraints that are active for this student/sitting are named. Any path that would violate them is marked unlawful *before* adaptive decisions are set.

**Must not:** Soften hard constraints because strategy is ambitious; treat preferences as constraints.

Authority: MS001 `PLANNING_CONSTRAINTS.md`.

---

### Stage E — Educational Decisions

**Educational job:** Settle mandatory and adaptive planning decisions in lawful order (see §3).

**Tutor questions:** What sequencing? What intensity band? How much revision reservation? What buffers, recovery, practice intensity, milestones, risk mitigation, confidence protection?

**Exit condition:** Every mandatory decision is made; adaptive decisions are set within bounds; forbidden decisions are absent.

---

### Stage F — Planning Decision Package

**Educational job:** Assemble decisions into one coherent, explainable, traceable package.

**Tutor questions:** Do all decisions tell one educational story under the chosen strategy? Can each material decision be explained to the student? Is feasibility explicit?

**Exit condition:** Package ready for future plan generation — still not a timetable.

---

## 3. Decision Order Within Stage E

Educational order an expert tutor follows when settling decisions. Algorithms must preserve this causality.

```
1. Anchor examination & sitting
2. Establish capacity envelope & leave posture
3. Reserve revision window (and mock/recovery scaffolding intent)
4. Determine starting coverage position
5. Fix topic sequencing policy
6. Judge feasibility → if fail, decide triage / trade-off / sitting counsel; do not pack fantasy
7. Set sustainable intensity band & study intensity posture
8. Set practice intensity, consolidation / retention posture
9. Allocate buffers & recovery allowance
10. Position milestones; set mock timing intent when warranted
11. Set risk mitigation & confidence protection postures
12. Attach explainability & traceability
13. Only then allow preference fit within remaining lawful room
```

**Unlawful:** Packing first-pass ambition before steps 3 and 6.

This order specialises the MS001 Decision Map for engine use. It does not redefine decision meanings.

---

## 4. Planning Decisions Catalogue (Engine View)

Each decision below exists as an educational judgement. Future algorithms may implement them; they may not invent parallel meanings.

Where an MS001 Decision Model ID applies, it is cited. Engine identifiers (PD-XX) name the decision for pipeline and explainability traceability.

For each decision:

- **Why it exists**
- **When it applies**
- **What educational objective it supports**
- **Traceability** (Profile / Strategy / Planning Model)

---

### PD-01 — Topic sequencing

| Aspect | Specification |
|--------|----------------|
| **What** | Establish the ordered first-pass learning sequence from official curriculum traversal and prerequisites |
| **Why it exists** | IFoA learning is cumulative; foundations enable later topics; random reordering is engagement theatre, not education |
| **When it applies** | Every complete package (mandatory). Adaptive modulation of *pace* never silently replaces *order* |
| **Objective supported** | O1 honest readiness; O9 prerequisite clarity; curriculum primacy |
| **Traceability** | Profile: coverage position & mode posture. Strategy: Build/Deepen refuse skip-ahead. Planning Model: D2, C6–C8 |
| **MS001** | D2 |

---

### PD-02 — Starting coverage position

| Aspect | Specification |
|--------|----------------|
| **What** | Begin first-pass allocation from lawful current syllabus progress — do not re-teach completed coverage as if new without educational reason |
| **Why it exists** | Continuity respects honest prior work; erasing history destroys trust |
| **When it applies** | Every complete package; especially after replan, recovery, or strategy transition |
| **Objective supported** | O6 recovery; O13 continuity of history; O1 readiness without waste |
| **Traceability** | Profile: Study Progress / coverage dimensions. Strategy: Recovery and Build strategies preserve history. Planning Model: D3 |
| **MS001** | D3 |

---

### PD-03 — Revision reservation

| Aspect | Specification |
|--------|----------------|
| **What** | Reserve a protected revision period before the sitting before packing first-pass density |
| **Why it exists** | Retention and exam readiness require consolidation time; revision must not be residual scrap |
| **When it applies** | Every complete package (mandatory). Size may adapt; non-zero protected intent is required when a sitting is planned |
| **Objective supported** | O5 reserve revision; O2 retention; O1 readiness |
| **Traceability** | Profile: runway & coverage maturity. Strategy: Approach/Triage privilege revision protection; Late Starter still reserves a minimum. Planning Model: D5, C10 |
| **MS001** | D5 |

---

### PD-04 — First-pass vs revision phase boundary

| Aspect | Specification |
|--------|----------------|
| **What** | Define when educational posture shifts from first-pass learning emphasis to revision emphasis |
| **Why it exists** | Students need a clear change of mission — not silent topic hopping dressed as “revision” |
| **When it applies** | Every complete package; timing adapts to coverage and strategy (earlier freeze under Rescue / Late Starter) |
| **Objective supported** | O5 revision; O7 earned confidence via legible phases; O1 readiness |
| **Traceability** | Profile: coverage vs runway. Strategy: Revision Intensive / Exam Rescue / Balanced Maintenance. Planning Model: D6 |
| **MS001** | D6 |

---

### PD-05 — Practice intensity

| Aspect | Specification |
|--------|----------------|
| **What** | Decide how heavily question practice and assessment exposure should feature on material already studied |
| **Why it exists** | Coverage without application produces false readiness; practice without coverage invents competence theatre |
| **When it applies** | Adaptive. Elevated under Practice Intensive, Weak Topic Reinforcement, High Performer Optimisation, and late Approach strategies; moderated under Recovery / Confidence Restoration |
| **Objective supported** | O1 readiness; O10 exam-craft rehearsal; Knowledge & Mastery separation of coverage vs understanding |
| **Traceability** | Profile: practice depth vs coverage; evidence posture. Strategy: ES-04 / ES-06 / ES-11 privileges. Planning Model: adaptive D10/D16 families; Evidence Model claim law |
| **MS001** | Related adaptive intensity / revision emphasis (D10, D16) |

---

### PD-06 — Study intensity

| Aspect | Specification |
|--------|----------------|
| **What** | Set sustainable daily/weekly intensity band and posture within declared available time |
| **Why it exists** | Keepable intensity compounds; heroic overload trains abandonment |
| **When it applies** | Band is mandatory for every package; exact posture within band is adaptive to strategy, runway, and recovery needs |
| **Objective supported** | O3 consistency; O4 burnout prevention; O8 realism |
| **Traceability** | Profile: capacity, consistency, burnout/recovery signals. Strategy: Steady Progression prefers keepable rhythm; Recovery / Confidence Restoration lower load; Late Starter / Rescue refuse impossible spikes as primary answer. Planning Model: D7, D10, C1–C5 |
| **MS001** | D7, D10 |

---

### PD-07 — Recovery allowance

| Aspect | Specification |
|--------|----------------|
| **What** | Decide lighter-load allowance after dense work, mocks, illness, leave, or abandoned intensity |
| **Why it exists** | Learning from dense study and life interruption requires cognitive and calendar recovery; punishment pacing is forbidden |
| **When it applies** | Adaptive; strongly expected after mocks, burnout signals, Recovering / Returning states, and strategy ES-07 / ES-08 |
| **Objective supported** | O4 burnout prevention; O6 recovery; O3 consistency rebuild |
| **Traceability** | Profile: recovery history, soft signals, consistency disruption. Strategy: Restore family. Planning Model: D13, D18 |
| **MS001** | D13, D18 |

---

### PD-08 — Buffer allocation

| Aspect | Specification |
|--------|----------------|
| **What** | Place spare educational capacity for slip, illness, and replan |
| **Why it exists** | Real candidates interrupt; buffers make recovery educationally possible without shame theatre |
| **When it applies** | Adaptive amount; non-zero buffer policy strongly expected when horizon allows. Triage strategies may shrink buffers but must still name residual risk |
| **Objective supported** | O6 recovery; O8 realism; O4 sustainability |
| **Traceability** | Profile: interruption history, leave uncertainty, runway. Strategy: Steady / Consolidation privilege buffers; Exam Rescue names reduced buffer honestly. Planning Model: D12 |
| **MS001** | D12 |

---

### PD-09 — Milestone positioning

| Aspect | Specification |
|--------|----------------|
| **What** | Place educational checkpoints (section coverage complete, revision start, final approach, mock windows) |
| **Why it exists** | Progress must be legible; earned confidence needs visible structure |
| **When it applies** | Adaptive calendar position; milestones themselves are educationally expected in every complete journey design |
| **Objective supported** | O7 earned confidence; O12 reduced decision burden; O1 readiness via honest progress markers |
| **Traceability** | Profile: coverage & state. Strategy: Confidence Restoration privileges completable wins; Late Starter privileges early triage checkpoints. Planning Model: D14 |
| **MS001** | D14 |

---

### PD-10 — Risk mitigation

| Aspect | Specification |
|--------|----------------|
| **What** | Decide how the package protects against educational risks: short runway, thin evidence, previous fails, weak foundations, adherence collapse, hidden infeasibility |
| **Why it exists** | Expert tutors name danger early and adjust posture — they do not publish optimistic theatre |
| **When it applies** | Always evaluate; elevated under At Risk / Late Starter / Exam Rescue / previous-attempt history / thin evidence |
| **Objective supported** | O8 avoid unrealistic plans; O1 honest readiness; O5 revision protection |
| **Traceability** | Profile: risk, attempt history, feasibility signals, evidence thinness. Strategy: Triage and Weak Reinforcement. Planning Model: D8, D20, F10 |
| **MS001** | D8, D20 |

---

### PD-11 — Confidence protection

| Aspect | Specification |
|--------|----------------|
| **What** | Decide how the package builds or restores *earned* confidence — completable intensity, clear next steps, truthful narration — without false reassurance |
| **Why it exists** | Confidence without warrant is dangerous; despair without guidance is useless |
| **When it applies** | Always consider; elevated under Confidence Restoration, after mock shock, previous fail aftermath, or fragile soft signals |
| **Objective supported** | O7 promote earned confidence; O3 consistency; understatement rules |
| **Traceability** | Profile: confidence / soft-signal dimensions. Strategy: ES-07 privileges achievable truthful wins. Planning Model: O7; explainability obligations |
| **MS001** | Related to D9 explainability and adaptive load (D10) |

---

### PD-12 — Capacity envelope

| Aspect | Specification |
|--------|----------------|
| **What** | Compute educationally usable study capacity to the exam after leave, working schedule, and mandatory phase reservations |
| **Why it exists** | Feasibility is the tutor’s first honesty check |
| **When it applies** | Every complete package (mandatory) |
| **Objective supported** | O8 realism; O4 burnout prevention; O2/O5 via room left after reservations |
| **Traceability** | Profile: capacity & leave. Strategy: all strategies consume capacity truth. Planning Model: D4 |
| **MS001** | D4 |

---

### PD-13 — Feasibility judgement

| Aspect | Specification |
|--------|----------------|
| **What** | Explicitly judge whether remaining syllabus work + revision + recovery fit capacity; surface infeasibility when they do not |
| **Why it exists** | Expert tutors refuse fantasy schedules |
| **When it applies** | Every complete package (mandatory); re-run after missed study, leave, or strategy change |
| **Objective supported** | O8 avoid unrealistic plans; O1 honest readiness |
| **Traceability** | Profile: remaining work vs capacity. Strategy: Late Starter / Exam Rescue privilege early truth. Planning Model: D8, C18 |
| **MS001** | D8 |

---

### PD-14 — Consolidation / retention posture

| Aspect | Specification |
|--------|----------------|
| **What** | Decide how often and how heavily to interleave return to recent topics during first pass without abandoning sequence |
| **Why it exists** | Long syllabuses punish one-way marching; retention protection is part of readiness |
| **When it applies** | Adaptive; elevated under Knowledge Consolidation and long first-pass runways; light under early Foundation Building |
| **Objective supported** | O2 retention; O1 readiness |
| **Traceability** | Profile: decay/retention risk, syllabus length. Strategy: ES-03. Planning Model: D11 |
| **MS001** | D11 |

---

### PD-15 — Mock timing intent

| Aspect | Specification |
|--------|----------------|
| **What** | Decide whether and roughly when timed exam simulations should occur |
| **Why it exists** | Exam craft needs rehearsal when coverage makes the exercise meaningful; mocks without recovery destroy learning |
| **When it applies** | Adaptive within constraint rules; more central under Approach / High Performer; deferred when coverage is too thin |
| **Objective supported** | O10 exam craft; O1 readiness; O4 recovery after mocks |
| **Traceability** | Profile: coverage maturity, previous attempts. Strategy: ES-05 / ES-11. Planning Model: D15, C11 |
| **MS001** | D15 |

---

### PD-16 — Catch-up / compression response

| Aspect | Specification |
|--------|----------------|
| **What** | After missed study or shortfall, choose among lawful options: use buffers, reduce intensity elsewhere, defer low-priority consolidation, escalate infeasibility — not silent impossible compression |
| **Why it exists** | Recovery that still counts must not violate sustainability or revision protection |
| **When it applies** | When Profile shows missed study, adherence collapse, or capacity shock |
| **Objective supported** | O6 recovery; O4 burnout prevention; O8 realism |
| **Traceability** | Profile: missed study / consistency. Strategy: Recovery / Rescue. Planning Model: D18; Forbidden F1/F2/F9 |
| **MS001** | D18 |

---

## 5. Strategy → Decision Emphasis Map

This map guides adaptive emphasis. It does not override constraints or mandatory decisions.

| Strategy | Heightened decisions | Softened / refused emphases |
|----------|----------------------|-----------------------------|
| ES-01 Foundation Building | PD-01, PD-02, PD-06 (sustainable), PD-03 (reserve even if far) | Heavy mock theatre; practice-as-main-story on unstudied units |
| ES-02 Steady Progression | PD-06 consistency, PD-08 buffers, PD-14 light | Boom–bust intensity; revision-as-daily-story too early |
| ES-03 Knowledge Consolidation | PD-14, PD-03, PD-09 | Abandoning remaining first-pass without warrant |
| ES-04 Practice Intensive | PD-05, PD-11 (earned via evidence), PD-15 when ready | Practising never-studied topics as coverage |
| ES-05 Revision Intensive | PD-03, PD-04, PD-05 on revised scope, PD-15 | New first-pass expansion into revision |
| ES-06 Weak Topic Reinforcement | PD-05 targeted, PD-10, PD-01 integrity | Ignoring evidenced weakness to protect schedule theatre |
| ES-07 Confidence Restoration | PD-11, PD-06 moderated, PD-09 completable | Pass-guarantee pep talk; readiness inflation |
| ES-08 Recovery Strategy | PD-07, PD-06 lower, PD-16, PD-08 | Immediate make-up-every-hour compression |
| ES-09 Exam Rescue | PD-13, PD-10, PD-03/PD-04 freeze, PD-16 triage | Impossible catch-up calendars; hidden infeasibility |
| ES-10 Late Starter | PD-13 early, PD-01 still lawful, PD-03 minimum, PD-10 | Pretend full leisurely journey fits |
| ES-11 High Performer Optimisation | PD-05 polish, PD-15, PD-14 light maintenance | Reinvention of beginner first-pass for novelty |
| ES-12 Balanced Maintenance | PD-11 stability, PD-14 light, PD-06 calm | Last-minute syllabus expansion; panic intensity |

---

## 6. Forbidden Pipeline Shortcuts

| Shortcut | Why unlawful |
|----------|--------------|
| Profile → Calendar | Skips strategy and decisions; invents approach in dates |
| Strategy → Schedule without decisions | Leaves intensity/revision/feasibility undefined |
| Pack first-pass before revision reservation | Violates O5 / D5 causality |
| Emit package without feasibility judgement | Hidden infeasibility (F10) |
| Numeric weights instead of priority model | Replaces educational reasoning with opaque scoring |
| Re-decide sequencing for “engagement” | Violates curriculum primacy |

---

## 7. Re-running the Pipeline

Re-run Stages A→F when any of the following become material:

- Profile evolution that changes educational state or capacity truth
- Strategy transition (MS003)
- Sitting date or examination change
- Major leave / missed-study shock
- Planning Model / constraint corpus amendment

Partial “tweak the calendar” without re-deciding is only lawful when decisions remain valid envelopes — future plan generation concern, not a licence to redefine decisions silently.

---

## 8. Cross References

- `PLANNING_DECISION_ENGINE.md` — engine overview and package definition
- `DECISION_PRIORITY_MODEL.md` — objective conflicts
- `DECISION_CONFLICT_RESOLUTION.md` — life and adherence conflicts
- `DECISION_EXPLAINABILITY.md` — how to narrate PD-01…PD-16
- `../planning/PLANNING_DECISION_MODEL.md` — mandatory / adaptive / forbidden classes
- `../strategy/STRATEGY_CATALOGUE.md` — ES-01…ES-12 meanings
