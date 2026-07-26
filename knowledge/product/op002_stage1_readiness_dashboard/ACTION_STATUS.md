# Action Status — Stage 1

**Programme:** OP-002 — Stage 1 Readiness Dashboard  
**As of:** 2026-07-26  
**Linked:** [`CRITICAL_EVIDENCE_SUMMARY.md`](CRITICAL_EVIDENCE_SUMMARY.md) · OP-001 [`ACTION_TRACKER.md`](../op001_critical_evidence_closure/ACTION_TRACKER.md) · PB-001 [`OPEN_ACTION_REGISTER.md`](../pb001_stage1_go_no_go_review/OPEN_ACTION_REGISTER.md)  
**Does not:** Authorise invites; fabricate evidence; clear HOLD  

---

## Status legend

| Status | Meaning |
|---|---|
| **OPEN** | Blocking or enrollment-relevant; not evidenced |
| **DOC READY** / **READY** | Docs or designation exist; execution or confirmation still needed |
| **CLOSED** | Evidenced with dated path — **none yet for Critical** |

**Target dates** are **proposed tracking targets** after PB-001 (2026-07-26). They are **not** evidence of completion.

---

## High-priority Critical actions (must close before Stage 1 GO reconsideration)

| ID | CE | Action | Responsible owner | Target date | Evidence location | Status | Board |
|---|---|---|---|---|---|---|---|
| **T-01** | CE-01 | Sign Privacy Review — Product | Product | 2026-07-28 | Privacy Sign-off §14 S1; `PRIVACY_REVIEW.md` | **OPEN** | PENDING |
| **T-02** | CE-01 | Sign Privacy Review — Security / ops | Security / ops | 2026-07-28 | Same §14 S2 | **OPEN** | PENDING |
| **T-03** | CE-03 | Execute export dry-run; fill log | Ops / beta operator | 2026-07-30 | `GO_LIVE_CHECKLIST.md` §E1 | **OPEN** | PENDING |
| **T-04** | CE-04 | Execute delete dry-run; fill log | Ops / beta operator | 2026-07-30 | `GO_LIVE_CHECKLIST.md` §E2 | **OPEN** | PENDING |
| **T-05** | CE-05 | Rehearse analytics kill switch; fill logs | Ops / on-call | 2026-07-30 | Go-Live §E3; Rollback §3.3 | **OPEN** | PENDING |
| **T-06** | CE-02 | Confirm named owners on activation log | Product + Ops | 2026-07-30 | Go-Live §E4 | **DOC READY** / confirmation **OPEN** | PENDING |

Paths under `knowledge/product/ep008_2b_stage1_pilot_readiness_closure/` unless noted.

---

## High enrollment actions (after Critical — not substitutes for CE-01…CE-05)

| ID | Action | Responsible owner | Target date | Status | Notes |
|---|---|---|---|---|---|
| **T-07** | Attach finalized privacy notice to invite pack | Product / beta ops | After Critical clear | **READY** (text) / **OPEN** (attach) | At invite time |
| **T-08** | Operationalise consent capture for BETA-PIL IDs | Beta ops | At first invite | **READY** (wording) / **OPEN** (live) | Before measurement inclusion |
| **T-09** | Record Pilot enable **or** written manual-measure decision | Product | After T-01…T-06 | **OPEN** / **HOLD** | Does not waive Critical |
| **T-10** | Reconfirm Stage 0 monitoring GREEN; no open P0 on Go day | Ops | Go day | **OPEN** (day-of) | Reconfirm |
| **T-11** | Record Rollout Stage 1 **Go** only after G-S1-1…G-S1-7 evidenced | Product + Security/ops | After T-01…T-10 | **OPEN** | Gate for first invite |
| **T-12** | Issue first external invite only after T-11 | Beta ops | After T-11 | **OPEN** | Forbidden until Critical closed |

---

## Execution sequence

```text
T-01 + T-02 (Privacy signatures)     ← target 2026-07-28
  → T-03 + T-04 + T-05 (export / delete / kill-switch)  ← target 2026-07-30
  → T-06 (named owners confirmed on §E4)
  → Update CE statuses → EVIDENCED (only with proof) → VERIFIED
  → Reconvene Product Board (OP-001 BOARD_REVIEW_AGENDA)
  → If BOARD ACCEPTED on CE-01…CE-05:
       T-09 → T-10 → T-11 → T-07 + T-08 + T-12
  → Else: retain HOLD
```

---

## Target dates summary

| Date | Items |
|---|---|
| **2026-07-28** | T-01, T-02 (privacy signatures) |
| **2026-07-30** | T-03, T-04, T-05, T-06 (dry-runs, kill-switch, named owners) |
| **After CE EVIDENCED** | Successor Board review for Critical acceptance |
| **After Board Option B + G-S1-*** | T-07…T-12 enrollment path |

---

## Responsible owner map

| Owner role | Actions |
|---|---|
| **Product** | T-01, T-06 (with Ops), T-09, T-11 (with Security/ops) |
| **Security / ops** | T-02, T-11 (with Product) |
| **Ops / beta operator** | T-03, T-04 |
| **Ops / on-call** | T-05 |
| **Product / beta ops** | T-07, T-08, T-12 |
| **Ops** | T-10 |
| **Product Board** | Critical **BOARD ACCEPTED**; Stage 1 HOLD/GO recommendation |
| **Product Governance Lead** | Dashboard stewardship (OP-002) |

---

## Non-blocking Version 1 context

| ID | Item | Status | Note |
|---|---|---|---|
| **T-13** | Validated KSI ≥ 80 (G1.1) | Open for Version 1 | Does **not** unblock Stage 1 invite alone |
| **T-14** | Educational effectiveness / G1.9 | FAIL until Stage 1 evidence | Stage 1 start enables path; ≠ effectiveness GO |
| **T-15** | Version 1 Evidence Package G2–G12 | Incomplete | Separable from Stage 1 enrollment |

---

## Snapshot

| Layer | Count incomplete | Count CLOSED |
|---|---:|---:|
| Critical (T-01…T-06) | **6** | **0** |
| High enrollment (T-07…T-12) | **6** | **0** |
| Stage 1 HOLD | Retained | — |

---

## How to close a Critical row

1. Execute the human action on the correct environment.  
2. Fill the Evidence location with real operator/name, date, and Pass/Approve.  
3. Update this file and OP-001 tracker → **CLOSED** for the tracker row; CE status → **EVIDENCED**.  
4. After verification check → **VERIFIED**.  
5. After successor Board → **BOARD ACCEPTED**.  
6. Do **not** mark CLOSED from memory, chat, or documentation completeness alone.

---

**End of ACTION_STATUS**
