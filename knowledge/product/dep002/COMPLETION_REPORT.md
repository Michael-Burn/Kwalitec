# DEP-002 — Completion Report

**Programme:** DEP-002 — Production Runtime Investigation  
**Date:** 2026-07-27  
**Repo HEAD / production commit:** `353f4b294a2a970208c433ed8c81619a91c66a1d`  
**RC tag compared:** `v1.0.0-rc1` → `550d0696a6e81331bbc0d0b8893da97a0ca09761` (production is two commits ahead)  
**Mode:** Investigation / documentation only — **application code, flags, routes, and database intentionally untouched**

---

## Summary

DEP-002 determined why production appears to expose both the legacy Kwalitec Learning Workspace and the Education Operating System. Render serves the current `main` commit with `KWALITEC_V2_SOLE_RUNTIME` behaviourally on (`/` → `/student/`). Dual experience is **not** a bad deploy or missing flag. The primary root cause is **H — legacy runtime intentionally preserved but never hidden**: sole runtime redirects competing homes while V1 blueprints, templates, and chrome remain for shared surfaces and rollback; EOS navigation and the no-plan login path still enter that V1 shell. Deliverables under `knowledge/product/dep002/` provide evidence for a single remediation programme (DEP-003).

---

## Files Created

- `knowledge/product/dep002/EXECUTIVE_SUMMARY.md`
- `knowledge/product/dep002/DEPLOYMENT_AUDIT.md`
- `knowledge/product/dep002/BLUEPRINT_AUDIT.md`
- `knowledge/product/dep002/ROUTE_INVENTORY.md`
- `knowledge/product/dep002/NAVIGATION_AUDIT.md`
- `knowledge/product/dep002/FEATURE_FLAG_AUDIT.md`
- `knowledge/product/dep002/TEMPLATE_AUDIT.md`
- `knowledge/product/dep002/LEGACY_RUNTIME_INVENTORY.md`
- `knowledge/product/dep002/ROOT_CAUSE_ANALYSIS.md`
- `knowledge/product/dep002/RECOMMENDED_REMEDIATION.md`
- `knowledge/product/dep002/COMPLETION_REPORT.md`

---

## Files Modified

None (documentation-only under a new directory). Pre-existing uncommitted local edits to `app/templates/auth/login.html` and `tests/test_px001_brand_identity.py` were **not** part of this programme and were left untouched.

---

## Tests Executed

None (documentation-only). Supporting evidence commands:

```bash
# Deployed identity
curl -sS https://kwalitec.onrender.com/health
curl -sS -D - -o /dev/null https://kwalitec.onrender.com/
curl -sS https://kwalitec.onrender.com/auth/login
curl -sS -D - -o /dev/null https://kwalitec.onrender.com/dashboard/
# … /student/ /missions/ /analytics/ /study-plan/ /health/details

# Local sole-runtime route + shell probes (APP_ENV=testing + V2 flag matrix)
python -c 'from app import create_app; … enumerate blueprints/routes …'
python # authenticated client: classify EOS_TOPNAV vs LEGACY_SIDEBAR

git rev-parse HEAD origin/main v1.0.0-rc1
```

---

## Migration Impact

**None.** No Alembic revisions added or changed. Production migrations observed current=`head`=`202607260001`.

---

## Architecture Compliance

- Layering / curriculum V1/V2: **N/A** — no application or curriculum engine changes.  
- Investigation affirms ADR-007 / V2-023 dual-run soak posture: sole runtime is a **presentation gate**, not blueprint deletion.  
- Separate `src/web` Education OS factory remains orthogonal to production `wsgi:app`.

---

## Technical Debt

- Two student-facing chrome systems remain under production sole runtime (EOS topnav vs V1 sidebar).  
- EOS nav and login no-plan path intentionally deep-link into V1 chrome.  
- Legacy dashboard/mission/analytics templates retained (soft-dead entry) pending retirement soak.  
- Authenticated live founder walkthrough not completed (no credentials in investigator environment).

---

## Known Limitations

- Render Dashboard environment UI / build logs / deploy logs not accessed (no Render API credentials); behavioural probes + `render.yaml` + `/health` used instead.  
- Public registration cannot be exercised (invite-only).  
- No application behaviour changes (by design).

---

## Student Impact Assessment

Template reference: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` (sections applied below).

| Section | Assessment |
|---|---|
| **Student problem** | After Stage 1 deploy, students/founders perceive two products: EOS Home/Session vs V1 Study Plan/Help/Onboarding chrome. |
| **Student benefit (of investigation)** | Clarifies that production is not “broken deploy”; sets correct remediation (unify chrome) vs wrong fixes (redeploy / unset sole). |
| **Learning benefit** | Indirect — reduces risk of chasing flag/deploy fixes that would restore dual-home chaos. |
| **Success metrics** | Root cause named with evidence; DEP-003 scoped; no false production incident. |
| **Risks** | Without DEP-003, Stage 1 pilots continue to see shell switching at Study Plan / Help / first login. |
| **Assumptions** | Founder observation matches dual-chrome behaviour proven under production flag matrix; live auth would show the same transitions. |

---

## Estimated KSI contribution

**ΔKSI = 0** (investigation / docs only; no student-facing behaviour change).  
Categories K1–K8 unchanged. Enables a future DEP-003 that could move K1 (journey coherence) if chrome is unified.

---

## Evidence collected

- Live: `https://kwalitec.onrender.com/health`, `/health/details`, `/`, `/auth/login`, unauthenticated probes of student/legacy paths  
- Repo: `render.yaml`, `wsgi.py`, `app/__init__.py`, `consolidation.py`, `v2_flags.py`, `sidebar.html`, `student/navigation.py`, `auth/routes.py`, V2-023 RC docs  
- Local: blueprint/route dump; authenticated shell classification under production flag matrix  
- Git: `353f4b2` vs `v1.0.0-rc1` (`550d069`)

---

## Lessons learned for student value

Sole-runtime “cutover” language can be read as “old app gone.” In Kwalitec it means “old homes redirect.” Shared V1 chassis still carries planning and help — the highest-friction student moments — so perceived replacement fails even when flags are correct. Future cutover programmes should define **chrome unification**, not only home redirects, as the student-visible done state.

---

## Explainability Review

**N/A** — no student-facing intelligence / recommendation / readiness behaviour changed.

---

## Recommendation Quality Review

**N/A** — no recommendation ranking or Coach/Insights behaviour changed.

---

## Version 1 readiness residual

**N/A for declaration.** Investigation does not claim Version 1 production-ready progress. Residual relevant to pilots: dual chrome under sole runtime remains an open presentation debt (see DEP-003). Gates G1–G12 unchanged by this docs programme.
