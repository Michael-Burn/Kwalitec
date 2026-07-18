# Learning Journey Domain Implementation

**Document ID:** V2-002-IMPL  
**Milestone:** V2-002 — Learning Journey Domain Foundation  
**Status:** Implemented (domain layer only)  
**Nature:** Code ↔ architecture mapping  

**Parent architecture:** [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md), [`STATE_MACHINE.md`](STATE_MACHINE.md), [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)

This document records how the Version 2 Learning Journey **domain package** maps to the V2-001 educational architecture. It does not change Version 1 runtime behaviour.

---

## 1. Package location

```
app/domain/learning_journey/
├── __init__.py                 # Lazy public exports
├── entities/
│   ├── learning_journey.py     # Aggregate root
│   ├── learning_session.py
│   ├── learning_objective.py
│   ├── journey_progress.py
│   ├── journey_recommendation.py
│   ├── journey_reflection.py
│   ├── journey_evidence.py
│   └── journey_history.py
├── value_objects/
│   ├── journey_state.py        # JourneyState + lawful transitions
│   ├── session_state.py        # SessionState + lawful transitions
│   ├── effort_estimate.py
│   └── completion_status.py
├── services/
│   ├── journey_progress_service.py
│   └── journey_validation_service.py
└── interfaces/
    └── learning_journey_repository.py   # Contract only
```

Pure domain: no Flask, SQLAlchemy, blueprints, migrations, or feature flags.

---

## 2. Entity → architecture mapping

| Architecture entity (V2-001) | Code | Notes |
|------------------------------|------|-------|
| LearningJourney | `entities.learning_journey.LearningJourney` | Aggregate; topic + learner owned |
| LearningSession | `entities.learning_session.LearningSession` | Session complete ≠ journey complete |
| LearningObjective | `entities.learning_objective.LearningObjective` | Kinds: Understand / Apply / Analyse / Review / Revise |
| JourneyProgress | `entities.journey_progress.JourneyProgress` | No mastery / competence scores |
| JourneyRecommendation | `entities.journey_recommendation.JourneyRecommendation` | Never claims certainty |
| JourneyReflection | `entities.journey_reflection.JourneyReflection` | PENDING → CAPTURED posture |
| JourneyEvidence | `entities.journey_evidence.JourneyEvidence` | Attributes Learning Evidence Model ids/types |
| JourneyHistory | `entities.journey_history.JourneyHistory` | Append-only event log |
| JourneyState | `value_objects.journey_state.JourneyState` | Includes RESUMED, DEFERRED, ARCHIVED |
| SessionState | `value_objects.session_state.SessionState` | Includes SKIPPED for planned cancel |

---

## 3. Value objects

| Value object | Code | Architecture source |
|--------------|------|---------------------|
| JourneyState + events | `journey_state.py` | [`STATE_MACHINE.md`](STATE_MACHINE.md) §2 |
| SessionState + events | `session_state.py` | [`STATE_MACHINE.md`](STATE_MACHINE.md) §3 |
| EffortEstimate | `effort_estimate.py` | LOW / MEDIUM / HIGH / EXTENSIVE — not time alone |
| CompletionStatus | `completion_status.py` | Coverage / obligation posture — not mastery |

Brief vocabulary aliases (PLANNED ≈ NOT_STARTED, IN_PROGRESS ≈ ACTIVE) are documented on `SessionState`; canonical enum members follow the state machine.

---

## 4. Services

| Service | Responsibility | Constraint |
|---------|----------------|------------|
| `JourneyProgressService` | Deterministic progress from sessions, evidence, objectives, reflections | No mastery maths; default min 2 completed sessions + reflection closure |
| `JourneyValidationService` | State transitions, ordering, aggregate consistency | Enforces session≠journey complete; reflection pending blocks Topic Complete confirm |

---

## 5. Repository

`LearningJourneyRepository` is an **ABC contract only**. No infrastructure adapter ships in V2-002. Future application layers may implement persistence without changing domain objects.

---

## 6. Relationship to existing domains

| Existing authority | Journey domain role |
|--------------------|---------------------|
| `app.domain.evidence` | `JourneyEvidence` cites `EvidenceType` and `EvidenceConfidenceLevel` — does not fork the catalogue |
| Student Digital Twin | Not written by this package |
| Mission / Recommendation engines | Untouched; journey recommendations are separate V2 artefacts |
| Curriculum Engine | Topic / objective identity referenced by id only |

---

## 7. Tests

Pure domain suite: `tests/test_learning_journey_domain.py` (entity invariants, value objects, transitions, validation, progress, repository contract, framework-purity AST check).

---

## 8. Non-goals (this milestone)

- Version 1 route / Mission / Recommendation / Dashboard / Study Session changes
- SQLAlchemy models or Alembic migrations
- Feature flags or UI
- Curriculum Graph persistence (sequenced separately)
- Learning Journey Engine runtime (V2-003)

---

## 9. Closing

V2-002 establishes the code vocabulary that V2-003+ engines must use. Implementations must not invent parallel meanings for Journey, Session, Evidence, Reflection, or Topic Complete.
