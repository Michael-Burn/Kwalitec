# KSI-003 — Protocol Deviations

**Programme:** KSI-003 — Stage 1 Educational Effectiveness Study  
**Date:** 2026-08-04  
**Protocol:** KSI-002 v1.0 (unchanged)  
**Rule:** Record every deviation; justify; classify severity; determine study validity. Do not silently continue.

Severity scale: `KSI002_RISK_AND_BIAS_REGISTER.md` §4 (S1 / S2 / S3).

---

## Deviation log

### PD-001 — Accepted external N below Stage 1 minimum

| Field | Content |
|-------|---------|
| **Observation** | ITT-Accepted external N = **0**; Stage 1 minimum accepted = **5** |
| **Protocol cite** | Study Design §4; Participant Protocol §1 |
| **Justification** | Invites for selected early-access rows remained pending at assessment; KSI-003 did not fabricate acceptance |
| **Severity** | **S1** |
| **Study remains valid?** | **No** for effectiveness GO, G1.9 PASS, Stage 1 ops-advance claimability, or Strong-band corroboration |
| **Action** | Stop primary endpoint inference; publish Unavailable + NO-GO / PENDING EVIDENCE |

### PD-002 — Observation window never started

| Field | Content |
|-------|---------|
| **Observation** | Personal start dates = null for all external IDs; longitudinal ≥4 weeks impossible |
| **Protocol cite** | Study Design §3 (personal start = acceptance); minimum study length 4 weeks |
| **Justification** | Acceptance is prerequisite; none occurred |
| **Severity** | **S1** |
| **Study remains valid?** | **No** for RQ-E primary endpoints E1–E4 |
| **Action** | Do not use 2-week directional memo language for G1.9 |

### PD-003 — Invites not sent during programme window

| Field | Content |
|-------|---------|
| **Observation** | Stage 1 invited N = 0 as of 2026-08-04; selected N=3 since 2026-07-26 with invites pending |
| **Protocol cite** | Participant Protocol §2 (invite-only; consent before KPI); Privacy/ops chain requires human invite send |
| **Justification** | Invite send requires Founder/ops use of private email map outside git; KSI-003 is evidence governance execution, not silent fabrication of outbound mail. Programme recorded the gap instead of inventing enrollment |
| **Severity** | **S1** |
| **Study remains valid?** | **No** until invites + acceptance + observation complete under protocol |
| **Action** | Founder ops must execute OR-07 invite send; then reopen observation clock |

### PD-004 — Selected early-access under-size vs design

| Field | Content |
|-------|---------|
| **Observation** | Even if pending invites were accepted tomorrow, selected external N=3 &lt; design minimum 5 |
| **Protocol cite** | Study Design §4; BETA_COHORT OR-07 labels wave “exploratory / early access (honest under-size)” |
| **Justification** | Pre-existing ops selection; KSI-003 does not expand recruitment silently |
| **Severity** | **S2** |
| **Study remains valid?** | **No** for Stage 1 minimum claimability even under optimistic future acceptance of current three alone |
| **Action** | Expand selection to ≥5 before counting Stage 1 design floor |

### PD-005 — Structured interviews not conducted

| Field | Content |
|-------|---------|
| **Observation** | Interview set N = 0; no Q1–Q10 instruments administered |
| **Protocol cite** | Participant Protocol §11; Study Design cadence week 4+ |
| **Justification** | Week-4 interviews require personal starts; none exist |
| **Severity** | **S1** for qualitative E3/E4 and GO-path interview floors |
| **Study remains valid?** | **No** for interview-based effectiveness or usefulness lifts |
| **Action** | Mark interview endpoints Unavailable; do not impute Final Test = Yes |

### PD-006 — Recommendation follow-through rates Unavailable

| Field | Content |
|-------|---------|
| **Observation** | E5 cannot be computed; no eligible exposures in accepted cohort; analytics Pilot OFF (C2) |
| **Protocol cite** | SAP §12; Validation Protocol §10; marketing freeze O8 |
| **Justification** | Prefer Unavailable over invented rates or Stage 0 substitution |
| **Severity** | **S2** for K2 Strong-band discussion |
| **Study remains valid?** | Partial — study can still report Unavailable honestly; **cannot** support Strong-band K2 |
| **Action** | Hold K2 at prior validated Partial; no Strong-band |

### PD-007 — Dated Founder decision artefact for KSI-002 accept not found in repo

| Field | Content |
|-------|---------|
| **Observation** | Programme brief states KSI-002 Founder-approved; no separate dated decision file located under KSI002_* |
| **Protocol cite** | Risk Register R3 — explicit Founder decision record |
| **Justification** | Proceeded on programme brief as Founder authority for this session; residual documentation gap |
| **Severity** | **S2** (documentation / audit trail) |
| **Study remains valid?** | **Conditional** — ops attempt allowed under brief; Founder should file dated accept record on review |
| **Action** | Request Founder attach decision record; do not treat as protocol rewrite |

### PD-008 — Privacy Review header vs enrollment clearance inconsistency

| Field | Content |
|-------|---------|
| **Observation** | `PRIVACY_REVIEW.md` header still says Stage 1 enrollment HOLD (OR-02 open); `ROLLOUT.md` / EP-008.2B README record Stage 1 Go under C2 with clearance |
| **Protocol cite** | Evidence must be claim-window matched and dated; prefer-lower on conflict |
| **Justification** | Operational truth for *clearance* taken from ROLLOUT (2026-07-26 Go C2); **invites still not sent** either way — outcome unchanged |
| **Severity** | **S3** (documentation drift) |
| **Study remains valid?** | Validity failure dominated by PD-001/002/003, not this drift |
| **Action** | Founder may reconcile PRIVACY_REVIEW header; KSI-003 does not edit that file (no product/docs cleanup beyond this study pack) |

### PD-009 — Subject mix on selected rows vs historical priority subjects

| Field | Content |
|-------|---------|
| **Observation** | Selected subjects CM1 / CB2 / CS1; historical Stage 1 priority often CM2/CS2 |
| **Protocol cite** | Participant Protocol §2 — in-scope loadable V1/V2 subjects; priority per ops plan |
| **Justification** | Not material while invites unsent; flag for inclusion check at invite time |
| **Severity** | **S3** |
| **Study remains valid?** | N/A until acceptance |
| **Action** | Confirm loadable curricula before invite send |

---

## Validity summary

| Question | Answer |
|----------|--------|
| May KSI-003 claim Stage 1 ops advance on behavioural endpoints? | **No** |
| May KSI-003 clear G1.9? | **No** |
| May KSI-003 publish a new validated KSI? | **No** (E6 refused; hold 64) |
| Does the study package remain useful? | **Yes** as honesty / ops-blocker evidence |
| Silent continuation without recording? | **Forbidden — not done** |
