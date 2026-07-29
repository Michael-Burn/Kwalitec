# CQ-007 — Executive Summary

**Programme:** CQ-007 — Internal Alpha Readiness Review  
**Status:** Complete  
**Date:** 2026-07-29  
**Method:** Evidence review only — no implementation; no UX re-validation  
**Release Candidate:** `RC-2026.07.29-01`

---

## Decision

# APPROVED WITH CONDITIONS

Internal Alpha may begin.

Conditions are tracked in [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) and [`RISK_REGISTER.md`](RISK_REGISTER.md).

**Designation:** Alpha Candidate 1

---

## Binding

| Binding | Value |
|---|---|
| Release Candidate | `RC-2026.07.29-01` |
| Commit | `f17058862baf9aa8c6f416c6fa7bd26739812fb8` |
| Worktree digest | `5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e` |
| Application version | `2.0.0` |
| Runtime (certified) | `http://127.0.0.1:5201` |
| Database (certified) | `sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3` |

---

## Evidence chain reviewed

| Programme | Outcome | Role in Alpha decision |
|---|---|---|
| PI-002 | Root cause found (validation stub AND-gate) | Explains prior NO-GO |
| PI-002R | Resolved — single validation authority | Publication gate fixed |
| EV-001 | VERIFIED WITH MINOR CONDITIONS | Studio Draft → Ready proved |
| EE-001 | Complete — catalogue projection fixed | Choose Exam 500 cleared |
| EV-002 | Case D — environment mismatch | Invalidated stale FV Final NO-GO vs EV |
| RC-001 | CERTIFIED WITH CONDITIONS | Frozen reproducible environment |
| FV-001B Final (RC) | GO WITH CONDITIONS | Founder publish path validated |
| FV-001C | GO WITH CONDITIONS | Student discovery / enrol start validated |

---

## Alpha Readiness Checklist

| Criterion | Status | Evidence |
|---|---|---|
| Founder can publish | ✓ | FV-001B Final on RC — Create → Ready |
| Student can discover | ✓ | FV-001C — CS1V Ready on Choose Exam |
| Student can enrol | ✓ | FV-001C — CS1V selectable; wizard advances |
| Ready state reliable | ✓ | EV-001 + FV-001B Ready · Version · Date |
| Validation reliable | ✓ | PI-002R + EV-001 + FV-001B passed validation |
| Release Candidate reproducible | ✓ | RC-001 certificate (digest-bound) |
| Critical regressions closed | ✓ | PI-002 defect remediated; RC re-validation cleared prior blockers |
| No unresolved P0 issues | ✓ | No P0 in FV-001B/C or engineering exit criteria |

---

## Why not unconditional APPROVED

1. RC certified against a **dirty working tree** (digest waiver).  
2. Residual **Major usability** conditions (stale NEXT STEP, findings trust friction, Coming Soon density).  
3. Post-enrol Student Home path packaged with lower evidence confidence than discovery.  
4. Invite-only Alpha operational posture relies on existing runbooks; commercial monitoring/rollback drills are not re-certified in this review.

None of these are P0 publication or discovery blockers.

---

## Why not NOT APPROVED

The critical publication failure chain from PI-002 is closed. On the frozen RC, a Founder published CS1V to Ready and a student discovered and selected it without HTTP 500. Safety gates remain enforced. No unresolved P0 remains.

---

## Exit actions authorised

1. Treat **Alpha Candidate 1** as the internal Alpha build designation for `RC-2026.07.29-01`.  
2. Begin internal Alpha testing on this RC (or an exact certified copy).  
3. **No further engineering programmes before Alpha** unless a **P0** defect is discovered.  
4. Track P1–P3 conditions during Alpha; schedule remediation after Alpha feedback unless a condition escalates to P0.

---

## Deliverables

| Artefact | Purpose |
|---|---|
| [`ENGINEERING_READINESS.md`](ENGINEERING_READINESS.md) | Pipeline, discovery, authority, validation, reliability |
| [`PRODUCT_READINESS.md`](PRODUCT_READINESS.md) | Founder/student workflow, navigation, terminology, learnability |
| [`QUALITY_READINESS.md`](QUALITY_READINESS.md) | Regression, coverage, RC integrity |
| [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) | P0–P3 register + Alpha block status |
| [`RISK_REGISTER.md`](RISK_REGISTER.md) | Residual Alpha risks |
| [`ALPHA_RELEASE_DECISION.md`](ALPHA_RELEASE_DECISION.md) | Formal decision record |
