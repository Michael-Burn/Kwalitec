# Stage 1 Readiness Dashboard

**Programme:** OP-002 — Stage 1 Readiness Dashboard  
**As of:** 2026-07-26  
**Authority (synthesis only):** PB-001 · OP-001 · EP-008.2A/2B · P-003.8 · `VERSION_1_READINESS.md`  
**Role:** Permanent single operational source of truth until Stage 1 begins  
**Does not:** Authorise invites; fabricate evidence; change Runtime A, KSI, or governance law  

---

## At a glance — Board questions

| Question | Answer (2026-07-26) |
|---|---|
| **Can Stage 1 begin?** | **No** |
| **If not, exactly why not?** | Critical operational evidence CE-01…CE-05 is not **EVIDENCED** / **BOARD ACCEPTED**. PB-001 rule: any Critical item without evidence → **HOLD**. |
| **Who owns each remaining action?** | See [`ACTION_STATUS.md`](ACTION_STATUS.md) (Product, Security/ops, Ops/beta operator, on-call). |
| **What evidence is still missing?** | Privacy signatures; named-owner confirmation; export dry-run Pass; deletion dry-run Pass; kill-switch rehearsal Pass. See [`CRITICAL_EVIDENCE_SUMMARY.md`](CRITICAL_EVIDENCE_SUMMARY.md). |
| **When should the Board meet again?** | **Proposed next Stage 1 reconsideration:** after CE-01…CE-05 are **EVIDENCED** (planning window earliest after Critical target dates **2026-07-30**). Do **not** convene a GO vote while Critical rows remain OPEN / DOC READY. Agenda: [`../op001_critical_evidence_closure/BOARD_REVIEW_AGENDA.md`](../op001_critical_evidence_closure/BOARD_REVIEW_AGENDA.md). |

**Companion one-pager:** [`BOARD_STATUS_CARD.md`](BOARD_STATUS_CARD.md)

---

## Overall Stage 1 status

# HOLD

| Field | Value | Source |
|---|---|---|
| Enrollment | **HOLD** — no first external invite | PB-001 `BOARD_RECOMMENDATION.md` |
| Decision class | Stage 1 external enrollment (not Version 1 GO) | DR-032; PB-001 |
| Safe-start gates G-S1-1…G-S1-7 | Not all evidenced | EP-008.2B `OPERATIONAL_SIGNOFF_SUMMARY.md` |
| External N | **0** | EP-007.3; EP-004 |
| Stage 0 private beta | May continue under **GO WITH CONDITIONS** | DR-040 |

---

## Current Board recommendation

# Stage 1 HOLD — do not invite the first external participant

| Field | Value |
|---|---|
| Programme | PB-001 — Stage 1 Go/No-Go Review |
| Date | 2026-07-26 |
| Invite first external? | **No** |
| Rationale | Critical items lack demonstrable evidence (privacy signatures; dry-runs; kill-switch; named owners) |
| Authorises | Retain HOLD; execute open actions; continue Stage 0; keep claim freezes |
| Does not authorise | External Stage 1 invitations; treating docs as sign-off; Version 1 production-ready |

Source: [`../pb001_stage1_go_no_go_review/BOARD_RECOMMENDATION.md`](../pb001_stage1_go_no_go_review/BOARD_RECOMMENDATION.md)

---

## Version 1 recommendation

# NO GO

| Field | Value | Source |
|---|---|---|
| Verdict | **NO GO** (production-ready declaration forbidden) | DR-041; P-003.8 |
| Separable from Stage 1? | **Yes** — Stage 1 enrollment clearance ≠ Version 1 GO | DR-032 |
| Hard blockers (context) | G1.1 (KSI &lt; 80); G1.9 (effectiveness NO-GO); Evidence Package incomplete | `CURRENT_RELEASE_POSITION.md` |

Stage 1 start enables the **path** to G1.9 evidence; it does **not** clear Version 1 NO GO by itself.

---

## Current KSI

| Field | Value | Source |
|---|---|---|
| Validated KSI | **64** | `VERSION_1_READINESS.md`; PB-001; EP-008.1B / EP-008.3B |
| Confidence | Medium | Tier B perception packs |
| Target (G1.1) | ≥ **80** | PSF; DR-025 |
| Gap | **16** | — |
| K1 / K2 / K3 | **72** / **68** / **65** | Journey / Trust / Readiness perception |
| K7 / K8 | **60** / **72** | Commitment / MES perception |
| ΔKSI from this programme | **0** (dashboard only; KSI not rescored) | OP-002 constraint |

