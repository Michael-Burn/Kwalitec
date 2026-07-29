# CQ-007 — Known Issues

**Programme:** CQ-007 — Internal Alpha Readiness Review  
**Release Candidate:** `RC-2026.07.29-01`  
**Date:** 2026-07-29  
**Designation:** Alpha Candidate 1

Severity model for this review:

| Class | Meaning | Blocks Internal Alpha? |
|---|---|---|
| **P0** | Critical — publication, discovery, enrol start, data integrity, or safety gate broken | **Yes** |
| **P1** | Major — trust / guidance / ops discipline issues that slow Alpha but do not stop core loops | No |
| **P2** | Moderate — evidence gaps or polish that Alpha can absorb | No |
| **P3** | Minor — backlog / nicety | No |

---

## P0 — Critical

| ID | Summary | Source | Status | Blocks Alpha? |
|---|---|---|---|---|
| — | *None unresolved* | — | — | — |

Cleared P0-class defects (historical):

| Cleared | How |
|---|---|
| Validation never passes / Ready unreachable | PI-002R + EV-001 + FV-001B Final (RC) |
| Choose Exam HTTP 500 on Ready subjects | EE-001 + FV-001C |
| Approve shown as Publish refusal | PI-002R + FV-001B Final (RC) |
| Stale-environment false NO-GO treated as product failure | EV-002 Case D + RC-001 protocol |

---

## P1 — Major (track during Alpha)

| ID | Summary | Source | Blocks Alpha? | Alpha action |
|---|---|---|---|---|
| P1-01 | Stale NEXT STEP after docs Ready / after Publish | FV-001B UX-01 | No | Document for testers; fix after Alpha unless escalates |
| P1-02 | Findings panel contradicts Validation passed / 0 errors | FV-001B UX-02 | No | Testers trust Status + Publish outcome; fix trust chrome post-Alpha |
| P1-03 | Workflow stage strip lags Status Published | FV-001B UX-03 | No | Use Status / Subjects Ready as truth |
| P1-04 | Coming Soon catalogue density on Choose Exam | FV-001C UX-S01 | No | Coach testers to Ready-first row |
| P1-05 | RC dirty tree — code image digest-bound, not clean commit | RC-001 Condition 1 | No | Freeze discipline; clean re-cert before commercial gates |
| P1-06 | Alpha must not reuse stale Flask / wrong DB (EV-002 Class D) | EV-002 / RC-001 | No | Bind runtime + DB to certificate; restart = new RC |

---

## P2 — Moderate

| ID | Summary | Source | Blocks Alpha? | Alpha action |
|---|---|---|---|---|
| P2-01 | Topic count Overview 28 vs Preview 23 | FV-001B UX-04 | No | Backlog |
| P2-02 | Dual-role login lands on Console | FV-001C UX-S02 | No | Use dedicated student accounts or bookmark Study Plan |
| P2-03 | Post-enrol Student Home / Today's Focus not primary E2E screenshot package | FV-001C Phase 6 | No | Capture during Alpha dogfood |
| P2-04 | Availability minutes need example values | FV-001C UX-S03 | No | Backlog |
| P2-05 | Commercial monitoring / live rollback drill not re-certified in CQ-007 | Ops evidence inheritance | No | Use existing runbooks; tabletop acceptable for invite-only Alpha |

---

## P3 — Minor

| ID | Summary | Source | Blocks Alpha? |
|---|---|---|---|
| P3-01 | Console Home operations-first (extra click to Studio) | FV-001B UX-05 | No |
| P3-02 | Prefer clean-tree RC ID for marketing / external packaging | RC-001 recommendation | No |

---

## Operational residuals (classified)

| Area | Assessment | Class | Blocks Alpha? |
|---|---|---|---|
| Logging | Privacy-safe observability guide + pipeline event patterns exist (`knowledge/release/OBSERVABILITY_GUIDE.md`) | P2 (not re-probed on RC) | No |
| Error handling | Studio flash recovery improved (Approve vs Publish); Flask error pages present | P1 residual only for findings honesty | No |
| Recovery | Session resume / sole-runtime rollback playbooks exist from prior release programmes | P2 | No |
| Deployment | RC local Flask certification; Render/production deploy not re-run in CQ-007 | P2 | No |
| Rollback | Flag / sole-runtime / prior tagged baseline playbooks documented; live drill not required for invite-only Alpha | P2 | No |
| Monitoring | `/health`, `/health/ready`, `/health/educational-intelligence` available; continuous external monitoring not Alpha gate | P2 | No |

---

## Unresolved P0 count

**0**

Alpha checklist item **No unresolved P0 issues** → **✓**
