# Student Digital Twin 2.0

**Document ID:** V2-013-STUDENT-DIGITAL-TWIN  
**Milestone:** V2-013 — Student Digital Twin 2.0  
**Status:** Authoritative domain + application specification  
**Authority:** Architectural  
**Nature:** Framework-independent deterministic evidence-driven learner state  

**Packages:**
- `app/domain/student_twin/`
- `app/application/student_twin/`

**Related:** [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md) · [`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md) · [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md) · [`EDUCATIONAL_PRINCIPLES.md`](EDUCATIONAL_PRINCIPLES.md) · [`../../STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)

---

## Document Responsibility

This document defines **how** the Version 2 Student Digital Twin is implemented: packages, engine contract, inputs, outputs, and success criteria.

It does **not** redefine Twin philosophy or amend constitutional law.

| Companion | Responsibility |
|-----------|----------------|
| [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md) | Why the Digital Twin exists |
| [`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md) | What rules every implementation must obey |

---

## 1. Purpose

The Student Digital Twin is the living, evidence-based model of a learner's educational state.

It answers:

> Given everything we know about this learner today,  
> what educational decision is most likely to improve long-term mastery?

It does **not**:

- Teach
- Store curriculum or PDFs
- Manage sessions
- Generate missions, activities, or questions
- Persist UI state
- Depend on Flask or SQLAlchemy
- Let AI determine learner state

Official syllabus structure remains owned by the Curriculum Graph. Session / activity / mission execution remain owned by their engines. This Twin **interprets evidence** and produces educational state + explainable recommendations.

Philosophy authority: [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md).

---

## 2. Architecture

```text
Evidence Events
      │
      ▼
StudentTwinEngine
      │
      ├─ EvidenceAggregator
      ├─ MasteryCalculator
      ├─ ConfidenceCalculator
      ├─ RetentionEstimator
      ├─ ReadinessEstimator
      ├─ LearningVelocityService
      ├─ WeaknessAnalyser
      ├─ RecommendationService
      └─ Snapshot / Timeline / Comparison / Explanation
      │
      ▼
Immutable TwinSnapshot (+ DTOs)
```

```text
app/domain/student_twin/          app/application/student_twin/
  learner.py                        twin_engine.py
  digital_twin.py                   evidence_aggregator.py
  twin_identity.py                  mastery_calculator.py
  twin_version.py                   confidence_calculator.py
  evidence_event.py                 retention_estimator.py
  evidence_type.py                  readiness_estimator.py
  evidence_profile.py               weakness_analyser.py
  knowledge_state.py                learning_velocity_service.py
  mastery_state.py                  recommendation_service.py
  confidence_state.py               snapshot_service.py
  retention_state.py                timeline_service.py
  readiness_state.py                comparison_service.py
  learning_velocity.py              explanation_service.py
  weakness_profile.py               diagnostics.py
  recommendation_state.py           policies/
  learning_history.py               dto/
  twin_snapshot.py                  exceptions.py
  confidence_band.py
```

---

## 3. Inputs

Evidence only:

| Evidence type | Role |
|---------------|------|
| `activity_completed` | Activity completion signal |
| `assessment_outcome` | Assessment result |
| `practice_result` | Practice attempt |
| `reflection` | Reflection signal |
| `self_assessment` | Learner self-rating |
| `recall_performance` | Recall / retrieval result |
| `confidence_rating` | Explicit confidence rating |
| `time_on_task` | Time-on-task signal |
| `session_completion` | Session completion |
| `mission_completion` | Mission completion |
| `revision_outcome` | Revision result |

Never curriculum JSON, PDFs, or AI responses as Twin truth.

---

## 4. Outputs

| Output | Meaning |
|--------|---------|
| Knowledge State | Understanding beliefs per topic |
| Mastery State | Demonstrated capability beliefs |
| Confidence | Explicit uncertainty bands |
| Retention | Durability estimates |
| Readiness | Preparedness blend |
| Learning Velocity | Recent progress rate |
| Weakness Profile | Ordered educational weaknesses |
| Recommendations | Explainable next interventions |
| Timeline snapshots | Immutable versioned history |

Every recommendation includes: evidence considered, rationale, expected benefit, confidence.

---

## 5. Binding rules

1. **Evidence before inference** — no state change without observable evidence.
2. **Immutable history** — past events are never rewritten; Twin evolves by accumulation.
3. **Determinism** — identical evidence → identical educational conclusions.
4. **Explicit uncertainty** — every conclusion carries a confidence band.
5. **Explainable recommendations** — no opaque scores as sole authority.
6. **Reversible recommendations** — new evidence may change advice.
7. **Smallest helpful intervention** — never optimise engagement or screen time.
8. **Framework independence** — no Flask, ORM, routes, UI, or persistence writes.

---

## 6. Relationship to Epic Twin (`app/domain/twin/`)

Version 1 / Epic Twin packages (`app/domain/twin/`, `app/application/twin_update/`) remain the production belief-update path for the existing platform.

V2-013 delivers a **Version 2 bounded context** (`student_twin`) aligned to the Digital Twin Philosophy responsibilities (Knowledge, Mastery, Confidence, Retention, Readiness, Velocity, Weaknesses, Recommendations, History). It does not silently replace Epic Twin persistence or routes.

Future integration may wire journey-attributed evidence into either path under Twin constitutional authority — without competing learner-state stores in product narratives.

---

## 7. Engine contract

```text
StudentTwinEngine
  create_twin(learner) → DigitalTwin
  ingest_evidence(twin, event) → DigitalTwin
  ingest_many(twin, events) → DigitalTwin
  recalculate(twin, as_of=…) → DigitalTwin
  snapshot(twin) → TwinSnapshotDTO
  explain / explain_all
  compare / timeline / diagnose
```

Injectable `clock` and `id_factory` support deterministic tests. Callers own persistence.

---

## 8. Success criteria

| Criterion | Status |
|-----------|--------|
| Deterministic learner model | ✓ |
| Evidence-driven state | ✓ |
| Immutable history | ✓ |
| Explainable recommendations | ✓ |
| Framework independent | ✓ |
| Foundation for adaptive learning | ✓ |

---

## 9. Non-goals

- HTTP routes / blueprints
- Alembic migrations / ORM models
- AI / LLM ownership of Twin mutations
- Curriculum storage or PDF parsing
- Session / mission / activity generation
- Version 1 behavioural changes

---

## References

The Digital Twin documentation hierarchy separates *why*, *what must be obeyed*, and *how*:

| Document | Defines |
|----------|---------|
| [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md) | **Why** the Digital Twin exists — purpose, principles, ethics, responsibilities |
| [`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md) | **What** rules every implementation must obey — non-negotiable constitutional law |
| This document (`STUDENT_DIGITAL_TWIN.md`) | **How** the Digital Twin is implemented — Version 2 bounded context, engine, and contracts |

Future Twin implementation work must remain consistent with all three. Philosophy and Constitution outrank convenience; this specification outranks ad-hoc package inventiveness.
