# Release Governance Model

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** Release Playbook · Release Protocol · P-002.1 · EVF · ER-002 · Product Constitution PC-02–PC-04  
**Constraint:** Governance model only — does not modify release artefacts or deploy configuration.

---

## 1. Purpose

Define how **releases** and **hotfixes** are classified, authorised, executed, evidenced, and constrained by claim class — without collapsing educational and engineering assessments.

**Procedure detail** remains in:

- `knowledge/RELEASE_PLAYBOOK.md` (operator summary)
- `docs/process/RELEASE_PROTOCOL.md` (canonical steps)

This model states **governance rules** those procedures must satisfy.

---

## 2. Independence of boards

| Board | Question | May authorise |
|-------|----------|---------------|
| **Educational (EVF + DG-001)** | Is educational quality / governance sufficient for the educational claims? | Educational trust claims |
| **Engineering (P-002.1 G7–G12 + ER)** | Is the system operable/safe for the engineering claim class? | Engineering claim class (e.g. invite-only Alpha) |
| **Product (P-002.1 full + P-003.1)** | May we declare Version 1 production-ready? | V1 production-ready language |

**PC-02:** Passing one board never implies the others.

Current baseline (contextual, not reassessed by OA-001):

- Engineering: **Conditional GO** (ER-002) for invite-only Internal Alpha under conditions C1–C7.
- Product Version 1: **NO GO** while educational hard gates (notably G1) remain FAIL.

---

## 3. Release lifecycle

```
Classify → Pre-verify → Governance artefacts → Stage → Tag/Push → Deploy → Fingerprint → Smoke → Communicate → Report → Operate
```

| Stage | Governance requirement |
|-------|------------------------|
| **Classify** | Change class + claim class + educational vs engineering impact |
| **Pre-verify** | Clean tree; tests/lint as class requires; architecture artefacts present |
| **Governance artefacts** | ADRs Accepted; EVF gate if educational claims; HOLDs observed |
| **Stage / Tag** | Intentional release commit; never force-push `main`; no secrets |
| **Deploy** | Per `docs/production/DEPLOYMENT.md` |
| **Fingerprint** | Prove expected version live (`app/version.py` / tag) |
| **Smoke** | Protocol + GA checklist; sole-runtime home reachable |
| **Communicate** | Claim language ≤ evidence; G12 flag honesty |
| **Report** | Release report; update Readiness / Dashboard if status changes |
| **Operate** | Watch residuals; renewal triggers per Operational Architecture §9 |

---

## 4. Release classes

| Class | Typical content | Extra gates |
|-------|-----------------|-------------|
| **Docs / governance** | Knowledge only | No deploy required; still update Dashboard |
| **Hotfix** | Urgent production correctives | Hotfix lifecycle (§5); minimal scope |
| **Feature** | Significant capability | Feature Lifecycle complete through Independent Review |
| **Architecture** | Boundary / ADR-backed | Accepted ADR; architecture tests green |
| **Migration** | Schema / data | Alembic discipline; backup/restore readiness |
| **Alpha / invite-only** | Cohort-facing under Alpha claims | ER-002 conditions; G7 HOLD; Contained disclosure |
| **Production-ready declaration** | V1 claim | Full P-002.1 evidence package + Product Board |

---

## 5. Hotfix lifecycle

Hotfixes optimise for **speed with containment**, not for skipping safety.

```
Detect → Triage → Branch from last known good → Minimal fix → Verify → Review → Deploy → Fingerprint → Smoke → Report → Follow-up debt/ADR
```

| Rule | Requirement |
|------|-------------|
| **Scope** | Fix the incident only; no opportunistic refactors |
| **Branch** | From last known good tag/commit when practical |
| **Verify** | Targeted tests + smoke; full suite before promoting claim class |
| **Review** | Engineering Owner accountable; second lens if educational path touched |
| **Educational algorithms** | No casual patches; Document → Recommend; Educational Gate if integrity incident |
| **Rollback** | Prefer redeploy last good tag over forward-fix gambling |
| **Follow-up** | File TD / risk / programme for proper remediation if hotfix is temporary |

Hotfixes **do not** authorise new marketing claims or lift HOLDs.

---

## 6. Claim language governance

Before any external or board-facing statement about a release:

1. Cite the engineering recommendation (e.g. ER-002 Conditional GO + conditions).  
2. Cite educational / Product board status if educational or V1 claims are made.  
3. List active HOLDs and Contained disclosures.  
4. Confirm G12 flag matrix matches what is marketed.  
5. If evidence is missing → **STOP** (PC-03, PC-12).

Forbidden examples (illustrative): “Engineering GO for Version 1” while Conditional; “G7 PASS” under HOLD; “fully converged runtime” while Contained dual-stack remains.

---

## 7. Rollback governance

| Situation | Action | Record |
|-----------|--------|--------|
| Bad fingerprint | Redeploy last known good | Release report |
| Critical functional break | Rollback; hotfix branch | Incident + report |
| Educational integrity incident | STOP cohort use if needed; no silent algorithm rewrite | Educational + ops records |
| Migration failure | Protocol rollback / restore | Backup evidence |

Do not destroy evidence needed for postmortem or recertification.

---

## 8. Certification linkage

A release that changes material gates or claim class triggers certification renewal per Operational Architecture §9. Routine invite-only deploys under unchanged ER-002 conditions do not themselves renew or strengthen certification.

---

**End of Release Governance Model**
