# VERSION1_RELEASE_MANIFEST.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Document type:** Release Manifest (candidate — **not yet GO**)  
**Date:** 2026-08-01  
**Status:** **RC TIP FINGERPRINTED** — Sprint A (hygiene + local fingerprint) complete; LIVE deploy Pending

---

## Identity

| Field | Value |
|-------|-------|
| **Product** | Kwalitec |
| **Application Version** | `2.0.0-beta.1` (from `VERSION`, `pyproject.toml`, `app.version.APP_VERSION`) |
| **Release Candidate** | **VERSION1-RC2** (stabilization sprint name) |
| **Manifest status** | Local RC tip cut; RR-001 still **NO-GO** until deploy + smoke + educational trust |
| **Prior related tag** | `v2.0.0-beta.1` (Private Beta RC lineage) |
| **Do not confuse with** | Historical tag `v1.0.0-rc2` @ `f2cbdc5` / lightweight `VERSION1-RC2` (older tips) |

---

## Git

| Field | Value |
|-------|-------|
| **Branch** | `main` |
| **Intended RC Git Commit** | `75c29d2b0017d7df44a0767ae0e428605151cd90` |
| **Git Tag** | `v2.0.0-beta.1-rc2` (annotated) |
| **Tag timestamp (UTC)** | `2026-08-01T08:25:15Z` |
| **Commit timestamp** | `2026-08-01 10:25:10 +0200` |
| **Working tree at tag** | Clean |
| **origin/main (at Sprint A close)** | `613722cffa16e6badbdb3a1161e4feaa35fd02db` — tip not yet pushed/deployed |
| **Build fingerprint** | `2.0.0-beta.1` + `v2.0.0-beta.1-rc2` + `75c29d2b0017d7df44a0767ae0e428605151cd90` + alembic `202607310002` |

---

## Database / migrations

| Field | Value |
|-------|-------|
| **Alembic script head** | `202607310002` |
| **LIVE database revision (RR-001)** | `202607310002` (`current=head`) |
| **Database Version (logical)** | PostgreSQL via Render `kwalitec-db` |
| **Migrations in RC tip** | None new (chain unchanged) |

---

## Deployment

| Field | Value |
|-------|-------|
| **Deployment URL** | https://kwalitec.onrender.com |
| **Render service** | `kwalitec` |
| **Build command** | `pip install -r requirements.txt` |
| **Release command** | `flask db upgrade` |
| **Start command** | `waitress-serve --port=$PORT wsgi:app` |
| **Currently deployed commit** | `613722cffa16e6badbdb3a1161e4feaa35fd02db` |
| **Deploy of intended RC tip** | **Pending** (Sprint A explicitly excludes deployment) |
| **Build Date (LIVE sample)** | Pending re-probe after deploy |
| **Build Number (LIVE sample)** | Pending |

---

## Educational inventory (intended vs LIVE)

| Item | Intended (tagged tip `75c29d2`) | On LIVE `613722c` |
|------|----------------------------------|-------------------|
| EF version | EF-001 FROZEN (in tip) | Freeze commit not deployed |
| Volume CS1-001 | `publication_ready` | Not student-released |
| Volume CS1-002 | `publication_ready` | Not student-released |
| Campaign Alpha | **in Git** under `educational_campaigns/` | Absent until deploy |
| Campaign Beta | **in Git** | Absent until deploy |
| EA-006 4.2 package | **in Git** + loader module | Absent until deploy |

---

## Known Issues

Canonical register: `KNOWN_ISSUES_RC2.md`.

| Issue | Sprint A status |
|-------|-----------------|
| KI-C1 Repository hygiene | **CLOSED** |
| KI-C2 Release fingerprint (local tip + tag) | **CLOSED** for local/authoritative tip; LIVE match **Pending** deploy |
| KI-C3 EV-001 educational trust | **OPEN** (out of Sprint A scope) |
| KI-C4 RR-001 smoke incomplete | **OPEN** (requires deploy) |

---

## Rollback procedure

1. On Render, manually redeploy the last known-good tagged commit (currently production tip `613722c` / tag lineage `v2.0.0-beta.1` as applicable).  
2. If the failed deploy advanced schema beyond backup compatibility, restore the pre-deploy PostgreSQL snapshot — do not rely on casual `alembic downgrade` in production.  
3. Verify `/health/live`, `/health/ready`, and `/health.commit` match the rollback tip.  
4. Re-run Founder login smoke.  
5. Record the rollback in ops notes and update this manifest’s deployed commit field.

---

## Approvals

| Role | Name / capacity | Status |
|------|-----------------|--------|
| Release Engineering | Sprint A hygiene + fingerprint | **Complete** for C1/C2 local tip |
| Founder / Educational Gate Owner | Required for educational GO | **Pending** |
| Publication Approver | Required for Volume `approved`→`released` | **Pending** (volumes still `publication_ready`) |
| RR-001 gate | — | **NO-GO** (`RR001_RELEASE_DECISION.md`) until deploy + smoke + trust |

---

## Release notes

| Item | Path / note |
|------|-------------|
| Current shipped baseline notes | `CHANGELOG.md` § `[2.0.0-beta.1]` |
| This RC notes | `CHANGELOG.md` § `[2.0.0-beta.1-rc2]` |
| Historical v1 RC2 notes | `docs/release/RELEASE_NOTES_v1.0.0-RC2.md` (different era) |

### Explicit non-goals of this RC tip (Sprint A)

- No LIVE deploy  
- No UI redesign  
- No Runtime/Twin/recommendation redesign  
- No EV-001 remediation  
- No new Educational Framework law beyond EF-001 stewardship  

---

## Fingerprint block

```
Application Version: 2.0.0-beta.1
Release Candidate:   VERSION1-RC2
Git Commit:          75c29d2b0017d7df44a0767ae0e428605151cd90
Git Tag:             v2.0.0-beta.1-rc2
Migration Head:      202607310002
Deployment URL:      https://kwalitec.onrender.com
/health.commit:      Pending (deploy not performed)
Build Date:          Pending
Decision:            NO-GO (C1/C2 local tip closed; C3/C4 + deploy remain)
```

**Current decision:** **NO-GO** for unconditional release — see `RC2_RELEASE_ACTION_PLAN.md` Priorities 3–5.
