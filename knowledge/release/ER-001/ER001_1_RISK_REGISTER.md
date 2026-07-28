# ER-001.1 — Risk Register

**Programme:** ER-001 — Engineering Readiness  
**Work Package:** ER-001.1 — Version 1 Engineering Baseline Assessment  
**Date:** 2026-07-28  
**Nature:** Engineering risk inventory — owners assigned  
**Companions:** `ER001_1_RELEASE_BLOCKERS.md`, `ER001_1_TECHNICAL_DEBT_REGISTER.md`

---

## Legend

| Field | Values |
|-------|--------|
| **Likelihood** | High / Medium / Low |
| **Impact** | Critical / High / Medium / Low |
| **Class** | Critical / High / Medium / Low / Accepted Risk / Enhancement |
| **Status** | Open / Contained / Accepted / Watch |

Every risk has a named **Owner**.

---

## Critical / High risks

| ID | Risk | Likelihood | Impact | Class | Owner | Mitigation / discipline | Status |
|----|------|------------|--------|-------|-------|-------------------------|--------|
| **ER-R-01** | Dual CI workflows produce contradictory signals; unsupported Python 3.14 in `tests.yml` | Medium | High | Critical | Engineering | Retire/align `tests.yml`; treat `ci.yml` as sole authority | **Closed** (EI-001.1) |
| **ER-R-02** | Version 1 declared without G7–G12 engineering evidence | Medium | Critical | High | Release + Product | Enforce P-002.1 board; ER-RB-02…06 | Open |
| **ER-R-03** | Known dependency advisory ships (Flask pin) via soft pip-audit | Medium | High | High | Security | Hard-fail Criticals; bump Flask; HOLD policy | **Contained** (EI-001.2 — hard gate + Security HOLD; Flask bump residual ER-TD-M04) |
| **ER-R-04** | Wrong runtime claimed (`src/web` vs sole-runtime `app/`) | Medium | High | High | Product + Architecture | RR-002.3 ownership; release checklist | Contained |
| **ER-R-05** | Dual educational code authorities diverge → inconsistent student outcomes | Medium | High | High | Engineering + Product | Consumer-chain map; Contained Alpha defaults; consolidation epic | Contained |
| **ER-R-06** | Sole-runtime misconfiguration reintroduces competing homes | Low | Critical | High | Release Engineering | Protect `KWALITEC_V2_SOLE_RUNTIME`; smoke before Alpha claims (RR-C04) | Contained |
| **ER-R-07** | Public registration accidentally exposed | Low | Critical | High | Security + Product | No register routes; review gate (RR-C05) | Contained |
| **ER-R-08** | Analytics flag ON without cron → silent outbox backlog | Medium | High | High | Release | Cron or worker before enablement | Watch |
| **ER-R-09** | Cohort expansion without rate limiting / privacy pack | Medium | High | High | Security | Close ER-RB-04; add throttle before Stage 1 | Open |
| **ER-R-10** | G12 flags ON without soak → dual educational speech | Medium | High | High | Product + Release | Publish matrix; keep OFF until certified | Open |

---

## Medium risks

| ID | Risk | Likelihood | Impact | Class | Owner | Mitigation / discipline | Status |
|----|------|------------|--------|-------|-------|-------------------------|--------|
| **ER-R-11** | XSS blast radius via CSP `'unsafe-inline'` | Medium | Medium | Medium | Security | Nonce/hash CSP; self-host assets | Accepted |
| **ER-R-12** | N+1 regressions on new list widgets | Medium | Medium | Medium | Engineering | `PROFILE_SQL=1`; GA query budgets | Watch |
| **ER-R-13** | SQLAlchemy 2.x deprecations become hard break | Medium | Medium | Medium | Engineering | TD-001/005 sweep | Open |
| **ER-R-14** | Large route/service modules slow incident response | High | Medium | Medium | Engineering | Split on edit; TD-002/003 | Open |
| **ER-R-15** | Dual migration paths mask releaseCommand failure | Low | Medium | Medium | Engineering | Prefer single owner; monitor both logs | Accepted |
| **ER-R-16** | Backup restore abuse (size / mass assignment) | Low | Medium | Medium | Engineering | Caps + allowlist | Open |
| **ER-R-17** | Remember-me cookie flags incomplete on logout | Low | Medium | Medium | Engineering | Explicit delete_cookie flags | Open |
| **ER-R-18** | Unit CI subset hides failures until integration | Medium | Medium | Medium | Engineering | Expand unit paths or accept latency | Open |
| **ER-R-19** | Free-tier Render capacity limits under growth | Medium | Medium | Medium | Release + Product | Plan upgrade before marketing traffic | Watch |
| **ER-R-20** | Coverage metrics unused → blind spots vs suite-green | Medium | Low | Medium | Engineering | Optional coverage artefact | Accepted |

