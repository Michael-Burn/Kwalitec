# PI-001A — Implementation Plan

**Programme:** PI-001A — Founder Curriculum Studio Foundation  
**Date:** 2026-07-27  

---

## Phase 0 — Orientation (done)

1. Review `PROJECT_CONTEXT.md`, `ARCHITECTURE.md`, V2 curriculum docs.  
2. Inventory curriculum models, services, Studio/Ingestion/Management packages, Founder UI.  
3. Produce gap analysis vs required lifecycle.

## Phase 1 — Design (done)

1. Define foundation lifecycle stages and publication safety invariant.  
2. Design durable tables (subject, version, document, audit, published package).  
3. Define service API for the full lifecycle.  
4. Define `PublishedCurriculumAuthority` as the only student-facing curriculum package reader from Studio.

## Phase 2 — Implement foundation (done)

1. Domain package `curriculum_studio_foundation`.  
2. ORM models + Alembic migration `202607270001`.  
3. `CurriculumStudioFoundationService` + DTOs + exceptions.  
4. `PublishedCurriculumAuthority`.  
5. Wire Studio upload form/route (functional, not polished).

## Phase 3 — Tests (done)

1. Domain unit tests (lifecycle + draft isolation).  
2. Application lifecycle tests (create → publish, audit, subject-agnostic).  
3. Integration tests (persistence + Founder upload HTTP).  
4. Update Studio presentation expectations for upload primary CTA.

## Phase 4 — Documentation (done)

1. `ARCHITECTURE.md`  
2. `GAP_ANALYSIS.md`  
3. `IMPLEMENTATION_PLAN.md` (this file)  
4. `COMPLETION_REPORT.md`  
5. `TEST_EVIDENCE.md`

## Phase 5 — Out of scope / follow-ups

1. Student runtime cutover to published packages.  
2. Durable Management catalogue mirror (optional).  
3. Binary CMP/PDF extractors.  
4. Mission / plan / recommendation consumption of new subjects.

---

## Acceptance checklist

- [x] Create subject  
- [x] Upload curriculum documents  
- [x] Track processing state  
- [x] Review parsed curriculum  
- [x] Validate curriculum  
- [x] Publish curriculum version  
- [x] Drafts unreachable via published authority  
- [x] Subject-agnostic evidence (`LAW1`)  
- [x] Unit + integration tests passing  
