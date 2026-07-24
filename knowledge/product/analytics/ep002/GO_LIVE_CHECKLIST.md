# Analytics Go-Live Checklist

**Programme:** EP-002  
**Prerequisite:** Operational readiness report = READY; flag currently OFF

## Before any ON environment

- [ ] Migrations applied (`analytics_events`, `analytics_outbox`, `analytics_audit_log`)
- [ ] Worker cron scheduled (`flask analytics-worker-once`)
- [ ] Retention cron scheduled (`flask analytics-retention`)
- [ ] Monitoring alerts configured (queue depth, DLQ, emit failures)
- [ ] Runbooks reviewed by on-call
- [ ] Kill switch procedure rehearsed
- [ ] Privacy deletion + export dry-run completed on staging
- [ ] Consent basis confirmed for target cohort (invite-only + privacy notice)
- [ ] Educational smoke tests (Session / Reflection / ESS / Twin) pass with flag OFF and ON

## Stage gates

| Stage | Extra checks |
|---|---|
| Internal | Founder accounts only; metrics inspected daily |
| Developer | Staging PROFILE latency budgets (PRD §10) |
| Pilot | Privacy Review for invitees; support export SLA owners named |
| Private beta | `PRIVACY_REVIEW.md` signed; cohort size logged |

## Activation steps

1. Confirm checklist above for the stage.
2. Set `ANALYTICS_EVENTS_V1=true` on target processes only.
3. Restart processes.
4. Verify `flask analytics-metrics` → `feature_flag_enabled: true`.
5. Confirm worker draining; queue depth stable.
6. Watch `analytics.emit_failed` for 24h.

## Abort

Unset / set flag false → restart → declare rollback complete when metrics show disabled and educational smoke still green.
