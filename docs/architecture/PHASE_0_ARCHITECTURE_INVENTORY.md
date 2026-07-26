# Phase 0 — Architecture Inventory

**Status:** Authoritative reference for Phase 1 consolidation  
**Branch:** `feature/educational-architecture-consolidation`  
**Date:** 2026-07-23  
**Mode:** Inventory only — no deletions  

This inventory enumerates competing student presentation layers and educational
engines as they exist in the repository. It is the authoritative input for
Phase 1 Canonical Architecture Declaration.

Protected architecture (never remove): IFoA syllabus integration, CMP educational
model, educational services, Student Digital Twin, Learning Evidence,
Recommendation / Adaptive Decision engines, educational reasoning, mission
generation, and domain models.

---

## 1. Dual student stacks

| Stack | Entry | Default? | Flag gate |
|-------|-------|----------|-----------|
| **Legacy (V1)** | `/dashboard/`, sidebar chrome | Yes (default `/`) | Always registered |
| **Student Experience** | `/student/`, `/session/` | When `KWALITEC_V2_SOLE_RUNTIME=1` | `KWALITEC_V2_STUDENT_EXPERIENCE` or sole runtime |

Blueprint registration: `app/__init__.py` (`_register_blueprints`, `_register_routes`).  
Flags: `app/application/config/v2_flags.py`.  
Retirement programme: `knowledge/version2/V2_020_RETIREMENT_RUNBOOK.md` (ADR-007).

---

## 2. Capability inventory

### 2.1 Dashboard

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| D-A | Legacy dashboard | `app/dashboard/routes.py` → `/dashboard/` · `templates/dashboard/index.html` | Production default |
| D-B | Student Home | `app/presentation/student/routes.py` → `/student/` · `templates/student/home.html` | Dual-run / sole-runtime target |

**Services (D-A):** `StudyPlanService`, `MissionService`, `ReadinessService`, `RecommendationService`, optional `EducationalDashboardComposer` + Twin when `ENABLE_EDUCATIONAL_ORCHESTRATOR`.  
**Services (D-B):** `StudentExperienceService` → `HomeService` via Twin / Adaptive / Mission ports.

### 2.2 Journey

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| J-A | Embedded progress | Dashboard + Study Plan views (no dedicated journey URL) | Production |
| J-B | Journey surface | `/student/journey` · `JourneyService` · Learning Journey Engine | Dual-run target |

### 2.3 Coach

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| C-A | Distributed tips / explainability | Dashboard study tips + recommendation narrative | Production supporting |
| C-B | Coach insight panel | Embedded on Student Home (`coach_insight` view model) | Dual-run target |

No standalone `/coach` route exists.

### 2.4 Analytics

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| A-A | Analytics page | `/analytics/` · `AnalyticsService` + `ReadinessService` | Production |
| A-B | History surface | `/student/history` · Twin learning insights | Dual-run target (progress, not full chart parity) |

### 2.5 Study Session

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| S-A | Mission study session (LXP) | `/missions/<id>/session*` · `StudySessionService` | Production evidence writer |
| S-B | Session Experience | `/session/<id>/*` · `SessionExperienceService` | Dual-run target |

### 2.6 Reflection

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| R-A | Legacy review | `/missions/review/*` redirects to session closure | Legacy shims only |
| R-B | Session reflection | `/session/<id>/reflection` · `ReflectionService` | Dual-run target |

### 2.7 Readiness

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| RD-A | ORM composite | `app/services/readiness_service.py` | Production SoT for V1 surfaces |
| RD-B | Twin aggregation | `domain/readiness/aggregation.py` + Twin pipeline | Engine authority for Experience |
| RD-C | EI overlay | `EducationalDashboardComposer` on V1 dashboard | Flag-gated bridge |

### 2.8 Mission

| ID | Implementation | Path | Status |
|----|----------------|------|--------|
| M-A | Planning + MissionService | `/missions/` · ORM missions | Production |
| M-B | Mission Engine packages | `application/mission_engine/` and `application/mission_engine_v2/` | Engines + Mission Adapter cutover |
| M-C | Experience mission card | Student Home CTA → Session | Dual-run presentation |

---

## 3. Navigation surfaces (duplicates)

| Surface | Location | Links |
|---------|----------|-------|
| V1 sidebar | `templates/partials/sidebar.html` | Dashboard, Study Plan, Session, Analytics, Settings, Help |
| Student top nav | `presentation/student/navigation.py` | Home, Journey, Revision, History, Profile |
| Session steps | `presentation/session/navigation.py` | Overview → Activity → Reflection → Summary → Complete |
| Dual-run CTAs | `dashboard/index.html`, `student/base.html` | “Open Version 2 Learning Experience” / “Back to Dashboard” |

---

## 4. Educational state sources (dual truth risk)

### Production writes / V1 calculators

- `CurriculumService`, `LearningService`, `AdaptiveLearningService`
- `ReadinessService`, `RecommendationService`
- `PlanningService` / `MissionService`
- `StudySessionService` + `EducationalEvidenceAuthority`

### Target authority (Experience / Twin)

- Student Digital Twin (`domain/student_twin`, Twin Provider / Update Coordinator)
- `domain/readiness/aggregation.py`
- Adaptive Decision Engine / `domain/decision/engine.py`
- Learning Journey Engine
- Learning Session Runtime + Activity Engine
- Mission Adapter → Mission Engine 2.0

### Bridge

- `application/mission_adapter/`
- Experience + Session composition roots
- Feature flags in `v2_flags.py` / `feature_flags.py`

---

## 5. Student-visible version terminology (found)

| Location | Phrase |
|----------|--------|
| `templates/dashboard/index.html` | “Open Version 2 Learning Experience” |
| Dual-run footer | Competing experience entry (“Back to Dashboard”) |

Internal package docs and founder gates may still say “Version 2”; those are not student-facing.

---

## 6. READY FOR MIGRATION (presentation only)

Do **not** delete in Phase 0/1 without soak. Marked for migration:

1. V1 `/dashboard/` widgets vs Student Home panels  
2. Dual-run version CTAs  
3. V1 `/missions/` session templates vs `/session/*`  
4. Legacy `/missions/review/*` shims  
5. V1 `/analytics/` vs Student History (analytics chart parity gap remains)  
6. Parallel readiness displays (`ReadinessService` vs Twin summary)  
7. Duplicate mission engine packages (presentation cutover only; engines protected until adapter sole path)  
8. V1 sidebar vs Student navigation chrome  
9. `StudyTipsService` vs Home coach insight  

---

## 7. Explicit non-actions

- Do not drop Twin, Evidence, CMP, IFoA curriculum, recommendation/decision engines, or domain models.
- Do not enable `KWALITEC_V2_SOLE_RUNTIME` by default (ADR-007 / V2-020 preconditions).
- Do not invent a second educational math path under “consolidation.”
