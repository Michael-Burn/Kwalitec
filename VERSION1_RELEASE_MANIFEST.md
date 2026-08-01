# VERSION1_RELEASE_MANIFEST.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Document type:** Release Manifest (Release Candidate)  
**Date:** 2026-08-01  
**Status:** **GO** — Sprint C deploy + fingerprint + smoke complete on LIVE

---

## Identity

| Field | Value |
|-------|-------|
| **Product** | Kwalitec |
| **Application Version** | `2.0.0-beta.1` (from `VERSION`, `pyproject.toml`, `app.version.APP_VERSION`) |
| **Release Candidate** | **VERSION1-RC2** (stabilization sprint name) |
| **Manifest status** | Authoritative tip deployed + smoked; RC **GO** |
| **Prior related tag** | `v2.0.0-beta.1` (Private Beta RC lineage) |
| **Do not confuse with** | Historical tag `v1.0.0-rc2` @ `f2cbdc5` / lightweight `VERSION1-RC2` (older tips) |

---

## Git

| Field | Value |
|-------|-------|
| **Branch** | `main` |
| **Intended RC Git Commit** | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` |
| **Git Tag** | `v2.0.0-beta.1-rc2` (annotated) |
| **Tag timestamp (UTC)** | Retagged at Sprint C fix cut (session advance persistence) |
| **Commit timestamp** | `2026-08-01` (local) — `fix(session): persist activity explanation after answer for Continue` |
| **Working tree at tag** | Clean at tip cut |
| **origin/main** | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` |
| **Build fingerprint** | `2.0.0-beta.1` + `v2.0.0-beta.1-rc2` + `0d3fc72137ba0ea51d1baa522c52aa526cf04438` + alembic `202607310002` |

---

## Database / migrations

| Field | Value |
|-------|-------|
| **Alembic script head** | `202607310002` |
| **LIVE database revision** | `202607310002` (`current=head`) |
| **Database Version (logical)** | PostgreSQL via Render `kwalitec-db` |
| **Migrations in RC tip** | None new (chain unchanged) |

---

## Deployment

| Field | Value |
|-------|-------|
| **Deployment URL** | https://kwalitec.onrender.com |
| **Render service** | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| **Build command** | `pip install -r requirements.txt` |
| **Release command** | `flask db upgrade` |
| **Start command** | `waitress-serve --port=$PORT wsgi:app` |
| **Currently deployed commit** | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` |
| **Authoritative deploy ID** | `dep-d9mr7o6417fc73c1o9h0` |
| **Deploy created (UTC)** | `2026-08-01T08:52:48.377225Z` |
| **LIVE fingerprint confirmed (UTC)** | `2026-08-01T08:55:02Z` |
| **Build Date (LIVE sample)** | `2026-08-01` |
| **Build Number (LIVE sample)** | `local` |

---

## Educational inventory (intended vs LIVE)

| Item | Intended (tagged tip `0d3fc72`) | On LIVE `0d3fc72` |
|------|----------------------------------|-------------------|
| EF version | EF-001 FROZEN | Deployed with tip |
| Volume CS1-001 | `publication_ready` | Same (not student-released) |
| Volume CS1-002 | `publication_ready` | Same (not student-released) |
| Campaign Alpha | in Git under `educational_campaigns/` | On tip filesystem |
| Campaign Beta | in Git | On tip filesystem |
| EA-006 4.2 package | in Git + loader module | On tip |

---

## Known Issues

Canonical register: `KNOWN_ISSUES_RC2.md`. Final board: `RC2_FINAL_RELEASE_REPORT.md`.

| Issue | Sprint C status |
|-------|-----------------|
| KI-C1 Repository hygiene | **CLOSED** |
| KI-C2 Release fingerprint (LIVE match) | **CLOSED** |
| KI-C3 EV-001 educational trust | **CLOSED** for consistency objectives on LIVE fresh account |
| KI-C4 RR-001 smoke / session completion | **CLOSED** |

---

## Rollback procedure

1. On Render, manually redeploy the last known-good tagged commit (previous production tip `613722c` / tag lineage `v2.0.0-beta.1` as applicable).  
2. If the failed deploy advanced schema beyond backup compatibility, restore the pre-deploy PostgreSQL snapshot — do not rely on casual `alembic downgrade` in production.  
3. Verify `/health/live`, `/health/ready`, and `/health.commit` match the rollback tip.  
4. Re-run Founder login smoke.  
5. Record the rollback in ops notes and update this manifest’s deployed commit field.

---

## Approvals

| Role | Name / capacity | Status |
|------|-----------------|--------|
| Release Engineering | Sprint C deploy + fingerprint + smoke | **Complete** — RC **GO** |
| Founder / Educational Gate Owner | Required for educational GO beyond RC | **Pending** for PB-001 / volume release |
| Publication Approver | Required for Volume `approved`→`released` | **Pending** (volumes still `publication_ready`) |
| RR-001 gate | Re-issue against this tip | See `RC2_FINAL_RELEASE_REPORT.md` — RC GO; PB-001 volume path still gated |

---

## Release notes

| Item | Path / note |
|------|-------------|
| Current shipped baseline notes | `CHANGELOG.md` § `[2.0.0-beta.1]` |
| This RC notes | `CHANGELOG.md` § `[2.0.0-beta.1-rc2]` |
| Final board | `RC2_FINAL_RELEASE_REPORT.md` |

---

## Fingerprint block

```
Application Version: 2.0.0-beta.1
Release Candidate:   VERSION1-RC2
Git Commit:          0d3fc72137ba0ea51d1baa522c52aa526cf04438
Git Tag:             v2.0.0-beta.1-rc2
Migration Head:      202607310002
Deployment URL:      https://kwalitec.onrender.com
/health.commit:      0d3fc72137ba0ea51d1baa522c52aa526cf04438
Build Date:          2026-08-01
Deploy ID:           dep-d9mr7o6417fc73c1o9h0
Decision:            GO
```

**Current decision:** **GO** for VERSION1-RC2 Release Candidate — see `RC2_FINAL_RELEASE_REPORT.md`.
