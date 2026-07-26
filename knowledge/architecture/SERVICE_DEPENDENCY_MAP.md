# MS-001 — Service Dependency Map

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)

Documents every service involved in **navigation / session / recommendation**, with dependencies, cycles, duplication, and coupling.

---

## 1. Layers involved in “what to study” and session flow

```
Presentation (Flask)
  student / session / dashboard / mission / study_plan / calibration / alpha
        │
        ▼
Application facades (ports)
  StudentExperienceService · SessionExperienceService · EducationalStateService
  LearningOrchestrator (hooks) · AdaptiveDecisionEngine (optional)
        │
        ▼
Infrastructure adapters / stores
  ExperienceMissionAdapter · ExperienceProjectionStore · SessionDocumentStore
  Opaque bridges · Orchestrator adapters
        │
        ▼
Legacy domain services (SQL)          Curriculum
  Planning · Mission · StudySession · CurriculumService ← Engine JSON/DB
  Recommendation · AdaptiveLearning · Readiness · Lifecycle
```

**Critical seam:** Application facades do **not** import `app/services/*`. Legacy services do **not** call Student/Session Experience. Coupling is only via future/missing bridge adapters.

---

## 2. Navigation-related services (catalogue)

### 2.1 Presentation helpers (not domain owners)

| Module | Role | Depends on |
|---|---|---|
| `app/presentation/consolidation.py` | Sole-runtime redirects | `v2_flags` |
| `app/presentation/student/navigation.py` | Canonical nav tree endpoints | ExperienceSurface domain |
| `app/presentation/session/navigation.py` | Session step endpoints | SessionSurface domain |
| `app/presentation/student/views.py` | load_page / start_todays_session | StudentExperienceService |
| `app/presentation/session/views.py` | resume + flow helpers | SessionExperienceService |

### 2.2 Application facades

| Service | Navigation role | Dependencies |
|---|---|---|
| `StudentExperienceService` | Home CTA start_session; dashboard projections | Ports: Twin, Adaptive, Mission, Journey, Orchestrator; `EducationalStateService`; projection services |
| `HomeService` | Assembles next-action UX | EducationalState / ports; ExplanationService |
| `DashboardService` | Surface routing inside experience | Home/Journey/Revision/History/Profile + registry |
| `SessionExperienceService` | Linear session flow | SessionRuntime, Activity, Mission, Twin, Adaptive ports |
| `EducationalStateService` | Merges twin + recommendation + todays_session | Same ports |
| `LearningOrchestrator` (+ pipelines) | Post-start learning loop (when hooked) | Its own Mission/Twin/Adaptive/Evidence adapters |

### 2.3 Legacy services on the request path

| Service | Role in navigation/session | Key dependencies |
|---|---|---|
| `PlanningService` | Creates today’s Mission (topic + tasks) | StudyPlanService, MissionService, CurriculumService, LearningLifecycleService |
| `MissionService` | CRUD/status for Mission/MissionTask | StudyPlanService (lazy) |
| `StudySessionService` | Start/finish/outcome/feedback | MissionService, LearningService, EducationalEvidenceAuthority; lazy AdaptiveLearning, Explainability |
| `RecommendationService` | Dashboard “next” card | ReadinessService; lazy Lifecycle, Curriculum, Planning (labels), StudyPlan |
| `AdaptiveLearningService` | Mastery, weak topics, review schedule | CurriculumService, EvidenceAuthority (lazy) |
| `ReadinessService` | Coverage, backlog, readiness aggregates | TopicProgress / curriculum summaries |
| `LearningLifecycleService` | Learning vs Revision stage | CurriculumService, StudyPlanService; lazy AdaptiveLearning, Planning (labels) |
| `StudyPlanService` | Active plan, week plans, wizard persistence | PlanningService (lazy, week generation) |
| `EducationalExplainabilityService` | Narratives for UI | StudySession constants (lazy) |
| `EducationalContinuityService` | History protection across plan changes | StudyPlanService |
| `EducationalEvidenceAuthority` | Gates mastery updates | Used by AdaptiveLearning / StudySession |
| `AlphaOnboardingService` | Redirect before dashboard | User flags |
| `PresentationTelemetryService` | Records nav/session events | DB/telemetry sink |
| `WelcomeService` / dismiss routes | First-run UX | Dashboard |

### 2.4 Built but unwired (from live HTTP path)

| Package | Notes |
|---|---|
| `app/application/mission_engine/` | Imported by self + tests only |
| `app/application/mission_engine_v2/` | Same |
| `AdaptiveDecisionEngine` | Instantiated in opaque bridges when inject flag on, but twin/mission/journey engines remain `None`; inputs not from SQL |

---

## 3. Dependency diagram (legacy core)

