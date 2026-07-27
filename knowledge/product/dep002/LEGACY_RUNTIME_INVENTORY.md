# DEP-002 — Legacy Runtime Inventory

**Programme:** DEP-002  
**Definition of “Version 1 / legacy” here:** Learning Workspace presentation (`dashboard` / `mission` / `analytics` + `layouts/base.html` chrome), not Runtime A educational engines.

---

## Inventory

| Component | Still reachable? | Linked from nav? | Loaded automatically? | Dead code? | Required by admin? | Required by migration? | Safe for removal? |
|---|---|---|---|---|---|---|---|
| Blueprint `dashboard` | Redirect under sole | No (sole nav) | Registered always | No | No | No | **Not yet** — soak/rollback |
| Blueprint `mission` + LXP templates | Nested redirects | No | Registered always | No | No | No | **Not yet** |
| Blueprint `analytics` | Redirect | No (History replaces) | Registered always | No | No | No | **Not yet** |
| Template `dashboard/index.html` | Only if sole bypassed | No | No | Soft-dead under sole | No | No | After soak + DEP-003 |
| Mission session templates | Soft-dead under sole | No | No | Soft-dead under sole | No | No | After soak |
| `layouts/base.html` + `sidebar.html` | **Yes** | Via Study Plan / Help / Settings | Yes for shared pages | **No** | Console separate | No | **No** until shared pages move |
| Study Plan wizard/list/view | **Yes** | **Yes (EOS + sole sidebar)** | Login no-plan path | No | No | No | **No** — core product |
| Settings subpages | **Yes** | Indirect (EOS Settings → profile; subpages legacy) | Yes | No | Partial | No | Needs EOS restyle / merge |
| Alpha help / onboarding | **Yes** | Help in EOS nav; onboarding forced | Login / gates | No | No | No | Needs EOS chrome |
| Research check-in | **Yes** | Settings share-feedback | Optional | No | Founder reviews | No | Needs EOS chrome or gate |
| `StudySessionService` / readiness calculators | Via bridges / dual-run | N/A | Services | No | Evidence | No | **Protected** — not presentation |
| `src/web` EOS Flask app | Not via Render wsgi | No | Tests / future | Parallel codebase | No | Separate tree | Out of scope |

---

## Automatic load paths into legacy chrome (sole runtime)

1. **Login without active plan** → Study Plan wizard.  
2. **Onboarding pending** → Alpha onboarding (also from `/dashboard/` before sole redirect).  
3. **EOS nav → Study Plan / Help**.  
4. **Direct URL** to settings subpages, research, calibration.  
5. **Bookmarks** to `/dashboard/` etc. → redirect (not chrome load).

---

## Safe-removal posture (for DEP-003 planning)

- **Unsafe now:** deleting blueprints, study plan templates, or `layouts/base.html`.  
- **Candidate after chrome unification:** physical deletion of dashboard/mission/analytics templates once redirects and dual-run rollback are retired.  
- **Never confuse with:** deleting Runtime A / Mission Engine / curriculum — out of presentation scope (V2-023 protected list).
