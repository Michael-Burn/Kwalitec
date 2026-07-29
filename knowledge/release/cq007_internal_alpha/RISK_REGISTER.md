# CQ-007 — Risk Register

**Programme:** CQ-007 — Internal Alpha Readiness Review  
**Release Candidate:** `RC-2026.07.29-01`  
**Date:** 2026-07-29  
**Designation:** Alpha Candidate 1

Likelihood × Impact for invite-only Internal Alpha (not Version 1 commercial declaration).

| ID | Risk | Likelihood | Impact | Class | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R-01 | Testers invalidate RC by editing frozen worktree or switching DB/port | Medium | High | P1 | Enforce RC citation + digest check before each Alpha session | Release / Founder |
| R-02 | Stale NEXT STEP / findings chrome causes Founder to abandon a healthy publish path | Medium | Medium | P1 | Alpha briefing: trust Status Published + Subjects Ready | Product |
| R-03 | Coming Soon density hides Ready subject for new student testers | Medium | Medium | P1 | Ready-first coaching; optional catalogue sort later | Product |
| R-04 | Environment mismatch recreates EV-002 false defect reports | Medium | High | P1 | Fresh process only after re-cert; never judge against orphan ports | Engineering |
| R-05 | Dirty-tree digest drift silently invalidates Alpha Candidate 1 | Medium | High | P1 | Recompute digest; any mismatch → stop / re-RC | Engineering |
| R-06 | Post-enrol Home surprises not caught by FV-001C package | Medium | Medium | P2 | Capture Home / Today's Focus in first Alpha week | Product / QA |
| R-07 | Topic count inconsistency erodes Founder trust in structure completeness | Low | Low | P2 | Single authoritative count backlog | Engineering |
| R-08 | Invite-only Alpha expands without dedicated student seed accounts | Medium | Low | P2 | Provision student-only accounts; avoid dual-role Console landing | Ops |
| R-09 | Production deploy differs from certified local RC | Low* | High | P2 | Treat Alpha Candidate 1 as local/RC-bound until deploy fingerprint matches | Release |
| R-10 | P0 appears in live Alpha use (unknown defect) | Low | Critical | P0 trigger | Pause Alpha; open defect programme; no other eng work until closed | All |

\*Likelihood low for *declared* local Alpha; rises if Alpha is silently moved to an uncertified host.

---

## Accepted risks for Alpha start

The following are **accepted** for Internal Alpha begin:

- P1 usability chrome residuals (R-02, R-03)  
- Digest-bound dirty tree (R-01, R-05) with operational freeze discipline  
- Incomplete Home E2E packaging (R-06)  
- Ops monitoring/rollback not re-drilled in CQ-007 (R-09 residual)

---

## Escalation

| Trigger | Action |
|---|---|
| Confirmed P0 (publish/discover/enrol-start/safety broken) | Pause Alpha; defect programme; engineering authorised only for that P0 |
| Digest or binding mismatch | Invalidate Alpha Candidate 1 evidence; re-run RC-001 |
| New Major usability only | Track as P1; do **not** open engineering programme before Alpha ends unless Founder escalates |

---

## Risk posture summary

Residual risk is **compatible with invite-only Internal Alpha**. It is **not** a Version 1 production-ready declaration.
