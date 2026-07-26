# PB-001 — Open Action Register

**Programme:** PB-001 — Stage 1 Go/No-Go Review  
**Date:** 2026-07-26  
**Board outcome:** Stage 1 **HOLD**  
**Purpose:** Track actions required before a future Stage 1 GO can be evidence-based  
**Does not:** Authorise invites; fabricate signatures; change Runtime A  

---

## Status legend

| Status | Meaning |
|---|---|
| **OPEN** | Blocking or enrollment-relevant; not evidenced |
| **READY** | Documentation / designation exists; execution or confirmation still needed |
| **CLOSED** | Evidenced with dated path (none in this register yet for Critical) |

---

## Critical actions (must close before Stage 1 GO)

| ID | Action | Owner role | Evidence target | Status | Blocks invite? |
|---|---|---|---|---|---|
| **A-01** | Sign Privacy Review — Product (Approve/Reject) | Product | `PRIVACY_SIGNOFF_PACKAGE.md` §14 S1; `private_beta/PRIVACY_REVIEW.md` | **OPEN** | **Yes** (OR-01) |
| **A-02** | Sign Privacy Review — Security / ops | Security / ops | Same §14 S2 | **OPEN** | **Yes** (OR-01) |
| **A-03** | Execute export dry-run; fill evidence log | Ops / beta operator | `GO_LIVE_CHECKLIST.md` §E1 | **OPEN** | **Yes** (OR-02) |
| **A-04** | Execute delete dry-run; confirm audit; fill log | Ops / beta operator | `GO_LIVE_CHECKLIST.md` §E2 | **OPEN** | **Yes** (OR-02) |
| **A-05** | Rehearse analytics kill switch on Pilot-hosting or staging twin; fill log | Ops / on-call | `GO_LIVE_CHECKLIST.md` §E3; `ROLLBACK_PLAYBOOK.md` §3.3 | **OPEN** | **Yes** (OR-02) |
| **A-06** | Confirm named owners (beta operator, export, deletion, kill-switch) on activation log | Product + Ops | `GO_LIVE_CHECKLIST.md` §E4; activation / Rollout log | **OPEN** | **Yes** (G-S1-5) |

---

## High enrollment actions (required for honest / supportable start)

| ID | Action | Owner role | Evidence target | Status | Notes |
|---|---|---|---|---|---|
| **A-07** | Attach finalized privacy notice to invite pack | Product / beta ops | Privacy package §7; OR-03 | **READY** (text) / **OPEN** (attach) | At invite time — after Critical clear |
| **A-08** | Operationalise consent capture for BETA-PIL IDs | Beta ops | Consent log (ops store); OR-04 | **READY** (wording) / **OPEN** (live) | Before measurement inclusion |
| **A-09** | Record Pilot enable **or** written manual-measure decision | Product | `ANALYTICS_ACTIVATION.md` C1 or C2; OR-06 | **OPEN** / **HOLD** | Does not waive A-01…A-06 |
| **A-10** | Reconfirm Stage 0 monitoring GREEN; no open P0 on Go day | Ops | `OPERATIONS_MONITORING.md`; G-S1-6 | **OPEN** (day-of) | Assumed GREEN as of prior Stage 0 reports — reconfirm |
| **A-11** | Record Rollout Stage 1 **Go** only after G-S1-1…G-S1-7 evidenced | Product + Security/ops | `ep004_private_beta/ROLLOUT.md` | **OPEN** | Gate for first invite |
| **A-12** | Issue first external invite only after A-11 | Beta ops | Invite pack + consent acks | **OPEN** | Forbidden until Critical closed |

---

## Non-blocking context (do not treat as Stage 1 GO criteria alone)

| ID | Item | Status | Note |
|---|---|---|---|
| **A-13** | Validated KSI ≥ 80 (G1.1) | Open for Version 1 | Does **not** unblock Stage 1 invite by itself; V1 still NO GO |
| **A-14** | Educational effectiveness / G1.9 | FAIL until Stage 1 evidence | Stage 1 start enables path; does not equal effectiveness GO |
| **A-15** | Multi-country DPA programme | Deferred | Not required for single-regime Stage 1 per Privacy package |
| **A-16** | Version 1 Evidence Package G2–G12 | Incomplete | Separable from Stage 1 enrollment |

---

## Closure rule for a future re-board

A successor Board may recommend Stage 1 **GO** only when:

1. A-01 and A-02 show real names, dates, and Approve.  
2. A-03, A-04, A-05 show Pass results with operator, environment, date.  
3. A-06 names are filled.  
4. A-07–A-11 completed or explicitly dated with paths.  
5. No open P0 / RED monitoring; public registration still closed.  

Until then: retain **HOLD**. Do not invent evidence.

---

## Immediate next owner sequence (ops)

```text
A-01 + A-02 (signatures)
  → A-03 + A-04 + A-05 (dry-run + kill-switch)
  → A-06 (named owners)
  → A-09 (C1 or C2)
  → A-10 (monitoring reconfirm)
  → A-11 (Rollout Go)
  → A-07 + A-08 + A-12 (notice, consent, invite)
```

---

**End of OPEN_ACTION_REGISTER**
