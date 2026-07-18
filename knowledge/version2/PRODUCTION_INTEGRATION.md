# Version 2 Production Integration

**Document ID:** V2-017-INTEGRATION  
**Status:** Architectural  
**Milestone:** V2-017 — Production Integration Foundation  
**Package:** `app/infrastructure/`

This milestone connects the framework-independent Version 2 application layer to host infrastructure through **adapters**, while preserving educational kernel purity.

No educational algorithms live in infrastructure. No domain rules move into repositories.

---

## Package Layout

```text
app/infrastructure/
├── adapters/
│   ├── curriculum_management/   → CurriculumManagementPort
│   ├── curriculum_ingestion/    → CurriculumIngestionPort
│   ├── education_platform/      → EducationPlatformPort
│   ├── student_twin/            → TwinPort
│   ├── adaptive_learning/       → AdaptiveLearningPort
│   ├── mission/                 → MissionPort (orchestrator)
│   └── learning_orchestrator/   → composition + Evidence/Analytics ports
├── persistence/                 → contracts, UoW, locking, stores
├── events/                      → envelope, versioning, serialization, registry
├── repositories/                → repository contracts + in-memory impls
└── diagnostics/                 → logging, correlation, tracing, metrics
```

---

## Port Adapter Contracts

Each adapter satisfies an existing application port. Application services never import Flask, SQLAlchemy, or infrastructure adapters.

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

Adapters may depend on: Flask, SQLAlchemy sessions (injected), repositories, configuration, logging.

Adapters must not: bypass ports into foreign engines, invent next actions, or embed Twin/Adaptive math.

---

## Persistence Strategy

### Aggregate ownership

Declared in `persistence/contracts.py` via `AggregateContract` / `AggregateOwner`. Examples:

- `DigitalTwin` → Student Twin (optimistic lock + snapshots)
- `EvidenceEvent` → Student Twin (append-only)
- `SubjectVersion` / `Publication` → Curriculum Management
- `DailyMission` → Mission
- `IntegrationEvent` → Orchestrator (append-only)

### Repository boundaries

Repositories persist opaque documents / snapshots / evidence. They never compute mastery, ROI, readiness, or publication eligibility.

### Unit-of-work strategy

`UnitOfWork` (and `SqlAlchemyUnitOfWork` when a session is injected):

- One boundary per request / orchestration cycle
- Repositories register writes while active
- Commit flushes; errors rollback
- Nested UoW is refused

### Transaction boundaries

`LearningOrchestratorAdapter.orchestrate` runs inside `UnitOfWork.transaction()` and correlation context.

### Optimistic locking

`OptimisticLockGuard` / `VersionToken` on mutable aggregates. Conflicts raise `OptimisticLockError` (operational metric: `optimistic_lock_conflict`).

### Snapshot persistence

`SnapshotStore` + `SnapshotRepository` — projected aggregate envelopes with schema version.

### Evidence persistence

`EvidenceStore` + `EvidenceRepository` — append-only; duplicate ids rejected.

---

## Event Model

Envelope (`IntegrationEvent`):

| Field | Role |
|-------|------|
| `event_id` | Identifier |
| `occurred_at` | Timestamp |
| `event_version` | Schema version |
| `source` | Emitting adapter / component |
| `payload` | Opaque body |
| `correlation_id` | Request / pipeline correlation |
| `causation_id` | Causal parent |

Catalogued types:

- `EvidenceRecorded`
- `TwinUpdated`
- `AdaptiveDecisionGenerated`
- `MissionUpdated`
- `CurriculumPublished`
- `CurriculumValidated`
- `LearningSessionCompleted`

### Event versioning

`EventVersionPolicy` upcasts on read. Historical stored events are never rewritten. Missing upcasters refuse replay rather than guessing. Future versions newer than supported are rejected.

---

## Observability

Operational only (no educational KPIs in this layer):

- Structured logging with correlation fields
- Correlation / causation context vars
- Execution tracing spans
- Adapter diagnostics (availability, call/error counts)
- Pipeline metrics (`pipeline_started`, `adapter_invoked`, `transaction_committed`, …)

Educational metrics belong to later Founder Intelligence work.

---

## Authority

See [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md) and ADRs 005–007.

---

## Success Posture (V2-017)

- Real infrastructure adapters exist and satisfy ports
- Event model + versioning established
- Repository / UoW / locking contracts defined
- Educational kernel packages unchanged in algorithm/law
- Version 2 is executable inside production infrastructure composition roots

SQLAlchemy ORM models and Alembic revisions for every aggregate remain additive follow-ons; V2-017 defines contracts and in-memory foundations safe for dual-run.
