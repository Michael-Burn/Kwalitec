# Change Management Standard

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** Operational Architecture · Product Constitution · `knowledge/GOVERNANCE.md`  
**Constraint:** Process standard only.

---

## 1. Purpose

Classify every material change so the correct lifecycle, owners, reviews, and evidence apply. Misclassification is a common path to skipped educational review or overclaimed releases.

---

## 2. Change classes

| Class | Definition | Primary lifecycle | Typical owner |
|-------|------------|-------------------|---------------|
| **Product / Feature** | New or material student/product capability | `FEATURE_LIFECYCLE.md` | Product Owner |
| **Architecture** | Boundaries, authority, dual paths, composition, curriculum contracts | ADR Standard → implement | Engineering Owner (architecture) |
| **Governance** | Constitutions, lexicons, standards, operating model, claim policy | Draft → Founder Review → publish | Educational Gate or Product Owner by topic |
| **Engineering** | CI, dependencies, performance evidence, security hardening, reliability packs | Engineering Standards + audit/recert as needed | Engineering Owner |
| **Release** | Shipping a version under a claim class | Release Governance Model | Operations Owner |
| **Hotfix** | Urgent production corrective | Hotfix lifecycle | Operations + Engineering |
| **Risk / Debt** | Register updates, Accepted Residuals, remediation programmes | Risk / Debt standards | Product or Engineering |
| **Docs-only** | Knowledge with no behaviour or authority change | Lightweight review | Authoring owner |
| **Audit / Certification** | Independent assessment without remediation | Audit programme charter | Domain auditor capacity |

A single programme may span classes; the **strictest** applicable review set wins.

---

## 3. Classification checklist (mandatory)

Before starting implementation or publishing authority docs, answer:

1. Does this change student-facing behaviour or educational speech? → Feature (+ Educational reviews as needed)  
2. Does this change who owns educational truth or runtime boundaries? → Architecture ADR required  
3. Does this amend law (Vision, EGI, DG-001, Architecture Constitution, OA-001 principles)? → Governance class  
4. Does this affect CI, authn/authz, dependencies, deploy, or performance claims? → Engineering class  
5. Does this deploy or retag production? → Release or Hotfix  
6. Does this only describe existing truth? → Docs-only (verify it does not silently redefine)

Record the class in the PRD, programme brief, or completion report.

---

## 4. Governance change process

For constitutions, operational standards, and claim policy:

1. **Draft** amendment with rationale, impacted principles/IDs, and downward impact.  
2. **Conflict check** against Vision 2030, EGI-001, DG-001, Architecture Constitution, GOVERNANCE.md.  
3. **Founder Review** with required capacity lenses (Educational / Engineering / Privacy as implicated).  
4. **Publish** version bump + effective date.  
5. **Cascade** — update indexes / Dashboard; open implementation programmes if remediation required.  
6. **Never** implement educational behaviour changes inside a governance-only programme (DG-001 / OA-001 constraint pattern).

Educational governance amendments follow DG-001 `GOVERNANCE_AMENDMENT_PROCESS.md` when that instrument applies.

---

## 5. Engineering change process

1. Classify impact on gates G7–G12 and ER residuals.  
2. Prefer additive fixes with tests; update dependency / security policies in their authoritative files.  
3. If claim class or HOLD posture changes, update recommendation / evidence packs and Dashboard.  
4. Material clearance of prior Critical findings warrants engineering recertification (ER-style), not self-certification inside the fix PR alone.  
5. Do not reopen educational baselines without educational evidence of regression or intentional programme authority.

---

## 6. Architecture change process

Follow `ARCHITECTURE_DECISION_RECORD_STANDARD.md`: Proposed ADR → review → Accepted → implement → enforce.

---

## 7. Approval matrix (summary)

| Class | Minimum approval |
|-------|------------------|
| Docs-only (no authority change) | Author + PR review |
| Hotfix | Engineering Owner; Operations for deploy |
| Feature (non-educational core) | Product + Engineering |
| Feature (educational intelligence) | Product + Educational Gate + Engineering |
| Architecture | Engineering (architecture) + Educational if authority touched |
| Governance (OA / meta) | Product Owner; Educational/Engineering lenses as needed |
| Governance (educational DG-001) | Educational Gate Owner per DG-001 |
| Release (invite-only) | Operations; observe ER-002 conditions |
| Version 1 declaration | Product Board Chair after full P-002.1 evidence |

GP-001 founder-operated capacities apply; independence of *assessment* still required for educational vs engineering conclusions.

---

## 8. STOP conditions

STOP and escalate when:

- Classification is disputed and implementation has started.  
- A “docs” change would alter educational meaning or claim rights.  
- Marketing copy needs a stronger claim than filed evidence.  
- ADR is still Proposed but code is ready to merge.  
- Hotfix scope creeps into feature work.

---

**End of Change Management Standard**
