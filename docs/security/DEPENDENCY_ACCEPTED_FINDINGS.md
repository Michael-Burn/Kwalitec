# Dependency Accepted Findings (Security HOLD Register)

**Programme:** EI-001.2  
**Policy:** `docs/security/DEPENDENCY_ASSURANCE_POLICY.md`  
**Machine IDs:** `docs/security/dependency_accepted_vulns.txt`  
**Date:** 2026-07-28  
**Recorder:** Engineering (Security disposition for invite-only / Alpha claim class)

Entries below are **Security HOLD / accepted residuals** for non-Critical advisories. They must stay in sync with `dependency_accepted_vulns.txt`. Criticals must never appear here.

---

## Active accepted findings

| Advisory ID | Package | Pin | Severity (Security) | Rationale | Review-by | Owner |
|-------------|---------|-----|---------------------|-----------|-----------|-------|
| **PYSEC-2026-1377** (CVE-2025-47278) | Flask | 3.1.0 | Medium | Affects `SECRET_KEY_FALLBACKS` key-order; product does **not** set fallbacks. Tracked as ER-TD-M04 bump. | Before V1 declaration or next dependency chore | Security + Engineering |
| **PYSEC-2026-2151** (CVE-2026-27205) | Flask | 3.1.0 | Medium | `Vary: Cookie` edge cases; HTML responses use `Cache-Control: no-store`. Tracked as ER-TD-M04 bump to ≥3.1.3. | Before V1 declaration or next dependency chore | Security + Engineering |
| **PYSEC-2026-1845** | pytest | 8.3.4 | Low / non-prod | Test dependency only; not on production runtime path. | Next test-toolchain bump | Engineering |
| **PYSEC-2026-2270** | python-dotenv | 1.0.1 | Low | `set_key` / `unset_key` symlink issue; app uses `load_dotenv()` only. | Next dependency chore | Engineering |

---

## Security HOLD statement (tag day)

For a Version 1 / RC tag that retains the pins above:

> Security **HOLDs** the Medium Flask advisories PYSEC-2026-1377 and PYSEC-2026-2151 for the invite-only / Alpha claim class, given mitigations above and ER-TD-M04 follow-up. Critical dependency findings remain **not** HOLD-waivable. pytest and python-dotenv advisories are accepted as Low / non-prod residual pending bump.

Tag evidence must cite this document path and the `./scripts/dependency_audit.sh` run on the tagged SHA.

---

## Change log

| Date | Change |
|------|--------|
| 2026-07-28 | Initial register under EI-001.2 (closes soft-gate ER-RB-07) |
