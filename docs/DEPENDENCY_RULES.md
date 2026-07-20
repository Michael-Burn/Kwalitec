# Kwalitec Dependency Rules

**Milestone:** APP-003 — Architecture Governance  
**Status:** Governing — Version 2 dependency law  
**Authority:** Normative; enforced by `tests/architecture/`  
**Date:** 2026-07-20  

---

## 1. Purpose

State the allowed and forbidden dependency directions for the Educational Operating System under `src/`.

These rules implement Articles VII–IX of the [Architecture Constitution](ARCHITECTURE_CONSTITUTION.md).

---

## 2. Allowed Dependency Graph

```
web ──────────────► application ──────────────► domain
  │                      │                         ▲
  │                      │ ports (ABC)              │
  │                      ▼                          │
  └────────────► infrastructure ────────────────────┘
                 (implements ports; may read domain types)
```

| From | May depend on | Must not depend on |
|---|---|---|
| `domain` | stdlib, other `domain.*` packages as published | `application`, `infrastructure`, `web`, `app`, Flask, SQLAlchemy, AI SDKs |
| `application` (non-composition) | `domain`, `application.ports`, stdlib | `infrastructure`, `web`, `app`, Flask, SQLAlchemy, AI SDKs |
| `application.composition` | `domain`, `application.*`, `infrastructure.*` (construction only) | Flask request globals; educational math ownership |
| `infrastructure` | `domain` (types), `application.ports`, vendor SDKs, SQLAlchemy | `web`, Flask blueprints as owners of educational logic |
| `web` | `application` facades/containers, Flask | Constructing domain engines; importing ORM sessions for educational math |

---

## 3. Concrete Import Rules

### Domain

- **No** `flask`, `sqlalchemy`, `alembic`, `jinja2`, `wtforms`
- **No** `openai`, `anthropic`, vendor AI SDKs, or `infrastructure.ai`
- **No** `application.*`, `infrastructure.*`, `web.*`, `app.*`

### Application (excluding composition)

- **No** ORM (`sqlalchemy`, `create_engine`, `sessionmaker` as persistence owners)
- **No** `infrastructure.*` imports (adapters are injected)
- **No** Flask request/session globals

### Application composition root

- **May** import infrastructure adapters to construct and inject them
- **Must** be the place where `EducationalPipeline`, enrichers, and provider defaults are wired for production

### Infrastructure

- **Owns** SQLAlchemy models/repositories, runtime clocks/UUIDs, event dispatch, AI providers/enrichers
- **Must not** define authoritative educational decision methods (`diagnose`, `calculate_mastery`, `choose_strategy`, …) outside delegated domain calls

### Student Experience (`domain.student_experience`)

- May consume completed educational outputs
- Must not import or invoke educational decision engines as authorities to mutate decisions
- Must not define methods that rewrite missions or recommendations

### AI (`infrastructure.ai`)

- May enrich already-decided missions/recommendations for presentation
- Must not import educational decision engines as decision authorities
- Must not define educational decision methods listed in architecture purity tests

### Pipeline (`application.pipeline`)

- Orchestrates stage order and delegates to injected engines/ports
- Must not define educational intelligence methods
- Must not own persistence or Flask

---

## 4. Construction Rules

| Construct | Allowed construction sites |
|---|---|
| `EducationalPipeline`, `MissionEnricher`, `RecommendationEnricher`, default `AIProvider` | `application.composition` (production wiring) |
| SQLAlchemy session factory / unit of work | `infrastructure.composition` factories invoked from composition root |
| Domain engine classes | Defined in `domain.*`; wired (as types or instances) via composition root |
| Web app factory | May call `create_application` / receive an injected container; must not new up domain engines |

Tests may construct collaborators directly. Production and web runtime must not.

---

## 5. Enforcement

| Gate | Location |
|---|---|
| Layer import purity | `tests/architecture/test_layer_dependency_rules.py` |
| Composition construction | `tests/architecture/test_composition_root.py` |
| Student experience non-authority | `tests/architecture/test_student_experience_boundary.py` |
| AI non-authority | `tests/architecture/test_ai_enrichment_boundary.py` |
| Pipeline orchestration-only | `tests/architecture/test_pipeline_orchestration.py` |
| Governance artefacts present | `tests/architecture/test_governance_artefacts.py` |

These tests are **mandatory CI gates**. Breaking a rule fails the build.

---

## 6. Related ADRs

- [ADR-001 Educational Operating System](adr/ADR-001-educational-operating-system.md)
- [ADR-007 Student Experience](adr/ADR-007-student-experience.md)
- [ADR-008 AI Enrichment Boundary](adr/ADR-008-ai-enrichment-boundary.md)
- [ADR-009 Composition Root](adr/ADR-009-composition-root.md)
- [ADR-010 Educational Pipeline](adr/ADR-010-educational-pipeline.md)
