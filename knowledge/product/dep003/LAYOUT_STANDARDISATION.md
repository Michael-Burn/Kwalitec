# DEP-003 — Layout Standardisation

**Programme:** DEP-003 — Student Experience Unification

---

## Goal

One Education Operating System student layout. No duplicate student shells, headers, or sidebars under sole runtime.

---

## Layout family (after DEP-003)

```
layouts/eos_student.html          ← canonical EOS student shell
        ↑
        ├── student/base.html     ← Student Experience surfaces (reading width)
        └── layouts/base.html     ← router under sole → eos_student
                    └── (dual-run) layouts/legacy_workspace.html

session/base.html                 ← EOS Session variant (linear progress chrome)
layouts/auth_base.html            ← login / errors
layouts/console_base.html         ← Founder Console (admin)
```

---

## Router contract (`layouts/base.html`)

```jinja
{% extends "layouts/eos_student.html"
   if (v2_flags and v2_flags.SOLE_RUNTIME)
   else "layouts/legacy_workspace.html" %}
```

Any template that already `{% extends "layouts/base.html" %}` automatically receives EOS chrome when sole runtime is on. **No controller or route changes required.**

Templates migrated by inheritance (not rewritten):

| Area | Templates |
|---|---|
| Study Plan | `wizard_base.html`, `list.html`, `view.html`, `edit.html`, review steps |
| Alpha | `help.html`, `onboarding.html`, feedback forms |
| Settings | `settings/index.html` |
| Research (student) | `checkin.html`, `thank_you.html` |
| Calibration | wizard-based calibration pages |
| Soft-dead LXP | `dashboard/`, `mission/`, `analytics/` (redirect before render under sole) |

---

## EOS student shell contents

`layouts/eos_student.html` provides:

- EOS typography / spacing via `css/student/student.css`
- EOS header (`student-topbar`) + brand logo
- EOS navigation (`student/components/navigation.html`)
- Sign out (POST `auth.logout`)
- Flash messages
- Optional `{% block page_header %}` (used by Student Experience)
- Content block (unchanged page bodies)
- EOS footer (“Reduce decisions. Increase learning.”)
- Confirm modal (Study Plan archive/delete parity)
- `student-main--workspace` width for shared blueprint pages

`student/base.html` extends the same layout and:

- Clears workspace width (reading measure for Home / Journey / …)
- Omits workspace `app.css` (Student Experience uses student tokens only)
- Fills `page_header` from `page.shell`

---

## Session shell

`session/base.html` remains a **focused** EOS variant (progress steps, not full product nav). It is not Version 1 chrome and is not a competing product. Documented as in-scope EOS family for Goal 1/5.

---

## Explicit non-goals

- Did not delete `layouts/legacy_workspace.html` or `partials/sidebar.html`
- Did not rewrite page-level forms or wizard steps
- Did not force Session to use full product nav (would harm focus UX)

---

## Dual-run / rollback

| Flag | Shared student templates (`layouts/base`) |
|---|---|
| `SOLE_RUNTIME=1` | EOS student shell |
| `SOLE_RUNTIME=0` | Legacy workspace (sidebar + topnav) |

Student Experience routes (`student/base`) always use EOS regardless of flag — they never used the sidebar.
