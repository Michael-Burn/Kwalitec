# Release Notes — Version 2.0.0

**Product:** Kwalitec Educational Operating System  
**Version:** 2.0.0  
**Tag:** `v2.0.0`  
**Date:** 2026-07-20  
**Milestone:** APP-004 — Production Readiness & Version 2 Release  

---

## Summary

Version 2.0.0 formally closes the Educational Operating System under `src/`.  
This release is **operational readiness only**: configuration, observability, resilience, security verification, CI gates, and release artefacts. No new educational functionality was added.

---

## What Version 2 Delivers

- Deterministic Educational Operating System (domain engines + application pipeline)
- Composition root as the sole construction path for wired services
- AI enrichment as optional presentation-only infrastructure (ADR-008)
- Architecture governance artefacts and CI gates (APP-003)
- Production readiness: typed configuration, structured logging, pipeline/AI timing, health endpoints, provider timeout/retry with deterministic fallback (APP-004)

---

## Operational Highlights (APP-004)

| Area | Capability |
|---|---|
| Configuration | Typed `AppSettings` / `AIProviderSettings`; fail-fast production validation |
| Provider config | `AI_PROVIDER` selects openai / anthropic / gemini / none without code changes |
| Observability | Structured JSON logging; pipeline + AI enrichment timing; success/failure metrics |
| Resilience | Provider timeouts, transient retries, deterministic enrichment fallback |
| Health | `GET /health` (liveness), `GET /health/ready` (readiness + metrics snapshot) |
| Security | Secrets from environment only; input validation on EOS web schemas; dependency audit |
| CI/CD | Architecture Governance, unit, integration, lint, and release-build jobs |

---

## Compatibility

- Legacy Flask product surfaces under `app/` remain available during coexistence.
- Educational authority for the EOS lives under `src/`.
- V1 curriculum traversal and product paths are unchanged by this release.

---

## Verification

See `docs/release/V2_RELEASE_CHECKLIST.md` and `docs/release/DEPENDENCY_AUDIT_V2.md`.

---

## Forward Look

Version 3 planning is documented in `ROADMAP_V3.md`. Version 2 is closed; new educational capability belongs to Version 3 evidence gates.
