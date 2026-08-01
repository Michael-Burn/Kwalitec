# RC2_INTEGRITY_REPORT.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Date:** 2026-08-01  
**Role:** Release Candidate integrity (reproducibility)  
**Sources:** `flask db heads`, `VERSION`, `pyproject.toml`, `app/version.py`, `requirements.txt`, `render.yaml`, `git status`, RR-001 reports, `tools/architecture_guardian.py`

---

## Verdict

**NOT RELEASE-CANDIDATE INTEGRITY CLEAN**

A reproducible RC tip cannot yet be cut: dirty tree, unpushed commit, educational inventory absent from Git, and LIVE/local fingerprint divergence. Alembic script head is singular and matches LIVE migrations — schema chain itself is not the primary blocker.

---

## 1. Git integrity

| Check | Result | Evidence |
|-------|--------|----------|
| Branch | `main` | `git status -sb` |
| Local HEAD | `f066bcf989d51e658b92d22d172d955d1e1d3ece` | EF-001 freeze |
| `origin/main` | `613722cffa16e6badbdb3a1161e4feaa35fd02db` | Matches LIVE (RR-001) |
| Ahead/behind | **Ahead 1**, behind 0 | Unpushed EF-001 |
| Working tree clean | **FAIL** | 10 modified + 117 untracked entries |
| Intended inventory in Git | **FAIL** | `git ls-files` campaign/package module counts = 0 (RR-001) |

**Blocks reproducible release:** Yes.

---

## 2. Migration chain / Alembic head

| Check | Result | Evidence |
|-------|--------|----------|
| `flask db heads` | **Single head** `202607310002` | Merge PB-001 + SB-001A |
| LIVE migrations (RR-001) | `current=head=202607310002` | `/health` components.migrations |
| Dirty-tree new migrations | **None** | No untracked `migrations/versions/*` |
| Local operator SQLite | **Behind head** | Startup log: db=`202607300004`, head=`202607310002` |
| Multiple heads | **No** (script directory) | `ScriptDirectory.get_heads() == ['202607310002']` |

Notes:

- Filename prefixes `202609*`, `202610*`, `202611*` appear in `flask db history` as **ancestors**, not orphaned heads. Naming is confusing but not a dual-head failure.
- Local SQLite lag is an **operator workstation** integrity issue, not a LIVE production mismatch.

**Blocks RC cut?** Does not block schema reproducibility of tip `613722c`/`f066bcf` lineage. Does require operator DB upgrade before trusting local RC verification.

---

## 3. Version consistency

| Source | Value |
|--------|-------|
| `VERSION` | `2.0.0-beta.1` |
| `pyproject.toml` `[project].version` | `2.0.0-beta.1` |
| `app/version.py` `_FALLBACK_VERSION` / `APP_VERSION` | `2.0.0-beta.1` |
| LIVE `/health.version` (RR-001) | `2.0.0-beta.1` |
| Annotated tag `v2.0.0-beta.1` | Exists |
| Tag `v1.0.0-rc2` | Exists at `f2cbdc5` — **different historical RC** |

| Issue | Severity |
|-------|----------|
| Application version still `2.0.0-beta.1` while sprint named VERSION1-RC2 | Naming collision risk with tag `v1.0.0-rc2` |
| LIVE `build_number` = `local` | Weak operator fingerprint (commit still present) |
| No new RC tag for this stabilization tip | Cannot claim immutable RC until tag cut after clean tip |

**Version triad (VERSION / pyproject / APP_VERSION):** internally consistent at `2.0.0-beta.1`.  
**Release identity for this sprint:** not yet assigned a new immutable tag.

---

## 4. Requirements / runtime config

| Check | Result | Evidence |
|-------|--------|----------|
| `requirements.txt` present | Yes (39 lines) | Pins Flask 3.1.0, waitress 3.0.2, psycopg 3.2.13, alembic 1.18.5 |
| Render `buildCommand` | `pip install -r requirements.txt` | `render.yaml` |
| Render `startCommand` | `waitress-serve --port=$PORT wsgi:app` | waitress pinned |
| `gunicorn` also pinned | Present but unused by `render.yaml` start | Harmless dual server pin |
| `.env.example` | Present | Documented in `docs/production/ENVIRONMENT.md` |
| Python CI | 3.13 in `.github/workflows/ci.yml`; project `requires-python >=3.11` | Compatible range |

**No requirements break detected** for the current committed tip. Uncommitted educational package module must be verified by tests after commit (see action plan).

---

## 5. Configuration / feature flags (Render blueprint)

From `render.yaml` (blueprint; dashboard may override):

| Key | Blueprint value |
|-----|-----------------|
| `APP_ENV` | `production` |
| `FLASK_APP` | `wsgi.py` |
| `SECRET_KEY` | `generateValue: true` |
| `DATABASE_URL` | from `kwalitec-db` |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | `sync: false` (dashboard) |
| `KWALITEC_V2_SOLE_RUNTIME` | `1` |
| `KWALITEC_COMMERCIAL_LOOP` | `1` |
| `KWALITEC_EI_INTERNAL_ALPHA` | `1` |
| `releaseCommand` | `flask db upgrade` |

Integrity note: operator `.env` lacked Render deploy API/hook at RR-001 — deploy is **manual dashboard** per Founder Deployment Guide.

---

## 6. Architecture / educational integrity signals

| Check | Result | Evidence |
|-------|--------|----------|
| Architecture Guardian overall | **40/100** with FAIL-class findings historically present | `python tools/architecture_guardian.py` |
| Blueprint separation | PASS | Guardian |
| Dirty-tree architecture redesign | Overlays only (EA-006 package prefer path) | Diffs sampled |
| Curriculum V1/V2 | Not altered in dirty tree migrations | No migration WIP |
| EF-001 freeze | Local HEAD declares freeze; not on LIVE | `f066bcf` vs `613722c` |

Guardian debt is **pre-existing** and not introduced solely by this WIP. Release Protocol still requires pytest/ruff green on the tip before GO — not re-run in this documentation sprint.

---

## 7. Reproducibility blockers (preventing RC)

1. Working tree not clean → tip SHA unstable.  
2. Educational campaigns/packages not in Git → cannot reproduce inventory on Render from commit alone.  
3. Local HEAD ≠ `origin/main` ≠ intended deployed tip.  
4. No immutable tag for this stabilization candidate.  
5. RR-001 smoke incomplete on intended tip (session completion not run).  
6. LIVE `build_number=local` weakens operator fingerprinting (commit remains authoritative).

---

## 8. What is already sound

- Single Alembic head aligned with LIVE.  
- Version string triad consistent at `2.0.0-beta.1`.  
- Render start/release/build commands coherent with requirements.  
- CI workflow exists for `main` (architecture + unit jobs).  
- LIVE process health was ok at RR-001 for tip `613722c`.

---

## Conclusion

Integrity for **cutting** a Version 1 RC2 candidate is blocked by repository hygiene and inventory commit gaps, not by a broken Alembic multi-head. Resolve `REPOSITORY_AUDIT.md` keep-set → push → tag → deploy fingerprint before claiming RC integrity.
