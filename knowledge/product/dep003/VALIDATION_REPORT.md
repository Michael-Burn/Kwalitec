# DEP-003 — Validation Report

**Programme:** DEP-003 — Student Experience Unification  
**Date:** 2026-07-27

---

## Acceptance criteria validation

| Criterion | Method | Result |
|---|---|---|
| Register → … (registration not public) | N/A — product constraint | N/A |
| Login without leaving EOS identity | Auth landing → sole student pages in EOS shell | **Pass** |
| Create Study Plan in EOS | `/study-plan/wizard/1` under sole → `student-shell`, no `app-sidebar` | **Pass** |
| Complete Onboarding in EOS | `/alpha/onboarding` under sole → EOS shell | **Pass** |
| Access Missions / Sessions | Sole redirects LXP hub; session via `/session/*` EOS Session | **Pass** |
| View Journey / History / Help / Settings | EOS shell assertions | **Pass** |
| Logout | EOS topbar Sign out present on sole student pages | **Pass** |
| One shell / nav / identity | Layout router + nav injection | **Pass** |
| Legacy available internally | Dual-run test keeps sidebar | **Pass** |
| Rollback intact | `SOLE_RUNTIME=0` path | **Pass** |
| No business logic / migrations / blueprint removal | Diff review + blueprint test | **Pass** |

---

## Automated validation suite

`tests/presentation/test_dep003_unification.py`:

- Parametrized sole-runtime shell checks for Home, Study Plan, wizard, Help, Onboarding, Settings  
- Wizard form retention  
- Help search retention  
- Dual-run legacy chrome preservation  
- Layout router / shared shell file contracts  
- Blueprint presence guard  

Supporting:

- `tests/presentation/student/test_navigation.py` — request-scoped active states  
- Canonical journey / dual-run / brand / theme / a11y suites (see `REGRESSION_REPORT.md`)

---

## Manual founder dogfood checklist (recommended soak)

1. Production flags locally: `KWALITEC_V2_SOLE_RUNTIME=1` (+ companion V2 flags as in `render.yaml`).  
2. Log in as a user **without** a study plan → confirm wizard is EOS topnav, not sidebar.  
3. Complete wizard → land on Home still in EOS.  
4. Click Study Plan, Help, Settings subpages → no sidebar flash.  
5. Start session from Home → session chrome → complete → Home.  
6. Sign out from topbar.  
7. Flip `SOLE_RUNTIME=0` → Study Plan shows sidebar again (rollback proof).

---

## Production deployability

Every commit remains deployable: router is additive; dual-run default in tests; production already sets sole runtime. No migration step required at deploy time.
