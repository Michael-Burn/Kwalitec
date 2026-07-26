# EP-009 — Hardening Plan

**Programme:** EP-009 — Version 1 Operational Hardening  
**Date:** 2026-07-26  
**Status:** Plan complete (triage + priority; **no application implementation in this programme**)  
**Upstream:** OP-004 Founder Operational Pilot (Day-0 rehearsal)  
**Downstream consumers:** OP-001 evidence filing · OP-002 dashboard · EP-008.2A/2B invite/support packs · Product Board Stage 1 reconsideration  
**Constraints:** No Version 1 redesign · No new educational features · No Runtime A expansion · No recommendation-logic change · Minimal, founder-pilot-traceable only  

---

## 1. Purpose

Close **operational gaps** found in the Founder Operational Pilot before external Stage 1 participants are invited.

This plan translates OP-004 issues into the **minimum** docs and ops actions required for enrollment honesty. It does **not** claim Stage 1 GO, educational effectiveness, KSI movement, or Version 1 production-ready.

---

## 2. Naming note (Board)

| Identifier | Meaning |
|---|---|
| **EP-009 (this programme)** | Version 1 **Operational Hardening** — commissioned from OP-004 findings |
| Earlier **EP-009.x** mentions in P-004.1 / EP-008.* | Proposed **personalisation** dogfood / cutover identifiers — **not** this programme; remain uncommissioned recommendations unless Board reassigns |

---

## 3. Scope

### In scope

| Area | Content |
|---|---|
| Triage | All OP-004 ISSUE-001…005 |
| Pre-Stage 1 work design | Critical + High items only |
| Artefact targets | Operator card; Account Deletion Checklist; CE-03…CE-05 evidence execution plan |
| Non-claims / HOLD retention | Explicit |

### Out of scope

- Runtime A ownership or behaviour  
- Recommendation ranking / selection / educational reasoning  
- Self-serve account-deletion UI (deferred Medium)  
- Public registration / invite-policy redesign (DR-034 stands)  
- Fabricating Privacy signatures or §E Passes  
- KSI rescoring / Version 1 GO declaration  
- Non–founder-pilot Stage 1 blockers as EP-009 “builds” (CE-01, CE-02 tracked in OP-001)

---

## 4. Work packages

### WP-A — Dual-export operator card (ISSUE-002) — High

**Objective:** One unambiguous “which export?” card for founder and future beta operator.

**Minimum content (two rows):**

| Request type | Artefact | Path / command | Owner |
|---|---|---|---|
| Learning backup | Student learning data JSON | Settings → `/settings/export/backup` | Student or support-assisted |
| Analytics events | Analytics export JSON | `flask analytics-export-user <id>` | Export SLA owner |

**Where to place:**

- EP-008.2A invite / support pack materials (or Pilot Runbook export section)  
- EP-008.2A `STAGE1_CHECKLIST.md` / go-live orientation  
- Cross-link: Privacy Ops Guide export workflow; Go-Live §E1  

**Done when:** Card exists in the pack operators will actually use; ISSUE-002 can move DOCUMENTED/CLOSED in OP-004 register with path citation.

**Forbidden:** Changing export code or merging Settings + analytics into one UI in this hardening pass.

---

### WP-B — Account Deletion Checklist (ISSUE-005 + ISSUE-001 ops) — High

**Objective:** Single founder/operator step list for full withdrawal / account deletion rehearsal.

**Minimum steps:**

1. Verify identity / request legitimacy (support process).  
2. Prefer export-before-delete if student requested a copy (link WP-A).  
3. Analytics: `flask analytics-delete-user <id> --yes --requested-by …`  
4. Confirm audit `analytics.user_deleted`.  
5. Educational domain: disable/remove account per existing support/ops workflow (enumerate concrete commands or admin steps as they exist in-repo — do not invent new product behaviour).  
6. Confirm learning rows / session data no longer accessible for that user.  
7. File Go-Live §E2 (opaque id, environment, Pass/Fail, audit Yes).  

**Hard controls:**

