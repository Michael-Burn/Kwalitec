# RF-002 — Risk Register

**Programme:** RF-002 Educational System Verification  
**Date:** 2026-07-31  
**Method:** Educational / operational / architectural / deployment / debt classification

---

## Summary

| ID | Class | Title | Impact | Likelihood | Priority |
|----|-------|-------|--------|------------|----------|
| R1 | Deployment | SB-001A / BF-001 not live | High | Certain (today) | **P0** |
| R2 | Deployment | Multiple Alembic heads | High | High if cutover attempted | **P0** |
| R3 | Educational | Runtime C Twin birth skip | Medium | Medium (published curricula) | P1 |
| R4 | Educational | Narrow Baseline Home gate | Medium | Low | P2 |
| R5 | Architectural | No DB unique on complete Baseline | Medium | Low | P2 |
| R6 | Educational | Founder reset leaves Twin current | Low–Medium | Low | P2 |
| R7 | Technical Debt | Session finish → summary test drift | Low | Certain (tests) | Accepted |
| R8 | Technical Debt | Full-tree pytest residual (RF-001) | Low for learning | Certain | Accepted |
| R9 | Operational | Manual Deploy dependency | Medium | Medium | P1 |
| R10 | Architectural | Thin Runtime C SCI seed | Medium | Accepted | Accepted |

---

## R1 — SB-001A / BF-001 not on live

- **Class:** Deployment  
- **Impact:** High — live students still on pre-Baseline Calibration path; Founder cannot validate new continuity on production. Studio Expand/Collapse still broken on live until BF-001 cutover.  
- **Likelihood:** Certain until Manual Deploy.  
- **Mitigation:** Commit, merge Alembic heads, Manual Deploy, verify `/baseline` + Studio JS.  
- **Recommendation:** Treat as hard precondition for live G1 Baseline claims.

## R2 — Multiple Alembic heads

- **Class:** Deployment  
- **Impact:** High — `student_baselines` may not apply; startup cannot determine migration state.  
- **Likelihood:** High if deploy proceeds without merge.  
- **Mitigation:** Create Alembic merge of `202607300005` × `202607310001` before production migrate.  
- **Recommendation:** Block production migrate until merge exists.

## R3 — Runtime C Twin birth may skip

- **Class:** Educational  
- **Impact:** Medium — Baseline + enrolment succeed; Twin-authoritative intelligence may be absent (`TwinAbsent`).  
- **Likelihood:** Medium for `curriculum_version=published` without loadable JSON id.  
- **Mitigation:** Honest user message already; follow-on to resolve curriculum id for published packages (out of RF-002 scope).  
- **Recommendation:** Accept for G1 with disclosure; monitor TwinAbsent rate post-cutover.

## R4 — Narrow Baseline gate (Home only)

- **Class:** Educational  
- **Impact:** Medium if deep-linked to journey/revision without complete Baseline while an active plan exists.  
- **Likelihood:** Low (primary entry is Home).  
- **Mitigation:** Home gate + finalize-before-Home ordering; optional extend gate to other student routes in a future polish programme.  
- **Recommendation:** Accept for G1; not Category A on happy path.

## R5 — Application-level uniqueness only

- **Class:** Architectural  
- **Impact:** Medium under concurrent double-finalize race.  
- **Likelihood:** Low (single user wizard).  
- **Mitigation:** Finalize refuses non-draft; plan create deactivates prior actives; Twin duplicate birth blocked.  
- **Recommendation:** Optional unique partial index later; not blocking G1.

## R6 — Founder reset vs Twin current

- **Class:** Educational  
- **Impact:** Low–Medium — Baseline superseded; Twin snapshot remains current until new evidence/birth path. History preserved (correct).  
- **Likelihood:** Low (Founder-only).  
- **Mitigation:** Document that reset requires student re-Baseline; Twin not deleted (history-safe).  
- **Recommendation:** Accept; clarify in Founder UI copy if confusion arises.

## R7 — Session finish redirect test debt

- **Class:** Technical Debt  
- **Impact:** Low — tests expect `/student`; product lands on Sitting Report (RC-002 intentional). Learning continuity intact.  
- **Likelihood:** Certain in residual suite.  
- **Mitigation:** Already classified RF-001A Category D.  
- **Recommendation:** Do not treat as educational defect.

## R8 — Full-tree pytest residual

- **Class:** Technical Debt  
- **Impact:** Low for daily learning (RF-001A: 0 Category A).  
- **Likelihood:** Certain until dedicated zero programme.  
- **Mitigation:** Carry RF-001A accepted debt.  
- **Recommendation:** Do not open polish programme inside RF-002.

## R9 — Manual Deploy process

- **Class:** Operational  
- **Impact:** Medium — code on `main` does not reach students until Manual Deploy.  
- **Likelihood:** Medium (human step).  
- **Mitigation:** Explicit cutover checklist in Deployment Verification.  
- **Recommendation:** Founder / ops owns the button after merge green.

## R10 — Thin Runtime C SCI seed

- **Class:** Architectural / accepted debt  
- **Impact:** Medium — SCI not seeded from Baseline declarations.  
- **Likelihood:** Accepted by SB-001A design.  
- **Mitigation:** Ordering gate + Baseline row; no SCI redesign in RF-002.  
- **Recommendation:** Track as future educational enrichment, not G1 blocker.

---

## Category A educational defects

**None identified** on the RF-002 candidate for the verified lifecycle.

Residual issues are deployment cutover, accepted thin-bridge debt, or presentation/test debt already classified under RF-001A.
