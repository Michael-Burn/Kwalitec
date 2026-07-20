# Version 2 Release Checklist

**Milestone:** APP-004 — Production Readiness & Version 2 Release  
**Version:** 2.0.0  
**Tag:** `v2.0.0`  
**Date:** 2026-07-20  

Operational verification only. Do not add educational functionality during this checklist.

---

## Release artefacts

- [ ] `VERSION` reads `2.0.0`
- [ ] `CHANGELOG.md` includes `[2.0.0]`
- [ ] `RELEASE_NOTES_V2.md` present
- [ ] `ROADMAP_V3.md` present
- [ ] Architecture governance docs present (APP-003 set under `docs/`)

---

## CI/CD gates

- [ ] **Architecture Governance** job green (`tests/architecture/`)
- [ ] **Unit tests** job green
- [ ] **Integration tests** job green
- [ ] **Lint** job green (`ruff`)
- [ ] **Release build** job green (app import + render.yaml + EOS factory)

---

## Configuration & security

- [ ] Secrets loaded only from environment / typed settings (no hard-coded production secrets)
- [ ] Production `SECRET_KEY` is non-default
- [ ] Production `DATABASE_URL` / `EOS_DATABASE_URL` set
- [ ] Provider selectable via `AI_PROVIDER` without code changes
- [ ] Input validation enforced on EOS web request schemas
- [ ] **Dependency audit** reviewed (`docs/release/DEPENDENCY_AUDIT_V2.md`)

---

## Observability & resilience

- [ ] Structured logging configurable (`STRUCTURED_LOGGING`, `LOG_LEVEL`)
- [ ] Pipeline execution timing recorded
- [ ] AI enrichment timing recorded when enrichment enabled
- [ ] Pipeline success/failure metrics available
- [ ] AI provider timeout + retry policy configured
- [ ] Deterministic enrichment fallback when AI unavailable / disabled

---

## Health endpoints

- [ ] `GET /health` returns liveness OK
- [ ] `GET /health/ready` returns readiness (configuration + composition)

---

## Sign-off

| Role | Result | Date |
|---|---|---|
| Engineering | PASS / FAIL | |
| Architecture | PASS / FAIL | |
| Release operator | PASS / FAIL | |

Version 2 is closed only when all mandatory gates above are PASS.
