# Environment Comparison

**Programme:** EV-002  
**Question:** Did both executions use identical build, branch, migrations, flags, configuration, and adapters?

---

## Summary

| Dimension | Identical? | Evidence |
|---|---|---|
| Alembic revision | **Yes** | Both DBs at `202607280080` |
| Application tree (on disk) | **Yes at FV walk time** | Same working tree; no second checkout |
| **Loaded code image in process** | **No** | See process timeline below |
| Database | **No** | Dedicated vs instance default |
| Host / port | **No** | `:5141` vs `:5130` |
| Feature flags (explicit) | **Mostly** | Neither EV nohup nor FV `:5130` set full `KWALITEC_V2_*` suite; `.env` has `APP_ENV` + `KWALITEC_EI_INTERNAL_ALPHA` |
| Adapters | Same modules on disk; **different process import time** | Stale process vs fresh process |

**Overall:** environments were **not identical**. Migrations matched; runtime configuration and process code image did not.

---

## Process timeline (UTC)

| Time (UTC) | Event |
|---|---|
| 22:00:01 | `structure_preparation_service.py` mtime (local 00:00:01 CEST) |
| **22:04:44** | **FV port 5130 server started** — `flask --app wsgi.py run --port 5130` (terminal `986439`, pid 56781 / listener 56789). Log: **“Using local SQLite database (DATABASE_URL is not set)”**. Debug off → **no auto-reload**. |
| 22:18:57 | Terminal session for 5130 marked ended; listener process continued to serve later walks |
| **22:27:18–22:28:34** | **PI-002R-related edits** to `validation_service.py`, `routes.py`, `preview_service.py` (disk mtimes) — **not loaded into already-running 5130 process** |
| **22:34:44** | **EV-001** walk against **new** process on `:5141` with `DATABASE_URL=sqlite:////tmp/ev001_verify.sqlite3` |
| **22:47:47** | **FV-001B Final** walk against **`:5130`** (surviving process + `instance/kwalitec.sqlite3`) |

---

## Database

| | EV-001 | FV-001B Final |
|---|---|---|
| URI | `sqlite:////tmp/ev001_verify.sqlite3` | Default local → `instance/kwalitec.sqlite3` |
| At walk start | Fresh (created for EV-001) | Pre-populated (CS1R, CS1S, CS1U visible in Subjects UI) |
| After walk subjects | CS1V (+ CS1Z regression probe) | CS1R, CS1S, CS1U, CS1F |
| Published packages | CS1V active | None |

---

## Configuration / flags

| Setting | EV-001 (`:5141`) | FV-001B (`:5130`) |
|---|---|---|
| `DATABASE_URL` | Set (dedicated) | **Unset** (instance DB) |
| `SECRET_KEY` | Default warning in server log | Default warning in server log |
| `APP_ENV` | development (log) | development (log) |
| Explicit `KWALITEC_V2_*` in start command | Not set in EV nohup | Not set in 5130 start |
| `.env` | Shared tree (`APP_ENV`, `KWALITEC_EI_INTERNAL_ALPHA`) | Same |

---

## Adapters / build

- Same repository path: `/Users/kwalitec/Developer/kwalitec`
- Same Alembic head at runtime: `202607280080`
- Curriculum Management / CIP adapters: same on-disk modules
- **Critical difference:** Python process import graph for `:5130` frozen at ~22:04; `:5141` imported post–22:27 edits (including PI-002R validation wiring and preview success semantics)

Symptom consistency with stale pre-fix behaviour on FV:

- Approve returns **Publish** refusal copy (PI-002R claimed Approve/Publish verb separation)
- Preview success flash with persistent `not_ready` (PI-002R claimed success only when `ready_for_review` + `validation_passed`)

---

## Conclusion

Environments differ on **database**, **HTTP process**, and **loaded code revision**. Claiming “identical build” from disk alone is false for runtime behaviour.
