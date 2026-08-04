# REL-001 — Early Access Baseline Release Evidence

**Programme:** REL-001 — Early Access Baseline Release  
**Date:** 2026-08-04  
**Nature:** Operational release only  

## Identity

| Field | Value |
|-------|--------|
| Git commit | `95a82b04ae50d32003add3a2f5e6789005a4c962` |
| Tag | `rel-001` |
| Deploy ID | `dep-d9p4a85bedkc73e3aa9g` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Application URL | https://kwalitec.onrender.com |
| Version | `2.0.0-beta.1` |
| Alembic | `202607310002` (current = head) |

## Artefacts

| Path | Purpose |
|------|---------|
| `deploy_create.json` / `deploy_status.json` | Render deploy create + final live status |
| `health.json` / `health_live.json` / `health_ready.json` | LIVE health fingerprint |
| `create_user_payload.json` / `create_user_job_final.json` | Smoke user create (password redacted) |
| `student.email` | Smoke account email only |
| `smoke_results.json` | LIVE smoke checklist results |
| `html/` | Captured HTML from smoke walkthrough |
| `suite/rel001_smoke_notes.md` | Operator notes for smoke |

## Companion reports (repo root)

- `REL001_DEPLOYMENT_REPORT.md`
- `REL001_RELEASE_NOTES.md`
- `REL001_SMOKE_TEST_REPORT.md`
- `REL001_BASELINE_FINGERPRINT.md`
