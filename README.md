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
| Internal Alpha build | **Build RC2** |
| Programme | Version 1 Stabilisation (V1SP) · invite-only Internal Alpha |
| Operational readiness | APPROVED WITH MINOR ISSUES — High items closed in V1SP-001B |

Epic Status

- ✅ Epic 1 — Curriculum Architecture Foundation
- ✅ Epic 2 — Educational Intelligence (core learning loop live for Alpha)
- 🚧 Version 1 Stabilisation — final optimisation and release validation

See `knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md` and `knowledge/releases/V1SP-001B_OPERATIONAL_FIXES.md`.

---

# Major Components

## Curriculum Engine

Responsible for:

- curriculum loading
- validation
- repository
- provider independence
- canonical traversal

---

## Digital Twin

Represents the educational state of a student.

The Digital Twin evolves from Learning Evidence rather than assumptions.

Current domains include:

- Knowledge
- Memory

Future domains include:

- Behaviour
- Performance
- Readiness

---

## Decision Engine *(Planned)*

The Decision Engine will answer one question:

> **What is the highest-value thing this student should do next?**

Every recommendation will be evidence-based and explainable.

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
| knowledge/releases/ | Release and operational readiness reports |
| docs/ENGINEERING_CHARTER.md | Engineering principles and workflow |
| CHANGELOG.md | Release history |
| docs/TECHNICAL_DEBT_REGISTER.md | Engineering debt tracking |
| docs/reviews/ | Epic and architecture reviews |
| docs/architecture/ | Architecture Decision Records |

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

## Epic 1

Curriculum Architecture

**Complete**

---

## Epic 2

Educational Intelligence

- Behaviour Engine
- Performance Engine
- Readiness Engine
- Decision Engine

---

## Epic 3

Adaptive Learning

- Personalised recommendations
- Dynamic study planning
- Revision optimisation
- Explainable coaching

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