---

## Low risks

| ID | Risk | Likelihood | Impact | Class | Owner | Mitigation | Status |
|----|------|------------|--------|-------|-------|------------|--------|
| **ER-R-21** | Study-plan ownership redirect leaks existence | Low | Low | Low | Engineering | Prefer 403/404 | Open |
| **ER-R-22** | Operator shell `create-test-user` abuse | Low | Medium | Low | Security | Restrict Render shell | Accepted |
| **ER-R-23** | Doc drift (CONTRIBUTING ruff vs CI) | Medium | Low | Low | Engineering | Align docs | Open |
| **ER-R-24** | Playwright unused in CI but in requirements | Low | Low | Low | Engineering | Optional dep | Accepted |
| **ER-R-25** | Legacy founder email allowlist over-grants Console | Low | Medium | Low | Security | Prefer RBAC-only | Contained |

---

## Accepted Risk (by design)

| ID | Risk | Owner | Why accepted |
|----|------|-------|--------------|
| **ER-R-AR01** | No async job broker | Architecture | Sync product; purity tests forbid Celery in domain |
| **ER-R-AR02** | No educational response caching | Engineering | Integrity over latency theatre |
| **ER-R-AR03** | Contained legacy shells remain in repo | Architecture | RR-002 soak; no safe delete yet |
| **ER-R-AR04** | Quarantined `src/` retained | Architecture | RR-001.3E Board residual |
| **ER-R-AR05** | Health endpoints public | Engineering | Ops requirement; no secrets |
| **ER-R-AR06** | G9 telemetry OFF in claim language | Product | Honest OFF posture |

---

## Enhancement opportunities (risk reduction)

| ID | Opportunity | Owner | Class |
|----|-------------|-------|-------|
| **ER-R-E01** | Dependabot / automated bumps | Engineering | Enhancement |
| **ER-R-E02** | Self-hosted CDN assets | Engineering | Enhancement |
| **ER-R-E03** | Structured auth audit log | Security | Enhancement |
| **ER-R-E04** | Dedicated analytics worker service | Release | Enhancement |

---

## Owner rollup

| Owner | Open Critical/High risks |
|-------|--------------------------|
| Engineering | ER-R-01, ER-R-05 (shared), ER-R-12…14, ER-R-16…18 |
| Security | ER-R-03, ER-R-07 (shared), ER-R-09, ER-R-11 |
| Release | ER-R-02 (shared), ER-R-06, ER-R-08, ER-R-10 (shared), ER-R-19 |
| Product | ER-R-02, ER-R-04, ER-R-05, ER-R-07, ER-R-10 |
| Architecture | ER-R-04, ER-R-05, Contained AR items |

---

## Educational residual pointer (not reopened)

Operational Contained Criticals **RR-C04 / RR-C05** from `RR001_3E_RESIDUAL_RISK_REGISTER.md` are mirrored as ER-R-06 / ER-R-07 for engineering awareness. No new educational regression evidence found; educational programmes remain closed baselines.

---

## Risk appetite for Version 1

| Appetite | Rule |
|----------|------|
| Invite-only Alpha | Contained / Accepted risks tolerable with disclosure |
| Version 1 production-ready declaration | Open Critical/High engineering risks ER-R-01…03, ER-R-09…10 must close or HOLD per P-002.1 |
| Security Criticals | Never HOLD-waived |

---

**End of ER-001.1 Risk Register**
