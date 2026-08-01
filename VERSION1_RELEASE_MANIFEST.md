# VERSION1_RELEASE_MANIFEST.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Document type:** Release Manifest (candidate — **not yet GO**)  
**Date:** 2026-08-01  
**Status:** **DRAFT / BLOCKED** — fields marked TBD until clean tip + deploy

---

## Identity

| Field | Value |
|-------|-------|
| **Product** | Kwalitec |
| **Application Version** | `2.0.0-beta.1` (from `VERSION`, `pyproject.toml`, `app.version.APP_VERSION`) |
| **Release Candidate** | **VERSION1-RC2** (stabilization sprint name) |
| **Manifest status** | Candidate blocked by RR-001 **NO-GO** |
| **Prior related tag** | `v2.0.0-beta.1` (Private Beta RC lineage) |
| **Do not confuse with** | Historical tag `v1.0.0-rc2` @ `f2cbdc5` (older Internal Alpha RC2) |

---

## Git

| Field | Value |
|-------|-------|
| **Branch** | `main` |
| **Local HEAD (now)** | `f066bcf989d51e658b92d22d172d955d1e1d3ece` — EF-001 freeze |
| **origin/main (now)** | `613722cffa16e6badbdb3a1161e4feaa35fd02db` |
| **Intended RC Git Commit** | **TBD** — must be clean tip after `REPOSITORY_AUDIT.md` keep-set commit |
| **Git Tag** | **TBD** — choose distinct name (recommend e.g. `v2.0.0-beta.1-rc2` or `v2.0.0-rc2` — **not** reuse `v1.0.0-rc2`) |
| **Working tree** | Dirty (see `REPOSITORY_AUDIT.md`) |

---

## Database / migrations

| Field | Value |
|-------|-------|
| **Alembic script head** | `202607310002` |
| **LIVE database revision (RR-001)** | `202607310002` (`current=head`) |
| **Database Version (logical)** | PostgreSQL via Render `kwalitec-db` |
| **Migrations in this dirty tree** | None new |

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
| **Deploy of intended RC tip** | **Not performed** |
| **Build Date (LIVE sample)** | `2026-08-01` (`/health.build_date`) |
| **Build Number (LIVE sample)** | `local` (improve via env) |

---

## Educational inventory (intended vs LIVE)

| Item | Intended (local disk / ops) | On LIVE `613722c` |
|------|-----------------------------|-------------------|
| EF version | EF-001 FROZEN (local HEAD/docs) | Freeze commit not deployed |
| Volume CS1-001 | `publication_ready` | Not student-released |
| Volume CS1-002 | `publication_ready` | Not student-released |
| Campaign Alpha | on disk, **untracked** | Absent from Git → absent from LIVE |
| Campaign Beta | on disk, **untracked** | Absent |
| EA-006 4.2 package | on disk, **untracked** | Module/JSON not in Git; LIVE still serves 4.2 sitting under prior pathway |

---

## Known Issues

Canonical register: `KNOWN_ISSUES_RC2.md`.

**GO-blocking (Critical):** KI-C1, KI-C2, KI-C3, KI-C4.

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
| Release Engineering | (operator) | Audit complete; **no GO recommend** |
| Founder / Educational Gate Owner | Required for educational GO | **Pending** |
| Publication Approver | Required for Volume `approved`→`released` | **Pending** (volumes still `publication_ready`) |
| RR-001 gate | — | **NO-GO** (`RR001_RELEASE_DECISION.md`) |

---

## Release notes (draft pointer)

| Item | Path / note |
|------|-------------|
| Current shipped baseline notes | `CHANGELOG.md` § `[2.0.0-beta.1]` |
| Historical v1 RC2 notes | `docs/release/RELEASE_NOTES_v1.0.0-RC2.md` (different era — do not treat as this tip) |
| This RC notes | **TBD** — add CHANGELOG section when tip SHA exists covering: EF-001 freeze, educational package loader + Campaign Alpha/Beta inventory commit, RR-001 gate artefacts, residual known issues |

### Intended user-visible themes (only if keep-set ships)

- Certified educational package pathway for authored topics (addresses placeholder substance where packages match).  
- Educational Framework Version 1 freeze under operational stewardship (governance).  
- Campaign Alpha / Beta catalogue inventory present in deployable tree (activation/`released` status still gated by ops).

### Explicit non-goals of this RC

- No UI redesign  
- No Runtime/Twin/recommendation redesign  
- No new Educational Framework law beyond EF-001 stewardship  

---

## Fingerprint block (fill on GO)

```
Application Version: 2.0.0-beta.1   (or bumped)
Release Candidate:   VERSION1-RC2
Git Commit:          ________________
Git Tag:             ________________
Migration Head:      202607310002     (confirm)
Deployment URL:      https://kwalitec.onrender.com
/health.commit:      ________________
Build Date:          ________________
Decision:            GO / NO-GO
```

**Current decision:** **NO-GO** — see `RC2_RELEASE_ACTION_PLAN.md`.
