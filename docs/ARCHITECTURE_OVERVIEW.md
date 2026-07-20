# Kwalitec Architecture Overview

**Milestone:** APP-003 — Architecture Governance  
**Status:** Governing — Version 2 structural map  
**Authority:** Descriptive map bound by the [Architecture Constitution](ARCHITECTURE_CONSTITUTION.md)  
**Date:** 2026-07-20  

---

## 1. Purpose

This document maps the Version 2 Educational Operating System: layers, major subsystems, and how educational authority flows. It does not specify algorithms, schemas, or product copy.

For actors and external systems, see [SYSTEM_CONTEXT.md](SYSTEM_CONTEXT.md).  
For import and construction rules, see [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md).  
For binding decisions, see [docs/adr/](adr/).

---

## 2. Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Web / Presentation (`src/web`, Flask blueprints)           │
│  HTTP, auth chrome, templates, request scoping              │
└───────────────────────────┬─────────────────────────────────┘
                            │ calls use-cases / read models
┌───────────────────────────▼─────────────────────────────────┐
│  Application (`src/application`)                            │
│  Commands, queries, handlers, pipeline, ports, DTOs         │
│  Composition root constructs and injects collaborators      │
└───────────────────────────┬─────────────────────────────────┘
                            │ uses domain engines + ports
┌───────────────────────────▼─────────────────────────────────┐
│  Domain (`src/domain`)                                      │
│  Educational Core + projection engines (pure Python)         │
└───────────────────────────▲─────────────────────────────────┘
                            │ implements ports
┌───────────────────────────┴─────────────────────────────────┐
│  Infrastructure (`src/infrastructure`)                      │
│  SQLAlchemy persistence, runtime, events, AI enrichment     │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Owns | Must not |
|---|---|---|
| **Domain** | Educational meaning, invariants, deterministic engines | Flask, ORM, AI SDKs, HTTP, persistence |
| **Application** | Use-case orchestration, ports, pipeline sequencing, DTOs | Educational math ownership; ORM outside composition |
| **Infrastructure** | Adapters: DB, clock, UUID, events, AI providers | Authoritative educational decisions |
| **Web** | HTTP surface, middleware, blueprint wiring | Domain construction; educational reasoning |

Legacy Flask product surfaces under `app/` coexist during migration. New Educational OS authority lives under `src/`. Root [`ARCHITECTURE.md`](../ARCHITECTURE.md) documents the historical application map.

---

## 3. Educational Operating System Subsystems

| Subsystem | Package | Authority |
|---|---|---|
| Educational Core | `domain.education.*` | Evidence, twin, diagnosis, hypothesis, priority, intention, strategy, decision, orchestrator, episodes, subject knowledge |
| Mission Generation | `domain.mission_generation` | Deterministic `MissionSpecification` |
| Study Planning | `domain.study_planning` | Deterministic `StudyPlan` |
| Progress Evaluation | `domain.progress_evaluation` | Deterministic `ProgressReport` |
| Recommendation Engine | `domain.recommendation` | Deterministic `RecommendationSpecification` |
| Explainability | `domain.explainability` | `EducationalExplanation` + decision trace |
| Student Experience | `domain.student_experience` | Presentation projection only |
| Educational Pipeline | `application.pipeline` | Orchestration only |
| AI Enrichment | `infrastructure.ai` | Presentation enrichment only |
| Composition Root | `application.composition` (+ infrastructure factories) | Sole construction of wired services |

Binding ADRs: [ADR-001](adr/ADR-001-educational-operating-system.md) … [ADR-010](adr/ADR-010-educational-pipeline.md).

---

## 4. Educational Authority Flow

```
Evidence → Educational Core judgements
        → Mission / Plan / Progress / Recommendations
        → Explainability (narrates; does not decide)
        → Student Experience (presents; does not decide)
        → AI Enrichment (words; does not decide)
        → Web / student surfaces
```

The **Educational Pipeline** sequences these stages. It does not invent diagnoses, mastery scores, or strategy choices. Those remain in domain engines.

---

## 5. Composition Root

All durable wiring of repositories, unit of work, domain engines, pipeline, and AI enrichers occurs in the composition root (`application.composition.application_factory`, supported by `infrastructure.composition` factories).

Web receives an assembled container. Routes and handlers receive injected collaborators. They do not construct educational engines.

See [ADR-009](adr/ADR-009-composition-root.md).

---

## 6. Governance and Verification

| Artefact | Role |
|---|---|
| [ARCHITECTURE_CONSTITUTION.md](ARCHITECTURE_CONSTITUTION.md) | Non-negotiable principles |
| This overview | Structural map |
| [SYSTEM_CONTEXT.md](SYSTEM_CONTEXT.md) | Context diagram narrative |
| [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md) | Dependency law |
| `tests/architecture/` | Mandatory CI architecture gates |
| Release protocol | Architecture docs are release artefacts |

Architecture documents in `docs/` (this set and `docs/adr/`) are **release artefacts**. Architecture tests are **mandatory CI gates**.
