# DEP-002 — Executive Summary

**Programme:** DEP-002 — Production Runtime Investigation  
**Date:** 2026-07-27  
**Mode:** Investigation only (no code, config, or deploy changes)  
**Production host:** `https://kwalitec.onrender.com`

---

## Verdict

**Exactly one primary root cause:**

### H — Legacy runtime intentionally preserved but never hidden

Stage 1 sole runtime (`KWALITEC_V2_SOLE_RUNTIME=1`) is a **presentation gate**, not a full replacement. Production correctly enables the flag and redirects competing educational homes (`/`, `/dashboard/`, `/missions/`, `/analytics/`, nested LXP session) to the Education Operating System (EOS). The Version 1 application shell, blueprints, and templates remain registered and **still render** for shared surfaces (Study Plan, Help, Onboarding, Settings subpages, Research). EOS navigation **intentionally links** into those V1 shells. New users without an active study plan **land in the V1 Study Plan wizard** immediately after login.

That is why production feels like EOS layered on top of the previous application: both stacks coexist by design under V2-023 / EP-007.1.

---

## What is *not* the root cause

| Hypothesis | Status | Evidence |
|---|---|---|
| E — Wrong commit deployed | **Falsified** | `/health` commit `353f4b2…` matches GitHub `main` / local `origin/main` |
| F — Configuration drift / flag missing | **Falsified** | `/` → `Location: /student/`; `render.yaml` sets `KWALITEC_V2_SOLE_RUNTIME=1` |
| B — Feature flag not enforced | **Falsified** | Root + legacy home redirects fire under sole runtime |
| G alone — Login always enters legacy home | **Insufficient** | Login uses `canonical_home_url()` when a plan exists; no-plan path uses Study Plan wizard (legacy shell) as a **symptom of H** |
| Separate `src/web` EOS Flask app live | **Falsified** | `wsgi.py` → `app.create_app()` only |

---

## One-line answer for release

Production is serving the intended sole-runtime commit with the flag on; dual experience persists because **legacy blueprints and the V1 `layouts/base.html` shell were retained for soak/rollback and remain reachable through EOS navigation and the no-plan login path**.

---

## Recommended next programme

**DEP-003** — Presentation unification / legacy shell retirement under sole runtime (see `RECOMMENDED_REMEDIATION.md`). Do not flip flags or delete blueprints until DEP-003 scopes the student-visible chrome contract.
