# DEP-002 — Blueprint Audit

**Programme:** DEP-002  
**Evidence:** `create_app()` → `_register_blueprints()` in `app/__init__.py` under production flag matrix  
**Fact:** Blueprint registration does **not** branch on `KWALITEC_V2_SOLE_RUNTIME`.

---

## Complete registered blueprints

Observed via Flask `app.blueprints` with sole-runtime env set:

| Blueprint | `url_prefix` | Module | Classification |
|---|---|---|---|
| `auth` | `/auth` | `app.auth.routes` | Authentication |
| `dashboard` | `/dashboard` | `app.dashboard.routes` | **Legacy** student shell (redirect under sole) |
| `mission` | `/missions` | `app.mission.routes` | **Legacy** session/LXP (redirect under sole) |
| `analytics` | `/analytics` | `app.analytics.routes` | **Legacy** analytics (redirect under sole) |
| `settings` | `/settings` | `app.settings.routes` | Shared / mostly **legacy shell** (index redirects; subpages live) |
| `study_plan` | `/study-plan` | `app.study_plan.routes` | Shared / **legacy shell** (live under sole) |
| `calibration` | `/calibration` | `app.calibration` | Shared / onboarding-adjacent |
| `alpha` | `/alpha` | `app.alpha` | Internal Alpha (help, onboarding, feedback) — **legacy shell** |
| `research` | `/research` | `app.research` | Research check-in — **legacy shell** |
| `founder_dashboard` | `/console` | `app.founder.dashboard` | Admin / Founder Console |
| `curriculum_studio` | `/console/studio` | `app.presentation.curriculum_studio` | Admin curriculum studio |
| `student` | `/student` | `app.presentation.student` | **EOS** Student Experience |
| `session` | `/session` | `app.presentation.session` | **EOS** Session Experience |

**Total:** 13 blueprints. App-level routes also register `/`, `/founder/*` shim, and `/health*`.

---

## Sole-runtime behaviour

From `app/presentation/consolidation.py` and route guards:

| Blueprint | Still registered when `SOLE_RUNTIME=1`? | Student-visible under sole? |
|---|---|---|
| `student`, `session` | Yes | **Yes** — canonical journey |
| `dashboard`, `mission`, `analytics` | Yes | Entry routes **redirect**; templates retained for rollback |
| `study_plan`, `alpha`, `research`, settings subpages | Yes | **Yes** — full V1 chrome |
| `founder_dashboard`, `curriculum_studio` | Yes | Admin-only |
| `auth` | Yes | Login / logout |

Documented intent (V2-023 RC): *“Keep legacy redirect shells for one soak window before physical template deletion.”* Blueprints were never unregistered.

---

## Non-production Education OS app (orthogonal)

`src/web/app.py` defines a **separate** Flask factory (`register_blueprints` → `health`, `learning`, `dashboard` under `src/`). Production `wsgi.py` does **not** call it. Treat as library / future EOS composition, not the live Render process.

---

## Implication for dual experience

Legacy blueprints remaining registered is **necessary** for redirects and rollback, and is **sufficient** to keep V1 code paths loadable. Combined with shared surfaces that still **render** V1 templates, registration alone explains coexistence; redirects alone do not eliminate the second UI chrome.
