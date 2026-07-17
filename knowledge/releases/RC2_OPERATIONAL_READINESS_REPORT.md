# V1SP-001 — Version1-RC2 Operational Readiness Report

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-001  
**Status:** QUALITY GATE — complete  
**Nature:** Audit only (no feature development). One **Critical** production defect was remediating during review.  
**Date:** 2026-07-17  
**Build identity:** Product `1.0.0` (`pyproject.toml` / `APP_VERSION`) · Internal Alpha chrome **Build RC2** (`app/brand_identity.py`)

---

## Executive Summary

Kwalitec Version1-RC2 was reviewed as a complete system against the Product Blueprint, Design Principles, POP-002 Founder Information Architecture, and the IAHF-003 / IAHF-004A / IAHF-004B implementation reports.

**Verdict:** The product is suitable for **continued Internal Alpha deployment** and can serve as the **operational baseline before Version 2**, provided the High-severity hardening items in this report are tracked and closed in a short stabilisation pass.

The major POP-001 / POP-002 failure modes (dual Founder homes, unwired Alpha zeros on the navigable home, missing brand infrastructure) are **resolved** in code by IAHF-003–004B. Student learning workflows (plan → session → analytics) are coherent. Auth is invite-only and intentionally closed to public registration. Brand and Internal Alpha identity are consistent across chrome.

One **Critical** defect was discovered: production CSP (`APP_ENV=production`, as set in `render.yaml`) blocked inline scripts used by Analytics, Product Check-in, Study Plan wizard step 4, and destructive-action confirms. That defect was **fixed during this review** (see Issues C-1). No other Critical blockers remain undocumented.

Remaining gaps are High/Medium/Low: session cookie hardening, open-redirect edge cases, Founder Feedback density, documentation drift, oversized brand rasters, and Alpha UX honesty issues (archive, settings no-ops).

---

## Release Recommendation

**APPROVED WITH MINOR ISSUES**

Interpretation for V1SP:

| Question | Answer |
|---|---|
| Continue Internal Alpha on RC2? | **Yes** |
| Use RC2 as operational baseline before Version 2? | **Yes**, with High items on a short backlog |
| Ship as public / wider release? | **No** — invite-only Alpha only |

---

## Findings

### Authentication

| Topic | Observation |
|---|---|
| Login | Implemented (`app/auth/routes.py`); email normalised; WTForms + CSRF |
| Logout | POST + CSRF; idempotent (not `@login_required`) |
| Registration | **Not publicly exposed** — intentional; regression-covered |
| Password reset | **Not implemented** — login directs users to coordinator; acceptable for Alpha |
| Session / remember-me | Works; production cookie `Secure` / `SameSite` flags **not configured** |
| Protected routes | Feature blueprints use `@login_required` / `@founder_required`; ownership checks present |
| Open redirect | Basic `urlsplit` guard present; bypasses remain (`///…`, `/\…`) |

**Assessment:** Fit for invite-only Alpha. Harden redirect + cookies before wider exposure.

---

### Student Experience

| Surface | Assessment |
|---|---|
| Dashboard | Learning Workspace identity; decision-oriented layout; honest empty states |
| Learning Workspace | Consistent eyebrow/title pattern on Dashboard, Study Plan list, Study Session, Analytics |
| Study Sessions | End-to-end list → start → session → outcomes; history cards are display-only |
| Study Plan | Wizard + active plan path works; **archived plans have no recovery UI** despite copy promising it |
| Analytics | Charts + KPIs present; empty series can show blank canvases / zero KPIs |
| Missions | Study Session naming in nav; core flow solid |
| Settings | Internal Alpha status present; profile Save is flash-only; daily goal claimed but session-only |

**Assessment:** Core study loop is RC2-ready. Polish items (archive, history links, settings honesty) are Medium — acceptable for Alpha with clear operator awareness.

---

### Founder Experience

| POP-002 expectation | Live status |
|---|---|
| One door (Founder Command Centre) | **Met** — sidebar → `/founder` Overview |
| Live Product Check-in SoT | **Met** — Command Centre services; not static empty zeros on home |
| Two-click section reach | **Met** — secondary nav (Overview, Attention, Feedback, Findings, Research, Internal Alpha, Participants, Operations, Releases, Settings) |
| Legacy `/research/founder*` | **Met** — redirects into Command Centre |
| Feedback = inbox (not second homepage) | **Partial** — Feedback still carries dense Research-style summary blocks |
| Post-login Founder landing | **Not met** — all users land on student Dashboard |
| Honest emptiness (offline pipeline) | **Met** on Operations labelling |

