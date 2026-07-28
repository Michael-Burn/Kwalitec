# ER-001.1 — Technical Debt Register

**Programme:** ER-001 — Engineering Readiness  
**Work Package:** ER-001.1 — Version 1 Engineering Baseline Assessment  
**Date:** 2026-07-28  
**Nature:** Audit inventory — no remediation executed  
**Companion:** `ER001_1_ENGINEERING_AUDIT.md`  
**Upstream register:** `docs/TECHNICAL_DEBT_REGISTER.md` v0.6.0 (not modified; this WP re-prioritises for Version 1 engineering)

---

## Priority order

Items are ordered **Critical → High → Medium → Low → Accepted Risk → Enhancement**.  
IDs use `ER-TD-*` for ER-001.1 inventory; cross-references to TD / E2 / PC / V1SP kept where known.

---

## Critical

| ID | Item | Why Critical | Owner | Proposed resolution | Target |
|----|------|--------------|-------|---------------------|--------|
| **ER-TD-C01** | Stale `.github/workflows/tests.yml` (Python 3.14, unscoped pytest, no ruff/cert/production gates) conflicts with canonical `ci.yml` | CI integrity; false green/red; unsupported Python vs `requires-python >=3.11` / CONTRIBUTING 3.11–3.13 | Engineering | Retire `tests.yml` or align triggers/jobs/Python with `ci.yml` | **Closed** (EI-001.1) |

---

## High

| ID | Item | Cross-ref | Owner | Proposed resolution | Target |
|----|------|-----------|-------|---------------------|--------|
| **ER-TD-H01** | Parallel `src/` stack (~1,100 `.py` files) on `sys.path`; dual factory maintenance | RR-001.3E · RR-002.3 | Architecture + Engineering | Document production ownership; plan consolidation/quarantine programme; keep CI green on both until retired | Next architecture epic |
| **ER-TD-H02** | Dual educational product authorities — legacy `app/services/` vs Twin / EIP pipeline | E2-PI-01…05 · PC-003 · PC-004 | Engineering + Product | Adapter map + retire/contain legacy on student paths without educational redesign in this programme | 1–2 epics |
| **ER-TD-H03** | Production entry `wsgi:app` vs CI-verified `src/web/app.py` factory | RR-002.3 | Engineering | Explicit runtime ownership doc + release checklist assertion | Next release WP |
| **ER-TD-H04** | `pip-audit` soft gate — known advisories may ship | DEPENDENCY_AUDIT_V2 · G10.5 | Security + Release | Hard-fail on Critical; HOLD policy for accepted Mediums | **Closed** (EI-001.2 — hard gate + accepted-findings HOLD; Flask pin bump remains ER-TD-M04) |
| **ER-TD-H05** | G7 incomplete — no staging/production operator sample / load evidence | P-002.1 G7 | Engineering + Release | Record operator sample; optional HOLD with claim restriction | Before V1 declaration |
| **ER-TD-H06** | G8 incomplete — rollback drill + backup acknowledgement for claim class | P-002.1 G8 | Engineering + Release | File drill note + BACKUP_AND_RECOVERY ack | Before V1 declaration |
| **ER-TD-H07** | G10 incomplete — privacy signatures + dependency critical policy for tag | P-002.1 G10 · V1SP-004 | Security | Close privacy pack for claim class; policy for pip-audit | **Partial** — dependency critical policy Closed (EI-001.2); privacy pack residual remains before Stage 1 / V1 |
| **ER-TD-H08** | G11 — continuous green on fingerprinted RC required | P-002.1 G11 | Engineering + Release | Tag RC; enforce `ci.yml` green only — **process/methodology Closed** (EI-001.1 fingerprint); tag execution remains Release operator step | Before V1 declaration (tag) |
| **ER-TD-H09** | G12 — Version 1 flag matrix not published | P-002.1 G12 · RP-001 FEATURE_FLAG_REGISTER | Product + Release + Engineering | Publish matrix: default ON/OFF, owner, rollback, kill-switch; align `.env.example` / `render.yaml` | Before V1 declaration |
| **ER-TD-H10** | CI unit job excludes `tests/application/`, `tests/infrastructure/`, many root suites | `ci.yml` | Engineering | Expand unit matrix or document intentional deferral to integration only | Next CI hygiene WP |
| **ER-TD-H11** | SQLAlchemy 2.x legacy APIs (`Query.get()`, etc.) | TD-001 · TD-005 | Engineering | Sweep to `Session.get` / 2.x style | Maintenance sprint |
| **ER-TD-H12** | `domain.Mission` vs `models.Mission` dual type identity | E2-PE-03 | Architecture + Engineering | Naming/adapter clarity; prevent cross-layer confusion | Architecture epic |

