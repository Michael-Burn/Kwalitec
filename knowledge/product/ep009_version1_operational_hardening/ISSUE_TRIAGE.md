# EP-009 — Issue Triage

**Programme:** EP-009 — Version 1 Operational Hardening  
**Date:** 2026-07-26  
**Source:** OP-004 Founder Operational Pilot (`ISSUE_REGISTER.md`, `OPERATIONAL_OBSERVATIONS.md`, `FOUNDER_PILOT_REPORT.md`)  
**Stage 1 context:** OP-001 / OP-002 (enrollment **HOLD**)  
**Does not:** Authorise invites; invent CE Passes; change Runtime A or recommendation logic  

---

## Triage method

For each OP-004 issue:

1. **Class** — documentation / workflow / application / operational (primary; secondary allowed).  
2. **EP-009 severity** — Critical / High / Medium / Low relative to **Stage 1 external invite readiness**.  
3. **Minimum appropriate solution** — smallest fix that closes the operational gap.  
4. **Pre-Stage 1?** — Only **Critical** and **High** are implementation candidates before Stage 1.

**Severity mapping note:** OP-004 used Pilot Runbook P0–P3. EP-009 reclassifies for **Stage 1 enrollment risk**, not Day-0 convenience. ISSUE-003 remains enrollment-Critical via OP-001 CE-03…CE-05 even though OP-004 labelled it P2 for the founder pilot.

---

## Summary matrix

| ID | Title | Primary class | Secondary | EP-009 severity | Pre-Stage 1 candidate? | Min solution type |
|---|---|---|---|---|---|---|
| **ISSUE-001** | No self-serve full account deletion in Settings | Application | Operational / Privacy | **High** (ops path); **Medium** (self-serve UI) | **Yes** — ops checklist only; **No** — UI | Docs + ops (UI deferred) |
| **ISSUE-002** | Dual export paths lack a single operator card | Documentation | Operational / Workflow | **High** | **Yes** | Docs (operator card) |
| **ISSUE-003** | CE-03/04/05 live evidence still blank | Operational | Evidence / Workflow | **Critical** | **Yes** | Ops execution + evidence filing |
| **ISSUE-004** | “Registration” wording vs invite-only | Documentation | — | **Low** | **No** | Docs hygiene (already DOCUMENTED) |
| **ISSUE-005** | No single account-deletion checklist | Documentation | Operational / Privacy | **High** | **Yes** | Docs (founder checklist) |

---

## ISSUE-001 — No self-serve full account deletion in Settings

| Field | Assessment |
|---|---|
| **Is this a documentation issue?** | Partially — Privacy Ops leaves educational-domain deletion as “existing support workflow” without a student-visible Settings control. |
| **Is this a workflow issue?** | Yes — withdrawal / full account exit requires an operator-run path, not a student click. |
| **Is this an application issue?** | Yes — Settings restore wipes/reimports learning rows; it is **not** privacy account deletion. No “delete my account” control found in Day-0 rehearsal. |
| **Is this an operational issue?** | Yes — Stage 1 support must fulfil withdrawal without guessing cascade steps. |
| **Risk if untreated before Stage 1** | Incomplete rights fulfilment (analytics wiped, educational rows remain — or reverse); CE-04 dry-run cannot be honest without a written full-account path. |
| **Minimum appropriate solution** | **Before Stage 1:** Publish a one-page **Account Deletion Checklist** (identity verify → analytics delete CLI → educational account disable/remove → audit confirm) and exercise it on **FND-TST-DEL** / staging twin. **Do not** require self-serve UI for Stage 1. |
| **Not in minimum scope** | Student Settings “delete my account” UI; Runtime A / recommendation changes; redesign of Settings restore. |
| **EP-009 severity** | **High** for checklist + operable ops path; **Medium** for self-serve UI (post-pilot candidate). |
| **Links** | OP-004 ISSUE-001; OBS-OPS-001; `PRIVACY_OPERATIONS_GUIDE.md`; EP-008.2B Privacy package §10; OP-001 CE-04 |

---

## ISSUE-002 — Dual export paths lack a single operator card

| Field | Assessment |
|---|---|
| **Is this a documentation issue?** | **Yes** — primary. |
| **Is this a workflow issue?** | Yes — operators may pick the wrong artefact under time pressure. |
| **Is this an application issue?** | No — both paths exist and Day-0 found them operable. |
| **Is this an operational issue?** | Yes — SLA / wrong-file delivery risk for future participants. |
| **Risk if untreated before Stage 1** | Learning backup delivered when analytics export was requested (or reverse); missed 14-day export SLA honesty. |
| **Minimum appropriate solution** | Add a **two-row operator card** to invite/support pack and Stage 1 checklist: (1) Learning backup — Settings `/settings/export/backup`; (2) Analytics events — `flask analytics-export-user <id>`. Cross-link Privacy Ops + Go-Live §E1. |
| **Not in minimum scope** | Merging export UIs; changing export payloads; recommendation/Runtime A work. |
| **EP-009 severity** | **High** |
| **Links** | OP-004 ISSUE-002; OBS-UX-001; EP-008.2A Pilot Runbook; Go-Live §E1 |

