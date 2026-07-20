# Changelog

All notable changes to Kwalitec are documented in this file.

The format follows the principles of Keep a Changelog and Semantic Versioning.

---

# [2.0.0] - 2026-07-20 — Educational Operating System (Version 2 Close)

## Fingerprint

| Field | Value |
|---|---|
| Product version | `2.0.0` |
| Release tag | `v2.0.0` |
| Release notes | `RELEASE_NOTES_V2.md` |
| Forward roadmap | `ROADMAP_V3.md` |

## Summary

Version 2.0.0 closes the Educational Operating System. APP-004 delivers production operational readiness only — typed configuration, observability, resilience, security verification, CI gates, and release artefacts. No new educational functionality.

## Added (operational)

- Typed `AppSettings` / `AIProviderSettings` with fail-fast production validation
- Provider selection via `AI_PROVIDER` without code changes (openai / anthropic / gemini / none)
- Structured logging, pipeline execution timing, AI enrichment timing, success/failure metrics
- AI provider timeout + retry with deterministic enrichment fallback
- EOS health endpoints: `/health`, `/health/ready`
- Release checklist and dependency audit under `docs/release/`
- CI jobs: Architecture Governance, Unit, Integration, Lint, Release Build

## Known limitations

- Legacy `app/` product surfaces coexist; sole-runtime cutover remains an explicit later programme
- Flask pin follow-ups tracked in `docs/release/DEPENDENCY_AUDIT_V2.md`

---

# [1.0.0] - July 2026 — Version1-RC2 (Internal Alpha)

## Fingerprint

| Field | Value |
|---|---|
| Product version | `1.0.0` |
| Internal Alpha chrome | **Build RC2** |
| Audience | Invite-only Internal Alpha (Founding Cohort) |
| Release notes | `docs/release/RELEASE_NOTES_v1.0.0-RC2.md` |

## Summary

Version 1.0.0 Build RC2 is the operational baseline for continued Internal Alpha after the Version 1 Stabilisation Programme (V1SP). It consolidates Epic 1 curriculum foundations, Epic 2 Educational Intelligence domain packages, Founder Command Centre / brand infrastructure (IAHF-003–004B), and V1SP hardening.

## Added / completed in the RC2 stabilisation window

- Learning lifecycle completion with **Revision Workspace** (V1SP-001A)
- Founder **Operational Health** decision surface (V1SP-001C)
- Founder **Vision Journal** strategic memory (V1SP-001D)
- Information architecture density simplification (V1SP-001E)
- Measured hot-path performance indexes and query reductions (V1SP-003)

## Security & operations

- RC2 operational readiness gate: APPROVED WITH MINOR ISSUES (`knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md`)
- High-severity readiness findings closed (V1SP-001B): open-redirect hardening, production cookie flags, SECRET_KEY gate, Founder nav honesty, Feedback triage, static caching, brand raster budgets, top-level docs refresh
- Independent security re-verification (V1SP-004): no Critical/High blockers for invite-only Alpha

## Known limitations (intentional for Version 1)

- Public self-registration remains disabled
- Twin-first product cutover / Twin persistence deferred to Version 2
- Exam Ready lifecycle deferred to Version 2
- Medium Alpha deferrals remain (rate limiting, CSP nonces, Founder post-login landing, archive recovery UI, etc.)

---

# [0.5.0] - July 2026

## 🎓 Educational Intelligence Platform

This release marks the completion of Epic 2 — Educational Intelligence.

---

## 1. Executive Summary

Epic 2 delivers Kwalitec’s structural Educational Intelligence stack: an immutable Student Digital Twin evolved only through Learning Evidence; write-path Update Strategies for Knowledge, Memory, Behaviour, and Performance; and read-side Readiness Aggregation, Decision Engine, Recommendation packaging, and Mission Intelligence.

Kwalitec now possesses a complete Educational Intelligence pipeline. The domain layer can answer, from evidence-backed Twin state, what the highest-value next action for a student should be — with curriculum-safe ownership, explainability, and deterministic reasoning. Product surfaces still coexist with Stage A legacy services; Twin-first cutover is the work of the next epic.

---

## 2. Major Additions

### Student Digital Twin

- Immutable educational-state aggregate
- Domain states for Knowledge, Memory, Behaviour, Performance, and related slots
- Twin Update Pipeline coordinating evidence-driven evolution

### Learning Evidence pipeline

- Append-only Learning Evidence as the sole legitimate input that may change Twin beliefs
- Evidence → Pipeline → Strategies → new Twin snapshot write path

### Knowledge Update Strategy

- Structural Knowledge evolution from evidence

### Memory Update Strategy

- Structural Memory evolution from evidence

### Behaviour Update Strategy

- Structural Behaviour evolution from evidence (adherence, feasibility — not mastery)

### Performance Update Strategy

- Structural Performance evolution from assessment-shaped evidence

### Readiness Aggregation

