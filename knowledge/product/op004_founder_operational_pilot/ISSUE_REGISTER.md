# OP-004 — Issue Register

**Programme:** OP-004 — Founder Operational Pilot  
**As of:** 2026-07-26  
**Scope:** Operational defects, usability, and documentation issues from founder rehearsal  
**Does not:** Authorise product development by itself; invent Critical evidence Passes; claim Stage 1 GO  

---

## Status legend

| Status | Meaning |
|---|---|
| **OPEN** | Confirmed; not yet resolved |
| **DOCUMENTED** | Known; tracked; workaround or docs path exists |
| **BLOCKED** | Waiting on external decision / capacity |
| **CLOSED** | Fixed or accepted with dated note |

Severity: **P0** / **P1** / **P2** / **P3** (Pilot Runbook triage).

---

## Register

| ID | Title | Severity | Class | Status | Owner capacity | Source |
|---|---|---|---|---|---|---|
| **ISSUE-001** | No self-serve full account deletion in Settings | P2 | Ops / Privacy | **OPEN** | Privacy Owner + Engineering Owner | Day-0 W9 |
| **ISSUE-002** | Dual export paths (Settings backup vs analytics CLI) lack a single operator card | P2 | Docs / Ops | **OPEN** | Operations Owner | Day-0 W8 · OBS-UX-001 |
| **ISSUE-003** | CE-03/04/05 live evidence still blank (export / delete / kill-switch) | P2* | Ops / Evidence | **OPEN** | Operations Owner | Day-0 W8–W10 · OP-001 |
| **ISSUE-004** | Scope language “Registration” conflicts with invite-only posture if read literally | P3 | Docs | **DOCUMENTED** | Product Owner | Day-0 W1 · DR-034 |
| **ISSUE-005** | Educational-domain account deletion procedure not spelled as a single founder checklist | P2 | Docs / Ops | **OPEN** | Operations Owner + Privacy Owner | Day-0 W9 · Privacy Ops guide |

\*ISSUE-003 is enrollment-Critical via OP-001 CE-03…CE-05; severity here is operational for the founder pilot. It remains a **Stage 1 blocker** until EVIDENCED elsewhere.

---

## Issue detail

### ISSUE-001 — No self-serve full account deletion

**Problem:** A dedicated test account cannot complete “delete my account” from the student Settings UI. Settings restore wipes/reimports learning rows; it is not privacy account deletion.  
**Risk:** Stage 1 participants (or support) may not fulfil withdrawal expectations without a written ops path.  
**Proposed next step (docs-only until authorised):** Write a one-page **Account Deletion Checklist** (verify identity → analytics-delete-user → educational account disable/remove → audit confirm). Do **not** implement UI in OP-004.  
**Links:** `PRIVACY_OPERATIONS_GUIDE.md`; EP-008.2B Rollback R3; OP-001 CE-04.

### ISSUE-002 — Dual export paths

**Problem:** “Export” means different artefacts in Settings vs analytics Privacy Ops.  
**Risk:** Missed SLA or wrong file delivered to a future participant.  
**Proposed next step:** Add a two-row table to invite/support pack and Stage 1 checklist: (1) Learning backup — Settings; (2) Analytics events — CLI.  
**Links:** OBS-UX-001; Go-Live §E1; DATA_COLLECTION_PLAN.

### ISSUE-003 — Live rights / kill-switch evidence blank

**Problem:** Day-0 tabletop confirmed procedures exist; dated Pass rows in `GO_LIVE_CHECKLIST.md` §E1–E3 are still empty.  
**Risk:** Board may confuse “procedure rehearsed on paper” with CE EVIDENCED.  
**Proposed next step:** During Days 3–5 of this pilot, execute on **FND-TST-DEL** / staging twin and file §E — or leave OPEN honestly.  
**Forbidden:** Marking CE-03…CE-05 EVIDENCED from OP-004 packaging alone.

### ISSUE-004 — “Registration” wording

**Problem:** Programme scope lists Registration; product has no public register.  
**Resolution path:** Plan §3/§5 already redefine as controlled provisioning. Keep wording explicit in Board materials.  
**Status:** **DOCUMENTED** (not a product defect).

### ISSUE-005 — Missing single account-deletion checklist

**Problem:** Privacy Ops covers analytics delete; educational deletion called “existing account/support workflow” without a consolidated founder runbook step list.  
**Risk:** Incomplete cascade (analytics wiped, educational rows remain — or reverse).  
**Proposed next step:** Docs checklist under EP-008.2B or Privacy Ops (no Runtime A change).

---

## Issues not opened (explicit)

| Topic | Why not an OP-004 issue |
|---|---|
| Validated KSI 64 / G1 FAIL | Governance fact; not a founder-pilot defect |
| Stage 1 HOLD | Correct control; not a bug |
| Recommendation ranking quality | Out of scope; no educational claims |

---

## Disposition at programme packaging

| Open | Documented | Closed |
|---:|---:|---:|
| 4 | 1 | 0 |

Live Days 1–7 may add rows; do not delete historical OPEN items without CLOSED note.

---

**End of ISSUE_REGISTER**
