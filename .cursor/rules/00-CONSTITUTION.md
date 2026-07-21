# Kwalitec Architectural Constitution

**Status:** Permanent — Cursor governance source of truth  
**Authority:** Normative for all implementation work  
**Canonical detail:** [`docs/ARCHITECTURE_CONSTITUTION.md`](../../docs/ARCHITECTURE_CONSTITUTION.md), [`docs/DEPENDENCY_RULES.md`](../../docs/DEPENDENCY_RULES.md)

This document is the permanent architectural constitution for Cursor agents. It consolidates the binding principles agents must obey without re-reading the full governance corpus on every task.

---

## Educational Authority

| Principle | Law |
|---|---|
| **Educational Operating System** | The only source of educational decisions. Curriculum structure, evidence, diagnoses, priorities, strategies, missions, plans, progress, and recommendations derive from authorised educational models — never from UI convenience or opaque automation. |
| **Student Twin** | The canonical educational model of a learner (`domain.education.digital_twin`). All educational reasoning reads from and writes to the twin through authorised ports. |
| **Educational Pipeline** | The only component permitted to **orchestrate** end-to-end educational outputs (`application.pipeline`). Recommendations are **generated** by domain engines and **sequenced** by the pipeline — never invented in adapters or presentation. |
| **AI augments; AI never replaces** | AI may enrich presentation wording. AI must not diagnose, score mastery, choose strategies, or author authoritative missions or recommendations. |

**Recommendations originate only from the Educational Pipeline** (delegating to `domain.recommendation`). No other layer may create educational recommendations.

---

## Hexagonal Architecture

```
Presentation  →  Application  →  Domain
     ↓              ↓
  Adapters    Infrastructure (implements Ports)
```

| Layer | Owns | Must not |
|---|---|---|
| **Domain** | Business rules, educational meaning, deterministic engines | Framework imports; persistence; HTTP; presentation |
| **Application** | Orchestration, use-cases, ports, DTOs, pipeline sequencing | Educational math ownership outside delegation; ORM outside composition |
| **Adapters** | HTTP (Flask blueprints), request/response, auth wiring | Educational decisions; domain construction |
| **Infrastructure** | SQLAlchemy, Argon2, clocks, events, AI providers | Authoritative educational decisions |
| **Presentation** | View models, mappers, design-system components, HTML templates | Educational authority; framework-specific business logic |

### Dependency laws

- **Domain has zero framework dependencies.** No Flask, SQLAlchemy, Jinja2, WTForms, AI SDKs.
- **Domain never imports Application.**
- **Application never imports Adapters.**
- **Presentation is framework independent.** Pure view models and design tokens; Flask wiring stays in adapters.
- **Flask exists only inside the Adapter layer** (`src/adapters/flask/`, legacy `app/` blueprints).
- **SQLAlchemy exists only inside Infrastructure** (`src/infrastructure/persistence/`).
- **Infrastructure implements Ports only.** Repositories and services satisfy `application.ports`; they do not own educational logic.

### Responsibility placement

| Concern | Layer |
|---|---|
| Business rules | Domain |
| Orchestration | Application |
| HTTP | Adapters |
| Persistence | Infrastructure |
| Rendering | Presentation |

---

## Cross-cutting invariants

1. **Educational logic must remain explainable.** Every guidance product traces to evidence, twin state, and a decision path.
2. **Deterministic cores.** Same educational inputs → same educational decisions (no randomness in the pipeline).
3. **Design System is the single source of UI truth** (`presentation.design_system`). No hard-coded colours or spacing in feature code.
4. **Composition root constructs collaborators.** Production wiring occurs in `application.composition`; routes and handlers receive injected services.
5. **Legacy coexistence.** `app/` (V1 Flask product) coexists with `src/` (Educational OS). New educational authority lives under `src/`. Do not break V1/V2 curriculum traversal during migration.

---

## Amendment

Constitutional changes require an ADR under `docs/adr/`, updates to `docs/DEPENDENCY_RULES.md` where relevant, and green `tests/architecture/` gates. Silent drift is forbidden.
