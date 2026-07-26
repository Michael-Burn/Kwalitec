# MS-001 — Navigation Graph

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)  
**Companion:** `NAVIGATION_AUDIT.md`

---

## 1. Legend

```
[Node]     = route / surface
-->        = navigation / redirect
--|G|-->   = guarded transition (auth / ownership / form / flag)
{state}    = required state for the edge
```

---

## 2. Global entry and stack selection

```
                    ┌─────────────┐
                    │  GET /      │
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │ SOLE_RUNTIME?           │
              └────────────┬────────────┘
                 yes │           │ no
                     ▼           ▼
            [student.home]  [dashboard.index]
                                 │
                    {onboarding pending?}
                           │ yes
                           ▼
                    [alpha.onboarding]
                           │ complete/skip
                           ▼
                    [dashboard.index]
```

**Guards on `/`:** authenticated users typically arrive after login; unauthenticated users hit Flask-Login redirect to `auth.login`.

**Required state for student surfaces:** logged-in user (`@login_required`).

---

## 3. Canonical Education OS graph

```
┌──────────────────────────────────────────────────────────────────┐
│ Student Experience                                               │
│                                                                  │
│  [student.home] ──GET──► render home.html                        │
│       │                                                          │
│       │ POST /student/session/start  {form valid, MissionPort OK}│
│       ▼                                                          │
│  [session.overview] ◄── resume_redirect_if_needed                │
│       │                  {SessionWorkspace.active_surface}       │
│       │ POST /begin                                              │
│       ▼                                                          │
│  [session.activity] ◄── answer / advance loops                   │
│       │                  {no next activity}                      │
│       ▼                                                          │
│  [session.reflection] ──POST continue──► [session.summary]       │
│                                              │                   │
│                                              ▼                   │
│                                         [session.complete]       │
│                                              │ POST finish       │
│                                              ▼                   │
│                                         [student.home]           │
│                                                                  │
│  [student.revision] ──POST /revision/begin──► [session.overview] │
│  [student.journey]   (read-only projection)                      │
│  [student.history]   (read-only projection)                      │
│  [student.profile]   (read-only projection)                      │
└──────────────────────────────────────────────────────────────────┘

Sidebar (SOLE_RUNTIME):
  Home → Journey → Revision → Analytics(=history) → Study Plan → Help
  (+ Profile via student nav endpoints)
```

### Canonical route table

| Route | Destination | Guards | Redirects | Required state |
|---|---|---|---|---|
| `GET /student/` | Home | login | — | user |
| `GET /student/journey` | Journey | login | — | user |
| `GET /student/revision` | Revision | login | — | user |
| `GET /student/history` | History | login | — | user |
| `GET /student/profile` | Profile | login | — | user |
| `POST /student/session/start` | Session overview | login, CSRF form | home on failure | MissionPort available; prefer mission/session ids from Home |
| `POST /student/revision/begin` | Session overview | login, form | revision/home on failure | same |
| `GET /session/<id>/overview` | Overview or active surface | login, ownership | missing → home; mismatch surface → active | workspace (opened if missing) |
| `POST /session/<id>/begin` | Activity | login, ownership, form | overview on failure | open workspace |
| `GET /session/<id>/activity` | Activity or resume | login, ownership | resume / home | active_surface == activity |
| `POST …/answer` | Activity | login, ownership, form | activity on failure | in activity |
| `POST …/advance` | Activity or Reflection | login, ownership, form | activity on failure | in activity |
| `GET …/reflection` | Reflection or resume | login, ownership | resume / home | — |
| `POST …/reflection/continue` | Summary | login, ownership, form | reflection on failure | — |
| `GET …/summary` | Summary or resume | login, ownership | resume / home | — |
| `GET …/complete` | Complete or resume | login, ownership | resume / home | — |
| `POST …/complete` | Student home | login, ownership, form | complete/home on failure | — |

**Resume rule:** if `surface_index(requested) != surface_index(workspace.active_surface)`, redirect to `SURFACE_ENDPOINTS[active]` (`app/presentation/session/navigation.py`).

---

## 4. Legacy study graph

```
[dashboard.index]
    │ CTA (status-based label)
    ▼
[mission.missions] ──SOLE_RUNTIME──► [student.home]
    │
    ├─ status Pending ──POST start──► [mission.study_session]
    ├─ status In Progress ──GET───► [mission.study_session]
    └─ status Completed ──GET────► [mission.study_session_recorded]
                                        ▲
[mission.study_session]                 │
    │ POST/GET finish                   │
    ▼                                   │
[mission.session/finish] ──► practice outcome ──► recorded
    │
    └─ complete_mission / review_* ──► same closure paths
```

### Legacy route table (study-relevant)

| Route | Destination | Guards | Redirects | Required state |
|---|---|---|---|---|
| `GET /dashboard/` | Dashboard HTML | login | onboarding; sole → student.home | — |
| `GET /missions/` | Mission hub | login | sole → student.home | active plan preferred for generation |
| `POST /missions/<id>/session/start` | Study session | login, ownership | sole → home | mission owned; Pending→In Progress |
| `GET /missions/<id>/session` | Session UI | login, ownership | Completed→recorded; sole→home | owned mission |
| `GET/POST …/session/finish` | Outcome / recorded | login, ownership | sole→home | In Progress / completion rules |
| `GET …/session/recorded` | Feedback | login, ownership | sole→home | Completed preferred |
| `POST /missions/tasks/<id>/toggle` | JSON | login | — | owned task |
| `GET /analytics/` | Analytics | login | sole → student.history | — |

---

## 5. Study Plan → Calibration → Home (shared)

```
[study_plan.index]
  ├─ has active plan → [study_plan.view]
  └─ else → wizard step 1 … 7 → review → create plan
                                              │
                                              ▼
                                    [calibration.start]
                                              │ submit / skip / abandon
                                              ▼
                                    [dashboard.index]
                                              │ SOLE_RUNTIME
                                              ▼
                                    [student.home]   (double-hop)
```

**Note:** Calibration always targets `dashboard.index`. Under sole runtime this becomes an indirect hop to Student Home — not a direct `student.home` redirect in calibration code.

---

## 6. Auth and ancillary edges

| From | To | Guard | Notes |
|---|---|---|---|
| Unauthenticated any protected | `auth.login` | Flask-Login | `next` must be local |
| Login success | `next` or default home | — | Open-redirect rejected |
| Welcome modal | `mission.missions` | — | Legacy-coupled; stale under sole runtime until retargeted |
| Settings / Help / Research | own blueprints | login | Do not start study sessions |

---

## 7. Competing “next” destinations

A student asking “where do I study?” may be sent to:

1. **Legacy Mission hub** (`/missions/`) — real SQL mission  
2. **Canonical Home CTA** → **Session Overview** — opaque session id  
3. **Recommendation card** (legacy dashboard) — advisory only; does not start a session by itself  
4. **Revision surface** — begins via same session-start path as Home  

There is **no single graph node** that owns “begin study” across both stacks. Sole runtime collapses presentation entry to Home, but does not by itself unify the underlying session stores (see `SOURCE_OF_TRUTH_ANALYSIS.md`).
