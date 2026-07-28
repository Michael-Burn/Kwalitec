# Dependency Assurance Policy

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.2 — Dependency Assurance & Security Controls  
**Status:** Governing — engineering security control  
**Authority:** ER-001.1 (ER-RB-07) · P-002.1 G10.5  
**Scope:** Python runtime dependencies declared in `requirements.txt`  
**Date:** 2026-07-28  

Educational governance and application behaviour are **out of scope**. This policy governs package vulnerability verification and release security evidence only.

---

## 1. Purpose

Make dependency verification **explicit**, **enforceable in CI**, and **reproducible for release tags**, so known advisories cannot ship without a Security disposition.

G10.5 (P-002.1): dependency audit reviewed for the tag; **Criticals blocked** or — for non-Critical accepted residuals — **explicitly HOLD-accepted by Security**.

---

## 2. Severity rules

| Class | CI behaviour | Release behaviour |
|-------|--------------|-------------------|
| **Critical** | Must fail CI | Must **not** ship. Security Criticals are **never** HOLD-waived (ER-001.1). |
| **High** | Must fail CI unless Security reclassifies and records HOLD before merge | Tag blocked until cleared or HOLD filed |
| **Medium / Low / Info** | Fail CI unless the advisory ID is listed in the accepted-findings register | May ship only with current Security HOLD / accepted-findings entry |
| **New / unclassified advisory** | Treated as **blocking** until Security classifies and either fixes, ignores via accepted register, or HOLDs | Same |

`pip-audit` does not always emit CVSS severity. **Operational rule:** any advisory returned by `pip-audit` that is **not** listed in `docs/security/dependency_accepted_vulns.txt` fails the engineering gate. Critical classification (when available from advisory text / Security review) never enters the accepted register.

---

## 3. Control artefacts

| Artefact | Role |
|----------|------|
| This policy | Normative rules |
| `docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md` | Human Security HOLD / disposition register |
| `docs/security/dependency_accepted_vulns.txt` | Machine-readable ignore IDs for `pip-audit --ignore-vuln` |
| `scripts/dependency_audit.sh` | Reproducible audit entrypoint (CI + operators) |
| `docs/release/DEPENDENCY_AUDIT_V2.md` | Version baseline inventory (historical + pointer) |
| `.github/workflows/ci.yml` | Hard gate in `production-gates` and `release-build` |

---

## 4. CI enforcement

1. Install `pip-audit` with project requirements.  
2. Run `./scripts/dependency_audit.sh` (loads accepted IDs; invokes `pip-audit -r requirements.txt`).  
3. Non-zero exit → **job failure** (hard gate). Soft-warn / `exit 0` / `|| true` on dependency audit is **forbidden**.  
4. Architecture tests assert policy docs, accepted-ID sync, and hard-gate wiring.

---

## 5. Release security evidence (reproducible)

Before tagging a security-sensitive or Version 1 / RC claim package:

```bash
./scripts/dependency_audit.sh --output pip-audit-release.txt
```

File with the release evidence pack (or RC fingerprint):

| Field | Value |
|-------|-------|
| `commit_sha` | Tagged SHA |
| `command` | `./scripts/dependency_audit.sh --output …` |
| `result` | exit 0 / fail |
| `accepted_findings_ref` | `docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md` |
| `raw_report` | Attached `pip-audit-release.txt` (optional if clean of unaccepted IDs) |
| `security_recorder` | Named Security or Release owner |

RC fingerprints may cite the report path in the optional `pip-audit` note field (`docs/production/RELEASE_CANDIDATE_FINGERPRINT.md`).

---

## 6. Adding or removing accepted findings

1. Re-run `./scripts/dependency_audit.sh` without ignoring the ID (or inspect `pip-audit` JSON).  
2. Security classifies severity and exploitability for **this** product posture.  
3. If Critical → fix dependency; do **not** accept.  
4. If Medium/Low acceptable → update **both** `DEPENDENCY_ACCEPTED_FINDINGS.md` and `dependency_accepted_vulns.txt` in the same change; record owner, rationale, review-by date.  
5. Merge only when architecture dependency-assurance tests pass.

Removing an ID (after bump / fix) requires deleting it from both files and confirming CI stays green.

---

## 7. Explicit non-claims

- This policy does **not** bump application pins by itself (e.g. Flask). Package upgrades remain separate chores.  
- Closing ER-RB-07 (policy + hard gate) does **not** close broader G10 residuals (privacy pack, CSP, rate limits).  
- Educational / recommendation / auth product behaviour is unchanged by this control.

---

## References

- `knowledge/release/ER-001/ER001_1_RELEASE_BLOCKERS.md` (ER-RB-07)  
- `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` (G10.5)  
- `knowledge/releases/V1SP-004_SECURITY_VERIFICATION.md`  
- `docs/ga/SECURITY_REVIEW.md`
