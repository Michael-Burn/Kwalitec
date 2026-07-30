# RC-2026.07.29-09 — Founder Validation Baseline Release Report

**Programme:** Release Engineering  
**Status:** **PRODUCTION DEPLOYED — CERTIFIED**  
**Date:** 2026-07-29  
**Host:** `https://kwalitec.onrender.com`  
**Commit Hash:** `a15a8decf76cf2fcbb739b5cc20793de375e6fe9`  
**Commit message:** `release(founder-validation): establish founder validation baseline`  
**Render deploy:** `dep-d9l473vavr4c73a10ngg` (live 2026-07-29T18:19:09Z)

---

## Release Summary

This release freezes and certifies the production platform for **Founder Validation**. No new features and no opportunistic refactors beyond release hygiene (ruff format + one stale Studio-hub test contract).

| Programme | Intent |
|-----------|--------|
| UX-001 | Founder routing — Console landing; deliberate Enter Student Experience |
| UX-002 / UX-002A | Production integrity + Study Plan delete lifecycle |
| UX-003 | Premium Settings |
| UX-004 | Settings information architecture (docs milestone) |
| UX-005 | Theme consistency |
| SOP-001 | Student OS — Home / Journey / History / Revision |
| UX-006 | First-time experience — Founder empty onboarding, published-only catalogue, appearance cycle, empty-state craft |

Production now starts as a true empty Founder Validation baseline: no founder subjects, no published catalogue, Choose Exam empty (legacy CS1/CM1/CB2 hidden when discovery is on).

---

## Commit Hash

`a15a8decf76cf2fcbb739b5cc20793de375e6fe9`

Pushed to `origin/main` and `origin/feature/ap-002-assessment-engine`. **No tag** (per mission). Single release commit only.

---

## Repository Status

### Audit

| Check | Result |
|-------|--------|
| Experimental / debug code | **Clean** — no TODO/FIXME/HACK/debugger markers in release delta |
| Temporary CSS / orphaned assets | **Clean** |
| Unused templates / temp fixtures | **Clean** |
| Scope | UX-006 presentation + published-catalogue membership + contract tests + UX-006 report |

### Files in release commit (29 paths)

Application / presentation: discovery + subject catalogue (published-only when discovery on); Founder Home empty DTO/copy; Choose Exam empty DTO; Console/Student templates; theme cycle JS; tokens / design system / student / founder CSS.

Tests: PX-002 / Console / Founder Home / theme / student templates aligned to product truth (including Studio hub redirects).

Knowledge: `knowledge/product/ux006_first_time_experience/UX006_FIRST_TIME_EXPERIENCE_REPORT.md`

`render.yaml` was **not** modified in git (bridge flags set on live Render env).

---

## Regression Results

| Suite | Result |
|-------|--------|
| Theme / PX-002 / DX-006B Founder Home / Console / student presentation / UX-001 / SOP-001 / UX-005 / platform_integration / auth / StartupService / UX-002A | **683 passed**, 0 failed |
| Ruff lint (release Python paths) | **Clean** |
| Ruff format (release Python paths) | **Clean** (5 files formatted as release hygiene) |

DeprecationWarnings (`datetime.utcnow`, SQLAlchemy `Query.get`) remain in shared libraries — not release blockers.

---

## Production Configuration Audit

Live Render env (service `kwalitec` / `srv-d97ji5t7vvec73cbs5l0`; secrets not printed):

| Variable | Status |
|----------|--------|
| `APP_ENV` | `production` |
| `DATABASE_URL` | SET (Render Postgres `kwalitec-db`) |
| `SECRET_KEY` | SET (≥32 chars; rotated during this release — see Known Issues) |
| `DOCUMENT_STORAGE_ROOT` | `/var/data/curriculum_documents` |
| Persistent disk | Mounted at `/var/data` (1 GB) |
| `KWALITEC_V2_SEED_DEMO` | `0` |
| `KWALITEC_PUBLISHED_SUBJECT_DISCOVERY` | `1` |
| `KWALITEC_RUNTIME_C_ENROLMENT` | `1` |
| V2 sole-runtime stack | Present and ON |
| Auto-deploy | **Off** |

---

## Deployment Results

| Check | Result |
|-------|--------|
| Push to `main` | **Success** (`210860c` → `a15a8de`) |
| First deploy attempt `dep-d9l451n10e5c73fpnij0` | **pre_deploy_failed** — insecure/short `SECRET_KEY` after env restore |
| Corrective env | Strong `SECRET_KEY` generated; full env set restored |
| Certified deploy `dep-d9l473vavr4c73a10ngg` | **live** |
| Build | **Success** |
| Pre-deploy / Alembic | **Success** — stamp `202607280080` = head |
| StartupService | **OK** — health ready after boot |
| Health fingerprint | **OK** — `/health` commit `a15a8de…` |
| Static / theme assets | **OK** — tokens, design_system, student.css, theme.js, app.css all **200** |

