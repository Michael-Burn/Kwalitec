# EP-007.1 — Journey Traceability

**Programme:** EP-007.1 — Student Journey Consolidation  
**Date:** 2026-07-26  
**Purpose:** Map every student path from login through study completion to the canonical journey, and record what changed vs what was preserved.

---

## 1. Canonical path (sole runtime ON)

| Step | Route | Owner | Notes |
|---:|---|---|---|
| 1 | `POST /auth/login` | `auth.login` | Success → `student.home` (or wizard if no plan) |
| 2 | `GET /student/` | `student.home` | Single Home; Start / Resume CTA |
| 3 | `POST /student/session/start` | `student.start_session` | Mission port / Runtime A bridge |
| 4 | `GET /session/<id>/overview` | `session.overview` | Resume guard |
| 5 | `POST …/begin` → `…/activity` | session | Study |
| 6 | Reflection → Summary → Complete | session | Linear surfaces |
| 7 | `POST …/complete` | session | → `student.home` |

Optional: Calibration / Study Plan wizard insert before step 2 for new students. Welcome modal may appear on Home.

---

## 2. Legacy path (sole runtime OFF — soak / Alpha)

| Step | Route | Notes |
|---:|---|---|
| 1 | Login → `dashboard.index` | Dual-run preserved |
| 2 | Dashboard CTA → `mission.missions` | Legacy hub |
| 3 | `/missions/<id>/session*` | Legacy session UX |
| — | `/student/*` still reachable by URL | Competing home if both used |

---

## 3. Redirect map (sole runtime ON)

| Incoming | Redirects to | Module |
|---|---|---|
| `/` | `student.home` | `app/__init__.py` |
| `/dashboard/` | `student.home` | `dashboard.routes` + `redirect_if_sole_runtime` |
| `/missions/` (+ nested) | `student.home` | `mission.routes` |
| `/analytics/` | `student.history` | `analytics.routes` |
| Login / onboarding / calibration / plan activate | `canonical_home_endpoint()` | consolidation helpers |

---

## 4. Duration traceability (one fact)

| Surface | Pre EP-007.1 | Post EP-007.1 |
|---|---|---|
| Student Home / bridges | `preferred_session_minutes` | Same via `resolve_planned_session_minutes` |
| Legacy Mission / StudySession | weekday / weekend minutes | **Preferred first**, day-type fallback |
| Mission template fallback | weekday / weekend | Preferred first, then day-type |

Shared resolver: `app/application/student_experience/session_duration.py`.

---

## 5. Finding → fix traceability

| Evidence ID / theme | Remediation | EP-007.1 artefact |
|---|---|---|
| Dual homes (EV-PERC-002, EP-005.2, EP-006.3/5) | REM-02 | Sole-runtime canonical home + entry redirects |
| Duration mismatch 30 vs 90 | REM-03 | Shared duration resolver |
| Login bounce via Dashboard | Journey audit | `auth.login` → `canonical_home_url` |
| Welcome / errors → Dashboard | Journey audit | Template globals + Student Home welcome |
| Runtime A ownership risk | Constraint | No service math changes; presentation only |

---

## 6. Explicit non-changes

| Component | Status |
|---|---|
| RecommendationService | Unchanged |
| PlanningService | Unchanged |
| ReadinessService | Unchanged |
| Runtime A educational calculators | Unchanged |
| Product Constitution / Release Framework | Unchanged |
| Legacy blueprint deletion | Not done (rollback shells retained) |

---

## 7. Test traceability

| Criterion | Test |
|---|---|
| Canonical navigation | `test_legacy_shells_redirect_under_sole_runtime`, `test_root_redirects_to_student_under_sole_runtime` |
| Login entry | `test_login_lands_on_student_home_under_sole_runtime` |
| Session continuity contract | `test_session_complete_returns_to_student_home` |
| Journey / duration consistency | `test_duration_consistency_*`, `test_study_session_service_matches_canonical_duration` |
| Backwards compatibility | `test_dual_run_preserves_dashboard_home_when_sole_off`, `test_login_lands_on_dashboard_under_dual_run` |

Suite: `tests/presentation/test_canonical_journey.py`.

---

**End of JOURNEY_TRACEABILITY**
