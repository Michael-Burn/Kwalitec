# DATABASE_CERTIFICATION.md

**Programme:** RC-001  
**Release Candidate ID:** `RC-2026.07.29-01`  
**Recorded at (UTC):** `2026-07-28T23:04:00Z` (approx., post-migrate / pre-walk)

---

## Recorded values

| Field | Value | Evidence |
|---|---|---|
| `DATABASE_URL` | `sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3` | Process env + `_evidence/database/seed_state.json` |
| Database engine | SQLite (SQLAlchemy dialect `sqlite://`) | Startup log: `SQLAlchemy database driver prefix: sqlite://` |
| Database file/location | `/tmp/rc001_RC-2026.07.29-01.sqlite3` | Created for this RC; size **2 723 840** bytes at seed check |
| Alembic migration revision | `202607280080` | `flask db current` + `alembic_version` table |
| Migration head | `202607280080` | `flask db heads` / health migrations component |
| Seed state | Fresh RC: migrations applied + single admin user only | `_evidence/database/seed_state.json` |

### Document storage (isolated)

| Field | Value |
|---|---|
| `DOCUMENT_STORAGE_ROOT` | `/tmp/rc001_RC-2026.07.29-01_documents` |

Isolated from `instance/curriculum_documents/` historical artefacts.

### Seed contents (measured)

| Table / metric | Count |
|---|---|
| `users` | 1 (`ctshumba01@gmail.com` — admin bootstrap) |
| `studio_foundation_subjects` | 0 |
| `studio_foundation_documents` | 0 |
| `published_curriculum_packages` | 0 |
| `ckg_subjects` | 0 |
| `subjects` | 0 |
| CIP / CKG curriculum artefact tables sampled | 0 rows |

Logs:

- `_evidence/database/migrate.log`
- `_evidence/database/create_admin.log`
- `_evidence/database/current.log`
- `_evidence/database/seed_state.json`

---

## Verification

| Check | Result | Notes |
|---|---|---|
| Database created specifically for RC | **PASS** | New file `/tmp/rc001_RC-2026.07.29-01.sqlite3`; not `instance/kwalitec.sqlite3` |
| No historical Founder workspaces | **PASS** | Subjects UI: “No workspaces yet.”; `studio_foundation_subjects=0` |
| No historical publication artefacts | **PASS** | `published_curriculum_packages=0`; CKG publication tables empty |

---

## Binding rule

Subsequent validation programmes **must** use this `DATABASE_URL` (or an exact copy of this file taken before any programme writes).  
Using `instance/kwalitec.sqlite3` or any prior EV/FV database **invalidates** the Release Candidate for that programme.
