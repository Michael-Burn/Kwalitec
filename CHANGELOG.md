# Changelog

All notable changes to Kwalitec are documented in this file.

The format follows the principles of Keep a Changelog and Semantic Versioning.

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
