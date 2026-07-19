# Student Experience

**Document ID:** V2-017B-A-STUDENT-EXPERIENCE  
**Milestone:** V2-017B-A — Student Experience Foundation · **V2-018 — Production Experience Integration**  
**Status:** Authoritative domain + application specification; production adapters active  
**Authority:** Architectural — source of truth for learner product projection  
**Nature:** Framework-independent learner projection / orchestration layer  

**Packages:**
- `app/domain/student_experience/`
- `app/application/student_experience/`
- `app/presentation/student/` (thin UI)
- `app/infrastructure/adapters/` (production Experience ports — V2-018)

**Depends on:** injected ports only (Student Twin, Adaptive Decision, Mission, Learning Journey, Learning Orchestrator). Does **not** import or modify those educational packages.

**Related:** [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md) · [`ARCHITECTURE_DECISIONS/ADR-005-Single-Next-Action-Authority.md`](ARCHITECTURE_DECISIONS/ADR-005-Single-Next-Action-Authority.md) · [`PRODUCTION_INTEGRATION.md`](PRODUCTION_INTEGRATION.md) · [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md) · [`VERSION2_ROADMAP.md`](VERSION2_ROADMAP.md)

---

## 1. Vision

Every screen must answer one question:

> **What should I do next, and why?**

Student Experience is **not** another educational engine.

It is a **projection and orchestration layer** that consumes existing bounded contexts and translates architecture into educational value.

The learner must never see internal concepts such as:

- Student Digital Twin
- Adaptive Decision Engine
- Learning Orchestrator
- Mission Engine
- Curriculum Graph

---

## 2. Design Philosophy

| Principle | Meaning |
|-----------|---------|
| Projection, not ownership | Experience assembles learner-facing views; it does not own learner state |
| Single next-action authority | Today's Recommendation comes only from Adaptive Decision (ADR-005) |
| Educational language | Internal engine names are translated into student vocabulary |
| Framework independence | Domain + application remain free of Flask / SQLAlchemy |
| Explainability | Every recommendation answers *why* using educational evidence |
| Navigation ownership | Experience owns presentation, workflow, projection, and navigation only |
| Production default | V2-018: production adapters are the default wiring; preview ports retired |

```text
Learner UI (presentation)
        │
        ▼
Student Experience (application)
        │
        ├── ports → Student Twin          (Learning Insights / Exam Readiness)
        ├── ports → Adaptive Decision     (Today's Recommendation / Revision)
        ├── ports → Mission               (Today's Session)
        ├── ports → Learning Journey      (Journey progress)
        └── ports → Learning Orchestrator (Learning Activity status)
                │
                ▼
Infrastructure Experience adapters (V2-018)
```

---

## 3. Experience Model

### Domain (`app/domain/student_experience/`)

| Module | Role |
|--------|------|
| `experience_workspace.py` | Student operational context + surface navigation |
| `experience_session.py` | Start Session presentation handle (references only) |
| `experience_snapshot.py` | Composite snapshot of all surfaces |
| `student_home.py` | Home projection facts |
| `journey_projection.py` | Journey progress without graph jargon |
| `revision_projection.py` | Revision options from Adaptive Decision outputs |
| `history_projection.py` | Accomplishments without raw event logs |
| `profile_projection.py` | Examination, preferences, stats, goals, settings |
| `recommendation_explanation.py` | Terminology translation + student-safe explanations |

### Application (`app/application/student_experience/`)

| Service | Responsibility | Owns authority? |
|---------|----------------|-----------------|
| `HomeService` | Greeting, countdown, readiness, recommendation, Start Session | No — Twin + Adaptive + Mission |
| `JourneyService` | Topic progress / completion estimate | No — Journey |
| `RevisionService` | Highest-value revision + alternatives | No — Adaptive Decision |
| `HistoryService` | Sessions, study time, readiness progression | No — Twin insights |
| `ProfileService` | Examination / preferences / goals / settings | No — Twin (+ presentation flags) |
| `ExplanationService` | Student-language “why recommended” | Projection wording only |
| `DashboardService` | Aggregate dashboard + navigation | Yes — UX navigation / workspace |
| `StudentExperienceService` | Public facade | Orchestration only |

DTOs under `dto/` are frozen snapshots. Ports under `ports/` are Protocols returning opaque dicts.

---

## 4. Production Adapters (V2-018)

