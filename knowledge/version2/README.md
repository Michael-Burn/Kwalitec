# Version 2 Educational Architecture

**Authority:** Informational (index) · points to Foundational / Architectural / Normative docs  

Authoritative educational architecture for Kwalitec Version 2.

**Start here:** [`V2_DESIGN_MANIFESTO.md`](V2_DESIGN_MANIFESTO.md) — philosophical foundation for all Version 2 work.

Established by **V2-001 — Learning Journey Domain Architecture** (documentation).

Domain code foundation delivered by **V2-002 — Learning Journey Domain Foundation** (`app/domain/learning_journey/`).

Application orchestration delivered by **V2-003 — Learning Journey Engine** (`app/application/learning_journey/`).

Curriculum knowledge model delivered by **V2-004 — Curriculum Graph Foundation** (`app/domain/curriculum/`).

Session execution delivered by **V2-005 — Learning Session Runtime** (`app/application/learning_session/`).

Activity execution inside sessions delivered by **V2-008 — Learning Activity Engine** (`app/application/learning_activity/`, `app/domain/learning_activity/`) — see [`LEARNING_ACTIVITY_ENGINE.md`](LEARNING_ACTIVITY_ENGINE.md).

Mission orchestration delivered by **Mission Engine 2.0** (`app/application/mission_engine_v2/`) — milestone V2-007; see [`MISSION_ENGINE_2.md`](MISSION_ENGINE_2.md).

Mission cutover routing delivered by **Mission Adapter** (`app/application/mission_adapter/`) — sole public entry point for mission generation; see [`MISSION_ADAPTER.md`](MISSION_ADAPTER.md).

Educational Core composition delivered by **Education Platform** (`app/application/education_platform/`) — sole public orchestration facade over Curriculum → Blueprint → Journey → Session → Activity → Mission; see [`EDUCATION_PLATFORM.md`](EDUCATION_PLATFORM.md).

Curriculum asset and publication management delivered by **Curriculum Management** (`app/domain/curriculum_management/`, `app/application/curriculum_management/`) — foundation for Curriculum Studio and Curriculum Ingestion; see [`CURRICULUM_MANAGEMENT.md`](CURRICULUM_MANAGEMENT.md).

Deterministic document-to-structure ingestion delivered by **Curriculum Ingestion** (`app/domain/curriculum_ingestion/`, `app/application/curriculum_ingestion/`) — classify → extract → normalise → validate only; see [`CURRICULUM_INGESTION.md`](CURRICULUM_INGESTION.md).

Evidence-driven learner state delivered by **Student Digital Twin 2.0** (`app/domain/student_twin/`, `app/application/student_twin/`) — deterministic mastery / confidence / retention / readiness / explainable recommendations from evidence only; see [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md) · [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md).

Deterministic revision decisions delivered by **Adaptive Decision Engine** (`app/domain/adaptive_learning/`, `app/application/adaptive_learning/`) — Phase 1 revision interventions with priority, educational ROI, and explainability; see [`ADAPTIVE_DECISION_ENGINE.md`](ADAPTIVE_DECISION_ENGINE.md).

Live learner event coordination delivered by **Learning Orchestrator** (`app/domain/learning_orchestrator/`, `app/application/learning_orchestrator/`) — Evidence → Twin → Adaptive Decision → Mission → Analytics via ports; see [`LEARNING_ORCHESTRATOR.md`](LEARNING_ORCHESTRATOR.md).

Founder curriculum readiness delivered by **Curriculum Studio** (`app/domain/curriculum_studio/`, `app/application/curriculum_studio/`) — thin orchestration over Management/Ingestion/Platform ports, workflow, checklist, preview, versioning, dashboard, and structural diffs (UI deferred); see [`CURRICULUM_STUDIO.md`](CURRICULUM_STUDIO.md).

Production integration foundation delivered by **V2-017** (`app/infrastructure/`) — port adapters, persistence contracts, integration events, observability; see [`PRODUCTION_INTEGRATION.md`](PRODUCTION_INTEGRATION.md) · [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md) · ADR-005/006/007.

Learner product projection delivered by **Student Experience** (`app/domain/student_experience/`, `app/application/student_experience/`) — Home / Journey / Revision / History / Profile orchestration over Twin, Adaptive Decision, Mission, Journey, and Orchestrator ports (UI deferred); see [`STUDENT_EXPERIENCE.md`](STUDENT_EXPERIENCE.md).