**Assessment:** Operationally usable daily ops console. IA not fully clean (Feedback density, sidebar Dashboard false-active, silent inbox cap). Does not re-introduce POP-001 Critical dual-home failure.

---

### Navigation

| Check | Result |
|---|---|
| Student sidebar destinations | Resolve to live endpoints |
| Founder secondary nav | Wired to Command Centre routes |
| Topnav | Email, Alpha badge, appearance — no competing product homes |
| Breadcrumbs | No true breadcrumb component (eyebrows only) — Alpha-acceptable |
| Legacy routes | Research Founder redirects present; mission `/review/*` redirects |
| Dead `url_for` targets | None found in live templates |
| Active-state bugs | **Dashboard** highlights on all `founder_dashboard.*` endpoints (`'dashboard' in request.endpoint`) |

**Assessment:** No dead ends on primary paths. Fix Dashboard active-state before calling nav “complete.”

---

### Branding

| Check | Result |
|---|---|
| Canonical assets | `app/static/branding/` pack present (IAHF-004A) |
| Logos in UI | SVG via `brand_logo.html` (runtime-correct) |
| Favicon / manifest / OG / apple | Wired via `brand_meta.html` |
| Internal Alpha identity | Badge + footer Build RC2 (IAHF-004B) |
| Founder naming | “Founder Command Centre” on live templates |
| Raster weight | PNG lockups / social preview ~5MB+ total — not served by default templates, but bloat repo and risk if referenced |

**Assessment:** Brand infrastructure and experience meet Alpha identity goals. Compress rasters as follow-up.

---

### Responsive Behaviour

| Viewport | Observation |
|---|---|
| Desktop | Shell, Founder secondary nav, Learning Workspace headers coherent |
| Tablet (`≤991.98px`) | Sidebar off-canvas + backdrop; settings sidebar adapts |
| Mobile | Hamburger toggle with `aria-label`; topnav full Alpha badge hidden below `md`; footer wraps |

IAHF-004B recorded desktop/tablet/mobile shell checks. This audit confirmed CSS breakpoints and patterns; full physical-device visual QA remains a release recommendation (not a blocker for invite-only Alpha).

**Assessment:** Responsive shell is present and intentional. Founder CC nav is dense on small screens (Low).

---

### Accessibility

| Check | Observation |
|---|---|
| Keyboard / focus | `--focus-ring` + `:focus-visible` on links, buttons, forms, appearance |
| Skip link | **Missing** |
| Colour contrast | Sidebar muted text at ~0.35–0.55 opacity on navy — risk vs WCAG AA |
| Heading hierarchy | Generally section-header pattern; some duplicate titles (e.g. study session) |
| Image alt | Decorative empty `alt` beside wordmark — acceptable; logos otherwise labelled |
| Nav naming | Founder secondary nav has `aria-label`; student sidebar `<nav>` does not |
| Reduced motion / contrast | Hooks present in `app.css` |

**Assessment:** Baseline focus treatment is good for Alpha. Skip link and contrast pass recommended before wider cohorts.

---

### Performance

| Check | Observation |
|---|---|
| Student Dashboard | Sequential multi-service fan-out; `_timed_call` warns >500ms — known Alpha cost |
| Founder Participants | N+1 user/badge loads |
| Founder Operations / Overview | Filesystem Operational State can be expensive (skipped under `TESTING`) |
| Static caching | Global `Cache-Control: no-store` on **all** responses including static |
| Brand rasters | Oversized PNGs (see Branding) |
| CDN | Bootstrap + Chart.js from jsDelivr — acceptable for Alpha; CSP/CDN trust dependency |

**Assessment:** No optimisation performed (per milestone). Documented for V1SP follow-up; not Alpha-blocking if cohort size remains small.

---

### Security

| Check | Observation |
|---|---|
| CSRF | Enabled outside tests; forms use tokens |
| SECRET_KEY | Rejected when default **and** `APP_ENV=production`; validation does not fully align with `FLASK_ENV`-only production selection footgun |
| DEBUG | `ProductionConfig.DEBUG = False` |
| Session cookies | `Secure` / `HttpOnly` / `SameSite` not set on `ProductionConfig` |
| Headers | nosniff, DENY frame, Referrer-Policy, Permissions-Policy, HSTS in production |
| CSP | **Was Critical** — production blocked inline scripts; **remediated** this review |
| Error handling | Custom 500 without traceback when not propagating; DB rollback |
| Secrets in repo | `.env` gitignored; no hardcoded production secrets found |
| Admin bootstrap | CLI + `StartupService`; email case / password policy gaps on create |

