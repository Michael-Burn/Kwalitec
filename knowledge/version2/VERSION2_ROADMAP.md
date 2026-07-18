# Version 2 Roadmap

**Document ID:** V2-001-ROADMAP  
**Status:** Implementation sequencing reference  
**Nature:** Milestone definitions — not a sprint backlog  

**Strategy context:** [`VERSION2_PRODUCT_STRATEGY.md`](../product/roadmap/VERSION2_PRODUCT_STRATEGY.md)  
**Architecture parent:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)

Version 2 is delivered as independently valuable milestones. Each milestone must improve educational decision quality even if work stopped afterwards. Evidence — not novelty — justifies scope expansion (Product Strategy).

---

## Milestone Sequence

```
PHASE I — CORE PLATFORM (COMPLETE)
  V2-001 Architecture
  V2-002 Learning Journey Domain
  V2-003 Learning Journey Engine
  V2-004 Curriculum Graph
  V2-005 Learning Session Runtime
  V2-006 Mission Engine
  V2-007 Learning Activity Engine
  V2-008 Instructional Blueprint Engine
  V2-009 Educational Composition Layer
  V2-010 Education Platform
  V2-011 Curriculum Management
  V2-012 Curriculum Ingestion
  V2-013 Student Digital Twin
  V2-014 Adaptive Decision Engine
  V2-015 Learning Orchestrator

PHASE II — PRODUCT EXPERIENCE
  V2-016 Curriculum Studio
  V2-017 Production Integration Foundation
  V2-017B Student Learning Experience

PHASE III — PRODUCTION
  V2-018 Infrastructure Deepening (ORM / cutover wiring)

PHASE IV — INTELLIGENCE
  V2-019 Founder Intelligence

PHASE V — PRODUCTION RELEASE
  V2-020 Version 1 Retirement
```

---

## PHASE I — CORE PLATFORM

**Status:** CORE PLATFORM COMPLETE

| ID | Milestone | Status | Primary docs / packages |
|----|-----------|--------|-------------------------|
| V2-001 | Architecture | ✓ Complete | [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md), `knowledge/version2/` |
| V2-002 | Learning Journey Domain | ✓ Complete | [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md), [`DOMAIN_IMPLEMENTATION.md`](DOMAIN_IMPLEMENTATION.md), `app/domain/learning_journey/` |
| V2-003 | Learning Journey Engine | ✓ Complete | [`LEARNING_JOURNEY_ENGINE.md`](LEARNING_JOURNEY_ENGINE.md), `app/application/learning_journey/` |
| V2-004 | Curriculum Graph | ✓ Complete | [`CURRICULUM_GRAPH.md`](CURRICULUM_GRAPH.md), `app/domain/curriculum/` |
| V2-005 | Learning Session Runtime | ✓ Complete | [`LEARNING_SESSION_RUNTIME.md`](LEARNING_SESSION_RUNTIME.md), `app/application/learning_session/` |
| V2-006 | Mission Engine | ✓ Complete | [`MISSION_ENGINE_2.md`](MISSION_ENGINE_2.md), [`MISSION_ADAPTER.md`](MISSION_ADAPTER.md), `app/application/mission_engine_v2/` |
| V2-007 | Learning Activity Engine | ✓ Complete | [`LEARNING_ACTIVITY_ENGINE.md`](LEARNING_ACTIVITY_ENGINE.md), `app/application/learning_activity/` |
| V2-008 | Instructional Blueprint Engine | ✓ Complete | ADR-002, `app/application/instructional_blueprint/` |
| V2-009 | Educational Composition Layer | ✓ Complete | Composition spine for educational services |
| V2-010 | Education Platform | ✓ Complete | [`EDUCATION_PLATFORM.md`](EDUCATION_PLATFORM.md), `app/application/education_platform/` |
| V2-011 | Curriculum Management | ✓ Complete | [`CURRICULUM_MANAGEMENT.md`](CURRICULUM_MANAGEMENT.md), `app/domain/curriculum_management/`, `app/application/curriculum_management/` |
| V2-012 | Curriculum Ingestion | ✓ Complete | [`CURRICULUM_INGESTION.md`](CURRICULUM_INGESTION.md), `app/application/curriculum_ingestion/` |
| V2-013 | Student Digital Twin | ✓ Complete | [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md), [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md), `app/domain/student_twin/`, `app/application/student_twin/` |
| V2-014 | Adaptive Decision Engine | ✓ Complete | [`ADAPTIVE_DECISION_ENGINE.md`](ADAPTIVE_DECISION_ENGINE.md), `app/application/adaptive_learning/` |
| V2-015 | Learning Orchestrator | ✓ Complete | [`LEARNING_ORCHESTRATOR.md`](LEARNING_ORCHESTRATOR.md), `app/domain/learning_orchestrator/`, `app/application/learning_orchestrator/` |

Phase I delivers the educational core: domain models, engines, composition, curriculum lifecycle, Twin, adaptive decisions, and live-event orchestration — without product UI or production cutover.

---

## PHASE II — PRODUCT EXPERIENCE

### V2-016 — Curriculum Studio

**Purpose**

Authoring, review, and publication UI over Curriculum Management and Curriculum Ingestion — so curriculum assets can be operated without code changes.

**Depends on**

- V2-011 Curriculum Management
- V2-012 Curriculum Ingestion

**Sub-milestones**