Documentation authority consolidated by **V2-013 P0.1 — Digital Twin Documentation Authority**.

---

## Documentation Structure

```text
knowledge/version2/
├── V2_DESIGN_MANIFESTO.md          ← Foundational (read first)
├── VERSION2_ARCHITECTURE.md        ← Architectural overview
├── VERSION2_ROADMAP.md
├── EDUCATIONAL_PRINCIPLES.md       ← Normative educational rules
├── EDUCATION_PLATFORM.md           ← Education Platform
├── CURRICULUM_MANAGEMENT.md        ← Curriculum Management
├── CURRICULUM_INGESTION.md         ← Curriculum Ingestion
├── CURRICULUM_STUDIO.md            ← Curriculum Studio (Founder readiness)
├── PRODUCTION_INTEGRATION.md       ← V2-017 infrastructure adapters / persistence
├── STUDENT_EXPERIENCE.md           ← Student Experience (learner projections)
├── AUTHORITY_MATRIX.md             ← Cross-context authority map
├── CURRICULUM_GRAPH.md / CURRICULUM_MODEL.md
├── STUDENT_DIGITAL_TWIN.md         ← Student Digital Twin (how)
├── DIGITAL_TWIN_PHILOSOPHY.md      ← Digital Twin Philosophy (why)
├── ADAPTIVE_DECISION_ENGINE.md     ← Adaptive Decision Engine (revision phase)
├── LEARNING_ORCHESTRATOR.md        ← Learning Orchestrator (live events)
├── V2_ARCHITECTURE_DESIGN_REVIEW.md ← Independent design critique (advisory)
├── ARCHITECTURE_DECISIONS/         ← Architecture Decision Records
│   ├── ADR-001-Educational-Core.md
│   ├── ADR-002-Instructional-Blueprint.md
│   ├── ADR-003-Education-Platform.md
│   ├── ADR-004-Digital-Twin.md
│   ├── ADR-005-Single-Next-Action-Authority.md
│   ├── ADR-006-Authority-Boundaries.md
│   └── ADR-007-Legacy-Retirement-Strategy.md
├── LEARNING_JOURNEY_*.md / LEARNING_SESSION_*.md / …
└── … companion specs
```

**Outside this folder (Twin hierarchy companions):**

