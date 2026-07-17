# Kwalitec

> **Educational Intelligence for Professional Examinations**

Kwalitec is an evidence-driven educational intelligence platform designed to help students preparing for professional examinations make better study decisions.

Rather than simply tracking study activity, Kwalitec models the student's educational state, understands the official curriculum, and provides explainable recommendations intended to maximise the probability of passing professional examinations.

---

# Vision

Build the world's most trusted educational intelligence platform for professional examinations.

---

# Mission

Kwalitec exists to maximise a student's probability of passing professional examinations in the shortest sustainable time through evidence-based educational guidance.

---

# The Problem

Many professional examination candidates:

- study consistently but inefficiently;
- repeat examinations multiple times;
- struggle to identify weak areas;
- revise at the wrong time;
- lack objective feedback on readiness.

Kwalitec is designed to reduce these problems by helping students make better educational decisions.

---

# Core Principles

Kwalitec is built on five principles.

- Educational outcomes before engagement
- Evidence before assumptions
- Explainable recommendations
- Sustainable learning
- Professional engineering standards

---

# Educational Model

The platform is built around four educational concepts.

```
Official Curriculum
        │
        ▼
Learning Evidence
        │
        ▼
Digital Twin
        │
        ▼
Decision Engine
        │
        ▼
Explainable Recommendation
```

---

# Architecture

The curriculum follows the official syllabus hierarchy.

```
Curriculum
    │
    ▼
Section
    │
    ▼
Topic
    │
    ▼
Learning Objective
```

This hierarchy is the canonical educational model used throughout the platform.

---

# Current Status

| Fingerprint | Value |
|---|---|
| Product version | **1.0.0** (`APP_VERSION` / `pyproject.toml`) |
| Internal Alpha build | **Build RC2** (`INTERNAL_ALPHA_BUILD_LABEL`) |
| Programme | Version 1 Stabilisation (V1SP) · invite-only Internal Alpha |
| Operational readiness | APPROVED WITH MINOR ISSUES — High items closed in V1SP-001B; security re-verified in V1SP-004 |

Epic Status

- ✅ Epic 1 — Curriculum Architecture Foundation
- ✅ Epic 2 — Educational Intelligence (domain stack + Stage A product loop for Alpha)
- ✅ Version 1 Stabilisation (V1SP-001A–001E, V1SP-003, V1SP-004) — RC2 operational baseline

See `knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md`, `knowledge/releases/V1SP-001B_OPERATIONAL_FIXES.md`, and `docs/release/RELEASE_NOTES_v1.0.0-RC2.md`.

---

# Version 1 vs Version 2

| | Version 1 (RC2) | Version 2 (deferred) |
|---|---|---|
| Audience | Invite-only Internal Alpha | Broader / public cohorts |
| Learning loop | Plan → Session → Analytics; Learning + Revision workspaces | Exam Ready lifecycle; deeper adaptive interruption |
| Recommendations | Deterministic Stage A services + optional EI Internal Alpha card | Twin-first product cutover as sole authority |
| Founder ops | Founder Command Centre (Overview, Operational Health, Feedback, Vision Journal, …) | Expanded operator programmes |
| Educational Intelligence | Domain Twin / Decision / Recommendation packages exist; product surfaces still coexist with Stage A | Full Twin persistence + Evidence journal product loops |

Version 2 capabilities must not be described as live Version 1 product behaviour.

---

# Major Components

## Curriculum Engine

Responsible for:

- curriculum loading
- validation
- repository
- provider independence
- canonical traversal (V1 flat + V2 hierarchical)

---

## Digital Twin

Represents the educational state of a student.

The Digital Twin evolves from Learning Evidence rather than assumptions.

**Domain packages (Epic 2):** Knowledge, Memory, Behaviour, Performance, plus read-side Readiness Aggregation.

**Version 1 product note:** Live student surfaces still primarily consume Stage A readiness / recommendation / planning services. Twin-first UI cutover and Twin persistence are Version 2 / Epic 3 product integration work.

---

## Decision Engine

Domain Decision Engine (Epic 2) answers:

> **What is the highest-value thing this student should do next?**

Recommendations are evidence-based and explainable. In Version 1 Internal Alpha, student-facing “study next” guidance still primarily flows through Stage A `RecommendationService` (with an optional Educational Intelligence Internal Alpha card when enabled).

---

# Getting Started

```bash
git clone <repository-url>
cd kwalitec
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # set SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD
export FLASK_APP=run.py
flask db upgrade
flask create-admin
flask run                   # or: python run.py
```

