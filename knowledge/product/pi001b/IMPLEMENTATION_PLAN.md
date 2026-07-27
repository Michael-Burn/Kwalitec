# PI-001B — Implementation Plan

## Phase 1 — published package fidelity

1. Preserve entry attributes when reconstructing ingestion payloads.
2. Preserve prerequisite edges and normalized metadata in published package structure.
3. Keep PI-001A publish-only safety invariant unchanged.

## Phase 2 — educational artefact derivation

1. Add a domain deriver for published curriculum packages.
2. Derive:
   - curriculum graph
   - study plan template
   - mission templates
   - journey structure
   - progress model
3. Expose snapshots through an application service backed by `PublishedCurriculumAuthority`.

## Phase 3 — equivalence evidence

1. Add unit tests for prerequisite-aware derivation.
2. Add integration test for a newly published subject.
3. Add CS1 equivalence test against the existing JSON hierarchy/order.
4. Re-run existing PI-001A integration and curriculum parity tests.

## Out of scope

- UI redesign
- Twin cutover
- Live study-plan wizard cutover to founder-published subjects
- Mission persistence refactor
- Readiness service denominator rewrite
