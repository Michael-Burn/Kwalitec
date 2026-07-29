# RC-2026.07.29-08 — Student Experience Platform Release Report

**Programme:** Release Engineering  
**Status:** **PRODUCTION DEPLOYED — VALIDATED**  
**Date:** 2026-07-29  
**Host:** `https://kwalitec.onrender.com`  
**Commit Hash:** `7577dfeaea46a6676c2315bacd4f6c471314ebbd`  
**Commit message:** `feat(student-os): premium student operating system and platform polish`  
**Render deploy:** `dep-d9l3bjrl550s73fh0op0` (live 2026-07-29T17:20:06Z)

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

`7577dfeaea46a6676c2315bacd4f6c471314ebbd`

Pushed to `origin/main` and `origin/feature/ap-002-assessment-engine`. No tag (per mission).

---

## Files Changed

70 paths (+6816 / −1192) including:

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
- Adjacent prior release artefacts (DP-002…004, RC-07A)
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

`tests/test_v1sp001c_operational_health.py::TestOperationalHealthPermissions::test_nav_includes_operational_health` fails on tip **and** on prior HEAD (`18ffad5`) — Console home HTML does not currently include the literal nav label `Operations`. Out of Student Experience Platform scope.

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

`render.yaml` unchanged. Auto-deploy remains **off**.

---

## Deployment Results

| Check | Result |
|-------|--------|
| Push to `main` | **Success** (`18ffad5` → `7577dfe`) |
| Manual Render deploy | **Success** `dep-d9l3bjrl550s73fh0op0` |
| Build | **Success** (reached update → live) |
| Pre-deploy / Alembic | **Success** — stamp remains `202607280080` = head |
| StartupService | **Inferred OK** — health ready after boot |
| Founder bootstrap | **OK** — admin login succeeded |
| Health | **OK** — `/health/ready` true; commit fingerprint match |
| Static / theme / CSS | **OK** — tokens, design_system, student, session_chrome, theme.js, app.js all **200** |

---

## Production Validation

| Check | Result |
|-------|--------|
| `/health` | **200** `status=ok` `environment=production` `commit=7577dfe…` |
| `/health/live` | **200** |
| `/health/ready` | **200** `ready=true` |
| `/health/details` | **200** — DB ok (~2–3ms); migrations head; queue ok |
| Logs (no startup crash) | **OK** — service reached live; probes clean |
| Persistent storage path | **Partial** — health `instance_storage` ok at `/opt/render/project/src/instance`; `DOCUMENT_STORAGE_ROOT=/var/data/curriculum_documents` set (R-C2 durability residual remains) |
| No 500 on probed routes | **OK** |
| No CSS 404 for session chrome / tokens | **OK** |

---

## Founder Validation

| Check | Result |
|-------|--------|
| Login → `/console/` | **Pass** — POST `/auth/login` → **302** `Location: /console/` |
| Navigation | **Pass** — `console-sidebar` present |
| Enter Student Experience | **Pass** — footer link present |
| Theme JS loaded | **Pass** — `theme.js` referenced |
| Page errors | **None** — console HTML 200, no traceback |

Dark Mode visual switch and browser console errors require human eyes in the browser; server HTML + theme assets are present and loading.

---

## Student Validation

| Surface | Result |
|---------|--------|
| Home | **Pass** — `ds-os-home`, “What should I do now?”, tokens + design_system + student.css + theme.js |
| Journey | **Pass** — `ds-os-journey`, `ds-os-path` |
| History | **Pass** — `ds-os-history`, archive markers |
| Revision | **Pass** — `ds-os-revision` (200) |
| Settings (`/student/profile`) | **Pass** — `settings-info-card`, Product Check-in |
| Help | **Pass** — Product Check-in + Study Sensei copy |
| Study Plan | Auth gate **302** (expected when unauthenticated mid-flow); authenticated path not fully walked |
| Choose Exam | Not separately HTTP-probed this run (covered by local regression) |
| Theme assets | **Pass** — Light/Dark machinery (`theme.js`, tokens) served |
| Welcome modal on Home | **Absent** (SOP-001 / sole-runtime — intentional) |

---

## Visual Validation

Automated HTTP/HTML checks:

- CSS present for OS + session chrome + tokens — **Pass**
- No template/traceback errors on probed authenticated pages — **Pass**
- No duplicate welcome-modal overlay on Home — **Pass**
- Icons / contrast / white-flash / browser DevTools — **Operator browser confirmation recommended** (not fully automatable here)

---

## Performance Notes

- Focused Student Experience regression: ~41s locally (605 tests).
- Production DB latency in health: ~2–3 ms.
- Deploy window (create → live): ~2 minutes.
- No performance tuning in this release.

---

## Known Issues

1. **Pre-existing:** Operational Health nav label assertion (`Operations` on `/console/`) fails on prior and current tip.
2. **R-C2 residual:** Document durability across redeploy — `DOCUMENT_STORAGE_ROOT` set; health still reports default instance path for `instance_storage` component.
3. **Stage 1 pilot credentials:** May still be stale (DP-004 residual).
4. **SQLAlchemy / utcnow deprecations:** Test-log noise; not fixed in this release.
5. **Report hash self-reference:** Git tip is `7577dfe…`; earlier amend cycles left temporary hashes in draft copies — this file records the deployed tip.

---

## Recommendation

1. Treat **`7577dfeaea46a6676c2315bacd4f6c471314ebbd`** as the live Student Experience Platform release tip.
2. Keep auto-deploy **off**.
3. **Freeze Student Experience work.**
4. Next programme: **FV-001 Founder Validation** (Curriculum Studio → subject creation → publish → student consumption). Do **not** begin FV-001 until this release is formally accepted.
5. Optionally complete a short browser pass (Dark Mode toggle + DevTools) and archive screenshots beside this report.

---

## Decision

# STUDENT EXPERIENCE PLATFORM RELEASE SUCCESSFUL

| Success criterion | Met? |
|-------------------|------|
| All release regression tests pass | **Yes** (605 + auth/startup) |
| One clean release commit | **Yes** (`7577dfe…`) |
| Successful Render deployment | **Yes** |
| Founder Console operational | **Yes** (login → `/console/`) |
| Student OS operational | **Yes** (Home/Journey/History/Revision/Settings) |
| Premium Settings operational | **Yes** |
| Theme system operational | **Yes** (assets + shell references) |
| Home, Journey, History, Revision render correctly | **Yes** |
| No production regressions observed on probes | **Yes** |
