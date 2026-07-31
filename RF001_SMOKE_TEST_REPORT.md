# RF-001 — Smoke Test Report

**Programme:** Release Freeze Programme RF-001  
**Date:** 2026-07-31  
**Method:** Uninterrupted Flask test-client walkthrough + existing workflow / alpha smoke suites  
**Authority:** Verification only — no product changes during smoke

---

## Overall

| Walkthrough | Result | Score |
|-------------|--------|-------|
| Founder | **PASS** | 8/8 primary steps |
| Student | **PASS** | 9/9 primary steps |
| Combined path checks | **PASS** | **17/17** |
| Workflow + alpha smoke (venv) | **PASS** | 84/84 integrity/smoke subset; founder/student workflow verbose all green |

**No release blockers discovered. No blocker fixes required.**

---

## Founder walkthrough

Login → Dashboard → Create Subject / Studio → Upload → Preview → Approve → Publish → Feedback → Logout

| Step | Result | Evidence |
|------|--------|----------|
| Login | **PASS** | Founder login → console grant |
| Dashboard | **PASS** | `GET /console/` → 200 |
| Create Subject / Studio | **PASS** | `GET /console/studio/` → 200, “Curriculum Studio” |
| Upload | **PASS** | Workspace `ws-cs1` shows Upload |
| Preview | **PASS** | Preview chrome present |
| Approve | **PASS** | Approve chrome present |
| Publish | **PASS** | Publish chrome present; workflow posts validate/preview/approve/publish redirect home→workspace |
| Feedback | **PASS** | `GET /console/feedback` → 200 |
| Logout | **PASS** | `POST /auth/logout` → login |

Supporting suite: `tests/presentation/workflows/test_workflow_founder_studio.py` — Create Subject form, stage labels Upload/Preview/Approve/Publish, primary CTAs, publish success flash — all **PASSED**.

---

## Student walkthrough

Login → Today's Mission / Home → Session Overview → Study Session → Reflection → Completion → History → Revision → Logout

| Step | Result | Evidence |
|------|--------|----------|
| Login → Home / Mission | **PASS** | `/student/` (follow redirects) → 200 |
| Session Overview | **PASS** | `/session/…/overview` → 200 |
| Study Session | **PASS** | `/activity` → 200 |
| Reflection | **PASS** | `/reflection` → 200 |
| Summary | **PASS** | `/summary` → 200 |
| Completion | **PASS** | `/complete` → 200 |
| History | **PASS** | `/student/history` → 200 |
| Revision | **PASS** | `/student/revision` → 200 |
| Logout | **PASS** | `POST /auth/logout` → login |

Supporting suite: `tests/presentation/workflows/test_workflow_student_session.py` — home handoff, begin→activity, full happy path, History — all **PASSED**. Alpha student smoke surfaces — **PASSED**.

---

## Performance sanity (Phase 6)

| Check | Result |
|-------|--------|
| Obvious slow pages | **PASS** — login ~0.5 s; console/studio workspace <100 ms in test client |
| Broken assets | **PASS** — live CSS/JS 200 |
| Missing CSS/JS | **PASS** — login references fingerprinted `/static/css/*` and `/static/js/*` |
| Unexpected redirects | **PASS** — auth gates and logout behave as designed; experience/onboarding redirects expected for fresh student |
| Console / network failures | **N/A browser** — HTTP smoke shows no 5xx on primary paths |

Not a performance optimisation programme. No release blockers.

---

## Notes

- Logout is **POST** (GET returns 405) — expected, not a blocker.
- Fresh students may pass through `/alpha/onboarding` / experience selection before Home — expected Internal Alpha behaviour.
- Session surfaces without an active SCI may log Runtime A fallback telemetry; pages still render 200. G1 study uses enrolled Runtime C learners.

---

## Verdict

**SMOKE PASS** — Founder and Student uninterrupted primary paths complete. Safe to document Founder Validation Build after deploy cutover.
