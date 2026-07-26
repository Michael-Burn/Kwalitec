# Phase 1 — Consolidation Report

**Branch:** `feature/educational-architecture-consolidation`  
**Date:** 2026-07-23  
**Authority:** [PHASE_0_ARCHITECTURE_INVENTORY.md](PHASE_0_ARCHITECTURE_INVENTORY.md) · [PHASE_1_CANONICAL_DECLARATION.md](PHASE_1_CANONICAL_DECLARATION.md)

---

## Summary

Phase 1 declares a single Education Operating System presentation architecture and begins controlled consolidation without deleting protected educational engines. Canonical student surfaces are Student Experience (`/student/*`) and Session Experience (`/session/*`). Legacy dashboard / missions / analytics remain registered and are marked READY FOR MIGRATION; under sole runtime they redirect to canonical surfaces. Student-visible “Version 2 / alternative experience” CTAs are removed. Shared `EducationalStateService` supplies one Twin/Adaptive/Journey/Mission read model to Dashboard, Journey, Revision, and Analytics projections.

---

## Components kept (canonical)

| Capability | Canonical implementation |
|------------|--------------------------|
| Dashboard | `/student/` · `HomeService` + coach insight |
| Journey | `/student/journey` · Learning Journey Engine via port |
| Coach | Home coach insight panel |
| Analytics | `/student/history` (label: Analytics) |
| Session | `/session/<id>/*` Session Experience |
| Reflection | `/session/<id>/reflection` |
| Readiness | Twin readiness aggregation (Experience path) |
| Mission presentation | Home CTA → Session; Mission Adapter / Engine 2.0 |
| Educational State | `app/application/educational_state/` |

---

## Components merged (presentation wiring)

- Student nav labels → one OS tree: Dashboard · Journey · Revision · Analytics · Settings · Study Plan · Help  
- Home / History / Journey / Revision projections → shared `EducationalStateService` cache  
- Product language constants aligned with consolidated labels  
- Dual-run “Version 2 Learning Experience” / “Back to Dashboard” CTAs removed  

---

## Components retired (student-visible only — code retained)

| Item | Disposition |
|------|-------------|
| Dual-run Version 2 CTA | Removed from templates |
| Competing footer “Back to Dashboard” | Removed |
| Legacy home / missions / analytics as *default* under sole runtime | Redirect to canonical (routes not deleted) |

---

## Components READY FOR MIGRATION (not deleted)

- Legacy `/dashboard/`, `/missions/`, `/analytics/` blueprints and templates  
- V1 sidebar chrome (still hosts Study Plan wizard path outside sole runtime)  
- `ReadinessService` ORM composite (V1 surfaces)  
- `StudySessionService` evidence write path (protected)  
- `PlanningService` / `MissionService` ORM mission generation  
- Duplicate `mission_engine` package (engine consolidation deferred)  
- V1 Analytics charts (parity gap vs Twin History)  

---

## Educational components preserved

IFoA syllabus integration · CMP educational model · educational services · Student Digital Twin · Learning Evidence · Recommendation / Adaptive Decision engines · educational reasoning · mission generation · domain models — **untouched as authorities**.

---

## Tests executed

```bash
.venv/bin/python -m pytest tests/ -q
```

**Outcome (this branch):** 33976 passed, 7 skipped, 18 failed.

Failures remaining are outside Phase 1 presentation consolidation (Education OS `/eos` snapshot/purity suite, brand-identity asset checks, CLI/startup admin creation, static asset budget, founder IA copy). Consolidation-related suites (student nav, dual-run, educational state, product language, alpha smoke) pass.

---

## Migration impact

**None** — no Alembic revisions added or changed.

---

## Architecture compliance

- Layering preserved: presentation → Student Experience application → ports → Twin/Adaptive/Journey/Mission.  
- Curriculum V1/V2 loadability unchanged.  
- ADR-007 honored: sole runtime **not** enabled by default; V2-020 evidence gates remain the cutover gate.  
- No protected educational engines deleted.

---

## Remaining technical debt

1. Legacy presentation still reachable when sole runtime is off (intentional dual-run soak).  
2. Analytics chart parity: V1 `/analytics/` richer than Twin History.  
3. Session evidence write path still dual until Session Experience fully owns Evidence Authority writes.  
4. Two mission engine packages remain; adapter is the cutover router.  
5. V1 sidebar still a second chrome for Study Plan wizard hosts outside Experience.  
6. PRODUCT_LANGUAGE_GUIDE still documents some historical “Home” synonyms in narrative sections.

---

## Outstanding architectural risks

1. Enabling `KWALITEC_V2_SOLE_RUNTIME` without V2-020 evidence gates risks dual-authority defects.  
2. Redirecting Analytics before chart parity may reduce founder/student insight on sole runtime.  
3. Premature deletion of `StudySessionService` / `ReadinessService` would break Learning Evidence — **do not delete**.  

---

## Stop conditions observed

Phase 0 inventory was missing from the repo; it was reconstructed from the live codebase and recorded as the authoritative Phase 0 reference before declarations. Sole runtime was **not** flipped by default (ADR-007 / FINAL RULE).
