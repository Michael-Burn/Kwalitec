# EP-008.2B — Rollback Playbook (Stage 1 Pilot)

**Programme:** EP-008.2B — Stage 1 Pilot Readiness Closure  
**Date:** 2026-07-26  
**Audience:** Beta operator / on-call / Product  
**Companions:** [`GO_LIVE_CHECKLIST.md`](GO_LIVE_CHECKLIST.md) · `../analytics/ep002/INCIDENT_RESPONSE.md` · `../ep004_private_beta/ROLLOUT.md`  
**Does not:** Change educational algorithms; invent rehearsal evidence  

---

## 1. Purpose

Restore a **safe state** if Stage 1 Pilot (invites and/or analytics emit) must be paused — without damaging student study paths and without public-launch confusion.

---

## 2. Rollback classes

| Class | When | Primary action |
|---|---|---|
| **R1 — Analytics kill switch** | Emit/backlog/privacy path implicated; SEV with UX risk | Flag OFF + restart |
| **R2 — Invite freeze** | Privacy incident; consent failure; P0; RED monitoring | Pause new invites; optional disable affected accounts |
| **R3 — Measurement exclusion** | Individual withdrawal / bad consent artefact | Exclude from KPI numerators; honour export/delete |
| **R4 — Deploy rollback** | Platform instability attributed to a release | Restore last known-good per Release Playbook (rare for ops-only Stage 1) |
| **R5 — Claim freeze** | Educational honesty incident | Freeze marketing / effectiveness language immediately |

Educational study must remain possible under R1 (fail-open / dark analytics).

---

## 3. R1 — Analytics kill switch (primary Stage 1 control)

### 3.1 Procedure

1. Set `ANALYTICS_EVENTS_V1=false` (or unset) on **all** Pilot-hosting web + worker processes.  
2. Restart web and worker.  
3. Verify: `flask analytics-metrics` → `feature_flag_enabled: false`.  
4. Optionally continue draining outbox if safe; do not replay until root cause known.  
5. Run educational smoke: Session / Reflection paths green.  
6. Update `ANALYTICS_ACTIVATION.md` with disable timestamp + reason.  
7. Update `ROLLOUT.md` Stage 1 to **HOLD** if invites were live.  
8. Notify Product + Security/ops.

### 3.2 Success criteria

| Check | Pass |
|---|---|
| Flag disabled in metrics | Yes |
| No student-visible analytics-induced errors | Yes |
| Educational smoke green | Yes |
| Activation log updated | Yes |

### 3.3 Rehearsal log (human — blank until rehearsed)

| Field | Value |
|---|---|
| Date | 2026-07-26 |
| Operator | Courage T Shumba |
| Environment | internal local (development SQLite); CLI process — no long-running Pilot web/worker |
| Result | **Pass** |
| Notes | Baseline metrics `feature_flag_enabled: false`; toggle `ANALYTICS_EVENTS_V1=true` → true; set `false` → false. Educational smoke with flag OFF: `/student/` 200, `/missions/` 200, `/study-plan/` 200. Recorded also in `GO_LIVE_CHECKLIST.md` §E3. Re-rehearse on Pilot-hosting twin before Pilot ON if host differs. |

---

## 4. R2 — Invite freeze / cohort pause

### 4.1 Triggers

- Privacy or security incident  
- Unsigned / dishonest consent artefacts for enrolled set  
- Open P0; monitoring RED  
- Educational honesty P1 unresolved  
- Analytics SEV with unresolved student risk  

### 4.2 Procedure

1. Stop sending new Stage 1 invites immediately.  
2. If privacy/security: freeze affected accounts; do not delete hastily before export rights considered.  
3. Execute R1 if analytics path implicated.  
4. Open incident per Support + `INCIDENT_RESPONSE.md`.  
5. Mark `ROLLOUT.md` Stage 1 **HOLD**; file monitoring note.  
6. Communicate honestly to affected participants (no overclaim, no blame-shifting).  
7. Resume invites only after Product + Security/ops re-clearance.

---

## 5. R3 — Individual measurement / data rollback

| Situation | Action |
|---|---|
| Measurement consent withdrawn | Exclude from M-series numerators; study may continue |
| Analytics delete requested | `flask analytics-delete-user <id> --yes` within 30 days; audit |
| Export requested | `flask analytics-export-user <id>` within 14 days |
| Full product withdrawal | Account/support deletion workflow + analytics cascade |
| Wrong-student data (P1) | Correct via support; incident if leak |

Never reverse hashes; never include other users in exports.

---

## 6. R4 — Platform / deploy rollback

Use only if a code/config deploy caused Stage 1 instability:

1. Identify last known-good deploy / config.  
2. Follow host Release / recovery playbooks (`RECOVERY_GUIDE.md` for analytics store issues).  
3. Re-run educational smoke.  
4. Keep analytics OFF until re-verified.  
5. Do **not** “fix” Runtime A ranking/readiness under pilot pressure.

---

## 7. R5 — Claim / research integrity freeze

1. Freeze language: no “educationally effective,” “exam ready,” “Version 1 production-ready,” or pass-rate claims.  
2. Tag defect `educational-integrity` if applicable.  
3. Keep scorecards labelled `exploratory` / `insufficient N` as needed.  
4. Board notified if C-EDU or C-V1 language was at risk.

---

## 8. Decision tree (quick)

```text
Incident detected
    │
    ├─ Student cannot study? ──► P1 same-day path (R2 if systemic)
    ├─ Data / privacy risk? ──► R2 + R1 + incident D
    ├─ Analytics backlog / DLQ / emit failures?
    │       └─ UX impacted? ──► R1; else drain/replay after root cause
    ├─ Honesty / overclaim? ──► R5
    └─ Single participant rights ──► R3
```

---

## 9. Pre-armed Stage 1 rollback (from EP-004 ROLLOUT)

| Trigger | Action |
|---|---|
| Privacy incident | Flag OFF; pause invites; incident response |
| Outbox lag / DLQ growth | Pause new Sessions **only if** UX impacted; drain/replay; flag OFF if needed |
| ≥2 P1 “cannot study” open > SLA | Freeze invites; triage before expansion |

---

## 10. After rollback — return to service

1. Root cause documented.  
2. Evidence re-run for affected GO_LIVE §E items if controls changed.  
3. Privacy Review still signed (or re-signed if scope changed).  
4. Product records new Go in `ROLLOUT.md` only when safe-start gates pass.  
5. Prefer-lower claims until N and monitoring re-stabilise.

---

## 11. Quick command card

```bash
# Status
flask analytics-metrics

# Kill switch
# set ANALYTICS_EVENTS_V1=false → restart web + worker

# Privacy
flask analytics-export-user <id>
flask analytics-delete-user <id> --yes --requested-by support
flask analytics-verify-consent <id>
flask analytics-export-audit
```

---

**End of ROLLBACK_PLAYBOOK**
