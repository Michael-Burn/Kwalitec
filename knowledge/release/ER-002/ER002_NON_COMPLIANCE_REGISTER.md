# ER-002 — Non-Compliance Register

**Programme:** ER-002 — Engineering Recertification  
**Date:** 2026-07-28  
**Nature:** Independent non-compliance / residual inventory against Version 1 engineering expectations  
**Companion:** `ER002_ENGINEERING_AUDIT.md`  
**Audit SHA:** `11d8a224cb4f40de94d7e48e65d467e569408d1c`

---

## 1. Scope

Items below are **live residuals** that prevent unqualified Engineering GO for Version 1 production-ready declaration, or that constrain claim language under a Conditional GO.

Cleared ER-001 Critical/High blockers that are **no longer non-compliant** are listed in §4 for traceability only.

Educational G1–G6 failures are **out of scope** (Product / Educational).

---

## 2. Open non-compliances (engineering)

| ID | Non-compliance | Gate / domain | Severity | Owner | Clearance criterion | Claim impact |
|----|----------------|---------------|----------|-------|---------------------|--------------|
| **ER2-NC-01** | G7.2 staging/production operator sample and production load evidence absent | G7 | High | Engineering + Release | File operator sample + load evidence **or** keep signed HOLD | **No high-traffic / public concurrency claims** (HOLD active) |
| **ER2-NC-02** | No Version 1 annotated RC fingerprint (tag + SHA + green sole `ci.yml` Actions URL) for current engineering tree | G11 | High | Release + Engineering | File fingerprint per `docs/production/RELEASE_CANDIDATE_FINGERPRINT.md` | Blocks unqualified Engineering GO / V1 declaration package |
| **ER2-NC-03** | G10 claim-class residual for Stage 1 / cohort-expansion privacy & enrollment clearance | G10 | High | Security + Product + Privacy | Close enrollment HOLD / privacy claim-class requirements for intended class | **No Stage 1 expansion** justified as G10 PASS |
| **ER2-NC-04** | G8.1 tagged-deploy health/smoke fingerprint not yet bound to a Version 1 declaration package | G8 | Medium | Release | Record live `/health` fingerprint on tagged deploy | Required for G8 full PASS at declaration |
| **ER2-NC-05** | Flask==3.1.0 Medium advisories remain (accepted Security HOLD) | G10.5 / deps | Medium | Engineering + Security | Bump ≥3.1.3 + regression; remove HOLD entries | Allowed under Conditional GO with HOLD disclosure |
| **ER2-NC-06** | Parallel `src/` stack bridged into runtime (`_ensure_src_on_path`) | Architecture | High | Architecture | Consolidation / quarantine programme; do not claim single-stack | Blocks “architecture fully converged” marketing |
| **ER2-NC-07** | Dual legacy vs EIP educational code authorities | Architecture | High | Engineering + Product | Adapter map + retire/contain without educational redesign in ER-002 | Contained for Alpha; sustainment risk |
| **ER2-NC-08** | Legacy Contained presentation shells still registered | Architecture | Medium | Engineering | Retirement WP after soak | Contained |
| **ER2-NC-09** | CI unit job excludes many `tests/application/` / root suites | Test infra | Medium | Engineering | Expand unit matrix or document intentional deferral | Latency of failure discovery |
| **ER2-NC-10** | No login rate limiting / lockout | Security | Medium | Security | Edge WAF or app throttle before cohort expansion | Blocks Stage 1 growth claims |
| **ER2-NC-11** | CSP `'unsafe-inline'` + CDN | Security | Medium | Security | Nonce/hash CSP; self-host where practical | Accepted Alpha residual |
| **ER2-NC-12** | Backup restore size / mass-assignment residuals (V1SP-004 M-3) | Security | Medium | Engineering | Caps + allowlist | Hardening before expansion |
| **ER2-NC-13** | Remember-me cookie clear Secure-flag residual | Security | Medium | Engineering | Explicit `delete_cookie` flags | Hardening |
| **ER2-NC-14** | Dual migration path (Render releaseCommand + StartupService) | Deploy | Medium | Engineering | Prefer single owner; keep idempotent | Ops hygiene |
| **ER2-NC-15** | Coverage unused in CI | Test infra | Low | Engineering | Optional artefact | Enhancement |
| **ER2-NC-16** | Readiness tracker Security summary still references historical soft dependency gate in one cell | Docs | Low | Engineering | Align tracker wording on next docs touch | Drift only |

---

## 3. Accepted / Contained (compliant with disclosure)

| ID | Item | Status | Why not a Conditional-GO breaker |
|----|------|--------|----------------------------------|
| ER2-AC-01 | Sync-only architecture (no Celery/Redis) | Accepted Risk | Intentional; purity tests |
| ER2-AC-02 | No educational-output response caching | Accepted Risk | Integrity policy |
| ER2-AC-03 | Health endpoints unauthenticated | Accepted Risk | Ops by design |
| ER2-AC-04 | G9 telemetry OFF | Accepted Risk | Claim-honest |
| ER2-AC-05 | Quarantined `src/` retained for bridge/tests | Contained | Disclosed; RR residual |
| ER2-AC-06 | Sole-runtime production-ON flags | Accepted Risk | Matches G12 matrix |
| ER2-AC-07 | Dependency Medium/Low HOLDs in accepted register | Accepted Risk | Hard gate + Security disposition |

---

## 4. Cleared vs ER-001 (no longer non-compliant)

| Prior ID | Topic | Evidence of clearance |
|----------|-------|------------------------|
| ER-RB-01 / ER-TD-C01 | Stale `tests.yml` | Workflow absent; sole `ci.yml`; `test_ci_integrity.py` green |
| ER-RB-07 / ER-TD-H04 | Soft pip-audit | Hard `dependency_audit.sh`; policy; local exit 0 |
| ER-RB-06 / ER-TD-H09 | G12 matrix missing | `VERSION_1_FLAG_MATRIX.md` + release-ops tests |
| ER-RB-03 / ER-TD-H06 | G8 pack missing | `G8_RELIABILITY_EVIDENCE.md` |
| ER-RB-02 | G7 incomplete without disposition | `G7_PERFORMANCE_HOLD.md` (HOLD, not PASS) |

---

## 5. Blocker vs residual classification

| Must clear or HOLD-disclose for Conditional GO | Already dispositioned |
|------------------------------------------------|------------------------|
| ER2-NC-01 (G7 HOLD — **filed**) | Cleared ER-RB-01/03/06/07 |
| ER2-NC-02 (G11 tag — **open**) | |
| ER2-NC-03 (G10 expansion — **open**) | |
| ER2-NC-05 (Flask HOLD — **filed**) | |
| ER2-NC-06…08 (architecture Contained disclosure) | |

**Critical open non-compliances:** **None** (invite-only CI integrity restored).

---

## 6. Owner rollup (open High)

| Owner | Open High IDs |
|-------|---------------|
| Release + Engineering | ER2-NC-01, ER2-NC-02, ER2-NC-04 |
| Security + Product + Privacy | ER2-NC-03, ER2-NC-10 |
| Architecture | ER2-NC-06, ER2-NC-07 |
| Engineering | ER2-NC-05, ER2-NC-08, ER2-NC-09, ER2-NC-12…14 |

---

**End of ER-002 Non-Compliance Register**
