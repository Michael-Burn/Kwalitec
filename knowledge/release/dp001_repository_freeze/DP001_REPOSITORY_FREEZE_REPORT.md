# DP-001 — Repository Freeze Report

**Programme:** Production Deployment  
**Phase:** Repository Freeze (RELEASE PREPARATION)  
**Date:** 2026-07-29  
**Certification baseline:** CQ-008B — **COMMERCIAL READY WITH MINOR CONDITIONS**  
**Git HEAD at audit:** `ecb1bfd` (`fix(ui): polish public sign-in layout and compact footer chrome`)  
**Branch:** `feature/ap-002-assessment-engine`

---

## Executive Summary

DP-001 cleaned local temporary artefacts and audited the repository for release preparation. **No application behaviour was changed** (no product code edits, no commits, no tags, no pushes).

The freeze **does not** meet the success criteria for advancing to DP-002. The working tree still contains the full uncommitted CQ-008B-era product delta; the standard regression suite reports **88 failures**; and the release identity is not yet a clean, committed snapshot of the certified product.

**Verdict: NOT READY for DP-002.**

---

## Repository Status

| Check | Result |
|-------|--------|
| Current branch | `feature/ap-002-assessment-engine` |
| Tracking | `origin/feature/ap-002-assessment-engine` (**ahead by 153 commits**) |
| Working tree | **Dirty** — ~85 porcelain entries (modified / deleted / untracked) |
| Temporary caches | Removed under DP-001 (see below) |
| Secrets in git index | None detected for `.env`, credentials, or SQLite DBs |
| Dependency pins | `requirements.txt` matches local `.venv` (39 pins) |
| Node package manifests | None (no `package.json`) |
| Alembic head | Single head `202607280080` (LP-001 learner lifecycle) |
| Local DB vs head | Up to date (`flask db` reported current = head) |
| Regression suite | **88 failed**, 44 737 passed, 7 skipped (~5m 13s) |

Other local branches observed (not used for this freeze): `main`, `chore/eng-001-engineering-standards`, `feature/cip-003-retrieval`, `feature/educational-architecture-consolidation`, `feature/sdt-001-foundation`, `post-v1-development`.

---

## Temporary Files Removed

Only clearly temporary / regenerable artefacts were deleted:

| Artefact | Approx. volume |
|----------|----------------|
| `__pycache__/` directories (excluding `.venv`) | **804** directories removed |
| `.pytest_cache/` | Removed |
| `.ruff_cache/` | Removed |
| `.coverage` | Removed |
| `.DS_Store` | Removed (repo tree) |

Not present at cleanup time (nothing to remove): `htmlcov/`, `playwright-report/`, `test-results/`, `test-output/`, `.mypy_cache/`.

**Note:** Running the regression suite regenerates `__pycache__` and may recreate `.pytest_cache`. These remain gitignored and are not part of the release snapshot.

---

## Items Preserved

Intentionally **not** deleted:

- All `knowledge/` engineering reports, product certification packs, and `_evidence/` screenshots (including CQ-008B, FV-001*, RC/EE/EV/PI programmes, browser acceptance evidence)
- Application source, templates, static assets, and tests (including uncommitted certified-product WIP)
- Tracked branding binaries under `app/static/`
- Local-only (gitignored) runtime data: `.env`, `instance/*.sqlite3`, `instance/curriculum_documents/`, ops `*.local.*` files, `.alpha_participant_credentials.txt`
- `.venv/`
- Tracked historical `imports.log` (see Outstanding Changes — recommend removal in a later release hygiene commit, **not** done here without commit authority)

---

## Git Status

```
On branch feature/ap-002-assessment-engine
Your branch is ahead of 'origin/feature/ap-002-assessment-engine' by 153 commits.
```

Porcelain summary at freeze time:

- **~46** modified paths
- **3** deleted paths (`legacy_workspace.html`, `partials/sidebar.html`, `partials/topnav.html`)
- **~36** untracked paths/directories (application modules, tests, and large `knowledge/` packs)

No files were staged. No commit was created.

---

## Outstanding Changes

Uncommitted work that appears to constitute the **CQ-008B certified product delta** (must be deliberately committed in a later release-prep step — **out of DP-001 scope**):

### Application / presentation (modified or new)

- Curriculum Studio: upload / preview / publication / validation / workspace services; `structure_preparation_service.py`; publication bridge; operator guidance; studio templates & JS
- Student experience: home / profile / navigation / view models / CSS tokens; `examination_identity.py`; shell unification (EOS student layout; removal of legacy workspace / sidebar / topnav)
- Related tests under `tests/application/`, `tests/presentation/`, and top-level UI regression tests

### Knowledge / certification (untracked — preserve)

- `knowledge/product/cq008_premium_product_certification/`
- `knowledge/engineering/rc20260729_03_student_shell_unification/` … `rc20260729_06_*`
- `knowledge/engineering/{ee001,ev001,ev002,pi002,pi002r}_*`
- Founder / student validation packs (`fv001*`, `px001`, `px002`, release `cq007` / `rc001`)

### Release blockers relative to “clean working tree”

1. Working tree is **not** clean.
2. Certified product changes are **not** fully represented by a single committed revision.
3. Remote tracking branch is **153 commits behind** local HEAD (push is out of scope for DP-001, but reproducibility for others requires a published tip).

---

## Dependency Audit