**Note:** P-003.8 `CURRENT_RELEASE_POSITION.md` freeze text still cites KSI **62** (EP-007.2-era). Board Stage 1 materials and the readiness tracker use **64** after EP-008.1B. This dashboard follows the **later** documented Board/tracker figure (**64**) and does not invent a new score.

---

## Current G1 status

# FAIL

| Criterion | Status | Notes |
|---|---|---|
| **G1 overall** | **FAIL** | Any hard FAIL → overall FAIL |
| G1.1 Validated KSI ≥ 80 | **FAIL** | KSI **64** |
| G1.2 Confidence High or Medium | **PASS** | Medium |
| G1.5 K8 ≥ 70 | **PASS** | K8 **72** (EP-008.1B) |
| G1.7 Independent re-score | **HOLD** | Formality open |
| G1.9 Educational effectiveness not NO-GO | **FAIL** | Effectiveness **NO-GO / PENDING EVIDENCE**; N_external = 0 |

Sources: `VERSION_1_READINESS.md`; EP-007.3 `G1_9_STATUS.md`; PB-001.

---

## Critical Evidence

**Status legend (mandatory):** OPEN · DOC READY · EVIDENCED · VERIFIED · BOARD ACCEPTED  

Full detail: [`CRITICAL_EVIDENCE_SUMMARY.md`](CRITICAL_EVIDENCE_SUMMARY.md) · Canonical register: [`../op001_critical_evidence_closure/CRITICAL_EVIDENCE_REGISTER.md`](../op001_critical_evidence_closure/CRITICAL_EVIDENCE_REGISTER.md)

| CE | Track | Status | Owner role | Target date | Blocks invite? |
|---|---|---|---|---|---|
| **CE-01** | Privacy Review signatures (Product + Security/ops) | **OPEN** | Product; Security / ops | 2026-07-28 | **Yes** |
| **CE-02** | Named operational owners confirmation | **DOC READY** | Product + Ops | 2026-07-30 | **Yes** |
| **CE-03** | Export dry-run completion | **OPEN** | Ops / beta operator | 2026-07-30 | **Yes** |
| **CE-04** | Deletion dry-run completion | **OPEN** | Ops / beta operator | 2026-07-30 | **Yes** |
| **CE-05** | Kill-switch rehearsal completion | **OPEN** | Ops / on-call | 2026-07-30 | **Yes** |

| Metric | Value |
|---|---|
| Critical items | 5 |
| EVIDENCED | **0** |
| VERIFIED | **0** |
| BOARD ACCEPTED | **0** |
| Fabricated fills | **None** |

**Documentation packages (not the same as EVIDENCED):** OR-01 Privacy Sign-off Package and OR-02 Go-Live / Rollback packages are **documentation-complete** (EP-008.2B). Prefer-lower: package COMPLETE ≠ Critical EVIDENCED.

---

## High-priority actions

| Priority | Action | Owner | Target | Status |
|---|---|---|---|---|
| P0 | Sign Privacy Review (Product + Security/ops) | Product; Security / ops | 2026-07-28 | **OPEN** |
| P0 | Export + delete dry-runs; fill §E1–E2 | Ops / beta operator | 2026-07-30 | **OPEN** |
| P0 | Kill-switch rehearsal; fill §E3 + Rollback §3.3 | Ops / on-call | 2026-07-30 | **OPEN** |
| P0 | Confirm named owners on §E4 | Product + Ops | 2026-07-30 | **DOC READY** / confirmation **OPEN** |
| P1 | After Critical EVIDENCED — High enrollment T-07…T-11 | Product / Ops / beta ops | After Critical | **OPEN** / partial **READY** |
| P1 | Successor Board Critical acceptance | Product Board | After CE EVIDENCED | **PENDING** |

See [`ACTION_STATUS.md`](ACTION_STATUS.md).

---

## Target dates

| Milestone | Target date | Meaning |
|---|---|---|
| Privacy signatures (CE-01) | **2026-07-28** | Proposed tracking target — **not** a completion claim |
| Dry-runs / kill-switch / named owners (CE-02…CE-05) | **2026-07-30** | Proposed tracking target — **not** a completion claim |
| Successor Stage 1 Board reconsideration | **After CE-01…CE-05 EVIDENCED** (earliest planning window post-2026-07-30) | Meet for Critical acceptance / HOLD lift path — only if evidence filed |
| First external invite | **Only after** Board Option B + G-S1-2…G-S1-7 / T-07…T-11 | Forbidden until Critical closed |

