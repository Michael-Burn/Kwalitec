# Risk Review Standard

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** P-003.3 Product Risk Register · Product Constitution PC-03–PC-04 · Operational Architecture  
**Constraint:** Process standard only — does not amend risk ratings by publication alone.

---

## 1. Purpose

Define how product and operational risks are identified, rated, reviewed, accepted, and closed so Version 1 and claim-class decisions remain honest.

**Authoritative product risk corpus:**

- `knowledge/product/p003_3_product_risk_register/PRODUCT_RISK_REGISTER.md`
- Companions: `ACTIVE_RISKS.md`, `CLOSED_RISKS.md`, `RISK_TRACEABILITY.md`, `RISK_REVIEW_PROCESS.md`

This OA-001 standard **aligns operating cadence** with that corpus. It does not replace P-003.3 card formats or ID scheme (`PR-NNN`).

---

## 2. What must be managed as a risk

Material exposure that could:

- Block Version 1 production-ready declaration.
- Harm student trust or educational integrity.
- Invalidate engineering claim class (security, CI, performance, deploy).
- Cause privacy / enrollment violations.
- Allow marketing claims beyond evidence.

Technical debt is related but distinct — use Technical Debt Governance for intentional compromises; escalate to the Risk Register when the compromise threatens release or trust outcomes.

---

## 3. Rating model

Use the P-003.3 Likelihood × Impact matrix and Overall band (Green / Amber / Red). Control adjustment may reduce Overall by one band when documented as `ACTIVE (controlled)`.

Every active risk requires:

- Owner capacity  
- Current controls  
- Residual rating  
- Next review date  
- Forbidden claims (if any) while open  

---

## 4. Review cadence

| Cadence | Scope | Owner |
|---------|-------|-------|
| **Per programme completion** | New risks introduced; existing risks affected | Programme lead + Product Owner |
| **Per release / claim-class change** | Risks that gate the claim | Operations + Product Board Chair |
| **Quarterly** | Full active register sweep | Product Owner |
| **Triggered** | Incident, audit finding, HOLD lift attempt, Stage 1 expansion proposal | Domain owner |

Triggered reviews are mandatory under Operational Architecture certification triggers when risks map to gate failures.

---

## 5. Review procedure

1. **Inventory** — pull ACTIVE / WATCH / ACCEPTED from P-003.3.  
2. **Evidence check** — each risk cites current artefacts; drop unsupported inventions.  
3. **Re-rate** — Likelihood / Impact / Overall; document control changes.  
4. **Disposition** — mitigate · accept · watch · close · escalate to programme.  
5. **Claim binding** — update forbidden/allowed claim language.  
6. **Record** — update register companions; note summary on Programme Dashboard.  
7. **Independence** — educational risks are not “cleared” by engineering mitigations alone (and vice versa).

---

## 6. Acceptance rules

A risk may be **ACCEPTED** only when:

1. Residual is explicit and time-bounded or claim-bounded.  
2. Owner is named.  
3. Forbidden claims are listed.  
4. Product Board Chair (or capacity equivalent) records Founder Review.  
5. Acceptance does not silently satisfy a P-002.1 hard gate (gates remain FAIL/HOLD until evidence clears them).

Accepted risks under invite-only Alpha (e.g. G7 HOLD operational posture) remain visible on the Dashboard.

---

## 7. Closure rules

Close only when evidence shows the exposure is gone or permanently out of scope, with traceability to verifying artefacts. Prefer `CLOSED_RISKS.md` history over deletion.

---

## 8. Audit and engineering findings

ER-style non-compliance items become:

- **Risk entries** when they threaten claim class or release success, and/or  
- **Debt entries** when they are intentional deferrals with remediation plans.

Cross-link IDs (`ER2-NC-…`, `PR-…`, `TD-…`) in all affected registers.

---

**End of Risk Review Standard**
