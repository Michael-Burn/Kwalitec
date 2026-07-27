# DEP-003 — Student Route Matrix

**Programme:** DEP-003 — Student Experience Unification  
**Flag posture:** `KWALITEC_V2_SOLE_RUNTIME=1` (production / sole)  
**Legend — Final Layout:**

| Value | Meaning |
|---|---|
| **EOS Student** | `layouts/eos_student.html` (via `student/base` or sole `layouts/base` router) |
| **EOS Session** | `session/base.html` (focused session chrome; EOS family) |
| **Auth** | `layouts/auth_base.html` |
| **Redirect** | Entry redirects to EOS; template retained for rollback |
| **Admin** | Founder Console / Studio (`layouts/console_base.html`) — out of student scope |
| **Legacy (dual-run only)** | `layouts/legacy_workspace.html` when `SOLE_RUNTIME=0` |

---

## Required student journey

| Route | Controller | Current Layout (pre-DEP-003) | Final Layout (sole) | Status |
|---|---|---|---|---|
| `GET\|POST /auth/login` | `auth.login` | Auth | Auth | Pass — brand landing unchanged |
| `POST /auth/logout` | `auth.logout` | N/A (action) | N/A — EOS topbar Sign out | Pass |
| `GET /` | `index` | Redirect → `/student/` | Redirect → EOS Home | Pass |
| `GET /student/` | `student.home` | EOS Student | EOS Student | Pass |
| `GET /alpha/onboarding` | `alpha.onboarding` | Legacy sidebar | **EOS Student** | Pass |
| `POST /alpha/onboarding/complete` | `alpha.onboarding_complete` | N/A | Redirect (unchanged logic) | Pass |
| `POST /alpha/onboarding/skip` | `alpha.onboarding_skip` | N/A | Redirect (unchanged logic) | Pass |
| `GET /study-plan/` | `study_plan.index` | Legacy sidebar | **EOS Student** | Pass |
| `GET\|POST /study-plan/wizard/<step>` | `study_plan.wizard_step` | Legacy sidebar | **EOS Student** | Pass |
| `GET /study-plan/review` | `study_plan.review` | Legacy sidebar | **EOS Student** | Pass |
| `GET /study-plan/<id>` | `study_plan.view_plan` | Legacy sidebar | **EOS Student** | Pass |
| `GET\|POST /study-plan/<id>/edit` | `study_plan.edit_plan` | Legacy sidebar | **EOS Student** | Pass |
| `GET /student/journey` | `student.journey` | EOS Student | EOS Student | Pass |
| `GET /student/revision` | `student.revision` | EOS Student | EOS Student | Pass |
| `POST /student/revision/begin` | `student.begin_revision` | N/A | Unchanged | Pass |
| `POST /student/session/start` | `student.start_session` | N/A | Starts EOS Session | Pass |
| `GET /session/<id>/…` | `session.*` | EOS Session | EOS Session | Pass |
| `GET /student/history` | `student.history` | EOS Student | EOS Student | Pass |
| `GET /alpha/help` | `alpha.help_centre` | Legacy sidebar | **EOS Student** | Pass |
| `GET /student/profile` | `student.profile` | EOS Student | EOS Student | Pass |
| `GET /settings/profile` etc. | `settings.*` | Legacy sidebar | **EOS Student** | Pass |
| `GET /settings/` | `settings.index` | Redirect → profile | Redirect → EOS Profile | Pass |

---

## Shared / secondary student surfaces

| Route | Controller | Current Layout | Final Layout (sole) | Status |
|---|---|---|---|---|
| `GET /study-plan/plans/all` | `study_plan.list_plans` | Legacy | EOS Student | Pass |
| `POST /study-plan/<id>/archive\|delete\|set-active` | `study_plan.*` | N/A | Unchanged actions | Pass |
| `GET /calibration/…` | `calibration.*` | Legacy (wizard_base) | EOS Student | Pass |
| `GET\|POST /research/checkin` | `research.checkin` | Legacy | EOS Student | Pass |
| `GET /research/thank-you` | `research.thank_you` | Legacy | EOS Student | Pass |
| `GET\|POST /alpha/feedback/*` | `alpha.feedback_*` | Legacy | EOS Student | Pass |
| `POST /student/commitment/*` | `student.*` | N/A | Unchanged | Pass |

---

## Legacy educational homes (retained, redirected under sole)

| Route | Controller | Current Layout | Final Layout (sole) | Status |
|---|---|---|---|---|
| `GET /dashboard/` | `dashboard.index` | Legacy (if rendered) | **Redirect** → `/student/` | Pass — no student chrome mix |
| `GET /missions/…` | `mission.*` | Legacy | **Redirect** → `/student/` | Pass |
| `GET /analytics/` | `analytics.index` | Legacy | **Redirect** → `/student/history` | Pass |

Under dual-run (`SOLE_RUNTIME=0`), these still render **Legacy** chrome — intentional rollback.

---

## Out of student scope (unchanged)

| Route prefix | Controller family | Final Layout | Notes |
|---|---|---|---|
| `/console/…` | `founder_dashboard.*`, `curriculum_studio.*` | Admin | Console chrome only |
| `/founder/…` | shim | 308 → `/console/` | Bookmark preservation |
| `/health*` | app | JSON | Ops |
| `/research/founder*` | research founder | Legacy / admin tooling | Not student journey |

---

## Shell transition check (acceptance)

| Transition | Pre-DEP-003 | Post-DEP-003 |
|---|---|---|
| Login → Home (has plan) | Auth → EOS | Auth → EOS |
| Login → Study Plan wizard (no plan) | Auth → **Legacy** | Auth → **EOS** |
| EOS Home → Study Plan nav | EOS → **Legacy** | EOS → **EOS** |
| EOS Home → Help | EOS → **Legacy** | EOS → **EOS** |
| Home → Session | EOS → EOS Session | Unchanged |
| Session → Home | EOS Session → EOS | Unchanged |

There is no remaining student journey step that paints Version 1 sidebar chrome under sole runtime.