Targets from OP-001 `ACTION_TRACKER.md`. Slippage does not invent evidence.

---

## Responsible owner

| Scope | Owner role |
|---|---|
| **Dashboard stewardship** | Product Governance Lead (keep statuses documentary; no inferred greening) |
| **Stage 1 HOLD / GO recommendation** | Product Board (PB-001 successor) |
| **Critical CE-01** | Product (S1); Security / ops (S2) |
| **Critical CE-02…CE-05** | Product + Ops; Ops / beta operator; Ops / on-call |
| **Version 1 NO GO posture** | Product Board (DR-041) — separable |

---

## Board review date

| Review | Date / trigger | Purpose |
|---|---|---|
| **Last Stage 1 Board outcome** | **2026-07-26** (PB-001) | HOLD recorded |
| **Next Stage 1 reconsideration (proposed)** | After CE-01…CE-05 **EVIDENCED**; planning window earliest after **2026-07-30** | Critical acceptance; HOLD lift path only if Option B |
| **Do not schedule GO vote while** | Any CE remains OPEN / DOC READY without EVIDENCED proof | Prefer-lower |
| Monthly governance cadence | Per P-003.7 `MEETING_CADENCE.md` | Registers / claims — not a substitute for Critical evidence Board |

---

## Operational readiness

| Layer | Status | Source |
|---|---|---|
| Ops assessment | **NOT YET — HOLD** on external enrollment | EP-008.2A `OPERATIONAL_READINESS_REPORT.md` |
| Process documentation | Mostly ready (protocol, support, analytics ops, Stage 0 GREEN assumed) | EP-008.2A |
| Critical blockers OR-01 / OR-02 | Packages **COMPLETE**; demonstrable closure **OPEN** | EP-008.2B |
| Safe-start G-S1-1…G-S1-7 | Not cleared | EP-008.2B §4 |

**Claim allowed:** Ops documentation is prepared enough that Stage 1 **can** be run safely **once** Critical/High enrollment blockers are closed.  
**Claim forbidden:** “Operationally cleared for invites”; “Stage 1 GO.”

---

## Pilot readiness

| Layer | Status | Source |
|---|---|---|
| Overall | **NOT YET — HOLD** | EP-008.2B `PILOT_READINESS_REPORT.md` |
| Runbooks / checklist / rollback | **DOC READY** (COMPLETE docs) | EP-008.2B |
| Dry-run / kill-switch evidence | **OPEN** | `GO_LIVE_CHECKLIST.md` §E blank |
| Analytics Pilot flag (OR-06) | **HOLD** (C1/C2 unset) | EP-008.2B |
| Incident / onboarding / support docs | **DOC READY** | EP-008.2B |

---

## Research readiness

| Layer | Status | Source |
|---|---|---|
| Stage 1 cohort **design** | **Complete** (frozen) | EP-007.3 `COHORT_DESIGN.md` |
| Stage 1 **ops** / measurement | **Not started** | EP-007.3; N_external = 0 |
| Effectiveness verdict | **NO-GO / PENDING EVIDENCE** | EP-007.3 `EDUCATIONAL_EFFECTIVENESS_REPORT.md` |
| M1–M9 external scorecards | Insufficient N / pending cohort | EP-003 / EP-007.3 |
| Protocol ↔ data plan consistency | **DOC READY** | EP-008.2A/2B research consistency notes |

Research design readiness ≠ effectiveness GO. Perception Pass does not substitute for Stage 1 behavioural evidence.

---

## Privacy readiness

| Layer | Status | Source |
|---|---|---|
| Privacy Sign-off Package (docs) | **DOC READY** / COMPLETE | EP-008.2B `PRIVACY_SIGNOFF_PACKAGE.md` |
| Product + Security/ops signatures | **OPEN** | §14 blank; `private_beta/PRIVACY_REVIEW.md` |
| Privacy notice text | Finalized text **READY**; invite attachment **OPEN** | OR-03 |
| Consent capture | Wording **READY**; live capture **OPEN** (N=0) | OR-04 |
| Linked risk | **PR-003** ACTIVE | P-003.3 |

**OR-01 remains the Critical privacy gate for invites.**

