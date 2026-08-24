# Cursor Current State Report — 2026-08-24

**Audience:** Chief architect (Claude) · Human founder  
**Author role:** Implementation engineer (Cursor / Composer)  
**Report class:** Engineering-state snapshot only (read-only collection)  
**Generated (UTC):** 2026-08-24T08:55:55Z (approx.; collection window continued past this stamp)  
**Workspace:** `/Users/kwalitec/Developer/kwalitec`  
**Collection note:** No application code, config, migrations, or product docs were modified for this report other than creating this file under `knowledge/product/status_reports/`.

---

## 1. Repo snapshot

| Item | Value | Source |
|------|-------|--------|
| Branch | `main` (tracks `origin/main`, up to date at collection) | `git status -sb`; `git rev-parse --abbrev-ref HEAD` |
| HEAD commit | `b4ea71d65fe862c4fdef4c043319a367c090df5a` | `git rev-parse HEAD` |
| HEAD date | 2026-08-04 22:13:05 +0200 | `git log -1 --format='%ci'` |
| HEAD subject | docs(rel001): record Early Access baseline deploy and smoke evidence | `git log -1 --format='%s'` |
| Product version file | `2.0.0-beta.1` | `VERSION`; `app/version.py` `_FALLBACK_VERSION` |
| Latest annotated tag (name) | `rel-001` | `git describe --tags --abbrev=0`; `git tag --sort=-creatordate` |
| `rel-001` tag object | `feaa7543d324c69f2a94fd64a8862ad90103d14d` | `git rev-parse rel-001` |
| `rel-001` peeled commit | `95a82b04ae50d32003add3a2f5e6789005a4c962` — *REL-001: Early Access Baseline Release* | `git rev-parse 'rel-001^{commit}'` |
| Commits after `rel-001` on `main` | 1 (`b4ea71d` docs-only REL-001 evidence) | `git rev-list --count rel-001..HEAD`; `git log --oneline rel-001..HEAD` |
| Other recent version tags observed | `v2.0.0-beta.1`, `v2.0.0-beta.1-rc2`, `v1.0.0-G1`, `v1.0.0-fv1`, `v1.0.0-rc2`, … | `git tag --sort=-creatordate` |
| Working tree | Dirty: **7** modified tracked files + **295** untracked paths (local WIP; not on `origin/main`) | `git status --porcelain` counts |

### 1.1 Commit volume (last 30 days)

- Window used: `git log --since='30 days ago'` on 2026-08-24 → first commit in window `7f5e9a4` (2026-07-26).
- Commit count in window: **240** (source: `git log --since='30 days ago' --oneline | wc -l`).
- Per brief: list the **smaller** of “30-day log” vs “50 commits” → **last 50 commits** shown below.

### 1.2 Last 50 commits (newest first)

```
b4ea71d 2026-08-04 docs(rel001): record Early Access baseline deploy and smoke evidence
95a82b0 2026-08-04 REL-001: Early Access Baseline Release
272a095 2026-08-04 feat(edu): activate CS1-017 Rho inventory on LIVE (RO-015)
4ff8c95 2026-08-04 fix(edu): keep Memory Front reachable after Continuity Front tip (RO-014)
667784f 2026-08-04 feat(edu): activate CS1-016 Pi inventory on LIVE (RO-014)
3cc6cc7 2026-08-03 docs(ro013): certify Wave 13 Omicron LIVE-complete with evidence
8432f6a 2026-08-03 feat(edu): activate CS1-015 Omicron inventory on LIVE (RO-013)
e36ded8 2026-08-03 docs(ro012): certify Wave 12 Xi LIVE-complete with evidence
a800c85 2026-08-03 feat(edu): activate CS1-014 Xi inventory on LIVE (RO-012)
bd5090e 2026-08-02 docs(ro011): certify Wave 11 Nu LIVE-complete with evidence
a0d8df6 2026-08-02 feat(edu): activate CS1-013 Nu inventory on LIVE (RO-011)
2429313 2026-08-02 docs(ro010): retain LIVE verify operation logs
8add832 2026-08-02 docs(ro010): certify Wave 10 Mu LIVE-complete with evidence
c409ad2 2026-08-02 feat(edu): activate CS1-012 Mu inventory on LIVE (RO-010)
42f0b72 2026-08-02 docs(ro009): certify Wave 9 Lambda LIVE-complete with evidence
5184675 2026-08-02 feat(edu): activate CS1-011 Lambda inventory on LIVE (RO-009)
17edcdc 2026-08-02 docs(ro008): certify Wave 8 Kappa LIVE-complete with evidence
28a06b1 2026-08-02 feat(edu): activate CS1-010 Kappa inventory on LIVE (RO-008)
1c747f3 2026-08-02 feat(edu): activate CS1-009 Iota inventory on LIVE (RO-007)
f946b8c 2026-08-02 docs(ro006): certify Wave 6 Theta LIVE-complete with evidence
a931f23 2026-08-02 feat(edu): activate CS1-008 Theta inventory on LIVE (RO-006)
7aceaa9 2026-08-02 docs(ro005): certify Wave 5 Eta LIVE-complete with evidence
40c487e 2026-08-01 feat(edu): activate CS1-007 Eta inventory on LIVE (RO-005)
b9a27b0 2026-08-01 docs(ro004): certify Wave 4 Zeta LIVE-complete with evidence
5809678 2026-08-01 feat(edu): activate CS1-006 Zeta inventory on LIVE (RO-004)
f10155e 2026-08-01 docs(ro003): certify Wave 3 Epsilon LIVE-complete with evidence
efe18ad 2026-08-01 feat(edu): activate CS1-005 Epsilon inventory on LIVE (RO-003)
b99b0a8 2026-08-01 feat(edu): activate CS1-003 Delta inventory on LIVE (RO-002)
a2adf49 2026-08-01 docs(ro1r1): record LIVE chrome honesty PASS and close residual
569ce20 2026-08-01 fix(edu): bind session package id from provisioned substance (RO1-R1)
b0d9949 2026-08-01 fix(edu): prevent shared-code cold-start chrome first-match (RO1-R1)
1e24026 2026-08-01 fix(edu): bind Tomorrow Preview chrome to approved package identity (RO1-R1)
e81c089 2026-08-01 docs(ro001): record Wave 1 LIVE deploy, verify, and governance updates
f1ff5dc 2026-08-01 feat(edu): activate CS1-004 Gamma inventory on LIVE publication path
94e02f5 2026-08-01 docs(release): record Sprint C1 commit hash in completion report
afa0010 2026-08-01 feat(edu): activate EC-001 packages on EA-006 live publication path
d8670d5 2026-08-01 docs(release): RC2 Sprint C final GO board and fingerprint update
0d3fc72 2026-08-01 fix(session): persist activity explanation after answer for Continue
06fa896 2026-08-01 docs(release): record Sprint B commit hash in completion report
f4666e8 2026-08-01 fix(edu): restore RC2 educational metric trust (Sprint B)
64ea07f 2026-08-01 docs(release): VERSION1-RC2 fingerprint manifest and Sprint A reports
75c29d2 2026-08-01 chore(release): VERSION1-RC2 hygiene tip with educational inventory
f066bcf 2026-08-01 EF-001: Freeze Educational Framework Version 1 under operational stewardship
613722c 2026-08-01 fix(scripts): make g1 student walkthrough importable on Render jobs
007f0a5 2026-08-01 fix(session): stop Core methods stub and clear placeholder sittings
62b9fc1 2026-07-31 fix(session): force-retire oversized open sittings and stop LO dump fallback
e1b17dc 2026-07-31 fix(session): chunk topic LOs to preferred session length
e5be323 2026-07-31 fix(ui): make flash banner close (X) work on success notices
0728d9f 2026-07-31 fix(session): stop opaque bridge overwriting CMP topics with Core methods
2fe8537 2026-07-31 fix(student): enable Study Session spine under sole-runtime production
```