---

## Medium

| ID | Item | Cross-ref | Owner | Proposed resolution | Target |
|----|------|-----------|-------|---------------------|--------|
| **ER-TD-M01** | CSP `'unsafe-inline'` + jsDelivr CDN | V1SP-004 M-2 · G10 residual | Security | Nonce/hash CSP; self-host Chart.js where practical | Hardening sprint |
| **ER-TD-M02** | No login rate limiting / lockout | V1SP-004 M-1 | Security | Edge WAF or app throttle before cohort expansion | Pre–Stage 1 |
| **ER-TD-M03** | Backup restore: content length / mass-assignment residuals | V1SP-004 M-3 | Engineering | `MAX_CONTENT_LENGTH` + column allowlist | Hardening sprint |
| **ER-TD-M04** | Flask==3.1.0 (advisories fixed in ≥3.1.3) | DEPENDENCY_AUDIT_V2 | Engineering + Security | Bump + regression suite | Dependency chore |
| **ER-TD-M05** | Remember-me cookie clear Secure flags | V1SP-004 M-6 | Engineering | Explicit `delete_cookie` flags on logout | Hardening sprint |
| **ER-TD-M06** | Large route modules (Study Plan ~1.4k lines) | TD-002 | Engineering | Split on edit boundaries | When touching module |
| **ER-TD-M07** | Oversized legacy services (planning / recommendation / research) | TD-003 | Engineering | Decompose by domain | Maintainability epic |
| **ER-TD-M08** | `presentation/student/view_models.py` ~2k lines | — | Engineering | Split view-model builders | When touching |
| **ER-TD-M09** | Topic/Curriculum index gaps; lazy N+1 residual | TD-007 | Engineering | Profile with `PROFILE_SQL=1`; add indexes/eager loads | Performance sprint |
| **ER-TD-M10** | Legacy blueprint shells still registered | PC-001 · RR-002.3 | Engineering | Retire after parity gates | Post–soak retirement WP |
| **ER-TD-M11** | ORM curriculum traversal on model | ARCHITECTURE drift | Engineering | Prefer `CurriculumService` only | Cleanup |
| **ER-TD-M12** | Dual migration path (Render `releaseCommand` + StartupService) | StartupService | Engineering | Prefer single owner; keep idempotent | Ops hygiene |
| **ER-TD-M13** | Dual config systems (`app/config.py` vs `src/.../settings.py`) | ER-A | Architecture | Consolidate when `src/` retires | Architecture epic |
| **ER-TD-M14** | `coverage` package unused in CI | pyproject / requirements | Engineering | Optional report artefact for G11 evidence | CI hygiene |
| **ER-TD-M15** | Analytics CLI worker requires external cron when flag ON | EP-002 | Release + Engineering | Document cron or add Render worker before flag ON | Flag enablement |
| **ER-TD-M16** | ProfileService Educational State bypass | PC-005 | Engineering | Align with Educational State authority | Consolidation |
| **ER-TD-M17** | Residual Ruff / Architecture Guardian findings | TD-004 · TD-006 | Engineering | Incremental on touched paths | Ongoing |
| **ER-TD-M18** | Mission adapter / dual mission engines | PC-003 | Engineering | Single adapter path | Consolidation |

---

## Low

