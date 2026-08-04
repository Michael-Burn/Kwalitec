# OP-002 — Founder Decision Guide

**Programme:** OP-002 — Early Access Pilot Operations  
**Version:** 1.0  
**Status:** TABLETOP REHEARSAL COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `OP001_EXECUTION_CHECKLIST.md` · `OP002_OPERATIONAL_PLAYBOOK.md` · `OP002_INCIDENT_RESPONSE_GUIDE.md` · KSI-002 · EF-001 · Educational Content Freeze

**Decision aid for Founder.** Does not grant invite permission by itself. Does not change product systems.

---

## 1. Purpose

List every **Founder-owned yes/no** in the Early Access lifecycle so approvals are explicit, dated, and not silently skipped (KSI-003 failure mode: invites never sent / accepted N = 0).

---

## 2. Decision register

| ID | Decision | Default if undecided | Required artefacts | Unlock / effect |
|----|----------|----------------------|--------------------|-----------------|
| **D0** | Approve OP-001 ops package? | **No invites** | OP-001 artefact set | Docs freeze acknowledged |
| **D1** | Approve OP-002 rehearsal package? | **No recruit** | OP-002 artefact set + evidence | Ops rehearsal frozen |
| **D2** | Pre-flight complete enough to invite? | **No G-INVITE** | Checklist B signed | Eligible for D3 |
| **D3** | **Authorise invite send (G-INVITE)?** | **No send** | Dated note; final invite list; OR-01 held | Operator may send invites |
| **D4** | Confirm final invite list? | Hold send | Screened queue; channels logged | List locked for wave |
| **D5** | Expand beyond pending pilots / buffer size? | Stay at pending only (insufficient for N≥5) | Recruitment notes | Invite buffer ≥8–12 posture |
| **D6** | Dual-mark prior internal as external? | **No** | Disclosure note | Rare exception |
| **D7** | Accept borderline eligibility? | Exclude from external N | Screening record | Count or discretionary access only |
| **D8** | Pause / kill invites (P0, overload, OR-01)? | Continue only if safe | Incident note | Invite freeze |
| **D9** | Resume invites after pause? | Remain paused | Clearance note | New sends allowed |
| **D10** | Stop recruitment below accepted ≥5? | Continue toward floor | Written rationale | Stop ≠ invent N |
| **D11** | Close accept wave? | Keep open | Dashboard Accepted | Hold cohort |
| **D12** | Ops-remove participant (abuse/safety)? | Retain unless unsafe | Incident + acknowledgement | Access revoked |
| **D13** | Allow educational / Recommendation / Twin / Runtime / package change mid-wave? | **No** (Content Freeze + EF-001) | EF-001 operational review | Only if EF insufficiency proven |
| **D14** | Engage engineering for **defect** fix? | Case-by-case | Bug ticket | Normal PR path — not OP redesign |
| **D15** | Approve irreversible deletion execution? | Follow Privacy Review after verify | Verified request | Data deleted per SLA |
| **D16** | Designate Operator cover for Founder absence? | Auto-pause invites if none | Cover rules in ops store | Continuity (see S9) |
| **D17** | Mark cohort observation complete / close? | Hold open | Final snapshot; open P0/P1 clear | Thank-yous; hand-off |
| **D18** | Hand-off to study / KSI authority? | Ops retains | Honest N flow note | Study programme owns KPIs |
| **D19** | Recalculate validated KSI / declare effectiveness GO? | **No** from ops alone | Study evidence under KSI-002 | Out of OP-002 |
| **D20** | Declare Version 1 production-ready / marketing launch? | **No** | P-002.1 gates | Forbidden under OP-002 |

---

## 3. Decision trees (short)

### 3.1 May we send the first invite?

```text
OP-001 approved (D0)? ─No→ STOP
        │ Yes
OP-002 approved (D1)? ─No→ STOP
        │ Yes
Pre-flight (D2)? ─No→ Complete checklist B
        │ Yes
OR-01 signed + support live + consent log ready?
        │ No → STOP
        │ Yes
Dated G-INVITE (D3) + list (D4)? ─No→ STOP
        │ Yes
        ▼
SEND (operator)
```

### 3.2 Participant wants engine / package changed

```text
Request received
  → Document as feedback (P2/P3)
  → Is this a clear product defect (broken path)?
        │ Yes → D14 defect engineering (no educational redesign)
        │ No → EF-001 operational review
              → Can resolve without frozen framework change?
                    │ Yes → proceed under existing law / content
                    │ No → D13 exceptional Founder EF unfreeze path (rare)
```

### 3.3 Accepted N still &lt; 5 at end of invite window

```text
Extend recruitment (D5) ─or─ D10 stop with rationale
  → Never invent Accepted
  → Do not declare study GO
  → Do not update validated KSI
```

---

## 4. Authority boundaries

| Actor | May | Must not |
|-------|-----|----------|
| **Founder** | All D0–D20 | Skip G-INVITE silently; claim V1 from ops |
| **Operator** | Execute protocols after D3; P1/P2; chase; log | Send invites without D3; change engines/packages; invent metrics |
| **Engineering** | Approved defect fixes | Educational algorithm / package changes under OP-002 |
| **Study authority** | Later KSI observation | Treat empty ops evidence as GO |

---

## 5. Dating and recording

Every Founder decision that unlocks external contact or irreversible privacy action must be recorded in the **ops store** (not git PII) with:

- Decision ID (D#)  
- Date (ISO)  
- Outcome (Yes / No / Deferred)  
- One-line rationale  

Optional pseudonymous pointer may be filed under `knowledge/evidence/releases/OP002/decisions/` when executing (empty in this rehearsal).

---

## 6. Immediate STOP state (current)

As of OP-002 delivery (2026-08-04):

| Decision | Status |
|----------|--------|
| D0 OP-001 | Awaiting Founder (package delivered) |
| D1 OP-002 | **Awaiting Founder** (this package) |
| D3 G-INVITE | **Not authorised** |
| D19 / D20 | **Forbidden** from this programme |

**Do not recruit. Do not send invitations.**

---

## 7. STOP

Await Founder approval of OP-002. Await separate G-INVITE before any participant invitation.

Signed: OP-002 Founder Decision Guide · 2026-08-04
