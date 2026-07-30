# RELEASE MANIFEST — Version 2.0.0-beta.1

**Archive programme:** AR-001 · Historical Release Archive  
**Nature:** Immutable historical identity document  
**Do not edit** after archival seal (except clerical corrections recorded in AR-001 report).

---

## Identity

| Field | Value |
|---|---|
| **Version** | `2.0.0-beta.1` |
| **Release type** | Private Beta · Release Candidate (RC-001) |
| **Release date** | 2026-07-30 |
| **Product status at release** | Deployed for Private Beta |
| **Build label** | `beta.1` |
| **Student badge** | Private Beta |
| **Static fingerprint** | `2.0.0-beta.1-rc001` |

---

## Git

| Field | Value |
|---|---|
| **Git tag** | `v2.0.0-beta.1` |
| **Annotated tag commit** | `f6245f45fa8dbf1c972f28980d0279829b6b846b` |
| **Tag message** | Kwalitec v2.0.0-beta.1 — Private Beta Release Candidate (RC-001) |
| **Deployed release commit** | `7302bb7f955e4f2e8512d5af28ee258f34abbc00` |
| **Deploy commit subject** | `release(v2.0.0-beta.1): Private Beta release candidate (RC-001)` |
| **Post-deploy evidence commit** | `f6245f45fa8dbf1c972f28980d0279829b6b846b` (`docs(rc001): record Private Beta deployment evidence`) |
| **Git tree (tag)** | See `GIT_TREE_SHA.txt` |

**Note:** The annotated tag points at the RC-001 deployment-evidence documentation commit, which is one commit after the application release tip that Render deployed (`7302bb7…`). Both are part of the official `v2.0.0-beta.1` release lineage.

---

## Build & runtime

| Field | Value |
|---|---|
| **Build number / label** | `beta.1` |
| **Python (requires)** | `>=3.11` (`pyproject.toml`) |
| **Python (archive host measurement)** | 3.14.6 (local archive environment; production Render Python may differ within ≥3.11) |
| **WSGI server** | Waitress (`waitress-serve --port=$PORT wsgi:app`) |
| **Flask** | 3.1.0 |
| **Werkzeug** | 3.1.8 |
| **Jinja2** | 3.1.6 |

---

## Database

| Field | Value |
|---|---|
| **Database revision (Alembic head at release)** | `202607300005` |
| **Revision name** | `pb001_private_beta_validation` |
| **Pre-deploy stamp (production)** | `202607290001` |
| **Post-deploy stamp (production)** | `202607300005` (= head) |
| **RC additive revisions** | `202607300001` … `202607300005` |
| **Destructive upgrades in RC set** | None |

---

## Deployment

| Field | Value |
|---|---|
| **Host / Render URL** | https://kwalitec.onrender.com |
| **Render service** | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| **Deploy id (RC-001)** | `dep-d9lg6su7bikc7390572g` |
| **Environment** | `production` |
| **Database** | PostgreSQL (`kwalitec-db` via `DATABASE_URL`) |
| **releaseCommand** | `flask db upgrade` |
| **Feature flags (render.yaml)** | `KWALITEC_EI_INTERNAL_ALPHA=1`, `KWALITEC_V2_STUDENT_EXPERIENCE=1`, sole-runtime related flags per `render.yaml` |

---

## Major dependencies

Pinned from `requirements.txt` at release:

| Package | Version |
|---|---|
| Flask | 3.1.0 |
| Flask-Login | 0.6.3 |
| Flask-Migrate | 4.0.7 |
| Flask-SQLAlchemy | 3.1.1 |
| Flask-WTF | 1.2.2 |
| SQLAlchemy | 2.0.51 |
| alembic | 1.18.5 |
| WTForms | 3.2.1 |
| gunicorn | 23.0.0 |
| waitress | 3.0.2 |
| psycopg / psycopg-binary | 3.2.13 |
| argon2-cffi | 23.1.0 |
| pypdf | 6.14.2 |
| Pillow | 12.3.0 |
| python-dotenv | 1.0.1 |
| pytest | 8.3.4 |
| ruff | 0.8.6 |
| playwright | 1.61.0 |

Full pin set archived at `release/requirements.txt`.

---

## Repository statistics (at archive measurement)

Measured against the working tree contemporaneous with AR-001 archival (aligned to `v2.0.0-beta.1` product identity; see `VERSION_STATISTICS.md` for detail).

| Metric | Value |
|---|---|
| Commits reachable from tag | 261 |
| Application Python files (`app/`) | 2,041 |
| Application Python LOC (approx.) | ~319,600 |
| Test Python files (`tests/`) | 1,401 |
| Test Python LOC (approx.) | ~246,600 |
| HTML templates (`app/templates/`) | 99 |
| CSS files (`app/static/`) | 10 |
| JS files (`app/static/`) | 13 |
| Registered blueprints | 21 |
| Alembic revision files | 58 |
| SQLAlchemy `__tablename__` declarations | ~145 |
| Top contributors (tag history) | Michael Burn (219), Eidolon (41), Courage Shumba (1) |

---

## Authoritative evidence

| Artefact | Path |
|---|---|
| RC-001 Release Report | `reports/rc001/RC001_RELEASE_REPORT.md` |
| Release Certificate | `RELEASE_CERTIFICATE.md` (archive root) |
| Changelog | `release/CHANGELOG.md` |
| Release notes | `release/RELEASE_NOTES.md` |
| Private Beta guide | `release/PRIVATE_BETA_GUIDE.md` |

---

*Archived under AR-001 on 2026-07-30. Museum-quality snapshot — not a living design document.*
