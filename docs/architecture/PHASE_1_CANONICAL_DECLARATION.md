# Phase 1 — Canonical Architecture Declaration

**Status:** Binding for consolidation on this branch  
**Authority:** [PHASE_0_ARCHITECTURE_INVENTORY.md](PHASE_0_ARCHITECTURE_INVENTORY.md)  
**Date:** 2026-07-23  
**Mode:** Controlled Refactoring — declare + wire presentation; do not delete protected engines  

---

## Canonical selections

| Capability | Canonical | Inventory ID | Why selected |
|------------|-----------|--------------|--------------|
| **Dashboard** | Student Home `/student/` (`presentation/student` + `HomeService`) | D-B | Sole learner home projection wired to Twin / Adaptive / Mission ports; documented as Experience authority (`STUDENT_EXPERIENCE.md`). Legacy dashboard remains READY FOR MIGRATION. |
| **Journey** | `/student/journey` + Learning Journey Engine | J-B | Only dedicated journey UI; journey progression authority is explicit in `learning_journey/engine.py`. |
| **Coach** | Student Home coach insight panel | C-B | Explicit product coaching slot on Home; no separate coach route. V1 tips/explainability merge into this panel over time. |
| **Analytics** | `/student/history` (student label: **Analytics**) | A-B | Twin-backed educational progress surface. V1 `/analytics/` charts remain READY FOR MIGRATION until chart parity is proven — not deleted. |
| **Session** | `/session/<id>/*` Session Experience | S-B | Full overview → activity → reflection → summary workflow with Twin/runtime ports. V1 LXP path READY FOR MIGRATION; evidence authority must stay intact. |
| **Reflection** | `/session/<id>/reflection` | R-B | Only active reflection UI; V1 review routes are redirects. |
| **Readiness** | Twin readiness aggregation (`domain/readiness` + Twin ports) | RD-B | Educational truth for Experience. V1 `ReadinessService` remains for legacy surfaces until migration completes — calculators not deleted. |
| **Mission Engine** | Mission Adapter → Mission Engine 2.0 (`mission_engine_v2`) | M-B | Cutover router already exists; Home CTA is the student presentation. ORM `PlanningService` path READY FOR MIGRATION, not removed. |
| **Educational State** | `EducationalStateService` snapshot (Twin + Adaptive + Journey + Mission ports) | New facade | Single read model; Dashboard / Journey / Coach / Analytics / Revision project from it. No per-screen recomputation of readiness/mastery. |

---

## Alternatives (READY FOR MIGRATION — not deleted)

| Alternative | Disposition |
|-------------|-------------|
| Legacy `/dashboard/` | Keep registered; under sole runtime redirect to Student Home |
| Legacy `/missions/` session UX | Keep; under sole runtime redirect toward Experience session entry |
| Legacy `/analytics/` | Keep for chart parity soak; under sole runtime redirect to History/Analytics |
| V1 sidebar chrome | Keep for non–sole-runtime / Study Plan wizard host; student chrome is canonical nav |
| Dual-run “Version 2” CTAs | Remove student-visible version terminology |
| `ReadinessService` ORM composite | Protected calculator until Twin path owns all surfaces |
| `StudySessionService` evidence path | Protected — Session Experience must continue to honour Learning Evidence |

---

## One navigation tree (canonical)

Primary (Experience chrome):

1. **Dashboard** → `student.home`  
2. **Journey** → `student.journey`  
3. **Revision** → `student.revision` (highest-value focus / today’s revision)  
4. **Analytics** → `student.history`  
5. **Settings** → `student.profile` (examination / preferences) + link to account settings  

System / workflow entry points (same tree, not competing products):

6. **Study Plan** → `study_plan.index`  
7. **Today’s Session** → Home primary CTA → Session Experience  
8. **Help** → `alpha.help_centre`  

Coach is embedded on Dashboard (not a separate top-level duplicate product).

---

## Educational State contract

```
EducationalStateSnapshot  (single load per request assembly)
        │
        ├── Dashboard (Home + Coach insight)
        ├── Journey
        ├── Revision
        ├── Analytics (History)
        ├── Readiness cards
        └── Reflection / Session (consume Twin/session ports; no parallel mastery math)
```

Forbidden: Dashboard, Journey, Coach, or Analytics inventing independent progress/readiness/mastery formulas.

---

## Phase 1 stop conditions (FINAL RULE)

Stop and report (do not guess) if:

1. Sole-runtime cutover is requested without V2-020 evidence gates.  
2. Deleting Twin, Evidence Authority, CMP, IFoA curriculum, or domain engines is proposed.  
3. Analytics chart parity is unclear — retain `/analytics/` as READY FOR MIGRATION.  
4. Session evidence write path would diverge without an explicit bridge.

Phase 1 therefore **does not** flip `KWALITEC_V2_SOLE_RUNTIME` by default and **does not** delete legacy blueprints.
