# DEP-003 — Presentation Architecture

**Programme:** DEP-003 — Student Experience Unification

---

## Principle

Unify **presentation** under one Education Operating System shell. Preserve **implementation** layers (blueprints → services → models/engines).

```
Templates (EOS shell) → Blueprints (unchanged) → Services (unchanged) → Models / Curriculum Engine
```

---

## Before / after (sole runtime)

```
BEFORE
  student/*  ──► student/base.html          (EOS)
  session/*  ──► session/base.html          (EOS Session)
  study_plan / alpha / settings / …
             ──► layouts/base.html          (V1 sidebar)  ← dual-app perception

AFTER
  student/*  ──► student/base.html
                      └── layouts/eos_student.html
  session/*  ──► session/base.html          (EOS Session family)
  study_plan / alpha / settings / …
             ──► layouts/base.html
                      └── layouts/eos_student.html   (sole)
                      └── layouts/legacy_workspace.html (dual-run)
```

---

## Components

| Component | Role |
|---|---|
| `layouts/eos_student.html` | Single EOS student shell (header, nav, footer, scripts) |
| `layouts/legacy_workspace.html` | Preserved V1 Learning Workspace chrome |
| `layouts/base.html` | Flag-gated presentation router |
| `student/base.html` | Student Experience adapter (page header + reading width) |
| `session/base.html` | Focused session chrome |
| `build_navigation_for_request` | Nav for templates without `page` view-model |
| Context `eos_navigation` | Global injection for shared pages |

---

## Flag boundary

| Flag | Student presentation |
|---|---|
| `KWALITEC_V2_SOLE_RUNTIME=1` | One EOS shell for all student-facing `layouts/base` pages |
| `KWALITEC_V2_SOLE_RUNTIME=0` | Dual-run: EOS for `/student/*`; legacy chrome for shared blueprints |

Educational redirects (dashboard → home, missions → home, analytics → history) remain EP-007.1 behaviour and are orthogonal to this shell router.

---

## Layering compliance

| Layer | DEP-003 change? |
|---|---|
| Templates / CSS (presentation) | **Yes** — shell unification |
| Blueprints / routes | No |
| Services / planning / recommendations | No |
| Models / DB / Alembic | No |
| Feature flags | No deletion; sole flag **used** as chrome gate |
| Curriculum V1/V2 engines | Untouched |

---

## Rollback architecture

1. Set `KWALITEC_V2_SOLE_RUNTIME=0` (or omit).  
2. Router selects `legacy_workspace.html`.  
3. Sidebar + topnav return for Study Plan / Help / Settings.  
4. Student Experience (`/student/*`) remains EOS (pre-existing).  
5. No migration reverse required.

Physical retirement of legacy templates remains a **future** programme (DEP-002 remediation step 6) — out of DEP-003 scope.
