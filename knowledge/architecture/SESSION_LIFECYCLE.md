# MS-001 — Session Lifecycle

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)

Maps the complete study-session lifecycle for **legacy** and **canonical** stacks. Every transition lists controller, service, model, DB, session, and error handling.

---

## Overview (both stacks)

```
Student opens app
        ↓
Navigation decision          (SOLE_RUNTIME / login / onboarding)
        ↓
Session created              (legacy: Mission row + status; canonical: opaque session + SessionWorkspace)
        ↓
Mission loaded               (legacy: Mission/MissionTask; canonical: MissionPort projection)
        ↓
Recommendation loaded        (legacy: RecommendationService; canonical: AdaptiveDecisionPort)
        ↓
Study begins                 (legacy: status In Progress + session UI; canonical: begin → activity)
        ↓
Progress saved               (legacy: TopicProgress / StudyAttempt / Evidence; canonical: opaque stores + optional orchestrator)
        ↓
Session ends                 (legacy: finish + recorded; canonical: complete → home)
        ↓
Resume state stored          (legacy: Mission.status; canonical: SessionWorkspace.active_surface)
```

---

## A. Canonical lifecycle (Student + Session Experience)

### A1. Student opens app → navigation decision

| Aspect | Evidence |
|---|---|
| **Controller** | `index` root (`app/__init__.py`) or `auth.login` → redirect |
| **Service** | `resolve_v2_feature_flags()` |
| **Model / DB** | None for navigation flag |
| **Session** | Flask cookie auth via Flask-Login |
| **Errors** | Unauthenticated → login |

### A2. Home load (recommendation + today’s session projected)

| Aspect | Evidence |
|---|---|
| **Controller** | `student.home` |
| **Service** | `load_page` → `StudentExperienceService.get_dashboard` → `HomeService.home` → `EducationalStateService` |
| **Ports** | Twin, Adaptive, Mission (optional Journey) |
| **Model / DB** | Default: in-memory `ExperienceProjectionStore`. Durable: `V2AggregateDocument` JSON when `ENABLE_DURABLE_STORE` |
| **Session** | No Flask keys for study; `ExperienceRegistry` may hold handles |
| **Errors** | `PortUnavailable` / `StudentExperienceError` → empty page + flash |

**Creation of demo state:** `ensure_learner` / `seed_learner(demo=True)` writes `seeded_demo_*` documents on first view when demo seeding is enabled (`SEED_DEMO_LEARNERS` defaults True).

### A3. Session created / started (Home CTA)

| Aspect | Evidence |
|---|---|
| **Controller** | `student.start_session` |
| **Service** | `StudentExperienceService.start_session` → `ExperienceMissionAdapter.start_session` |
| **Model** | Opaque mission document (`todays_session.status = in_progress`); optional `start_opaque` if engine injected |
| **DB** | Projection store save; not SQL `missions` table by default |
| **Session** | Experience session handle in registry; events `learning_session_started`, `mission_updated` |
| **Errors** | Form invalid / port down / experience error → flash → home |

Then redirect to `session.overview`.

### A4. Mission / overview loaded

| Aspect | Evidence |
|---|---|
| **Controller** | `session.overview` |
| **Service** | `resume_redirect_if_needed`, `open_session` / `get_flow` via `SessionExperienceService` |
| **Model** | `SessionWorkspace` (`ACTIVE`, `active_surface=OVERVIEW`) |
| **DB** | `SessionDocumentStore` (memory or durable LearningSession aggregate) |
| **Errors** | Ownership → 403; missing → home |

### A5. Study begins (Begin Session)

| Aspect | Evidence |
|---|---|
| **Controller** | `session.begin` |
| **Service** | `SessionExperienceService.begin_session` → session/activity ports |
| **Model** | Workspace advances toward ACTIVITY |
| **DB** | Session document update |
| **Errors** | Port / experience errors → flash → overview |

### A6. Progress during activity

| Aspect | Evidence |
|---|---|
| **Controller** | `answer`, `advance` |
| **Service** | `submit_response`, `advance_activity` (Activity engine port) |
| **Model** | Activity projection / workspace surface |
| **DB** | Session store; Learning Orchestrator may write evidence via separate adapters when learning-loop hook runs |
| **Errors** | Flash + stay on activity |

**Important:** Default wiring does **not** call `AdaptiveLearningService.update_mastery_after_attempt` or write `TopicProgress` from this path.

### A7. Reflection → summary → complete

| Transition | Controller | Service | Errors |
|---|---|---|---|
| Continue reflection | `reflection_continue` | `continue_from_reflection` | flash → reflection |
| View summary | `summary` | completion service snapshot | resume / home |
| Finish | `finish` | `complete_session` (+ MissionPort.complete when wired) | flash → complete or home |

### A8. Resume state