**Assessment:** Sound invite-only posture. Cookie + redirect hardening should precede any broader exposure.

---

### Documentation

| Check | Observation |
|---|---|
| IAHF-003 / 004A / 004B reports | Present under `knowledge/releases/`; structured and complete |
| README Current Release | Still **v0.4.0** — obsolete vs `1.0.0` / RC2 |
| PROJECT_CONTEXT | Frozen at “Milestone 0.1”; blueprint list omits founder / research / calibration |
| ARCHITECTURE | Blueprint map incomplete vs live registration |
| POP-002 “Current Architecture” | Still describes pre–IAHF-003 dual-home world in places |
| Version story | `1.0.0` + Build RC2 + `knowledge/release/VERSION1_RC1*` + CHANGELOG drift |
| Registration messaging | Correctly invite-only in product UI and security docs |

**Assessment:** Release reports for recent hotfixes are good. Top-level orientation docs must be refreshed so Alpha operators are not briefed from obsolete status.

---

## Issues

### Critical

#### C-1 — Production CSP blocked required inline scripts *(remediated)*

| | |
|---|---|
| **Severity** | Critical |
| **Description** | With `APP_ENV=production` (`render.yaml`), CSP `script-src` omitted `'unsafe-inline'`, while Analytics, Product Check-in, Study Plan wizard step 4, and `onsubmit`/`onclick` confirms rely on inline script. Production Alpha would silently lose charts and confirmations. |
| **Evidence** | `app/__init__.py` CSP; templates under `analytics/`, `research/checkin.html`, `study_plan/wizard_step_4.html`, `study_plan/list.html`, `settings/index.html` |
| **Recommendation** | **Fixed in this review:** production `script-src` now includes `'unsafe-inline'` (parity with development). Follow-up: move scripts to static files / nonces and tighten CSP. |
| **Status** | **Remediated** — `app/__init__.py` |

---

### High

#### H-1 — Open-redirect bypasses in `_safe_next_url`