```
                    CurriculumService ◄──── Curriculum Engine
                           ▲
           ┌───────────────┼────────────────┐
           │               │                │
   PlanningService   AdaptiveLearning   ReadinessService
           │               │                │
           │               └───────┬────────┘
           │                       │
           ▼                       ▼
     MissionService      RecommendationService
           ▲                       │
           │                       │ (labels)
           │                       ▼
   StudySessionService ◄─── (private Planning label helpers)
           │
           ▼
   EvidenceAuthority / TopicProgress
```

`LearningLifecycleService` sits beside Planning and Recommendation (stage gate).

---

## 4. Circular dependencies

| Cycle | Mitigation | Risk |
|---|---|---|
| `PlanningService` ↔ `StudyPlanService` | Planning imports StudyPlan at module scope; StudyPlan imports Planning **lazily** inside functions | Moving Planning import to module scope in StudyPlan breaks import; hard to reason about |
| Label helpers | Recommendation & Lifecycle call `PlanningService._resolve_official_topic_code` / `_topic_study_label` | Cross-service use of **private** API |

No import cycle found between StudentExperience and legacy services (because they do not connect).

---

## 5. Duplicated logic

| Concern | Locations | Notes |
|---|---|---|
| Next incomplete topic | `CurriculumService.get_next_incomplete_topic` used by Planning + Recommendation labels | Math not duplicated — good |
| Topic human labels | Private Planning helpers used by 3 services | Should be shared public helper |
| Daily vs week sequencing | Leaf-order incomplete vs Kahn prerequisites | Two algorithms |
| “What next” narrative | RecommendationService rules vs Planning mission title vs Adaptive demo vs AdaptiveDecisionEngine | Product-visible duplication |
| Mission lifecycle | SQL MissionService vs ExperienceMissionAdapter vs MissionEngine* packages | Three conceptual models |
| Mastery / readiness | AdaptiveLearningService + ReadinessService vs Twin opaque projections | Parallel truths |

---

## 6. Coupling assessment

| Coupling | Severity | Evidence |
|---|---|---|
| Blueprint → many services in one route (dashboard/mission) | High | Fat composition in route handlers |
| Recommendation → Planning private methods | Medium | Underscore API leakage |
| Planning ↔ StudyPlan | Medium | Bidirectional domain ownership of week vs day |
| Presentation consolidation → env flag | Low (intentional) | Clean gate |
| Experience facades → ports only | Low (healthy) | Hexagonal boundary held |
| Experience adapters → legacy SQL | **Missing** | Highest product risk under sole runtime |
| Session resume → workspace store | Medium | In-memory default → multi-worker / restart loss |

---

## 7. Recommendation pipeline (service view)

Documented fully in narrative form here; see also `SOURCE_OF_TRUTH_ANALYSIS.md`.

### Legacy mission topic (authoritative for legacy study)

**Inputs:** `user_id`, active `StudyPlan`, `date`, `TopicProgress`, curriculum order, lifecycle stage.  
**Algorithm:**  
- Learning → first incomplete leaf (`get_next_incomplete_topic`).  
- Revision → ordinal template rotation + weakest completed topic label.  
**Service:** `PlanningService`.  
**Fallback:** No plan / outside window → no mission; generic mission replace after curriculum bind.

### Legacy recommendation card

**Inputs:** Readiness backlog/weak/coverage, ExamTimeline, BurnoutMonitor, lifecycle stage.  
**Algorithm:** Priority-sorted rule sets; dedupe by title; limit N.  
**Service:** `RecommendationService`.  
**Fallback:** Empty list → no card; EI orchestrator may replace when flagged.

### Canonical Home recommendation

**Inputs:** Opaque Adaptive document (seeded demo by default).  
**Algorithm:** Projection only in HomeService (no curriculum math).  
**Services:** Adaptive port (+ optional AdaptiveDecisionEngine if injected with real context — not default).  
**Fallback:** Empty recommendation → CTA disabled / empty strings via start_action helpers.

---

## 8. Session state locations (service perspective)

| Location | Created by | Modified by | Destroyed / lost |
|---|---|---|---|
| SQL `Mission.status` | Planning / MissionService | StudySession / MissionService | Soft: Completed remains as history |
| Opaque mission doc | seed / start_session | adapter start/complete | Process restart if not durable |
| `SessionWorkspace` | open_session | begin/advance/complete | Close; restart if not durable |
| Flask `wizard_data` | study_plan wizard | each step | Pop on complete/cancel |
| localStorage timer | study_session.js | timer ticks | Manual / browser clear |
| ExperienceRegistry session handle | start_session facade | — | Process memory |
| Orchestrator evidence / aggregates | learning loop | evidence adapter | Separate plane |

---

## 9. Summary for MS-001

- Navigation decisions are split across **env flag**, **legacy planning**, and **canonical ports**.  
- The healthiest dependency boundary is the Experience **port/adapter** design — but adapters currently depend on **opaque stores**, not legacy educational services.  
- Safest refactoring target for trust: introduce explicit bridge adapters and collapse duplicate “next” producers behind one authority — without breaking CurriculumService traversal invariants.