| Store | What | Destroyed when |
|---|---|---|
| `SessionWorkspace.active_surface` | Resume screen | Workspace closed / process restart (unless durable) |
| Opaque `todays_session` | Mission/session ids + status | Overwritten on next start/complete; memory unless durable |
| Flask session | Not used for resume | — |
| localStorage | Not used by canonical session templates | — |

---

## B. Legacy lifecycle (Dashboard + Mission + StudySessionService)

### B1. Open app → navigation

Same root/login; without sole runtime lands on `dashboard.index` (after optional onboarding).

### B2. Mission created (idempotent on page load)

| Aspect | Evidence |
|---|---|
| **Controller** | `dashboard.index` and/or `mission.missions` |
| **Service** | `PlanningService.generate_today_mission` |
| **Model** | Creates `Mission` + `MissionTask` via `MissionService.create_mission` |
| **DB** | SQL insert; scoped to active `StudyPlan` |
| **Session** | None |
| **Errors** | No active plan / outside date window → `None` (no mission) |

Topic selection: `CurriculumService.get_next_incomplete_topic` (Learning) or revision templates (Revision lifecycle).

### B3. Recommendation loaded (parallel, independent)

| Aspect | Evidence |
|---|---|
| **Controller** | `dashboard.index` |
| **Service** | `RecommendationService.generate_today_recommendation` (unless EI orchestrator card active) |
| **Model** | Optional `Decision` journal rows if recorded |
| **DB** | Reads `TopicProgress` / readiness aggregates; does not create Mission |
| **Errors** | Timed/guarded calls; dashboard still renders |

### B4. Study begins

| Aspect | Evidence |
|---|---|
| **Controller** | `start_study_session` or auto-start in `study_session` |
| **Service** | `StudySessionService.start_session` |
| **Model** | `Mission.status`: Pending → In Progress |
| **DB** | SQL update |
| **Errors** | Ownership failures; sole runtime redirects away |

### B5. Progress saved

| Aspect | Evidence |
|---|---|
| **Controller** | Task toggle; finish POST |
| **Service** | `MissionService.mark_task_complete`; `StudySessionService.finish_session` / `record_practice_outcome` → `AdaptiveLearningService.update_mastery_after_attempt` (Evidence Authority gated) |
| **Model** | `MissionTask.completed`, `TopicProgress`, `StudyAttempt`, mistakes as applicable |
| **DB** | SQL commits |
| **Client** | `study_session.js` timer in localStorage (presentational; duration prefill only) |
| **Errors** | Validation on outcome form; service raises / flashes |

### B6. Session ends

| Aspect | Evidence |
|---|---|
| **Controller** | `finish_study_session` → `study_session_recorded` |
| **Service** | Completion semantics (Yes/Partially/No); feedback builders / explainability |
| **Model** | `Mission.status` → Completed |
| **DB** | SQL |
| **Errors** | Redirect to recorded / home under sole runtime |

### B7. Resume state

| Store | What |
|---|---|
| `Mission.status` | Pending / In Progress / Completed — **authoritative resume signal for legacy** |
| URL | Student navigates to `/missions/<id>/session` when In Progress |
| Flask | Unused for mission pointer |
| localStorage timer | Does not decide resume; only UI timer continuity |

There is **no** dedicated StudySession ORM model in `app/models/`. Lifecycle is proxied through `Mission`.

---

## C. Transition matrix (condensed)

| Lifecycle step | Legacy controller | Canonical controller | Shared? |
|---|---|---|---|
| Open app | `/`, dashboard | `/`, student.home | Flag diverges |
| Nav decision | consolidation + onboarding | consolidation | Flag |
| Session created | PlanningService + Mission | MissionPort.start_session | **No** |
| Mission loaded | MissionService | MissionPort.get_todays_session | **No** |
| Recommendation | RecommendationService | AdaptiveDecisionPort | **No** |
| Study begins | StudySessionService.start | SessionExperience.begin | **No** |
| Progress | AdaptiveLearning + Evidence | Opaque activity / orchestrator stores | **No** |
| Session ends | finish + recorded | complete → home | **No** |
| Resume stored | Mission.status | SessionWorkspace.active_surface | **No** |

---

## D. Error-handling patterns

| Layer | Pattern |
|---|---|
| Flask routes | Flash + redirect to safe surface (home / overview / activity) |
| Ownership | Legacy: query scoped to user. Canonical: `SessionOwnershipError` → 403 |
| Ports down | `PortUnavailable` → user-visible warning, empty/degraded UX |
| Dashboard | Per-service timed calls; failures degrade widgets without blocking page |
| Sole runtime | Legacy study routes short-circuit to `student.home` before legacy logic |

---

## E. Lifecycle conclusion

Two complete lifecycles exist. They share **authentication**, **Study Plan / calibration onboarding**, and **curriculum SQL** (legacy only for daily selection). They do **not** share session identity, resume storage, or progress write paths under default V2 wiring.
