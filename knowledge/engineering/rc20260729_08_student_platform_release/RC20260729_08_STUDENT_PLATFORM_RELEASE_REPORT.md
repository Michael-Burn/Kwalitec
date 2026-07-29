# RC-2026.07.29-08 — Student Experience Platform Release Report

**Programme:** Release Engineering  
**Status:** Release Candidate — certified for production deploy  
**Date:** 2026-07-29  
**Host:** `https://kwalitec.onrender.com`  
**Commit Hash:** `000fe4b5d900648df3e41317ce268934e0dfea14`  
**Commit message:** `feat(student-os): premium student operating system and platform polish`

---

## Release Summary

This release certifies and deploys the complete Student Experience Platform stack:

| Programme | Intent |
|-----------|--------|
| UX-001 | Founder routing — Administrator/Console operators land on `/console/`; deliberate Enter Student Experience |
| UX-002 / UX-002A | Production state + Study Plan delete lifecycle (research feedback detach; IntegrityError handling) |
| UX-003 | Premium Settings presentation on Student Settings |
| UX-004 | Settings information architecture review (docs; no code in that milestone) |
| UX-005 | Theme consistency — `session_chrome.css`, semantic tokens, Dark Mode contrast |
| SOP-001 | Student OS — Home / Journey / History / Revision as one-question mastery surfaces |

No additional feature work. No opportunistic refactors beyond release hygiene (lint/format, test contract alignment to certified product).

---

## Commit Hash

`000fe4b5d900648df3e41317ce268934e0dfea14`

---

## Files Changed

### Application / presentation

- Founder access + Console sidebar + Console CSS
- Student Home DTO/service/view models/views; consolidation
- Educational continuity + internal alpha reset + Study Plan delete paths
- Student OS templates (home, journey, history, revision, profile)
- Design system / tokens / student CSS / Assessment + Quick Check session chrome
- Icons, empty-state, macros; assessment base CSS links

### Tests

- New: SOP-001, UX-001, UX-005, UX-002A contract suites
- Updated: student presentation contracts aligned to SOP/UX product truth
- Theme system + Internal Alpha reset coverage

### Knowledge

- Programme reports for UX-001…005, SOP-001
- Adjacent prior release artefacts (DP-002…004, RC-07A) archived with this tip
- This report

`render.yaml` was **not** modified.

---

## Regression Results

| Suite | Result |
|-------|--------|
| SOP-001 / UX-001 / UX-005 / UX-002A / theme / reset / DX-006B + `tests/presentation/student/` | **605 passed** |
| Auth (`tests/test_auth.py`) | **Passed** |
| StartupService (`tests/test_startup_service.py`) | **Passed** |
| UX-001 founder routing | **Passed** |
| Ruff lint (release Python paths) | **Clean** |
| Ruff format (release Python paths) | **Clean** |

### Pre-existing residual (not introduced by this release)

`tests/test_v1sp001c_operational_health.py::TestOperationalHealthPermissions::test_nav_includes_operational_health` fails on tip **and** on prior HEAD (`18ffad5`) — Console home HTML does not currently include the literal nav label `Operations`. Out of Student Experience Platform scope; tracked as Known Issue.

DeprecationWarnings (`datetime.utcnow`, SQLAlchemy `Query.get`) remain in shared libraries — not release blockers.

---

## Production Configuration Review

Live Render env (service `kwalitec`, secrets not printed):

| Variable | Status |
|----------|--------|
| `APP_ENV` | `production` |
| `DATABASE_URL` | SET (from Render Postgres) |
| `SECRET_KEY` | SET |
| `DOCUMENT_STORAGE_ROOT` | `/var/data/curriculum_documents` |
| `KWALITEC_V2_SEED_DEMO` | `0` |
| `FLASK_APP` | `wsgi.py` |
| V2 sole-runtime flags | Present and ON |

`render.yaml` unchanged vs repository tip (MD5 match to HEAD). Auto-deploy remains **off**.

---

## Deployment Results

*(Filled after Render deploy.)*

| Check | Result |
|-------|--------|
| Push to deploy branch | PENDING |
| Manual Render deploy | PENDING |
| Build | PENDING |
| Pre-deploy / Alembic | PENDING |
| StartupService | PENDING |
| Founder bootstrap | PENDING |
| Health | PENDING |
| Static / theme / CSS | PENDING |

---

## Production Validation

*(Filled after deploy.)*

| Check | Result |
|-------|--------|
| `/health` / `/health/ready` | PENDING |
| Logs (no startup crash) | PENDING |
| Persistent storage path | PENDING (R-C2 residual may remain) |
| No 500 on probed routes | PENDING |
| No CSS 404 for session chrome / tokens | PENDING |

---

## Founder Validation

*(Filled after deploy.)*

| Check | Result |
|-------|--------|
| Login → `/console/` | PENDING |
| Navigation | PENDING |
| Dark Mode | PENDING |
| Theme switch | PENDING |
| Enter Student Experience | PENDING |

---

## Student Validation

*(Filled after deploy.)*

| Surface | Result |
|---------|--------|
| Home | PENDING |
| Journey | PENDING |
| Revision | PENDING |
| History | PENDING |
| Settings | PENDING |
| Study Plan | PENDING |
| Help | PENDING |
| Choose Exam | PENDING |
| Theme Light / Dark | PENDING |
| Responsive | PENDING |

---

## Visual Validation

*(Filled after deploy.)*

Confirm: readable text, CSS present, icons intact, no broken layouts, no white flashes, no colour/contrast regressions, no duplicate navigation — PENDING.

---

## Performance Notes

- Focused Student Experience regression: ~41s locally (605 tests).
- No performance tuning in this release.

---

## Known Issues

1. **Pre-existing:** Operational Health nav label assertion (`Operations` on `/console/`) fails on prior and current tip.
2. **R-C2 residual:** Document durability across redeploy depends on Render disk / `DOCUMENT_STORAGE_ROOT` — path is set; cross-redeploy durability still operator-owned.
3. **Stage 1 pilot credentials:** May still be stale (DP-004 residual); not re-litigated here.
4. **SQLAlchemy / utcnow deprecations:** Noise in test logs; not fixed in this release (scope freeze).

---

## Recommendation

1. Deploy this commit to Render `kwalitec` (manual deploy; auto-deploy off).
2. Complete Founder + Student + visual validation checklists in this report.
3. On acceptance: **freeze Student Experience work**.
4. Next programme: **FV-001 Founder Validation** (Curriculum Studio → publish → student consumption). Do **not** start FV-001 during this release window.

---

## Decision

# PENDING PRODUCTION DEPLOYMENT

Local certification (tests + lint + config review) complete. Deploy and live validation required before final ACCEPT.
