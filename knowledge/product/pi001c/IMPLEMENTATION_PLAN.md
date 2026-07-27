# PI-001C — Implementation Plan

## Phase 1 — domain rules

1. Educational event types
2. Enrolment / plan / mission / journey state transitions
3. Pure progress derivation from events + progress model

## Phase 2 — persistence

1. ORM tables for enrolment, plan instance, mission instance, events
2. Alembic migration revising PI-001A head

## Phase 3 — application runtime

1. `EducationalRuntimeEngineService` consuming PI-001B artefacts
2. Coexistence policy vs JSON Runtime A
3. Readiness + Estimated Knowledge input projections

## Phase 4 — evidence

1. Domain unit tests
2. Integration + end-to-end acceptance tests
3. Architecture / state / event / migration docs + completion report

## Out of scope

- UI / wizard cutover
- Twin cutover
- Rewriting ReadinessService formulas
- Minting EK from mission completion
