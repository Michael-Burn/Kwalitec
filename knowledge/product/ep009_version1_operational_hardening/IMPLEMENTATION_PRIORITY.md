# EP-009 — Implementation Priority

**Programme:** EP-009 — Version 1 Operational Hardening  
**Date:** 2026-07-26  
**Authority:** [`ISSUE_TRIAGE.md`](ISSUE_TRIAGE.md)  
**Rule:** Only **Critical** and **High** are candidates for work before Stage 1 external invites.  
**Does not:** Schedule Runtime A, recommendation ranking, or educational feature work  

---

## Board one-liner

> Fix live rights/rollback evidence (Critical) and the dual-export + account-deletion operator docs (High) before Stage 1. Defer self-serve delete UI and registration wording polish.

---

## Priority bands

| Band | Meaning | Stage 1 rule |
|---|---|---|
| **Critical** | Enrollment-blocking operational evidence or control failure | Must close (or remain HOLD) before invites |
| **High** | Material risk of rights/SLA failure for first external participants | Must close before invites |
| **Medium** | Real gap; Stage 1 operable with documented workaround | After pilot / after first cohort start |
| **Low** | Clarity / hygiene | Anytime; not a gate |

---

## Pre-Stage 1 candidates (Critical + High)

| Rank | Work item | Issue IDs | Severity | Type | Owner capacity | Target artefact / evidence |
|---:|---|---|---|---|---|---|
| **1** | Execute and file export dry-run Pass | ISSUE-003 → CE-03 | Critical | Operational execution | Operations Owner | `GO_LIVE_CHECKLIST.md` §E1 |
| **2** | Execute and file deletion dry-run Pass (full cascade) | ISSUE-003 → CE-04; uses ISSUE-005 checklist | Critical | Operational execution | Operations Owner + Privacy Owner | §E2 + audit Yes; **FND-TST-DEL** only |
| **3** | Execute and file kill-switch rehearsal Pass | ISSUE-003 → CE-05 | Critical | Operational execution | Operations Owner / on-call | §E3 + Rollback §3.3 |
| **4** | Publish Account Deletion Checklist | ISSUE-005 + ISSUE-001 (ops half) | High | Documentation | Operations Owner + Privacy Owner | New checklist under EP-008.2B or Privacy Ops; no UI |
| **5** | Publish dual-export operator card | ISSUE-002 | High | Documentation | Operations Owner | Invite/support pack + Stage 1 checklist two-row table |

### Sequencing

```text
(4) Account Deletion Checklist  ─┐
(5) Dual-export operator card   ─┼─→ docs ready
                                 │
(1) Export dry-run §E1           ┤
(2) Deletion dry-run §E2         ├─→ Critical EVIDENCED path (OP-001)
(3) Kill-switch §E3 / R1         ┘
```

Checklist (4) should exist **before** deletion dry-run (2) so CE-04 exercises the full cascade, not analytics-only.

Items 1–3 are **human evidence**, not application builds. EP-009 does not invent Passes; OP-004 live window Days 3–5 remain the preferred execution slot.

---

## Deferred past Stage 1 start (Medium / Low)

| Rank | Work item | Issue IDs | Severity | Type | Rationale for deferral |
|---:|---|---|---|---|---|
| **6** | Self-serve “delete my account” in Settings | ISSUE-001 (UI half) | Medium | Application | Stage 1 is invite-only with named support; written ops path + CE-04 Pass is sufficient for first cohort rights. UI is product polish, not enrollment honesty. |
| **7** | Board/invite “Registration” → “controlled provisioning” wording pass | ISSUE-004 | Low | Documentation | Already DOCUMENTED; DR-034 unchanged; no defect. |

---

## Explicitly out of EP-009 priority (still Stage 1 blockers)

Track in OP-001 / OP-002 — **do not** treat as founder-pilot hardening builds:

| Item | Severity for Stage 1 | Why not EP-009 build |
|---|---|---|
| CE-01 Privacy signatures | Critical | Governance / Founder Review; not OP-004 Day-0 defect |
| CE-02 Named owners §E4 | Critical (enrollment) | Confirmation gap; docs already DOC READY |
| Recommendation / Runtime A / Twin flags | N/A | Forbidden by programme constraints |

---

## Implementation type counts (pre-Stage 1)

| Type | Count | IDs |
|---|---:|---|
| Operational execution (evidence) | 3 | ISSUE-003 → CE-03, CE-04, CE-05 |
| Documentation | 2 | ISSUE-002; ISSUE-005 (+ ISSUE-001 ops) |
| Application code | **0** | Self-serve delete deferred (Medium) |
| Runtime A / recommendation / educational reasoning | **0** | Forbidden |

---

## Decision record (why each call)

| Decision | Why |
|---|---|
| ISSUE-003 = Critical | PB-001 / OP-001: any of CE-03…CE-05 without evidence → HOLD |
| ISSUE-002 = High pre-Stage 1 | Wrong export artefact breaks privacy SLA honesty for first externals |
| ISSUE-005 + ISSUE-001 ops = High pre-Stage 1 | CE-04 cannot be complete without educational + analytics cascade |
| ISSUE-001 UI = Medium post-pilot | Ops path meets Stage 1 rights; UI expands product scope beyond founder-pilot hardening |
| ISSUE-004 = Low | Wording already corrected in pilot plan; product posture correct |
| No educational / Runtime A work | OP-004 findings are operational; constraints forbid redesign |

---

## Definition of “done enough for Stage 1 reconsideration”

From founder-pilot issues alone:

1. Dual-export operator card filed in invite/support materials.  
2. Account Deletion Checklist published and used.  
3. §E1, §E2, §E3 (+ Rollback §3.3) contain real Pass evidence (or HOLD retained honestly).  

Still required outside EP-009: CE-01 signatures, CE-02 named-owner confirmation, Board acceptance, High enrollment T-07…T-11.

---

**End of IMPLEMENTATION_PRIORITY**