Source: `git log -50 --oneline --format='%h %ad %s' --date=short`.

### 1.3 Theme grouping (30-day window, prefix heuristic)

Approximate counts from subject prefixes (`git log --since='30 days ago' --oneline` + sort/uniq):

| Theme / prefix | Approx. count | Notes |
|----------------|---------------|-------|
| `feat(edu):` inventory LIVE activation | 16 | RO / CS1 campaign packages |
| `docs(ro*)` / release certification | many | Wave LIVE-complete evidence |
| `fix(session):` / `fix(edu):` / `fix(student):` | ~15+ | Session substance, chrome, baseline |
| `feat(ui):` DX-004/DX-005 | 6 | Founder + Student OS surface migrations |
| `EF-001` | 1 | Educational Framework freeze |
| `REL-001` / release seals | several | Early Access baseline |
| Docs-heavy programme closes (EI/CQ/RI/VP/LP/…) | large share of 240 | Governance / evidence commits |

Exact per-prefix table generated during collection from `git log --since='30 days ago'`.

---

## 2. What has shipped recently (last 30 days)

Layer labels follow `docs/architecture/SYSTEM_ARCHITECTURE.md` (presentation / services / application / domain / models + curriculum data).

### 2.1 REL-001 — Early Access Baseline Release

| Field | Evidence |
|-------|----------|
| Commits | `95a82b0` REL-001; `b4ea71d` docs evidence follow-up |
| What changed | Large release bundle (574 files in `95a82b0` alone per `git show --stat`): evidence under `knowledge/evidence/releases/REL001/`, presentation/student+session tests, release artefacts |
| Layers | presentation (`app/presentation/student`, `session` tests); docs/evidence; not a Runtime A core rewrite in the tip commit |
| Runtime A (`RecommendationService` / `PlanningService` / `ReadinessService`) | **No** in `95a82b0`/`b4ea71d` file lists for those three services |
| Curriculum V1/V2 traversal (`CurriculumService` / engine ordering) | **No** change to `app/services/curriculum_service.py` in these tip commits |
| Programme / reports | REL-001; `REL001_DEPLOYMENT_REPORT.md`, `REL001_SMOKE_TEST_REPORT.md`, `knowledge/evidence/releases/REL001/README.md` (tracked) |
| Tests | Many presentation/PX/LXP tests added/adjusted in `95a82b0` (`git show --stat 95a82b0`) |

### 2.2 RO-002 … RO-015 — CS1 educational inventory LIVE waves

| Field | Evidence |
|-------|----------|
| Commits (examples) | `b99b0a8` RO-002 … `272a095` RO-015 (`feat(edu): activate CS1-0xx …`) |
| What changed | Educational campaign/package JSON under `app/curriculum/data/educational_campaigns/` and `app/curriculum/data/educational_packages/`; selection/view-model tweaks; `tests/application/educational_packages/test_pb002_package_selection.py` updates (e.g. `272a095` 27 files / +4073) |
| Layers | **curriculum data** + **application** (`educational_packages`, occasionally `educational_experience` / `educational_runtime_engine`) + **presentation** view models; not models/ORM |
| Runtime A | **No** (those commits do not touch `app/services/recommendation_service.py`, `planning_service.py`, or `readiness_service.py` — verified via `git log --since=… -- <paths>`) |
| Curriculum V1/V2 traversal | **No** for `CurriculumService` API. Inventory JSON lives under `app/curriculum/data/…`. Separate note: `75c29d2` touched `app/curriculum/loader.py` (+9 lines, discovery exclusions) — **loader discovery**, not section/topic ordering helpers |
| Programme / reports | RO-NNN; examples tracked at repo root: `RO015_DEPLOYMENT_REPORT.md`, `RO015_LIVE_VERIFICATION_REPORT.md`, `RO015_RELEASE_DECISION.md`; evidence dir `knowledge/evidence/releases/RO015/` (README present at HEAD). Parallel untracked `EP015_*` wave docs exist in working tree only |
| Tests | Package-selection tests updated per wave (e.g. `test_pb002_package_selection.py` in RO-014/015 commits) |

### 2.3 RO1-R1 — Tomorrow Preview / chrome honesty

| Field | Evidence |
|-------|----------|
| Commits | `1e24026`, `b0d9949`, `569ce20`, docs `a2adf49` |
| What changed | `app/application/educational_packages/tomorrow_chrome.py`, `composition_overlay.py`, `student_runtime/coordinator.py`, session adapters, `presentation/session` + `presentation/student` |
| Layers | application + infrastructure adapters + presentation |
| Runtime A | **No** |
| Curriculum V1/V2 traversal | **No** |
| Programme / reports | RO1-R1; `RO1R1_IMPLEMENTATION_REPORT.md`, `RO1R1_REGRESSION_REPORT.md`, `RO1R1_LIVE_VERIFICATION.md` (tracked) |
| Tests | `tests/application/educational_packages/test_ro1r1_tomorrow_chrome.py` |

### 2.4 RO-014 follow-up — Memory Front reachability

| Field | Evidence |
|-------|----------|
| Commit | `4ff8c95` |
| What changed | `educational_experience/service.py`, `educational_packages/selection.py`, `educational_runtime_engine/service.py`, `presentation/student/educational_view_models.py` |
| Layers | application + presentation |
| Runtime A | **No** |
| Curriculum V1/V2 traversal | **No** |
| Tests | Not a dedicated new test file in `--stat`; relies on existing package-selection coverage (Evidence: `git show --stat 4ff8c95` shows 4 files, no new test path) |

### 2.5 EF-001 — Educational Framework freeze

| Field | Evidence |
|-------|----------|
| Commit | `f066bcf` |
| What changed | `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md`, `.cursor/rules/11-educational-framework-freeze.mdc`, `knowledge/GOVERNANCE.md` |
| Layers | docs / governance only |
| Runtime A / curriculum traversal | **No** / **No** |
| Tests | None (documentation-only) |