| | |
|---|---|
| **Severity** | High |
| **Description** | Guard rejects `scheme`/`netloc` only. Values such as `///evil.com` and `/\evil.com` are accepted by `urlsplit` and returned. |
| **Evidence** | `app/auth/routes.py` `_safe_next_url` |
| **Recommendation** | Use Werkzeug `url_has_allowed_host_and_scheme`; require a single leading `/`; reject `//` and `\`; expand tests. |

#### H-2 — Production session / remember-me cookies lack Secure and SameSite

| | |
|---|---|
| **Severity** | High |
| **Description** | `ProductionConfig` does not set `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`, or matching `REMEMBER_COOKIE_*`. Defaults leave Secure off. |
| **Evidence** | `app/config.py` |
| **Recommendation** | Set `Secure=True`, `HttpOnly=True`, `SameSite=Lax` for session and remember cookies in production; confirm HTTPS / proxy scheme. |

#### H-3 — SECRET_KEY production gate keys only on `APP_ENV`

| | |
|---|---|
| **Severity** | High |
| **Description** | Default secret is rejected only when `APP_ENV=production`. Selecting production via `FLASK_ENV` alone with unset `APP_ENV` can load `ProductionConfig` without the hard fail. Render path sets `APP_ENV` correctly. |
| **Evidence** | `app/__init__.py` `_validate_env_vars` vs `_select_config` |
| **Recommendation** | Align validation with the config actually selected; reject empty / placeholder secrets whenever production config is active. |

#### H-4 — Sidebar “Dashboard” falsely active on Founder pages

| | |
|---|---|
| **Severity** | High |
| **Description** | `'dashboard' in request.endpoint` matches `founder_dashboard.*`, so student Dashboard appears selected throughout the Command Centre. |
| **Evidence** | `app/templates/partials/sidebar.html` |
| **Recommendation** | Match `request.endpoint.startswith('dashboard.')`; add regression test. |

#### H-5 — Feedback section still overloaded as a second homepage

| | |
|---|---|
| **Severity** | High |
| **Description** | Feedback carries Internal Alpha summary, “since yesterday”, Product Health, and insights before the inbox — fighting POP-002 “triage before analysis.” |
| **Evidence** | `founder_dashboard/feedback.html` |
| **Recommendation** | Reduce Feedback to inbox + filters + actions; keep health/insights on Research / Internal Alpha. |

#### H-6 — Inbox hard-capped at 50 without in-page truncation notice

| | |
|---|---|
| **Severity** | High |
| **Description** | Inbox listing is capped; Feedback UI may not surface “showing 50 of N,” risking silent loss of older submissions. |
| **Evidence** | `FounderResearchService.list_inbox(limit=50)`; Command Centre inbox display cap |
| **Recommendation** | Pagination or explicit truncation banner with total count. |

#### H-7 — Top-level documentation obsolete for RC2 briefing

| | |
|---|---|
| **Severity** | High |
| **Description** | README still claims **v0.4.0**; PROJECT_CONTEXT / ARCHITECTURE omit live blueprints and brand paths. Operators reading top-level docs get a false product status. |
| **Evidence** | `README.md`, `PROJECT_CONTEXT.md`, `ARCHITECTURE.md` |
| **Recommendation** | Refresh Current Status to Version1-RC2 Internal Alpha; update blueprint maps; publish one version fingerprint table (`1.0.0` / Build RC2). |

#### H-8 — Global `Cache-Control: no-store` on every response

| | |
|---|---|
| **Severity** | High |
| **Description** | Security header middleware forces `no-store` for HTML **and** static assets, preventing browser caching of CSS/JS/branding. |
| **Evidence** | `app/__init__.py` `_add_security_headers` |
| **Recommendation** | Exempt static (or hashed static) from `no-store`; keep strict caching for authenticated HTML if desired. |

#### H-9 — Oversized brand raster assets

| | |
|---|---|
| **Severity** | High |
| **Description** | `logo-primary.png` (~1.2MB), `logo-white.png` (~1.4MB), `logo-icon.png` (~738KB), `social-preview.png` (~1.7MB). Templates prefer SVG, but assets remain a deploy/weight risk. |
| **Evidence** | `app/static/branding/` |
| **Recommendation** | Compress/resize; export a 1200×630 OG crop; keep SVG as runtime default. |

---

### Medium

| ID | Area | Description | Recommendation |
|---|---|---|---|
| M-1 | Auth | No login rate limiting / lockout | Rate-limit IP+email or use edge WAF |
| M-2 | Auth | Admin email not lowercased on create; weak password policy on admin bootstrap | Normalise email; enforce ≥8 chars |
| M-3 | Student | Study plan archive is a dead end (copy promises archived list) | Add archived filter/list or change copy |
| M-4 | Student | Mission history cards non-interactive | Link to recorded / in-progress session |
| M-5 | Student | Settings profile Save no-op; daily goal session-only but claimed as product behaviour | Implement or remove claims |
| M-6 | Student | Analytics empty charts / zero KPIs without empty-state copy | Empty-state messaging in chart cards |
| M-7 | Founder | Founders post-login land on student Dashboard | Optional Founder Overview default |
| M-8 | Founder | Overview “Today” card does not filter Feedback to today | Pass today’s date range on click-through |
| M-9 | Founder | Participants N+1 queries; Operations capability titles incomplete | Batch loads; honest title/status |
| M-10 | Founder | Shared student Main/Analysis chrome while operating | Optional denser Founder shell later |
| M-11 | Nav / Docs | Heritage Research/FOS templates retained; POP-002 as-built appendix stale | Deprecate heritage templates; refresh POP-002 appendix |
| M-12 | A11y | Likely low-contrast muted sidebar text; student nav lacks accessible name | Raise opacity; `aria-label="Primary"` |
| M-13 | Security | Backup restore mass-assignment risk; CDN script trust | Allowlist restore fields; prefer vendored assets later |
| M-14 | Performance | Student dashboard multi-service fan-out | Coalesce / drop unused widgets in a perf milestone |

---

### Low

| ID | Area | Description | Recommendation |
|---|---|---|---|
| L-1 | Auth | No self-service password change | Document operator reset; add later |
| L-2 | Student | Learning Outcomes always “Not available yet” on roadmap | Hide until available |
| L-3 | Nav | No breadcrumb component | Accept for Alpha or add on deep pages |
| L-4 | Brand | Study Plan **view** still uses `display-6` | Align to section-header pattern |
| L-5 | A11y | No skip link; duplicate session headings; hamburger SVG lacks `aria-hidden` | Add skip link; tidy headings |
| L-6 | Terminology | Share Feedback vs Daily Reflection / Product Research eyebrow | Align labels |
| L-7 | Founder | Ten-link CC nav dense on mobile; heritage `data-rip003` attribute | Group nav later; rename data attr |
| L-8 | Docs | IAHF-003 limitations mention branding not in scope after 004A/B; twin `knowledge/release` vs `releases` folders | Errata + cross-link |

---

## Strengths

1. **Invite-only auth posture** — public registration closed and tested; CSRF; password hashing; broad login protection.
2. **Founder Command Centre (IAHF-003)** — one operational door, live Product Check-in source of truth, legacy Research redirects, honest Operations emptiness for unwired offline pipeline.
3. **Brand system (IAHF-004A/B)** — canonical branding directory, shared meta/logo/badge/footer partials, Internal Alpha · Founding Cohort · Build RC2 chrome, Learning Workspace / Command Centre naming.
4. **Student learning loop** — Dashboard → Study Plan → Study Session → Analytics is navigable and explainability language is cautious.
5. **Design governance** — PRODUCT_BLUEPRINT, DESIGN_PRINCIPLES, and POP-002 give a coherent evaluation frame; recent release reports are complete.
6. **Production bootstrap** — `StartupService` migrations + admin creation; health endpoint; security headers and HSTS in production.
7. **Responsive shell** — off-canvas sidebar, viewport meta, Alpha badge responsive behaviour already considered.
8. **Focus treatment** — intentional `:focus-visible` rings rather than none.

---

## Release Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Session cookies without Secure on public HTTPS | High | H-2 before wider cohort |
| Open redirect after login | High | H-1 |
| Operators briefed from obsolete README / PROJECT_CONTEXT | High | H-7 docs refresh |
| Founder misses submissions past inbox cap | High | H-6 |
| Dashboard fan-out latency as Alpha grows | Medium | M-14; monitor `_timed_call` |
| Accidental reliance on heritage Research templates by future editors | Medium | M-11 |
| CDN / `'unsafe-inline'` CSP trade-off (post C-1 fix) | Medium | Plan nonce + external JS hardening |
| Archive / settings trust gaps for Alpha testers | Medium | M-3, M-5 copy or implement |

No undocumented Critical runtime blockers remain after C-1 remediation.

---

## Final Recommendation

**RC2 should proceed** as the Internal Alpha operational baseline under recommendation **APPROVED WITH MINOR ISSUES**.

Proceed with:

1. Continued Internal Alpha deployment on the current RC2 build identity (`1.0.0` / Build RC2).
2. A short V1SP hardening backlog for High items H-1–H-9 (security cookies/redirect, Founder Feedback/nav honesty, docs refresh, static caching, asset compression).
3. **Do not** open public registration or widen beyond Founding Cohort until High security items (H-1, H-2, H-3) are closed.
4. Treat Version 2 feature programmes as **out of band** until High stabilisation items are accepted or explicitly deferred by product owner.

**Critical remediation applied this review:** production CSP now permits the inline scripts the application already ships (`app/__init__.py`). No other code changes were made.

---

## Review Method & Scope

| Item | Detail |
|---|---|
| Method | Inspect → classify → prioritise → recommend |
| Code changes | Critical C-1 CSP fix only |
| Mandatory references reviewed | PRODUCT_BLUEPRINT.md; DESIGN_PRINCIPLES.md; POP-002; IAHF-003; IAHF-004A; IAHF-004B |
| Areas covered | Authentication, Student, Founder, Navigation, Branding, Responsive, Accessibility, Performance, Security, Documentation |
| Tests executed this gate | None mandated (audit); recommend re-run auth / IAHF / routes suites after any hardening commits |

---

## Acceptance Criteria

| Criterion | Status |
|---|---|
| Entire application reviewed across mandated areas | Met |
| Findings classified by severity | Met |
| No undocumented Critical issues remain | Met (C-1 documented and remediated) |
| Operational readiness recommendation produced | Met — **APPROVED WITH MINOR ISSUES** |
| Report completed at `knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md` | Met |
| No feature development except Critical | Met |

---

*End of V1SP-001 Operational Readiness Report.*

---

## Errata (post-gate — V1SP documentation trail)

Recorded during **V1SP-005** so operators do not treat closed findings as still open:

| Finding | Status after V1SP |
|---|---|
| H-1–H-9 (incl. H-7 docs refresh) | **Closed** in V1SP-001B (`77edeb8`) |
| Documentation section claiming README `v0.4.0` / PROJECT_CONTEXT “Milestone 0.1” | **Superseded** — top-level docs carry `1.0.0` / Build RC2; further refreshed in V1SP-005 |
| Medium/Low Alpha deferrals | Remain open unless a later V1SP report closes them |

Canonical release notes for this fingerprint: `docs/release/RELEASE_NOTES_v1.0.0-RC2.md`.
