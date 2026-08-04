# P-002.1 — Founder Walkthrough

**Programme:** P-002.1 — Version 1 Release Readiness Validation  
**Date:** 2026-08-04  
**Runtime:** Sole student runtime (`/student/` · `/session/`)  
**Method:** Re-execution of PX-007 17-step surface protocol against tip `272a095…` + automated HTTP/static contracts + LIVE health probe  
**Prior authority:** `knowledge/evidence/releases/PX007/dogfood/WALKTHROUGH.md` · `PX007_DOGFOOD_REPORT.md`

---

## 1. Classification rule

| Class | Meaning |
|-------|---------|
| Critical | Blocks primary path trust or safety |
| Major | Material honesty / premium / safety break on default student paths |
| Minor | Friction or incompleteness; owned |
| Cosmetic | Non-student or comment-level |
| Ideas | Not Version 1 work → Version 1.1 backlog |

---

## 2. Surface walkthrough

| Step | Surface | Result | Notes |
|------|---------|--------|-------|
| 1 | Onboarding | Pass | Private Beta eyebrow; orientation steps honest; no Internal Alpha student voice |
| 2 | Login | Pass | Descriptor + Private Beta; recovery honest |
| 3 | Home | Pass | One composition; skeleton; authorised CTA |
| 4 | Study plan | Pass / Conditional | Sole-runtime identity; archive confirm; dual-settings residual owned |
| 5 | Mission | Pass | Legacy `/mission/` → Home under sole runtime |
| 6 | Session start | Pass | Authoritative `/session/` path |
| 7 | Session during | Pass | Visible steps; timer live region |
| 8 | Finish | Pass | Shared confirm modal; summary path (intentional — see P0021-T1) |
| 9 | Continue | Pass / Conditional | Contention flash + retry contracts; LIVE re-measure residual |
| 10 | Revision | Pass | EOS shell; honest empty |
| 11 | History / Journey | Pass | Day-zero honesty |
| 12 | Analytics | Pass | Redirects to History under sole runtime (emit OFF) |
| 13 | Settings | Conditional | Premium hub + legacy subpages (Minor owned) |
| 14 | Help | Pass | FAQ; Private Beta / Kwalitec identity |
| 15 | Mobile | Conditional | Drawer + 44px tokens; LIVE gallery residual |
| 16 | Accessibility | Conditional | Keyboard/focus/reduced-motion contracts; AT recording residual |
| 17 | Errors | Pass | Reference ID + guidance |

**Primary path verdict:** Completes without Critical or Major product blockers.

---

## 3. Findings register (this validation)

### Critical — 0

None.

### Major — 0

None.

### Minor — owned / carried

| ID | Surface | Description | Disposition |
|----|---------|-------------|-------------|
| PX7-003 / P0021-M1 | Settings | Dual chrome: premium hub vs legacy `/settings/*` | V1.1 |
| PX7-004 / P0021-M2 | Settings | Session-scoped study-goal durability honesty | V1.1 |
| PX7-005 | Settings | “Not set” when prefs unset | Accept |
| PX7-006 | Study plan | Skeleton macro visually-hidden on empty list | Accept |
| PX7-007 / P0021-M3 | Session | Focus control disabled until JS | V1.1 |
| PX7-008 | Mobile | Founder Curriculum Health footer on dual-role | Expected RBAC |

### Cosmetic — carried

| ID | Notes |
|----|-------|
| PX7-009 | Nav docstring “Education Operating System” — comment-only |
| PX7-010 | `/settings/internal-alpha` slug retained — V1.1 optional alias |

### Stale-test residuals (not student defects)

| ID | Test | Interpretation |
|----|------|----------------|
| P0021-T1 | `test_finish_returns_home` | Expects `/student` redirect; product finish → `/session/…/summary` (intentional) |
| P0021-T2 | `test_onboarding_page_explains_core_concepts` | Expects “Meet Study Sensei”; current Private Beta onboarding omits Sensei meet-and-greet (intentional identity) |
| P0021-T3 | `test_allowed_events_match_alpha_contract` | Frozen Alpha allowlist vs expanded EVENT_CATALOGUE; analytics flag OFF |

### Ideas → Version 1.1 backlog (MUST NOT become Version 1 work)

- Account-durable daily study goal  
- Unified settings hub migration  
- Full icon library (`PX-B-051`)  
- Self-service password reset backend  
- axe/Lighthouse CI gate  
- Recorded VoiceOver/NVDA pass  
- LIVE Core Web Vitals field measure  
- LIVE Continue contention re-measure  
- Optional bottom-nav only via Board amendment to `D-MOBILE-NAV`  
- Coach panel contract if Coach returns  

---

## 4. Counts

| Severity | Count |
|----------|------:|
| Critical | **0** |
| Major | **0** |
| Minor (owned) | 6 (carried) |
| Cosmetic | 2 (carried) |
| Ideas | → V1.1 backlog |
| Stale-test residuals | 3 |

---

## 5. Educational / runtime honesty

| Check | Result |
|-------|--------|
| Educational Content Freeze | **Held** |
| EF-001 | **Unchanged** |
| Recommendation Engine | **Unchanged by P-002.1** |
| Student Twin | **Unchanged by P-002.1** |
| Runtime architecture | **Unchanged by P-002.1** |

---

## 6. Exit

Walkthrough complete. No Critical/Major product findings.  
**Do not** declare Version 1 production-ready from walkthrough alone — Gate **G1 FAIL** remains blocking.

Signed: P-002.1 Founder Walkthrough · 2026-08-04