### 2.6 RC2 educational trust + session substance fixes (late July / 1 Aug)

| Field | Evidence |
|-------|----------|
| Commits | `f4666e8` Sprint B trust; `0d3fc72` activity explanation; `007f0a5`/`62b9fc1`/`e1b17dc`/`0728d9f` session substance; `2fe8537` sole-runtime session spine; baseline/wizard fixes `580c159`/`6a3d528`/… |
| What changed | Session/runtime coordinators, substance planners, readiness presentation trust, baseline topic loading |
| Layers | application + infrastructure + presentation + **services** (see Runtime A) |
| Runtime A | **Yes — `ReadinessService`** in `f4666e8` (`app/services/readiness_service.py` 240-line rewrite per `--stat`). **Yes — `RecommendationService`** timestamp stability in `ee38ac2` (2026-07-27). **Yes — `PlanningService`** appeared in `65cb380` Release Candidate 1 (2026-07-27) file list |
| Curriculum V1/V2 traversal | Baseline topic loading uses published syllabus topics (`6a3d528` `student_baseline/topics.py`) — **not** a change to `CurriculumService.get_*` ordering APIs (`git log --since=… -- app/services/curriculum_service.py` empty in window) |
| Reports | `RC2_SPRINT_B_COMPLETION_REPORT.md` (in `f4666e8` tree); various RC2 docs |
| Tests | `tests/test_rc2_educational_trust_consistency.py`; `tests/test_lxp004a_session_substance.py`; `tests/unit/test_objective_chunk.py`; `tests/application/…/test_session_budget_objective_chunk.py`; `tests/application/student_baseline/test_topics.py`; `tests/test_kwp002_student_value_activation.py` |

### 2.7 DX / Student OS UI migrations (late July)

| Field | Evidence |
|-------|----------|
| Commits | `75db780` DX-005A Home; `e1648ee` DX-005B Choose Exam; `ab21b92` DX-005C Study Session; Founder DX-004A–C; `7577dfe` student-os polish |
| Layers | **presentation** (templates/static) primarily |
| Runtime A | **No** (UI commits; not those three service files in the sampled `--stat` outputs) |
| Curriculum V1/V2 traversal | **No** |
| Tests | DX / accessibility / product language tests updated in related release commits |

### 2.8 Settings password change

| Field | Evidence |
|-------|----------|
| Commit | `ee1101d` |
| Layers | presentation (`settings` routes/templates) + forms |
| Runtime A / curriculum | **No** / **No** |
| Tests | `tests/test_settings_password.py` |

### 2.9 Migrations PostgreSQL hotfix

| Field | Evidence |
|-------|----------|
| Commit | `18ffad5` |
| Layers | **models**/schema via Alembic revision edits under `migrations/versions/` |
| Runtime A / curriculum traversal | **No** / **No** |
| Tests | Evidence currently unavailable for a dedicated regression test name beyond the hotfix doc `RC20260729_07_POSTGRES_MIGRATION_HOTFIX.md` in that commit |

### 2.10 Earlier-in-window platform / EI programmes (compressed)

Many `feat(ei-*)`, `feat(ri-*)`, `feat(lp-001)`, `feat(vp-001)`, `feat(fv-001)`, `feat(cq-*)` commits appear in the 30-day log (from ~2026-07-26). Individual file-level audits for every programme were **not** fully expanded in this pass; treat detailed layer maps for those as **Evidence currently unavailable** beyond commit subjects and the selective Runtime A path logs above.

---

## 3. Current test and CI state

### 3.1 Local pytest

| Item | Value | Source |
|------|-------|--------|
| Interpreter | `.venv/bin/python` → **CPython 3.14.6** | `sys.version` |
| Command | `.venv/bin/python -m pytest tests/ --tb=line -q` | collection run 2026-08-24 |
| Result | **229 failed**, **45918 passed**, **9 skipped**, 68275 warnings | final summary line of run (~305.87s) |
| Note | CI matrix uses Python **3.11 / 3.12 / 3.13** (`.github/workflows/ci.yml`). Local 3.14 results are **not** identical to CI target runtimes |

Sampled failure modes (re-run with `--tb=short`):

- `tests/test_time_engine.py::…::test_returns_none_when_no_curriculum_id` → `sqlalchemy.exc.IntegrityError: FOREIGN KEY constraint failed` inserting `study_plans` with `curriculum_id=None`.
- `tests/application/adaptive_mission/…::test_prioritisation_is_deterministic` → FK failure inserting `decision_records`.
- `tests/test_smoke.py::…::test_dashboard_after_plan_creation` → `AssertionError: Study plan was not created` (wizard/baseline redirect loop observed in HTTP log).

Failure taxonomy (top groups by path prefix, from FAILED list):

| Count | Area |
|------:|------|
| 33 | `tests/test_smoke.py` |
| 20 | `tests/infrastructure/adapters` |
| 18 | `tests/test_time_engine.py` |
| 13 | `tests/education_os/adapters` |
| 12 | `tests/infrastructure/session` |
| 10 | `tests/application/assessment_pipeline` |
| 10 | `tests/application/intelligent_tutor` |
| 9 | `tests/application/adaptive_mission` |
| … | remaining 229 total |

Full FAILED nodeids: see **Appendix A**.

Bare `python -m pytest` without `.venv` failed at collection (`ModuleNotFoundError: argon2`) when using system Python 3.14 outside the venv — source: first collection attempt log.

### 3.2 Local architecture suite (informational)

Command: `.venv/bin/python -m pytest tests/architecture/ -q --tb=line`  
Result: **2137 passed** in 3.70s.  
Source: local run output 2026-08-24.

### 3.3 Ruff

Command: `ruff check app/ tests/` (also via `.venv/bin/ruff check … --statistics`)

| Item | Value |
|------|-------|
| Finding count | **790 errors** (full check run; exit non-zero on full report) |
| Top rules | E501 400 · I001 197 · W293 106 · F401 35 · W292 24 · **F821 8** · others |
| Notable F821 | `app/founder/dashboard/routes.py` undefined `flash` / `redirect` (lines ~666+) — `.venv/bin/ruff check --select F821` |

### 3.4 CI on `main`

