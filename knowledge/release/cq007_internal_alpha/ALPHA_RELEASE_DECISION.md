# CQ-007 — Alpha Release Decision

**Programme:** CQ-007 — Internal Alpha Readiness Review  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01`

---

## Formal decision

# APPROVED WITH CONDITIONS

Internal Alpha may begin.

Conditions are tracked.

---

## Designation

```text
Alpha Candidate 1
```

Bound to:

| Field | Value |
|---|---|
| Release Candidate | `RC-2026.07.29-01` |
| Commit | `f17058862baf9aa8c6f416c6fa7bd26739812fb8` |
| Worktree digest | `5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e` |
| Application version | `2.0.0` |

---

## Decision options (exclusive)

| Option | Selected? |
|---|---|
| APPROVED | No |
| **APPROVED WITH CONDITIONS** | **Yes** |
| NOT APPROVED | No |

---

## Alpha Readiness Checklist (decision basis)

| Criterion | Result |
|---|---|
| Founder can publish | ✓ |
| Student can discover | ✓ |
| Student can enrol | ✓ |
| Ready state reliable | ✓ |
| Validation reliable | ✓ |
| Release Candidate reproducible | ✓ |
| Critical regressions closed | ✓ |
| No unresolved P0 issues | ✓ |

---

## Conditions of approval

1. Alpha testing cites **Release Candidate: RC-2026.07.29-01** and respects RC invalidation rules.  
2. P1–P3 issues in [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) remain tracked; they do not block start.  
3. No further engineering programmes before Alpha unless a **P0** is discovered.  
4. A clean-tree re-certification is recommended before commercial / external gates (not required to begin Internal Alpha).

---

## Authorised next actions

1. **Begin internal testing** on Alpha Candidate 1.  
2. Collect Founder and student dogfood against the frozen RC (or exact certified copy).  
3. Escalate only on P0; otherwise log Alpha findings against the known-issue register.  
4. Do not treat this decision as Version 1 production-ready or commercial launch approval.

---

## Evidence package

| Document |
|---|
| [`CQ007_EXECUTIVE_SUMMARY.md`](CQ007_EXECUTIVE_SUMMARY.md) |
| [`ENGINEERING_READINESS.md`](ENGINEERING_READINESS.md) |
| [`PRODUCT_READINESS.md`](PRODUCT_READINESS.md) |
| [`QUALITY_READINESS.md`](QUALITY_READINESS.md) |
| [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) |
| [`RISK_REGISTER.md`](RISK_REGISTER.md) |

Upstream programme roots: PI-002, PI-002R, EV-001, EE-001, EV-002, RC-001, FV-001B Final (`fv001b_final_rc001`), FV-001C.

---

## Sign-off statement

On the evidence reviewed for CQ-007, Kwalitec is **ready for invite-only Internal Alpha** as **Alpha Candidate 1**, subject to the conditions above.

```text
Decision: APPROVED WITH CONDITIONS
Designation: Alpha Candidate 1
Release Candidate: RC-2026.07.29-01
```
