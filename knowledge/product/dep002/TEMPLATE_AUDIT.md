# DEP-002 — Template Audit

**Programme:** DEP-002  
**Tree:** `app/templates/` (84 HTML files at investigation time)

---

## Shell families still in the repo (and on production disk)

| Family | Base template | CSS | Used by |
|---|---|---|---|
| **Legacy Learning Workspace** | `layouts/base.html` | `css/app.css` + sidebar | Dashboard*, missions*, analytics*, study plan, settings pages, alpha, research |
| **EOS Student** | `student/base.html` | `css/student/student.css` | `student/*.html` |
| **EOS Session** | `session/base.html` | student CSS family | `session/*.html` |
| **Auth landing** | `layouts/auth_base.html` | brand/landing | `auth/login.html` |
| **Founder Console** | `layouts/console_base.html` | console | `/console/*` |

\*Dashboard / mission / analytics **templates remain on disk** but entry routes redirect under sole runtime (soak / rollback).

---

## Dashboard / student / mission / EOS templates

### Dashboard (legacy)
- `dashboard/index.html` — retained; not rendered when sole + authenticated past onboarding

### Student (EOS)
- `student/home.html`, `journey.html`, `revision.html`, `history.html`, `profile.html`
- Components under `student/components/`

### Mission / LXP (legacy)
- `mission/index.html`, `session.html`, `session_recorded.html`, `session_practice_outcome.html`
- Entry + nested routes redirect under sole; templates retained

### Session Experience (EOS)
- `session/overview.html`, `activity.html`, `reflection.html`, `summary.html`, `complete.html` + components

### Study Plan (legacy chrome, **still rendered**)
- Wizard steps, `list.html`, `view.html`, `edit.html`, `review.html` — all extend `layouts/base.html` / `wizard_base.html`

---

## Which templates are actually rendered under sole runtime?

| Still reachable (200) | Shell |
|---|---|
| `student/*`, `session/*` | EOS |
| `study_plan/*` (wizard, list, view, …) | Legacy |
| `settings/profile|preferences|data|…` | Legacy |
| `alpha/help`, `alpha/onboarding`, feedback | Legacy |
| `research/checkin` (+ thank you) | Legacy |
| `auth/login` | Auth landing |
| `calibration/*` | Legacy / calibration |

| Retained but redirected at entry | Notes |
|---|---|
| `dashboard/index.html` | Redirect unless onboarding short-circuits first |
| `mission/*` session templates | Nested routes redirect to student home |
| `analytics/index.html` | Redirect to student history |

---

## Mixing / inheritance issue

There is **no single template that extends both bases**. The mix is **session-level**:

1. User views EOS Home (`student/base.html`).  
2. Clicks Study Plan (EOS nav).  
3. Renders Study Plan wizard/list (`layouts/base.html` + sole-flavoured sidebar).  

Visual language, layout density, and chrome change abruptly — perceived as “two applications.”

Hard-coded legacy CTAs still exist in some retained templates (e.g. mission recorded → `dashboard.index`, thank-you → `dashboard.index`). Under sole those targets redirect, but the copy/links reveal V1 heritage.

---

## Production login template check

Live login HTML includes `landing-brand-name` + “Education Operating System” descriptor — matches **committed** `HEAD` template. Local uncommitted edit removing the brand-name line is **not** deployed.
