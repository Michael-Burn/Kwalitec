# EP-008.2A — Operational Readiness Report

**Programme:** EP-008.2A — Stage 1 Operational Readiness  
**Date:** 2026-07-26  
**Status:** Assessment COMPLETE — Stage 1 enrollment **NOT CLEARED**  
**Claim window:** W-PROD (sole-runtime Student Home)  
**Validated product position (inputs):** KSI **64**; K2 **68**; K7 **60**; K8 **72**; Gate G1 **FAIL** (G1.1 / G1.9); Recommendation Trust validated; Recommendation Commitment presentation validated; behavioural effectiveness **unproven**  
**Does not:** Change Runtime A, recommendations, planning, readiness, ranking, Learning Twin, student UX, or educational algorithms  

---

## 1. Board question answered

> Can Kwalitec Version 1 begin a **controlled Stage 1 external pilot** safely?

### Verdict

# NOT YET — HOLD on external enrollment

| Question | Answer |
|---|---|
| Can Stage 1 begin **safely** today? | **No** — Critical privacy / consent gates remain open |
| Can Stage 0 continue? | **Yes** — under EP-004 GO WITH CONDITIONS |
| Is Stage 1 **design** ready? | **Yes** — EP-007.3 `COHORT_DESIGN.md` frozen |
| Is operational process documentation ready? | **Mostly yes** — protocol, runbooks, support, analytics ops exist |
| What must finish before first external invite? | Privacy Review **signed**; Pilot analytics checklist; finalized privacy notice + consent capture; named export/delete owners; invite pack attached |
| Does this clear G1.9 / effectiveness? | **No** — this programme only assesses ops readiness; effectiveness remains NO-GO until Stage 1 evidence |
| Does this claim release readiness? | **No** — Version 1 production-ready remains **NO GO** (P-003.8) |

**Claim allowed by this report (C-REL, Stage 1 class only):**  
> Operational documentation and Stage 0 posture are sufficiently prepared that a controlled Stage 1 pilot **can be run safely once Critical/High enrollment blockers are closed**. Enrollment is **not** authorised by this programme.

**Claims forbidden:** educational effectiveness; pilot success; student outcomes; Version 1 production-ready; Strong-band K2 from behavioural rates; public launch.

---

## 2. Scope of assessment

Reviewed artefacts (non-exhaustive index):

| Domain | Primary paths |
|---|---|
| Readiness tracker | `knowledge/VERSION_1_READINESS.md` |
| Board / exit | `p003_7_product_board_charter/`; `p003_8_version1_exit_criteria/`; `p003_1_version1_release_dossier/` |
| Risk / evidence / claims | `p003_3_product_risk_register/`; `p003_5_evidence_hierarchy/` |
| Stage 1 design | `ep007_3_educational_effectiveness_validation_stage1/` |
| Private beta ops | `ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md`; `ep004_private_beta/`; `private_beta/` |
| Privacy / analytics ops | `private_beta/PRIVACY_REVIEW.md`; `analytics/ep002/` |
| Commitment telemetry (observational) | `ep008_3_recommendation_commitment_followthrough/` |

---

## 3. Dimension assessment

Status legend: **READY** | **READY WITH GAPS** | **NOT READY** | **N/A**

### 3.1 Participant onboarding

| Item | Status | Evidence |
|---|---|---|
| Onboarding process documented | READY | `private_beta/BETA_ONBOARDING.md`; protocol §4 |
| Orientation surfaces exist in product | READY | Sole-runtime Home / Session path (W-PROD) |
| Ops success definition (≥1 productive Session / 7 days) | READY | `BETA_COHORT.md` §5; protocol |
| Orientation content density / FB-008 residual | READY WITH GAPS | PR-017 ACTIVE — Medium; do not redesign UI in this programme |
| External invite pack finalized | NOT READY | Recruitment checklist unchecked; notice not attached |

### 3.2 Consent process

