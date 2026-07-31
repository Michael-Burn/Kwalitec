# RC-002 — Deployment Audit

**Programme:** Release Candidate RC-002  
**Date:** 2026-07-31  

---

## Verdict

**DEPLOYMENT ARTEFACTS READY**

Render Blueprint + WSGI entry point + migrations are sufficient for founder deployment. Missing Procfile/runtime.txt are intentional (Render Python env + `render.yaml`).

---

## Artefacts

| Artefact | Present | Notes |
|---|---|---|
| `requirements.txt` | Yes | Pinned; includes waitress + psycopg; also ships pytest/ruff/playwright (build bloat WARN) |
| `render.yaml` | Yes | Web service `kwalitec` + DB `kwalitec-db`; release `flask db upgrade`; start Waitress |
| `Procfile` | No | Not required — `startCommand` in yaml |
| `runtime.txt` | No | Not required — Render `env: python` |
| Flask entry | `wsgi.py` | `app = create_app()` |
| Gunicorn command | N/A | Waitress is production server |
| Static assets | Flask static | Version query via app version |
| Database migrations | `migrations/` | Head **`202607300005`** (PB-001 Private Beta Validation evidence tables) |

---

## `render.yaml` flags (frozen educational profile)

- `KWALITEC_V2_SOLE_RUNTIME=1`
- `KWALITEC_V2_STUDENT_EXPERIENCE=1`
- `KWALITEC_V2_DURABLE_STORE=1`
- `KWALITEC_V2_INJECT_ENGINES=1`
- `KWALITEC_V2_SEED_DEMO=0`
- `KWALITEC_V2_FOUNDER_INTELLIGENCE=1`
- `KWALITEC_COMMERCIAL_LOOP=1`
- `KWALITEC_EI_INTERNAL_ALPHA=1`

---

## Release command

`flask db upgrade` on each deploy — verified locally against head `202607300005`.

---

## CI note

`.github/workflows/ci.yml` Alembic head assertion updated to `202607300005` so production-gates match reality.
