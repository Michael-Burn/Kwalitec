# Adaptive Decision Engine

**Document ID:** V2-014-ADAPTIVE-DECISION-ENGINE  
**Milestone:** V2-014 — Adaptive Decision Engine (Revision Phase)  
**Status:** Authoritative domain + application specification  
**Authority:** Architectural  
**Nature:** Framework-independent deterministic educational intervention selection  

**Packages:**
- `app/domain/adaptive_learning/`
- `app/application/adaptive_learning/`

**Related:** [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) · [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md) · [`EDUCATIONAL_PRINCIPLES.md`](EDUCATIONAL_PRINCIPLES.md) · [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)

---

## 1. Purpose

The Adaptive Decision Engine evaluates learner educational state and recommends the **highest educational-value intervention**.

Phase 1 implements **Revision Decisions only**.

It answers:

> Given Twin state, journey position, and curriculum context —  
> which revision intervention most improves long-term readiness per study minute?

It does **not**:

- Modify the Digital Twin
- Teach or generate educational content / questions
- Persist data
- Own session, mission, or curriculum execution
- Use AI / LLM reasoning
- Depend on Flask or SQLAlchemy

Twin remains the authority for learner-state claims. This engine **consumes** Twin snapshots and produces explainable intervention decisions.

---

## 2. Educational decision pipeline

```text
Twin Snapshot
  + Knowledge / Mastery / Retention / Readiness
  + Weakness Profile / Velocity / History
  + Journey Position + Curriculum Context
        │
        ▼
AdaptiveDecisionEngine
        │
        ├─ RevisionPlanner      → ranked RevisionCandidates
        ├─ PriorityCalculator   → InterventionPriority
        ├─ ROIEstimator         → EducationalROI
        ├─ RevisionScheduler    → RevisionWindows
        ├─ InterventionSelector → Intervention + RevisionPlan
        └─ ExplanationService   → DecisionExplanation
        │
        ▼
AdaptiveDecision (+ DecisionSnapshot DTOs)
```

Determinism: identical Twin + context inputs → identical decision outputs. No randomness.

---

## 3. Architecture

```text
app/domain/adaptive_learning/          app/application/adaptive_learning/
  intervention_type.py                   decision_engine.py
  intervention_priority.py               revision_planner.py
  intervention.py                        priority_calculator.py
  decision_explanation.py                roi_estimator.py
  revision_candidate.py                  revision_scheduler.py
  revision_plan.py                       intervention_selector.py
  revision_window.py                     explanation_service.py
  educational_roi.py                     diagnostics.py
  adaptive_decision.py                   exceptions.py
  decision_snapshot.py                   policies/
                                         dto/
```

---

## 4. Priority model

Priority is a weighted blend of educational factors (weights sum to 1.0):

| Factor | Role |
|--------|------|
| Retention risk | `1 − retention` — durability threat |
| Mastery gap | `1 − mastery` — capability deficit |
| Prerequisite criticality | Blocks downstream topics |
| Curriculum importance | Exam / syllabus weight |
| Historical struggle | Weakness + struggle signals |
| Confidence gap | Explicit uncertainty |
| Learning velocity | Low activity / declining mastery |
| Exam proximity | Time pressure (0…1) |

Bands: negligible / low / medium / high / critical.

Revision is recommended only when priority ≥ `MIN_REVISION_PRIORITY` (0.20).

---

## 5. ROI philosophy

Educational ROI estimates **readiness improvement per study time**, not engagement:

| Output | Meaning |
|--------|---------|
| Expected readiness improvement | Bounded improvement estimate |
| Estimated study duration | Deterministic minutes from severity |
| Educational benefit | Blend of improvement, importance, priority |
| Cost-benefit ratio | Benefit ÷ study hours |
| Return on study time | Same ratio (Phase 1 alias) |

ROI never invents mastery scores or generates content. It ranks interventions by educational value density.

---

## 6. Intervention strategy

### Supported domain types

`REVISION` · `CONTINUE` · `REPEAT` · `ASSESS` · `BREAK` · `SKIP`

### Phase 1 behaviour

Only **REVISION** is selected and planned.

Other types remain domain vocabulary so future phases can add selectors without redesigning the decision aggregate, priority model, or explanation contract.

Every recommendation includes:

1. Evidence considered  
2. Decision rationale  
3. Priority (score + band)  
4. Expected educational benefit  
5. Confidence  

Plus estimated study time and Educational ROI.

---

## 7. Inputs and outputs

### Inputs (consumed, never mutated)

- Digital Twin Snapshot  
- Knowledge / Mastery / Retention / Readiness / Confidence  
- Weakness Profile / Learning Velocity / History ids  
- Current Journey Position  
- Current Curriculum Context (importance, prerequisites, exam proximity, struggle)

### Outputs

- `AdaptiveDecision`  
- `RevisionPlan` (+ windows)  
- Priority scores  
- Educational ROI  
- Explanation  
- Estimated study time  
- Confidence  

---

## 8. Future extension roadmap

| Phase | Focus |
|-------|-------|
| Phase 1 (this milestone) | Revision decisions |
| Phase 2 | CONTINUE / REPEAT selection from Twin readiness |
| Phase 3 | ASSESS triggers from confidence/evidence gaps |
| Phase 4 | BREAK / SKIP with workload and diminishing-returns gates |
| Later | Multi-intervention portfolios; journey-aware interrupt policies |

Architecture already separates **type vocabulary**, **priority**, **ROI**, **selection**, and **explanation** so new intervention strategies plug in without redesign.

---

## 9. Constraints and success criteria

**Must not** modify Digital Twin, Education Platform, Mission Engine, Curriculum Management, or Curriculum Ingestion.  
**Must not** use AI, generate content/questions, or persist.

**Success**

- Deterministic adaptive decisions  
- Explainable recommendations  
- Educational ROI estimation  
- Revision planning + scheduling  
- Extensible intervention architecture  
- Framework independence  

---

## 10. Package contracts

Public facade: `AdaptiveDecisionEngine.decide(twin_snapshot, …)`.

Diagnostics: `AdaptiveDiagnostics.inspect(decision)` — integrity only, no mutation.
