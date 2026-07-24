# Privacy Operations Guide

**Programme:** EP-002 WS4  
**Authority:** PRD-001 §7–§8  

## Policy → executable mapping

| PRD policy | Executable |
|---|---|
| §7.1 Raw retention 18 months | `flask analytics-retention --execute` (`AnalyticsRetentionEnforcer`) |
| §7.2 Student-requested deletion (30 days) | `flask analytics-delete-user <id> --yes` |
| §7.2 Scheduled deletion | Same retention command (daily cron) |
| §7.2 Cascade on account delete | Call `AnalyticsPrivacyService.delete_user_analytics` from account workflow |
| §7.3 Student export | `flask analytics-export-user <id>` (JSON; 14-day SLA manual OK in beta) |
| §7.3 Audit export | `flask analytics-export-audit` (JSONL) |
| §7.3 Audit retrieval | `AnalyticsPrivacyService.retrieve_audit` / audit export |
| §8 Consent (invite-only + privacy notice) | `flask analytics-verify-consent <id>` |

## Deletion workflow

1. Verify identity (support process).
2. `flask analytics-delete-user <user_id> --yes --requested-by support`
3. Confirm audit action `analytics.user_deleted`.
4. Educational domain deletion remains existing account/support workflow (out of scope to redefine).

## Export workflow

1. Verify requester (self or support).
2. `flask analytics-export-user <user_id> --output student.json`
3. Deliver securely; do not include other users.
4. Hashes are exported as stored (not reversed).

## Consent verification

Invite-only private beta basis:

- Account invitation + privacy notice covering first-party learning analytics.
- No marketing / advertising / resale use.
- Expanding beyond invite-only requires Privacy Review update.

```bash
flask analytics-verify-consent 123
flask analytics-verify-consent 123 --marketing-use   # must deny
```

## Audit retention

Operational audit log retained **36 months** (PRD §9). Purge of audit rows is not automated in EP-002; retention window is documented for future enforcement.

## Checkpoint

Before cohort > dogfood / external IFoA invitees: complete `knowledge/product/private_beta/PRIVACY_REVIEW.md` citing PRD-001 §7–§8 and this guide.
