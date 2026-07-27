# DEP-002 — Route Inventory

**Programme:** DEP-002  
**Method:** Enumerate `app.url_map` under `KWALITEC_V2_SOLE_RUNTIME=1` (+ companion V2 flags).  
**Totals:** 122 rules, 13 blueprints (plus static / health / index / founder shim).

---

## Classification legend

| Class | Meaning |
|---|---|
| **EOS** | Education OS student/session presentation |
| **Legacy** | V1 Learning Workspace educational shells |
| **Shared-legacy-chrome** | Required product surfaces that still extend `layouts/base.html` |
| **Auth** | Authentication |
| **Admin** | Founder Console / Studio |
| **Internal** | Alpha help, onboarding, telemetry, research |
| **API/Health** | Ops probes |

---

## Comparison: Legacy vs EOS coexistence under sole runtime

| Concern | Finding |
|---|---|
| Do both route trees exist in the process? | **Yes** |
| Do competing educational homes still *render*? | **No** — they redirect |
| Do other V1 routes still *render*? | **Yes** — Study Plan, Settings subpages, Help, Onboarding, Research |
| Can a student reach both chrome systems in one session? | **Yes** — via nav and login |

---

## Authenticated behaviour matrix (local, production flag matrix)

| Path | Status under sole | Destination / shell |
|---|---|---|
| `/` | 302 | `/student/` |
| `/dashboard/` | 302 | `/student/` (or `/alpha/onboarding` if onboarding pending — checked **before** sole redirect) |
| `/missions/` | 302 | `/student/` |
| `/missions/<id>/session*` / review | 302 | `/student/` |
| `/analytics/` | 302 | `/student/history` |
| `/settings/` | 302 | `/student/profile` |
| `/settings/profile` etc. | **200** | **Legacy sidebar** |
| `/student/*` | **200** | **EOS topnav** |
| `/session/<id>/*` | **200** | **EOS session shell** |
| `/study-plan/*` | **200** (wizard/list) | **Legacy sidebar** |
| `/alpha/help`, `/alpha/onboarding` | **200** | **Legacy sidebar** |

---

## Inventory by class (representative)

### Auth
- `GET|POST /auth/login` — `auth.login`
- `POST /auth/logout` — `auth.logout`

### EOS
- `GET /student/`, `/student/journey`, `/student/revision`, `/student/history`, `/student/profile`
- `POST /student/session/start`, `/student/revision/begin`, commitment posts
- `GET|POST /session/<session_id>/…` (overview, begin, activity, reflection, summary, complete)

### Legacy (registered; entry redirected under sole)
- `GET /dashboard/` (+ welcome / revision acknowledge POSTs)
- `GET /missions/` (+ nested session/finish/recorded/start, review, task toggle, complete)
- `GET /analytics/`

### Shared-legacy-chrome (live under sole)
- `/study-plan/` index, wizard steps, edit, archive, set-active, plans/all, review
- `/settings/profile|preferences|data|export|import|internal-alpha`
- `/calibration/…`
- `/alpha/help`, onboarding, feedback forms
- `/research/checkin`, thank-you, dismiss (+ founder research mirrors)

### Admin
- `/console/…` founder dashboard surfaces
- `/console/studio/…` curriculum studio
- `/founder/*` → 308 `/console/*`

### Health / internal
- `/health`, `/health/live`, `/health/ready`, `/health/details`
- `/alpha/telemetry`

Full machine listing captured during investigation (122 lines) matches `app.url_map` dump; regenerate with:

```bash
KWALITEC_V2_SOLE_RUNTIME=1 KWALITEC_V2_STUDENT_EXPERIENCE=1 \
KWALITEC_V2_DURABLE_STORE=1 KWALITEC_V2_INJECT_ENGINES=1 \
APP_ENV=testing SECRET_KEY=test-secret-key-for-testing-only-32chars \
python -c 'from app import create_app; app=create_app();
print("\n".join(sorted(f"{r.rule}\t{r.endpoint}" for r in app.url_map.iter_rules())))'
```

---

## Route comparison summary

```
Legacy educational homes ──redirect──► EOS Home / History
EOS student + session     ──render───► EOS chrome
Study Plan / Help / …     ──render───► Legacy chrome  ← dual-experience hinge
```
