# DEP-003 — Navigation Migration

**Programme:** DEP-003 — Student Experience Unification

---

## Old navigation → New navigation

### Under sole runtime (production)

```
Legacy sidebar (app-sidebar)
  Home / Journey / Revision / History / Study Plan / Settings / Help / Sign out
        ↓
EOS topnav (student-nav) — single student navigation
  Home · Journey · Revision · History · Settings · Study Plan · Help · Sign out
```

Destinations are unchanged. Only chrome ownership moved.

### Dual-run rollback (`SOLE_RUNTIME=0`)

Legacy sidebar remains for templates extending `layouts/base.html` (Learning Workspace dual-home soak). EOS Student Experience pages keep EOS topnav.

---

## Item map

| Old (legacy sidebar, sole branch) | New (EOS topnav) | Endpoint | Notes |
|---|---|---|---|
| Home | Home | `student.home` | Same |
| Journey | Journey | `student.journey` | Same |
| Revision | Revision | `student.revision` | Same |
| History | History | `student.history` | Same |
| Study Plan | Study Plan | `study_plan.index` | Same endpoint; **now EOS shell** |
| Settings | Settings | `student.profile` | Settings subpages highlight Settings via `settings.*` → Profile surface |
| Help | Help | `alpha.help_centre` | Same endpoint; **now EOS shell** |
| Sign out | Sign out | `auth.logout` | Moved from sidebar form into EOS topbar |

### Removed duplicate destinations

| Duplicate | Resolution |
|---|---|
| Sidebar + EOS both linking Study Plan / Help with different chrome | One chrome: EOS; one nav tree: `build_navigation()` |
| Dual “Dashboard” / “Home” under sole | Already removed by EP-007.1; preserved |
| Settings index vs Profile | Index still redirects to `student.profile` under sole |

### Dual-run-only items (not in sole EOS nav)

| Item | Endpoint | Status |
|---|---|---|
| Dashboard | `dashboard.index` | Dual-run sidebar only |
| Session (LXP hub) | `mission.missions` | Dual-run sidebar only; sole uses Home start |
| Analytics | `analytics.index` | Dual-run sidebar only; sole → History |
| Share Feedback | `research.checkin` | Reachable via Settings / profile CTAs; not primary EOS nav |

---

## Navigation ownership

| Concern | Owner |
|---|---|
| Canonical nav tree | `app/presentation/student/navigation.py` → `build_navigation()` / `build_navigation_for_request()` |
| Template render | `student/components/navigation.html` |
| Injection for pages without `page.shell` | Context processor `eos_navigation` in `app/__init__.py` |
| Active highlighting for Study Plan / Help / Settings | `build_navigation_for_request(request.endpoint)` |

---

## Guarantee

Every navigation action under sole runtime lands on a page that either:

1. Extends `layouts/eos_student.html` / `student/base.html`, or  
2. Extends `session/base.html` (EOS Session), or  
3. Redirects into (1)/(2), or  
4. Is Auth / logout

No primary nav item opens Version 1 sidebar chrome under sole runtime.
