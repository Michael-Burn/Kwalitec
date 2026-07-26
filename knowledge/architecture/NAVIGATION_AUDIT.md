# MS-001 — Navigation Audit

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)  
**Evidence date:** 2026-07-25  
**Scope:** Every path a student can take to begin, resume, or complete a study session.

---

## 1. Runtime context

Kwalitec exposes **two coexisting presentation stacks**:

| Stack | Blueprints | Flag |
|---|---|---|
| **Legacy (V1)** | `dashboard`, `mission`, `analytics` | Default when `KWALITEC_V2_SOLE_RUNTIME` is unset/false |
| **Canonical (V2 Education OS)** | `student`, `session` | Forced when `KWALITEC_V2_SOLE_RUNTIME` is truthy |

Shared infrastructure (not sole-runtime-gated): `study_plan`, `calibration`, `alpha`, `settings`, `auth`, `research`.

Gate implementation: `app/presentation/consolidation.py` → `redirect_if_sole_runtime()`.  
Flag resolution: `app/application/config/v2_flags.py` (`Version2FeatureFlags.SOLE_RUNTIME`).

Root `/` (`app/__init__.py`): redirects to `student.home` under sole runtime, else `dashboard.index`.

---

## 2. Study entry points (complete inventory)

### 2.1 Canonical — Student Home primary CTA

| Field | Value |
|---|---|
| **Route** | `POST /student/session/start` |
| **Blueprint** | `student` (`app/presentation/student`) |
| **Controller** | `start_session` — `app/presentation/student/routes.py` |
| **Template** | Form on `app/templates/student/home.html` (no dedicated template for POST) |
| **Component** | Primary CTA `[data-student-cta="primary"]`; chrome in `student.js` |
| **Service** | `start_todays_session` → `StudentExperienceService.start_session` → `MissionPort.start_session` (`ExperienceMissionAdapter`) |
| **Decision owner** | Presentation: route validates form. Educational start: Mission port (opaque projection / optional engine). **Not** `PlanningService`. |
| **Destination** | `session.overview` (`/session/<session_id>/overview`) if `session_id` returned; else `student.home` |

**Guards:** `@login_required`; WTForms `StartSessionForm`; `PortUnavailable` / `StudentExperienceError` → flash + redirect home.

---

### 2.2 Canonical — Revision begin CTA

| Field | Value |
|---|---|
| **Route** | `POST /student/revision/begin` |
| **Blueprint** | `student` |
| **Controller** | `begin_revision` — `app/presentation/student/routes.py` |
| **Template** | Form on `app/templates/student/revision.html` |
| **Component** | Revision primary option form (`BeginRevisionForm`) |
| **Service** | Same `start_todays_session` path as §2.1; additionally `emit_revision_started` on composition |
| **Decision owner** | Same as §2.1; revision option_id is telemetry/event only for start |
| **Destination** | `session.overview` or `student.home` / `student.revision` on error |

---

### 2.3 Canonical — Session linear flow (begin / resume / complete)

| Route | Method | Controller | Template | Service | Destination |
|---|---|---|---|---|---|
| `/session/<id>/` · `/overview` | GET | `overview` | `session/overview.html` | `resume_redirect_if_needed` → `load_page` → `SessionExperienceService` | Stay / redirect to active surface |
| `/session/<id>/begin` | POST | `begin` | — | `begin_session` | `session.activity` |
| `/session/<id>/activity` | GET | `activity` | `session/activity.html` | resume + load | Stay / resume redirect |
| `/session/<id>/activity/answer` | POST | `answer` | — | `submit_answer` | `session.activity` |
| `/session/<id>/activity/advance` | POST | `advance` | — | `advance_activity` | `session.activity` or `session.reflection` |
| `/session/<id>/reflection` | GET | `reflection` | `session/reflection.html` | resume + load | Stay / resume |
| `/session/<id>/reflection/continue` | POST | `reflection_continue` | — | `continue_reflection` | `session.summary` |
| `/session/<id>/summary` | GET | `summary` | `session/summary.html` | resume + load | Stay / resume |
| `/session/<id>/complete` | GET | `complete` | `session/complete.html` | resume + load | Stay / resume |
| `/session/<id>/complete` | POST | `finish` | — | `complete_and_return` | `student.home` |

**Blueprint:** `session` (`app/presentation/session`).  
**Decision owner (resume):** `SessionWorkspace.active_surface` via `resume_redirect_if_needed` (`app/presentation/session/views.py`) — URL cannot rewind/skip.  
**Guards:** ownership (`SessionOwnershipError` → 403); missing session → flash + `student.home`.

---

### 2.4 Legacy — Dashboard → Mission hub

| Field | Value |
|---|---|
| **Route** | `GET /dashboard/` |
| **Blueprint** | `dashboard` |
| **Controller** | `index` — `app/dashboard/routes.py` |
| **Template** | `dashboard/index.html` |
| **Component** | Start/Resume/Review CTA linking to `mission.missions` |
| **Service** | `PlanningService.generate_today_mission`, `MissionService.get_today_mission`, `RecommendationService`, `ReadinessService`, `LearningLifecycleService` |
| **Decision owner** | Mission topic: `PlanningService`. Recommendation card: `RecommendationService` (or EI orchestrator when flagged). Nav destination of CTA: template (status-based label) → always `mission.missions`. |
| **Destination** | Under sole runtime: `student.home`. Else: render dashboard. Onboarding pending → `alpha.onboarding`. |