- Use **FND-TST-DEL** or staging twin only — never primary dogfood account (OBS-SEC-001).  
- Settings restore ≠ account deletion (state explicitly on checklist).  

**Where to place:** EP-008.2B Privacy Sign-off Package companion or Privacy Ops Guide appendix; link from Rollback R3 / Go-Live §E2.

**Done when:** Checklist published; CE-04 dry-run can follow it without improvisation.

**Forbidden:** Implementing Settings “delete my account” UI under EP-009 (see WP-D deferred).

---

### WP-C — Live Critical evidence execution (ISSUE-003) — Critical

**Objective:** Convert Day-0 tabletop into dated Pass (or honest OPEN) for CE-03…CE-05.

| CE | Action | Evidence location |
|---|---|---|
| CE-03 | Export dry-run (prefer analytics CLI per §E1; note learning backup separately via WP-A) | `GO_LIVE_CHECKLIST.md` §E1 |
| CE-04 | Deletion dry-run using WP-B checklist on **FND-TST-DEL** | §E2 |
| CE-05 | Kill-switch R1 rehearsal | §E3 + `ROLLBACK_PLAYBOOK.md` §3.3 |

**Preferred window:** OP-004 live Days 3–5 (already planned).

**Done when:** Rows filled with operator, environment, opaque user id, command/steps, **Pass**, notes without PII — **or** remain OPEN with no fabricated Pass.

**Forbidden:** Marking CE EVIDENCED from EP-009 documentation alone; treating Day-0 path checks as Pass.

---

### WP-D — Deferred: self-serve account deletion UI (ISSUE-001 application) — Medium

**Objective (later):** Student-initiated full account deletion in Settings with privacy-safe cascade.

**Why deferred:** Stage 1 invite-only + named Deletion SLA owner + WP-B checklist + CE-04 Pass meet enrollment honesty without expanding product surface. UI is not required to lift HOLD if ops evidence is real.

**When to reopen:** After Stage 1 start or Board product decision; separate engineering programme; still no Runtime A / recommendation coupling.

---

### WP-E — Deferred: registration wording hygiene (ISSUE-004) — Low

**Objective:** Prefer “controlled provisioning” in Board/invite copy.

**Status:** Already DOCUMENTED in OP-004; DR-034 intact. Optional wording pass only.

---

## 5. Application code stance

| Question | Answer |
|---|---|
| Does pre-Stage 1 hardening require application commits? | **No** — Critical/High are docs + ops execution |
| May engineering implement WP-D under “hardening”? | Only if Board commissions a separate app milestone; not this plan’s pre-Stage 1 set |
| Educational reasoning / Runtime A / recommendations? | **Do not modify** |

---

## 6. Traceability

| Finding | Work package | Pre-Stage 1? |
|---|---|---|
| ISSUE-001 | WP-B (ops) · WP-D (UI deferred) | Ops yes · UI no |
| ISSUE-002 | WP-A | Yes |
| ISSUE-003 | WP-C | Yes |
| ISSUE-004 | WP-E | No |
| ISSUE-005 | WP-B | Yes |

---

## 7. Success criteria (this plan)

The Product Board can answer:

1. **What must be fixed before Stage 1?** — WP-A, WP-B, WP-C (plus OP-001 CE-01/CE-02 outside this programme).  
2. **What may wait?** — WP-D self-serve delete UI; WP-E wording polish.  
3. **Why?** — Documented in [`IMPLEMENTATION_PRIORITY.md`](IMPLEMENTATION_PRIORITY.md) decision record.

EP-009 programme packaging itself does **not** execute WP-A–C; it defines them. Execution remains with Operations / Privacy capacities and OP-001 evidence discipline.

---

## 8. Explicit non-claims

- Not Stage 1 GO  
- Not Version 1 production-ready  
- Not educational effectiveness / KSI improvement  
- Not CE-01…CE-05 EVIDENCED by virtue of this plan  
- Not authorisation to change Runtime A or recommendations  

---

**End of HARDENING_PLAN**
