# REL-001 — Baseline Fingerprint

**Programme:** REL-001 — Early Access Baseline Release  
**Date:** 2026-08-04  
**Claim class:** Early Access operational baseline (invite-only) — **not** Version 1 production-ready declaration  

---

## Immutable identity

| Field | Value |
|-------|--------|
| Git commit (full) | `95a82b04ae50d32003add3a2f5e6789005a4c962` |
| Git commit (short) | `95a82b0` |
| Annotated tag | `rel-001` |
| Branch | `main` |
| Prior LIVE tip (rollback) | `272a0950ca1a65df01badf5e180c3c06a41681e7` (RO-015 / tag none for this ship) |
| `VERSION` / `APP_VERSION` | `2.0.0-beta.1` |
| Render service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9p4a85bedkc73e3aa9g` |
| Deploy finished (UTC) | `2026-08-04T20:06:12.278143Z` |
| Application URL | https://kwalitec.onrender.com |

---

## LIVE health snapshot

| Endpoint | Result |
|----------|--------|
| `GET /health` | `status=ok` · `environment=production` · `database=connected` · commit match |
| `GET /health/live` | `status=ok` · commit match |
| `GET /health/ready` | `status=ok` · `ready=true` · commit match |
| Migrations | `current=202607310002` · `head=202607310002` |

Evidence: `knowledge/evidence/releases/REL001/health.json`, `health_live.json`, `health_ready.json`, `deploy_status.json`.

---

## Scope of baseline

**Included (validated working-tree ship):**

- Premium Experience PX-001…PX-007 presentation / reliability / continuity fixes Conditional PASS
- Early Access ops authority (OP-001 / OP-002 / EA-001)
- P-002.1 release readiness artefacts (NO-GO for Version 1 declaration retained)
- PB-017 / RO-015 educational volume evidence references

**Explicitly excluded / held:**

- Educational package JSON bodies (Educational Content Freeze)
- Curriculum JSON / engine redesign
- Recommendation Engine redesign
- Student Twin redesign
- Educational Framework (EF-001 freeze)
- New feature work under REL-001

---

## Pre-release verification (recorded)

| Check | Result |
|-------|--------|
| Educational Content Freeze (no package JSON in commit) | **Held** |
| Recommendation / Twin / curriculum engine diffs | **None** |
| Application `create_app()` starts | **PASS** |
| Alembic script head | `202607310002` (matches production) |
| Architecture + student workflow + PX suites | **PASS** (legacy `tests/test_smoke.py` wizard failures pre-exist on prior tip — residual, not introduced) |

---

## Smoke

See `REL001_SMOKE_TEST_REPORT.md` — **PASS** (19/19 critical+journey checks).

---

## Rollback reference

1. Redeploy prior artefact at commit `272a0950ca1a65df01badf5e180c3c06a41681e7` (last known RO-015 LIVE).  
2. Prefer redeploy over DB downgrade (no new migrations in REL-001).  
3. Confirm `/health/ready` and commit field before restoring invites.

---

## Authority chain

PB-017 PASS · Educational Content Freeze · EF-001 · PX-007 Premium Conditional PASS · P-002.1 Release Readiness · OP-001 · OP-002 · EA-001  

**Stop:** Founder approval required before sending the first Early Access invitations.
