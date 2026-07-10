# Kwalitec Architecture Knowledge Base

Permanent reference for **why** Kwalitec is shaped the way it is, **how** major subsystems work, and **how** developers and AI agents should extend the product safely.

This knowledge base complements (does not replace):

| Document | Role |
|---|---|
| [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) | Product thesis, stack, current status |
| [`ARCHITECTURE.md`](../ARCHITECTURE.md) | Structural map and layer diagrams |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Branching, commits, PRs, milestones |
| [`.cursor/rules/`](../.cursor/rules/) | Enforceable agent conventions |
| [`prompts/`](../prompts/) | Task-start templates |

---

## Purpose

Kwalitec is a commercial adaptive learning product. Core behaviour must stay:

- **Curriculum-first** — syllabus structure drives planning and recommendations
- **Deterministic** — same inputs produce the same outputs
- **Explainable** — suggestions are traceable to data, not opaque scores
- **V1/V2 compatible** — flat and hierarchical curricula both remain loadable

This knowledge base preserves the architectural decisions behind those invariants so future work does not accidentally reintroduce god routes, duplicate topic ordering, or break legacy syllabuses.

---

## Organisation

```
knowledge/
├── README.md                 ← you are here
├── architecture/             ← Architecture Decision Records (ADRs)
│   ├── ADR-001-service-layer.md
│   ├── ADR-002-blueprint-architecture.md
│   ├── ADR-003-curriculum-v1-v2.md
│   ├── ADR-004-canonical-topic-traversal.md
│   └── ADR-005-testing-strategy.md
├── subsystems/               ← How major domains work
│   ├── curriculum-engine.md
│   ├── study-planning.md
│   ├── readiness.md
│   ├── missions.md
│   ├── analytics.md
│   └── authentication.md
└── development/              ← How to work on the codebase
    ├── coding-standards.md
    ├── ai-workflow.md
    ├── project-history.md
    └── glossary.md
```

| Folder | Use when |
|---|---|
| `architecture/` | You need the **why** behind a hard constraint |
| `subsystems/` | You need the **how** of a domain before changing it |
| `development/` | You need style, AI process, history, or terminology |

---

## How developers should use it

1. **Before structural changes** — read the relevant ADR(s) and subsystem doc, then [`ARCHITECTURE.md`](../ARCHITECTURE.md).
2. **Before curriculum work** — read [ADR-003](architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](architecture/ADR-004-canonical-topic-traversal.md), and [curriculum-engine.md](subsystems/curriculum-engine.md).
3. **Before adding business logic** — read [ADR-001](architecture/ADR-001-service-layer.md) and [ADR-002](architecture/ADR-002-blueprint-architecture.md); put logic in services, not routes.
4. **When stuck on naming** — check [glossary.md](development/glossary.md).
5. **When proposing a new architectural pattern** — add or update an ADR; do not silently diverge from Accepted decisions.

Cross-links inside these docs point to concrete modules under `app/` (services, blueprints, engine). Prefer those paths over inventing parallel abstractions.

---

## How AI agents should use it

1. Treat this directory as **durable project memory** alongside `PROJECT_CONTEXT.md`, `ARCHITECTURE.md`, and `.cursor/rules/`.
2. At the start of a milestone, identify which ADRs and subsystem docs apply; obey “do not modify …” constraints literally.
3. Prefer [canonical traversal](architecture/ADR-004-canonical-topic-traversal.md) helpers over ad-hoc topic queries.
4. Prefer [service-layer](architecture/ADR-001-service-layer.md) placement for any planning, mastery, readiness, or recommendation math.
5. Follow [ai-workflow.md](development/ai-workflow.md) for ChatGPT vs Cursor responsibilities, review, and completion reporting.
6. For documentation-only milestones: create/update docs only; leave application WIP unstaged unless the brief says otherwise.

Agents must not invent black-box LLM calls into core learning paths, break V1 loaders, or duplicate `CurriculumService` ordering logic.

---

## Related quick links

| Topic | Document |
|---|---|
| Service layer decision | [ADR-001](architecture/ADR-001-service-layer.md) |
| Thin blueprints | [ADR-002](architecture/ADR-002-blueprint-architecture.md) |
| V1 + V2 coexistence | [ADR-003](architecture/ADR-003-curriculum-v1-v2.md) |
| Topic ordering | [ADR-004](architecture/ADR-004-canonical-topic-traversal.md) |
| Test pyramid | [ADR-005](architecture/ADR-005-testing-strategy.md) |
| Curriculum Engine | [subsystems/curriculum-engine.md](subsystems/curriculum-engine.md) |
| AI development loop | [development/ai-workflow.md](development/ai-workflow.md) |
| Term definitions | [development/glossary.md](development/glossary.md) |
