# Analytics Activation Log (EP-004)

**Programme:** EP-004 — Workstream 3  
**Follows:** [`../analytics/ep002/FEATURE_FLAG_STRATEGY.md`](../analytics/ep002/FEATURE_FLAG_STRATEGY.md)  
**Flag:** `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1`  
**Updated:** 2026-07-26 (OR-06 C2 recorded)  
**Rule:** Every activation requires **Monitoring**, **Health verification**, and **Rollback readiness**.  
**Invariant:** Educational behaviour does not depend on the flag.

---

## Progression (required)

```text
OFF
 ↓
Internal only
 ↓
Pilot
 ↓
Private beta
```

---

## Stage: OFF (default)

| Field | Value |
|---|---|
| Flag | OFF / unset |
| Environment | Production default |
| Worker | Optional dry-run drain of empty queue |
| Status | **ACTIVE DEFAULT** until an ON stage is explicitly enabled |

### Monitoring

| Check | Result |
|---|---|
| `flask analytics-metrics` → `feature_flag_enabled: false` | Expected when OFF |
| Educational smoke | Pass (baseline) |
| Outbox growth from emits | None expected |

### Health verification

Dispatcher no-op; fail-open emitters unused. **Healthy.**

### Rollback readiness

N/A (already dark). Kill switch documented.

**Activation decision:** Remain OFF for any environment that hosts external students until Pilot checklist signed.

---

## Stage: Internal only

| Field | Value |
|---|---|
| Who | Founder / eng accounts (Stage 0 cohort) |
| Flag | ON in **internal** env only |
| Worker | Cron `flask analytics-worker-once` |
| Success criteria | Zero educational regressions; metrics healthy |
| Status | **AUTHORIZED** — enable only on internal processes |

### Pre-activation checklist

- [x] EP-002 READY FOR STAGED ACTIVATION
- [x] Migrations present (`analytics_events`, `analytics_outbox`, `analytics_audit_log`)
- [x] Kill switch rehearsed (env OFF + restart)
- [ ] Operator enables flag on internal env and records timestamp below when done

### Monitoring (when ON)

| Check | Cadence |
|---|---|
| `feature_flag_enabled: true` | At enable |
| `queue_depth` stable; worker draining | Daily |
| `events_failed` / DLQ | Daily |
| Educational smoke Session + Reflection | At enable + 24h |

### Health verification

Pass when: emit path fail-open preserved, no Session UX breakage, dispatch latency within PRD soft budgets for internal load.

### Rollback

1. Set `ANALYTICS_EVENTS_V1=false` (or unset).  
2. Restart web / worker.  
3. Confirm metrics show disabled.  
4. Optionally continue draining outbox.

**Activation decision (programme):** **GO for internal-only** when operator completes enable steps. Do **not** enable on shared production hosting external accounts until Pilot.

| Enable log | Timestamp | Operator | Env | Notes |
|---|---|---|---|---|
| Reserved | | | internal | Fill when flag flipped |

---

## Stage: Pilot

| Field | Value |
|---|---|
| Who | Small invite cohort (Stage 1) |
| Flag | **OFF** (C2 — measurement-manual-only) |
| Worker | Not required while flag OFF |
| Extra | Privacy workflows exercised; retention job when/if C1 later |
| Status | **C2 RECORDED** — Pilot analytics remain OFF; measurement labelled `manual` / `exploratory` |

### Gates before ON (C1 — not selected)

- [x] [`../private_beta/PRIVACY_REVIEW.md`](../private_beta/PRIVACY_REVIEW.md) signed (2026-07-26)  
- [x] Export/delete dry-run evidence attached (`../ep008_2b_stage1_pilot_readiness_closure/GO_LIVE_CHECKLIST.md` §E)  
- [x] Consent capture process ready (OR-04 template) — live per-invitee rows still N=0  
- [ ] Worker cron + retention cron + monitoring on Pilot-hosting env (required only if switching to C1)  

### Monitoring / health / rollback

Same as Internal when/if C1 is chosen later. Kill switch rehearsed 2026-07-26 (internal local).

### C2 — Product decision (OR-06) — RECORDED

| Field | Value |
|---|---|
| Decision | **C2 — Measurement-manual-only** |
| Date | 2026-07-26 |
| Capacity | Product Owner |
| Reviewer | Courage T Shumba |
| Flag posture | `ANALYTICS_EVENTS_V1` remains **OFF** / unset on Pilot path |
| Scorecard method label | `manual` / `exploratory` |
| Rationale | Stage 1 N=0; Pilot-hosting cron/monitoring not fully scheduled; honest measurement without claiming analytics ON. Privacy + export/delete readiness still complete for student rights. |
| Switch to C1 later | Allowed after Section A residuals + enable log row; re-run §E on Pilot host if different |

**Activation decision:** **NO-GO for Pilot analytics ON.** **GO for C2 manual/exploratory measurement path** when enrollment clearance is filed.

---

## Stage: Private beta

| Field | Value |
|---|---|
| Who | 20–50 students (Stage 2) |
| Flag | ON |
| Worker | Hardened cron |
| Extra | Privacy Review signed; go-live checklist complete |
| Status | **HOLD** |

**Activation decision:** **NO-GO** until Stage 1 monitoring GO and checklist Private-beta row signed.

---

## Mapping to EP-002 stages

| EP-002 stage | EP-004 rollout | Flag posture (2026-07-24) |
|---|---|---|
| 0 — Dark | Pre-Stage 0 / production default | OFF |
| 1 — Internal | Stage 0 | Authorized ON (internal env) |
| 2 — Developer | Staging dogfood | Per staging ops (not this cohort log) |
| 3 — Pilot | Stage 1 | **C2** — flag OFF; manual/exploratory measurement (2026-07-26) |
| 4 — Private beta | Stage 2 | HOLD |

---

## Exit criteria (WS3)

| Criterion | Status |
|---|---|
| Feature-flag progression documented | COMPLETE |
| OFF + Internal decisions recorded | COMPLETE |
| Pilot / Private beta holds recorded | COMPLETE |
| Monitoring + health + rollback per activation | COMPLETE (templates + Stage OFF verified) |
