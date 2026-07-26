# EP-007.1 — Student Journey Consolidation

**Programme:** EP-007.1 — Student Journey Consolidation  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Implemented  
**Implements:** REM-02 (single authoritative home) + REM-03 (one duration fact) from EP-005.2  
**Does not:** Change Runtime A / RecommendationService / PlanningService / ReadinessService educational reasoning  

---

## 1. Purpose

Remove the dual-home experience and establish one canonical student journey from login through study completion, so students no longer choose between competing homes or conflicting session clocks.

Evidence driving this programme:

| Source | Finding |
|---|---|
| EP-005.2 Student Journey Review | Dual homes / dual start paths; Near Universal friction |
| EP-005.2 Prioritised Remediation | **REM-02** single home; **REM-03** one duration fact |
| EP-006.3 MES Perception | Dual-home residual caps trust after MES delivery |
| EP-006.5 Readiness Perception | Dual homes remain a trust cap after readiness unpackability Pass |

---

## 2. Journey audit (pre-consolidation)

### 2.1 Competing stacks

| Stack | Entry | Session path |
|---|---|---|
| Legacy Learning Workspace | `/dashboard/` → `/missions/` | Mission hub → `/missions/<id>/session*` |
| Canonical Education OS | `/student/` → `/session/` | Home → overview → activity → reflection → summary → complete |

`KWALITEC_V2_SOLE_RUNTIME` redirected legacy shells when ON (production), but login still bounced through `dashboard.index`, completion / welcome / error CTAs often hard-coded Dashboard, and legacy duration used **weekday/weekend minutes** while Home/bridges used **preferred_session_minutes** (30 vs 90 theme).

### 2.2 Duplicate decisions removed

| Decision | Pre | Post (sole runtime) |
|---|---|---|
| Which home? | Dashboard vs Student Home | Student Home only |
| Where to start? | Missions hub vs Home CTA | Home primary CTA |
| How long tonight? | Preferred vs day-type minutes | Preferred first (shared resolver) |
| Where after login / calibration / onboarding? | Often Dashboard | Canonical home helper |

---

## 3. Canonical journey design

```
Login
  → (no plan) Study Plan wizard → Calibration (optional) → Home
  → (has plan) Student Home
       → Start / Resume Study Session
            → Overview → Activity → Reflection → Summary → Complete
       → Student Home
```

### Design principles

| Principle | Implementation |
|---|---|
| **Single Home** | `student.home` when `SOLE_RUNTIME`; helpers in `app/presentation/consolidation.py` |
| **Consistent duration** | `resolve_planned_session_minutes()` — prefer `preferred_session_minutes` |
| **Unified navigation** | Sole-runtime sidebar mirrors Education OS; Student chrome owns `/student/*` |
| **Clear progression** | Linear `/session/*` surfaces; resume via `SessionWorkspace.active_surface` |
| **Runtime A preserved** | Presentation / redirects only — no educational recalculation |

### Educational ownership (unchanged)

| Concern | Owner |
|---|---|
| What to study / recommendation MES | RecommendationService (+ Runtime A bridges) |
| Today's mission topic (legacy ORM) | PlanningService |
| Readiness estimate | ReadinessService |
| Journey chrome / redirects / duration display | Experience / presentation layer |

---

## 4. Implementation summary

| Change | Location |
|---|---|
| Canonical home / session-entry helpers | `app/presentation/consolidation.py` |
| Shared duration resolver | `app/application/student_experience/session_duration.py` |
| Legacy mission duration uses resolver | `StudySessionService.estimated_minutes_for_mission` |
| Bridge adapters use resolver | educational_runtime_bridge `*_adapter.py` |
| Login / onboarding / calibration / plan activate → canonical home | auth, alpha, calibration, study_plan, research, dashboard |
| Welcome modal on Student Home; CTA → canonical session entry | `student/home.html`, `welcome_modal.html` |
| Error pages → canonical home | `errors/403.html`, `404.html`, `500.html` |
| Template globals | `canonical_home_url`, `canonical_session_entry_url` |

### Flag posture

| Flag | Role after EP-007.1 |
|---|---|
| `KWALITEC_V2_SOLE_RUNTIME` | **Authoritative dual-home gate.** ON = single canonical journey. OFF = dual-run soak / Internal Alpha rollback. |
| `KWALITEC_UNIFIED_JOURNEY` | Optional guided DayExperience chrome (unchanged default OFF). |

Production (`render.yaml`) already sets `KWALITEC_V2_SOLE_RUNTIME=1`.

---

## 5. Backwards compatibility

When `SOLE_RUNTIME` is OFF:

- Login and root still land on Dashboard.
- Legacy `/dashboard/`, `/missions/`, `/analytics/` remain live.
- Duration resolver still prefers preferred minutes (improves consistency even in dual-run).

Legacy blueprints are **not deleted** — redirect shells remain for soak / rollback (Release Framework / V2-023).

---

## 6. Validation readiness

Regression suite: `tests/presentation/test_canonical_journey.py`.

Ready for **Tier B journey validation** (successor pack to EP-006.3 / EP-006.5 dual-home residual themes). Do not claim validated K1 Strong until Tier B re-tests dual-home / duration perception.

---

## 7. Non-goals

- No RecommendationService / PlanningService / ReadinessService math changes
- No second educational runtime
- No deletion of protected engines
- No Product Constitution or Release Framework amendments
- No claiming Gate G1 PASS from this programme alone

---

## References

- [`JOURNEY_TRACEABILITY.md`](JOURNEY_TRACEABILITY.md)
- [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md)
- [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md)
- `../ep005_2_educational_experience_validation/STUDENT_JOURNEY_REVIEW.md`
- `../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md`
- `knowledge/architecture/NAVIGATION_AUDIT.md`
- `knowledge/architecture/UNIFIED_STUDENT_JOURNEY_ARCHITECTURE.md`

---

**End of STUDENT_JOURNEY_CONSOLIDATION**
