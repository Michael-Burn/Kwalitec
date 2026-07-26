# Planning Blueprint Model

**Programme:** VI — Master Planner  
**Milestone:** MS005 — Planning Blueprint Model  
**Classification:** Educational blueprint — bridge from Planning Decision Package to future scheduling  
**Status:** APPROVED — governing for educational journey-structure reasoning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how an excellent IFoA tutor organises settled planning decisions into a coherent study journey structure** before any calendar or timetable is produced.

It answers *what educational phases and components compose the journey*, *how the student progresses through them*, and *how that structure is explained*.

It does **not** allocate dates, generate schedules, or implement Runtime A services.

> **This blueprint organises educational decisions already made.  
> It introduces no new educational reasoning.  
> Future scheduling engines place this blueprint onto a calendar — they never invent educational structure in packing code.**

## Authority

Subordinate to:

1. [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`EDUCATIONAL_LOGIC_REGISTRY.md`](../EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
5. [`../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`](../student_profile/STUDENT_EDUCATIONAL_PROFILE.md) (Programme VI / MS002)
6. [`../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`](../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md) (Programme VI / MS003)
7. [`../planning/EDUCATIONAL_PLANNING_MODEL.md`](../planning/EDUCATIONAL_PLANNING_MODEL.md) (Programme VI / MS001)
8. [`../planning_engine/PLANNING_DECISION_ENGINE.md`](../planning_engine/PLANNING_DECISION_ENGINE.md) (Programme VI / MS004)

Sole educational input for assembly:

- **Planning Decision Package** produced under MS004 — the complete set of educational planning decisions for a named sitting

Related (non-authoritative for educational meaning):

- [`knowledge/subsystems/study-planning.md`](../../subsystems/study-planning.md) — current Runtime A subsystem map

## Contents

| Document | Role |
|---|---|
| [`PLANNING_BLUEPRINT_MODEL.md`](PLANNING_BLUEPRINT_MODEL.md) | Constitutional overview: what the blueprint is, stack position, derivation rule |
| [`BLUEPRINT_PHASES.md`](BLUEPRINT_PHASES.md) | Ordered educational phases of an ideal study journey (date-independent) |
| [`BLUEPRINT_COMPONENTS.md`](BLUEPRINT_COMPONENTS.md) | Educational building blocks that compose phases |
| [`BLUEPRINT_PROGRESSION.md`](BLUEPRINT_PROGRESSION.md) | Entry, progression, pause, recovery, revision, and completion criteria |
| [`BLUEPRINT_EXPLAINABILITY.md`](BLUEPRINT_EXPLAINABILITY.md) | How the journey structure is explained to students |

## Relationship to MS001–MS004

| Horizon | Job |
|---------|-----|
| **MS002 — Student Educational Profile** | Diagnose *where the student is now* educationally |
| **MS003 — Educational Strategy** | Choose *which overall educational approach to adopt* |
| **MS001 — Educational Planning Model** | Define *design law* (objectives, constraints, phases, decision classes) |
| **MS004 — Planning Decision Engine** | Produce *structured planning decisions* (Planning Decision Package) |
| **MS005 — this corpus** | Organise those decisions into a *date-independent study journey blueprint* |

```
Profile (diagnosis)
     →  Strategy (approach)
           →  Planning Model (design law)
                 →  Planning Decision Engine
                       →  Planning Decision Package
                             →  Planning Blueprint (this milestone)
                                   →  Scheduling Engine / Study Timetable (MS006)
```

MS004 settles *what* educationally must be true.  
MS005 organises those truths into *journey structure* ready for scheduling — without inventing new educational meaning.

Downstream allocation (Programme VI):

- [`../scheduling/`](../scheduling/) — Scheduling Engine Specification (MS006)

## Architectural requirement

Every phase, component, and progression rule in this blueprint must be **derived entirely from the Planning Decision Package** (and the MS001–MS004 law that package already embodies).

| Lawful | Unlawful |
|--------|----------|
| Organise PD-01…PD-16 / D1–D20 decisions into phases and components | Introduce new educational objectives, constraints, or decision meanings |
| Name journey structure that scheduling will later place on dates | Allocate calendar cells, minutes, or session UI |
| Explain structure using package explainability attachments | Invent readiness, mastery, or pass claims absent from the package |

No blueprint element may exist without a Planning Decision Package warrant.

## Out of scope (MS005)

- Scheduling / calendar allocation / date calculations
- Study plan generation or rebalancing code
- Optimisation algorithms or numeric weighting schemes
- Recommendation engines
- Database models, feature flags, or Runtime A integration
- Software class designs or service interfaces
- New educational reasoning beyond organising existing decisions

## How to use this corpus

1. Read `PLANNING_BLUEPRINT_MODEL.md` first.
2. Map package decisions onto phases via `BLUEPRINT_PHASES.md`.
3. Compose phases from components in `BLUEPRINT_COMPONENTS.md`.
4. Apply progression rules from `BLUEPRINT_PROGRESSION.md` — educational criteria only, no dates.
5. Require explainability contracts from `BLUEPRINT_EXPLAINABILITY.md` before student-facing journey narration.
6. Do not implement scheduling that invents phases, intensity envelopes, or revision protection outside a blueprint derived from a lawful package.
7. Do not implement algorithms that contradict this corpus without amending it first.