| Item | Status | Evidence |
|---|---|---|
| Consent model defined | READY | Protocol §3; `BETA_COHORT.md` §3 |
| Measurement / interview / quote split | READY | Same |
| Withdrawal → KPI exclusion rule | READY | Protocol; cohort exit defs |
| Signed Privacy Review (external) | NOT READY | `PRIVACY_REVIEW.md` unsigned — **Critical** |
| Capture artefacts for invitees (ack records) | NOT READY | Process described; no Stage 1 capture log / signed notice attachment |

### 3.3 Privacy and data handling

| Item | Status | Evidence |
|---|---|---|
| Invite-only / no public registration | READY | Auth posture; DR-034; checklist item (unsigned) |
| Analytics privacy ops (export/delete/retention) | READY | `PRIVACY_OPERATIONS_GUIDE.md`; CLI paths |
| Export/delete dry-run for Pilot | NOT READY | GO_LIVE Pilot extras open |
| Honest privacy notice text finalized | NOT READY | Required by protocol; not filed as signed artefact |
| Multi-country DPA programme | N/A (Stage 1) | Deferred; prefer single privacy regime (cohort design) |

### 3.4 Pilot configuration

| Item | Status | Evidence |
|---|---|---|
| Size 5–10; IDs BETA-PIL-001…010 reserved | READY | `COHORT_DESIGN.md`; `BETA_COHORT.md` |
| Subjects CM2/CS2 priority; V1/V2 loadable | READY | Cohort design + architecture invariants |
| Stage 1 rollout HOLD / rollback pre-armed | READY | `ROLLOUT.md` Stage 1 |
| Analytics flag progression OFF → Internal → Pilot | READY (docs) | `ANALYTICS_ACTIVATION.md` — Pilot **HOLD** |
| Pilot flag ON authorised | NOT READY | C2 / EFF-06 open |
| Educational algorithm freeze for pilot | READY | Experiment Framework; EP-008.2A constraints |

### 3.5 Operational support

| Item | Status | Evidence |
|---|---|---|
| Support tiers P0–P3 documented | READY | `SUPPORT_WORKFLOW.md` |
| Issue reporting guide | READY | `ISSUE_REPORTING.md` |
| Stage 0 P0/P1 clear | READY | Ops monitoring GREEN (2026-07-24) |
| Staffed support rota | READY WITH GAPS | Founder-operated accepted for Stage 1 N≤10 (PR-015 ACCEPTED for invite-only) |
| Named export/delete SLA owners for Pilot | NOT READY | Interim founder named in rollout; Pilot checklist requires named owners |

### 3.6 Logging and diagnostics

| Item | Status | Evidence |
|---|---|---|
| Analytics metrics CLI / monitoring signals | READY | `OPERATIONS_MONITORING.md`; EP-002 runbooks |
| Incident response (analytics SEV) | READY | `INCIDENT_RESPONSE.md` |
| Stage 1 monitoring report template | READY | Ops monitoring §4 |
| Production load test for marketing scale | N/A (Stage 1) | PR-010 — not required for N 5–10 invite-only |

### 3.7 Behavioural event integrity

| Item | Status | Evidence |
|---|---|---|
| Session / reflection productive-use paths | READY | Platform Baseline; Stage 0 smoke |
| Commitment observational events shipped | READY | EP-008.3A: `commitment_confirmed` / `_deferred` / `_completed` — research only |
| Analytics durable outbox / fail-open emit | READY | EP-002 READY FOR STAGED ACTIVATION |
| Flag ON for external hosts | NOT READY | Pilot HOLD |
| Journey emit (ADR-026) | READY WITH GAPS | Provisional / gated — scorecard M5 labelled provisional (EP-004 C7) |
| Events as ranking inputs | N/A forbidden | Commitment metrics must remain non-authority |

### 3.8 Research procedures

| Item | Status | Evidence |
|---|---|---|
| Feedback cadence + interview week 4+ | READY | Protocol §5 |
| Themes must map to M / O / surface IDs | READY | Protocol; FEEDBACK_SYSTEM |
| Scorecard definitions | READY | `PRODUCT_SCORECARD.md`; Educational Metrics |
| Stage 1 directional success metrics | READY | `COHORT_DESIGN.md` §4 |
| Interview guide as standalone artefact | READY WITH GAPS | Themes specified; no separate interviewer script file — Medium gap |
| No silent educational experiments | READY | Experiment Framework |