---

## Risk summary

Enrollment-blocking and material Stage 1 risks (documentary; not a new risk register):

| ID | Risk | Severity | Stage 1 effect |
|---|---|---|---|
| **OR-01 / PR-003** | Privacy Review unsigned | Critical | Blocks invites |
| **OR-02** | Pilot dry-run / kill-switch unevidenced | Critical | Blocks safe / measurement-honest start |
| **OR-03…OR-06** | Notice, consent, named owners, Pilot C1/C2 | High | Enrollment honesty controls |
| **PR-001** | Educational effectiveness unproven | Critical (V1) | Pilot collects evidence; start ≠ clear |
| **PR-002** | KSI 64 &lt; 80 | Critical (V1) | Orthogonal to Stage 1 invite criteria alone |
| **PR-006 / PR-007** | External floors unmet; recruitment blocked on privacy | High | N=0 until OR-01 clears |

Sources: EP-008.2A `RISK_REVIEW.md`; P-003.3 `ACTIVE_RISKS.md`; P-003.1 `Risk_Summary.md`.

---

## Open actions

See [`ACTION_STATUS.md`](ACTION_STATUS.md) for the full tracker.

| Layer | OPEN / incomplete | CLOSED |
|---|---:|---:|
| Critical (T-01…T-06 / CE-01…CE-05) | **6 tracker rows / 5 CE items** | **0** |
| High enrollment (T-07…T-12) | **6** | **0** |
| Stage 1 HOLD | Retained | — |

---

## Recent Board decisions

| Decision | Date | Outcome | Relevance |
|---|---|---|---|
| **PB-001** Stage 1 Go/No-Go | 2026-07-26 | Stage 1 **HOLD** | Binding enrollment posture |
| **DR-041** | ACTIVE (posture) | Version 1 **NO GO** | Separable; unchanged by Stage 1 HOLD |
| **DR-040** | ACTIVE (posture) | Private beta **GO WITH CONDITIONS** (Stage 0) | Stage 0 may continue |
| **DR-032** | ACTIVE | Three separable verdicts | Programme ≠ effectiveness ≠ V1 GO |
| **DR-034** | ACTIVE | No public registration | Invite-only preserved |
| Claim freezes (DR-035 / DR-036) | ACTIVE | Exam Ready ban; recommendation-effectiveness freeze | No Stage 1 GO marketing language |

---

## How to update this dashboard

1. Change a Critical status **only** when the cited Evidence location contains real names, dates, and Pass/Approve.  
2. Move **EVIDENCED → VERIFIED** only after a documented check of that artefact.  
3. Move **VERIFIED → BOARD ACCEPTED** only after a successor Board minutes/record.  
4. Mirror updates into OP-001 register/tracker (canonical Critical store).  
5. Never mark complete from chat, memory, or “docs are ready.”

---

## Explicit non-claims

- Stage 1 is **not** GO.  
- Critical evidence is **not** complete.  
- Privacy is **not** signed.  
- Dry-run / kill-switch are **not** completed.  
- Version 1 is **not** production-ready.  
- Educational effectiveness remains **NO-GO / PENDING EVIDENCE**.  
- This dashboard does **not** change product behaviour, KSI, or governance law.

---

## Pointers

| Need | Document |
|---|---|
| Board one-pager | [`BOARD_STATUS_CARD.md`](BOARD_STATUS_CARD.md) |
| Critical evidence | [`CRITICAL_EVIDENCE_SUMMARY.md`](CRITICAL_EVIDENCE_SUMMARY.md) |
| Actions / owners / dates | [`ACTION_STATUS.md`](ACTION_STATUS.md) |
| OP-001 register | [`../op001_critical_evidence_closure/`](../op001_critical_evidence_closure/) |
| PB-001 decision | [`../pb001_stage1_go_no_go_review/`](../pb001_stage1_go_no_go_review/) |
| Privacy / go-live packages | [`../ep008_2b_stage1_pilot_readiness_closure/`](../ep008_2b_stage1_pilot_readiness_closure/) |
| Version 1 position | [`../p003_8_version1_exit_criteria/CURRENT_RELEASE_POSITION.md`](../p003_8_version1_exit_criteria/CURRENT_RELEASE_POSITION.md) |
| Readiness tracker | `knowledge/VERSION_1_READINESS.md` |

---

**End of STAGE1_READINESS_DASHBOARD**
