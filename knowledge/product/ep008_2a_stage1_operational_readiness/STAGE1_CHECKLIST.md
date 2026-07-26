# EP-008.2A — Stage 1 Checklist

**Programme:** EP-008.2A — Stage 1 Operational Readiness  
**Date:** 2026-07-26  
**Purpose:** Single operator checklist for controlled Stage 1 external pilot readiness and start  
**Authority:** EP-003 Private Beta Protocol · EP-004 Go/No-Go conditions · EP-007.3 Cohort Design  
**Does not:** Authorise invites by itself — Critical items must be evidenced and Rollout Go recorded  

**Status legend:** `[ ]` open · `[x]` complete · `N/A` with rationale  

---

## A. Preconditions (must be true before any external invite)

### A1. Privacy and consent — Critical / High

- [x] **OR-01** Privacy Review signed — Product Owner capacity (`../private_beta/PRIVACY_REVIEW.md`) — Courage T Shumba · 2026-07-26
- [x] **OR-01** Privacy Review signed — Privacy Owner capacity — Courage T Shumba · 2026-07-26
- [x] **OR-03** Privacy notice text finalized (honest scope: storage, analytics metadata/hashes not reflection body, retention, support access)
- [x] **OR-03** Privacy notice attached to invite pack — `../private_beta/STAGE1_INVITE_PACK.md`
- [x] **OR-04** Measurement consent capture process ready (include / exclude from KPI numerators) — `../ep008_2b_stage1_pilot_readiness_closure/CONSENT_CAPTURE_LOG_TEMPLATE.md`
- [x] **OR-04** Optional interview consent and quote consent paths ready (decline ≠ lose study access)
- [x] Withdrawal / export / delete path documented and operators know it (`../analytics/ep002/PRIVACY_OPERATIONS_GUIDE.md`) — §E dry-run Pass 2026-07-26

### A2. Analytics Pilot — Critical / High

- [x] EP-002 go-live **before any ON** rows complete for Pilot target env (`../analytics/ep002/GO_LIVE_CHECKLIST.md`) — **N/A for C2** (flag remains OFF); required before any C1 switch
- [x] **OR-02** Pilot-stage extras: Privacy Review for invitees; support export SLA owners named
- [x] **OR-02** Privacy deletion + export dry-run evidence attached (staging or controlled internal) — 2026-07-26
- [x] **OR-02** Kill-switch procedure rehearsed on target processes — internal local 2026-07-26; re-confirm on Pilot host if different
- [x] Worker cron + retention cron scheduled when flag will be ON — **N/A for C2** (flag OFF); required before any C1 switch
- [x] Monitoring alerts configured (queue depth, DLQ, emit failures) — **N/A for C2**; required before C1
- [x] Educational smoke (Session / Reflection / ESS / Twin) pass with flag OFF and ON (internal rehearsal) — OFF smoke Pass; ON=metrics toggle
- [x] **OR-06** Pilot enable decision recorded in `../ep004_private_beta/ANALYTICS_ACTIVATION.md` **or** written Product decision: measurement-manual-only with exploratory label — **C2** 2026-07-26

### A3. Platform and Stage 0 health

- [x] Public registration still closed
- [x] Stage 0 monitoring GREEN; no open P0 (`../ep004_private_beta/OPERATIONS_MONITORING.md`) — Stage 0 snapshot GREEN 2026-07-24; founder reconfirm 2026-07-26 (flag OFF / dark path; no known P0)
- [x] No open P1 “cannot study” backlog — founder reconfirm 2026-07-26 (none known)
- [x] GA / Platform Baseline retained for study paths
- [x] Feature-flag honesty: Twin / personalisation / Journey emit defaults not marketed as ON if OFF — C2 scorecard = `manual` / `exploratory`

### A4. Ops ownership

- [x] **OR-05** Named beta operator (triage owner) — Courage T Shumba
- [x] **OR-05** Named export SLA owner (≤14 days beta) — Courage T Shumba
- [x] **OR-05** Named deletion SLA owner (≤30 days) — Courage T Shumba
- [x] On-call knows analytics kill switch + Support P0 path — rehearsed 2026-07-26

---

## B. Cohort setup (after A complete)