| Document | Authority | Role |
|----------|-----------|------|
| [`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md) | Normative | Twin constitutional law (*what must be obeyed*) |
| [`../../STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Architectural | Epic Twin domain architecture (canonical learner-state law) |

**Hierarchy (conceptual):**

```text
Version 2
├── Design Manifesto (Foundational)
├── Educational Platform
├── Curriculum Management
├── Curriculum Ingestion
├── Student Digital Twin
│   └── Digital Twin Philosophy
├── Adaptive Decision Engine
├── Learning Orchestrator
├── Production Integration (adapters / events / persistence)
└── Architecture Decisions
```

`ARCHITECTURE_DECISIONS/` is the Version 2 ADR folder (created by V2-013 P0.1). Do not invent parallel Twin law outside the Philosophy → Constitution → Architecture triad. Next-action authority is ADR-005; cross-context ownership is [`AUTHORITY_MATRIX.md`](AUTHORITY_MATRIX.md).

---

## Authority Classes

Version 2 documentation uses consistent authority labels:

| Class | Meaning |
|-------|---------|
| **Foundational** | Philosophical / design conscience — orients all work |
| **Architectural** | Structures, boundaries, and implementation contracts |
| **Normative** | Binding rules that must not be violated |
| **Informational** | Indexes, roadmaps, and navigational aids |

---

## Documents

| Document | Authority | Role |
|----------|-----------|------|
| [V2_DESIGN_MANIFESTO.md](V2_DESIGN_MANIFESTO.md) | Foundational | Version 2 design philosophy — read first |
| [VERSION2_ARCHITECTURE.md](VERSION2_ARCHITECTURE.md) | Architectural | High-level vision, goals, non-goals, relationship to Version 1 |
| [LEARNING_JOURNEY_DOMAIN.md](LEARNING_JOURNEY_DOMAIN.md) | Architectural | Domain entities (Journey, Session, Evidence, Reflection, …) |
| [LEARNING_JOURNEY_ENGINE.md](LEARNING_JOURNEY_ENGINE.md) | Architectural | V2-003 engine responsibilities, sequences, consumer contracts |
| [LEARNING_SESSION_RUNTIME.md](LEARNING_SESSION_RUNTIME.md) | Architectural | V2-005 session runtime lifecycle, evidence, reflection, scheduling |
| [LEARNING_ACTIVITY_ENGINE.md](LEARNING_ACTIVITY_ENGINE.md) | Architectural | V2-008 activity sequencing, transitions, completion signal inside sessions |
| [MISSION_ENGINE_2.md](MISSION_ENGINE_2.md) | Architectural | Mission Engine 2.0 lifecycle, scheduling, V1 coexistence |
| [MISSION_ADAPTER.md](MISSION_ADAPTER.md) | Architectural | Mission Adapter routing, parallel validation, migration, audit |
| [EDUCATION_PLATFORM.md](EDUCATION_PLATFORM.md) | Architectural | V2-010 Educational Composition Layer — EducationPlatform facade |
| [CURRICULUM_MANAGEMENT.md](CURRICULUM_MANAGEMENT.md) | Architectural | V2-011 Curriculum Management — assets, versions, publication lifecycle |
| [CURRICULUM_INGESTION.md](CURRICULUM_INGESTION.md) | Architectural | V2-012 Curriculum Ingestion — classify, extract, normalise, validate |
| [STUDENT_DIGITAL_TWIN.md](STUDENT_DIGITAL_TWIN.md) | Architectural | V2-013 Student Digital Twin 2.0 — evidence-driven learner state (*how*) |
| [DIGITAL_TWIN_PHILOSOPHY.md](DIGITAL_TWIN_PHILOSOPHY.md) | Foundational | Twin philosophy — principles, responsibilities, ethics (*why*) |
| [ADAPTIVE_DECISION_ENGINE.md](ADAPTIVE_DECISION_ENGINE.md) | Architectural | V2-014 Adaptive Decision Engine — revision decisions, priority, ROI |
| [LEARNING_ORCHESTRATOR.md](LEARNING_ORCHESTRATOR.md) | Architectural | V2-015 Learning Orchestrator — live event pipeline coordination |
| [ARCHITECTURE_DECISIONS/](ARCHITECTURE_DECISIONS/) | Architectural | Version 2 Architecture Decision Records |
| [STATE_MACHINE.md](STATE_MACHINE.md) | Normative | Lawful and invalid state transitions |
| [EDUCATIONAL_PRINCIPLES.md](EDUCATIONAL_PRINCIPLES.md) | Normative | Binding Version 2 educational rules |
| [CURRICULUM_MODEL.md](CURRICULUM_MODEL.md) | Architectural | Subject → Chapter → Topic structure and completion criteria |
| [CURRICULUM_GRAPH.md](CURRICULUM_GRAPH.md) | Architectural | V2-004 Curriculum Graph model, algorithms, integration |
| [MIGRATION_STRATEGY.md](MIGRATION_STRATEGY.md) | Informational | Version 1 → Version 2 concept mapping |
| [VERSION2_ROADMAP.md](VERSION2_ROADMAP.md) | Informational | Implementation milestones V2-001 … V2-015 |
| [DOMAIN_IMPLEMENTATION.md](DOMAIN_IMPLEMENTATION.md) | Informational | V2-002 code ↔ V2-001 architecture mapping |
| [V2_ARCHITECTURE_DESIGN_REVIEW.md](V2_ARCHITECTURE_DESIGN_REVIEW.md) | Informational | Independent Core Platform + Studio Foundation critique (advisory; non-normative) |

### Architecture Decision Records

| ADR | Topic |
|-----|-------|
| [ADR-001-Educational-Core.md](ARCHITECTURE_DECISIONS/ADR-001-Educational-Core.md) | Why Educational Core is separated into bounded contexts |
| [ADR-002-Instructional-Blueprint.md](ARCHITECTURE_DECISIONS/ADR-002-Instructional-Blueprint.md) | Why pedagogy is independent from curriculum |
| [ADR-003-Education-Platform.md](ARCHITECTURE_DECISIONS/ADR-003-Education-Platform.md) | Why orchestration is separated from educational engines |
| [ADR-004-Digital-Twin.md](ARCHITECTURE_DECISIONS/ADR-004-Digital-Twin.md) | Why the Digital Twin is evidence-driven and deterministic |

## Authority

These documents define Version 2 **educational concepts**. They are subordinate to the Educational Constitution and do not replace the Student Digital Twin Constitution or Learning Evidence Model.

V2-001 alone does not change Version 1 production behaviour. V2-002 adds a pure domain package with **no** Version 1 behavioural coupling (no routes, ORM, migrations, or feature flags). V2-003 adds a framework-independent application engine that coordinates that domain — still without Flask routes, persistence writes, UI, migrations, or feature flags. V2-004 adds the Curriculum Graph bounded context (`app/domain/curriculum/`) as the structural sequencing source for future Journey / Mission / Twin integration — still without Flask routes, persistence, UI, or Version 1 behavioural changes. V2-005 adds the Learning Session Runtime (`app/application/learning_session/`) as the session execution layer — still without Flask routes, persistence, UI, or Version 1 behavioural changes. V2-008 adds the Learning Activity Engine (`app/application/learning_activity/`) as the in-session activity execution layer — still without Flask routes, persistence, UI, or Version 1 behavioural changes, and without modifying Session Runtime / Journey / Mission packages. Mission Engine 2.0 (`app/application/mission_engine_v2/`) adds mission generation / scheduling / lifecycle / dashboard DTO orchestration in parallel with Version 1 `MissionService` — still without Flask routes, persistence writes, UI, or Version 1 behavioural changes. The Mission Adapter (`app/application/mission_adapter/`) adds the sole public routing / comparison / audit entry point for mission generation — still without Flask routes, persistence writes, UI, or Version 1 behavioural changes until migration phases lawfully cut over. V2-010 adds the Educational Composition Layer (`app/application/education_platform/`) as the sole public `EducationPlatform` facade coordinating Curriculum → Blueprint → Journey → Session → Activity → Mission via ports — still without Flask routes, persistence, UI, educational rule ownership, or modifications to those engines. V2-011 adds Curriculum Management (`app/domain/curriculum_management/`, `app/application/curriculum_management/`) for versioned subject assets and publication lifecycle — still without Flask routes, persistence, PDF parsing, or modifications to EducationPlatform / educational engines. V2-012 adds Curriculum Ingestion (`app/domain/curriculum_ingestion/`, `app/application/curriculum_ingestion/`) for deterministic classification / extraction / normalisation / validation of abstract curriculum documents — still without Flask routes, persistence, AI reasoning, teaching, session / activity / mission generation, or modifications to EducationPlatform / Curriculum Management. V2-013 adds Student Digital Twin 2.0 (`app/domain/student_twin/`, `app/application/student_twin/`) as a deterministic evidence-driven learner-state bounded context — still without Flask routes, persistence, curriculum storage, teaching, or AI ownership of Twin mutations. **V2-013 P0.1** consolidates Twin documentation authority (Philosophy ↔ Constitution ↔ Architecture), the Version 2 Design Manifesto, and Architecture Decision Records — documentation only; no implementation changes. V2-014 adds the Adaptive Decision Engine (`app/domain/adaptive_learning/`, `app/application/adaptive_learning/`) for deterministic Phase-1 revision decisions with priority, educational ROI, and explainability — still without Flask routes, persistence, AI, content generation, or modifications to Twin / Education Platform / Mission / Curriculum Management / Curriculum Ingestion. V2-015 adds the Learning Orchestrator (`app/domain/learning_orchestrator/`, `app/application/learning_orchestrator/`) for live learner event coordination (Evidence → Twin → Adaptive Decision → Mission → Analytics) via ports — still without Flask routes, persistence, AI, educational rule ownership, or modifications to Education Platform / Twin / Adaptive / Mission / Curriculum packages.

## Related

- [`../product/roadmap/VERSION2_PRODUCT_STRATEGY.md`](../product/roadmap/VERSION2_PRODUCT_STRATEGY.md) — strategic decision framework
- [`../../PRODUCT_BLUEPRINT.md`](../../PRODUCT_BLUEPRINT.md) — product vision
- [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational law
- [`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md) — Digital Twin constitutional law
