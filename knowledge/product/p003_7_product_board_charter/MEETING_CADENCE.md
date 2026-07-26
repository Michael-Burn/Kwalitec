# Meeting Cadence

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — Board procedure  
**Effective:** 2026-07-26  
**Companion:** [`PRODUCT_BOARD_CHARTER.md`](PRODUCT_BOARD_CHARTER.md)  
**Does not:** Mandate calendar tooling; amend gate law  

**Founder-operated quorum:** When the organisation is founder-operated (GP-001), apply `BOARD_ROLES_AND_RESPONSIBILITIES.md` §1a — Founder as Chair with capacity Founder Reviews — instead of inventing multi-person attendance. Evidence requirements are unchanged.

---

## 1. Purpose

Suggest a **repeatable meeting set** so governance does not rely on ad-hoc chat. Cadence is guidance; Release and Emergency reviews fire when triggers demand, not only on the monthly slot.

---

## 2. Meeting catalogue

### 2.1 Monthly governance review

| Field | Content |
|---|---|
| **Cadence** | Monthly |
| **Purpose** | Keep registers, claims, risks, and maturity heat current |
| **Quorum** | Chair + Product Governance Lead + one of Evidence / Architecture / Engineering |
| **Typical agenda** | (1) Open blockers (G1, effectiveness, package gaps) (2) DR/PR/PA deltas (3) Claim freeze status (4) Maturity heatmap glance (5) Actions |
| **Standard outputs** | Confirm / DEFER notes; action list; optional Confirm on DR-041 while NO GO holds |
| **Duration target** | 45–60 minutes |

### 2.2 Milestone review

| Field | Content |
|---|---|
| **Cadence** | End of material EP / P programme |
| **Purpose** | Absorb programme evidence into Board memory without waiting for month-end |
| **Quorum** | Chair or Product Governance Lead + Evidence Lead (or deputy) |
| **Typical agenda** | (1) SIA / ΔKSI honesty (2) New evidence classification (3) Register candidates (4) Student-visible / flag impacts (5) Whether Release review needed |
| **Standard outputs** | Accept / reject evidence for claims; Lifecycle tasks for DR/PR/PA |
| **Duration target** | 30–45 minutes |

### 2.3 Release review

| Field | Content |
|---|---|
| **Cadence** | Before any C-V1 / C-REC recommendation change; otherwise when Chair calls a declaration attempt |
| **Purpose** | Form GO / CONDITIONAL GO / NO GO / DEFER |
| **Quorum** | Full Release quorum ([`BOARD_ROLES_AND_RESPONSIBILITIES.md`](BOARD_ROLES_AND_RESPONSIBILITIES.md) §4) |
| **Typical agenda** | Follow [`RELEASE_DECISION_PROCESS.md`](RELEASE_DECISION_PROCESS.md) exit checklist |
| **Standard outputs** | Signed recommendation record; readiness alignment tasks; DR posture update if class changes |
| **Duration target** | 90 minutes (package pre-read mandatory) |

**Pre-read rule:** No Release review without circulated evidence index ≥ 48 hours prior (Emergency excepted).

### 2.4 Emergency review

| Field | Content |
|---|---|
| **Cadence** | As needed |
| **Triggers** | Educational honesty P1; production flag-default flip proposal; critical privacy / security incident affecting students; public claim published without ack |
| **Quorum** | Chair + Product Governance + owning Representative |
| **Typical agenda** | (1) Incident fact (2) Student harm / claim exposure (3) Immediate HOLD/freeze (4) Register / communicate (5) Follow-up Release or Evidence review |
| **Standard outputs** | HOLD / freeze / rollback recommendation to operators; PR open or escalate |
| **Duration target** | As short as safe; record within 24 hours |

### 2.5 Evidence review

| Field | Content |
|---|---|
| **Cadence** | When new validation / perception / effectiveness packs land (may combine with Milestone) |
| **Purpose** | Classify E1–E5; refresh permitted claims |
| **Quorum** | Evidence Lead + Product Governance Lead |
| **Typical agenda** | Per [`EVIDENCE_REVIEW_PROCESS.md`](EVIDENCE_REVIEW_PROCESS.md) §6 |
| **Standard outputs** | Classification table; freeze impacts; register candidates |
| **Duration target** | 30–60 minutes |

---

## 3. Standing pre-reads (by meeting)

| Meeting | Minimum pre-read |
|---|---|
| Monthly | `ACTIVE_RISKS.md`; ACTIVE decisions board order; dossier recommendation banner |
| Milestone | Programme COMPLETION_REPORT + SIA + evidence paths |
| Release | Full package §2 of Release Decision Process |
| Emergency | Incident note + related DR/PR |
| Evidence | Packet fields from Evidence Review Process §3.1 |

---

## 4. Minutes standard (lightweight)

Every meeting records:

1. Date and meeting type  
2. Roles present (not necessarily personal bios)  
3. Decisions / outcomes (Approve, Confirm, HOLD, DEFER, NO GO, …)  
4. Evidence paths cited  
5. Actions with owners and due triggers  

Store under a Board minutes path chosen by the organisation (or attach to the relevant programme completion / dossier update). Minutes must be **findable**; format is secondary.

---

## 5. What not to discuss in Board meetings

- Line-by-line code review  
- Sprint capacity planning  
- Deploy command execution  
- Unprepared brainstorms without a decision question  

Those belong to engineering / release forums. Escalate to Board only when Version 1 posture, claims, or educational honesty are at stake.

---

## 6. Cadence vs current NO GO

While DR-041 **NO GO** holds:

- Monthly reviews **Confirm** blockers rather than hunting for optimistic GO.  
- Release reviews are called when evidence programmes plausibly clear G1.1 + G1.9 + package completeness — not on a fixed “launch date.”  
- Milestone / Evidence reviews remain the primary engine of progress.

---

## 7. Success check

The Board meets often enough that:

- register drift is caught within a month,  
- new evidence is classified before it is marketed,  
- release recommendations are never improvised in chat without a record.

---

**End of Meeting Cadence**