---

## ISSUE-003 — CE-03/04/05 live evidence still blank

| Field | Assessment |
|---|---|
| **Is this a documentation issue?** | No — procedures already exist (EP-008.2B packages COMPLETE). |
| **Is this a workflow issue?** | Partially — execution cadence during OP-004 live window Days 3–5. |
| **Is this an application issue?** | No (Day-0 path checks OK for export CLI / kill-switch tabletop). |
| **Is this an operational issue?** | **Yes** — primary. Missing dated human Passes in `GO_LIVE_CHECKLIST.md` §E1–E3 and Rollback §3.3. |
| **Risk if untreated before Stage 1** | Board confuses tabletop rehearsal with Critical EVIDENCED; unsafe or dishonest enrollment under PB-001 HOLD rule. |
| **Minimum appropriate solution** | During OP-004 live window (or staging twin): execute export dry-run, deletion dry-run on **FND-TST-DEL**, kill-switch R1; file Pass rows with operator / environment / opaque id / result; leave OPEN honestly if not Pass. Never fabricate. |
| **Not in minimum scope** | Treating OP-004 packaging or EP-009 docs as CE closure; marking CE EVIDENCED without §E fills. |
| **EP-009 severity** | **Critical** (enrollment blocker via OP-001 CE-03…CE-05) |
| **Links** | OP-004 ISSUE-003; OBS-OPS-002; OP-001 CE-03…CE-05; OP-002 dashboard |

---

## ISSUE-004 — “Registration” wording vs invite-only

| Field | Assessment |
|---|---|
| **Is this a documentation issue?** | **Yes** — primary. |
| **Is this a workflow issue?** | No — controlled provisioning works (`flask create-test-user`). |
| **Is this an application issue?** | No — public registration correctly closed (DR-034). |
| **Is this an operational issue?** | No — by-design posture. |
| **Risk if untreated before Stage 1** | Board or operators misread “Registration” as self-serve signup. Low if Board materials keep invite-only explicit. |
| **Minimum appropriate solution** | Keep OP-004 Plan §3/§5 redefinition; prefer “controlled provisioning” in Board / invite language. No product change. |
| **Status** | Already **DOCUMENTED** in OP-004. |
| **EP-009 severity** | **Low** |
| **Links** | OP-004 ISSUE-004; OBS-WF-001; DR-034 |

---

## ISSUE-005 — No single account-deletion checklist

| Field | Assessment |
|---|---|
| **Is this a documentation issue?** | **Yes** — primary. |
| **Is this a workflow issue?** | Yes — multi-step cascade across analytics + educational domain. |
| **Is this an application issue?** | No (checklist gap, not missing CLI). |
| **Is this an operational issue?** | Yes — founder/operator cannot run CE-04 confidently without a single step list. |
| **Risk if untreated before Stage 1** | Incomplete cascade; CE-04 Pass on analytics-only while educational rows remain. |
| **Minimum appropriate solution** | Write **Account Deletion Checklist** under EP-008.2B or Privacy Ops (verify → analytics delete → educational disable/remove → audit → §E2 log). Satisfies ISSUE-001 ops half without UI. |
| **Relationship to ISSUE-001** | ISSUE-005 is the docs fix for ISSUE-001’s operational risk. Treat as one hardening work item with two issue IDs. |
| **EP-009 severity** | **High** |
| **Links** | OP-004 ISSUE-005; Privacy Ops § deletion; EP-008.2B Privacy package §10 |

---

## Observations not opened as issues (disposition)

| Observation | Disposition in EP-009 |
|---|---|
| OBS-WF-001 Invite-only by design | Info — supports ISSUE-004 Low |
| OBS-WF-002 Journey operable on paper | Info — no hardening item |
| OBS-DOC-001 Stage 1 HOLD truth | Governance — out of EP-009 fix scope; retain HOLD |
| OBS-SEC-001 Do not delete primary study account | Control — reinforce in checklist; not a defect |
| OBS-UX-L01… / OBS-OPS-L01… (live Days 1–7) | Deferred — fill during live window; re-triage if new defects appear |

---

## Explicit non-scope (even if Stage 1 still blocked)

These block Stage 1 but are **not** founder-pilot application defects and are **not** EP-009 implementation work:

| Item | Owner track |
|---|---|
| CE-01 Privacy Review signatures | OP-001 T-01/T-02 |
| CE-02 Named operational owners §E4 | OP-001 T-06 |
| Validated KSI / G1 / Version 1 GO | P-002.1 / P-003.8 |
| Educational effectiveness / N_external | EP-007.3 |

---

**End of ISSUE_TRIAGE**
