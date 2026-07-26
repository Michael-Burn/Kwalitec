# Operations Monitoring — Private Beta

**Programme:** EP-004 — Workstream 6  
**Updated:** 2026-07-26  
**Scope:** Dispatch latency, outbox health, worker health, failures, replay, retention, privacy requests  
**Non-scope:** Mastery / readiness / recommendation scores (educational authorities only)

---

## 1. Signals

| Signal | Source | Target / alert |
|---|---|---|
| Dispatch latency | `dispatch_latency_ms_avg` via `flask analytics-metrics` | Watch if sustained >> PRD soft budget under cohort load |
| Outbox health | `queue_depth` (`pending` + `failed`) | Alert if elevated > 5 min with worker running |
| Worker health | Cron success + depth trend | Worker must run when flag ON |
| Failures | `events_failed`, `dead_letter_count` | Investigate any sustained DLQ growth |
| Replay activity | `replay_count` + audit | Log every replay; no silent requeue |
| Retention | `purge_deleted` + `analytics.purge_run` audit | Run daily when flag ON for external; alert if none in 48h |
| Privacy requests | `user_deletions`, `exports_completed` + support tickets | Export SLA ≤ 14 days (PRD-001 beta) |

CLI:

```bash
flask analytics-metrics
```

Runbooks: `../analytics/ep002/PRODUCTION_RUNBOOK.md`, `INCIDENT_RESPONSE.md`, `RECOVERY_GUIDE.md`, `PRIVACY_OPERATIONS_GUIDE.md`.

---

## 2. Stage 0 snapshot (2026-07-24)

| Signal | Observation | Verdict |
|---|---|---|
| Feature flag (production default) | OFF | Expected |
| Dispatch latency | N/A / disabled path | Green |
| Outbox depth | Empty / idle expected | Green |
| Worker | Not required while OFF | Green |
| Failures / DLQ | None attributed to EP-004 | Green |
| Replay | None | Green |
| Retention | Not required while dark for external | Green |
| Privacy requests | None open | Green |
| Educational regression | None | Green |
| P0 / P1 study blockers | None open from EP-004 | Green |

**Stage 0 monitoring report:** **GREEN** — safe to continue Stage 0.  
**Stage 1 advance (2026-07-26):** Privacy signed; enrollment clearance filed; Stage 1 Go under **C2** (analytics OFF). Reconfirm no open P0 before each invite wave.

### 2.1 Founder reconfirm (2026-07-26)

| Signal | Observation | Verdict |
|---|---|---|
| Feature flag | OFF (C2) | Expected |
| Open P0 / P1 (known) | None | Green |
| Privacy / export-delete path | §E Pass | Green |
| Educational smoke (flag OFF) | Pass | Green |

**Reconfirm verdict:** **GREEN** for Stage 1 invite authorization under C2.

---

## 3. Weekly ops checklist (when flag ON)

- [ ] Capture `flask analytics-metrics` JSON snapshot (store under ops notes / date)
- [ ] Confirm worker cron fired in last 24h
- [ ] Confirm retention cron fired in last 48h (Pilot+)
- [ ] Review DLQ; replay or ticket
- [ ] Review privacy / export queue
- [ ] Confirm kill switch still documented for on-call

---

## 4. Stage 1 / 2 report template

| Field | Fill |
|---|---|
| Date / stage | |
| Flag enabled? | |
| queue_depth | |
| dead_letter_count (delta) | |
| events_failed (delta) | |
| replay_count (delta) | |
| Last retention audit | |
| Open privacy requests | |
| Open P0 / P1 | |
| Educational smoke | Pass / Fail |
| Verdict | GREEN / AMBER / RED |
| Go / Rollback recommendation | |

---

## 5. Exit criteria (WS6)

| Criterion | Status |
|---|---|
| Signals defined | COMPLETE |
| Stage 0 baseline recorded | COMPLETE |
| Templates for later stages | COMPLETE |
