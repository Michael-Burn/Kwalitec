# DEP-002 — Navigation Audit

**Programme:** DEP-002  
**Sources:** `app/templates/partials/sidebar.html`, `app/presentation/student/navigation.py`, `app/templates/student/components/navigation.html`, `app/templates/partials/topnav.html`

---

## Two chrome systems

| Chrome | Template / builder | When shown |
|---|---|---|
| **EOS topnav** | `student/base.html` + `student/components/navigation.html` fed by `build_navigation()` | `/student/*`, `/session/*` |
| **Legacy sidebar** | `layouts/base.html` → `partials/sidebar.html` (+ `topnav.html`) | Study Plan, Help, Onboarding, Settings subpages, Research, any V1 page that still renders |

Under sole runtime, `sidebar.html` switches its **link targets** to the EOS tree (Home · Journey · Revision · History · Study Plan · Settings · Help) — but the **visual shell** remains the V1 sidebar layout whenever a V1 template renders.

---

## EOS navigation destinations

From `SYSTEM_NAV_ITEMS` + canonical surfaces (`navigation.py`):

| Label | Endpoint | Runtime class |
|---|---|---|
| Home | `student.home` | EOS |
| Journey | `student.journey` | EOS |
| Revision | `student.revision` | EOS |
| History | `student.history` | EOS |
| Settings (profile surface) | `student.profile` | EOS |
| **Study Plan** | **`study_plan.index`** | **Legacy chrome** |
| **Help** | **`alpha.help_centre`** | **Legacy chrome** |

**Finding:** EOS primary navigation **deliberately** deep-links into legacy-shell blueprints. A student who never types a legacy URL still leaves the EOS shell when opening Study Plan or Help.

---

## Legacy sidebar under sole runtime

Sole branch of `sidebar.html` mirrors the EOS destinations (including Study Plan → `study_plan.index`). Dual-run branch still exposes Dashboard · Study Plan · Session · Analytics · Settings · Share Feedback · Help.

Production (`SOLE_RUNTIME=1`) should only ever *template* the sole branch — but that branch still lives inside the legacy `app-shell` / `app-sidebar` markup.

---

## Multiple dashboards via navigation?

| Question | Answer |
|---|---|
| Can nav show two separate “Dashboard” products at once? | **No** under sole — EOS “Home” replaces Dashboard label in sole sidebar |
| Can the user reach two different home shells in one session? | **Yes** — EOS Home (`student/base`) vs any shared page that uses `layouts/base` (Study Plan list shows Learning Workspace labelling) |
| Are `/dashboard/` and `/missions/` linked from sole nav? | **No** (sole tree). Still reachable by URL / bookmarks until redirected |

---

## Login → first chrome

`app/auth/routes.py` after successful login:

1. Onboarding if required → `/alpha/onboarding` (**legacy shell**)  
2. Else if no active study plan → `/study-plan/wizard/1` (**legacy shell**)  
3. Else → `canonical_home_url()` → `/student/` (**EOS shell**)

**Evidence (local, production flags):** user with onboarding complete and no plan → `LOGIN 302 /study-plan/wizard/1` → `shell: LEGACY`. Subsequent `/student/` → `EOS_TOPNAV`.

This is the sharpest founder-visible transition: **first authenticated screen can be V1**, then EOS appears after plan creation / navigation to Home.

---

## Other nav surfaces

- `partials/topnav.html` — email + appearance only; no dual product links.  
- Session flow uses `session/base.html` (EOS family), not the sidebar.  
- Founder Console uses `layouts/console_base.html` (admin; out of student scope).