- Read-side, factorable preparedness derived from Twin, Goals, and Curriculum weights
- Does not select next actions or mutate Twin beliefs

### Decision Engine

- Highest-value next-action selection with reason codes and warrant / cold-start honesty
- Sole selection authority in the Twin-first stack

### Recommendation Engine

- Decision → Recommendation packaging (title, explanation chain, affordances, warrant posture)
- Does not re-rank or invent a second Decision

### Mission Intelligence

- Decision → Mission operationalisation into attributable session tasks
- Does not plan WeekPlans, invent filler, or replace Decision selection

---

## 3. Architectural Achievements

- **Educational ownership** — Knowledge ≠ Memory ≠ Behaviour ≠ Performance; Readiness ≠ Decision; Recommendation ≠ Decision; Mission ≠ Decision / Planning
- **Explainability** — Mandatory chain Curriculum → Evidence → Twin → Readiness → Decision → Recommendation → Mission
- **Framework-independent domains** — Twin, Evidence, Readiness, Decision, Recommendation, and Mission packages free of Flask / SQLAlchemy / route globals (AST-enforced purity)
- **Read-side / write-side separation** — Strategies write structure; Readiness / Decision / Recommendation / Mission never write beliefs
- **Immutable Twin** — Evidence-driven snapshots only; no in-place educational-state mutation from product layers
- **Curriculum V1/V2 compatibility** — Domain contracts use format-aware context / lineage; Epic 1 traversal invariants preserved

---

## 4. Documentation

- **ADR-002** — Accepted decision to adopt Educational Intelligence as the authoritative educational reasoning architecture
- **Educational Intelligence Architecture** — Governing specification for Twin, Evidence, Update Strategies, Readiness, Decision, Recommendation, and Mission
- **Integrity Reviews** — Recommendation Integrity Review and Mission Integrity Review (both APPROVED WITH CONDITIONS)
- **Epic 2 Completion Review** — Official domain epic sign-off (APPROVED WITH CONDITIONS); subordinate gates closed

---

## 5. Known Limitations

- **Stage A coexistence** — Live product surfaces still consume legacy readiness, recommendation, and planning / ORM mission paths alongside the Twin-first domain stack (named dual authority; no hybrid averages)
- **Legacy services** — `ReadinessService`, `RecommendationService`, and `PlanningService` remain Stage A product peers, not Twin-first authority
- **Twin persistence** — No production Twin ORM / persistence bridge yet
- **Evidence journal** — Decision Journal and accept/dismiss / completion → Evidence recording loops not yet shipped in product
- **Confidence ownership** — Confidence domain / update path incomplete; Confidence risk framing remains constrained
- **Product integration deferred** — Orchestration, UI cutover, and Twin-first student experience are out of Epic 2 scope

---

## 6. Next Release

**Epic 3 — Product Integration & Experience**

Wire Educational Intelligence into product surfaces: thin orchestration, Stage B/C cutover from legacy dual authority, Twin persistence, Evidence loops, and explainable student-facing experience.

---

# [0.4.0] - July 2026

## 🎉 Epic 1 — Curriculum Architecture Foundation

This release represents the completion of the foundational Curriculum Architecture for Kwalitec.

Rather than introducing significant user-facing functionality, this release establishes the educational architecture that future adaptive learning capabilities will build upon.

---

## Added

### Curriculum Architecture

- Canonical Curriculum hierarchy
  - Curriculum
  - Section
  - Topic
  - Learning Objective

- Section SQLAlchemy model

- Topic → Section relationship

- Canonical Curriculum JSON (V2)

- Curriculum Engine V2

- Automatic V1/V2 curriculum detection

- Curriculum Repository V2

- Curriculum validation framework

---

### Database

- Section persistence

- Section-aware curriculum importer

- Legacy curriculum backfill

- Stable curriculum identifiers

---

### Services

- Section-aware CurriculumService

- Section-aware StudyPlanService

- Shared curriculum loading

- Canonical curriculum traversal

---

### Testing

- Extensive regression coverage

- Fresh database verification

- Migration verification

- Import verification

- Section-aware service testing

- Deterministic test execution

Total passing tests:

**977**

---

### Documentation

Added:

- Epic 1 Completion Review

- Curriculum Architecture Review

- ADR-001

- Technical Debt Register

---

## Changed

- Curriculum model redesigned to match official professional examination syllabi.

- Assessment weighting moved from Topics to Sections.

- Study Plan generation updated to use section-aware traversal.

- Curriculum import redesigned around the canonical Curriculum Engine.

---

## Removed

- Duplicate curriculum traversal logic

- Manual V1/V2 handling

- Flat curriculum assumptions

---

## Technical Notes

No breaking user-facing changes.

Database migrations remain fully supported.

Existing study plans remain compatible.

---

## Next

Epic 2 — Educational Intelligence

- Behaviour Engine

- Performance Engine

- Readiness Aggregation

- Decision Engine

- Explainable Recommendations
