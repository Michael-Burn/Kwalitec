# EI-001.2 — Traceability Matrix

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.2 — Dependency Assurance & Security Controls  
**Date:** 2026-07-28  
**Rule:** Every remediation references ER finding → control → artefact → release impact.  
**Companion:** `EI001_2_IMPLEMENTATION_REPORT.md` · `ER001_1_RELEASE_BLOCKERS.md`

---

## 1. Finding → evidence

| Finding | ER debt / risk | Control | Artefact(s) | Release impact | Closure |
|---------|----------------|---------|-------------|----------------|---------|
| **ER-RB-07** | ER-TD-H04 · ER-R-03 | Hard dependency audit + Security HOLD register | Policy; accepted findings; `dependency_accepted_vulns.txt`; `scripts/dependency_audit.sh`; `ci.yml` hard steps; architecture tests; release/security docs | Unaccepted advisories cannot green CI; tag evidence reproducible | **Closed** |
| ER-RB-04 (G10.5 portion) | ER-TD-H07 (partial) | Same G10.5 policy | As above | Dependency critical policy satisfied; privacy pack **not** claimed | **Partial** (privacy residual open) |

---

## 2. Evidence chain map

| Link | Requirement | EI-001.2 delivery |
|------|-------------|-------------------|
| Policy | Explicit enforceable rules | `DEPENDENCY_ASSURANCE_POLICY.md` |
| Verification | Reproducible command | `./scripts/dependency_audit.sh` |
| CI | Hard fail unaccepted | `production-gates` + `release-build` |
| HOLD | Documented Medium/Low | `DEPENDENCY_ACCEPTED_FINDINGS.md` synced to `.txt` |
| Release docs | Cite policy / evidence | RELEASE_PROCESS, PROTOCOL, CHECKLIST, fingerprint, Quality Manual, Playbook |

---

## 3. Gate mapping (P-002.1)

| Gate criterion | How advanced |
|----------------|--------------|
| G10.5 Dependency audit | Hard CI gate + HOLD register + reproducible script |
| G10.1 / G10.2–G10.4 / G10.6–G10.7 | Unchanged (not in scope) |
| G11 | Fingerprint notes hard dependency job; integrity tests extended |

Educational G1–G6: **not in scope** (frozen).

---

## 4. Explicit non-claims

| Item | Why not claimed |
|------|-----------------|
| Version 1 production-ready | ER-RB-02…04 (privacy), 06; educational G1–G6 |
| Flask advisory eliminated | HOLD only; bump = ER-TD-M04 |
| Privacy pack complete | ER-RB-04 residual |
| Application behaviour change | Forbidden by WP |

---

**End of EI001_2_TRACEABILITY_MATRIX**