### 3.9 Incident handling

| Item | Status | Evidence |
|---|---|---|
| Privacy / security incident playbook | READY | Analytics incident D; Support P0 |
| Educational honesty incident freeze | READY | Issue reporting; claim freezes |
| Stage 1 rollback triggers | READY | `ROLLOUT.md` Stage 1 pre-armed |
| Kill switch rehearsal recorded for Pilot env | NOT READY | Required before Pilot ON |

### 3.10 Success criteria (ops vs educational)

| Layer | Status | Notes |
|---|---|---|
| Stage 1 **ops** exit (EP-007.3 §8) | Documented READY | Not claimed met — ops not started |
| Stage 1 **directional** behavioural targets | Documented READY | M-series provisional until live baseline |
| Educational effectiveness GO (C5–C6) | NOT Stage 1 alone | N≥20 / ≥4 weeks — Stage 2 / waiver path |
| Version 1 production-ready | NOT READY | Orthogonal; NO GO remains |

### 3.11 Data export for analysis

| Item | Status | Evidence |
|---|---|---|
| Per-user analytics export CLI | READY | `flask analytics-export-user` |
| Audit export | READY | `flask analytics-export-audit` |
| Scorecard export process (weekly file) | READY WITH GAPS | Definitions exist; Stage 1 filing not started |
| Pseudonymous ID discipline in knowledge artefacts | READY | Cohort registry rule |
| Aggregated research export pack template | READY WITH GAPS | See `DATA_COLLECTION_PLAN.md` — template new in this programme |

---

## 4. Gap analysis (remaining blockers)

| ID | Gap | Severity | Blocks enrollment? | Owner | Closure evidence |
|---|---|---|---|---|---|
| **OR-01** | Privacy Review checklist unsigned | **Critical** | Yes | Founder — Product Owner + Privacy Owner capacities (GP-001) | Founder Reviews on `PRIVACY_REVIEW.md` (both capacities) |
| **OR-02** | EP-002 Pilot go-live row incomplete (incl. export/delete dry-run, kill-switch rehearsal on target env) | **Critical** | Yes (for measurement-honest Pilot) | Ops | Signed Pilot row in `GO_LIVE_CHECKLIST.md` + activation log |
| **OR-03** | Finalized privacy notice text not attached to invite pack | **High** | Yes | Product | Notice file + invite checklist tick |
| **OR-04** | External consent capture log (privacy ack + measurement ± interview/quote) not operationalised | **High** | Yes | Product (beta ops) | Per-participant consent fields populated in registry (no PII in knowledge repo) |
| **OR-05** | Named Pilot support / export / delete SLA owners not confirmed for Stage 1 window | **High** | Yes (Pilot checklist) | Product + Ops | Named owners in activation log |
| **OR-06** | Analytics Pilot flag ON for invite-hosting env not authorised | **High** | Yes if KPIs require emit | Ops | `ANALYTICS_ACTIVATION.md` Pilot enable row filled |
| **OR-07** | Stage 1 invite candidate shortlist (5–10) not selected under inclusion rules | **Medium** | Soft (ops start) | Product | Pseudonymous shortlist ready post-privacy |
| **OR-08** | Standalone interview script / codebook artefact thin | **Medium** | No (can run from protocol themes) | Product | Optional `INTERVIEW_GUIDE` in successor EP-008.2 execution |
| **OR-09** | Orientation / onboarding sparse (PR-017 / FB-008) | **Medium** | No | Product | Watch via Week-1 check-in; no UI redesign in 008.2A |
| **OR-10** | Founder-only support rota | **Low** | No for N≤10 | Product | Accepted under invite-only; escalate if P1 backlog |
| **OR-11** | Journey emit provisional (ADR-026) | **Low** | No | Product + Analytics | Keep M5 provisional label |
| **OR-12** | CSP / dependency residuals (G10) | **Low** | No for Stage 1 claim class | Engineering | Accepted residual; not enrollment blocker |

**Speculative features intentionally not recommended:** new ranking, LLM coach, public registration, automated multi-country DPA tooling, vanity dashboards, UI redesign.

