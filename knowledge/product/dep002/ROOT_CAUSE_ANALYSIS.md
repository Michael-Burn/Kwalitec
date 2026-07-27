# DEP-002 — Root Cause Analysis

**Programme:** DEP-002  
**Date:** 2026-07-27  
**Standard:** Exactly **one** primary root cause, evidence-backed.

---

## Primary root cause

### **H — Legacy runtime intentionally preserved but never hidden**

Stage 1 sole runtime retires **competing educational entry points** by redirect. It does **not** retire the Version 1 application shell, unregister legacy blueprints, or re-home shared product surfaces (Study Plan, Help, Onboarding, Settings subpages) into the EOS chrome. EOS navigation and the no-plan login path **actively surface** that preserved legacy shell. Production therefore exhibits two application experiences in one deploy — by architecture, not by failed deploy.

Supporting design citations:

- `app/presentation/consolidation.py`: “READY FOR MIGRATION shells stay registered but send learners to the canonical Student Experience…”
- `docs/architecture/V2_023_RELEASE_CANDIDATE.md`: keep legacy redirect shells for soak; engines/templates not deleted
- `knowledge/architecture/NAVIGATION_AUDIT.md`: shared infrastructure (`study_plan`, `alpha`, `settings`, …) not sole-runtime-gated

---

## Evidence chain

| # | Claim | Evidence |
|---|---|---|
| 1 | Correct commit on Render | `/health` `commit=353f4b2…` = `origin/main` |
| 2 | Sole flag active | `GET /` → `302 Location: /student/` |
| 3 | Not a second Flask process | `wsgi.py` → `app.create_app`; waitress |
| 4 | Legacy + EOS blueprints always registered | `_register_blueprints` unconditional; 13 BPs |
| 5 | Competing homes redirect | Local + code: dashboard/missions/analytics/nested LXP |
| 6 | Shared V1 pages still render | Study Plan wizard/list, settings subpages, help, onboarding → `layouts/base.html` |
| 7 | EOS nav links into V1 | `SYSTEM_NAV_ITEMS` → `study_plan.index`, `alpha.help_centre` |
| 8 | Login can open V1 first | No-plan → `/study-plan/wizard/1` (legacy shell) before EOS Home |
| 9 | Dual chrome in one session | Local probe: `/student/` = EOS_TOPNAV; `/study-plan/*` = LEGACY_SIDEBAR |

---

## Hypothesis board (all evaluated)

| ID | Hypothesis | Verdict |
|---|---|---|
| A | Legacy blueprint still registered | **Contributing mechanism** — true, intentional; subsumed by H |
| B | Feature flag not enforced | **Falsified** |
| C | Navigation exposes legacy routes | **Contributing mechanism** — true for Study Plan/Help; subsumed by H |
| D | Template inheritance mixes runtimes | **Contributing mechanism** — session-level shell mix; subsumed by H |
| E | Render deployed incorrect commit | **Falsified** |
| F | Configuration drift | **Falsified** (behavioural) |
| G | Authentication redirect enters legacy runtime | **Contributing symptom** when no plan / onboarding; not universal |
| **H** | **Legacy intentionally preserved but never hidden** | **PRIMARY** |

---

## Issue category for remediation scoping

| Category | Applies? |
|---|---|
| Deployment | No |
| Configuration | No (flag correct) |
| Routing | Partial (redirects work; shared routes still live) |
| Templates | Yes (two shell families) |
| Feature flags | Scope too narrow vs founder expectation |
| **Retained legacy architecture** | **Yes — primary** |

---

## Founder reproduction (deployed app + flag-matched local)

### A. Deployed application only (unauthenticated — credentials not available to investigator)

| Step | Observation |
|---|---|
| Landing | `GET /` → `/student/` → `/auth/login?next=/student/` |
| Registration | **Not publicly exposed** (invite-only Internal Alpha copy on login) |
| Login page | Brand **Kwalitec**, descriptor **Education Operating System**, Internal Alpha / Founding Cohort / Build RC2, footer `Kwalitec v2.0.0` |
| Health | commit `353f4b2`, env `production`, migrations current |
| Protected paths | `/dashboard/`, `/student/`, `/missions/`, `/analytics/`, `/study-plan/` all 302 to login with `next=` |

Authenticated founder steps on live Render were **not** executable without credentials. No assumptions filled in.

### B. Flag-matched authenticated simulation (local = production env matrix)

| Step | Observation |
|---|---|
| Login (no plan) | → `/study-plan/wizard/1` **legacy sidebar** |
| Complete / reach home | `/student/` **EOS topnav** |
| Nav → Study Plan | **legacy sidebar** again |
| Nav → Help | **legacy sidebar** |
| `/dashboard/`, `/missions/` | 302 → `/student/` |
| Logout | → `/auth/login` |

**Transition points (evidence):**  
1. Login → Study Plan wizard (legacy).  
2. Study Plan / Help ↔ Student Home (legacy ↔ EOS).  
3. Not at deploy boundary; not at flag miss.

---

## Why this matches the founder report

“EOS layered on top of the previous application instead of completely replacing it” is an accurate description of V2-023 sole runtime: EOS is the **canonical educational home**, while the previous Learning Workspace shell remains the **shared-application chassis** for planning, help, and several settings flows.