| ID | Item | Cross-ref | Owner | Proposed resolution |
|----|------|-----------|-------|---------------------|
| **ER-TD-L01** | Study-plan ownership failures → flash/redirect vs 403/404 | Authz | Engineering | Prefer 403/404 for foreign resources |
| **ER-TD-L02** | CONTRIBUTING ruff scope omits `src/` | Docs | Engineering | Align docs with `ci.yml` |
| **ER-TD-L03** | Playwright in requirements without browser CI job | Deps | Engineering | Move to optional/dev or add job |
| **ER-TD-L04** | Deprecated founder URL redirects / dead branding assets | PC-006 · PC-007 | Engineering | Cleanup when safe |
| **ER-TD-L05** | Gunicorn pinned but unused on Render (Waitress used) | Deps | Engineering | Document alternate or remove pin |
| **ER-TD-L06** | Auth success/failure not structured audit logs | V1SP-004 L-1 | Security | Structured auth events |
| **ER-TD-L07** | Legacy founder email allowlist env bridge | Founder access | Security | Prefer durable RBAC only |

---

## Accepted Risk

| ID | Item | Justification | Owner |
|----|------|---------------|-------|
| **ER-TD-AR01** | Sync-only architecture (no Celery/Redis) | Intentional; architecture purity tests forbid Celery in domain | Architecture |
| **ER-TD-AR02** | No educational-output response caching | PERFORMANCE_GUIDE / educational integrity | Engineering |
| **ER-TD-AR03** | CSP residual for invite-only Alpha | Documented; Chart.js / wizard needs | Security |
| **ER-TD-AR04** | Legacy Contained shells under sole-runtime redirects | RR-002.3 soak strategy | Architecture |
| **ER-TD-AR05** | Quarantined `src/` retained for tests / bridge | RR-001.3E Board residual — do not claim as Alpha sole story | Architecture |
| **ER-TD-AR06** | Health endpoints unauthenticated | Liveness/readiness by design | Engineering |
| **ER-TD-AR07** | CSRF disabled only in TestingConfig | Isolated; production gate | Engineering |
| **ER-TD-AR08** | Analytics telemetry COMPLETE with flag OFF | G9 claim-safe if not overclaimed | Product + Engineering |
| **ER-TD-AR09** | Production SECRET_KEY / DATABASE_URL validation | Factory fail-fast | Engineering |
| **ER-TD-AR10** | Services free of `flask.request` | Layering invariant held | Engineering |

---

## Enhancement

| ID | Item | Owner | Notes |
|----|------|-------|-------|
| **ER-TD-E01** | Service decomposition beyond TD-003 | Engineering | After V1 engineering clearance |
| **ER-TD-E02** | Eager-load catalogue for all list views | Engineering | Profile-driven |
| **ER-TD-E03** | Coverage thresholds (if desired beyond G11 suite-green rule) | Engineering | Optional; G11 does not require % |
| **ER-TD-E04** | Dependabot / Renovate | Engineering | Supply-chain hygiene |
| **ER-TD-E05** | Self-hosted static assets (drop CDN) | Engineering | Enables stricter CSP |
| **ER-TD-E06** | Dedicated Render worker for analytics outbox | Release | When analytics ON |

---

## Mapping to upstream register

| Upstream | ER-001.1 treatment |
|----------|-------------------|
| TD-001 / TD-005 | → ER-TD-H11 |
| TD-002 | → ER-TD-M06 |
| TD-003 | → ER-TD-M07 / E01 |
| TD-004 / TD-006 | → ER-TD-M17 |
| TD-007 | → ER-TD-M09 |
| E2-PI-01…05 / PC-003 / PC-004 | → ER-TD-H02 / M18 |
| E2-PE-03 | → ER-TD-H12 |
| PC-001 | → ER-TD-M10 / AR04 |
| PC-005 | → ER-TD-M16 |
| PC-006 / PC-007 | → ER-TD-L04 |

`docs/TECHNICAL_DEBT_REGISTER.md` remains the living engineering register; this document is the **Version 1 baseline snapshot** for ER-001.1.

---

## Prioritisation summary for Version 1

**Must clear before engineering V1 GO:**

1. ER-TD-C01 (CI workflow integrity)  
2. ER-TD-H04…H09 (G7–G12 evidence / dependency policy / flag matrix)  
3. ER-TD-H08 (green fingerprinted RC)

**May HOLD with claim restriction (P-002.1):** G7–G9 style residuals with Product + Release sign-off — never security Criticals.

**Sustainment (not Alpha blockers):** ER-TD-H01–H03, H11–H12, Medium/Low/Enhancement.

---

**End of ER-001.1 Technical Debt Register**
