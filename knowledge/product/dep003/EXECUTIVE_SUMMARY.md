# DEP-003 — Executive Summary

**Programme:** DEP-003 — Student Experience Unification  
**Date:** 2026-07-27  
**Mode:** Implementation (presentation only)  
**Predecessor:** DEP-002 (root cause H — legacy runtime preserved but never hidden)

---

## Verdict

Students under `KWALITEC_V2_SOLE_RUNTIME=1` now experience **one** Education Operating System shell from login through Study Plan, Help, Settings, Session, and logout.

Legacy controllers, blueprints, routes, services, feature flags, and rollback capability remain intact. Only the outer presentation shell changed.

---

## What changed

| Before (DEP-002) | After (DEP-003) |
|---|---|
| EOS Home + Session use `student/` / `session/` chrome | Unchanged (still EOS) |
| Study Plan / Help / Onboarding / Settings use V1 sidebar | Same templates extend EOS shell under sole runtime |
| Login → Study Plan wizard felt like a second app | Wizard renders inside EOS topnav + footer |
| Sign out only in legacy sidebar | Sign out on EOS topbar for all EOS student pages |

**Mechanism:** `layouts/base.html` is a presentation router:

- Sole runtime → `layouts/eos_student.html`
- Dual-run / rollback → `layouts/legacy_workspace.html`

`student/base.html` now extends the same shared EOS layout (Goal 6 — single student shell).

---

## What did **not** change

- No blueprints, routes, controllers, or services deleted
- No study-plan / onboarding / recommendation / persistence rewrites
- No migrations or schema changes
- No feature-flag removals
- Dashboard / mission / analytics still redirect under sole (EP-007.1)
- Session flow keeps focused `session/base.html` (EOS family, linear progress — not a second product)

---

## Success criteria status

| Criterion | Status |
|---|---|
| One shell for student-facing pages under sole | **Met** |
| One navigation (EOS topnav) | **Met** |
| One visual identity | **Met** |
| Legacy implementation available internally / dual-run | **Met** |
| Rollback via `SOLE_RUNTIME=0` | **Met** |
| No business-logic / migration changes | **Met** |

---

## Rollback

Unset or set `KWALITEC_V2_SOLE_RUNTIME=0`. Shared pages again render `layouts/legacy_workspace.html` (sidebar + topnav). No deploy of alternate code required beyond flag/config.
