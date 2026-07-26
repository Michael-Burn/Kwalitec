# EP-008.2B — Stage 1 Go-Live Checklist

**Programme:** EP-008.2B — Stage 1 Pilot Readiness Closure  
**Date:** 2026-07-26  
**Purpose:** Single operator checklist to close OR-02 evidence and (only then) consider Pilot analytics / enrollment gates  
**Authority:** EP-002 `GO_LIVE_CHECKLIST.md` · EP-004 `ANALYTICS_ACTIVATION.md` · EP-008.2A `STAGE1_CHECKLIST.md`  
**Does not:** Fabricate dry-run or kill-switch completion; authorise invites without OR-01 signatures  

**Status legend:** `[ ]` open · `[x]` complete with evidence · `N/A` with rationale  

---

## A. Before any Pilot ON (inherits EP-002)

- [x] Migrations applied (`analytics_events`, `analytics_outbox`, `analytics_audit_log`) — local SQLite upgraded to `202607240001` for this dry-run
- [ ] Worker cron scheduled (`flask analytics-worker-once`) — or documented schedule ready for enable day
- [ ] Retention cron scheduled (`flask analytics-retention`) — required when Pilot ON for external
- [ ] Monitoring alerts configured (queue depth, DLQ, emit failures)
- [ ] Runbooks reviewed by on-call (`PRODUCTION_RUNBOOK`, `INCIDENT_RESPONSE`, `RECOVERY_GUIDE`, Privacy Ops)
- [x] Kill-switch procedure rehearsed — **evidence in §E** (2026-07-26)
- [x] Privacy deletion + export dry-run completed — **evidence in §E** (2026-07-26)
- [x] Consent basis confirmed for target cohort (invite-only + privacy notice) — verified via `flask analytics-verify-consent` on dry-run user; marketing denied
- [x] Educational smoke (Session / Reflection / ESS / Twin) pass with flag OFF and ON (internal rehearsal) — flag OFF smoke Pass (`/student/`, `/missions/`, `/study-plan/` 200); flag ON metrics toggle verified (no separate long-running web with ON)

---

## B. Pilot-stage extras (OR-02 Critical)

- [x] Privacy Review — Founder Review (Product Owner capacity) (`PRIVACY_SIGNOFF_PACKAGE.md` / `PRIVACY_REVIEW.md`) — Courage T Shumba · 2026-07-26 · Approve
- [x] Privacy Review — Founder Review (Privacy Owner capacity) — Courage T Shumba · 2026-07-26 · Approve
- [x] Privacy notice finalized text attached to invite pack (OR-03) — [`../private_beta/STAGE1_INVITE_PACK.md`](../private_beta/STAGE1_INVITE_PACK.md) §5 (2026-07-26); first external send still awaits clearance
- [x] Support export SLA owner **named** on activation log (OR-05) — §E4 Courage T Shumba 2026-07-26 (also confirm on Rollout/activation log before Pilot ON)
- [x] Support deletion SLA owner **named** on activation log (OR-05) — §E4 Courage T Shumba 2026-07-26
- [x] Beta operator / triage owner named — §E4 Courage T Shumba 2026-07-26
- [x] Consent capture process ready for BETA-PIL IDs (OR-04) — [`CONSENT_CAPTURE_LOG_TEMPLATE.md`](CONSENT_CAPTURE_LOG_TEMPLATE.md); live rows start at first invite
- [x] Export dry-run evidence attached (§E)
- [x] Delete dry-run evidence attached (§E)
- [x] Kill-switch rehearsal evidence attached for Pilot-hosting or staging twin (§E) — **internal local** rehearsal; re-confirm on Pilot-hosting env before Pilot ON if different host
- [ ] Stage 0 monitoring still GREEN; no open P0 (`OPERATIONS_MONITORING.md`)
- [x] Public registration still closed — product posture invite-only (no public self-registration)

---

## C. Pilot enable decision (OR-06)

Choose **exactly one**:

### C1 — Analytics Pilot ON (measurement-honest emit)

- [ ] Sections A–B complete with evidence
- [ ] Set `ANALYTICS_EVENTS_V1=true` on Pilot-hosting processes only
- [ ] Restart web + worker
- [ ] `flask analytics-metrics` → `feature_flag_enabled: true`
- [ ] Worker draining; queue depth stable
- [ ] Watch `analytics.emit_failed` for 24h
- [ ] Enable row filled in `../ep004_private_beta/ANALYTICS_ACTIVATION.md`
- [ ] Scorecard method label = analytics ON

### C2 — Measurement-manual-only (flag remains OFF)

