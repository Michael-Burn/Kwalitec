# Student Experience

**Document ID:** V2-017B-A-STUDENT-EXPERIENCE  
**Milestone:** V2-017B-A — Student Experience Foundation  
**Status:** Authoritative domain + application specification  
**Authority:** Architectural — source of truth for learner product projection  
**Nature:** Framework-independent learner projection / orchestration layer  

**Packages:**
- `app/domain/student_experience/`
- `app/application/student_experience/`

**Depends on:** optional injected ports only (Student Twin, Adaptive Decision, Mission, Learning Journey, Learning Orchestrator). Does **not** import or modify those packages.

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
| Framework independence | No Flask, HTML, CSS, JavaScript, SQLAlchemy, or persistence in this milestone |
| Explainability | Every recommendation answers *why* using educational evidence |
| Navigation ownership | Experience owns presentation, workflow, projection, and navigation only |

```text
Learner (future UI)
        │
        ▼
Student Experience (this package)
        │
        ├── ports → Student Twin          (Learning Insights / Exam Readiness)
        ├── ports → Adaptive Decision     (Today's Recommendation / Revision)
        ├── ports → Mission               (Today's Session)
        ├── ports → Learning Journey      (Journey progress)
        └── ports → Learning Orchestrator (Learning Activity status)
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

## 4. Primary Experiences

### Student Home

Represents: greeting, exam countdown, exam readiness, today's recommendation, estimated study time, expected readiness improvement, recommendation explanation, Start Session action.

### Journey

Represents: current topic, completed topics, upcoming topics, prerequisite visibility (plain language), overall journey progress, estimated completion.

Must not expose curriculum graph concepts (nodes, edges, graph).

### Revision

Represents: today's highest-value revision, priority, estimated study time, expected educational benefit, explanation, alternative options.

Consumes **only** Adaptive Decision outputs.

### History

Represents: completed sessions, study time, readiness progression, mastered topics, revision history, recent achievements.

No raw event logs.

### Profile

Represents: current examination, study preferences, learning statistics, goals, account settings (presentation flags).

---

## 5. Navigation

Canonical surfaces (owned by Experience):

1. Home  
2. Journey  
3. Revision  
4. History  
5. Profile  

`ExperienceWorkspace` holds `active_surface` and examination / display presentation context. Navigating surfaces is Experience workflow ownership — analogous to Curriculum Studio's Founder workflow stages, but for the learner product shell.

---

## 6. Explanations

Every recommendation must answer:

> Why was this recommended?

Explanations are built from educational evidence phrases provided by Adaptive Decision, then translated into student language via `recommendation_explanation.py`.

Never mention Digital Twin, Adaptive Decision Engine, or Learning Orchestrator in learner-facing copy.

---

## 7. Authority Matrix

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

**Explicit non-authority:** Student Experience must not invent mastery, Topic Complete, readiness scores, or next actions.

---

## 8. Terminology Mapping

| Internal | Student |
|----------|---------|
| Student Digital Twin | Learning Insights |
| Adaptive Decision | Today's Recommendation |
| Readiness Score | Exam Readiness |
| Mission Engine | Today's Session |
| Learning Orchestrator | Learning Activity |

---

## 9. Future UI Roadmap

| Step | Scope |
|------|-------|
| V2-017B-A (this) | Domain + application foundation, ports, DTOs, explanations, tests |
| V2-017B-B+ | Flask blueprints / templates / JS for Home → Profile shell |
| Later | Session runtime UI, reflection UX, accessibility polish |

UI must remain a thin renderer of Experience snapshots. Templates must not embed Twin, Adaptive, Mission, or Journey mathematics.

---

## 10. Constraints (must not)

- Implement Flask / HTML / CSS / JavaScript in this milestone
- Implement persistence
- Duplicate Twin / Adaptive / Mission / Journey calculations
- Modify educational algorithms
- Expose internal architectural terminology to learners

---

## 11. Success Criteria

- Student experience model established  
- Navigation modelled  
- Projection services complete  
- Educational explanations translated  
- Internal architecture hidden from learners  
- Authority boundaries preserved  
- Framework independent  
- Ready for UI implementation  
