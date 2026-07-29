# RUNTIME_CERTIFICATION.md

**Programme:** RC-001  
**Release Candidate ID:** `RC-2026.07.29-01`  
**Recorded at (UTC):** `2026-07-28T23:04:14Z` (process start)

---

## Recorded values

| Field | Value | Evidence |
|---|---|---|
| Python version | `3.14.6` (Clang 21.0.0) | `.venv/bin/python -c "import sys; print(sys.version)"` |
| Flask version | `3.1.0` | `importlib.metadata.version("flask")` |
| Active configuration | `DevelopmentConfig` (`APP_ENV=development`, `FLASK_ENV=development`) | `_evidence/runtime/flask.log` |
| Debug mode | **off** | Log line: `* Debug mode: off` |
| Reload mode | **off** | Started with `--no-reload --no-debugger` |
| Process start timestamp | `2026-07-28T23:04:14Z` | `_evidence/runtime/start_meta.txt` |
| Process PID | `83805` | `_evidence/runtime/pid.txt` |
| Base URL | `http://127.0.0.1:5201` | Listener + health probe |
| Active port | `5201` | `lsof -nP -iTCP:5201 -sTCP:LISTEN` |

### Start command (exact)

```bash
DATABASE_URL=sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3 \
DOCUMENT_STORAGE_ROOT=/tmp/rc001_RC-2026.07.29-01_documents \
FLASK_APP=run.py \
APP_ENV=development \
FLASK_ENV=development \
.venv/bin/flask --app run.py run --host 127.0.0.1 --port 5201 --no-reload --no-debugger
```

### Health snapshot (at certification)

From `GET /health` → `_evidence/runtime/health.json`:

| Field | Value |
|---|---|
| `status` | `ok` |
| `version` | `2.0.0` |
| `environment` | `development` |
| `build_number` | `local` |
| `build_date` | `2026-07-28` |
| `commit` | `null` (env `KWALITEC_GIT_COMMIT` unset) |
| migrations current/head | `202607280080` / `202607280080` |

Full fingerprint: `_evidence/runtime/env_fingerprint.json`

---

## Orphan / stale process audit

Listeners present at certification (not used for this RC):

| Port | PID | Role vs RC |
|---|---|---|
| `5001` | 73692 / 94648 | Unrelated — **not** RC |
| `5055` | 77122 | Unrelated — **not** RC |
| `5128` | 17666 | Unrelated — **not** RC |
| `5130` | 56789 | Known EV-002 stale FV process — **not** RC |
| **`5201`** | **83805** | **RC-2026.07.29-01 runtime** |

RC certification binds exclusively to **`http://127.0.0.1:5201`**. Other listeners must not be used by subsequent validation programmes.

---

## Verification

| Check | Result | Notes |
|---|---|---|
| Runtime started after latest implementation | **PASS** | Key PI-002R file mtimes (UTC): validation `2026-07-28T22:27:18Z`, routes `2026-07-28T22:27:28Z`, preview `2026-07-28T22:28:34Z`. Process start `2026-07-28T23:04:14Z` (≥ all). |
| No orphan processes serving stale RC code | **PASS** | Fresh PID `83805` on dedicated port `5201`; `--no-reload` so import graph frozen at start |

---

## Binding rule for subsequent programmes

Every validation walk JSON / report for this RC **must** record:

- `base`: `http://127.0.0.1:5201`
- `process_pid`: `83805` (or a restarted process that re-certifies under a **new** RC ID)
- `process_start_timestamp_utc`

Restarting the process without a new RC certification **invalidates** this Release Candidate (EV-002 class failure).
