# Architecture Invariants

**Document ID:** ENG-STD-006  
**Pack:** Engineering Standards Pack  
**Status:** Canonical — architectural law  
**Audience:** All engineers and AI agents  
**Related:** [`ENGINEERING_STANDARD.md`](ENGINEERING_STANDARD.md), [`ARCHITECTURE.md`](../../ARCHITECTURE.md), Educational Intelligence programme architecture under `knowledge/product/`

---

## Purpose

These invariants are permanent architectural laws for Kwalitec’s Educational Intelligence Platform. Feature work may extend behaviour **only** within these laws. Violations require an ADR and explicit programme authority — not a convenience merge.

---

## Educational Intelligence authorities

### 1. Student Digital Twin is the sole learner state

The Student Digital Twin is the system of record for learner educational belief (mastery, confidence, readiness dimensions, and related Twin-owned estimates). Presentation layers, Tutor, Mission Engine, and infrastructure adapters must not maintain a competing long-term learner-state store.

### 2. StudentReasoningService performs educational reasoning

Educational reasoning — why Twin inferences and educational decisions change — is performed through `StudentReasoningService` (Educational Reasoning Engine path). Other components consume reasoning outputs; they do not reimplement reasoning policy.

### 3. Mission Engine consumes decisions

The Adaptive Mission Engine / Mission Engine schedules and structures **what to do**. It consumes Twin state and reasoning outputs (and graph structure for lawful ordering). It must not invent educational recommendations or Twin inferences.

### 4. Tutor explains decisions

The Intelligent Tutor explains decisions already produced by Reasoning, Twin state, Learning Graph structure, missions, and assessment feedback. The Tutor must not become a second reasoning engine and must not mutate Twin inferences.

### 5. Learning Graph stores relationships only

The Learning Graph holds structural relationships (prerequisites, recovery paths, related concepts). It is not a learner-state store and not a recommendation engine.

### 6. Curriculum Retrieval is the only evidence interface

Curriculum evidence for intelligence paths is obtained through Curriculum Retrieval (approved retrieval profiles/services). Application code must not bypass retrieval with ad-hoc syllabus scraping or direct vector-store access without ports.

### 7. Assessment produces observations

The Assessment Pipeline produces observations and feedback evidence. It does not own Twin authority or rewrite educational reasoning. Twin updates from assessment flow through the lawful reasoning/Twin update path.

---

## Clean Architecture laws

### 8. Application never imports Infrastructure

Dependency direction: Presentation → Application → Domain; Infrastructure implements Application/Domain ports and is wired at composition roots. Application modules must not import Infrastructure adapters, ORM session wiring, or framework-specific persistence directly.

### 9. Thin presentation

Blueprints and templates do not contain planning, mastery, readiness, or recommendation mathematics. Templates present decisions; they do not invent them.

### 10. Domain purity

Domain packages remain free of Flask, HTTP, and filesystem side effects. Educational policy is not encoded in infrastructure adapters.

---

## Educational integrity laws

### 11. No LLM inside educational reasoning

Core educational reasoning and Twin inference paths are deterministic rule/evidence systems. LLMs (when present) may only appear behind explicit generation ports for prose explanation, never as the source of educational decisions.

### 12. Evidence precedes inference

Inferences require observations and/or retrieved curriculum evidence. Do not fabricate mastery, readiness, gaps, or recommendations to fill missing data. Cold-start / thin-Twin cases must be honest.

### 13. Deterministic educational decisions

Same Twin state + evidence + curriculum inputs → same educational decisions. No hidden randomness in planning, readiness, recommendation, or reasoning cores.

### 14. No hidden educational logic

Educational behaviour lives in designated authorities. Do not embed shadow policy in templates, presentation helpers, adapters, or “temporary” route math.

### 15. Explainability is mandatory for student-facing intelligence

Claims shown to students must be traceable to evidence and declared rules. Incomplete explainability must not ship as Twin Authority insight.

---

## Platform structural laws

### 16. Application factory is the only app construction path

Apps are constructed via `create_app` (or documented Education OS entry equivalents). Do not invent parallel bootstraps that skip security, migration, or composition guarantees.

### 17. Schema changes go through Alembic

Durable schema evolution uses Alembic under `migrations/versions/`. No raw DDL from request handlers.

### 18. Curriculum V1 and V2 both remain loadable

Flat (V1) and hierarchical (V2) curricula must remain loadable and traversable. Feature work must not silently break either.

### 19. Idempotent bootstrap

Startup import, migrate, and admin bootstrap paths must be safe to re-run.

### 20. Secrets stay out of the repository

Secrets live in environment variables. Never commit `.env`, credentials, or private keys.

---

## Enforcement

| Mechanism | Role |
|---|---|
| Architecture tests | Automated import and boundary checks |
| Code review checklist | Human verification of educational authorities |
| Release protocol | Blocks ship on architecture regression |
| ADRs | Sole lawful exception path |

---

## Non-negotiable summary

> Twin owns learner state. Reasoning decides. Mission schedules. Tutor explains. Graph relates. Retrieval evidences. Assessment observes. Application depends inward. Evidence before inference. Deterministic. No LLM in reasoning.
