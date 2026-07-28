# EI-001.2 — Design Report

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.2 — Dependency Assurance & Security Controls  
**Date:** 2026-07-28  
**Change class:** Infrastructure  
**Authority:** ER-001.1 · ER-RB-07 · P-002.1 G10.5  
**Governance stance:** Educational baselines frozen — no application / educational behaviour changes

---

## 1. Problem

ER-001.1 recorded **ER-RB-07**: `pip-audit` in `ci.yml` soft-failed (warn + `exit 0` / `|| true`). Known Flask advisories and any future advisory could therefore reach a green CI signal without an explicit Security disposition, undermining G10.5 and release confidence.

---

## 2. Design goals

1. **Explicit policy** — severity / HOLD rules written once and cited by release docs.  
2. **Enforceable CI** — unaccepted advisories fail `production-gates` and `release-build`.  
3. **Reproducible evidence** — one operator/CI command produces the audit used for tags.  
4. **No application behaviour change** — do not bump Flask or rewrite product code in this WP; Medium residuals use Security HOLD.

---

## 3. Control model

```
requirements.txt
       │
       ▼
scripts/dependency_audit.sh
       │  reads docs/security/dependency_accepted_vulns.txt
       │  pip-audit --ignore-vuln <accepted IDs>
       ▼
  exit 0  →  only accepted (or zero) findings
  exit ≠0 →  CI / release STOP
       │
       ├── Policy: DEPENDENCY_ASSURANCE_POLICY.md
       └── HOLD register: DEPENDENCY_ACCEPTED_FINDINGS.md
```

| Severity / case | Behaviour |
|-----------------|-----------|
| Critical | Never accepted; never HOLD-waived |
| Unlisted advisory | Hard-fail until Security classifies |
| Documented Medium/Low | Allowed only via synced accepted-ID register + HOLD text |

`pip-audit` may not emit CVSS; therefore **absence from the accepted register is the operational blocking signal**.

---

## 4. Alternatives considered

| Option | Rejected because |
|--------|------------------|
| Soft-fail forever + manual review | Fails ER-RB-07 clearance |
| Bump Flask in this WP | Application dependency change; tracked separately as ER-TD-M04 |
| Fail on *all* findings with no ignore list | Would block CI on already-mitigated Mediums without a HOLD mechanism |
| Dependabot-only | Enhancement (ER-TD-E04); does not replace tag-day evidence |

---

## 5. Integration with release documentation

- RC fingerprint optional note → dependency audit output path  
- RELEASE_PROCESS / PROTOCOL / CHECKLIST / Quality Manual / Release Playbook cite hard gate + policy  
- Historical `DEPENDENCY_AUDIT_V2.md` retained as inventory; points at governing policy  

---

## 6. Verification design

Architecture tests assert artefacts, accepted-ID ↔ register sync, script behaviour markers, and absence of soft-fail patterns in `ci.yml`. Operators re-run `./scripts/dependency_audit.sh` for tag evidence.

---

## 7. Non-goals

Application authZ/authN features, UI, schema, educational systems, recommendation algorithms, Mission Intelligence, privacy pack closure (ER-RB-04 residual).

---

**End of EI001_2_DESIGN_REPORT**