Then open `http://127.0.0.1:5000` and sign in with the admin credentials from `.env`.

| Step | Command / note |
|---|---|
| Tests | `python -m pytest tests/ -v` |
| Lint | `ruff check app/ tests/` |
| Migrations | `flask db upgrade` (Alembic under `migrations/`) |
| Production entry | `wsgi.py` via Waitress (`render.yaml`) |

Contributor conventions: [CONTRIBUTING.md](CONTRIBUTING.md). Architecture orientation: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), [ARCHITECTURE.md](ARCHITECTURE.md).

---

# Deploy (RC2)

1. Follow [docs/process/RELEASE_PROTOCOL.md](docs/process/RELEASE_PROTOCOL.md) (Internal Alpha classification).
2. Confirm fingerprint: product `1.0.0`, chrome **Build RC2**.
3. Deploy via Render Blueprint (`render.yaml`) — `StartupService` runs migrations + admin bootstrap in production.
4. Verify `/health` and smoke the login → Dashboard → Study Plan → Study Session path.
5. Release notes: [docs/release/RELEASE_NOTES_v1.0.0-RC2.md](docs/release/RELEASE_NOTES_v1.0.0-RC2.md).

Historical checklists under `docs/release/*_v0.4.0.md` apply to Epic 1 only — do not use them as the RC2 runbook.

---

# Engineering Standards

Kwalitec follows an architecture-first development process.

Every capability progresses through:

```
Analysis

↓

Architecture

↓

Implementation

↓

Testing

↓

Review

↓

Acceptance
```

Every release includes:

- Architecture Review
- Technical Debt Review
- Release Notes
- CHANGELOG
- Production Smoke Tests

---

# Repository Documentation

| Document | Purpose |
|-----------|---------|
| PRODUCT_BLUEPRINT.md | Product vision and long-term strategy |
| PROJECT_CONTEXT.md | Developer / agent orientation |
| ARCHITECTURE.md | Layers, blueprints, curriculum invariants |
| knowledge/architecture/DESIGN_PRINCIPLES.md | Governing product design principles |
| knowledge/architecture/POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md | Founder Command Centre IA |
| knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md | Highest educational authority |
| knowledge/releases/ | Release and operational readiness reports (IAHF, V1SP, RC2) |
| docs/process/RELEASE_PROTOCOL.md | Canonical release procedure |
| docs/release/RELEASE_NOTES_v1.0.0-RC2.md | Version 1.0.0 Build RC2 release notes |
| docs/ENGINEERING_CHARTER.md | Engineering principles and workflow |
| CHANGELOG.md | Release history |
| docs/TECHNICAL_DEBT_REGISTER.md | Engineering debt tracking |
| docs/reviews/ | Epic and architecture reviews |
| docs/architecture/ | Architecture Decision Records / capability specs |

---

# Technology Stack

Backend

- Python
- Flask
- SQLAlchemy
- Alembic

Database

- SQLite (development)
- PostgreSQL (production)

Testing

- pytest

Deployment

- Render

---

# Development Philosophy

Kwalitec is developed incrementally through small, test-driven milestones.

The project prioritises:

- educational correctness;
- maintainability;
- architectural consistency;
- explainability;
- long-term sustainability.

---

# Roadmap

## Version 1 (complete for RC2 Internal Alpha)

- Epic 1 — Curriculum Architecture — **Complete**
- Epic 2 — Educational Intelligence domain stack — **Complete** (Stage A product coexistence remains)
- V1SP — Stabilisation (lifecycle, Founder Command Centre, brand, performance, security) — **Complete for RC2 baseline**

## Version 2 / Epic 3 (deferred)

- Twin-first product cutover and Twin persistence
- Evidence journal product loops
- Exam Ready lifecycle
- Broader cohort / public registration (only after explicit release gates)
- Advanced adaptive interruption and coaching surfaces

---

# Contributing

Contributions should align with the Engineering Charter and Product Blueprint.

Before implementing significant functionality, contributors are expected to:

- analyse the problem;
- document the architecture;
- implement incrementally;
- maintain backwards compatibility where appropriate;
- provide comprehensive tests.

---

# License

License information will be added prior to the first public release.

---

# Closing Statement

Professional examinations shape careers.

Kwalitec exists to help students approach those examinations with greater confidence through evidence-based educational guidance, transparent reasoning, and disciplined engineering.