| Item | Value | Source |
|------|-------|--------|
| Latest run on HEAD `b4ea71d` | **failure** — [run 30946857267](https://github.com/Michael-Burn/Kwalitec/actions/runs/30946857267) | GitHub Actions API `…/actions/runs?branch=main` |
| Failed job | **Architecture Governance** (`python -m pytest tests/architecture/ -v`) | job list for that run; workflow `.github/workflows/ci.yml` lines ~12–38 |
| Downstream jobs | Lint, Unit Tests, EI Certification, Integration, Production Gates, Release Build → **skipped** | same job list |
| Job logs | **Evidence currently unavailable** (API logs endpoint returned HTTP 403 “Must have admin rights”) | `…/actions/jobs/92118874971/logs` |
| Recent history | Last **100** workflow runs on `main` retrieved via API: **100 failures / 0 successes** (oldest in page ~2026-07-13) | `actions/runs?branch=main&per_page=100` |
| Verdict | **CI is not green on `main`** at collection time | above |

Local contradiction: `tests/architecture/` passes on this machine (3.14) while CI Architecture Governance fails — root cause of CI failure **not verified** without logs.

---

## 4. Architecture compliance check

Hard invariants referenced from `CLAUDE.md` §6 / architecture rules. This is a **spot check**, not a full formal audit.

| Invariant | Observation | Source |
|-----------|-------------|--------|
| Business math only in services/application | Legacy `app/dashboard/routes.py` still orchestrates multiple services (`PlanningService`, `ReadinessService`, `RecommendationService`, timed calls). Under sole runtime, index redirects via `redirect_if_sole_runtime("student.home")`. Residual dual-run path retains heavy route orchestration — **layering smell / residual risk**, not newly introduced in RO waves | `app/dashboard/routes.py`; consolidation redirects |
| Flask `request` / `session` in services | **No matches** for `flask.request` / `session[` under `app/services/` | `rg` over `app/services` |
| Flask imports in services | `startup_service.py`, `health_service.py`, `database_readiness_service.py` import `Flask` / `current_app` (bootstrap/health) — explicit app objects, not request handlers | `rg 'from flask import'` |
| Ad-hoc curriculum traversal outside `CurriculumService` | No 30-day commits to `app/services/curriculum_service.py`. Inventory work used educational package JSON + package selection services. `75c29d2` changed `app/curriculum/loader.py` discovery — **flag as loader change**, not proven V1/V2 ordering duplication | `git log -- app/services/curriculum_service.py`; `git show 75c29d2 -- app/curriculum/loader.py` |
| `db.create_all()` in production paths | **No matches** under `app/` / `migrations/` / `wsgi.py` | `rg 'create_all\('` |
| LLM in deterministic cores | **No matches** for openai/anthropic/litellm in `recommendation_service.py` / `planning_service.py` / `readiness_service.py`; broader `app/` scan returned no hits in this pass | `rg -i` |
| New educational UX under legacy shells | Legacy `app/dashboard`, `app/mission`, `app/analytics` still registered (`app/__init__.py`) and redirect when sole runtime ON (`consolidation.py`; route-level `redirect_if_sole_runtime`). **No new files** added under those three trees in the last 30 days (`git log --diff-filter=A -- app/dashboard/ app/mission/ app/analytics/` empty) | git + routes |
| Alembic | Single head `202607310002` (`migrations/versions/202607310002_merge_pb001_sb001a_heads.py`); 59 revision files | Alembic `ScriptDirectory.get_heads()` |

### 4.1 TODOs / FIXMEs recently added

- `git log --since='30 days ago' -p -S'TODO|FIXME' -- app/ tests/` produced **no `+TODO`/`+FIXME` hits** in this collection.
- Live `rg 'TODO|FIXME|XXX|HACK' app/ --glob '*.py'` also returned **empty** in this environment.
- **Evidence currently unavailable** for latent debt markers outside those patterns (e.g. “technical debt” prose in docs).

### 4.2 Ruff-defined defects touching routes

Undefined names in founder dashboard routes (F821) are concrete quality defects in presentation code — see §3.3.

---

## 5. Feature flag state

Authority docs: `docs/production/VERSION_1_FLAG_MATRIX.md` (dated 2026-07-28), production keys in `render.yaml`, resolver `app/application/config/v2_flags.py`, analytics `app/infrastructure/analytics/feature_flag.py`, EI dataclass defaults `app/application/config/feature_flags.py`.

### 5.1 Matrix §2 Production-ON — `render.yaml` vs resolver

| Flag | Matrix intent | `render.yaml` | Resolver with render-like env | Bare empty env |
|------|---------------|---------------|-------------------------------|----------------|
| `KWALITEC_V2_SOLE_RUNTIME` | ON | `value: "1"` | `SOLE_RUNTIME=True` | `False` |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | ON | `1` | `True` | `False` |
| `KWALITEC_V2_DURABLE_STORE` | ON | `1` | `True` | `False` |
| `KWALITEC_V2_INJECT_ENGINES` | ON | `1` | `INJECT_PHASE_I_ENGINES=True` | `False` |
| `KWALITEC_V2_SEED_DEMO` | OFF | `0` | `SEED_DEMO_LEARNERS=False` | `True` (default-true when unset — see resolver) |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | ON | `1` | `True` | `False` |
| `KWALITEC_EI_INTERNAL_ALPHA` | ON | `1` | Not a field on `Version2FeatureFlags`; EI product flags remain code-default OFF (`FEATURE_FLAGS` all `False`) | same |
| `KWALITEC_COMMERCIAL_LOOP` | (matrix §2 footnotes / render comment) | `1` | `SR_COMMERCIAL_LOOP=True` and SR bundle children True except `SR_PILOT_MARK_COMPLETE=False` | commercial OFF |

Sources: `render.yaml` lines 45–69; `resolve_v2_feature_flags(environ=…)` executed 2026-08-24; `FEATURE_FLAGS` dataclass defaults.

### 5.2 Matrix §3 Production-OFF (Twin / personalisation / feedback / analytics)

| Flag | Matrix | In `render.yaml`? | Empty env | Render-like env (only §2 keys set) |
|------|--------|-------------------|-----------|-------------------------------------|
| `KWALITEC_DIGITAL_TWIN` | OFF | **Absent** | `ENABLE_DIGITAL_TWIN=False` | `False` |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | OFF | Absent | `False` | `False` |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | OFF | Absent | `False` | `False` |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | OFF | Absent | `False` | `False` |
| `KWALITEC_DAILY_PLAN_CUTOVER` | OFF | Absent | `False` | `False` |
| `KWALITEC_UNIFIED_JOURNEY` | OFF | Absent | `False` | `False` |
| `KWALITEC_EXPERIENCE_FEEDBACK` (Journey emit UI) | OFF | Absent | `False` | `False` |
| `KWALITEC_LEARNING_FEEDBACK` | OFF | Absent | `False` | `False` |
| `KWALITEC_PERSONAL_LEARNING_PROFILE` | OFF | Absent | `False` | `False` |
| `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1` | OFF | **Absent** from `render.yaml`; also **absent** from `.env.example` grep | `events_v1=False` | `False` |

**Important distinction observed in code:** with `KWALITEC_COMMERCIAL_LOOP=1`, resolver sets `SR_TWIN_DAILY_LOOP=True` (commercial SR bundle) while `ENABLE_DIGITAL_TWIN` remains `False`. These are **different flags** (`v2_flags.py` field docs: SR twin daily-loop vs Digital Twin cutover family). Live Render secret store beyond `render.yaml` was **not** inspected — Evidence currently unavailable for runtime secrets that might override YAML.

`.env.example` documents the OFF flags as commented examples (unset locally).

---

## 6. Known limitations / open debt (code-observed)

1. **Legacy redirect shells still present** — `app/dashboard`, `app/mission`, `app/analytics` packages remain registered; sole-runtime redirects implemented in `app/presentation/consolidation.py` and per-blueprint guards (`dashboard`/`mission`/`analytics` routes). Source: file tree + `rg redirect_if_sole_runtime`.

2. **Stage A vs Twin / Epic 2 coexistence** — Twin/Epic 2 packages and tests remain in-tree (`app/application/student_digital_twin`, `adaptive_mission`, `intelligent_tutor`, …). Cutover flags OFF per §5, but commercial `SR_TWIN_DAILY_LOOP` can be ON independently. Competing dual paths are therefore **structurally present**; which path students hit depends on flags. Source: flag resolver output + package layout.

3. **Dashboard route still service-orchestrating** under non-sole / fallback paths — see §4.

4. **Schema / migrations** — Alembic reports a **single head** (`202607310002`); no multi-head drift detected locally. Incomplete migrations: **none observed** via Alembic heads API. Live DB vs head drift on Render: **Evidence currently unavailable** (no production DB inspection).

5. **Local test instability on Python 3.14** — 229 failures including FK constraint errors; may be environment-specific relative to CI’s 3.11–3.13 matrix — not proven.

6. **Ruff debt** — 790 open findings including undefined names in founder routes.

7. **CI Architecture Governance failing with skipped suite** — blocks verification of green main; logs inaccessible without admin.

---

## 7. What remains (engineering-only view)

Do **not** interpret the following as G1–G12 / KSI / CRI board status.

1. **Dirty working tree** — ~295 untracked artefacts (CS10xx/HR/PB/RO campaign docs, scripts, extra evidence folders, `CLAUDE.md`, `knowledge/product/p003_private_beta_welcome/`, etc.) and 7 modified tracked coverage docs / `PROJECT_CONTEXT.md`. These are **not shipped** on `origin/main`. Source: `git status --porcelain`.

2. **Stale local branches** (behind `main`; ahead counts from `git rev-list --left-right --count main...<branch>`):
   - `feature/ap-002-assessment-engine` — main is 62 commits ahead
   - `feature/sdt-001-foundation` — 229 ahead
   - `feature/educational-architecture-consolidation` — 237 ahead
   - `chore/eng-001-engineering-standards` — 228 ahead
   - `post-v1-development` — 267 ahead / 1 unique

3. **CI not green** — Architecture Governance failure cascades to skip unit/integration/lint jobs (§3.4).

4. **Local full-suite failures** — 229 failing nodeids (§3.1 / Appendix A), including smoke and time-engine suites.

5. **Open feature branches on remote** still tracked: `feature/ap-002-assessment-engine`, `feature/sdt-001-foundation`, `feature/educational-architecture-consolidation` (`git remote show origin`).

6. **Incomplete cutover** — Twin HTTP cutovers, Unified Journey, learning feedback, personalisation, analytics emit remain OFF in code defaults / render.yaml absence (§5), while sole-runtime + commercial loop are ON in render.yaml.

---

## 8. Explicit non-claims

This report:

- does **not** declare Version 1 production-ready;
- does **not** assert educational effectiveness, pass-rate impact, or Private Beta cohort outcomes;
- does **not** change, validate, or re-score KSI, CRI, or gates G1–G12;
- is an **engineering-state snapshot** of the git repository, local test/lint commands, GitHub Actions API metadata, and in-repo flag/config sources only;
- does **not** certify that Render live secrets match `render.yaml` beyond what is committed.

---

## Appendix A — Full local FAILED test nodeids (229)

Collected from `.venv/bin/python -m pytest tests/ --tb=line -q` on 2026-08-24 (Python 3.14.6).

```
FAILED tests/application/adaptive_assessment/test_product_foundations.py::test_regression_alembic_head_unchanged
FAILED tests/application/adaptive_assessment/test_quick_check.py::test_regression_alembic_head_unchanged
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_mission_generation_consumes_twin_decisions
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_prioritisation_is_deterministic
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_prerequisite_recovery_steps_included
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_validation_rejects_inconsistent_recommendation
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_duplicate_active_prevention
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_progress_tracking_and_completion
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_persistence_roundtrip
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_integration_with_learning_graph_and_reasoning
FAILED tests/application/adaptive_mission/test_adaptive_mission.py::test_founder_mission_endpoints
FAILED tests/application/assessment_pipeline/evidence_ingress/test_service.py::test_accept_maps_and_reasons_via_existing_pipeline
FAILED tests/application/assessment_pipeline/evidence_ingress/test_service.py::test_duplicate_bundle_rejected
FAILED tests/application/assessment_pipeline/evidence_ingress/test_service.py::test_student_reasoning_service_entry_point
FAILED tests/application/assessment_pipeline/evidence_ingress/test_service.py::test_regression_existing_reason_unchanged
FAILED tests/application/assessment_pipeline/test_assessment_pipeline.py::test_pipeline_updates_twin_via_reasoning
FAILED tests/application/assessment_pipeline/test_assessment_pipeline.py::test_mission_completion_produces_assessment_evidence
FAILED tests/application/assessment_pipeline/test_assessment_pipeline.py::test_mission_step_progress_emits_assessment
FAILED tests/application/assessment_pipeline/test_assessment_pipeline.py::test_no_duplicated_twin_state_in_assessment_tables
FAILED tests/application/assessment_pipeline/test_assessment_pipeline.py::test_founder_assessment_endpoints
FAILED tests/application/assessment_pipeline/test_assessment_pipeline.py::test_regression_ame_and_sdt_still_load
FAILED tests/application/curriculum_studio/test_independence.py::test_application_no_forbidden_imports
FAILED tests/application/curriculum_studio/test_independence.py::test_no_flask_sqlalchemy_in_application
FAILED tests/application/curriculum_studio/test_matrix.py::test_publication_checklist_matrix[255]
FAILED tests/application/curriculum_studio/test_pi002r_validation_wiring.py::test_regression_validation_requires_version
FAILED tests/application/curriculum_studio/test_regression.py::test_workspace_snapshot_mapping
FAILED tests/application/curriculum_studio/test_regression.py::test_publication_snapshot_mapping
FAILED tests/application/educational_experience/test_acceptance.py::test_home_and_journey_http_render_educational_fields
FAILED tests/application/educational_reasoning/test_educational_reasoning.py::test_student_reasoning_delegates_to_registry
FAILED tests/application/educational_reasoning/test_educational_reasoning.py::test_reasoning_history_immutable
FAILED tests/application/educational_reasoning/test_educational_reasoning.py::test_founder_reasoning_diagnostics
FAILED tests/application/educational_reasoning/test_educational_reasoning.py::test_cip003_retrieval_profile_regression
FAILED tests/application/educational_reasoning/test_educational_reasoning.py::test_educational_reasoning_service_pure_path
FAILED tests/application/educational_runtime_engine/test_integration.py::test_daily_mission_from_derived_template_and_completion_advances
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_tutor_context_construction
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_evidence_assembly
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_response_generation_deterministic
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_deterministic_placeholder_generation
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_integration_with_student_digital_twin
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_integration_with_educational_reasoning
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_integration_with_curriculum_retrieval
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_regression_ame001_and_ap001
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_tutor_does_not_invent_reasoning
FAILED tests/application/intelligent_tutor/test_intelligent_tutor.py::test_founder_tutor_diagnostics
FAILED tests/application/learning_graph/test_learning_graph.py::test_reasoning_pipeline_syncs_graph
FAILED tests/application/learning_graph/test_learning_graph.py::test_sdt001_sdt002_regression_with_graph
FAILED tests/application/reasoning/test_service.py::test_existing_reason_path_unaffected
FAILED tests/application/reasoning/test_twin_integration.py::test_existing_reason_path_regression
FAILED tests/application/runtime_integration/test_ri002_verification.py::test_student_surfaces_route_through_runtime_integration_service
FAILED tests/application/session_experience/test_services.py::test_reflection_summary_complete_flow
FAILED tests/application/session_experience/test_services.py::test_end_to_end_session_lifecycle
FAILED tests/application/student_digital_twin/test_student_digital_twin.py::test_mastery_and_learning_state_updates
FAILED tests/application/student_digital_twin/test_student_digital_twin.py::test_recommendation_and_prediction_scaffolding
FAILED tests/application/student_digital_twin/test_student_digital_twin.py::test_persistence_round_trip
FAILED tests/application/student_digital_twin/test_student_digital_twin.py::test_curriculum_retrieval_integration_contract
FAILED tests/application/student_digital_twin/test_student_digital_twin.py::test_founder_diagnostics_endpoints
FAILED tests/application/student_digital_twin/test_student_digital_twin.py::test_observations_never_overwritten_on_reasoning
FAILED tests/application/student_experience/test_independence.py::test_application_no_forbidden_imports
FAILED tests/application/unified_journey/test_session_outcome.py::test_assemble_session_outcome_after_complete
FAILED tests/certification/test_pr001b_student_pilot.py::TestFirstDayExperience::test_home_shows_mission_and_clarity
FAILED tests/certification/test_pr001b_student_pilot.py::TestFirstDayExperience::test_complete_mission_updates_progress
FAILED tests/certification/test_pr001b_student_pilot.py::TestInterruptedAndMissedDay::test_interrupted_session_keeps_same_mission
FAILED tests/certification/test_pr001b_student_pilot.py::TestConsecutiveSessionsAndMultipleMissions::test_next_day_advances_after_completion
FAILED tests/certification/test_pr001b_student_pilot.py::TestConsecutiveSessionsAndMultipleMissions::test_multiple_missions_across_days
FAILED tests/certification/test_pr001b_student_pilot.py::TestEducationalClarityAnswers::test_four_clarity_questions
FAILED tests/certification/test_pr001b_student_pilot.py::TestOperationalRecovery::test_duplicate_complete_is_recoverable
FAILED tests/certification/test_pr001b_student_pilot.py::TestOperationalRecovery::test_journey_shows_advancement_after_complete
FAILED tests/dashboard/test_educational_dashboard_integration.py::TestInternalAlphaDailyPath::test_alpha_env_renders_ei_card_with_real_composition
FAILED tests/domain/session_experience/test_entities.py::test_completion_readiness_label
FAILED tests/domain/session_experience/test_volume.py::test_completion_delta_labels[0.05-improved]
FAILED tests/domain/session_experience/test_volume.py::test_completion_delta_labels[-0.05-dipped]
FAILED tests/domain/session_experience/test_volume.py::test_completion_delta_labels[0.021-improved]
FAILED tests/domain/session_experience/test_volume.py::test_completion_delta_labels[-0.021-dipped]
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_page_header
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_mission_card
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_section
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_badge
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_timeline
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_buttons
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_achievement_and_statistic
FAILED tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_token_style_tag
FAILED tests/education_os/adapters/flask/rendering/test_token_rendering.py::test_style_renderer_maps_contract_to_css_vars
FAILED tests/education_os/adapters/flask/test_page_snapshots.py::test_page_regression_snapshots[/eos/dashboard/?student_id=student-ada-dashboard.html]
FAILED tests/education_os/adapters/flask/test_page_snapshots.py::test_page_regression_snapshots[/eos/mission/?student_id=student-ada-mission.html]
FAILED tests/education_os/adapters/flask/test_page_snapshots.py::test_page_regression_snapshots[/eos/session/?student_id=student-ada&session_id=snap-1-session.html]
FAILED tests/education_os/adapters/flask/test_page_snapshots.py::test_page_regression_snapshots[/eos/reflection/?student_id=student-ada&session_id=snap-1-reflection.html]
FAILED tests/infrastructure/adapters/adaptive_engine/test_assembler_integration.py::test_identical_runtime_a_state_produces_identical_bundles
FAILED tests/infrastructure/adapters/adaptive_engine/test_assembler_integration.py::test_assembled_bundle_reflects_runtime_a_facts
FAILED tests/infrastructure/adapters/adaptive_engine/test_assembler_integration.py::test_no_runtime_a_writes_during_assemble
FAILED tests/infrastructure/adapters/adaptive_engine/test_gate_integration.py::test_gate_does_not_mutate_runtime_a
FAILED tests/infrastructure/adapters/adaptive_engine/test_port_cutover_integration.py::test_runtime_a_unchanged_under_cutover
FAILED tests/infrastructure/adapters/adaptive_engine/test_shadow_integration.py::test_shadow_determinism_identical_runtime_a_snapshots
FAILED tests/infrastructure/adapters/adaptive_engine/test_shadow_integration.py::test_shadow_does_not_mutate_runtime_a
FAILED tests/infrastructure/adapters/adaptive_engine/test_soak_integration.py::test_soak_adaptive_path_does_not_mutate_runtime_a
FAILED tests/infrastructure/adapters/adaptive_engine/test_traceability_integration.py::test_assembler_and_executor_pipeline_still_deterministic
FAILED tests/infrastructure/adapters/digital_twin/test_explainability_integration.py::test_runtime_a_snapshot_explanations_are_deterministic
FAILED tests/infrastructure/adapters/digital_twin/test_facet_integration.py::test_identical_runtime_a_state_produces_identical_facets
FAILED tests/infrastructure/adapters/digital_twin/test_shadow_integration.py::test_shadow_pipeline_deterministic_for_learner
FAILED tests/infrastructure/adapters/digital_twin/test_shadow_integration.py::test_projection_stability_across_replays
FAILED tests/infrastructure/adapters/digital_twin/test_shadow_integration.py::test_long_running_replay_preserves_health_rates
FAILED tests/infrastructure/adapters/digital_twin/test_shadow_integration.py::test_shadow_does_not_influence_experience_home
FAILED tests/infrastructure/adapters/digital_twin/test_snapshot_integration.py::test_identical_runtime_a_state_produces_identical_snapshots
FAILED tests/infrastructure/adapters/digital_twin/test_snapshot_integration.py::test_build_from_bundle_matches_direct_build
FAILED tests/infrastructure/adapters/educational_runtime_bridge/test_journey_integration.py::test_composition_flag_off_preserves_seed_path
FAILED tests/infrastructure/adapters/educational_runtime_bridge/test_mission_read_integration.py::test_composition_flag_off_preserves_seed_path
FAILED tests/infrastructure/adapters/educational_runtime_bridge/test_recommendation_integration.py::test_composition_flag_off_preserves_seed_path
FAILED tests/infrastructure/authority/test_authority.py::test_adapters_do_not_import_flask_into_application_ports
FAILED tests/infrastructure/session/test_adapters.py::test_runtime_delegates_to_engine[sess-L0]
FAILED tests/infrastructure/session/test_adapters.py::test_runtime_delegates_to_engine[sess-L1]
FAILED tests/infrastructure/session/test_adapters.py::test_runtime_delegates_to_engine[sess-L2]
FAILED tests/infrastructure/session/test_adapters.py::test_runtime_delegates_to_engine[sess-L3]
FAILED tests/infrastructure/session/test_integration.py::test_facade_submit_advance_to_reflection[sess-L0]
FAILED tests/infrastructure/session/test_integration.py::test_facade_submit_advance_to_reflection[sess-L1]
FAILED tests/infrastructure/session/test_integration.py::test_facade_submit_advance_to_reflection[sess-L2]
FAILED tests/infrastructure/session/test_volume_matrix.py::test_composition_op_grid[complete-sess-L0]
FAILED tests/infrastructure/session/test_volume_matrix.py::test_composition_op_grid[complete-sess-L1]
FAILED tests/infrastructure/session/test_volume_matrix.py::test_composition_op_grid[complete-sess-L2]
FAILED tests/infrastructure/session/test_volume_matrix.py::test_composition_op_grid[complete-sess-L3]
FAILED tests/infrastructure/session/test_volume_matrix.py::test_composition_op_grid[complete-sess-L4]
FAILED tests/infrastructure/test_independence.py::test_application_does_not_import_infrastructure
FAILED tests/operational/test_alpha_configuration.py::test_alembic_head_and_migration_files
FAILED tests/presentation/session/test_commitment_completion_link.py::test_v2_session_finish_marks_commitment_completed
FAILED tests/presentation/session/test_commitment_completion_link.py::test_v2_session_finish_fails_open_without_commitment
FAILED tests/presentation/session/test_product_language.py::test_session_warning_flashes_guide_recovery[continue_contention]
FAILED tests/presentation/session/test_product_language.py::test_session_warning_flashes_guide_recovery[continue_retry]
FAILED tests/presentation/session/test_product_language.py::test_session_templates_avoid_study_session
FAILED tests/presentation/session/test_regression.py::test_full_http_session_flow
FAILED tests/presentation/session/test_routes.py::test_finish_returns_home - ...
FAILED tests/presentation/session/test_templates.py::test_presentation_does_not_import_engines
FAILED tests/presentation/student/test_cq004_session_substance.py::test_completion_vm_headline_uses_topic
FAILED tests/presentation/student/test_educational_timeline.py::TestEducationalTimelineRoute::test_history_links_to_timeline
FAILED tests/presentation/student/test_independence.py::test_no_forbidden_imports[path1]
FAILED tests/presentation/student/test_recommendation_trust_contract.py::test_tr_a01_schema_complete_home_binds_trust_mes_fields
FAILED tests/presentation/test_product_language_matrix.py::test_founder_ctas_documented[Generate preview]
FAILED tests/presentation/test_product_language_matrix.py::test_all_warning_flashes_offer_recovery[Your session is still open. Wait a moment, then try Continue again \u2014 this is a temporary hiccup, not a study failure.]
FAILED tests/presentation/workflows/test_workflow_session_resume.py::test_resume_then_complete
FAILED tests/presentation/workflows/test_workflow_volume_matrix.py::test_page_meta_step_counts[overview]
FAILED tests/presentation/workflows/test_workflow_volume_matrix.py::test_page_meta_step_counts[activity]
FAILED tests/presentation/workflows/test_workflow_volume_matrix.py::test_page_meta_step_counts[reflection]
FAILED tests/presentation/workflows/test_workflow_volume_matrix.py::test_page_meta_step_counts[summary]
FAILED tests/presentation/workflows/test_workflow_volume_matrix.py::test_page_meta_step_counts[complete]
FAILED tests/test_alpha_001_infrastructure.py::TestAlphaOnboarding::test_onboarding_page_explains_core_concepts
FAILED tests/test_alpha_001_infrastructure.py::TestPresentationTelemetry::test_allowed_events_match_alpha_contract
FAILED tests/test_bi001_brand_identity.py::TestBrandThemeTokens::test_app_css_uses_official_primary_and_gold
FAILED tests/test_bi001_brand_identity.py::TestStudentShellBrandChrome::test_eos_shell_active_nav_uses_brand_tokens
FAILED tests/test_dx006b_choose_exam.py::test_confirm_is_begin_learning_only
FAILED tests/test_dx006b_study_session.py::test_overview_page_has_start_primary
FAILED tests/test_dx006b_study_session.py::test_reflection_and_complete_primaries
FAILED tests/test_dx006b_study_session.py::test_overview_template_structure
FAILED tests/test_eip006_version1_educational_state_refinement.py::TestNegativeNoUnsupportedMasteryClaims::test_coverage_completion_does_not_mint_estimated_knowledge
FAILED tests/test_eip006_version1_educational_state_refinement.py::TestPositiveVersion1EducationalStates::test_evidence_gates_estimated_knowledge_alias
FAILED tests/test_ev001b_evidence_gate.py::TestAcceptanceGEvidence::test_mark_complete_blocked_when_gate_on
FAILED tests/test_ia002_study_plan_state_synchronization.py::TestStudyPlanStateSynchronization::test_switch_cs1_to_cm1_updates_immediately
FAILED tests/test_ia002_study_plan_state_synchronization.py::TestStudyPlanStateSynchronization::test_back_and_forth_preserves_plan_missions
FAILED tests/test_iahf004a_brand_infrastructure.py::TestBrandTemplateWiring::test_brand_meta_partial_standardises_identity
FAILED tests/test_iahf005_static_asset_versioning.py::TestTemplateVersionedStaticWiring::test_brand_meta_still_references_canonical_assets
FAILED tests/test_kwp011_educational_memory.py::TestProductSurfaces::test_history_bridge_to_journey
FAILED tests/test_lxp003_session_product.py::TestPersistenceAndRecovery::test_silent_complete_rejected_when_required
FAILED tests/test_lxp003_session_product.py::TestAcceptanceHttp::test_pause_resume_finish_review_flow
FAILED tests/test_lxp003_session_product.py::TestAcceptanceHttp::test_flag_off_allows_complete_without_review
FAILED tests/test_lxp004a_session_substance.py::TestRuntimeSubstanceProjection::test_overview_and_reflection_when_substance_on
FAILED tests/test_mission002_briefing_coherence.py::test_integration_mission_matches_progress_and_home_why
FAILED tests/test_mission002_briefing_coherence.py::test_integration_mid_progress_coherence
FAILED tests/test_ptp001_supported_subject_integrity.py::TestNoHollowPlans::test_review_post_refuses_coming_soon
FAILED tests/test_qs001_ptp005_cohesion.py::TestOnboardingDedup::test_begin_learning_does_not_collect_completed_topics
FAILED tests/test_rip001_daily_checkin.py::TestCheckinHttpFlow::test_invitation_on_session_recorded
FAILED tests/test_rip004_research_insight_engine.py::TestInsightEngineHttp::test_dashboard_shows_insight_panels
FAILED tests/test_routes.py::TestDashboardRoute::test_dashboard_unsupported_exam_no_error
FAILED tests/test_routes.py::TestStudyPlanManagementRoutes::test_set_active_plan_post
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_wizard_step_2_post
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_wizard_step_3_post_redirects_to_baseline
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_baseline_experience_renders
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_create_study_plan_succeeds
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_exactly_one_study_plan_created
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_week_plans_generated
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_topic_progress_created_for_curriculum_backed_exam
FAILED tests/test_smoke.py::TestSmokeStudyPlanWizard::test_no_500_during_wizard
FAILED tests/test_smoke.py::TestSmokeDashboard::test_dashboard_after_plan_creation
FAILED tests/test_smoke.py::TestSmokeDashboard::test_curriculum_progress_section
FAILED tests/test_smoke.py::TestSmokeDashboard::test_readiness_section - Asse...
FAILED tests/test_smoke.py::TestSmokeDashboard::test_time_status_section - As...
FAILED tests/test_smoke.py::TestSmokeDashboard::test_todays_mission_section
FAILED tests/test_smoke.py::TestSmokeDashboard::test_no_exceptions_on_dashboard
FAILED tests/test_smoke.py::TestSmokeMission::test_mission_page_returns_200
FAILED tests/test_smoke.py::TestSmokeMission::test_mission_hero_renders - Ass...
FAILED tests/test_smoke.py::TestSmokeMission::test_progress_bar_renders - Ass...
FAILED tests/test_smoke.py::TestSmokeMission::test_task_checklist_renders - A...
FAILED tests/test_smoke.py::TestSmokeMission::test_no_exceptions_on_mission
FAILED tests/test_smoke.py::TestSmokeStudyPlanPage::test_study_plan_page_returns_200
FAILED tests/test_smoke.py::TestSmokeStudyPlanPage::test_roadmap_renders - As...
FAILED tests/test_smoke.py::TestSmokeStudyPlanPage::test_curriculum_topics_render
FAILED tests/test_smoke.py::TestSmokeStudyPlanPage::test_status_badges_render
FAILED tests/test_smoke.py::TestSmokeStudyPlanPage::test_no_exceptions_on_study_plan
FAILED tests/test_smoke.py::TestSmokeExport::test_backup_export_returns_200
FAILED tests/test_smoke.py::TestSmokeExport::test_backup_contains_expected_sections
FAILED tests/test_smoke.py::TestSmokeExport::test_backup_includes_study_plan_data
FAILED tests/test_smoke.py::TestSmokeExport::test_no_exceptions_on_backup - A...
FAILED tests/test_smoke.py::TestSmokeAnalytics::test_analytics_returns_200 - ...
FAILED tests/test_smoke.py::TestSmokeAnalytics::test_analytics_empty_state_or_dashboard
FAILED tests/test_smoke.py::TestSmokeAnalytics::test_no_exceptions_on_analytics
FAILED tests/test_smoke.py::TestSmokeStudyPlanLifecycle::test_complete_lifecycle
FAILED tests/test_smoke.py::TestFullEndToEnd::test_complete_user_journey - As...
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_returns_none_when_no_curriculum_id
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_returns_none_when_no_curriculum_version
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_returns_none_when_curriculum_not_loadable
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_returns_none_when_exam_name_unparseable
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_no_completed_topics_all_hours_remaining
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_some_completed_topics
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_all_topics_completed
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_available_study_hours_calculation
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_available_study_hours_weighted_average
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_exam_in_past_available_hours_zero
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_exam_today_available_hours_zero
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_surplus_when_available_exceeds_remaining
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_deficit_when_remaining_exceeds_available
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_deterministic_same_input_same_output
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_handles_datetime_exam_date
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_different_user_sees_only_their_progress
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_values_are_rounded_to_two_decimals
FAILED tests/test_time_engine.py::TestCalculateTimeSummary::test_result_is_time_summary_type
FAILED tests/test_v1s002_curriculum_authority_cutover.py::test_v1_readiness_snapshot_includes_ownership_sections
FAILED tests/test_v1s003_repository_health.py::test_every_application_package_is_registered
FAILED tests/test_v1s003_repository_health.py::test_v1_readiness_snapshot_includes_repository_health
FAILED tests/test_v1s004_dogfood_validation.py::test_v1_readiness_snapshot_includes_dogfood_sections
FAILED tests/test_v1sp001a_learning_lifecycle.py::TestRevisionMissions::test_revision_mission_never_restarts_topic_one
FAILED tests/test_v1sp001c_operational_health.py::TestOperationalHealthPermissions::test_nav_includes_operational_health
FAILED tests/test_v1sp001e_information_architecture.py::TestV1sp001eProgressiveDisclosure::test_dashboard_uses_help_patterns
FAILED tests/test_v1sp003_performance.py::TestQueryBudgets::test_overall_readiness_batches_leaf_progress
FAILED tests/test_v1sp003_performance.py::TestStaticAssetsOptimised::test_first_party_css_js_under_budget
```

---

## Appendix B — Collection commands (audit trail)

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git log -1 --format='%H%n%ci%n%s'
git describe --tags --abbrev=0
git tag --sort=-creatordate | head
git log --since='30 days ago' --oneline | wc -l
git log -50 --oneline --format='%h %ad %s' --date=short
.venv/bin/python -m pytest tests/ --tb=line -q
.venv/bin/python -m pytest tests/architecture/ -q --tb=line
ruff check app/ tests/
curl -sS "https://api.github.com/repos/Michael-Burn/Kwalitec/actions/runs?branch=main&per_page=…"
# flag resolution via resolve_v2_feature_flags / resolve_analytics_feature_flag
```

---

*End of CURSOR_CURRENT_STATE_REPORT_2026-08-24.*
