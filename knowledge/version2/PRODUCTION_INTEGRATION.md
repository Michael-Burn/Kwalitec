# Version 2 Production Integration

**Document ID:** V2-017-INTEGRATION  
**Status:** Architectural  
**Milestones:** V2-017 — Production Integration Foundation · **V2-018 — Production Experience Integration**  
**Package:** `app/infrastructure/`

This layer connects the framework-independent Version 2 application layer to host infrastructure through **adapters**, while preserving educational kernel purity.

No educational algorithms live in infrastructure. No domain rules move into repositories.

---

## Package Layout

```text
app/infrastructure/
├── adapters/
│   ├── curriculum_management/   → CurriculumManagementPort
│   ├── curriculum_ingestion/    → CurriculumIngestionPort
│   ├── education_platform/      → EducationPlatformPort
│   ├── student_twin/            → TwinPort + ExperienceTwinAdapter (StudentTwinPort)
│   ├── adaptive_learning/       → AdaptiveLearningPort (orchestrator)
│   ├── adaptive/                → ExperienceAdaptiveAdapter (AdaptiveDecisionPort)
│   ├── mission/                 → MissionPortAdapter + ExperienceMissionAdapter
│   ├── journey/                 → ExperienceJourneyAdapter (LearningJourneyPort)
│   ├── learning_orchestrator/   → composition + Evidence/Analytics ports
│   ├── orchestrator/            → ExperienceOrchestratorAdapter
│   └── student_experience/      → composition root, projection store, registry
├── persistence/                 → contracts, UoW, locking, stores
├── events/                      → envelope, versioning, serialization, registry
├── repositories/                → repository contracts + in-memory impls
└── diagnostics/                 → logging, correlation, tracing, metrics
```

---

## Port Adapter Contracts

### Studio / Orchestrator (V2-017)

| Adapter | Port | Application dependency |
|---------|------|------------------------|
| `CurriculumManagementAdapter` | Studio `CurriculumManagementPort` | `CurriculumManagementFacade` |
| `CurriculumIngestionAdapter` | Studio `CurriculumIngestionPort` | `CurriculumIngestionEngine` |
| `EducationPlatformAdapter` | Studio `EducationPlatformPort` | `EducationPlatform` |
| `StudentTwinAdapter` | Orchestrator `TwinPort` | Twin projection store (+ optional engine bridge) |
| `AdaptiveLearningAdapter` | Orchestrator `AdaptiveLearningPort` | Adaptive Decision bridge |
| `MissionPortAdapter` | Orchestrator `MissionPort` | Mission delivery store (+ optional engine) |
| `EvidencePortAdapter` / `AnalyticsPortAdapter` | Orchestrator ports | Evidence store / pipeline metrics |
| `LearningOrchestratorAdapter` | Composition root | `LearningOrchestrator` + ports |

### Student Experience (V2-018)

| Adapter | Port | Role |
|---------|------|------|
| `ExperienceTwinAdapter` | Experience `StudentTwinPort` | Learner summary / readiness / insights |
| `ExperienceAdaptiveAdapter` | Experience `AdaptiveDecisionPort` | Today's recommendation / revision (ADR-005) |
| `ExperienceMissionAdapter` | Experience `MissionPort` | Today's Session start / status |
| `ExperienceJourneyAdapter` | Experience `LearningJourneyPort` | Journey progress / topics |
| `ExperienceOrchestratorAdapter` | Experience `LearningOrchestratorPort` | Learning Activity status |

Composition: `StudentExperienceComposition` wires shared `ExperienceProjectionStore`, `PersistedExperienceRegistry`, events, optional `LearningOrchestratorAdapter` learning loop, and builds `StudentExperienceService`.

Adapters may depend on: Flask (presentation factory only), repositories, configuration, logging.

Adapters must not: bypass ports into foreign engines for educational math, invent next actions, or embed Twin/Adaptive algorithms.

---

## Persistence Strategy

### Aggregate ownership

Declared in `persistence/contracts.py` via `AggregateContract` / `AggregateOwner`. Examples:

- `DigitalTwin` → Student Twin (optimistic lock + snapshots)
- `EvidenceEvent` → Student Twin (append-only)
- `SubjectVersion` / `Publication` → Curriculum Management
- `DailyMission` → Mission
- `IntegrationEvent` → Orchestrator (append-only)
- Experience projections / workspaces / sessions → Student Experience infrastructure (V2-018)

### Experience persistence (V2-018)

| Concern | Owner |
|---------|-------|
| Twin / Adaptive / Journey / Mission / Activity projections | `ExperienceProjectionStore` + aggregate repos |
| Workspace / session presentation state | `PersistedExperienceRegistry` |
| Snapshots | `SnapshotStore` on projection writes |
| Unit of Work | Shared `UnitOfWork` on composition learning-loop boundary |
| Optimistic locking | `OptimisticLockGuard` on aggregate saves |

### Repository boundaries

Repositories persist opaque documents / snapshots / evidence. They never compute mastery, ROI, readiness, or publication eligibility.

### Unit-of-work strategy

`UnitOfWork` (and `SqlAlchemyUnitOfWork` when a session is injected):

- One boundary per request / orchestration cycle
- Repositories register writes while active
- Commit flushes; errors rollback
- Nested UoW is refused

### Transaction boundaries

`LearningOrchestratorAdapter.orchestrate` and `StudentExperienceComposition` learning loop run inside `UnitOfWork.transaction()` and correlation context.

---

## Event Model

Envelope (`IntegrationEvent`): identity, time, schema version, source, payload, correlation / causation.

### Catalogued types

**Core (V2-017)**

- `EvidenceRecorded`
- `TwinUpdated`
- `AdaptiveDecisionGenerated`
- `MissionUpdated`
- `CurriculumPublished`
- `CurriculumValidated`
- `LearningSessionCompleted`

**Experience surfaces (V2-018)**

- `StudentHomeViewed`
- `LearningSessionStarted`
- `RecommendationAccepted`
- `RecommendationDismissed`
- `JourneyViewed`
- `RevisionStarted`
- `HistoryViewed`
- `ProfileUpdated`

### Event versioning

`EventVersionPolicy` upcasts on read. Historical stored events are never rewritten. Missing upcasters refuse replay rather than guessing.

---

## Preview Retirement (V2-018)

Removed:

- `app/presentation/student/preview_ports.py`
- Preview-default factory wiring
- Temporary preview feature flags for Experience ports

Production adapters are the default. Tests may still inject fakes via explicit port overrides or `use_production_adapters=False`.

---

## Observability

Operational only (no educational KPIs in this layer):

- Structured logging with correlation fields
- Correlation / causation context vars
- Execution tracing spans
- Adapter diagnostics (availability, call/error counts)
- Pipeline metrics (`pipeline_started`, `adapter_invoked`, `transaction_committed`, …)
- Experience surface events (above)

Educational metrics belong to later Founder Intelligence work.

---

## Authority

See [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md) and ADRs 005–007.

---

## Success Posture

### V2-017

- Real infrastructure adapters exist and satisfy ports
- Event model + versioning established
- Repository / UoW / locking contracts defined
- Educational kernel packages unchanged in algorithm/law

### V2-018

- Student Experience production adapters active
- Preview infrastructure removed
- Complete learning loop executable through Mission → Twin → Adaptive
- Workspace / session / snapshot persistence foundations in place
- Ready for ORM / Alembic expansion without changing port contracts

SQLAlchemy ORM models and Alembic revisions for every aggregate remain additive follow-ons; contracts and in-memory foundations remain safe for dual-run until V2-020.