---

### 2.5 Legacy — Mission hub (Today's Study Session)

| Field | Value |
|---|---|
| **Route** | `GET /missions/` |
| **Blueprint** | `mission` |
| **Controller** | `missions` — `app/mission/routes.py` |
| **Template** | `mission/index.html` |
| **Component** | Start / Resume / Review buttons by `Mission.status` |
| **Service** | `PlanningService.generate_today_mission`, `MissionService.get_today_mission`, `StudySessionService.build_session_context`, `ReadinessService`, `LearningLifecycleService` |
| **Decision owner** | Topic content already decided by prior `generate_today_mission`. Page owns display and CTA routing by status. |
| **Destination** | Sole runtime → `student.home`. Else render. |

---

### 2.6 Legacy — Start study session

| Field | Value |
|---|---|
| **Route** | `POST /missions/<mission_id>/session/start` |
| **Blueprint** | `mission` |
| **Controller** | `start_study_session` |
| **Template** | — |
| **Component** | Form on `mission/index.html` |
| **Service** | `StudySessionService.start_session` (`Mission.status` Pending → In Progress) |
| **Decision owner** | Ownership check + status transition in `StudySessionService` |
| **Destination** | `mission.study_session`; sole runtime → `student.home` |

---

### 2.7 Legacy — Resume / open in-progress session

| Field | Value |
|---|---|
| **Route** | `GET /missions/<mission_id>/session` |
| **Blueprint** | `mission` |
| **Controller** | `study_session` |
| **Template** | `mission/session.html` |
| **Component** | Timer/checklist via `app/static/js/study_session.js` |
| **Service** | `StudySessionService.get_owned_mission`; auto-`start_session` if still Pending |
| **Decision owner** | If Completed → redirect recorded. Else render. |
| **Destination** | Session screen, recorded page, or sole-runtime home |

---

### 2.8 Legacy — Finish / practice outcome / recorded

| Route | Controller | Service | Destination |
|---|---|---|---|
| `GET/POST /missions/<id>/session/finish` | `finish_study_session` | `StudySessionService.finish_session` / `record_practice_outcome` | `mission.study_session_recorded` |
| `GET /missions/<id>/session/recorded` | `study_session_recorded` | `StudySessionService.build_session_feedback` | Render feedback |
| `POST /missions/<id>/complete` | `complete_mission` | Closure redirect helper | Finish / recorded |
| `GET/POST /missions/review/<id>` | `review_mission` / `submit_review` | No state write on submit | Closure redirect |

---

### 2.9 Indirect / pre-study entry (not study itself)

| Route | Role | Ends at |
|---|---|---|
| `GET /` | App entry | `student.home` or `dashboard.index` |
| `GET/POST /auth/login` | Auth | Local `next` or default home |
| `GET /alpha/onboarding` (+ complete/skip) | First-run onboarding | `dashboard.index` (then sole-runtime bounce to student home if flagged) |
| Study Plan wizard → `calibration.start` → dashboard | Plan creation | `dashboard.index` |
| Sidebar "Session" (legacy) | Nav link | `mission.missions` |
| Sidebar "Home" (canonical) | Nav link | `student.home` |
| Welcome modal | First-run CTA | Links `mission.missions` (legacy-coupled) |

---

## 3. Decision-owner summary

| Decision | Owner (evidence) | Not owner |
|---|---|---|
| Which presentation stack is live | `KWALITEC_V2_SOLE_RUNTIME` / `redirect_if_sole_runtime` | Individual templates |
| Which topic is today's mission (legacy) | `PlanningService._select_topic_for_today` → `CurriculumService.get_next_incomplete_topic` | Dashboard CTA, RecommendationService |
| What recommendation card says (legacy) | `RecommendationService` (or EI when enabled) | PlanningService |
| What Home shows as next action (canonical) | Opaque Adaptive + Mission projections (`EducationalStateService`) | `PlanningService` / SQL `Mission` (not wired by default) |
| Where resume lands in canonical session | `SessionWorkspace.active_surface` | Browser URL alone |
| Mission status transitions (legacy) | `StudySessionService` / `MissionService` | Templates |

---

## 4. Critical finding (audit)

Under default V2 composition (`INJECT_PHASE_I_ENGINES=False`, no real `mission_engine`/`twin_engine`), canonical entry points (§2.1–2.3) operate on **demo-seeded opaque projections** (`seeded_demo_mission`, `seeded_demo_adaptive` in `app/infrastructure/adapters/student_experience/defaults.py`), **not** on SQL `Mission` / `PlanningService` output.

Legacy entry points (§2.4–2.8) operate on real SQL `Mission` rows generated by `PlanningService`.

When `SOLE_RUNTIME=1`, legacy entry points redirect to Home — so the student is steered into the canonical stack. Whether that Home reflects real curriculum state depends on adapter wiring (see `SOURCE_OF_TRUTH_ANALYSIS.md`).

---

## 5. Success-criteria answers (navigation)

| Question | Answer |
|---|---|
| Where every study session begins | Legacy: `POST …/session/start` or auto-start on `GET …/session`. Canonical: `POST /student/session/start` or `/student/revision/begin`, then `POST /session/<id>/begin` for activity. |
| Who owns every navigation decision | Stack choice: env flag. Topic: PlanningService (legacy) vs opaque Adaptive/Mission ports (canonical). Resume surface: SessionWorkspace. CTA routing: templates + status. |