---

## Founder Validation Baseline

| Check | Result |
|-------|--------|
| No existing subjects (Home empty) | **Pass** — “No subjects have been created yet.” |
| Create Subject CTA | **Pass** |
| No published curriculum exposed to students | **Pass** — Choose Exam empty |
| Login → `/console/` | **Pass** |
| Theme assets / Light+Dark capture | **Pass** |
| Page errors (Playwright) | **None** |

---

## Student Validation

| Surface | Result |
|---------|--------|
| Home | **Pass** — OS empty “No exam selected yet”; appearance cycle present |
| Journey | **Pass** (200) |
| History | **Pass** (200) |
| Revision | **Pass** (200) |
| Settings | **Pass** (200) |
| Help | **Pass** (200) |
| Choose Exam | **Pass** — empty catalogue copy + Founder Console CTA |
| Appearance cycle / Light / Dark | **Pass** (assets + screenshots) |
| No HTTP 500 / no traceback HTML | **Pass** on all probed routes |

---

## Published Catalogue Validation

| Check | Result |
|-------|--------|
| Discovery enabled in production | **Yes** (`KWALITEC_PUBLISHED_SUBJECT_DISCOVERY=1`) |
| Published catalogue empty | **Yes** |
| Legacy CS1 / CM1 / CB2 selectable | **No** (HTML probe + Choose Exam screenshot) |
| Empty-state copy | “No exams are available yet.” |

---

## Visual Evidence

Stored under `knowledge/evidence/releases/RC20260729_09/`:

| File | Surface |
|------|---------|
| `01_founder_console_light.png` | Founder Console Light — first-time Create Subject |
| `02_founder_console_dark.png` | Founder Console Dark |
| `03_student_home_light.png` | Student Home Light |
| `04_student_home_dark.png` | Student Home Dark |
| `05_journey.png` | Journey |
| `06_history.png` | History |
| `07_revision.png` | Revision |
| `08_settings.png` | Settings |
| `09_choose_exam.png` | Choose Exam empty catalogue |

Metadata: `evidence.json` (0 page errors). Capture helper: `capture_rc09_evidence.py`.

---

## Performance Notes

- Focused regression: **683 passed in ~51s** locally.
- Production DB latency in health: ~2–3 ms.
- Certified deploy window (create → live): ~2 minutes after SECRET_KEY fix.
- No performance tuning in this release.

---

## Known Issues

1. **Env-var PUT hazard (this release):** An initial Render `PUT /env-vars` with only bridge keys replaced the full env set. Env was immediately restored from `render.yaml` intent + Postgres connection-info + admin credentials. **Lesson:** always PUT the complete env vector.
2. **SECRET_KEY rotation:** Production `SECRET_KEY` was rotated to a ≥32-character value during restore (prior live secret was not recoverable after the wipe). Existing browser sessions were invalidated; admin login with restored credentials succeeded.
3. **R-C2 residual:** Health `instance_storage` still reports `/opt/render/project/src/instance` while `DOCUMENT_STORAGE_ROOT=/var/data/curriculum_documents` on the persistent disk mount.
4. **Deprecation noise:** `datetime.utcnow` / SQLAlchemy legacy `Query.get` in shared libraries — not fixed here.
5. **Evidence / this report are post-commit artefacts** on disk (mission: single release commit, no follow-up commits). Commit them in a later docs stamp if archive permanence in git is required.

---

## Recommendation

1. Treat **`a15a8decf76cf2fcbb739b5cc20793de375e6fe9`** as the live **Founder Validation baseline**.
2. Keep auto-deploy **off**.
3. **Freeze** UX/platform polish. Begin **FV-001 Founder Validation** only:
   - Create first subject → curriculum structure → publish → student discovery → enrol → study plan.
4. Do not re-merge legacy on-disk Ready papers into student discovery while the bridge is enabled.
5. Optionally docs-stamp this report + `RC20260729_09` evidence into git when convenient (not required for production certification).

---

## Decision

# FOUNDER VALIDATION BASELINE RELEASE SUCCESSFUL

| Success criterion | Met? |
|-------------------|------|
| Repository clean | **Yes** |
| All release regression tests pass | **Yes** (683 / 0 failing) |
| Single release commit | **Yes** (`a15a8de…`) |
| Successful production deployment | **Yes** (`dep-d9l473vavr4c73a10ngg`) |
| Founder onboarding complete (empty) | **Yes** |
| Student OS operational | **Yes** |
| Published discovery operational | **Yes** |
| No legacy examinations visible | **Yes** |
| Theme system operational | **Yes** |
| Empty states consistent | **Yes** |
| Platform certified for Founder Validation | **Yes** |
