# Kwalitec Architecture Knowledge Base

Permanent reference for **why** Kwalitec is shaped the way it is, **how** major subsystems work, and **how** developers and AI agents should extend the product safely.

This knowledge base complements (does not replace):

| Document | Role |
|---|---|
| [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) | Product thesis, stack, current status |
| [`ARCHITECTURE.md`](../ARCHITECTURE.md) | Structural map and layer diagrams |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Branching, commits, PRs, milestones |
| [`PRODUCT_BLUEPRINT.md`](../PRODUCT_BLUEPRINT.md) | Long-term product vision |
| [`docs/process/RELEASE_PROTOCOL.md`](../docs/process/RELEASE_PROTOCOL.md) | Release procedure |
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
├── architecture/             ← ADRs, Design Principles, Founder IA
├── educational/              ← Educational Constitution & governance
├── engineering/              ← Handbook, patterns, standards
├── founder/                  ← Founder OS / FSI programme docs
├── investigations/           ← Audits (e.g. POP-001)
├── product/                  ← Product programmes (PTP, LXP, IA)
├── release/                  ← Version 1 RC1 / certification trail
├── releases/                 ← Implementation & verification reports (IAHF, V1SP, RC2)
├── research/                 ← Research Intelligence Programme
├── subsystems/               ← How major domains work
└── development/              ← Coding standards, AI workflow, glossary
```

| Folder | Use when |
|---|---|
| `architecture/` | Design Principles, POP-002 IA, ADRs — the **why** behind hard constraints |
| `educational/` | Educational Constitution and governance law |
| `releases/` | Milestone implementation / verification reports for RC2 and IAHF |
| `release/` | Version 1 RC1 certification and release-candidate records |
| `subsystems/` | The **how** of a domain before changing it |
| `development/` | Style, AI process, history, or terminology |
| `investigations/` | Pre-implementation audits (do not treat as live as-built without checking `releases/`) |

**Avoid duplication:** Prefer updating the authoritative programme doc (e.g. POP-002, Design Principles) over copying guidance into multiple status files. Historical investigation text may describe pre-fix state — check the matching implementation report for live behaviour.

---

## How developers should use it

1. **Before structural changes** — read the relevant ADR(s) and subsystem doc, then [`ARCHITECTURE.md`](../ARCHITECTURE.md).
2. **Before curriculum work** — read [ADR-003](architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](architecture/ADR-004-canonical-topic-traversal.md), and [curriculum-engine.md](subsystems/curriculum-engine.md).
3. **Before adding business logic** — read [ADR-001](architecture/ADR-001-service-layer.md) and [ADR-002](architecture/ADR-002-blueprint-architecture.md); put logic in services, not routes.
4. **Before Founder / ops UI work** — read [Design Principles](architecture/DESIGN_PRINCIPLES.md) and [POP-002](architecture/POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md); confirm as-built status against IAHF / V1SP reports.
5. **When stuck on naming** — check [glossary.md](development/glossary.md) and `app/brand_identity.py` for user-facing labels.
6. **When proposing a new architectural pattern** — add or update an ADR; do not silently diverge from Accepted decisions.

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

## Version 1 RC2 quick links

| Topic | Document |
|---|---|
| Operational readiness | [RC2 report](releases/RC2_OPERATIONAL_READINESS_REPORT.md) |
| Release notes | [`docs/release/RELEASE_NOTES_v1.0.0-RC2.md`](../docs/release/RELEASE_NOTES_v1.0.0-RC2.md) |
| Design Principles | [DESIGN_PRINCIPLES.md](architecture/DESIGN_PRINCIPLES.md) |
| Founder IA | [POP-002](architecture/POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md) |
| Educational Constitution | [KWALITEC_EDUCATIONAL_CONSTITUTION.md](educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) |
| Brand assets | [`app/static/branding/README.md`](../app/static/branding/README.md) |

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