- [x] Confirm Stage 1 design freeze still current (`../ep007_3_educational_effectiveness_validation_stage1/COHORT_DESIGN.md`) — design COMPLETE; ops may execute under clearance
- [x] **OR-07** Select candidates under inclusion — **early-access wave:** 3 external (`BETA-PIL-001…003`) + founder as Stage 0; N=3 labelled exploratory (design target 5–10)
- [x] Assign pseudonymous IDs `BETA-PIL-001` … `003` (do not put emails/names in knowledge artefacts) — see `BETA_COHORT.md`
- [x] Record subject + exam proximity (ops store only) — CM1 / CB2 / CS1; Sept 2026 (ops map)
- [x] Provision invite-only accounts (admin / controlled creation) — three students (local DB 2026-07-26)
- [ ] Send welcome + onboarding pack (`../private_beta/STAGE1_INVITE_PACK.md`)
- [ ] Link support + issue reporting channels (fill invite pack §3 per send)
- [ ] Capture consents before productive measurement inclusion (ops log — not git)
- [ ] Update cohort registry status fields (`../ep004_private_beta/BETA_COHORT.md`) — Invited / Accepted / … after send

### B — enrollment clearance record

| Field | Value |
|---|---|
| Clearance date | 2026-07-26 |
| Product Owner Founder Review | Courage T Shumba — **Approve** — authorize Stage 1 invites under C2 |
| Privacy Owner Founder Review | Courage T Shumba — **Approve** — participant protection controls adequate for invite-only N≤10 |
| Rollout Stage 1 Go recorded? | **Yes** — `../ep004_private_beta/ROLLOUT.md` |

**Enrollment clearance: FILED.** Invites may proceed only after OR-07 candidate selection + per-invitee consent capture. Do not invent invitees in git.

---

## C. Week 0–1 activation (ops)

- [ ] Confirm first login for each accepted pilot
- [ ] Week-1 check-in: understood? stuck? first Session done?
- [ ] Track onboarding success: ≥1 productive Session within 7 days of acceptance
- [ ] Follow up Stalled participants (protocol)
- [ ] Triage P0/P1 same-day / immediate
- [ ] If analytics ON: capture `flask analytics-metrics` snapshot; confirm worker draining

---

## D. Ongoing measurement (weeks 1–4+)

- [ ] Weekly scorecard filed (M1–M4, M6–M7 minimum) with honest N labels — see [`DATA_COLLECTION_PLAN.md`](DATA_COLLECTION_PLAN.md)
- [ ] Bi-weekly M5 if available (label provisional if Journey emit gated)
- [ ] Observational commitment events reviewed (research only; not ranking)
- [ ] Week 2–3 check-in: consistency, reflection, Journey clarity
- [ ] Week 4+: structured interviews (≥3 for Stage 1 ops exit; map codes to M / Q IDs)
- [ ] No silent educational behaviour experiments without Approved PRD
- [ ] No effectiveness / Exam Ready / pass-rate marketing language to cohort or public

---

## E. Stage 1 ops exit checklist (future — not claimed by EP-008.2A)

From EP-007.3 Cohort Design §8:

- [ ] Privacy signed; invites under protocol
- [ ] ≥5 accepted pilots with ≥1 productive Session
- [ ] ≥4 weekly scorecards with honest N
- [ ] ≥3 structured interviews coded
- [ ] No open P0/P1 study blockers
- [ ] Effectiveness verdict updated (may still be PENDING)
- [ ] No public registration

---

## F. Abort / HOLD triggers (any → pause invites)

- [ ] Privacy or security incident
- [ ] Educational honesty P1 unresolved
- [ ] Analytics SEV-1 / sustained SEV-2 with UX risk → kill switch
- [ ] Stage 0 / Pilot monitoring RED
- [ ] Consent artefact found dishonest or incomplete for enrolled set

---

## G. Claim discipline reminder

| Allowed during Stage 1 ops | Forbidden |
|---|---|
| “Controlled invite-only pilot running” | “Educationally effective” |
| “Ops GREEN / AMBER / RED” | “Version 1 production-ready” |
| “Directional M-series with N=…” | “Pilot success proves outcomes” |
| “Interviews coded to M/Q” | Public C-COM educational claims |

---

**Current programme snapshot (2026-07-26):** Section **A complete** (C2 path); enrollment clearance **FILED**; Rollout Stage 1 **Go** recorded. **OR-07** candidate selection + per-invite sends still open. Measurement label = `manual` / `exploratory`.

---

**End of STAGE1_CHECKLIST**
