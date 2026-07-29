# UX-001 — Founder Experience & Role Routing Report

**Programme:** Product Experience  
**Status:** Complete  
**Date:** 2026-07-29  
**Scope:** Correct Founder-first post-login routing only — no UI redesign  

---

## Current behaviour

Before this programme:

| Path | Behaviour |
|------|-----------|
| Post-login (`POST /auth/login`) | Called `is_founder_user(user)`; on True → `/console/`, else Student onboarding / study-plan wizard / `/student/` |
| Root (`GET /`) | `redirect_to_canonical_home()` — Console when `is_founder_user()`, else Student Home under sole runtime |
| Already authenticated `GET /auth/login` | Same canonical home redirect |
| Founder OS → Student OS | No obvious chrome entry; operators had to type `/student/` or use bookmarks |

**Observed defect:** Accounts holding **Administrator** (or Administrator + Student) **without** durable Founder role **and** without `UserCapability(console)` rows were classified as non-Console users. Login and `/` therefore sent them into the Student Operating System.

Fully bootstrapped Founder/Admin accounts (`IdentityService.ensure_founder_admin` / `ADMIN_EMAIL` allowlist sync) already landed on `/console/` (confirmed in DP-004R). The gap was role-permission detection for Administrator without capability rows, plus missing deliberate Student OS entry from Console.

---

## Root cause

`is_founder_user()` required either:

1. Durable `founder` role, or  
2. Durable `console` **capability** *and* `console.access` permission, or  
3. Legacy `ADMIN_EMAIL` / `FOUNDER_EMAILS` allowlist  

`console.access` is granted by the role → permission matrix for `administrator` (and other staff roles). Capability rows are a separate store. An Administrator with a correct `user_roles` row but no `user_capabilities` row failed check (2), was not on the allowlist, and was treated as a student for landing.

That contradicts the intended product architecture: Founder / Administrator Console operators enter Founder OS first; Student OS is secondary (dogfood).

---

## Files modified

| Path | Change |
|------|--------|
| `app/founder/dashboard/access.py` | Treat Founder role, Administrator role, and `console.access` permission as Console access (capability row no longer required for landing) |
| `app/presentation/consolidation.py` | Document UX-001 role-aware landing (Founder/Admin → Console; dual-role still Console-first) |
| `app/founder/dashboard/templates/founder_dashboard/_sidebar.html` | Add **Enter Student Experience** link to Student Home |
| `tests/presentation/test_ux001_founder_routing.py` | Role-matrix login + home + entry-point tests (**new**) |

Application learning engines, Student OS chrome, and Console visual design were not redesigned.

---

## Routing logic

```text
POST /auth/login (success)
        │
        ├─ is_founder_user(user)?  ──yes──►  safe next OR /console/
        │         (Founder / Administrator / console.access / allowlist)
        │
        ├─ Alpha onboarding required? ──yes──► /alpha/onboarding
        │
        ├─ No active study plan and no Runtime C enrolment?
        │         ──yes──► study-plan wizard
        │
        └─ else ──► safe next OR canonical student home (/student/ under sole runtime)

GET /  and  GET /auth/login (already authenticated)
        │
        └─ canonical_home_endpoint()
                  ├─ is_founder_user() → founder_dashboard.index  (/console/)
                  ├─ sole runtime     → student.home             (/student/)
                  └─ dual-run         → dashboard.index
```

Safe `?next=` remains allowed for same-origin deep links (e.g. returning to a bookmarked `/student/` URL after re-auth). Default landing without `next` is Console for operators.

---

## Role matrix

| Identity | Post-login default | `/console/` | Student OS via chrome |
|----------|-------------------|-------------|------------------------|
| **Founder** | `/console/` | Yes | **Enter Student Experience** |
| **Administrator** | `/console/` | Yes | **Enter Student Experience** |
| **Student** | Student OS (`/student/` / onboarding / wizard as applicable) | 403 | N/A (already there) |
| **Founder + Student** | `/console/` | Yes | **Enter Student Experience** → `/student/` |
| **Administrator + Student** | `/console/` | Yes | **Enter Student Experience** → `/student/` |

Console remains the primary surface for dual-role Internal Alpha dogfood accounts. Student shell stays reachable deliberately; it is not the default home for operators.

---

## Validation results

Commands:

```bash
python3 -m pytest \
  tests/presentation/test_ux001_founder_routing.py \
  tests/presentation/test_canonical_journey.py::test_founder_login_lands_on_console \
  tests/presentation/test_canonical_journey.py::test_founder_root_redirects_to_console \
  tests/test_founder_dashboard.py::TestFounderAccess \
  -q
```

| Suite | Result |
|-------|--------|
| `test_ux001_founder_routing` (7 cases: Founder, Admin, Student, Founder+Student, Admin+Student, home endpoint matrix, Student entry link) | **Pass** |
| Existing founder login / root → console | **Pass** |
| Founder access helpers | **Pass** |
| Ruff on touched Python | **Pass** |

---

## Recommendation

1. **Ship as-is** — routing now matches Founder-first architecture for all supported Console operator shapes, including Administrator without capability rows.  
2. **Keep Student OS entry muted** in the Console sidebar foot (as implemented); do not promote it into primary nav.  
3. **Optional follow-up (out of scope):** reciprocal “Return to Console” affordance on the Student shell for dual-role operators — useful for dogfood, not required for UX-001 landing correctness.  
4. **Ops:** Prefer `flask create-admin` / `ensure_founder_admin` so production identities carry Founder + Administrator + Student with capabilities; UX-001 no longer depends on capability rows for Administrator landing, but full bootstrap remains best practice for Studio and permissions depth.

---

## Summary

Founder and Administrator identities now land on `/console/` by default. Student-only identities continue to land in Student OS. Dual-role accounts stay Console-first with an explicit **Enter Student Experience** link. No UI redesign beyond that single routing affordance.
