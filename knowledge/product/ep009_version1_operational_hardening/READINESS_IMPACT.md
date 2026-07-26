# EP-009 — Readiness Impact

**Programme:** EP-009 — Version 1 Operational Hardening  
**Date:** 2026-07-26  
**Audience:** Product Board  
**Upstream readiness truth:** OP-002 [`STAGE1_READINESS_DASHBOARD.md`](../op002_stage1_readiness_dashboard/STAGE1_READINESS_DASHBOARD.md)  
**Does not:** Lift HOLD · invent evidence · declare Version 1 GO  

---

## Board answers

| Question | Answer |
|---|---|
| Can Stage 1 begin today because of EP-009? | **No** — EP-009 is triage/plan only; Critical evidence still not EVIDENCED |
| Which founder-pilot issues **must** be fixed before Stage 1? | **ISSUE-003** (Critical); **ISSUE-002**, **ISSUE-005**, and **ISSUE-001 ops path** (High) |
| Which may **safely wait** until after the pilot / first cohort start? | **ISSUE-001 self-serve UI** (Medium); **ISSUE-004** wording (Low) |
| Does EP-009 change enrollment posture? | **No** — Stage 1 remains **HOLD** until OP-001 CE-01…CE-05 are EVIDENCED and Board-accepted |

---

## Impact on Stage 1 HOLD

| Layer | Before EP-009 | After EP-009 packaging | After WP-A/B/C executed (future) |
|---|---|---|---|
| Stage 1 enrollment | **HOLD** | **HOLD** (unchanged) | HOLD lift **eligible to reconsider** only if CE-01…CE-05 also EVIDENCED (incl. CE-01/02 outside EP-009) |
| Founder-pilot gap clarity | Issues listed in OP-004 | Prioritised Critical/High vs deferred | Critical/High closed or honestly OPEN |
| Application behaviour | Unchanged | Unchanged | Unchanged for pre-Stage 1 set (no code required) |

**Rule restated (PB-001 / OP-001):** any Critical item without documentary evidence → do not invite.

---

## Founder-pilot issues → Stage 1 effect

| Issue | EP-009 severity | Stage 1 effect if left open | Pre-Stage 1 action |
|---|---|---|---|
| **ISSUE-003** | Critical | CE-03…CE-05 remain OPEN → **HOLD mandatory** | Execute dry-runs / kill-switch; file §E |
| **ISSUE-002** | High | First externals risk wrong export / SLA miss | Dual-export operator card |
| **ISSUE-005** | High | CE-04 incomplete / cascade risk | Account Deletion Checklist |
| **ISSUE-001** (ops) | High | Same as ISSUE-005 | Covered by checklist + dry-run |
| **ISSUE-001** (UI) | Medium | Support-handled deletion still viable under invite-only | **Defer** self-serve UI |
| **ISSUE-004** | Low | Misread “registration” if copy is sloppy | Optional wording; not a gate |

---

## Mapping to OP-001 Critical Evidence

| CE | Blocks invite? | EP-009 contribution | Still required outside EP-009 |
|---|---|---|---|
| **CE-01** Privacy signatures | Yes | None (not a founder-pilot Day-0 issue) | Founder Reviews S1/S2 |
| **CE-02** Named owners | Yes | None (DOC READY confirmation only) | §E4 name/date confirm |
| **CE-03** Export dry-run | Yes | WP-C + WP-A (operator clarity) | Dated §E1 Pass |
| **CE-04** Deletion dry-run | Yes | WP-C + WP-B (checklist) | Dated §E2 Pass + audit |
| **CE-05** Kill-switch | Yes | WP-C | Dated §E3 + Rollback §3.3 Pass |

EP-009 **enables honest CE-03/04** by specifying operator card + deletion checklist; it does **not** substitute for filled evidence rows.

---

## What changes for Version 1 production-ready?

| Gate / verdict | Impact of EP-009 |
|---|---|
| Version 1 **NO GO** (DR-041 / P-003.8) | **None** — operational hardening ≠ G1 / effectiveness clearance |
| G1.1 KSI ≥ 80 | **None** (ΔKSI = 0) |
| G1.9 effectiveness | **None** — N_external still 0 until Stage 1 runs |
| G8 / G10 operational/privacy claim class | Indirect — better ops docs/evidence **support** future claim honesty; do not score PASS here |

---

## Safe-to-wait rationale (Board)

### ISSUE-001 self-serve UI — wait

- Stage 1 is **invite-only** (DR-034) with named Deletion SLA owner.  
- Privacy commitments are met by **operable ops path + SLA**, not by Settings chrome.  
- Day-0 found analytics delete CLI; gap is cascade checklist and evidence, not missing CLI.  
- Building UI now expands application scope beyond founder-pilot operational findings and risks coupling to account lifecycle work unrelated to enrollment honesty.

### ISSUE-004 wording — wait

- Product correctly has no public register.  
- OP-004 already redefined “Registration” as controlled provisioning.  
- Residual risk is communication hygiene only.

---

## Must-fix-before-invite rationale (Board)

### ISSUE-003 — must

Without dated §E Passes, inviting externals would violate PB-001 Critical evidence rule and risk unrehearsed export/delete/kill-switch failure on a real participant.

### ISSUE-002 — must

Dual export surfaces confused the founder on Day-0. First external support tickets will hit the same ambiguity; wrong file = privacy/SLA failure.

### ISSUE-005 / ISSUE-001 ops — must

Privacy package still says educational deletion is “existing support workflow” without a single checklist. CE-04 cannot be trusted as full-account rehearsal until that list exists and is executed.

---

## Residual enrollment blockers after EP-009 WPs (if executed)

Even if WP-A/B/C complete successfully:

1. CE-01 unsigned Privacy Review  
2. CE-02 unconfirmed named owners  
3. Board acceptance of Critical evidence  
4. High enrollment actions T-07…T-11 (invite pack attachment, consent capture, etc.)  

EP-009 does not close those.

---

## Explicit non-claims

- EP-009 does **not** make Stage 1 ready.  
- EP-009 does **not** close CE-01…CE-05 by documentation alone.  
- EP-009 does **not** improve educational effectiveness or KSI.  
- EP-009 does **not** authorise external invites.

---

**End of READINESS_IMPACT**