| Item | Status |
|------|--------|
| `requirements.txt` | Present; 39 pinned packages |
| Installed `.venv` vs pins | **Match** — 0 missing, 0 version mismatches |
| Notable runtime pins | Flask 3.1.0, SQLAlchemy 2.0.51, alembic 1.18.5, gunicorn 23.0.0, pytest 8.3.4, ruff 0.8.6, playwright 1.61.0, psycopg 3.2.13 |
| Node / npm | No package manifests — N/A |
| Dependency changes required | **None** (audit only) |

Inconsistency notes (report only):

- Some regression tests still **hard-code** Alembic head `202607270013` while the live head is `202607280080` (see Regression Results). This is a test-pin drift, not a packaging inconsistency.

---

## Migration Audit

| Item | Status |
|------|--------|
| Migration scripts under `migrations/versions/` | 51 Python revisions |
| Alembic / Flask-Migrate head | **`202607280080`** (single head) |
| Local SQLite (`flask db` startup check) | current = head (up to date) |
| Config | `migrations/alembic.ini` + Flask-Migrate integration |
| Schema changes in DP-001 | **None** |

Filename chronology includes older-dated revisions (e.g. `20260907*`, `20261007*`, `20261112*`) that sit **below** the merged head in the Alembic graph; this is historical graph shape, not multiple heads.

---

## Security Observations

| Finding | Severity | Notes |
|---------|----------|-------|
| `.env` present locally | Expected | Gitignored; not in index |
| `.alpha_participant_credentials.txt` | Expected | Gitignored |
| `ops/STAGE1_CREDENTIALS.local.txt`, `ops/STAGE1_PILOT_MAP.local.md` | Expected | Gitignored per `.gitignore` Stage 1 PII rules |
| `instance/*.sqlite3` and backups | Expected | Gitignored local DBs / harness outputs |
| Tracked secrets / API keys / PEM / AWS keys in index | **None found** | Pattern scan of tracked suspicious names empty |
| `.env.example` | Safe placeholders | `SECRET_KEY=change-this-secret-key`, example admin credentials |
| Absolute machine paths | Low (docs/evidence) | Appear in some evidence JSON/Markdown (`/Users/kwalitec/...`) and a few historical `TEST_EVIDENCE_RAW.txt` files — not runtime config |
| Debug configuration | Local only | App factory logs DEBUG when `app.debug`; production must set strong `SECRET_KEY` and non-development `APP_ENV` (enforced in factory) |
| Unnecessary tracked binaries | Branding assets only | Expected product assets under `app/static/assets/branding/` |
| Tracked `imports.log` | Hygiene | Import-timing debug log committed historically — should not ship as product signal |

**No secrets were committed during DP-001.** Local secret files were left in place (required for local operation) and remain ignored.

---

## Regression Results

Command (per `CONTRIBUTING.md` / `pyproject.toml`):

```bash
python -m pytest tests/ -v
```

(Executed via `.venv/bin/python -m pytest tests/ -v --tb=line`.)

| Metric | Value |
|--------|-------|
| Passed | **44 737** |
| Failed | **88** |
| Skipped | **7** |
| Warnings | 67 334 |
| Duration | 312.67s (~5m 13s) |

### Failure clusters (not exhaustive node IDs)

1. **Alembic head pin drift** — tests still expect `202607270013`; live head is `202607280080`.
2. **Student Home / shell contract drift** — missing legacy markers (`data-educational-experience="runtime-c"`, welcome modal id, CSS class names such as `.student-hero` / `.student-session-next`); Jinja `UndefinedError: 'home'/'study' is undefined` in older presentation contracts.
3. **EOS Design System snapshots / tokens** — intentional-looking snapshot drift after token/CSS updates (`--space-sm` vs `--space-md`, page HTML snapshots).
4. **Layering / independence guards** — `examination_identity.py` imports `app.services.study_plan_service`; `enrolment_bridge.py` flagged for infrastructure / Flask boundary imports.
5. **Product language / copy** — Session wording, readiness delta labels (`improved`/`dipped` vs softer copy), onboarding step counts, “Study Sensei” documentation matrix.
6. **Curriculum Studio certification path** — at least one founder validation workspace assertion expecting “Validation” copy on an unexpected page title path.

These failures are **pre-existing relative to the uncommitted certified-product working tree**; DP-001 did not modify product code to fix them.

---

## Release Readiness

| Success criterion | Met? |
|-------------------|------|
| Clean working tree | **No** |
| No temporary artefacts (caches cleaned) | **Yes** (gitignored caches removed; suite may regenerate) |
| No secrets in repository index | **Yes** |
| No unintended tracked temp files newly introduced | **Yes** (historical `imports.log` remains) |
| Tests passing | **No** (88 failures) |
| Repository reproducible as certified product tip | **No** (unclean tree + unpushed/uncommitted delta) |
| Ready for Production Database Reset (DP-002) | **No** |

Application behaviour was not altered by this phase.

---

## Recommendation

1. **Do not start DP-002** until the certified product working tree is intentionally frozen into git (commit scope decided by release owners — **not performed in DP-001**).
2. Resolve or explicitly waive the **88** regression failures so the release tip has a green (or formally excepted) suite.
3. Align Alembic head pin tests with `202607280080`.
4. Publish / align remote tip if other environments must reproduce the freeze (push remains out of DP-001).
5. Keep local `.env` / ops credentials out of git; rotate any credentials that may have been shared outside this machine before production cutover.
6. Optionally remove tracked `imports.log` in a hygiene commit.

---

## Decision

# NOT READY

**READY FOR DP-002:** No.

DP-001 completed its **audit + temporary cleanup** mandate. The repository is **not** yet a clean, reproducible release snapshot of the CQ-008B-certified product.