- [x] Written Product decision recorded in `ANALYTICS_ACTIVATION.md` (Pilot remains HOLD / OFF) — Courage T Shumba · 2026-07-26 · C2
- [x] Scorecard method label = `manual` / `exploratory`
- [x] Sections B privacy + export/delete readiness still complete (students may still request rights)
- [x] Educational smoke green with flag OFF

**C2 recorded 2026-07-26. Do not claim Pilot analytics ON. Until enrollment clearance: do not invite.**

---

## D. Enrollment clearance (not OR-02 alone)

Complete EP-008.2A `STAGE1_CHECKLIST.md` Section A, then:

- [x] Rollout Stage 1 **Go** recorded in `../ep004_private_beta/ROLLOUT.md` — **GO** 2026-07-26 (C2)
- [x] Enrollment clearance table filled (Founder Reviews — Product Owner + Privacy Owner capacities; GP-001) — `STAGE1_CHECKLIST.md` §B
- [ ] First external invite sent only after clearance — **authorized**; send after OR-07 candidate selection

**Current programme snapshot:** enrollment clearance **FILED**; Stage 1 **Go** under C2; invites **not yet sent** (OR-07 open).

---

## E. Evidence log (must be human-filled — do not invent)

### E1. Export dry-run

| Field | Value |
|---|---|
| Date | 2026-07-26 |
| Operator | Courage T Shumba |
| Environment | internal (local SQLite / development — controlled dry-run account) |
| User id (opaque) | 31 (disposable `stage1-dryrun@example.invalid`) |
| Command | `flask analytics-export-user 31 --requested-by dryrun --output /tmp/stage1-dryrun-export.json` |
| Result | **Pass** |
| Notes (no PII) | Prerequisite: applied analytics migration `202607240001`. Export wrote 0 events; JSON `user_id=31` only; notes state hashes not reversed / no other users; no reflection body. Consent verify allowed (invite-only + notice); `--marketing-use` denied. |

### E2. Delete dry-run

| Field | Value |
|---|---|
| Date | 2026-07-26 |
| Operator | Courage T Shumba |
| Environment | internal (local SQLite / development — same disposable user) |
| User id (opaque) | 31 |
| Command | `flask analytics-delete-user 31 --yes --requested-by dryrun` |
| Audit confirmed | **Yes** — `analytics.user_deleted` audit_id `5b20750232b246e6be103c7231cfed83` |
| Result | **Pass** |
| Notes (no PII) | Deleted 0 events / 0 outbox (empty set). Re-export after delete still 0 events for user 31. Educational domain untouched by this CLI. |

### E3. Kill-switch rehearsal

| Field | Value |
|---|---|
| Date | 2026-07-26 |
| Operator | Courage T Shumba |
| Environment | internal (local process; no long-running Pilot web/worker at rehearsal time) |
| Steps | Metrics baseline `feature_flag_enabled: false` → set `ANALYTICS_EVENTS_V1=true` (metrics true) → set `ANALYTICS_EVENTS_V1=false` (metrics false) → educational smoke with flag OFF (`/student/` 200, `/missions/` 200, `/study-plan/`→plan 200) |
| Result | **Pass** |
| Notes | Proved env kill switch toggles metrics without code deploy. No production Pilot restart required (services not running). Soft log on missions commitment echo (missing `recommendation_commitments` table on this SQLite — other head migration); page still 200. Mirror: `ROLLBACK_PLAYBOOK.md` §3.3. |

### E4. Named owners confirmation

| Role | Name | Date confirmed |
|---|---|---|
| Beta operator | Courage T Shumba | 2026-07-26 |
| Export SLA owner | Courage T Shumba | 2026-07-26 |
| Deletion SLA owner | Courage T Shumba | 2026-07-26 |
| Kill-switch on-call | Courage T Shumba | 2026-07-26 |

---

## F. Abort / do-not-enable

Stop and keep HOLD if any of:

- ~~Privacy Founder Reviews (Product Owner + Privacy Owner) unsigned~~ — **SIGNED** 2026-07-26
- §E dry-run or kill-switch blank / failed
- Open P0 or RED monitoring  
- Consent artefacts dishonest  
- Proposal to enable marketing analytics or third-party SDK  

---

## G. Relationship to EP-002 checklist

This document **extends** `../analytics/ep002/GO_LIVE_CHECKLIST.md` for Stage 1 Pilot. Completing EP-002 “before any ON” without §E does **not** close OR-02.

---

**OR-02 evidence status (2026-07-26):** §E1–E4 **Pass** (internal local). OR-03 invite pack **READY**. OR-04 consent process **READY** (live N=0). OR-06 **C2** recorded. Remaining before invites: enrollment clearance (Section D) + Rollout Stage 1 Go; OR-03/OR-04 live application at first send.

---

**End of GO_LIVE_CHECKLIST**
