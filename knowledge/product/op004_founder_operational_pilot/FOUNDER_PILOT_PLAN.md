# OP-004 — Founder Pilot Plan

**Programme:** OP-004 — Founder Operational Pilot  
**Date:** 2026-07-26  
**Status:** Active plan (Day-0 rehearsal complete; live window open)  
**Operator:** Founder (Product Owner + Operations Owner capacities — GP-001)  
**Companions:** EP-008.2A [`PILOT_RUNBOOK.md`](../ep008_2a_stage1_operational_readiness/PILOT_RUNBOOK.md) · EP-008.2B [`ROLLBACK_PLAYBOOK.md`](../ep008_2b_stage1_pilot_readiness_closure/ROLLBACK_PLAYBOOK.md) · OP-002 Stage 1 dashboard  

---

## 1. Purpose

Use Kwalitec Version 1 as the founder’s **primary study system** for a defined window, and rehearse every operational workflow that Stage 1 participants would exercise — **before** any external invite.

This is an **operational rehearsal**, not educational validation.

---

## 2. Pilot window

| Field | Value |
|---|---|
| Window | **2026-07-26 → 2026-08-01** (7 calendar days) |
| Day 0 | 2026-07-26 — structured workflow rehearsal (all scoped items) |
| Days 1–7 | Daily primary-study use + log entries |
| Environment | Local / Stage 0 private-beta host (DR-040) — **not** public launch |
| External participants | **None** |
| Analytics Pilot ON | Optional for founder dogfood; default **OFF** unless Product records C1/C2 in EP-004 activation log |

---

## 3. Accounts

| ID | Role | Rules |
|---|---|---|
| **FND-PIL-001** | Founder primary study account | Normal student path; no PII in knowledge artefacts |
| **FND-TST-DEL** | Dedicated deletion / rights test account | Provisioned only for export + deletion rehearsal; **not** the primary study account |

Provisioning (invite-only posture — DR-034):

```text
flask create-test-user --name "…" --email "…" --password "…"
```

Public self-service registration remains **closed**. Scope item “Registration” means **controlled account creation**, then first login as a student.

---

## 4. Daily operating protocol (Days 1–7)

Minimum daily student path (≈ one realistic study block):

1. **Login** via `/auth/login`.  
2. Open **Home** (canonical student home).  
3. Read **today’s recommendation** (what / why / why now — trust chrome).  
4. **Commitment:** confirm (“I’m doing this next”) **or** honest defer with reason.  
5. Start and complete a **study session** / today’s session when committing.  
6. Complete **reflection** when prompted; acknowledge commitment reflection if shown.  
7. Open **History** (`/student/history` or consolidated history surface).  
8. Log operational notes in [`DAILY_OPERATION_LOG.md`](DAILY_OPERATION_LOG.md) (friction, defects, docs gaps — **not** learning outcomes).

Cadence extras:

| When | Action |
|---|---|
| Day 0 | Full workflow matrix (§5) |
| Mid-window (≥1×) | Student data **export** (`/settings/data` → backup export) |
| Mid-window (≥1×) | Analytics export dry-run on **FND-TST-DEL** if env ready — file evidence to EP-008.2B §E1 if Pass |
| Late window (≥1×) | Deletion process on **FND-TST-DEL** only — file §E2 if Pass |
| Where appropriate (≥1×) | Rollback rehearsal R1 (analytics kill switch) on non-prod — file §E3 if Pass |

---

## 5. Workflow exercise matrix

| # | Workflow | Student / operator path | Day-0 method | Success (operational) |
|---|---|---|---|---|
| W1 | Registration (controlled) | `flask create-test-user`; confirm `/auth/register` absent / closed | Procedure + code/path check | Account exists; public registration still closed |
| W2 | Login | `/auth/login` → Home or study-plan wizard | Path check + Day-0 note | Authenticated session; safe `next` behaviour |
| W3 | Daily recommendations | Student Home tip / MES trust chrome | Path check | Tip visible with explainable fields (no outcome claim) |
| W4 | Study sessions | Start today’s session / mission session → complete | Path check | Session start/complete reachable |
| W5 | Commitment | Confirm / defer on Home (`/commitment/defer`, start-with-commitment) | Path check | C-states advance without ranking mutation |
| W6 | Reflection | Session reflection + commitment reflection ack | Path check | Reflection surfaces reachable |
| W7 | History | `/student/history` (or sole-runtime redirect) | Path check | History loads for current user only |
| W8 | Export | `/settings/export/backup`; optional `flask analytics-export-user <id>` | Path check; live CLI optional | Backup JSON obtainable; analytics export only with dated evidence |
| W9 | Deletion | Analytics: `flask analytics-delete-user <id> --yes` on **FND-TST-DEL**; educational account deletion via support/ops path | Path check; live only on test account | Documented path operable; **no** use of primary study account |
| W10 | Rollback | EP-008.2B R1 kill switch (and R5 claim freeze awareness) | Tabletop + optional live | Procedure understood; live Pass only with §E3 evidence |

---

## 6. Observation protocol

Record in [`OPERATIONAL_OBSERVATIONS.md`](OPERATIONAL_OBSERVATIONS.md) and/or daily log:

| Allowed | Forbidden |
|---|---|
| Friction, defects, missing docs, SLA clarity | “This improved my exam readiness” |
| Workflow latency / broken links / confusing copy | Pass-rate or effectiveness claims |
| Gaps vs EP-008.2A/2B runbooks | KSI deltas |
| Export/delete/rollback operability notes | “Stage 1 ready” / external validation |

Issue severity (align Pilot Runbook):

| Tier | Meaning |
|---|---|
| **P0** | Security / privacy / data integrity |
| **P1** | Cannot login / cannot study / wrong-student data |
| **P2** | Confusing guidance / navigation / docs |
| **P3** | Nit / polish |

---

## 7. Linkage to Critical evidence (OP-001)

OP-004 **may produce** human evidence that later files into:

| CE | Evidence target |
|---|---|
| CE-03 Export dry-run | EP-008.2B `GO_LIVE_CHECKLIST.md` §E1 |
| CE-04 Deletion dry-run | §E2 |
| CE-05 Kill-switch rehearsal | §E3 + Rollback §3.3 |

Filing rules:

- Do **not** mark CE items EVIDENCED from this programme alone without dated §E rows.  
- Do **not** invent Pass results.  
- Stage 1 **HOLD** remains until OP-001 / Board acceptance.

---

## 8. Explicit non-claims

This plan does **not** authorise or imply:

- Educational effectiveness  
- KSI improvement  
- External validation  
- Stage 1 readiness / enrollment GO  
- Version 1 production-ready  

---

## 9. Stop conditions

Pause live study rehearsal and open an issue if:

- P0 privacy/security event  
- P1 cannot-study on primary path without workaround  
- Temptation to invite externals under HOLD  
- Educational honesty risk (overclaim language in UI or notes)

---

**End of FOUNDER_PILOT_PLAN**
