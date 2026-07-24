# Analytics Feature Flag Strategy

**Programme:** EP-002 WS5  
**Flag:** `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1`  
**Default:** **OFF** (truthy: `1`, `true`, `yes`, `on`)

## Principle

Analytics can be enabled or disabled **without deployment** by changing process environment and restarting app processes. Educational behaviour does not depend on the flag.

## Stages

| Stage | Who | Flag | Worker | Success criteria |
|---|---|---|---|---|
| 0 — Dark | All | OFF | Optional dry-run drain of empty queue | EP-002 exit (current) |
| 1 — Internal | Founder / eng accounts | ON in internal env only | Cron worker | Zero educational regressions; metrics healthy |
| 2 — Developer | Dev / staging dogfood | ON | Cron worker | Outbox lag < 60s p95; DLQ ~0 |
| 3 — Pilot | Small invite cohort | ON | Cron + on-call | Privacy workflows exercised; retention job daily |
| 4 — Private beta | 20–50 students | ON | Hardened cron | Privacy Review signed; go-live checklist complete |

## Rollback

1. Set `ANALYTICS_EVENTS_V1=false` (or unset).
2. Restart web / worker processes.
3. Confirm `flask analytics-metrics` → `feature_flag_enabled: false`.
4. Optionally continue draining outbox (safe; does not re-enable emits).

## Kill switch

Same as rollback. Prefer env change over code revert. Do not drop analytics tables unless Privacy mandates purge.

## Removability

- Flag OFF → dispatcher no-op; educational paths identical to pre-analytics.
- Domain emitters remain fail-open even when flag ON.
- Full code removal is a future ADR; operational removability is the env kill switch.

## Anti-patterns

- Enabling flag in production without worker cron.
- Enabling before Privacy Review for external invitees.
- Using analytics metrics as educational truth.
