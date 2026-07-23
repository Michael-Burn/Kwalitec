# Environment Guide

**Programme:** PR-001

Copy `.env.example` to `.env` for local development. Production hosts inject secrets via the platform (Render env vars).

## Required (production)

| Variable | Purpose |
|---|---|
| `APP_ENV=production` | Selects `ProductionConfig`; enables StartupService migrate/admin |
| `SECRET_KEY` | Session + CSRF signing — ≥32 chars, not a placeholder |
| `DATABASE_URL` | PostgreSQL URL (`postgres://` or `postgresql://` auto-normalised to `postgresql+psycopg://`) |
| `ADMIN_EMAIL` | Bootstrap administrator email |
| `ADMIN_PASSWORD` | Bootstrap administrator password (first boot only) |

## Strongly recommended

| Variable | Purpose |
|---|---|
| `FOUNDER_EMAILS` | Legacy bootstrap allowlist (comma-separated). Prefer durable RBAC roles; allowlist syncs Founder on access when matched |
| `TRUSTED_PROXY_HOPS=1` | Enable `ProxyFix` behind one reverse proxy |
| `PREFERRED_URL_SCHEME=https` | URL generation behind TLS termination |
| `KWALITEC_GIT_COMMIT` / `RENDER_GIT_COMMIT` | Deploy fingerprint in `/health` |
| `KWALITEC_BUILD_NUMBER` / `KWALITEC_BUILD_DATE` | Operator-visible build metadata |
| `KWALITEC_SUPPORT_CONTACT` | Support contact surfaced in UI |

## Database pool (PostgreSQL)

| Variable | Default | Purpose |
|---|---|---|
| `DB_POOL_SIZE` | `5` | SQLAlchemy pool size |
| `DB_MAX_OVERFLOW` | `10` | Overflow connections |
| `DB_POOL_RECYCLE` | `1800` | Recycle seconds (`pool_pre_ping` always on for Postgres) |

## Observability

| Variable | Default | Purpose |
|---|---|---|
| `SLOW_REQUEST_THRESHOLD_MS` | `1000` | Warn on slow HTTP requests |
| `HEALTH_ALERT_DB_LATENCY_MS` | `500` | Mark DB component degraded when probe exceeds threshold |
| `PROFILE_SQL=1` | off | Per-request SQL statement counts (diagnostics only) |
| `SESSION_LIFETIME_HOURS` | `12` | Permanent session lifetime |

## RBAC notes

- One **User** identity may hold multiple **roles** and **portal capabilities**.
- Roles: `founder`, `administrator`, `content_manager`, `support`, `research`, `student`
- Capabilities: `student_portal`, `console`, `organization_portal` (future), `api` (future)
- Do not create separate accounts for Console vs Student Portal.

## Forbidden in production

- Placeholder `SECRET_KEY` values (`change-this-secret-key`, `dev-change-this-secret-key`, …)
- Missing `DATABASE_URL` (SQLite)
- `WTF_CSRF_ENABLED=False`
- Committing `.env` or credentials
