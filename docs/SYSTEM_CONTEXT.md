# Kwalitec System Context

**Milestone:** APP-003 — Architecture Governance  
**Status:** Governing — Version 2 context map  
**Authority:** Descriptive; bound by the [Architecture Constitution](ARCHITECTURE_CONSTITUTION.md)  
**Date:** 2026-07-20  

---

## 1. Purpose

Describe who interacts with Kwalitec Version 2, which systems sit outside the Educational Operating System, and where educational authority stops.

---

## 2. Context Diagram (narrative)

```
                    ┌──────────────────────┐
                    │      Students        │
                    │  (study & guidance)  │
                    └──────────┬───────────┘
                               │ browser / HTTP
┌──────────────────────────────▼────────────────────────────────┐
│                     Kwalitec Product Surface                   │
│  Legacy app/ blueprints  ·  src/web Education OS runtime       │
└───────────────┬───────────────────────────────┬───────────────┘
                │                               │
                │ use-cases                     │ ops / founder
                ▼                               ▼
┌───────────────────────────────┐   ┌───────────────────────────┐
│  Educational Operating System │   │ Founder / operator tools  │
│  Domain · Application · Infra │   │ observe; do not rewrite   │
│  educational authority        │   │ educational truth         │
└───────────────┬───────────────┘   └───────────────────────────┘
                │
     ┌──────────┼──────────┬────────────────┐
     ▼          ▼          ▼                ▼
 Curriculum   Database   Clock/UUID     AI providers
  JSON /      (SQL)      runtime         (optional
  engine                                 enrichment)
```

---

## 3. Actors

| Actor | Intent | Educational authority |
|---|---|---|
| **Student** | Study with clear next actions, progress honesty, explainable guidance | None — receives decisions |
| **Founder / operator** | Observe product health, alpha feedback, operational signals | Observe only — must not rewrite educational evidence for convenience |
| **Curriculum author / importer** | Maintain official syllabus structure | Owns syllabus structure via authorised import paths |
| **System (batch / startup)** | Migrate, bootstrap admin, import curriculum | Must remain idempotent; must not invent learner state |

---

## 4. System Boundary

**Inside the Educational Operating System (`src/`):**

- Domain educational engines and Educational Core aggregates
- Application commands, queries, pipeline, ports, composition root
- Infrastructure adapters (persistence, runtime, events, AI enrichment)
- Thin web runtime for Education OS blueprints

**Outside (depended upon, not owned as educational truth):**

| External | Role | Constraint |
|---|---|---|
| Relational database | Persist aggregates and projections | Schema via migrations; no educational math in SQL |
| Curriculum JSON / engine | Official syllabus structure | Traversal through authorised curriculum services |
| AI vendor APIs | Optional presentation enrichment | Never educational decision authority |
| Hosting / process manager | Deploy and health | No educational semantics |

**Coexistence:** Legacy `app/` product surfaces remain during Version 2 migration. They must not silently become a second educational authority. New educational intelligence lands in `src/` under this governance.

---

## 5. Trust Boundaries

1. **Educational Core boundary** — only domain engines author missions, plans, progress, and recommendations.
2. **Enrichment boundary** — AI may rephrase; it may not decide.
3. **Experience boundary** — student experience may celebrate; it may not diagnose.
4. **Operator boundary** — founder tools may inspect; they may not fabricate learner evidence.
5. **Framework boundary** — Flask/ORM stay outside domain and (except composition) outside application business modules.

---

## 6. Related Documents

- [ARCHITECTURE_CONSTITUTION.md](ARCHITECTURE_CONSTITUTION.md)
- [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md)
- [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md)
- [ADR-001 Educational Operating System](adr/ADR-001-educational-operating-system.md)
- [ADR-008 AI Enrichment Boundary](adr/ADR-008-ai-enrichment-boundary.md)