| ID | Scope | Status |
|----|-------|--------|
| V2-016A | Foundation — domain/application contracts, workflow, checklist, versioning, diff, docs (no UI) | ✓ Complete — [`CURRICULUM_STUDIO.md`](CURRICULUM_STUDIO.md), `app/domain/curriculum_studio/`, `app/application/curriculum_studio/` |
| V2-016B | Application services — Founder use-cases, port orchestration, dashboard projection, authority-safe DTOs (no UI) | ✓ Complete — [`CURRICULUM_STUDIO.md`](CURRICULUM_STUDIO.md) |
| V2-016C+ | Founder UI surfaces (routes / templates / JS) | Pending |

**Expected outcomes**

- Studio surfaces for asset review, versioning, validation, and publication
- Preview workflows aligned to management/ingestion snapshots
- Authoritative readiness contracts from V2-016A before UI work

**Must not**

- Embed educational decision math in the UI layer
- Bypass Curriculum Management publication / approval policies

---

### V2-017 — Production Integration Foundation

**Purpose**

Connect the framework-independent Version 2 application layer to production infrastructure through adapters, persistence contracts, integration events, and operational observability — without introducing educational logic into infrastructure.

**Status:** ✓ Complete — [`PRODUCTION_INTEGRATION.md`](PRODUCTION_INTEGRATION.md), [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md), ADR-005/006/007, `app/infrastructure/`

**Depends on**

- Phase I core engines (V2-003–015)
- V2-016A/B Curriculum Studio application contracts

**Expected outcomes**

- Real port adapters under `app/infrastructure/adapters/`
- Event model + schema versioning
- Repository / unit-of-work / optimistic locking contracts
- Authority Matrix + next-action authority (ADR-005)
- Operational diagnostics (correlation, tracing, adapter metrics)

**Must not**

- Change domain educational algorithms or Twin/Adaptive policies
- Introduce business rules into repositories
- Bypass application ports from frameworks into engines

---

### V2-017B — Student Learning Experience

**Purpose**

Student-facing product experience that exercises Journey, Session, Mission, Activity, Twin, and Orchestrator as one coherent learning path — consuming V2-017 adapters.

**Depends on**

- V2-017 Production Integration Foundation
- Phase I core engines (V2-003–015)
- Product Strategy evidence gates

**Sub-milestones**

| ID | Scope | Status |
|----|-------|--------|
| V2-017B-A | Foundation — domain/application projections, navigation, explanations, ports/DTOs, docs (no UI) | ✓ Complete — [`STUDENT_EXPERIENCE.md`](STUDENT_EXPERIENCE.md), `app/domain/student_experience/`, `app/application/student_experience/` |
| V2-017B-B+ | Student UI surfaces (routes / templates / JS) | Pending |

**Expected outcomes**

- Continuity of recommendation, session, and reflection
- Explainable next-action surfaces grounded in Twin state + Adaptive Decision authority (ADR-005)
- Framework-independent Student Experience model ready for UI (V2-017B-A)

**Must not**

- Ship without explainability and continuity invariants
- Let UI invent mastery or Topic Complete outside engine authority
- Duplicate Twin / Adaptive / Mission / Journey calculations in the experience layer

---

## PHASE III — PRODUCTION

### V2-018 — Infrastructure Deepening

**Purpose**

Deepen Version 2 persistence (ORM/Alembic where required), application factory wiring, and operational dual-run controls so the core runs as a product service alongside Version 1 until explicit retirement.

**Depends on**

- V2-017 Production Integration Foundation
- Phase II product surfaces sufficiently defined for cutover boundaries

**Expected outcomes**

- Durable ORM mappings for priority aggregates
- Startup / deployment paths for Version 2 engines
- Safe dual-run / feature-flag coexistence with Version 1

**Must not**

- Drop Version 1 data or silently cut over student traffic
- Bypass Alembic / StartupService safety guarantees

---

## PHASE IV — INTELLIGENCE

### V2-019 — Founder Intelligence

**Purpose**

Extend founder operational insight with journey-level educational signals (inactive journeys, stalled completion, reflection gaps, recommendation thrash) while keeping Founder systems non-authoritative over student Learning Mode.

**Depends on**

- Stable Phase I/II evidence and operational snapshots
- Existing Founder OS patterns (advisory only)

**Must not**

- Allow founder tools to mutate student journeys directly as a side channel

---

## PHASE V — PRODUCTION RELEASE

### V2-020 — Version 1 Retirement

**Purpose**

Explicit cutover from Version 1 educational runtime to Version 2 as the sole student path — after evidence gates and operational readiness are met.

**Depends on**

- V2-017B Student Learning Experience validated
- V2-017/V2-018 infrastructure dual-run production-ready
- Product Strategy evidence gates

**Expected outcomes**

- Version 2 is the authoritative educational runtime
- Version 1 paths retired under a controlled migration

**Must not**

- Retire Version 1 without explainability, continuity, and dual-run confidence
- Treat novelty as proof of educational value without measurement

---

## Cross-Milestone Constraints

| Constraint | Applies to |
|------------|------------|
| No Constitution contradiction | All |
| V1 runtime safe until explicit cutover (V2-020) | All implementation milestones |
| Deterministic core paths | Phase I engines |
| Evidence before opinion | Phase I Twin / Adaptive / Orchestrator → Phase IV |
| Documentation in `knowledge/version2/` remains concept authority | All |

---

## Closing

This roadmap is the implementation sequence for Version 2. Phase I (Core Platform) is complete. New milestones may be inserted only if they refine — not redefine — the Learning Journey architecture established in V2-001. Remaining work is product experience, production integration, founder intelligence, and Version 1 retirement.
