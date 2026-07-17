# Kwalitec v1.0.0 — Build RC2

**Status:** Internal Alpha operational baseline  
**Product version:** `1.0.0`  
**Chrome:** Internal Alpha · Founding Cohort · **Build RC2**  
**Date:** July 2026  

---

## Overview

Version 1.0.0 Build RC2 is the fingerprinted baseline for continued invite-only Internal Alpha after the Version 1 Stabilisation Programme (V1SP).

It is **not** a public production launch. Public registration remains disabled.

---

## Highlights

- Curriculum Engine with V1 (flat) and V2 (hierarchical) coexistence
- Student Learning Workspace: Dashboard, Study Plan, Study Session, Analytics
- Revision Workspace when syllabus coverage is complete (V1SP-001A)
- Deterministic Stage A recommendations and readiness (optional EI Internal Alpha card)
- Founder Command Centre: Overview, Operational Health, Feedback, Research, Vision Journal, Releases
- Canonical brand infrastructure and Internal Alpha chrome
- Production hardening: cookies, redirects, SECRET_KEY gate, static cache fingerprinting
- Performance indexes on measured Alpha hot paths

---

## Migration notes

Apply Alembic migrations via `flask db upgrade` locally or via production `StartupService` on Render.

Notable additive revisions in the RC2 window:

| Revision | Purpose |
|---|---|
| `202607170001` | Revision lifecycle fields on study plans (V1SP-001A) |
| `202607170002` | Vision Journal tables (V1SP-001D) |
| `202607170003` | Performance indexes (V1SP-003) |

No destructive schema changes. Curriculum V1/V2 import paths remain intact.

---

## Known limitations

Documented in RC2 readiness and V1SP reports. Intentional Version 1 deferrals include:

- No public registration / password reset self-service
- Twin-first UI cutover and Twin persistence
- Exam Ready lifecycle
- Login rate limiting, CSP nonces, Founder post-login landing

---

## Operator references

| Document | Use |
|---|---|
| `docs/process/RELEASE_PROTOCOL.md` | Canonical release procedure |
| `knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md` | Quality gate |
| `knowledge/releases/V1SP-001B_OPERATIONAL_FIXES.md` | High-severity closure |
| `knowledge/releases/V1SP-004_SECURITY_VERIFICATION.md` | Security re-verification |
| `CHANGELOG.md` | Version history |
| `render.yaml` | Render deploy Blueprint |

---

## Fingerprint checklist

- [ ] `pyproject.toml` / `APP_VERSION` = `1.0.0`
- [ ] Footer / badge shows Build **RC2**
- [ ] `/health` returns healthy after deploy
- [ ] Login → Dashboard → Study Plan → Study Session smoke passes
- [ ] Founder email can open `/founder` Overview and Operational Health
