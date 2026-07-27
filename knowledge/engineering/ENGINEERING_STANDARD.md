# Kwalitec Engineering Standard

**Document ID:** ENG-STD-001  
**Pack:** Engineering Standards Pack  
**Status:** Canonical  
**Audience:** All engineers and AI agents contributing to Kwalitec  
**Related:** [`handbook/ENG-001_ENGINEERING_HANDBOOK.md`](handbook/ENG-001_ENGINEERING_HANDBOOK.md) (constitutional depth), [`ARCHITECTURE_INVARIANTS.md`](ARCHITECTURE_INVARIANTS.md), [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md), [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

## Purpose

This standard is the permanent engineering contract for Kwalitec development. It defines how work is designed, implemented, and judged. Capability briefs may add constraints; they may not weaken this contract.

---

## Engineering philosophy

Kwalitec is a commercial adaptive learning product. Prefer disciplined, explainable engineering over cleverness.

| Value | Meaning |
|---|---|
| Correctness | Behaviour is predictable and reproducible from stated inputs |
| Simplicity | Prefer the simplest architecture that satisfies current requirements |
| Maintainability | Future engineers are first-class stakeholders |
| Explainability | Intent and educational conclusions must be communicable |
| Educational integrity | Never fabricate educational conclusions |
| Evidence-driven evolution | Prefer measured evidence over speculative redesign |

Engineering exists to enable sustainable product evolution, not merely to produce code.

---

## Clean Architecture principles

Dependencies point inward toward stable abstractions.

| Layer | Owns | Must not |
|---|---|---|
| Presentation (templates, blueprints, JS) | HTTP, forms, rendering | Planning, mastery, recommendation, or Twin math |
| Application | Use-case orchestration via ports | Concrete infrastructure imports |
| Domain | Educational entities, invariants, pure rules | Flask, ORM, HTTP, filesystem I/O |
| Infrastructure | Adapters, persistence, external systems | Educational policy invention |

**Rule:** Application never imports Infrastructure. Infrastructure implements ports defined by Application/Domain. Composition roots wire adapters at the edge.

See also: [`standards/ENG-004_ENGINEERING_DEPENDENCY_RULES.md`](standards/ENG-004_ENGINEERING_DEPENDENCY_RULES.md).

---

## DDD principles

- Model educational language explicitly (Twin, Mission, Assessment, Curriculum, Reasoning).
- Keep bounded contexts cohesive; do not collapse distinct educational authorities into one service.
- Protect aggregate invariants in domain/application code — not in templates or ad-hoc route math.
- Prefer explicit ports and adapters over ambient global state.
- Treat curriculum structure as official syllabus truth, not as UI convenience data.

---

## Layer responsibilities

### Thin routes

Routes authenticate, validate input, call services/application use cases, and render or redirect. They do not contain planning, mastery, readiness, or recommendation mathematics.

### Services own business logic

Business rules live in services / application layers with explicit arguments. They must not depend on `flask.request` or session globals.

### Templates are presentation only

Jinja2 templates and student JS display decisions already made. They do not invent educational state, reorder missions by hidden heuristics, or embed Twin inference.

---

## Delivery principles

### One capability per milestone

Each milestone delivers one coherent capability (or one bounded documentation pack). Do not bundle unrelated features, drive-by refactors, or speculative architecture into the same delivery unit.

### Preserve backwards compatibility

- Prefer additive change with compatibility shims over breaking rewrites.
- Curriculum V1 (flat) and V2 (hierarchical) must both remain loadable and traversable.
- Schema changes go through Alembic; startup import/migrate/admin paths remain idempotent.

### No architectural shortcuts

Do not bypass ports, composition roots, or authority boundaries for convenience. Temporary shortcuts become permanent debt and educational risk.

---

## Educational engineering principles

### Evidence before inference

Observations and retrieved curriculum evidence precede educational inferences. Do not invent mastery, readiness, or recommendations to fill gaps.

### Deterministic educational reasoning

Given the same Twin state, evidence, and curriculum inputs, educational decisions must reproduce. No hidden randomness and no LLM inside educational reasoning cores.

### No hidden educational logic

Educational behaviour must live in designated reasoning and Twin update paths — not in templates, presentation helpers, or infrastructure adapters.

### Educational honesty

Surfaces must not overclaim certainty. Communicate what the system knows, what it does not know, and why a suggestion was made. Prefer under-claiming to fabricated confidence.

### Explainability requirements

Student-facing intelligence (recommendations, readiness, Coach/Insights, Tutor explanations, planning guidance) must be traceable to data and declared rules.

For programmes that change student-facing intelligence, complete:

- [`knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md`](../product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md)
- [`knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_REVIEW_CHECKLIST.md`](../product/p001_3_recommendation_quality_standard/RECOMMENDATION_REVIEW_CHECKLIST.md) when recommendations are in scope

---

## Working rules

1. Read `PROJECT_CONTEXT.md` and `ARCHITECTURE.md` before structural changes.
2. Obey explicit “do not modify …” constraints literally.
3. Fix root causes; do not patch symptoms across layers.
4. Do not add dependencies, refactors, or features outside the task.
5. Leave secrets in environment variables; never commit `.env`.
6. Match existing naming, typing, and docstring patterns.

---

## Definition of done

A change is done when:

1. Scope is respected.
2. Relevant tests and lints pass (or N/A for documentation-only with stated rationale).
3. Architecture invariants hold — especially Educational Intelligence authorities and curriculum V1/V2.
4. Explainability / recommendation reviews are completed when in scope.
5. Any required completion report is produced.

---

## Authority

Where this pack and the Engineering Handbook both apply, they must agree. If a conflict appears, raise an Architecture Decision Record (ADR); do not silently pick a side. Detailed operational procedures live in sibling documents in this pack and must not restate contradictory rules.
