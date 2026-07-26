# Analytics Release Checklist (EP-002)

Use before merging / deploying analytics operational changes.

## Code

- [ ] Feature flag default remains OFF
- [ ] No educational algorithm / Twin / ESS / recommendation changes
- [ ] Import guards green (`tests/architecture/test_analytics_import_guard.py`)
- [ ] Reliability + analytics suites green
- [ ] Ruff clean on touched analytics modules
- [ ] CLI commands registered and documented in Production Runbook

## Ops artefacts

- [ ] Operational Readiness Report updated
- [ ] Runbooks / replay / recovery / monitoring / privacy guides current
- [ ] Feature flag strategy stage for this release identified
- [ ] Go-live checklist owners assigned if activation is planned

## Deploy

- [ ] No requirement to enable flag as part of deploy
- [ ] Worker / retention cron present only when activation planned
- [ ] Rollback = env kill switch (no emergency migration required)

## Post-deploy (flag still OFF)

- [ ] `flask analytics-metrics` returns JSON
- [ ] `flask analytics-worker-once` succeeds on empty queue
- [ ] Educational smoke unaffected