| Adapter | Port | Package |
|---------|------|---------|
| `ExperienceTwinAdapter` | `StudentTwinPort` | `adapters/student_twin/` |
| `ExperienceAdaptiveAdapter` | `AdaptiveDecisionPort` | `adapters/adaptive/` |
| `ExperienceMissionAdapter` | `MissionPort` | `adapters/mission/` |
| `ExperienceJourneyAdapter` | `LearningJourneyPort` | `adapters/journey/` |
| `ExperienceOrchestratorAdapter` | `LearningOrchestratorPort` | `adapters/orchestrator/` |

Composition root: `StudentExperienceComposition` / `build_production_experience()` under `adapters/student_experience/`.

**Adapter responsibilities**

- Satisfy Experience ports with opaque documents from stores / optional engines
- Persist workspace, session, and projection snapshots via V2-017 persistence
- Emit Experience observability events
- Run the learning loop on Start Session (Mission → evidence/orchestrator → Twin → Adaptive → updated Home)

**Must not:** compute readiness, invent recommendations, duplicate Journey / Mission / Twin math, or couple Flask into educational kernels.

**Preview retirement:** `preview_ports.py` removed. Production adapters are the default in `app/presentation/student/factory.py`.

---

## 5. Primary Experiences

### Student Home

Greeting, exam countdown, exam readiness, today's recommendation, estimated study time, expected readiness improvement, recommendation explanation, Start Session — all from production ports.

### Journey

Current / completed / upcoming topics, progress, estimated completion — from Learning Journey port. No preview roadmap.

### Revision

Highest-value revision, priority, benefit, duration, reasoning, alternatives — from Adaptive Decision only.

### History

Completed sessions, readiness progression, revision history, statistics — from Twin insights / orchestrator activity observations.

### Profile

Exam, goals, preferences, learning statistics — from Twin learner summary.

---

## 6. Session Start Loop

```text
Student Home
    → Start Today's Session
    → Mission Engine (ExperienceMissionAdapter)
    → Learning Session Runtime / Orchestrator cycle
    → Evidence Recording
    → Twin Update
    → Adaptive Recalculation
    → Updated Home
```

Legacy numeric redirect to V1 `mission.session` is removed. The learner returns to Student Home with refreshed production projections.

---

## 7. Observability Events

| Event | When |
|-------|------|
| `StudentHomeViewed` | Home surface loaded |
| `JourneyViewed` | Journey surface loaded |
| `HistoryViewed` | History surface loaded |
| `LearningSessionStarted` | Mission start |
| `LearningSessionCompleted` | Session completion in loop |
| `RecommendationAccepted` | Recommendation accepted after loop |
| `RecommendationDismissed` | Explicit dismiss |
| `RevisionStarted` | Revision begin CTA |
| `ProfileUpdated` | Twin projection updated from session outcome |

---

## 8. Authority Matrix

| Capability | Owner | Student Experience role |
|------------|-------|-------------------------|
| Presentation | **Student Experience** | Owns |
| Workflow / navigation | **Student Experience** | Owns |
| Projection | **Student Experience** | Owns |
| Learner state | Student Digital Twin | Consume via port |
| Readiness calculations | Student Digital Twin | Consume (as Exam Readiness) |
| Recommendations / next action | Adaptive Decision Engine | Consume (ADR-005) |
| Mission generation / delivery | Mission Engine | Consume (Today's Session) |
| Journey progression | Learning Journey | Consume |
| Evidence | Evidence spine / Twin intake | Never own |
| Live pipeline order | Learning Orchestrator | Observe (Learning Activity) |
| Persistence / events | Infrastructure | Owns stores and envelopes |

**Explicit non-authority:** Student Experience must not invent mastery, Topic Complete, readiness scores, or next actions.

---

## 9. Terminology Mapping

| Internal | Student |
|----------|---------|
| Student Digital Twin | Learning Insights |
| Adaptive Decision | Today's Recommendation |
| Readiness Score | Exam Readiness |
| Mission Engine | Today's Session |
| Learning Orchestrator | Learning Activity |

---

## 10. Constraints (must not)

- Move educational logic into adapters or Flask
- Compute readiness in infrastructure
- Compute recommendations outside Adaptive
- Duplicate Mission / Journey / Twin calculations
- Reintroduce preview ports as the production default
- Expose internal architectural terminology to learners

---

## 11. Success Criteria

- Preview infrastructure removed  
- Production adapters active  
- Student Experience powered by live educational platform ports  
- Complete learning loop operational  
- Authority boundaries preserved  
- Existing UI unchanged (no presentation redesign)  
- Educational kernel remains framework independent  
- Ready for further ORM / persistence expansion  