---

## 5. What is already safe / ready

1. **Stage 0** invite-only dogfood under EP-004 GO WITH CONDITIONS; monitoring **GREEN**.  
2. **Platform Baseline** + Education OS sole-runtime path for study.  
3. **Frozen Stage 1 design** (selection, window, metrics, ethics, confidence) — EP-007.3.  
4. **Private beta protocol** + support / onboarding / feedback / issue docs.  
5. **Analytics stack** operationally ready for *staged* activation (flag still OFF by default).  
6. **Observational commitment events** available for research integrity once Pilot emit is ON.  
7. **Claim freezes** and Evidence Hierarchy prevent effectiveness / V1 overclaim during pilot.

---

## 6. Safe-start gate (enrollment clearance)

Stage 1 external enrollment may begin **only** when **all** of the following are evidenced:

| # | Gate | Maps to |
|---|---|---|
| G-S1-1 | Privacy Review signed | OR-01; EP-004 C1; EFF-02; PR-003 |
| G-S1-2 | Privacy notice finalized + attached to invites | OR-03 |
| G-S1-3 | Consent capture process live for BETA-PIL IDs | OR-04 |
| G-S1-4 | Pilot analytics checklist complete (or written Product decision to run measurement-manual-only with explicit label) | OR-02 / OR-06 |
| G-S1-5 | Export/delete owners named; dry-run evidence attached | OR-05 |
| G-S1-6 | Stage 0 monitoring still GREEN; no open P0 | EP-004 C3 |
| G-S1-7 | Rollout Go decision recorded in `ROLLOUT.md` Stage 1 | Ops |

Until then: **HOLD** — design and ops docs may be rehearsed internally; **no external invites**.

---

## 7. Evidence this pilot will collect (preview)

Full plan: [`DATA_COLLECTION_PLAN.md`](DATA_COLLECTION_PLAN.md).

| Class | What | Claim use |
|---|---|---|
| Ops | Activation, P0/P1, analytics health | C-REL Stage 1 |
| Behavioural | M1–M4, M6–M7 (+ provisional M3/M5) | Directional; feeds later G1.9 path — **not** C-EDU yet |
| Observational commitment | confirm / defer / complete rates | Research; not ranking; not effectiveness marketing |
| Qualitative | Week-1/2–3 check-ins; week-4+ interviews | Q1–Q3 context; Stage 1 ops exit (≥3 interviews) |
| Privacy | Export/delete fulfilment logs | Compliance |

---

## 8. Residual operational risks after clearance

Even after enrollment gates close, Active risks remain material to **interpretation** (not necessarily to start):

- PR-001 / G1.9 — effectiveness still unproven until floors.  
- PR-006 — N floors for educational GO unmet by Stage 1 alone.  
- PR-008 — confidence Medium ceiling until external corroboration accumulates.  
- PR-017 — onboarding friction may depress activation metrics.  
- PR-011 — telemetry overclaim if flag/claim misaligned.

Detail: [`RISK_REVIEW.md`](RISK_REVIEW.md).

---

## 9. Relationship to Version 1 / G1

| Item | After EP-008.2A |
|---|---|
| Validated KSI | **64** (unchanged) |
| Gate G1 | **FAIL** (unchanged) |
| G1.9 | **FAIL** (unchanged — ops not executed) |
| Board Version 1 recommendation | **NO GO** (unchanged) |
| Stage 1 ops | Still **NOT STARTED**; readiness assessed; enrollment HOLD |

---

## 10. Founder Review (assessment)

| Founder Review | Reviewer | Date | Capacity | Decision | Notes |
|---|---|---|---|---|---|
| Stage 1 ops readiness assessment | | 2026-07-26 | Product Owner | HOLD | Enrollment not cleared; Critical OR-01/OR-02 open |
| Effectiveness claims | | 2026-07-26 | Educational Gate Owner | NO-GO / PENDING EVIDENCE | Unchanged |
| Stage 1 expansion privacy posture | | 2026-07-26 | Privacy Owner | HOLD | Until Privacy Founder Reviews filed |

Authority: `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`.

---

**End of OPERATIONAL_READINESS_REPORT**
