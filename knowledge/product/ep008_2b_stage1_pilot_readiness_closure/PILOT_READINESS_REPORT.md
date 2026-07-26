# EP-008.2B — Pilot Readiness Report (OR-02)

**Programme:** EP-008.2B — Stage 1 Pilot Readiness Closure  
**Date:** 2026-07-26  
**Status:** Procedures **COMPLETE** — execution evidence **OPEN** (not fabricated)  
**Closes documentation for:** OR-02 (Pilot Go-Live readiness)  
**Companions:** [`GO_LIVE_CHECKLIST.md`](GO_LIVE_CHECKLIST.md) · [`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md) · [`../ep008_2a_stage1_operational_readiness/PILOT_RUNBOOK.md`](../ep008_2a_stage1_operational_readiness/PILOT_RUNBOOK.md)  
**Does not:** Enable `ANALYTICS_EVENTS_V1`; invite externals; change Runtime A / recommendations  

---

## 1. Board question

> Is Pilot operational readiness complete enough for safe Stage 1 measurement-honest enrolment?

### Verdict

# NOT YET — HOLD

| Layer | Status |
|---|---|
| Runbooks / checklists / rollback | **COMPLETE** |
| Dry-run evidence attached | **OPEN** |
| Kill-switch rehearsal recorded for Pilot-hosting env | **OPEN** |
| Incident pathway documented | **COMPLETE** |
| Onboarding / support / research consistency | **COMPLETE** (docs) |
| Analytics Pilot flag authorisation (OR-06) | **HOLD** |
| Stage 1 enrollment | **HOLD** |

**Claim allowed:** Pilot operational controls are documented and executable; operators know how to rehearse and evidence them.  
**Claim forbidden:** “Dry-run completed”; “Kill-switch rehearsed on Pilot env”; “Pilot analytics ON”; “Stage 1 GO.”

---

## 2. Verification matrix (OR-02 scope)

Status legend: **DOC READY** = procedure exists · **EVIDENCED** = dated evidence filed · **OPEN** = not evidenced · **N/A** with rationale

| Requirement | Status | Evidence / gap |
|---|---|---|
| Dry-run completed (export + delete on staging or controlled internal) | **DOC READY / OPEN evidence** | Procedure in [`GO_LIVE_CHECKLIST.md`](GO_LIVE_CHECKLIST.md) §B; evidence log blank |
| Kill-switch rehearsal | **DOC READY / OPEN evidence** | [`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md) §3; evidence log blank |
| Incident reporting pathway | **DOC READY** | Support P0; analytics `INCIDENT_RESPONSE.md` §D; runbook §9 |
| Participant onboarding flow | **DOC READY** | `BETA_ONBOARDING.md` + EP-008.2A runbook §4–5 + Privacy package notice |
| Support contacts | **DOC READY** | Named role owners in Privacy package §11; founder rota accepted for N≤10 |
| Rollback procedure | **DOC READY** | [`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md) |
| Analytics verification | **DOC READY / OPEN evidence** | Metrics CLI + activation log templates; Pilot enable row unfilled |
| Behavioural event integrity | **DOC READY** | Fail-open emit; commitment observational-only; Journey emit provisional label |
| Research documentation consistency | **DOC READY** | Protocol ↔ Data Collection Plan ↔ Cohort design ↔ scorecard method labels |

---

## 3. Dry-run (export / delete) — procedure ready

### 3.1 Purpose

Prove operators can fulfil student privacy rights **before** external data subjects enroll.

### 3.2 Required rehearsal (must be executed by a human operator)

**Environment:** staging **or** controlled internal account that will **not** be counted as Stage 1 N.

1. Create / select a disposable invite-only test user.  
2. (Optional if flag ON internal) Generate a small set of analytics events; else verify empty export path still succeeds.  
3. Export: `flask analytics-export-user <id> --output /tmp/stage1-dryrun-export.json`  
4. Verify JSON contains only that user; hashes not reversed; no reflection body.  
5. Delete: `flask analytics-delete-user <id> --yes --requested-by dryrun`  
6. Confirm audit `analytics.user_deleted`.  
7. Re-export or list → expect no residual user events.  
8. Educational smoke (Session start path) still green on a normal account.  
9. Attach dated notes to evidence log in [`GO_LIVE_CHECKLIST.md`](GO_LIVE_CHECKLIST.md) §E.

**Until §E is filled: OR-02 evidence remains OPEN.**

---

## 4. Kill-switch rehearsal — procedure ready

### 4.1 Target behaviour

Analytics must be disableable **without** a code deploy and **without** breaking study UX.

### 4.2 Required rehearsal

1. On Pilot-hosting (or staging twin) processes: confirm current flag state via `flask analytics-metrics`.  
2. Set `ANALYTICS_EVENTS_V1=false` (or unset).  
3. Restart web + worker.  
4. Confirm `feature_flag_enabled: false`.  
5. Run educational smoke: Session / Reflection / ESS / Twin paths pass.  
6. (If previously ON) Confirm no student-visible error from dark emit.  
7. Record operator, env, timestamp in [`GO_LIVE_CHECKLIST.md`](GO_LIVE_CHECKLIST.md) §E and [`ROLLBACK_PLAYBOOK.md`](ROLLBACK_PLAYBOOK.md) rehearsal log.

Stage 0 docs note kill switch was rehearsed for internal path; **Pilot-target env rehearsal for Stage 1 must still be recorded** before Pilot ON.

---

## 5. Incident reporting pathway

| Severity | Path | First actions |
|---|---|---|
| P0 Security / data | Immediate — Support + Security | Freeze affected access; kill switch if analytics implicated; follow analytics incident D |
| Analytics SEV-1 / sustained SEV-2 with UX risk | On-call + Product | Kill switch; `INCIDENT_RESPONSE.md` |
| P1 Cannot study | Same day — beta operator | Reproduce; fix/workaround; confirm with student |
| Educational honesty P1 | Product + Educational governance | Freeze claim language; no algorithm hot-fix for metric gaming |
| Privacy request backlog | Export/delete owners | Honour SLAs; pause invites if dishonest consent artefacts found |

**Reporting intake:** `../private_beta/ISSUE_REPORTING.md` + support channel in invite pack.  
**Abort triggers:** EP-008.2A `STAGE1_CHECKLIST.md` Section F.

---

## 6. Participant onboarding flow (ops)

```text
Select candidate (inclusion rules)
  → Privacy Review signed (OR-01 human)
  → Provision invite-only account
  → Assign BETA-PIL-NNN (private ops map)
  → Send: welcome + Privacy Notice + Participant Information + consent requests + support link
  → Capture privacy ack + measurement (± interview/quote)
  → First login → Accepted
  → Orientation: Home → Today’s Session → Reflection when prompted
  → Week-1 check-in (≥1 productive Session / 7 days)
```

**Sources:** `BETA_ONBOARDING.md`; EP-008.2A `PILOT_RUNBOOK.md`; Privacy Sign-off Package §§5–7.  
**No UI redesign** in this programme (PR-017 watch only).

---

## 7. Support contacts (Stage 1)

| Need | Contact model |
|---|---|
| Student-facing support | Channel named in invite pack (founder-operated) |
| P0 security / data | Immediate escalation to Security / ops role + Product |
| Export requests | Export SLA owner (Founder / Product — confirm on log) |
| Delete requests | Deletion SLA owner (Founder / Product — confirm on log) |
| Analytics kill switch | On-call = same rota; playbook linked |
| Educational algorithm change requests | STOP → Document → PRD path — do not hot-fix Runtime A |

Staffed 24/7 commercial support is **not** required for N≤10 (OR-10 / PR-015 accepted).

---

## 8. Analytics verification (pre- and post-enable)

### 8.1 Before Pilot ON

| Check | Method |
|---|---|
| Migrations present | `analytics_events`, `analytics_outbox`, `analytics_audit_log` |
| Worker cron planned | `flask analytics-worker-once` |
| Retention cron planned | `flask analytics-retention` |
| Monitoring alerts configured | queue depth, DLQ, emit failures |
| Educational smoke OFF and ON (internal rehearsal) | Session / Reflection / ESS / Twin |
| Consent basis | Invite-only + notice; `flask analytics-verify-consent` |
| Privacy Review signed | OR-01 human signatures |
| Owners named | Export / delete / on-call |

### 8.2 After Pilot ON (future — not authorised by this programme)

1. `flask analytics-metrics` → `feature_flag_enabled: true`  
2. Worker draining; queue depth stable  
3. Watch `analytics.emit_failed` 24h  
4. Log enable row in `ANALYTICS_ACTIVATION.md`  
5. Scorecard method label = analytics ON (not manual exploratory)

### 8.3 Alternative (measurement-manual-only)

Product may explicitly decide Pilot **flag OFF** with manual scorecard method labelled `exploratory` / `manual`. That closes OR-06 via written decision but does **not** remove OR-01 or export/delete readiness. Record in activation log.

---

## 9. Behavioural event integrity

| Control | Posture |
|---|---|
| Emit fail-open | Educational completion never rolls back solely because analytics failed |
| Allowlist schemas | PRD-001 §7.4; no reflection body |
| Commitment events | Observational research only — not ranking / readiness / Twin authority |
| Journey emit (ADR-026) | Provisional — M5 labelled provisional (EP-004 C7) |
| Stage 0 vs Stage 1 N | Never inflate Stage 1 N with dogfood |
| Flag honesty | Do not market Twin/personalisation/Journey as ON if OFF |
| Experiment freeze | No silent educational behaviour experiments without Approved PRD |

---

## 10. Research documentation consistency

| Artefact | Aligns with |
|---|---|
| EP-007.3 `COHORT_DESIGN.md` | Size 5–10; metrics; ethics; confidence Medium ceiling |
| EP-003 protocol | Consent split; feedback cadence; exit criteria |
| EP-008.2A Data Collection Plan | Streams, claim mapping, export pack |
| EP-004 `WEEKLY_SCORECARD` / Educational Metrics | M1–M9 formulae; honest N labels |
| Evidence Hierarchy (P-003.5) | Prefer-lower; no C-EDU / C-V1 from Stage 1 start alone |
| Claim freezes | DR-036 recommendation-effectiveness; Exam Ready; public launch |

**Thin residual (OR-08 Medium):** standalone interview script still optional — protocol themes sufficient to start interviews after enrolment; not Critical.

---

## 11. Relationship to High enrollment controls

OR-02 documentation does **not** auto-close:

| ID | Item | Still needed |
|---|---|---|
| OR-03 | Notice on invite pack | Attach §7 notice when inviting |
| OR-04 | Consent capture live | Ops log before measurement inclusion |
| OR-05 | Owners confirmed on activation log | Fill names |
| OR-06 | Pilot flag ON **or** manual-measure decision | Written enable / decision |

---

## 12. OR-02 closure status

| Layer | Status |
|---|---|
| Operational procedures package | **COMPLETE** |
| Dry-run + kill-switch evidence | **OPEN** |
| Enrollment implication | **HOLD** — do not invite; do not enable Pilot flag |

---

## 13. Sign-off (assessment)

| Role | Verdict | Date |
|---|---|---|
| Product (pilot readiness documentation) | Procedures ready; evidence OPEN; Stage 1 **HOLD** | 2026-07-26 |
| Ops (execution) | Pending dry-run / rehearsal evidence in GO_LIVE checklist §E | — |

---

**End of PILOT_READINESS_REPORT**
