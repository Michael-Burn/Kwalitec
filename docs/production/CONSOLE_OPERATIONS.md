# Console Operations

**Programme:** PR-001

## Access model

Console (`/console/*`) requires an authenticated identity with:

- Portal capability `console`, and
- Permission `console.access`

Granted by roles: Founder, Administrator, Content Manager, Support, Research (with role-specific permissions inside Console).

Students without Console capability receive **403**.

Legacy bridge: emails in `ADMIN_EMAIL` ∪ `FOUNDER_EMAILS` are treated as Founder and synced to durable roles on access.

## Operator tasks

| Task | Where |
|---|---|
| Attention / overview | Console Home |
| Operational health | `/console/operational-health` |
| Alpha observability | `/console/alpha-observability` |
| Curriculum Studio | `/console/studio/` |
| Vision journal | Console Vision section |
| Research feedback | Research + Console feedback views |

## Do / don't

- **Do** assign durable roles for staff identities.
- **Do** use one account for Student Portal + Console (capabilities differ; identity does not).
- **Don't** put authorization branches in Jinja — use `can`, `has_role`, `has_capability` helpers only.
- **Don't** expand email allowlists as the long-term access model.
