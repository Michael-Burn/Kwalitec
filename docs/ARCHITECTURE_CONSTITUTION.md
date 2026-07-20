# Kwalitec Architecture Constitution

**Milestone:** APP-003 — Architecture Governance  
**Status:** Governing — Version 2 architectural law  
**Authority:** Normative for the Educational Operating System (`src/`)  
**Nature:** Principles only — no product features, no stack prescriptions beyond layer boundaries  
**Date:** 2026-07-20  

---

## Preamble

Kwalitec Version 2 is an Educational Operating System: a disciplined platform that helps candidates for demanding professional examinations study with clarity, honesty, and continuity.

Technologies will change. Frameworks will be replaced. Persistence engines will evolve. The principles in this Constitution must remain.

This Constitution freezes the architectural law of Version 2. Specialised ADRs, layer documents, and executable architecture tests interpret and enforce it. They do not override it.

Companion artefacts:

| Document | Role |
|---|---|
| [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md) | Layer map and subsystem map |
| [SYSTEM_CONTEXT.md](SYSTEM_CONTEXT.md) | Actors, boundaries, and external systems |
| [DEPENDENCY_RULES.md](DEPENDENCY_RULES.md) | Allowed and forbidden dependency directions |
| [docs/adr/](adr/) | Binding architectural decisions (ADR-001 … ADR-010) |
| `tests/architecture/` | Executable enforcement of this Constitution |

---

## Article I — Educational Truth

Educational truth is owned by authorised educational models and workflows.

Curriculum structure, evidence, diagnoses, priorities, teaching intentions, strategies, missions, study plans, progress evaluations, and recommendations must derive from official syllabus structure and observable learning evidence — not from presentation convenience, engagement heuristics, or opaque automation.

No surface — student UI, founder console, analytics, research, or AI enrichment — may invent or rewrite educational truth for demonstration, completeness, or perceived intelligence.

**Law:** If a claim cannot be traced to curriculum structure or authorised evidence, it is not educational truth.

---

## Article II — Deterministic Decisions

Core educational decisions must be reproducible from the same inputs.

Given identical evidence, twin state, curriculum context, and decision parameters, mission generation, study planning, progress evaluation, recommendation generation, and explainability must produce the same educational outcomes.

Non-determinism (wall-clock entropy, random sampling, model sampling) must not enter the educational decision path. Presentation enrichment may vary in wording only when explicitly isolated behind enrichment ports and never allowed to alter educational decisions.

**Law:** Same educational inputs → same educational decisions.

---

## Article III — Evidence-first Reasoning

Educational understanding is provisional and evidence-bound.

Inference may interpret evidence. Inference must not invent evidence. Absence of evidence is not proof of mastery, readiness, or weakness stated as fact. Unknown remains unknown.

Evidence flows inward to the Educational Core. Speculation, narrative polish, and motivational framing flow outward as presentation — never back as educational authority.

**Law:** Evidence before opinion; honesty before confidence.

---

## Article IV — Explainability

Every educational guidance product must be explainable.

Students and operators must be able to understand, in plain language, what the system knows, what it estimates, why it recommends an action, and what should happen next — from identifiable inputs and a decision trace.

If a result cannot be explained, it is not ready to be shown as educational guidance.

**Law:** Unexplainable guidance is incomplete guidance.

---

## Article V — Student Experience Separation

Student Experience is a presentation projection, not an educational authority.

Streaks, achievements, celebrations, motivational messaging, and reminders may interpret completed educational outputs for engagement. They must never diagnose, prioritise, select strategies, rewrite missions, mutate recommendations, or alter progress evaluations.

**Law:** Experience presents educational decisions; it never authors them.

---

## Article VI — AI Enrichment Boundary

Artificial intelligence may enrich presentation. It must not decide education.

AI providers and enrichers may improve wording, summaries, or motivational framing of already-decided missions and recommendations. They must not diagnose, score mastery, choose strategies, generate authoritative missions or recommendations, or rewrite educational specifications.

AI failures must degrade enrichment only. Educational pipelines must remain correct without AI.

**Law:** AI advises presentation; deterministic engines own educational decisions.

---

## Article VII — Dependency Inversion

Inner layers never depend on outer layers.

Domain depends on nothing outside the domain. Application depends on domain and on abstract ports. Infrastructure and web implement ports and adapt frameworks. Construction of concrete adapters occurs at composition roots.

**Law:** Dependencies point inward toward educational meaning.

---

## Article VIII — Framework Independence

The Educational Core is framework-independent.

Domain and application business orchestration must not import Flask, SQLAlchemy, Jinja2, WTForms, HTTP clients, cloud SDKs, or vendor AI SDKs. Persistence, web, and AI concerns live in infrastructure (and thin web adapters).

The Educational Operating System must remain testable and portable without a web framework or ORM.

**Law:** Educational meaning outlives any single framework.

---

## Article IX — Replaceable Infrastructure

Infrastructure is replaceable.

Databases, clocks, UUID generators, event buses, AI vendors, and web frameworks are adapters. Replacing an adapter must not require rewriting domain educational logic. Provider replacement for AI occurs at the composition root.

**Law:** Swap adapters; preserve educational decisions.

---

## Article X — Testing Philosophy

Architecture is enforced by tests, not by intention alone.

Architecture purity, dependency direction, composition-root construction, pipeline orchestration boundaries, student-experience non-authority, and AI non-authority are mandatory executable gates. Documentation without tests is advisory; documentation with failing gates is incomplete.

Release verification includes architecture governance artefacts and architecture test gates.

**Law:** If a boundary matters, a test must fail when it is broken.

---

## Amendment

Amendments to this Constitution require an explicit Architecture Decision Record, a matching update to `DEPENDENCY_RULES.md` where relevant, and green `tests/architecture/` gates. Silent drift is forbidden.
